"""Parse Betfair Historic Data (BASIC tier) match-odds files.

File format (Betfair Exchange Stream API, one file per market, usually .bz2):
each line is JSON like
    {"op": "mcm", "pt": 1700000000000, "mc": [{"id": "1.2345",
        "marketDefinition": {...},              # sometimes: market info, runners, status
        "rc": [{"id": 47999, "ltp": 2.1}, ...]  # sometimes: last traded prices
    }]}
``pt`` = publish time in milliseconds since 1970 (UTC). BASIC has last traded prices
(ltp) at 1-minute intervals; no volumes or order book.

Definitions used here
- kick-off: the first time the market is seen in-play, if that is within 10 minutes
  before to 30 minutes after the scheduled ``marketTime``. Otherwise (never seen
  in-play, or the flag only shows up e.g. in the final settlement message) the scheduled
  time is used. ``kickoff_source`` says which.
- closing price: the last traded price strictly before kick-off.
- early price at H hours: the last traded price at or before kick-off minus H hours.
A price is None when nothing had traded yet by that time - never invented.
"""

from __future__ import annotations

import bz2
import datetime as dt
import gzip
import io
import json
import tarfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

DRAW_NAMES = {"the draw", "draw"}


def _ts(ms: int) -> dt.datetime:
    return dt.datetime.fromtimestamp(ms / 1000, tz=dt.timezone.utc)


def _parse_time(s: str | None) -> dt.datetime | None:
    if not s:
        return None
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(dt.timezone.utc)


@dataclass
class Runner:
    id: int
    name: str
    sort_priority: int | None
    status: str | None = None                     # final status: WINNER / LOSER / REMOVED
    ticks: list[tuple[dt.datetime, float]] = field(default_factory=list)  # (time, ltp)

    def last_price_at(self, t: dt.datetime, strict: bool = False):
        """(time, price) of the last trade at/before t (strictly before if ``strict``)."""
        best = None
        for when, price in self.ticks:          # ticks are in file order (time order)
            if when < t or (not strict and when == t):
                best = (when, price)
            else:
                break
        return best


@dataclass
class Market:
    market_id: str
    source: str
    event_id: str | None = None
    event_name: str | None = None
    market_type: str | None = None
    event_type_id: str | None = None
    country_code: str | None = None
    scheduled_start: dt.datetime | None = None
    inplay_time: dt.datetime | None = None
    status: str | None = None
    runners: dict[int, Runner] = field(default_factory=dict)

    INPLAY_EARLY = dt.timedelta(minutes=10)
    INPLAY_LATE = dt.timedelta(minutes=30)

    def _inplay_trusted(self) -> bool:
        if self.inplay_time is None:
            return False
        if self.scheduled_start is None:
            return True
        return (self.scheduled_start - self.INPLAY_EARLY <= self.inplay_time
                <= self.scheduled_start + self.INPLAY_LATE)

    @property
    def kickoff(self) -> dt.datetime | None:
        return self.inplay_time if self._inplay_trusted() else self.scheduled_start

    @property
    def kickoff_source(self) -> str:
        if self._inplay_trusted():
            return "in_play"
        if self.inplay_time is None:
            return "scheduled"
        return "scheduled (in-play time out of range)"

    def teams(self) -> tuple[str, str] | None:
        """Home and away names from the event name 'Home v Away'."""
        if not self.event_name or " v " not in self.event_name:
            return None
        home, away = self.event_name.split(" v ", 1)
        return home.strip(), away.strip()

    def selections(self) -> dict[str, Runner]:
        """Map runners to 'home' / 'draw' / 'away'. Raises ValueError if unclear."""
        teams = self.teams()
        if teams is None:
            raise ValueError(f"event name not 'Home v Away': {self.event_name!r}")
        active = [r for r in self.runners.values() if r.status != "REMOVED"]
        if len(active) != 3:
            raise ValueError(f"expected 3 runners, got {len(active)}")
        out: dict[str, Runner] = {}
        for r in active:
            name = r.name.strip()
            if name.lower() in DRAW_NAMES:
                out["draw"] = r
            elif name == teams[0]:
                out["home"] = r
            elif name == teams[1]:
                out["away"] = r
        if len(out) != 3:  # fall back to Betfair's usual order: home, away, draw
            by_prio = sorted(active, key=lambda r: (r.sort_priority is None, r.sort_priority))
            if [r.sort_priority for r in by_prio] == [1, 2, 3] and \
                    by_prio[2].name.strip().lower() in DRAW_NAMES:
                out = {"home": by_prio[0], "away": by_prio[1], "draw": by_prio[2]}
            else:
                raise ValueError(f"can't tell home/draw/away from runners "
                                 f"{[r.name for r in active]}")
        return out

    def winner(self) -> str | None:
        try:
            sel = self.selections()
        except ValueError:
            return None
        won = [k for k, r in sel.items() if r.status == "WINNER"]
        return won[0] if len(won) == 1 else None


