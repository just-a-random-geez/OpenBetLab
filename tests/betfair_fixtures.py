"""Synthetic Betfair BASIC stream files for tests (format as in Betfair's spec)."""

import bz2
import datetime as dt
import json

UTC = dt.timezone.utc


def ms(t: dt.datetime) -> int:
    return int(t.timestamp() * 1000)


def market_lines(market_id="1.100", event="Man City v Wolves", kickoff=None, runners=None,
                 ticks=(), inplay_at=None, winner="home", market_type="MATCH_ODDS"):
    """ticks: list of (datetime, {selection: ltp}). Selections: home/away/draw."""
    kickoff = kickoff or dt.datetime(2024, 8, 17, 14, 0, tzinfo=UTC)
    if runners is None:
        home, away = event.split(" v ")
        runners = [(101, home, 1), (102, away, 2), (103, "The Draw", 3)]
    ids = {"home": runners[0][0], "away": runners[1][0], "draw": runners[2][0]}

    def definition(in_play, status, final=False):
        sel_of = {runners[0][0]: "home", runners[1][0]: "away", runners[2][0]: "draw"}
        return {"eventId": "999", "eventName": event, "marketType": market_type,
                "eventTypeId": "1", "countryCode": "GB",
                "marketTime": kickoff.isoformat().replace("+00:00", "Z"),
                "inPlay": in_play, "status": status,
                "runners": [{"id": rid, "name": name, "sortPriority": prio,
                             "status": (("WINNER" if sel_of[rid] == winner else "LOSER")
                                        if final else "ACTIVE")}
                            for rid, name, prio in runners]}

    start = kickoff - dt.timedelta(days=3)
    lines = [{"op": "mcm", "pt": ms(start), "mc": [{"id": market_id,
                                                     "marketDefinition": definition(False, "OPEN")}]}]
    for when, prices in ticks:
        lines.append({"op": "mcm", "pt": ms(when), "mc": [{"id": market_id, "rc": [
            {"id": ids[k], "ltp": v} for k, v in prices.items()]}]})
    if inplay_at is not None:
        lines.append({"op": "mcm", "pt": ms(inplay_at),
                      "mc": [{"id": market_id, "marketDefinition": definition(True, "OPEN")}]})
    end = kickoff + dt.timedelta(hours=2)
    lines.append({"op": "mcm", "pt": ms(end),
                  "mc": [{"id": market_id, "marketDefinition": definition(True, "CLOSED", True)}]})
    lines.sort(key=lambda l: l["pt"])
    return "\n".join(json.dumps(l) for l in lines) + "\n"


def write_market(directory, name, text, compress=True):
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (name + (".bz2" if compress else ""))
    path.write_bytes(bz2.compress(text.encode()) if compress else text.encode())
    return path
