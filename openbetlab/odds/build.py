"""Build odds tables from Betfair BASIC files and match them to openfootball.

    python -m openbetlab.odds.build

Inputs : data/raw/betfair/**  (Betfair files; personal-use licence, never committed)
         data/clean/matches.csv
Outputs (all gitignored, personal use only):
         data/odds/betfair_prices.csv       one row per market x selection
         data/odds/betfair_match_probs.csv  one row per market x snapshot
         data/odds/odds_report.md
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
from collections import Counter
from pathlib import Path
from statistics import mean

from openbetlab.evaluation.data import load_matches_csv
from openbetlab.settings import ROOT, Settings, load_settings

from .betfair import iter_markets, price_rows, snapshot_label
from .matching import FixtureRef, Matcher, load_mapping
from .probabilities import overround, remove_margin_proportional
from .profit import breakeven_probability

SELECTIONS = ("home", "draw", "away")


def fixtures_from_rows(rows: list[dict]) -> list[FixtureRef]:
    out = []
    for r in rows:
        if not r["date"]:
            continue
        out.append(FixtureRef(r["league"], r["season"], r["date"], r["home_team"],
                              r["away_team"],
                              int(r["ft_home"]) if r["ft_home"] != "" else None,
                              int(r["ft_away"]) if r["ft_away"] != "" else None))
    return out


def build(betfair_dir: Path, fixtures: list[FixtureRef], mapping: dict[str, str],
          settings: Settings):
    matcher = Matcher(fixtures, mapping, settings.fuzzy_min_score)
    snaps = ["close"] + [snapshot_label(h) for h in settings.early_snapshots_hours]
    skipped: Counter = Counter()
    price_table, prob_table, matches, seen = [], [], [], {}
    n_markets = 0
    for market in iter_markets(betfair_dir):
        n_markets += 1
        if market.market_type != "MATCH_ODDS" or market.event_type_id not in (None, "1"):
            skipped["not a football match-odds market"] += 1
            continue
        try:
            rows = price_rows(market, settings.early_snapshots_hours)
        except ValueError as e:
            skipped[f"unusable market: {e}"] += 1
            continue
        res = matcher.match(rows[0].home_name, rows[0].away_name, market.kickoff)
        fx = res.fixture
        if fx is not None:
            key = (fx.league, fx.season, fx.date, fx.home_team, fx.away_team)
            if key in seen:
                skipped["second market for an already-matched fixture"] += 1
                continue
            seen[key] = market.market_id
        winner = market.winner()
        result_check = ("n/a" if fx is None or fx.outcome() is None or winner is None
                        else "agree" if fx.outcome() == winner else "DISAGREE")
        matches.append({"market_id": market.market_id, "event_name": market.event_name,
                        "kickoff_utc": market.kickoff.isoformat(), "method": res.method,
                        "score": res.score, "reason": res.reason, "fixture": fx,
                        "result_check": result_check})
        fx_cols = {"league": fx.league if fx else "", "season": fx.season if fx else "",
                   "match_date": fx.date if fx else "",
                   "home_team": fx.home_team if fx else "", "away_team": fx.away_team if fx else "",
                   "match_method": res.method}
        for r in rows:
            row = {"market_id": r.market_id, "event_name": r.event_name, **fx_cols,
                   "scheduled_start_utc": r.scheduled_start_utc, "kickoff_utc": r.kickoff_utc,
                   "kickoff_source": r.kickoff_source, "selection": r.selection,
                   "runner_name": r.runner_name,
                   "winner": "" if r.winner is None else int(r.winner)}
            for s in snaps:
                row[f"price_{s}"] = r.prices[s]
                row[f"price_time_{s}"] = r.price_times[s]
            price_table.append(row)
        by_sel = {r.selection: r for r in rows}
        for s in snaps:
            odds = [by_sel[k].prices[s] for k in SELECTIONS]
            row = {"market_id": market.market_id, **fx_cols, "kickoff_utc": rows[0].kickoff_utc,
                   "snapshot": s, "winner": winner or ""}
            complete = all(o is not None and o > 1 for o in odds)
            fair = remove_margin_proportional(odds) if complete else [None] * 3
            row["overround"] = overround(odds) if complete else None
            for k, o, f in zip(SELECTIONS, odds, fair):
                row[f"odds_{k}"] = o
                row[f"price_time_{k}"] = by_sel[k].price_times[s]
                row[f"implied_{k}"] = 1 / o if o and o > 1 else None
                row[f"fair_prob_{k}"] = f
                row[f"breakeven_prob_{k}"] = (breakeven_probability(o, settings.commission)
                                              if o and o > 1 else None)
            prob_table.append(row)
    return {"n_markets": n_markets, "skipped": skipped, "prices": price_table,
            "probs": prob_table, "matches": matches, "snapshots": snaps}


def _write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        if not rows:
            fh.write("")
            return
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: "" if v is None else v for k, v in r.items()})


def render_report(out: dict, settings: Settings) -> str:
    methods = Counter(m["method"] for m in out["matches"])
    checks = Counter(m["result_check"] for m in out["matches"])
    lines = ["# Betfair Odds Report (PRIVATE - personal-use data, do not commit or share)", "",
             f"- Generated: {dt.date.today().isoformat()}",
             f"- Commission setting: {settings.commission:.1%} "
             "(applied to all profit / break-even figures)",
             f"- Markets read: {out['n_markets']}",
             f"- Usable match-odds markets: {len(out['matches'])}",
             f"- Matched by mapping file: {methods['mapping']}, by fuzzy names: "
             f"{methods['fuzzy']}, unmatched: {methods['unmatched']}",
             f"- Betfair winner vs openfootball result: agree {checks['agree']}, "
             f"**disagree {checks['DISAGREE']}**, not checkable {checks['n/a']}", "",
             "## Skipped markets", ""]
    lines += ([f"- {k}: {v}" for k, v in out["skipped"].most_common()] or ["None."])
    lines += ["", "## Prices and overround by snapshot", "",
              "| Snapshot | Markets with all 3 prices | Missing | Mean overround | Min | Max |",
              "|---|---|---|---|---|---|"]
    for s in out["snapshots"]:
        rows = [r for r in out["probs"] if r["snapshot"] == s]
        ors = [r["overround"] for r in rows if r["overround"] is not None]
        lines.append(f"| {s} | {len(ors)} | {len(rows) - len(ors)} | "
                     + (f"{mean(ors):+.4f} | {min(ors):+.4f} | {max(ors):+.4f} |" if ors
                        else "- | - | - |"))
    fuzzy = [m for m in out["matches"] if m["method"] == "fuzzy"]
    lines += ["", "## Fuzzy matches (check, then add names to data/team_names/betfair/england.csv)",
              ""]
    lines += [f"- {m['event_name']} ({m['kickoff_utc'][:10]}) -> {m['fixture'].home_team} v "
              f"{m['fixture'].away_team} [{m['fixture'].league}] score {m['score']:.2f}"
              for m in fuzzy] or ["None."]
    lines += ["", "## Unmatched markets", ""]
    lines += [f"- {m['event_name']} ({m['kickoff_utc'][:16]}): {m['reason']}"
              for m in out["matches"] if m["method"] == "unmatched"] or ["None."]
    bad = [m for m in out["matches"] if m["result_check"] == "DISAGREE"]
    lines += ["", "## Result disagreements (possible wrong match or data error)", ""]
    lines += [f"- {m['event_name']} -> {m['fixture'].home_team} v {m['fixture'].away_team} "
              f"{m['fixture'].date}" for m in bad] or ["None."]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--betfair-dir", type=Path, default=ROOT / "data/raw/betfair")
    p.add_argument("--matches", type=Path, default=ROOT / "data/clean/matches.csv")
    p.add_argument("--names-dir", type=Path, default=ROOT / "data/team_names/betfair")
    p.add_argument("--out-dir", type=Path, default=ROOT / "data/odds")
    p.add_argument("--settings", type=Path, default=ROOT / "config/settings.toml")
    a = p.parse_args(argv)
    if not a.betfair_dir.exists():
        print(f"No Betfair files: put the BASIC downloads in {a.betfair_dir}")
        return 1
    settings = load_settings(a.settings)
    out = build(a.betfair_dir, fixtures_from_rows(load_matches_csv(a.matches)),
                load_mapping(a.names_dir), settings)
    _write_csv(out["prices"], a.out_dir / "betfair_prices.csv")
    _write_csv(out["probs"], a.out_dir / "betfair_match_probs.csv")
    (a.out_dir / "odds_report.md").write_text(render_report(out, settings), encoding="utf-8")
    print(f"{len(out['matches'])} markets -> {a.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
