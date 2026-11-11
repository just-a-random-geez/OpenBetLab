"""Basic Elo rating model with home / draw / away probabilities.

1. Ratings (sequential, past data only)
   Every team has a rating (start 1500). Before a match:
       expected home score E = 1 / (1 + 10 ** ((R_away - R_home - home_adv) / 400))
   After it (result S = 1 win, 0.5 draw, 0 loss for the home side):
       R_home += K * (S - E);  R_away -= K * (S - E)
   Matches on the same date are all predicted first, then all applied.

2. League changes
   Leagues have no matches against each other, so ratings aren't comparable across
   them. When a team appears in a different league it is reset to that league's
   current average rating, minus ``promotion_gap`` if it moved up (e.g. en.2 -> en.1)
   or plus it if it moved down. New teams start at the league average.
   At the start of each new season ratings are pulled ``season_regression`` of the
   way back to the league average (squads change over the summer).

3. Ratings -> probabilities (ordered logistic)
   d = R_home - R_away (rating difference before the match)
       P(away)          = sigmoid(c1 - b * d)
       P(away or draw)  = sigmoid(c2 - b * d)
       P(draw) = the difference; P(home) = the rest.
   b, c1, c2 are fitted by maximum likelihood on (d, result) pairs from the training
   seasons only (the first season is skipped as burn-in: everyone starts at 1500).
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass

import numpy as np

from openbetlab.evaluation.data import Result, season_sort_key

START = 1500.0
_SCORE = {"H": 1.0, "D": 0.5, "A": 0.0}


def league_level(league: str) -> int | None:
    """'en.2' -> 2. Lower number = higher division."""
    try:
        return int(league.rsplit(".", 1)[1])
    except (IndexError, ValueError):
        return None


def expected_home_score(r_home: float, r_away: float, home_adv: float) -> float:
    return 1 / (1 + 10 ** ((r_away - r_home - home_adv) / 400))


@dataclass
class EloParams:
    k: float = 20
    home_adv: float = 75
    promotion_gap: float = 100
    season_regression: float = 0.2


class EloRatings:
    """Runs through matches in date order, recording each match's pre-match rating gap."""

    def __init__(self, params: EloParams):
        self.p = params
        self.rating: dict[str, float] = {}
        self.league_of: dict[str, str] = {}
        self.season_of: dict[str, str] = {}
        self.league_seasons: dict[str, set[str]] = defaultdict(set)
        self.played_in: dict[tuple, set[str]] = defaultdict(set)
        self._mean_cache: dict[tuple, float] = {}
        self.final_rating: dict[tuple, float] = {}  # (league, season, team) -> end rating

    def league_mean(self, league: str, season: str) -> float:
        """League average rating at the start of ``season``.

        Computed once per league-season, from the teams that played in that league in its
        previous season (before anyone is regressed), so it doesn't drift as teams enter.
        """
        key = (league, season)
        if key not in self._mean_cache:
            earlier = [s for s in self.league_seasons[league]
                       if season_sort_key(s) < season_sort_key(season)]
            prev = max(earlier, key=season_sort_key) if earlier else None
            rs = ([self.final_rating.get((league, prev, t), self.rating[t])
                   for t in self.played_in[(league, prev)]] if prev else [])
            self._mean_cache[key] = sum(rs) / len(rs) if rs else START
        return self._mean_cache[key]

    def _enter(self, team: str, league: str, season: str) -> None:
        """Set a team's rating when it plays its first match of a season."""
        if self.season_of.get(team) == season and self.league_of.get(team) == league:
            return
        prev = self.league_of.get(team)
        if team in self.rating:  # remember how the team finished its previous season
            self.final_rating[(prev, self.season_of[team], team)] = self.rating[team]
        mean = self.league_mean(league, season)
        self.league_seasons[league].add(season)
        self.played_in[(league, season)].add(team)
        if team not in self.rating:
            self.rating[team] = mean
        elif prev != league:
            lv_new, lv_old = league_level(league), league_level(prev)
            sign = 0 if lv_new is None or lv_old is None else (1 if lv_new < lv_old else -1)
            self.rating[team] = mean - sign * self.p.promotion_gap
        else:  # same league, new season
            self.rating[team] = mean + (1 - self.p.season_regression) * (self.rating[team] - mean)
        self.league_of[team] = league
        self.season_of[team] = season

    def run(self, matches: list[Result]) -> list[float]:
        """Process matches (any order; sorted here by date). Returns the pre-match rating
        difference (home - away) for each input match, aligned with the input list."""
        order = sorted(range(len(matches)), key=lambda i: (matches[i].date, i))
        diffs = [0.0] * len(matches)
        by_date: dict[str, list[int]] = defaultdict(list)
        for i in order:
            by_date[matches[i].date].append(i)
        for d in sorted(by_date):
            day = by_date[d]
            pre = {}
            for i in day:  # predict the whole day with ratings from earlier dates only
                m = matches[i]
                self._enter(m.home_team, m.league, m.season)
                self._enter(m.away_team, m.league, m.season)
                pre[i] = (self.rating[m.home_team], self.rating[m.away_team])
                diffs[i] = pre[i][0] - pre[i][1]
            for i in day:  # then apply the day's results (expectations from pre-day ratings)
                m = matches[i]
                e = expected_home_score(pre[i][0], pre[i][1], self.p.home_adv)
                delta = self.p.k * (_SCORE[m.outcome] - e)
                self.rating[m.home_team] += delta
                self.rating[m.away_team] -= delta
        return diffs


