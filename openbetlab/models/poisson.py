"""Simple Poisson goals model (Maher 1982 style, with time decay and shrinkage).

Expected goals:
    home team:  lambda = home_rate * attack[home] * defence[away]
    away team:  mu     = away_rate * attack[away] * defence[home]

attack > 1  = scores more than an average team in this league.
defence > 1 = concedes more than average (weaker defence).

Parameters are fitted per league by weighted maximum likelihood:
- recent matches count more (weight halves every ``half_life_days``);
- every team gets ``prior_goals`` pseudo-goals of "average" evidence, which pulls
  teams with little data (e.g. newly promoted) towards 1.0 instead of extremes.
"""

from __future__ import annotations

import datetime as dt
import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

import numpy as np

from openbetlab.evaluation.data import Result

MAX_GOALS = 10


def poisson_pmf(k: int, lam: float) -> float:
    return math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1)) if lam > 0 else float(k == 0)


def outcome_probs(lam_home: float, lam_away: float, max_goals: int = MAX_GOALS):
    """P(home win), P(draw), P(away win) assuming independent Poisson goal counts.

    Scores above ``max_goals`` are ignored and the rest renormalised (the cut mass is tiny).
    """
    ph = [poisson_pmf(k, lam_home) for k in range(max_goals + 1)]
    pa = [poisson_pmf(k, lam_away) for k in range(max_goals + 1)]
    home = sum(ph[i] * pa[j] for i in range(max_goals + 1) for j in range(i))
    draw = sum(ph[i] * pa[i] for i in range(max_goals + 1))
    away = sum(ph[i] * pa[j] for j in range(max_goals + 1) for i in range(j))
    total = home + draw + away
    return home / total, draw / total, away / total


@dataclass
class LeagueParams:
    home_rate: float
    away_rate: float
    attack: dict[str, float] = field(default_factory=dict)
    defence: dict[str, float] = field(default_factory=dict)
    n_matches: int = 0


def fit_league(matches: list[tuple[str, str, int, int, float]], prior_goals: float,
               start: LeagueParams | None = None, max_iter: int = 500,
               tol: float = 1e-7) -> LeagueParams:
    """Weighted Poisson MLE (with a Gamma-style prior) by coordinate updates.

    ``matches`` = (home, away, home_goals, away_goals, weight).
    Each update is the closed-form optimum for one block of parameters given the others:
        attack[t]  = (goals t scored    + k) / (goals t was expected to score    + k)
        defence[t] = (goals t conceded  + k) / (goals t was expected to concede  + k)
    with k = ``prior_goals`` pulling every team towards 1.0 (average).
    """
    if not matches:
        raise ValueError("no matches to fit")
    teams = sorted({m[0] for m in matches} | {m[1] for m in matches})
    idx = {t: i for i, t in enumerate(teams)}
    n = len(teams)
    h = np.array([idx[m[0]] for m in matches])
    a = np.array([idx[m[1]] for m in matches])
    gh = np.array([m[2] for m in matches], dtype=float)
    ga = np.array([m[3] for m in matches], dtype=float)
    w = np.array([m[4] for m in matches], dtype=float)
    k = prior_goals

    def bins(i1, v1, i2, v2):
        return np.bincount(i1, v1, n) + np.bincount(i2, v2, n)

    scored = bins(h, w * gh, a, w * ga)
    conceded = bins(h, w * ga, a, w * gh)
    sum_gh, sum_ga = (w * gh).sum(), (w * ga).sum()
    if start:
        att = np.array([start.attack.get(t, 1.0) for t in teams])
        dfn = np.array([start.defence.get(t, 1.0) for t in teams])
        hr, ar = start.home_rate, start.away_rate
    else:
        att, dfn = np.ones(n), np.ones(n)
        hr, ar = sum_gh / w.sum(), sum_ga / w.sum()

    for _ in range(max_iter):
        new_att = (scored + k) / (bins(h, w * hr * dfn[a], a, w * ar * dfn[h]) + k)
        new_def = (conceded + k) / (bins(a, w * hr * new_att[h], h, w * ar * new_att[a]) + k)
        new_hr = sum_gh / (w * new_att[h] * new_def[a]).sum()
        new_ar = sum_ga / (w * new_att[a] * new_def[h]).sum()
        change = max(np.abs(new_att - att).max(), np.abs(new_def - dfn).max(),
                     abs(new_hr - hr), abs(new_ar - ar))
        att, dfn, hr, ar = new_att, new_def, new_hr, new_ar
        if change < tol:
            break
    return LeagueParams(home_rate=float(hr), away_rate=float(ar),
                        attack=dict(zip(teams, att.tolist())),
                        defence=dict(zip(teams, dfn.tolist())), n_matches=len(matches))


