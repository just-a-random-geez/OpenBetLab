"""reports/model_comparison.md: every model on the held-out season, reproducibly."""

from __future__ import annotations

import platform
from collections import Counter

import numpy as np

from .metrics import (OUTCOMES, brier_per_match, brier_score, calibration_table, log_loss,
                      log_loss_per_match, paired_difference)

MODEL_ORDER = ["uniform", "league_average", "poisson_no_decay", "poisson", "poisson_calibrated",
               "dixon_coles", "dixon_coles_calibrated", "elo", "elo_calibrated"]

DESCRIPTIONS = {
    "uniform": "1/3 each - knows nothing",
    "league_average": "each league's home/draw/away rates from the train seasons",
    "poisson_no_decay": "Poisson goals model, all past matches weighted equally",
    "poisson": "Poisson goals model with time decay (walk-forward)",
    "poisson_calibrated": "poisson + calibration step",
    "dixon_coles": "Poisson + Dixon-Coles low-score correction (walk-forward)",
    "dixon_coles_calibrated": "dixon_coles + calibration step",
    "elo": "Elo ratings + ordered-logit probabilities",
    "elo_calibrated": "elo + calibration step",
}


def _table(headers, rows) -> str:
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
                     + ["| " + " | ".join(str(v) for v in r) + " |" for r in rows])


def reproduce_commands(holdout: str, build_info: dict) -> list[str]:
    as_of = build_info.get("as_of", "YYYY-MM-DD")
    return [
        'pip install -e ".[dev]"',
        "python scripts/fetch_openfootball.py",
        f"python -m openbetlab.data.build --as-of {as_of}",
        f"python -m openbetlab.evaluation.run --holdout-season {holdout}",
    ]


def render_comparison(ev: dict, build_info: dict | None = None) -> str:
    build_info = build_info or {}
    split, fc = ev["split"], ev["forecasts"]
    outs = [m.outcome for m in split.test]
    n = len(outs)
    names = [m for m in MODEL_ORDER if m in fc] + [m for m in fc if m not in MODEL_ORDER]
    actual = Counter(outs)
    seasons = sorted({m.season for m in split.train})

    lines = [
        "# Model Comparison",
        "",
        "> **No betting edge is claimed.** These numbers measure how accurate the "
        "probabilities are against actual results. They were not compared with bookmaker "
        "odds, include no margins, staking or costs, and a better score than a naive "
        "baseline does not imply profit.",
        "",
        "## Reproduce",
        "",
        "```bash",
        *reproduce_commands(split.holdout_season, build_info),
        "```",
        "",
        f"- Data: openfootball/football.json @ `{build_info.get('source_commit', 'unknown')}` "
        f"(CC0-1.0), leagues {', '.join(build_info.get('leagues') or [])}, "
        f"built with as-of date {build_info.get('as_of', 'unknown')}",
        f"- Python {platform.python_version()}, numpy {np.__version__}",
        "- Deterministic: no random numbers are used, so the same inputs give the same output.",
        "",
        "## Setup",
        "",
        f"- Held-out (test) season: **{split.holdout_season}**, {n} played matches "
        f"(home {actual['H'] / n:.1%}, draw {actual['D'] / n:.1%}, away {actual['A'] / n:.1%})",
        f"- Train: {len(split.train)} matches, {seasons[0]} to {seasons[-1]}. "
        f"Model settings and calibration were chosen using {ev['val_season']} (a train "
        "season) only.",
        "- Every forecast uses only matches played before that match's date.",
        "",
        "## Scores on the held-out season",
        "",
        "Lower is better for both. Brier: 0 perfect, 2 worst. Log loss: penalises confident "
        "mistakes most.",
        "",
    ]
    rows = [[f"`{m}`", DESCRIPTIONS.get(m, ""), f"{brier_score(fc[m], outs):.4f}",
             f"{log_loss(fc[m], outs):.4f}"] for m in names]
    lines.append(_table(["Model", "What it is", "Brier", "Log loss"], rows))

    lines += ["", "### Paired differences", "",
              "Mean per-match difference (first minus second; negative = first better) and "
              "how many standard errors that is. Beyond ±2 SE is unlikely to be chance.", ""]
    pairs = [("poisson", "league_average"), ("elo", "league_average"), ("elo", "poisson"),
             ("dixon_coles", "poisson"), ("poisson", "poisson_no_decay"),
             ("poisson_calibrated", "poisson"), ("dixon_coles_calibrated", "dixon_coles"),
             ("elo_calibrated", "elo")]
    prow = []
    for a, b in pairs:
        if a in fc and b in fc:
            mb, sb = paired_difference(brier_per_match(fc[a], outs), brier_per_match(fc[b], outs))
            ml, sl = paired_difference(log_loss_per_match(fc[a], outs),
                                       log_loss_per_match(fc[b], outs))
            verdict = (f"{a} better" if ml < -2 * sl else f"{b} better" if ml > 2 * sl
                       else "no clear difference")
            prow.append([f"{a} vs {b}", f"{mb:+.4f} ({mb / sb:+.1f} SE)",
                         f"{ml:+.4f} ({ml / sl:+.1f} SE)", verdict])
    lines.append(_table(["Comparison", "Brier diff", "Log loss diff", "Verdict (log loss)"],
                        prow))

    lines += ["", "## Calibration step", "",
              "calibrated p ∝ exp(b + w · log p), fitted by maximum likelihood on each model's "
              "walk-forward forecasts for the validation season only. w > 1 = make forecasts "
              "more confident; b shifts probability towards draw / away.", ""]
    crow = []
    for name, c in ev.get("calibration", {}).items():
        cal = c["calibrator"]
        crow.append([f"`{name}`", ", ".join(c["seasons"]), cal.n_fit, f"{cal.w:.3f}",
                     f"{cal.b[1]:+.3f}", f"{cal.b[2]:+.3f}"])
    lines.append(_table(["Model", "Fitted on", "Matches", "w", "b draw", "b away"], crow))

    lines += ["", "## Calibration tables (held-out season)", "",
              "Forecasts grouped into 10%-wide buckets per outcome. *Actual* = how often the "
              "outcome happened. Buckets with few matches are noisy.", ""]
    label = dict(zip(OUTCOMES, ["home", "draw", "away"]))
    for m in names:
        lines += [f"### `{m}`", "",
                  _table(["Outcome", "Bucket", "Matches", "Mean predicted", "Actual", "Gap"],
                         [[label[r.outcome], f"{r.bucket_low:.1f}-{r.bucket_high:.1f}", r.n,
                           f"{r.mean_predicted:.3f}", f"{r.actual_rate:.3f}", f"{r.gap:+.3f}"]
                          for r in calibration_table(fc[m], outs)]), ""]
    return "\n".join(lines)