def parse_lines(lines: Iterator[str], source: str = "") -> list[Market]:
    """Parse the stream lines of one file (a file can, rarely, hold several markets)."""
    markets: dict[str, Market] = {}
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        msg = json.loads(raw)
        if msg.get("op") != "mcm":
            continue
        when = _ts(msg["pt"])
        for mc in msg.get("mc", []):
            m = markets.setdefault(mc["id"], Market(market_id=mc["id"], source=source))
            md = mc.get("marketDefinition")
            if md:
                m.event_id = md.get("eventId", m.event_id)
                m.event_name = md.get("eventName", m.event_name)
                m.market_type = md.get("marketType", m.market_type)
                m.event_type_id = md.get("eventTypeId", m.event_type_id)
                m.country_code = md.get("countryCode", m.country_code)
                m.scheduled_start = _parse_time(md.get("marketTime")) or m.scheduled_start
                m.status = md.get("status", m.status)
                if md.get("inPlay") and m.inplay_time is None:
                    m.inplay_time = when
                for rd in md.get("runners", []):
                    r = m.runners.get(rd["id"])
                    if r is None:
                        r = m.runners[rd["id"]] = Runner(rd["id"], rd.get("name", str(rd["id"])),
                                                          rd.get("sortPriority"))
                    r.name = rd.get("name", r.name)
                    r.sort_priority = rd.get("sortPriority", r.sort_priority)
                    r.status = rd.get("status", r.status)
            for rc in mc.get("rc", []):
                if "ltp" in rc and rc["ltp"]:
                    r = m.runners.setdefault(rc["id"], Runner(rc["id"], str(rc["id"]), None))
                    r.ticks.append((when, float(rc["ltp"])))
    for m in markets.values():
        for r in m.runners.values():
            r.ticks.sort(key=lambda t: t[0])
    return list(markets.values())


def _open_text(name: str, data: bytes) -> Iterator[str]:
    if name.endswith(".bz2"):
        data = bz2.decompress(data)
    elif name.endswith(".gz"):
        data = gzip.decompress(data)
    return io.StringIO(data.decode("utf-8"))


def iter_markets(root: Path) -> Iterator[Market]:
    """Every market in every file under ``root``: plain, .bz2, .gz, or inside .tar archives."""
    for path in sorted(Path(root).rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        if tarfile.is_tarfile(path):
            with tarfile.open(path) as tar:
                for member in tar:
                    if member.isfile():
                        data = tar.extractfile(member).read()
                        yield from parse_lines(_open_text(member.name, data),
                                               f"{path.name}:{member.name}")
        else:
            yield from parse_lines(_open_text(path.name, path.read_bytes()), str(path))


@dataclass
class PriceRow:
    """One selection of one market with its prices at the chosen snapshots."""
    market_id: str
    event_name: str
    home_name: str
    away_name: str
    scheduled_start_utc: str
    kickoff_utc: str
    kickoff_source: str
    selection: str            # home / draw / away
    runner_name: str
    winner: bool | None
    prices: dict[str, float | None]          # snapshot -> last traded price
    price_times: dict[str, str | None]       # snapshot -> time of that trade (UTC)


def snapshot_label(hours: float) -> str:
    return f"{hours:g}h"


def price_rows(market: Market, early_hours=(24, 2)) -> list[PriceRow]:
    """Long-format rows (one per selection). Raises ValueError if the market is unusable."""
    if market.kickoff is None:
        raise ValueError("no kick-off time")
    sel = market.selections()
    home, away = market.teams()
    win = market.winner()
    times = {"close": (market.kickoff, True)}
    for h in early_hours:
        times[snapshot_label(h)] = (market.kickoff - dt.timedelta(hours=h), False)
    rows = []
    for name in ("home", "draw", "away"):
        r = sel[name]
        prices, ptimes = {}, {}
        for label, (t, strict) in times.items():
            hit = r.last_price_at(t, strict=strict)
            prices[label] = hit[1] if hit else None
            ptimes[label] = hit[0].isoformat() if hit else None
        rows.append(PriceRow(
            market_id=market.market_id, event_name=market.event_name, home_name=home,
            away_name=away,
            scheduled_start_utc=market.scheduled_start.isoformat() if market.scheduled_start else "",
            kickoff_utc=market.kickoff.isoformat(), kickoff_source=market.kickoff_source,
            selection=name, runner_name=r.name,
            winner=None if win is None else win == name, prices=prices, price_times=ptimes))
    return rows
