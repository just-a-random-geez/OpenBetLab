from dataclasses import replace

import numpy as np
import pytest

from openbetlab.simulation import run as R
from openbetlab.simulation.montecarlo import (Opportunity, Scenario, default_scenarios,
                                              edge_after_commission, kelly_fraction, plan_bets,
                                              simulate, synthetic_season, uniforms)


def season(n=300, noise=0.12, seed=1, margin=0.0):
    rng = np.random.default_rng(seed)
    out = []
    for i in range(n):
        market = np.array([0.45, 0.27, 0.28]) * np.exp(rng.normal(0, 0.3, 3))
        market /= market.sum()
        model = market * np.exp(rng.normal(0, noise, 3))
        model /= model.sum()
        out.append(Opportunity(f"d{i // 5:04d}", tuple(model), tuple(market),
                               tuple(1 / (market * (1 + margin)))))
    return out


BASE = Scenario("base", min_odds=1.01, max_odds=100)


def test_reproducible_with_fixed_seed():
    opps = season()
    a, b = simulate(opps, BASE, 2000, seed=5), simulate(opps, BASE, 2000, seed=5)
    assert np.array_equal(a.final, b.final)
    c = simulate(opps, BASE, 2000, seed=6)
    assert not np.array_equal(a.final, c.final)


def test_same_luck_for_a_match_in_every_scenario():
    assert np.array_equal(uniforms([3, 7], 100)[7], uniforms([7], 100)[7])


def test_market_truth_at_fair_odds_has_no_edge():
    """If results follow the market and odds are fair with no commission, expected
    profit is zero whatever the model thinks."""
    opps = season(margin=0.0)
    r = simulate(opps, replace(BASE, truth="market", commission=0.0), 10_000)
    assert r.bets_per_season > 50
    sd = r.final.std() / np.sqrt(len(r.final))
    assert abs(r.final.mean() - 100) < 4 * sd


def test_model_truth_profit_matches_model_edge():
    opps = season()
    sc = replace(BASE, commission=0.05)
    r = simulate(opps, sc, 20_000)
    expected = sum(edge_after_commission(*best) for best in _best_picks(opps, sc))
    sd = r.final.std() / np.sqrt(len(r.final))
    assert r.final.mean() - 100 == pytest.approx(expected, abs=4 * sd)


def _best_picks(opps, sc):
    for o in opps:
        cands = [(o.model[k], o.odds[k], sc.commission) for k in range(3)
                 if sc.min_odds <= o.odds[k] <= sc.max_odds
                 and edge_after_commission(o.model[k], o.odds[k], sc.commission) >= sc.min_edge]
        if cands:
            yield max(cands, key=lambda c: edge_after_commission(*c))


def test_overconfidence_lowers_results():
    opps = season()
    means = [simulate(opps, replace(BASE, overconfidence=d), 5000).final.mean()
             for d in (0.0, 0.02, 0.05)]
    assert means[0] > means[1] > means[2]


def test_plan_bets_rules():
    o = Opportunity("d1", (0.60, 0.25, 0.15), (0.5, 0.27, 0.23), (2.0, 4.0, 6.0))
    sc = Scenario("s")                       # odds 1.5-5, min edge 5%
    (b,) = plan_bets([o], sc)
    assert b.odds == 2.0 and b.legs == [(0, 0.60)]
    assert plan_bets([o], replace(sc, min_odds=2.1)) == []         # only 4.0 left: no edge
    assert plan_bets([o], replace(sc, truth="market"))[0].legs == [(0, 0.5)]
    assert plan_bets([o], replace(sc, overconfidence=0.05))[0].legs[0][1] == pytest.approx(0.57)