def _sigmoid(x):
    return 1 / (1 + np.exp(-x))


class OrderedLogit:
    """P(away) = s(c1 - b*d), P(away or draw) = s(c2 - b*d), d in units of 100 Elo points."""

    def __init__(self, b: float = 0.0, c1: float = -0.8, c2: float = 0.3):
        self.b, self.c1, self.c2 = b, c1, c2

    @staticmethod
    def _unpack(theta):
        b, c1, g = theta
        return b, c1, c1 + math.exp(g)  # c2 > c1 always

    @staticmethod
    def _nll(theta, x, y) -> float:
        b, c1, c2 = OrderedLogit._unpack(theta)
        pa = _sigmoid(c1 - b * x)
        pad = _sigmoid(c2 - b * x)
        p = np.where(y == 0, pa, np.where(y == 1, pad - pa, 1 - pad))
        return float(-np.log(np.clip(p, 1e-15, None)).sum())

    def fit(self, diffs, outcomes) -> "OrderedLogit":
        if len(diffs) == 0:
            raise ValueError("no data to fit")
        x = np.asarray(diffs, dtype=float) / 100
        y = np.array([{"A": 0, "D": 1, "H": 2}[o] for o in outcomes])
        theta = np.array([0.0, -0.8, math.log(1.1)])
        h = 1e-5
        f = self._nll(theta, x, y)
        for _ in range(100):  # Newton's method with numerical derivatives (3 parameters)
            grad = np.array([(self._nll(theta + h * e, x, y) - self._nll(theta - h * e, x, y))
                             / (2 * h) for e in np.eye(3)])
            hess = np.array([[(self._nll(theta + h * ei + h * ej, x, y)
                               - self._nll(theta + h * ei - h * ej, x, y)
                               - self._nll(theta - h * ei + h * ej, x, y)
                               + self._nll(theta - h * ei - h * ej, x, y)) / (4 * h * h)
                              for ej in np.eye(3)] for ei in np.eye(3)])
            try:
                step = np.linalg.solve(hess, grad)
            except np.linalg.LinAlgError:
                step = grad * 1e-3
            t = 1.0
            while t > 1e-6:
                cand = theta - t * step
                fc = self._nll(cand, x, y)
                if fc <= f:
                    break
                t /= 2
            else:
                break
            done = abs(f - fc) < 1e-9
            theta, f = cand, fc
            if done:
                break
        self.b, self.c1, self.c2 = self._unpack(theta)
        return self

    def predict(self, diff: float) -> tuple[float, float, float]:
        x = diff / 100
        pa = 1 / (1 + math.exp(-(self.c1 - self.b * x)))
        pad = 1 / (1 + math.exp(-(self.c2 - self.b * x)))
        return 1 - pad, pad - pa, pa


def elo_forecasts(history: list[Result], targets: list[Result], params: EloParams,
                  burn_in_seasons: int = 1):
    """Forecasts for ``targets`` using ratings from earlier dates only.

    The ordered-logit mapping is fitted on ``history`` only (minus burn-in seasons),
    so the targets' results never influence it. Targets must all be dated after history.
    """
    if history and targets and max(m.date for m in history) >= min(m.date for m in targets):
        raise ValueError("history must end before the first target date")
    diffs = EloRatings(params).run(history + targets)
    hist_d, targ_d = diffs[:len(history)], diffs[len(history):]
    seasons = sorted({m.season for m in history}, key=season_sort_key)
    skip = set(seasons[:min(burn_in_seasons, len(seasons) - 1)])  # keep at least one season
    fit_x = [d for d, m in zip(hist_d, history) if m.season not in skip]
    fit_y = [m.outcome for m in history if m.season not in skip]
    link = OrderedLogit().fit(fit_x, fit_y)
    return [link.predict(d) for d in targ_d], link
