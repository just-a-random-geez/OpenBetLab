import dataclasses
import datetime as dt
import re
from pathlib import Path

import numpy as np
import pytest

from openbetlab.backtest import run as R
from openbetlab.backtest.engine import (MarketPrices, PlanRules, Snapshot, build_parlays,
                                        choose_bet, edge_after_commission, run_backtest)
from openbetlab.backtest.metrics import (bankroll_curve, bootstrap_roi_ci, longest_losing_run,
                                         max_drawdown, summarise)
from openbetlab.evaluation.data import Result, outcome
from openbetlab.models.poisson import PoissonModel, walk_forward

ROOT = Path(__file__).resolve().parents[1]
UTC = dt.timezone.utc
TEAMS = list("ABCDEF")


def _season(season, start, rng, n_rounds=4):
    out, day = [], start
    for _ in range(n_rounds):
        for h in TEAMS:
            for a in TEAMS:
                if h != a and rng.random() < 0.5:
                    gh, ga = int(rng.poisson(1.5)), int(rng.poisson(1.1))
                    out.append(Result("en.1", season, day.isoformat(), h, a, outcome(gh, ga),
                                      gh, ga))
                    if len(out) % 3 == 0:          # three matches per date
                        day += dt.timedelta(days=1)
    return out


def _data(seed=0):
    rng = np.random.default_rng(seed)
    history = (_season("2022-23", dt.date(2022, 8, 1), rng)
               + _season("2023-24", dt.date(2023, 8, 1), rng))
    targets = _season("2024-25", dt.date(2024, 8, 1), rng)
    return history, targets


def _prices(targets, odds_fn):
    out = {}
    for i, m in enumerate(targets):
        ko = dt.datetime.fromisoformat(m.date + "T15:00:00+00:00")
        snaps = {}
        for label, hours in (("2h", 2), ("close", 0.02)):
            odds = odds_fn(i, label)
            imp = [1 / o for o in odds]
            snaps[label] = Snapshot(odds, tuple(p / sum(imp) for p in imp),
                                    ((ko - dt.timedelta(hours=hours)).isoformat(),) * 3)
        out[(m.league, m.season, m.date, m.home_team, m.away_team)] = MarketPrices(
            ko.isoformat(), snaps)
    return out


def _odds(i, label):
    base = [(1.9, 3.6, 4.2), (2.6, 3.3, 2.9), (3.8, 3.4, 2.0), (2.2, 3.5, 3.4)][i % 4]
    return base if label == "2h" else tuple(round(o * 0.97, 2) for o in base)


def forecaster(h, t):
    return walk_forward(PoissonModel(180, 5), h, t)


RULES = PlanRules(min_edge=0.0)   # loose so the synthetic test produces plenty of bets


def _key(b):
    return (b.date, b.match, b.selection, b.odds, round(b.edge, 12), round(b.model_prob, 12))


# --------------------------------------------------------------------- no future data

