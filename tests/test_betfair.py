import datetime as dt
import subprocess
from pathlib import Path

import pytest
from betfair_fixtures import UTC, market_lines, write_market

from openbetlab.odds.betfair import iter_markets, parse_lines, price_rows

KO = dt.datetime(2024, 8, 17, 14, 0, tzinfo=UTC)


def at(**kw):
    return KO - dt.timedelta(**kw)


TICKS = [
    (at(hours=30), {"home": 1.50, "draw": 4.6, "away": 7.0}),
    (at(hours=24, minutes=1), {"home": 1.52}),                       # just before 24h mark
    (at(hours=20), {"home": 1.55, "draw": 4.4}),
    (at(hours=2), {"away": 7.4}),                                     # exactly at 2h mark
    (at(minutes=1), {"home": 1.60, "draw": 4.2, "away": 6.8}),
    (KO + dt.timedelta(minutes=3), {"home": 1.30}),                   # in-play: ignored
]


def market(**kw):
    kw.setdefault("ticks", TICKS)
    kw.setdefault("inplay_at", KO + dt.timedelta(minutes=2))
    return parse_lines(market_lines(**kw).splitlines(), "test")[0]


def test_parse_definition_and_runners():
    m = market()
    assert m.event_name == "Man City v Wolves" and m.market_type == "MATCH_ODDS"
    assert m.scheduled_start == KO
    assert m.inplay_time == KO + dt.timedelta(minutes=2)
    assert m.kickoff == KO                      # earlier of in-play (KO+2) and scheduled (KO)
    assert set(m.selections()) == {"home", "draw", "away"}
    assert m.winner() == "home"


def test_closing_and_early_prices():
    rows = {r.selection: r for r in price_rows(market(), early_hours=(24, 2))}
    # closing = last trade before kick-off
    assert [rows[s].prices["close"] for s in ("home", "draw", "away")] == [1.60, 4.2, 6.8]
    # 24h before kick-off: last trades at or before then
    assert rows["home"].prices["24h"] == 1.52
    assert rows["draw"].prices["24h"] == 4.6 and rows["away"].prices["24h"] == 7.0
    # 2h: trade exactly at the 2h mark counts
    assert rows["away"].prices["2h"] == 7.4 and rows["home"].prices["2h"] == 1.55
    assert rows["home"].price_times["24h"] == at(hours=24, minutes=1).isoformat()
    assert rows["home"].winner is True and rows["draw"].winner is False


def test_in_play_trades_never_used_for_closing():
    rows = {r.selection: r for r in price_rows(market())}
    assert rows["home"].prices["close"] != 1.30


def test_missing_price_is_none_not_invented():
    ticks = [(at(hours=5), {"home": 1.5, "draw": 4.0, "away": 7.0})]
    rows = {r.selection: r for r in price_rows(market(ticks=ticks), early_hours=(24,))}
    assert rows["home"].prices["24h"] is None and rows["home"].price_times["24h"] is None
    assert rows["home"].prices["close"] == 1.5


def test_scheduled_time_used_when_in_play_flag_only_seen_late():
    m = market(inplay_at=None)      # in-play flag first appears in the settlement message
    assert m.kickoff == KO and m.kickoff_source == "scheduled (in-play seen later)"
    rows = {r.selection: r for r in price_rows(m)}
    assert rows["home"].prices["close"] == 1.60       # trade at KO+3min excluded (strictly before)


def test_late_in_play_uses_scheduled_start():
    late = market(inplay_at=KO + dt.timedelta(minutes=25))
    assert late.kickoff == KO and late.kickoff_source == "scheduled (in-play seen later)"


def test_early_in_play_cuts_prices_at_in_play_time():
    """Reviewer case: market in-play at 11:30 while the scheduled time says 14:00.
    In-play trades at 11:50 must never become the closing or 2h price."""
    early = KO - dt.timedelta(hours=2, minutes=30)                  # 11:30
    ticks = [(KO - dt.timedelta(hours=5), {"home": 1.9, "draw": 3.4, "away": 4.2}),
             (early + dt.timedelta(minutes=20), {"home": 1.2, "draw": 7.0, "away": 15.0})]
    m = market(ticks=ticks, inplay_at=early)
    assert m.kickoff == early and m.kickoff_source == "in_play"
    rows = {r.selection: r for r in price_rows(m, early_hours=(2,))}
    assert rows["home"].prices["close"] == 1.9 and rows["home"].prices["2h"] == 1.9


def test_runner_order_by_name_not_position():
    lines = market_lines(runners=[(103, "The Draw", 3), (102, "Wolves", 2),
                                  (101, "Man City", 1)], ticks=[])
    m = parse_lines(lines.splitlines())[0]
    sel = m.selections()
    assert (sel["home"].name, sel["away"].name, sel["draw"].name) == ("Man City", "Wolves",
                                                                       "The Draw")


def test_bad_markets_rejected():
    m = parse_lines(market_lines(event="Man City vs Wolves", runners=[
        (101, "Man City", 1), (102, "Wolves", 2), (103, "The Draw", 3)]).splitlines())[0]
    with pytest.raises(ValueError):
        price_rows(m)


def test_reads_bz2_plain_and_tar(tmp_path):
    import tarfile
    d = tmp_path / "bf"
    write_market(d / "a", "1.1", market_lines(market_id="1.1", ticks=TICKS))
    write_market(d / "b", "1.2", market_lines(market_id="1.2", ticks=TICKS), compress=False)
    inner = write_market(tmp_path / "tmp", "1.3", market_lines(market_id="1.3", ticks=TICKS))
    with tarfile.open(d / "pack.tar", "w") as tar:
        tar.add(inner, arcname="BASIC/2024/Aug/17/999/1.3.bz2")
    ids = sorted(m.market_id for m in iter_markets(d))
    assert ids == ["1.1", "1.2", "1.3"]


def test_betfair_files_are_never_tracked_by_git():
    root = Path(__file__).resolve().parents[1]
    ignored = subprocess.run(["git", "check-ignore", "data/raw/betfair/x.bz2", "data/odds/x.csv",
                              "reports/private/x.md"], cwd=root, capture_output=True, text=True)
    assert ignored.stdout.split() == ["data/raw/betfair/x.bz2", "data/odds/x.csv",
                                      "reports/private/x.md"]
    tracked = subprocess.run(["git", "ls-files", "data/raw", "data/odds", "reports/private"],
                             cwd=root, capture_output=True, text=True)
    assert tracked.stdout.strip() == ""
