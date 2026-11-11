"""Evaluate models with a time-based split and write a report.

    python -m openbetlab.evaluation.run [--holdout-season 2025-26]
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from .baseline import LeagueAverageModel, UniformModel
from .data import (latest_complete_season, load_matches_csv, results_from_rows,
                   season_sort_key, time_split)
from .metrics import OUTCOMES, brier_score, calibration_table, log_loss

ROOT = Path(__file__).resolve().parents[2]


def score(model, matches) -> dict:
    probs = [model.predict(m) for m in matches]
    outs = [m.outcome for m in matches]
    return {"n": len(matches), "brier": brier_score(probs, outs), "log_loss": log_loss(probs, outs)}


def _table(headers, rows) -> str:
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
                     + ["| " + " | ".join(str(v) for v in r) + " |" for r in rows])


def render(split, models) -> str:
    seasons = sorted({m.season for m in split.train}, key=season_sort_key)
    leagues = sorted({m.league for m in split.test})
    actual = Counter(m.outcome for m in split.test)
    n = len(split.test)
    lines = [
        "# Evaluation Report",
        "",
        "## Split (by time, never shuffled)",
        "",
        f"- Train: {len(split.train)} played matches, seasons {seasons[0]} to {seasons[-1]}",
        f"- Test (out-of-sample): {len(split.test)} played matches, season {split.holdout_season}",
        f"- Later seasons not used: {split.excluded_later} matches",
        f"- Test-season actual rates: home {actual['H'] / n:.3f}, draw {actual['D'] / n:.3f}, "
        f"away {actual['A'] / n:.3f}",
        "",
        "## Scores on the test season",
        "",
        "Lower is better. Reference: always 1/3 each = Brier 0.6667, log loss 1.0986.",
        "",
    ]
    rows = []
    for model in models:
        for lg in ["ALL"] + leagues:
            ms = split.test if lg == "ALL" else [m for m in split.test if m.league == lg]
            s = score(model, ms)
            rows.append([model.name, lg, s["n"], f"{s['brier']:.4f}", f"{s['log_loss']:.4f}"])
    lines.append(_table(["Model", "League", "Matches", "Brier", "Log loss"], rows))

    lines += ["", "In-sample (train) scores, for comparison only - not a test of skill:", ""]
    lines.append(_table(["Model", "Matches", "Brier", "Log loss"],
                        [[mo.name, s["n"], f"{s['brier']:.4f}", f"{s['log_loss']:.4f}"]
                         for mo in models for s in [score(mo, split.train)]]))

    base = models[0]
    lines += ["", f"## Calibration: {base.name} on the test season", "",
              "Forecasts grouped by predicted probability; *actual* = how often that outcome "
              "happened. Well calibrated means actual ≈ predicted.", ""]
    cal = calibration_table([base.predict(m) for m in split.test],
                            [m.outcome for m in split.test])
    names = dict(zip(OUTCOMES, ["home", "draw", "away"]))
    lines.append(_table(["Outcome", "Bucket", "Matches", "Mean predicted", "Actual", "Gap"],
                        [[names[r.outcome], f"{r.bucket_low:.1f}-{r.bucket_high:.1f}", r.n,
                          f"{r.mean_predicted:.3f}", f"{r.actual_rate:.3f}", f"{r.gap:+.3f}"]
                         for r in cal]))
    lines += ["", "League rates learned from the train seasons:", "",
              _table(["League", "Home", "Draw", "Away"],
                     [[lg, *(f"{p:.3f}" for p in base.league_rates[lg])]
                      for lg in sorted(base.league_rates)])]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--matches", type=Path, default=ROOT / "data/clean/matches.csv")
    p.add_argument("--holdout-season", default=None,
                   help="default: latest season with no matches still scheduled")
    p.add_argument("--report", type=Path, default=ROOT / "docs/evaluation_report.md")
    a = p.parse_args(argv)

    rows = load_matches_csv(a.matches)
    holdout = a.holdout_season or latest_complete_season(rows)
    split = time_split(results_from_rows(rows), holdout)
    models = [LeagueAverageModel().fit(split.train), UniformModel().fit(split.train)]
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(render(split, models), encoding="utf-8")
    print(f"holdout {holdout}: train {len(split.train)}, test {len(split.test)} -> {a.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
