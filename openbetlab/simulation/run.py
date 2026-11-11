"""Run the Monte Carlo risk simulation and write a report.

    python -m openbetlab.simulation.run                      # validation season (2024-25) odds
    python -m openbetlab.simulation.run --source synthetic   # illustration, no real data
    python -m openbetlab.simulation.run --source holdout     # only once the plan is FROZEN

Real-odds reports contain Betfair-derived numbers -> reports/private/ (gitignored).
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

from openbetlab.backtest.run import PLAN, plan_status
from openbetlab.odds.compare import join
from openbetlab.settings import ROOT, load_settings

from .montecarlo import SEED, Opportunity, default_scenarios, simulate, synthetic_season

DISCLAIMER = (
    "> **This simulation measures RISK, not edge.** It replays the strategy on the same "
    "set of matches 10,000 times with results drawn at random from an *assumed* truth. "
    "Under \"model\" truth the model is assumed to be right, so a profit there is built "
    "in, not discovered. Under \"market\" truth the market is assumed right - the model then "
    "has no edge, and the result shows what that costs. Only the pre-registered backtest "
    "can say anything about a real edge.")


def opportunities_from_files(forecasts: Path, market: Path, model: str, snapshot: str):
    with forecasts.open(newline="", encoding="utf-8") as fh:
        fc = list(csv.DictReader(fh))
    with market.open(newline="", encoding="utf-8") as fh:
        mk = list(csv.DictReader(fh))
    joined, counts = join(fc, mk, model, snapshot)
    opps = [Opportunity(j.key[2], j.model, j.market, j.odds) for j in joined]
    return sorted(opps, key=lambda o: o.date), counts


def render(results, source: str, n: int, seed: int, extra: list[str]) -> str:
    lines = [f"# Monte Carlo Risk Simulation ({source})", "", DISCLAIMER, "",
             f"- Seasons simulated per scenario: {n:,}; random seed {seed} (fixed - "
             "re-running gives identical numbers)",
             "- Every scenario uses the same simulated results for the same match, so "
             "scenarios are compared on equal luck.",
             "- Start bankroll £100. Ruin = bankroll below £1 (Betfair's minimum stake). "
             "Bets placed on the same day are sized from that morning's bankroll.",
             *extra, "",
             "Profit columns are £ at the end of the season (median and 5th / 95th "
             "percentile). 'Worst drawdown' = median across seasons of the biggest fall from "
             "a peak.", "",
             "| Scenario | Bets/season | Median £ | 5th pct £ | 95th pct £ | P(profit) | "
             "P(lose 50%) | P(ruin) | Typical worst drawdown |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        s = r.summary()
        lines.append(f"| {r.scenario.name} | {s['bets']} | {s['median']:+.2f} | {s['p5']:+.2f} | "
                     f"{s['p95']:+.2f} | {s['p_profit']:.1%} | {s['p_lose_half']:.1%} | "
                     f"{s['p_ruin']:.1%} | {s['median_max_dd']:.1%} |")
    lines += ["", "Definitions: *rollover* = stakes sized on the current bankroll (winnings "
              "are re-staked); *no rollover* = stakes sized on the starting £100. Flat = £1 "
              "(or 1% of bankroll with rollover). Kelly x% = x% of the Kelly stake computed "
              "from the MODEL's probability and the odds after commission. Parlays are "
              "hypothetical (Betfair Exchange has no multiples): same-day qualifying picks "
              "grouped by highest edge. Overconfident x% = when the model backs an outcome, "
              "its true chance is x% lower (relative) than the model says."]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--source", choices=("validation", "holdout", "synthetic"),
                   default="validation")
    p.add_argument("--seasons", type=int, default=10_000)
    p.add_argument("--seed", type=int, default=SEED)
    p.add_argument("--model", default=None)
    p.add_argument("--market", type=Path, default=ROOT / "data/odds/betfair_match_probs.csv")
    p.add_argument("--report", type=Path, default=None)
    a = p.parse_args(argv)
    settings = load_settings()
    extra = [f"- Commission: {settings.commission:.0%}"]

    if a.source == "synthetic":
        opps = synthetic_season()
        extra.append("- **SYNTHETIC season (2,000 made-up matches)**: illustrates the "
                     "method only; says nothing about the real model or market.")
        report = a.report or ROOT / "reports/monte_carlo_synthetic.md"
    else:
        if a.source == "holdout" and not plan_status(PLAN)[0]:
            print("Refusing: the held-out season's prices may only be used once "
                  "docs/RESEARCH_PLAN_v1.md is FROZEN.")
            return 2
        fpath = ROOT / ("data/clean/forecasts_validation.csv" if a.source == "validation"
                        else "data/clean/forecasts.csv")
        for path, how in ((fpath, "python -m openbetlab.evaluation.run"),
                          (a.market, "python -m openbetlab.odds.build")):
            if not path.exists():
                print(f"Missing {path}. Run: {how}")
                return 1
        meta = json.loads((ROOT / "data/clean/forecasts.json").read_text())
        model = a.model or min(meta["validation_log_loss"], key=meta["validation_log_loss"].get)
        opps, counts = opportunities_from_files(fpath, a.market, model, "2h")
        if not opps:
            print("No matches with both a forecast and a complete 2h price.")
            return 1
        extra.append(f"- Opportunities: {counts['with_market']} {a.source}-season matches "
                     f"with model `{model}` forecasts and complete 2h Betfair prices")
        report = a.report or ROOT / f"reports/private/monte_carlo_{a.source}.md"

    t = time.time()
    results = [simulate(opps, sc, a.seasons, a.seed) for sc in default_scenarios()]
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(render(results, a.source, a.seasons, a.seed, extra), encoding="utf-8")
    print(f"{len(results)} scenarios x {a.seasons} seasons in {time.time() - t:.0f}s -> {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
