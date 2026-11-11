import datetime as dt
import math

import numpy as np
import pytest

from openbetlab.evaluation.data import Result, outcome
from openbetlab.models.poisson import (PoissonModel, fit_league, outcome_probs, poisson_pmf,
                                       walk_forward)


def res(date, home, away, gh, ga, league="en.1", season="2020-21"):
    return Result(league, season, date, home, away, outcome(gh, ga), gh, ga)


def test_poisson_pmf():
    assert poisson_pmf(0, 1.0) == pytest.approx(math.exp(-1))
    assert poisson_pmf(2, 1.5) == pytest.approx(1.5 ** 2 * math.exp(-1.5) / 2)


def test_outcome_probs_basic_properties():
    h, d, a = outcome_probs(1.0, 1.0)
    assert h + d + a == pytest.approx(1)
    assert h == pytest.approx(a)
    # P(draw) = sum_k p(k)^2 for Poisson(1) = e^-2 * I0(2) ≈ 0.3085 (before the tiny cut-off)
    assert d == pytest.approx(0.3085, abs=1e-3)
    h2, _, a2 = outcome_probs(2.0, 0.8)
    assert h2 > 0.5 > a2


def _synthetic(attack, defence, home_rate, away_rate, rounds, seed=0):
    rng = np.random.default_rng(seed)
    teams = list(attack)
    out = []
    for _ in range(rounds):
        for h in teams:
            for a in teams:
                if h != a:
                    gh = rng.poisson(home_rate * attack[h] * defence[a])
                    ga = rng.poisson(away_rate * attack[a] * defence[h])
                    out.append((h, a, int(gh), int(ga), 1.0))
    return out


def test_fit_recovers_known_strengths():
    attack = {"A": 1.5, "B": 1.0, "C": 0.7, "D": 1.0}
    defence = {"A": 0.7, "B": 1.0, "C": 1.4, "D": 1.0}
    p = fit_league(_synthetic(attack, defence, 1.5, 1.1, rounds=300), prior_goals=0)
    # Only products are identified, so compare expected goals, not raw parameters.
    for h in attack:
        for a in attack:
            if h != a:
                true = 1.5 * attack[h] * defence[a]
                fit = p.home_rate * p.attack[h] * p.defence[a]
                assert fit == pytest.approx(true, rel=0.06)
    assert p.attack["A"] > p.attack["B"] > p.attack["C"]
    assert p.defence["C"] > p.defence["B"] > p.defence["A"]


def test_prior_shrinks_teams_towards_average():
    ms = [("A", "B", 5, 0, 1.0), ("B", "A", 0, 5, 1.0)]
    weak = fit_league(ms, prior_goals=0.5)
    strong = fit_league(ms, prior_goals=50)
    assert abs(strong.attack["A"] - 1) < abs(weak.attack["A"] - 1)


def test_fit_rejects_matches_on_or_after_as_of():
    m = PoissonModel()
    with pytest.raises(ValueError, match="leak"):
        m.fit([res("2020-10-01", "A", "B", 1, 0)], dt.date(2020, 10, 1))


def test_predict_requires_fit_as_of_match_date():
    m = PoissonModel().fit([res("2020-09-01", "A", "B", 1, 0)], dt.date(2020, 10, 1))
    with pytest.raises(ValueError):
        m.predict(res("2020-09-15", "A", "B", 0, 0))     # match is before fit date


def test_new_team_gets_average_strength():
    hist = [res(f"2020-09-{d:02d}", h, a, 2, 1) for d, (h, a) in
            enumerate([("A", "B"), ("B", "A"), ("A", "C"), ("C", "A")], start=1)]
    m = PoissonModel().fit(hist, dt.date(2020, 10, 1))
    lam, mu = m.expected_goals(res("2020-10-01", "New FC", "Other New FC", 0, 0))
    p = m.params["en.1"]
    assert (lam, mu) == pytest.approx((p.home_rate, p.away_rate))


def test_older_matches_count_less():
    # A scored a lot long ago, scored nothing recently.
    hist = ([res("2018-09-01", "A", "B", 6, 0), res("2018-09-08", "B", "A", 0, 6)]
            + [res("2020-09-01", "A", "B", 0, 1), res("2020-09-08", "B", "A", 1, 0)])
    m = PoissonModel(half_life_days=60, prior_goals=1, max_age_factor=100)
    m.fit(hist, dt.date(2020, 9, 15))
    assert m.params["en.1"].attack["A"] < m.params["en.1"].attack["B"]


class SpyModel(PoissonModel):
    def __init__(self):
        super().__init__()
        self.calls = []

    def fit(self, history, as_of):
        history = list(history)
        self.calls.append((as_of, [m.date for m in history]))
        return super().fit(history, as_of)


def test_walk_forward_uses_only_earlier_dates():
    history = [res("2020-08-01", "A", "B", 1, 0), res("2020-08-02", "B", "A", 1, 1)]
    targets = [res("2020-09-01", "A", "B", 2, 0), res("2020-09-01", "B", "C", 0, 0),
               res("2020-09-05", "C", "A", 1, 3)]
    spy = SpyModel()
    probs = walk_forward(spy, history, targets)
    assert len(probs) == 3 and all(sum(p) == pytest.approx(1) for p in probs)
    assert [c[0] for c in spy.calls] == [dt.date(2020, 9, 1), dt.date(2020, 9, 5)]
    # 1 Sep: only August matches. Same-day matches are NOT used.
    assert spy.calls[0][1] == ["2020-08-01", "2020-08-02"]
    # 5 Sep: August + both 1 Sep results, never the 5 Sep match itself.
    assert spy.calls[1][1] == ["2020-08-01", "2020-08-02", "2020-09-01", "2020-09-01"]
    for as_of, dates in spy.calls:
        assert all(dt.date.fromisoformat(d) < as_of for d in dates)


def test_walk_forward_does_not_depend_on_future_results():
    history = [res("2020-08-01", "A", "B", 1, 0), res("2020-08-02", "B", "A", 1, 1)]
    t1 = [res("2020-09-01", "A", "B", 2, 0), res("2020-09-08", "B", "A", 0, 0)]
    t2 = [t1[0], res("2020-09-08", "B", "A", 9, 0)]   # only the later result differs
    p1 = walk_forward(PoissonModel(), history, t1)
    p2 = walk_forward(PoissonModel(), history, t2)
    assert p1 == p2  # forecasts can't change because of a result not yet played


def test_walk_forward_many_future_changes_and_same_day():
    """Change EVERY result on or after a cut-off date (including that day): forecasts for
    matches up to and including the cut-off day must not move."""
    hist = [res(f"2020-08-{d:02d}", h, a, (d * 7) % 4, (d * 3) % 3)
            for d, (h, a) in enumerate([("A", "B"), ("C", "D"), ("B", "C"), ("D", "A"),
                                        ("A", "C"), ("B", "D")] * 4, start=1) if d <= 28]
    targets = [res(f"2020-09-{d:02d}", h, a, d % 3, (d + 1) % 2)
               for d, (h, a) in enumerate([("A", "B"), ("C", "D"), ("B", "C"), ("D", "A")] * 3,
                                          start=1)]
    cutoff = "2020-09-06"
    changed = [res(m.date, m.home_team, m.away_team, 9, 0) if m.date >= cutoff else m
               for m in targets]
    p1 = walk_forward(PoissonModel(), hist, targets)
    p2 = walk_forward(PoissonModel(), hist, changed)
    for m, a, b in zip(targets, p1, p2):
        if m.date <= cutoff:
            assert a == b
