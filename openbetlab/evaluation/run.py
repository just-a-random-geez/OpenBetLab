"""Evaluate models with a time-based split and write a report.

    python -m openbetlab.evaluation.run [--holdout-season 2025-26]

Steps:
1. Test season = latest completed season (held out). Train = all earlier seasons.
2. Poisson settings are tuned on the LAST TRAIN season (validation), walk-forward,
   using only seasons before it. The test season is never looked at while tuning.
3. Both models are scored once on the test season.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from openbetlab.models.poisson import PoissonModel, walk_forward

from .baseline import LeagueAverageModel, UniformModel
from .data import (latest_complete_season, load_matches_csv, results_from_rows,
                   season_sort_key, time_split)
from .metrics import (OUTCOMES, brier_per_match, brier_score, calibration_table, log_loss,
                      log_loss_per_match, paired_difference)

ROOT = Path(__file__).resolve().parents[2]
HALF_LIVES = (90, 180, 365, 730)
PRIOR_GOALS = (5, 10, 20)


def score(probs, matches) -> dict:
    outs = [m.outcome for m in matches]
    return {"n": len(matches), "brier": brier_score(probs, outs), "log_loss": log_loss(probs, outs)}


def tune_poisson(train, half_lives=HALF_LIVES, priors=PRIOR_GOALS):
    """Grid-search Poisson settings on the last train season (walk-forward). Lowest log loss wins."""
    val_season = max({m.season for m in train}, key=season_sort_key)
    inner = time_split(train, val_season)
    grid = []
    for hl in half_lives:
        for k in priors:
            probs = walk_forward(PoissonModel(hl, k), inner.train, inner.test)
            grid.append({"half_life_days": hl, "prior_goals": k, **score(probs, inner.test)})
    best = min(grid, key=lambda g: g["log_loss"])
    return best, grid, val_season


def _table(headers, rows) -> str:
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
                     + ["| " + " | ".join(str(v) for v in r) + " |" for r in rows])


def evaluate(rows, holdout: str | None = None, half_lives=HALF_LIVES, priors=PRIOR_GOALS):
    skipped: dict = {}
    results = results_from_rows(rows, skipped)
    holdout = holdout or latest_complete_season(rows)
    split = time_split(results, holdout)
    best, grid, val_season = tune_poisson(split.train, half_lives, priors)

    baseline = LeagueAverageModel().fit(split.train)
    forecasts = {
        "poisson": walk_forward(PoissonModel(best["half_life_days"], best["prior_goals"]),
                                split.train, split.test),
        "league_average": [baseline.predict(m) for m in split.test],
        "uniform": [UniformModel().predict(m) for m in split.test],
    }
    return {"split": split, "skipped": skipped, "best": best, "grid": grid,
            "val_season": val_season, "baseline": baseline, "forecasts": forecasts}


def render(ev) -> str:
    split, forecasts = ev["split"], ev["forecasts"]
    seasons = sorted({m.season for m in split.train}, key=season_sort_key)
    leagues = sorted({m.league for m in split.test})
    actual = Counter(m.outcome for m in split.test)
    n = len(split.test)
    best = ev["best"]
    lines = [
        "# Evaluation Report",
        "",
        "## Split (by time, never shuffled)",
        "",
        f"- Train: {len(split.train)} played matches, seasons {seasons[0]} to {seasons[-1]}",
        f"- Test (out-of-sample): {n} played matches, season {split.holdout_season}",
        f"- Later seasons not used: {split.excluded_later} matches",
        f"- Played matches excluded for an out-of-season date (can't be placed in time): "
        f"{ev['skipped'].get('bad_date', 0)}",
        f"- Test-season actual rates: home {actual['H'] / n:.3f}, draw {actual['D'] / n:.3f}, "
        f"away {actual['A'] / n:.3f}",
        "",
        "## Scores on the test season",
        "",
        "Lower is better. Reference: always 1/3 each = Brier 0.6667, log loss 1.0986.",
        "Poisson forecasts are walk-forward: refitted before each match date on earlier "
        "matches only. The league-average baseline uses the train seasons only.",
        "",
    ]
    rows = []
    for name, probs in forecasts.items():
        for lg in ["ALL"] + leagues:
            idx = [i for i, m in enumerate(split.test) if lg == "ALL" or m.league == lg]
            s = score([probs[i] for i in idx], [split.test[i] for i in idx])
            rows.append([name, lg, s["n"], f"{s['brier']:.4f}", f"{s['log_loss']:.4f}"])
    lines.append(_table(["Model", "League", "Matches", "Brier", "Log loss"], rows))

    outs = [m.outcome for m in split.test]
    lines += ["", "## Is Poisson really better than the baseline?", "",
              "Per-match score difference (Poisson minus league average). Negative = Poisson "
              "better. A gap larger than 2 standard errors is unlikely to be luck.", ""]
    diff_rows = []
    for label, fn in (("Brier", brier_per_match), ("Log loss", log_loss_per_match)):
        mean, se = paired_difference(fn(forecasts["poisson"], outs),
                                     fn(forecasts["league_average"], outs))
        diff_rows.append([label, f"{mean:+.4f}", f"{se:.4f}", f"{mean / se:+.1f}",
                          "yes" if mean < -2 * se else "no"])
    lines.append(_table(["Score", "Mean difference", "Std. error", "Difference / SE",
                         "Clearly better?"], diff_rows))

    lines += ["", f"## Poisson settings (tuned on {ev['val_season']}, a train season)", "",
              f"Chosen: half-life **{best['half_life_days']} days**, prior "
              f"**{best['prior_goals']} goals** (lowest validation log loss).", "",
              _table(["Half-life (days)", "Prior (goals)", "Val. matches", "Brier", "Log loss"],
                     [[g["half_life_days"], g["prior_goals"], g["n"], f"{g['brier']:.4f}",
                       f"{g['log_loss']:.4f}"] for g in ev["grid"]])]

    names = dict(zip(OUTCOMES, ["home", "draw", "away"]))
    for name in ("poisson", "league_average"):
        cal = calibration_table(forecasts[name], [m.outcome for m in split.test])
        lines += ["", f"## Calibration: {name} on the test season", "",
                  "*Actual* = how often that outcome happened. Well calibrated: actual ≈ "
                  "predicted. Small buckets are noisy.", "",
                  _table(["Outcome", "Bucket", "Matches", "Mean predicted", "Actual", "Gap"],
                         [[names[r.outcome], f"{r.bucket_low:.1f}-{r.bucket_high:.1f}", r.n,
                           f"{r.mean_predicted:.3f}", f"{r.actual_rate:.3f}", f"{r.gap:+.3f}"]
                          for r in cal])]

    base = ev["baseline"]
    lines += ["", "League rates learned by the baseline from the train seasons:", "",
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

    ev = evaluate(load_matches_csv(a.matches), a.holdout_season)
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(render(ev), encoding="utf-8")
    s = ev["split"]
    print(f"holdout {s.holdout_season}: train {len(s.train)}, test {len(s.test)} -> {a.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
