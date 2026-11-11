"""Run the pre-registered walk-forward backtest.

    python -m openbetlab.backtest.run

Refuses to run unless docs/RESEARCH_PLAN_v1.md is marked FROZEN, so results can only be
produced under the pre-registered rules. Outputs contain Betfair prices -> gitignored:
    data/odds/backtest_bets.csv
    reports/private/backtest_v1.md
    reports/private/bankroll_v1.svg
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import json
from pathlib import Path

from openbetlab.evaluation.data import load_matches_csv, results_from_rows, time_split
from openbetlab.models.dixon_coles import DixonColesModel
from openbetlab.models.elo import EloParams, elo_forecasts
from openbetlab.models.poisson import PoissonModel, walk_forward
from openbetlab.settings import ROOT

from .engine import SEL, MarketPrices, PlanRules, Snapshot, run_backtest
from .metrics import summarise

PLAN = ROOT / "docs/RESEARCH_PLAN_v1.md"


def plan_status(path: Path) -> tuple[bool, str]:
    """(frozen?, sha256). Frozen = the plan says 'Status: FROZEN' and is not a DRAFT."""
    text = path.read_text(encoding="utf-8")
    head = text[:600].upper()
    frozen = "STATUS: FROZEN" in head and "DRAFT" not in head
    return frozen, hashlib.sha256(text.encode()).hexdigest()


def load_prices(rows: list[dict]) -> dict[tuple, MarketPrices]:
    def f(x):
        return float(x) if x not in ("", None) else None
    out: dict[tuple, dict] = {}
    for r in rows:
        if not r.get("home_team"):
            continue
        key = (r["league"], r["season"], r["match_date"], r["home_team"], r["away_team"])
        snap = Snapshot(tuple(f(r[f"odds_{k}"]) for k in SEL),
                        tuple(f(r[f"fair_prob_{k}"]) for k in SEL),
                        tuple(r.get(f"price_time_{k}") or None for k in SEL))
        out.setdefault(key, {"kickoff": r["kickoff_utc"], "snaps": {}})["snaps"][r["snapshot"]] = snap
    return {k: MarketPrices(v["kickoff"], v["snaps"]) for k, v in out.items()}


def make_forecaster(model: str, settings: dict):
    if model == "poisson":
        return lambda h, t: walk_forward(PoissonModel(**settings["poisson"]), h, t)
    if model == "dixon_coles":
        return lambda h, t: walk_forward(DixonColesModel(**settings["dixon_coles"]), h, t)
    if model == "elo":
        return lambda h, t: elo_forecasts(h, t, EloParams(**settings["elo"]))[0]
    raise ValueError(f"unknown model {model!r}")


def bankroll_svg(curve: list[float], start: float, width=800, height=300) -> str:
    lo, hi = min(curve + [start]), max(curve + [start])
    span = (hi - lo) or 1
    n = max(len(curve) - 1, 1)

    def xy(i, v):
        return 40 + (width - 60) * i / n, 20 + (height - 50) * (hi - v) / span
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (xy(i, v) for i, v in enumerate(curve)))
    y0 = xy(0, start)[1]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'font-family="sans-serif" font-size="12">'
            f'<rect width="100%" height="100%" fill="white"/>'
            f'<line x1="40" y1="{y0:.1f}" x2="{width - 20}" y2="{y0:.1f}" stroke="#999" '
            f'stroke-dasharray="4"/>'
            f'<polyline points="{pts}" fill="none" stroke="#1f77b4" stroke-width="1.5"/>'
            f'<text x="5" y="{y0 + 4:.1f}">£{start:.0f}</text>'
            f'<text x="5" y="20">£{hi:.0f}</text><text x="5" y="{height - 30}">£{lo:.0f}</text>'
            f'<text x="{width / 2 - 60}" y="{height - 8}">bets in time order ({n})</text></svg>')


def summarise_result(result, rules: PlanRules):
    bets = result.bets
    return summarise([b.profit for b in bets], [b.won for b in bets], [b.clv for b in bets],
                     rules.stake, rules.start_bankroll, groups=[b.kickoff_utc for b in bets],
                     clusters=[b.date for b in bets])


def render(result, s, ps, rules: PlanRules, sha: str, frozen: bool, holdout: str,
           sens=None) -> str:
    def pct(x):
        return "-" if x is None else f"{x:+.2%}"
    lines = ["# Backtest v1 (PRIVATE - contains Betfair prices)", "",
             f"- Plan: `docs/RESEARCH_PLAN_v1.md` sha256 `{sha}` "
             + ("(FROZEN)" if frozen else "(**NOT FROZEN - NOT A VALID PRE-REGISTERED RESULT**)"),
             f"- Out-of-sample season: {holdout}",
             f"- Rules: {json.dumps(dataclasses.asdict(rules))}", "",
             "## Singles", "",
             "| Metric | Value |", "|---|---|",
             f"| Bets | {s.bets} |", f"| Wins | {s.wins} |",
             f"| Hit rate | {'-' if s.hit_rate is None else f'{s.hit_rate:.1%}'} |",
             f"| Staked | £{s.staked:.2f} |", f"| Profit after commission | £{s.profit:+.2f} |",
             f"| ROI | {pct(s.roi)} |",
             f"| ROI on all {s.qualifying_bets} qualifying bets (ignoring ruin) | "
             f"{pct(s.roi_all_bets)} |",
             f"| ROI 95% CI (bootstrap by match day) | "
             + ("-" if s.roi_ci95 is None else f"{s.roi_ci95[0]:+.2%} to {s.roi_ci95[1]:+.2%}")
             + " |",
             f"| Average CLV (before commission) | {pct(s.avg_clv)} ({s.clv_bets} bets with a "
             "closing price) |",
             f"| Worst drawdown | £{s.max_drawdown:.2f} ({s.max_drawdown_pct:.1%} of peak) |",
             f"| Longest losing run | {s.longest_losing_run} |",
             f"| Bankroll £{rules.start_bankroll:.0f} → | £{s.final_bankroll:.2f}"
             + (" (RUINED - stopped)" if s.ruined else "") + " |", "",
             "Bankroll curve: `reports/private/bankroll_v1.svg`. Bets: "
             "`data/odds/backtest_bets.csv`.", "",
             "Skipped matches: " + ", ".join(f"{k} {v}" for k, v in result.skipped.items())]
    if sens:
        lines += ["", "## Spread sensitivity (not a pass criterion)", "",
                  "Last traded prices may not be backable: the same rules re-run taking each "
                  "price 1 or 2 Betfair ticks worse.", "",
                  "| Haircut | Bets | ROI | ROI 95% CI |", "|---|---|---|---|"]
        for ticks, x in sens:
            ci = "-" if x.roi_ci95 is None else f"{x.roi_ci95[0]:+.2%} to {x.roi_ci95[1]:+.2%}"
            lines.append(f"| {ticks} tick(s) | {x.bets} | {pct(x.roi)} | {ci} |")
    lines += ["", "CLV is measured before commission: a small positive CLV can still lose "
              "money after commission."]
    if ps is not None:
        lines += ["", "## Parlays (HYPOTHETICAL - Betfair Exchange has no multiples)", "",
                  f"- {ps.bets} parlays, {ps.wins} won, profit £{ps.profit:+.2f}, ROI {pct(ps.roi)}"]
    lines += ["", "Judge these numbers ONLY against the criteria in the frozen plan."]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--plan", type=Path, default=PLAN)
    p.add_argument("--matches", type=Path, default=ROOT / "data/clean/matches.csv")
    p.add_argument("--forecast-meta", type=Path, default=ROOT / "data/clean/forecasts.json")
    p.add_argument("--market", type=Path, default=ROOT / "data/odds/betfair_match_probs.csv")
    p.add_argument("--out-dir", type=Path, default=ROOT)
    a = p.parse_args(argv)

    frozen, sha = plan_status(a.plan)
    if not frozen:
        print(f"Refusing to run: {a.plan} is not FROZEN. Freeze the research plan first.")
        return 2
    for path, how in ((a.forecast_meta, "python -m openbetlab.evaluation.run"),
                      (a.market, "python -m openbetlab.odds.build")):
        if not path.exists():
            print(f"Missing {path}. Run: {how}")
            return 1
    rules = PlanRules()
    meta = json.loads(a.forecast_meta.read_text())
    holdout = meta["holdout_season"]
    split = time_split(results_from_rows(load_matches_csv(a.matches)), holdout)
    with a.market.open(newline="", encoding="utf-8") as fh:
        prices = load_prices(list(csv.DictReader(fh)))
    result = run_backtest(split.train, split.test, prices,
                          make_forecaster(rules.model, meta["settings"]), rules)
    s = summarise_result(result, rules)
    forecaster = make_forecaster(rules.model, meta["settings"])
    sens = []
    for ticks in (1, 2):
        alt_rules = dataclasses.replace(rules, price_haircut_ticks=ticks)
        sens.append((ticks, summarise_result(
            run_backtest(split.train, split.test, prices, forecaster, alt_rules), alt_rules)))
    ps = (summarise([x.profit for x in result.parlays], [x.won for x in result.parlays],
                    [None] * len(result.parlays), rules.stake, rules.start_bankroll)
          if rules.parlays else None)

    bets_path = a.out_dir / "data/odds/backtest_bets.csv"
    priv = a.out_dir / "reports/private"
    bets_path.parent.mkdir(parents=True, exist_ok=True)
    priv.mkdir(parents=True, exist_ok=True)
    with bets_path.open("w", newline="", encoding="utf-8") as fh:
        fields = [f.name for f in dataclasses.fields(result.bets[0])] if result.bets else ["none"]
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for b in result.bets:
            w.writerow(dataclasses.asdict(b))
    (priv / "bankroll_v1.svg").write_text(bankroll_svg(s.curve, rules.start_bankroll))
    (priv / "backtest_v1.md").write_text(render(result, s, ps, rules, sha, frozen, holdout,
                                                sens))
    print(f"{s.bets} bets, ROI {s.roi} -> {priv / 'backtest_v1.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