class PoissonModel:
    """Per-league Poisson model. Call ``fit(history, as_of)`` then ``predict(match)``."""

    name = "poisson"

    def __init__(self, half_life_days: float = 180, prior_goals: float = 5,
                 max_age_factor: float = 6):
        self.half_life_days = half_life_days
        self.prior_goals = prior_goals
        # Matches older than max_age_factor half-lives (weight < ~1.6%) are skipped for speed.
        self.max_age_days = half_life_days * max_age_factor
        self.params: dict[str, LeagueParams] = {}
        self.fit_data: dict[str, list] = {}  # league -> weighted matches used in the last fit
        self.as_of: dt.date | None = None

    def fit(self, history: Iterable[Result], as_of: dt.date) -> "PoissonModel":
        """Fit on matches strictly before ``as_of``. Later matches are rejected loudly."""
        per_league: dict[str, list] = defaultdict(list)
        for m in history:
            d = dt.date.fromisoformat(m.date)
            if d >= as_of:
                raise ValueError(f"match on {m.date} is not before {as_of}: would leak the future")
            age = (as_of - d).days
            per_league[m.league].append((age, (m.home_team, m.away_team, m.home_goals,
                                               m.away_goals, 0.5 ** (age / self.half_life_days))))
        params = {}
        for lg, items in per_league.items():
            recent = [x for age, x in items if age <= self.max_age_days]
            # Upstream has multi-season gaps for some leagues: if nothing is recent,
            # use the old matches anyway (their tiny weights keep teams near average).
            ms = recent or [x for _, x in items]
            params[lg] = fit_league(ms, self.prior_goals, start=self.params.get(lg))
            self.fit_data[lg] = ms
        self.params = params
        self.as_of = as_of
        self._after_fit()
        return self

    def _after_fit(self) -> None:
        """Hook for subclasses (e.g. Dixon-Coles) that fit extra parameters."""

    def expected_goals(self, match: Result) -> tuple[float, float]:
        p = self.params.get(match.league)
        if p is None:
            raise ValueError(f"no history for league {match.league}")
        ah, dh = p.attack.get(match.home_team, 1.0), p.defence.get(match.home_team, 1.0)
        aa, da = p.attack.get(match.away_team, 1.0), p.defence.get(match.away_team, 1.0)
        return p.home_rate * ah * da, p.away_rate * aa * dh

    def predict(self, match: Result) -> tuple[float, float, float]:
        if self.as_of is None or dt.date.fromisoformat(match.date) < self.as_of:
            raise ValueError("model must be fitted as of the match date (or earlier)")
        return outcome_probs(*self.expected_goals(match))


def walk_forward(model: PoissonModel, history: list[Result], targets: list[Result]):
    """Predict each target using only matches played on earlier dates.

    For every distinct target date d (in order): refit on all history + earlier
    targets with date < d, then predict that day's matches. Returns forecasts
    aligned with ``targets``.
    """
    pool = sorted(history + targets, key=lambda m: m.date)
    by_date: dict[str, list[int]] = defaultdict(list)
    for i, m in enumerate(targets):
        by_date[m.date].append(i)
    out: list = [None] * len(targets)
    j = 0
    for d in sorted(by_date):
        while j < len(pool) and pool[j].date < d:
            j += 1
        model.fit(pool[:j], dt.date.fromisoformat(d))
        for i in by_date[d]:
            out[i] = model.predict(targets[i])
    return out
