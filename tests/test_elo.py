import math

import numpy as np
import pytest

from openbetlab.evaluation.data import Result
from openbetlab.models.elo import (START, EloParams, EloRatings, OrderedLogit, elo_forecasts,
                                   expected_home_score, league_level)


def res(date, home, away, o, league="en.1", season="2020-21"):
    return Result(league, season, date, home, away, o)


NO_REG = EloParams(k=20, home_adv=0, promotion_gap=100, season_regression=0)


def test_league_level():
    assert (league_level("en.1"), league_level("en.4"), league_level("mls")) == (1, 4, None)


def test_expected_score():
    assert expected_home_score(1500, 1500, 0) == 0.5
    assert expected_home_score(1900, 1500, 0) == pytest.approx(10 / 11)
    assert expected_home_score(1500, 1500, 100) > 0.5


def test_update_is_zero_sum_and_uses_k():
    elo = EloRatings(NO_REG)
    diffs = elo.run([res("2020-09-01", "A", "B", "H")])
    assert diffs == [0.0]
    assert elo.rating["A"] == pytest.approx(START + 10)   # K * (1 - 0.5)
    assert elo.rating["B"] == pytest.approx(START - 10)


def test_draw_moves_ratings_towards_each_other():
    elo = EloRatings(NO_REG)
    elo.run([res("2020-09-01", "A", "B", "H"), res("2020-09-08", "A", "B", "D")])
    assert elo.rating["A"] < START + 10


def test_same_day_matches_use_ratings_from_before_that_day():
    elo = EloRatings(NO_REG)
    diffs = elo.run([res("2020-09-01", "A", "B", "H"), res("2020-09-01", "A", "C", "H"),
                     res("2020-09-02", "A", "C", "H")])
    assert diffs[:2] == [0.0, 0.0]          # A's first win not yet applied
    assert diffs[2] == pytest.approx(30)    # after day 1: A 1520, C 1490


def test_future_results_do_not_change_earlier_forecasts():
    ms = [res("2020-09-01", "A", "B", "H"), res("2020-09-08", "B", "A", "D"),
          res("2020-09-15", "A", "B", "A")]
    alt = ms[:2] + [res("2020-09-15", "A", "B", "H")]
    assert EloRatings(NO_REG).run(ms) == EloRatings(NO_REG).run(alt)


def test_promotion_gap_direction():
    elo = EloRatings(EloParams(promotion_gap=100, season_regression=0, home_adv=0))
    elo.run([res("2020-09-01", "Up", "X", "D", league="en.2"),
             res("2020-09-01", "Down", "Y", "D", league="en.1"),
             res("2020-09-01", "Stay", "Y2", "D", league="en.1")])
    d = elo.run([res("2021-09-01", "Up", "Stay", "D", league="en.1", season="2021-22"),
                 res("2021-09-01", "Down", "X", "D", league="en.2", season="2021-22")])
    assert d[0] == pytest.approx(-100)   # promoted: league mean (1500) - 100 vs Stay 1500
    assert d[1] == pytest.approx(100)    # relegated: en.2 mean (1500) + 100 vs X 1500


def test_new_team_starts_at_league_mean():
    elo = EloRatings(EloParams(k=20, home_adv=0))
    elo.run([res("2020-09-01", "A", "B", "H")])        # A 1510, B 1490 -> mean 1500
    d = elo.run([res("2021-09-01", "New", "C", "D", season="2021-22")])
    assert elo.league_mean("en.1", "2021-22") == pytest.approx(1500)
    assert d[0] == pytest.approx(0)                    # both new: league mean 1500


def test_season_regression_pulls_towards_mean():
    elo = EloRatings(EloParams(k=20, home_adv=0, season_regression=0.5))
    elo.run([res("2020-09-01", "A", "B", "H")])        # A 1510, B 1490
    d = elo.run([res("2021-09-01", "A", "B", "D", season="2021-22")])
    assert d[0] == pytest.approx(10)                   # gap 20 halved


def test_league_mean_uses_only_previous_season_teams():
    elo = EloRatings(EloParams(k=200, home_adv=0, season_regression=0))
    elo.run([res("2018-09-01", "Gone", "B", "A", season="2018-19")])   # Gone ends very low
    elo.run([res("2020-09-01", "B", "C", "D", season="2020-21")])
    assert elo.league_mean("en.1", "2021-22") == pytest.approx(
        (elo.rating["B"] + elo.rating["C"]) / 2)


def test_ordered_logit_recovers_parameters():
    rng = np.random.default_rng(1)
    b, c1, c2 = 0.5, -0.8, 0.35
    x = rng.normal(0, 150, 20000)
    u = rng.random(20000)
    pa = 1 / (1 + np.exp(-(c1 - b * x / 100)))
    pad = 1 / (1 + np.exp(-(c2 - b * x / 100)))
    y = np.where(u < pa, "A", np.where(u < pad, "D", "H"))
    link = OrderedLogit().fit(list(x), list(y))
    assert (link.b, link.c1, link.c2) == pytest.approx((b, c1, c2), abs=0.06)


def test_ordered_logit_probabilities():
    link = OrderedLogit(b=0.5, c1=-0.8, c2=0.3)
    for d in (-400, 0, 400):
        assert sum(link.predict(d)) == pytest.approx(1)
    assert link.predict(400)[0] > link.predict(0)[0] > link.predict(-400)[0]
    assert link.predict(400)[2] < link.predict(-400)[2]
    with pytest.raises(ValueError):
        OrderedLogit().fit([], [])


def test_elo_forecasts_past_only():
    hist = [res(f"2019-{m:02d}-01", "A", "B", "HDA"[m % 3], season="2019-20") for m in range(8, 13)]
    hist += [res(f"2020-{m:02d}-01", "B", "A", "HDA"[m % 3], season="2020-21") for m in range(8, 13)]
    targets = [res("2021-09-01", "A", "B", "H", season="2021-22"),
               res("2021-09-08", "B", "A", "H", season="2021-22")]
    probs, _ = elo_forecasts(hist, targets, EloParams())
    assert len(probs) == 2 and all(sum(p) == pytest.approx(1) for p in probs)
    alt = targets[:1] + [res("2021-09-08", "B", "A", "A", season="2021-22")]
    assert elo_forecasts(hist, alt, EloParams())[0] == probs   # target results never used
    with pytest.raises(ValueError, match="before"):
        elo_forecasts(hist, [res("2020-09-01", "A", "B", "H")], EloParams())