def test_parlays_group_same_day_picks_and_drop_leftovers():
    o = Opportunity("d1", (0.60, 0.25, 0.15), (0.5, 0.27, 0.23), (2.0, 4.0, 6.0))
    opps = [o] * 5 + [replace(o, date="d2")]
    bets = plan_bets(opps, Scenario("p", parlay_legs=2))
    assert len(bets) == 2 and all(len(b.legs) == 2 for b in bets)   # d1: 2 pairs, 1 left; d2: 1 left
    assert bets[0].odds == pytest.approx(4.0) and bets[0].model_p == pytest.approx(0.36)


def test_kelly_fraction():
    # p=0.6, odds 2, no commission: (0.6*1 - 0.4)/1 = 0.2
    assert kelly_fraction(0.6, 2.0, 0.0) == pytest.approx(0.2)
    assert kelly_fraction(0.4, 2.0, 0.0) == 0.0
    assert kelly_fraction(0.6, 2.0, 0.05) < 0.2


def test_ruin_and_lose_half_detected_and_bank_never_negative():
    o = Opportunity("d", (0.9, 0.05, 0.05), (0.0, 0.5, 0.5), (2.0, 20.0, 20.0))
    opps = [replace(o, date=f"d{i:03d}") for i in range(150)]
    r = simulate(opps, Scenario("doomed", truth="market"), 200)
    assert r.ruined.all() and r.lost_half.all() and (r.final >= 0).all()
    k = simulate(opps, Scenario("doomed kelly", truth="market", staking="kelly",
                                kelly_fraction=1.0), 200)
    assert (k.final >= 0).all()


def test_summary_fields():
    r = simulate(season(), BASE, 1000)
    s = r.summary()
    assert s["p5"] <= s["median"] <= s["p95"]
    assert 0 <= s["p_ruin"] <= s["p_lose_half"] <= 1   # ruin (<£1) implies losing half


def test_scenario_validation_and_defaults():
    with pytest.raises(ValueError):
        Scenario("x", parlay_legs=5)
    with pytest.raises(ValueError):
        Scenario("x", truth="oracle")
    names = [s.name for s in default_scenarios()]
    assert len(names) == len(set(names))
    sc = default_scenarios()
    assert {s.parlay_legs for s in sc} == {1, 2, 3, 4}
    assert {s.staking for s in sc} == {"flat", "kelly"} and {s.rollover for s in sc} == {True, False}
    assert {s.overconfidence for s in sc} == {0.0, 0.02, 0.05}
    assert {s.truth for s in sc} == {"model", "market"}


def test_cli_synthetic_and_holdout_guard(tmp_path):
    rep = tmp_path / "mc.md"
    assert R.main(["--source", "synthetic", "--seasons", "200", "--report", str(rep)]) == 0
    text = rep.read_text()
    assert "measures RISK, not edge" in text and "SYNTHETIC" in text and "seed 20261111" in text
    assert R.main(["--source", "holdout"]) == 2       # plan not frozen
    assert len(synthetic_season()) == 2000


def test_min_stake_makes_ruin_possible_with_rollover():
    """Reviewer counter-example: with 1% rollover stakes the bankroll used to shrink forever
    without ever being 'ruined', because stakes below Betfair's £1 minimum were allowed."""
    o = Opportunity("d", (0.9, 0.05, 0.05), (0.0, 0.5, 0.5), (2.0, 20.0, 20.0))
    opps = [replace(o, date=f"d{i:03d}") for i in range(150)]
    for sc in (Scenario("roll", truth="market", rollover=True),
               Scenario("kelly roll", truth="market", staking="kelly", rollover=True)):
        r = simulate(opps, sc, 200)
        assert r.ruined.all() and (r.final < 1).all()


def test_daily_stakes_never_exceed_bankroll():
    o = Opportunity("d", (0.9, 0.05, 0.05), (0.0, 0.5, 0.5), (2.0, 20.0, 20.0))
    opps = [o] * 300                          # 300 bets on ONE day, £100 bankroll, £1 each
    r = simulate(opps, Scenario("one day", truth="market"), 50)
    assert (r.final == 0).all()               # only 100 bets could be placed, all lost
