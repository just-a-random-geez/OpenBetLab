import csv
import datetime as dt
from pathlib import Path

import pytest
from betfair_fixtures import UTC, market_lines, write_market

from openbetlab.odds.build import build, render_report
from openbetlab.odds.matching import FixtureRef, Matcher, load_mapping, similarity, uk_date
from openbetlab.settings import Settings

ROOT = Path(__file__).resolve().parents[1]
FIX = [
    FixtureRef("en.1", "2024-25", "2024-08-17", "Manchester City FC",
               "Wolverhampton Wanderers FC", 2, 0),
    FixtureRef("en.1", "2024-25", "2024-08-17", "Brighton & Hove Albion FC", "Everton FC", 1, 1),
    FixtureRef("en.2", "2024-25", "2024-08-17", "Preston North End FC", "Sheffield United FC", 0, 2),
]
MAP = {"Man City": "Manchester City FC", "Wolves": "Wolverhampton Wanderers FC"}
KO = dt.datetime(2024, 8, 17, 14, 0, tzinfo=UTC)


def test_similarity():
    assert similarity("Brighton", "Brighton & Hove Albion FC") == 1.0
    assert similarity("Sheff Utd", "Sheffield United FC") == 1.0
    assert similarity("Wolves", "Wolverhampton Wanderers FC") == 1.0
    assert similarity("Man Utd", "Manchester City FC") < 0.8
    assert similarity("Sutton Utd", "Southend United") < 0.8


def test_uk_date_uses_london_time():
    # 23:30 UTC on 16 Aug is 00:30 on 17 Aug in London (BST)
    assert uk_date(dt.datetime(2024, 8, 16, 23, 30, tzinfo=UTC)) == "2024-08-17"


def test_exact_mapping_match():
    r = Matcher(FIX, MAP).match("Man City", "Wolves", KO)
    assert r.method == "mapping" and r.fixture == FIX[0]


def test_fuzzy_match_same_date_only():
    m = Matcher(FIX, MAP, min_score=0.8)
    r = m.match("Brighton", "Everton", KO)
    assert r.method == "fuzzy" and r.fixture == FIX[1]
    r = m.match("Preston", "Sheff Utd", KO)
    assert r.method == "fuzzy" and r.fixture == FIX[2]
    assert m.match("Brighton", "Everton", KO + dt.timedelta(days=1)).method == "unmatched"


def test_unknown_or_reversed_is_unmatched():
    m = Matcher(FIX, MAP, min_score=0.8)
    assert m.match("Arsenal", "Chelsea", KO).method == "unmatched"
    r = m.match("Wolves", "Man City", KO)
    assert r.method == "unmatched" and "reversed" in r.reason
    assert m.match("Everton", "Brighton", KO).method == "unmatched"


def test_ambiguous_candidates_rejected():
    fx = [FixtureRef("en.1", "s", "2024-08-17", "Bristol City FC", "Leeds United FC"),
          FixtureRef("en.2", "s", "2024-08-17", "Bristol Rovers", "Leeds Town")]
    r = Matcher(fx, {}, min_score=0.8).match("Bristol", "Leeds", KO)
    assert r.method == "unmatched" and "ambiguous" in r.reason


def test_repo_betfair_mapping_points_to_real_canonical_names():
    canon = {row["canonical_name"] for row in
             csv.DictReader((ROOT / "data/team_names/england.csv").open())}
    mapping = load_mapping(ROOT / "data/team_names/betfair")
    assert mapping and set(mapping.values()) <= canon


def test_build_end_to_end(tmp_path):
    d = tmp_path / "bf"
    ticks = [(KO - dt.timedelta(hours=30), {"home": 1.5, "draw": 4.5, "away": 7.0}),
             (KO - dt.timedelta(minutes=5), {"home": 1.6, "draw": 4.2, "away": 6.4})]
    write_market(d, "1.1", market_lines("1.1", "Man City v Wolves", KO, ticks=ticks,
                                        inplay_at=KO))
    write_market(d, "1.2", market_lines("1.2", "Brighton v Everton", KO, ticks=ticks,
                                        inplay_at=KO, winner="away"))      # disagrees: was 1-1
    write_market(d, "1.3", market_lines("1.3", "Arsenal v Chelsea", KO, ticks=ticks))
    write_market(d, "1.4", market_lines("1.4", "Man City v Wolves", KO, ticks=ticks,
                                        market_type="OVER_UNDER_25"))
    out = build(d, FIX, MAP, Settings(commission=0.02, early_snapshots_hours=(24,)))
    assert {m["method"] for m in out["matches"]} == {"mapping", "fuzzy", "unmatched"}
    assert out["skipped"]["not a football match-odds market"] == 1
    assert len(out["prices"]) == 9                       # 3 markets x 3 selections
    close = [r for r in out["probs"] if r["market_id"] == "1.1" and r["snapshot"] == "close"][0]
    assert (close["odds_home"], close["odds_draw"], close["odds_away"]) == (1.6, 4.2, 6.4)
    assert close["overround"] == pytest.approx(1 / 1.6 + 1 / 4.2 + 1 / 6.4 - 1)
    assert sum(close[f"fair_prob_{k}"] for k in ("home", "draw", "away")) == pytest.approx(1)
    assert close["breakeven_prob_home"] == pytest.approx(1 / (1 + 0.6 * 0.98))
    assert close["home_team"] == "Manchester City FC" and close["winner"] == "home"
    text = render_report(out, Settings(commission=0.02))
    assert "Commission setting: 2.0%" in text and "**disagree 1**" in text
    assert "Brighton v Everton" in text and "Arsenal v Chelsea" in text


def test_second_market_for_same_fixture_skipped(tmp_path):
    d = tmp_path / "bf"
    for mid in ("1.1", "1.2"):
        write_market(d, mid, market_lines(mid, "Man City v Wolves", KO, ticks=[]))
    out = build(d, FIX, MAP, Settings())
    assert out["skipped"]["second market for an already-matched fixture"] == 1