def test_no_future_data_is_used():
    """Changing everything after a cut-off date (results AND prices, incl. closing prices)
    must not change any bet placed on or before that date."""
    history, targets = _data()
    base = run_backtest(history, targets, _prices(targets, _odds), forecaster, RULES)
    cutoff = targets[len(targets) // 2].date
    assert any(b.date <= cutoff for b in base.bets) and any(b.date > cutoff for b in base.bets)

    rng = np.random.default_rng(99)
    future_changed = []
    for m in targets:
        if m.date > cutoff:
            gh, ga = int(rng.poisson(3)), int(rng.poisson(3))
            m = dataclasses.replace(m, home_goals=gh, away_goals=ga, outcome=outcome(gh, ga))
        future_changed.append(m)

    def wild_odds(i, label):
        return (6.0, 1.3, 9.0) if targets[i].date > cutoff else _odds(i, label)

    alt = run_backtest(history, future_changed, _prices(future_changed, wild_odds),
                       forecaster, RULES)
    before = [_key(b) for b in base.bets if b.date <= cutoff]
    assert before == [_key(b) for b in alt.bets if b.date <= cutoff]


def test_model_is_only_fitted_on_earlier_dates():
    history, targets = _data()
    calls = []

    class Spy(PoissonModel):
        def fit(self, hist, as_of):
            hist = list(hist)
            calls.append((as_of, max(dt.date.fromisoformat(m.date) for m in hist)))
            return super().fit(hist, as_of)

    run_backtest(history, targets, _prices(targets, _odds),
                 lambda h, t: walk_forward(Spy(180, 5), h, t), RULES)
    assert calls and all(latest < as_of for as_of, latest in calls)


def test_closing_price_never_affects_picks():
    history, targets = _data()
    a = run_backtest(history, targets, _prices(targets, _odds), forecaster, RULES)

    def other_close(i, label):
        return _odds(i, "2h") if label == "2h" else (1.01 + i % 7, 50.0, 1.5)
    b = run_backtest(history, targets, _prices(targets, other_close), forecaster, RULES)
    assert [_key(x) for x in a.bets] == [_key(x) for x in b.bets]
    assert [x.clv for x in a.bets] != [x.clv for x in b.bets]   # only CLV uses the close


def test_pick_price_after_kickoff_rejected():
    snap = Snapshot((2.0, 3.5, 4.0), (0.5, 0.28, 0.22), ("2024-08-01T15:00:00+00:00",) * 3)
    with pytest.raises(ValueError, match="not before kick-off"):
        choose_bet((0.6, 0.2, 0.2), snap, "2024-08-01T15:00:00+00:00", RULES)


def test_rules_forbid_closing_price_for_picks():
    with pytest.raises(ValueError):
        PlanRules(pick_snapshot="close")


# --------------------------------------------------------------------- pick rules

SNAP = Snapshot((2.0, 3.5, 6.0), (0.5, 0.28, 0.17), ("2024-08-01T13:00:00+00:00",) * 3)
KO = "2024-08-01T15:00:00+00:00"


def test_edge_after_commission():
    assert edge_after_commission(0.6, 2.0, 0.05) == pytest.approx(0.6 * 0.95 - 0.4)


def test_choose_bet_min_edge_odds_range_and_best_only():
    rules = PlanRules()   # min edge 0.05, odds 1.5-5.0, commission 5%
    # home: 0.6*1*0.95-0.4 = 0.17 ; draw: 0.35*2.5*.95-.65 = 0.181 -> draw best
    assert choose_bet((0.6, 0.35, 0.05), SNAP, KO, rules)[0] == "draw"
    # away at 6.0 is outside 1.5-5.0 even with a huge edge
    assert choose_bet((0.2, 0.2, 0.6), SNAP, KO, rules) is None
    # edge below 5% -> no bet
    assert choose_bet((0.53, 0.28, 0.19), SNAP, KO, rules) is None   # 0.53*.95-.47 = 0.0335


def test_missing_price_means_no_bet():
    snap = Snapshot((None, 3.5, 4.0), (None, None, None), (None, "2024-08-01T13:00:00", None))
    assert choose_bet((0.9, 0.05, 0.05), snap, KO, PlanRules()) is None


# --------------------------------------------------------------------- metrics

def test_bankroll_drawdown_losing_run():
    profits = [0.95, -1, -1, -1, 1.9, -1]
    curve, used, ruined = bankroll_curve(profits, 100, 1)
    assert curve == pytest.approx([100, 100.95, 99.95, 98.95, 97.95, 99.85, 98.85])
    assert (used, ruined) == (6, False)
    dd, pct = max_drawdown(curve)
    assert dd == pytest.approx(3.0) and pct == pytest.approx(3 / 100.95)
    assert longest_losing_run([True, False, False, False, True, False]) == 3


def test_ruin_stops_betting():
    curve, used, ruined = bankroll_curve([-1] * 5, 2.5, 1)
    assert ruined and used == 2 and curve[-1] == 0.5


def test_summary():
    s = summarise([0.95, -1, 1.9, -1], [True, False, True, False], [0.02, None, -0.01, 0.03],
                  1, 100)
    assert (s.bets, s.wins, s.hit_rate) == (4, 2, 0.5)
    assert s.profit == pytest.approx(0.85) and s.roi == pytest.approx(0.2125)
    assert s.avg_clv == pytest.approx(0.04 / 3) and s.clv_bets == 3
    assert s.final_bankroll == pytest.approx(100.85)


def test_bootstrap_ci_is_deterministic_and_brackets_roi():
    profits = [0.95, -1, 1.9, -1, 0.5, -1, 2.85, -1]
    ci1, ci2 = bootstrap_roi_ci(profits, 1), bootstrap_roi_ci(profits, 1)
    assert ci1 == ci2 and ci1[0] < sum(profits) / 8 < ci1[1]


# --------------------------------------------------------------------- parlays

def test_parlays_only_from_qualifying_singles():
    history, targets = _data()
    rules = PlanRules(min_edge=0.0, parlays=True, parlay_legs=2)
    res = run_backtest(history, targets, _prices(targets, _odds), forecaster, rules)
    singles = {id(b) for b in res.bets}
    assert res.parlays
    for p in res.parlays:
        assert all(id(leg) in singles for leg in p.legs) and len(p.legs) == 2
        assert p.odds == pytest.approx(p.legs[0].odds * p.legs[1].odds)
        expected = (rules.stake * (p.odds - 1) * (1 - rules.commission)
                    if all(l.won for l in p.legs) else -rules.stake)
        assert p.profit == pytest.approx(expected)
    assert build_parlays([], rules) == []


def test_plan_v1_has_parlays_off():
    assert PlanRules().parlays is False


# --------------------------------------------------------------------- plan link

def test_rules_match_research_plan():
    text = (ROOT / "docs/RESEARCH_PLAN_v1.md").read_text()
    r = PlanRules()
    assert f"`{r.model}`" in text
    assert f"(`{r.pick_snapshot}` snapshot)" in text
    assert re.search(r"Minimum edge \| ≥ \*\*([\d.]+)\*\*", text).group(1) == f"{r.min_edge:.2f}"
    lo, hi = re.search(r"\*\*([\d.]+) ≤ odds ≤ ([\d.]+)\*\*", text).groups()
    assert (float(lo), float(hi)) == (r.min_odds, r.max_odds)
    assert re.search(r"Commission c \| \*\*(\d+)%\*\*", text).group(1) == f"{r.commission:.0%}"[:-1]
    assert "singles only" in text and r.parlays is False


def test_backtest_refuses_unfrozen_plan(tmp_path):
    draft = tmp_path / "plan.md"
    draft.write_text("# Plan\n\n> Status: DRAFT. Not frozen.\n")
    assert R.plan_status(draft)[0] is False
    assert R.main(["--plan", str(draft)]) == 2
    frozen = tmp_path / "plan2.md"
    frozen.write_text("# Plan\n\n> Status: FROZEN on 2026-11-12.\n")
    ok, sha = R.plan_status(frozen)
    assert ok and len(sha) == 64
    assert R.plan_status(ROOT / "docs/RESEARCH_PLAN_v1.md")[0] is False   # repo plan still draft


def test_load_prices_and_svg():
    rows = [{"league": "en.1", "season": "s", "match_date": "2024-08-01", "home_team": "A",
             "away_team": "B", "kickoff_utc": KO, "snapshot": "2h",
             "odds_home": "2.0", "odds_draw": "3.5", "odds_away": "4.0",
             "fair_prob_home": "0.5", "fair_prob_draw": "0.28", "fair_prob_away": "0.22",
             "price_time_home": "2024-08-01T13:00:00+00:00", "price_time_draw": "",
             "price_time_away": "2024-08-01T13:00:00+00:00"}]
    p = R.load_prices(rows)[("en.1", "s", "2024-08-01", "A", "B")]
    assert p.snapshots["2h"].odds == (2.0, 3.5, 4.0) and p.snapshots["2h"].times[1] is None
    assert R.bankroll_svg([100, 101, 99.5], 100).startswith("<svg")
