"""Evaluate models with a time-based split and write a report.

    python -m openbetlab.evaluation.run [--holdout-season 2025-26]

Steps:
1. Test season = latest completed season (held out). Train = all earlier seasons.
2. Poisson and Elo settings are tuned on the LAST TRAIN season (validation),
   walk-forward, using only seasons before it. The test season is never looked at
   while tuning.
3. All models are scored once on the test season.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from openbetlab.models.dixon_coles import DixonColesModel
from openbetlab.models.elo import EloParams, elo_forecasts
from openbetlab.models.poisson import PoissonModel, walk_forward

from .baseline import LeagueAverageModel, UniformModel
from .calibration import Calibrator
from .comparison import render_comparison
from .data import (latest_complete_season, load_matches_csv, results_from_rows,
                   season_sort_key, time_split)
from .metrics import (OUTCOMES, brier_per_match, brier_score, calibration_table, log_loss,
                      log_loss_per_match, paired_difference)

ROOT = Path(__file__).resolve().parents[2]
HALF_LIVES = (90, 180, 365, 730)
PRIOR_GOALS = (5, 10, 20)
# (K, home advantage, promotion gap, season regression)
ELO_GRID = list(itertools.product((20, 30, 40, 50), (50, 75, 100), (0, 50, 100, 150),
                                  (0.2, 0.4, 0.6)))


def score(probs, matches) -> dict:
    outs = [m.outcome for m in matches]
    return {"n": len(matches), "brier": brier_score(probs, outs), "log_loss": log_loss(probs, outs)}


def tune_poisson(train, half_lives=HALF_LIVES, priors=PRIOR_GOALS, model_cls=PoissonModel):
    """Grid-search Poisson-type settings on the last train season (walk-forward).
    Lowest log loss wins."""
    val_season = max({m.season for m in train}, key=season_sort_key)
    inner = time_split(train, val_season)
    grid = []
    for hl in half_lives:
        for k in priors:
            probs = walk_forward(model_cls(hl, k), inner.train, inner.test)
            grid.append({"half_life_days": hl, "prior_goals": k, "probs": probs,
                         **score(probs, inner.test)})
    best = min(grid, key=lambda g: g["log_loss"])
    best["val_matches"] = inner.test
    return best, grid, val_season


def tune_elo(train, grid=ELO_GRID):
    """Grid-search Elo settings on the last train season. Lowest log loss wins."""
    val_season = max({m.season for m in train}, key=season_sort_key)
    inner = time_split(train, val_season)
    results = []
    for k, h, gap, reg in grid:
        probs, _ = elo_forecasts(inner.train, inner.test, EloParams(k, h, gap, reg))
        results.append({"k": k, "home_adv": h, "promotion_gap": gap, "season_regression": reg,
                        "probs": probs, **score(probs, inner.test)})
    best = min(results, key=lambda g: g["log_loss"])
    best["val_matches"] = inner.test
    return best, results


def _table(headers, rows) -> str:
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
                     + ["| " + " | ".join(str(v) for v in r) + " |" for r in rows])


def evaluate(rows, holdout: str | None = None, half_lives=HALF_LIVES, priors=PRIOR_GOALS,
             elo_grid=ELO_GRID):
    skipped: dict = {}
    results = results_from_rows(rows, skipped)
    holdout = holdout or latest_complete_season(rows)
    split = time_split(results, holdout)
    best, grid, val_season = tune_poisson(split.train, half_lives, priors)

    dc_best, dc_grid, _ = tune_poisson(split.train, half_lives, priors, DixonColesModel)
    dc_model = DixonColesModel(dc_best["half_life_days"], dc_best["prior_goals"])
    dc_probs = walk_forward(dc_model, split.train, split.test)
    # Ablation: same Poisson model with every past match weighted equally (no time decay).
    no_decay = PoissonModel(1e12, best["prior_goals"], max_age_factor=1)
    no_decay_probs = walk_forward(no_decay, split.train, split.test)

    elo_best, elo_grid_res = tune_elo(split.train, elo_grid)
    elo_probs, elo_link = elo_forecasts(
        split.train, split.test,
        EloParams(elo_best["k"], elo_best["home_adv"], elo_best["promotion_gap"],
                  elo_best["season_regression"]))

    baseline = LeagueAverageModel().fit(split.train)
    forecasts = {
        "poisson": walk_forward(PoissonModel(best["half_life_days"], best["prior_goals"]),
                                split.train, split.test),
        "dixon_coles": dc_probs,
        "poisson_no_decay": no_decay_probs,
        "elo": elo_probs,
        "league_average": [baseline.predict(m) for m in split.test],
        "uniform": [UniformModel().predict(m) for m in split.test],
    }
    # Calibration: fitted ONLY on each model's out-of-sample (walk-forward) forecasts for
    # the validation season, which is part of the training data. Applied unchanged to test.
    calibration = {}
    for name, tuned in (("poisson", best), ("dixon_coles", dc_best), ("elo", elo_best)):
        val = tuned["val_matches"]
        cal = Calibrator().fit(tuned["probs"], [m.outcome for m in val])
        forecasts[f"{name}_calibrated"] = cal.transform(forecasts[name])
        calibration[name] = {"calibrator": cal, "seasons": sorted({m.season for m in val}),
                             "last_date": max(m.date for m in val)}

    return {"split": split, "skipped": skipped, "best": best, "grid": grid,
            "calibration": calibration,
            "val_season": val_season, "baseline": baseline, "forecasts": forecasts,
            "elo_best": elo_best, "elo_grid": elo_grid_res, "elo_link": elo_link,
            "dc_best": dc_best, "dc_grid": dc_grid, "dc_rho": dict(dc_model.rho)}


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
        "matches only. Elo ratings are updated match by match, each match predicted with "
        "ratings from earlier dates only. The league-average baseline uses the train "
        "seasons only.",
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
    lines += ["", "## Are the differences real?", "",
              "Per-match score difference (first model minus second). Negative = first model "
              "better. A gap larger than 2 standard errors is unlikely to be luck.", ""]
    diff_rows = []
    for a, b in (("poisson", "league_average"), ("elo", "league_average"), ("elo", "poisson"),
                 ("dixon_coles", "poisson"), ("poisson", "poisson_no_decay")):
        for label, fn in (("Brier", brier_per_match), ("Log loss", log_loss_per_match)):
            mean, se = paired_difference(fn(forecasts[a], outs), fn(forecasts[b], outs))
            verdict = (f"{a} better" if mean < -2 * se else
                       f"{b} better" if mean > 2 * se else "no clear difference")
            diff_rows.append([f"{a} vs {b}", label, f"{mean:+.4f}", f"{se:.4f}",
                              f"{mean / se:+.1f}", verdict])
    lines.append(_table(["Comparison", "Score", "Mean difference", "Std. error",
                         "Difference / SE", "Verdict"], diff_rows))

    lines += ["", f"## Poisson settings (tuned on {ev['val_season']}, a train season)", "",
              f"Chosen: half-life **{best['half_life_days']} days**, prior "
              f"**{best['prior_goals']} goals** (lowest validation log loss).", "",
              _table(["Half-life (days)", "Prior (goals)", "Val. matches", "Brier", "Log loss"],
                     [[g["half_life_days"], g["prior_goals"], g["n"], f"{g['brier']:.4f}",
                       f"{g['log_loss']:.4f}"] for g in ev["grid"]])]

    db = ev["dc_best"]
    lines += ["", f"## Dixon-Coles settings (tuned on {ev['val_season']}, a train season)", "",
              f"Chosen: half-life **{db['half_life_days']} days**, prior "
              f"**{db['prior_goals']} goals**. Low-score correction rho per league "
              "(from the last fit, i.e. all matches before the final test date): "
              + ", ".join(f"{lg} {r:+.3f}" for lg, r in sorted(ev["dc_rho"].items()))
              + ". rho near 0 = almost plain Poisson.", "",
              _table(["Half-life (days)", "Prior (goals)", "Val. matches", "Brier", "Log loss"],
                     [[g["half_life_days"], g["prior_goals"], g["n"], f"{g['brier']:.4f}",
                       f"{g['log_loss']:.4f}"] for g in ev["dc_grid"]]),
              "", "`poisson_no_decay` = the Poisson model with every past match weighted "
              f"equally (prior {best['prior_goals']} goals), to measure what time decay adds."]

    eb, link = ev["elo_best"], ev["elo_link"]
    top = sorted(ev["elo_grid"], key=lambda g: g["log_loss"])[:10]
    lines += ["", f"## Elo settings (tuned on {ev['val_season']}, a train season)", "",
              f"Chosen: K **{eb['k']}**, home advantage **{eb['home_adv']}**, promotion gap "
              f"**{eb['promotion_gap']}**, season regression **{eb['season_regression']}** "
              f"(lowest validation log loss of {len(ev['elo_grid'])} combinations; top 10 "
              "shown).", "",
              _table(["K", "Home adv.", "Promotion gap", "Season regression", "Val. matches",
                      "Brier", "Log loss"],
                     [[g["k"], g["home_adv"], g["promotion_gap"], g["season_regression"],
                       g["n"], f"{g['brier']:.4f}", f"{g['log_loss']:.4f}"] for g in top]),
              "", "Rating gap -> probability mapping (fitted on train seasons): "
              f"b = {link.b:.4f} per 100 points, c1 = {link.c1:.4f}, c2 = {link.c2:.4f}. "
              "Equal ratings give home {:.3f} / draw {:.3f} / away {:.3f}.".format(
                  *link.predict(0))]

    names = dict(zip(OUTCOMES, ["home", "draw", "away"]))
    for name in ("poisson", "dixon_coles", "elo", "league_average"):
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


def write_forecasts(ev, path: Path) -> None:
    """Per-match held-out forecasts of every model + validation log loss per tuned model.

    Used by the model-vs-market comparison (Phase 3).
    """
    import csv
    split, fc = ev["split"], ev["forecasts"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["league", "season", "date", "home_team", "away_team", "outcome"]
                   + [f"{m}_{k}" for m in fc for k in ("home", "draw", "away")])
        for i, m in enumerate(split.test):
            w.writerow([m.league, m.season, m.date, m.home_team, m.away_team, m.outcome]
                       + [f"{x:.6f}" for name in fc for x in fc[name][i]])
    meta = {"holdout_season": split.holdout_season, "validation_season": ev["val_season"],
            # Validation (training-data) log loss: the only fair way to pick a model
            # before looking at the held-out season or the market.
            "validation_log_loss": {"poisson": ev["best"]["log_loss"],
                                    "dixon_coles": ev["dc_best"]["log_loss"],
                                    "elo": ev["elo_best"]["log_loss"]},
            # Settings chosen on the validation season (needed to re-run walk-forward).
            "settings": {
                "poisson": {k: ev["best"][k] for k in ("half_life_days", "prior_goals")},
                "dixon_coles": {k: ev["dc_best"][k] for k in ("half_life_days", "prior_goals")},
                "elo": {k: ev["elo_best"][k] for k in ("k", "home_adv", "promotion_gap",
                                                       "season_regression")}}}
    path.with_suffix(".json").write_text(json.dumps(meta, indent=2) + "\n")

    # Walk-forward forecasts for the VALIDATION season (a training season). Safe to combine
    # with that season's odds for risk simulations without touching the held-out season.
    val = ev["best"]["val_matches"]
    tuned = {"poisson": ev["best"]["probs"], "dixon_coles": ev["dc_best"]["probs"],
             "elo": ev["elo_best"]["probs"]}
    with path.with_name(path.stem + "_validation.csv").open("w", newline="",
                                                            encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["league", "season", "date", "home_team", "away_team", "outcome"]
                   + [f"{m}_{k}" for m in tuned for k in ("home", "draw", "away")])
        for i, m in enumerate(val):
            w.writerow([m.league, m.season, m.date, m.home_team, m.away_team, m.outcome]
                       + [f"{x:.6f}" for name in tuned for x in tuned[name][i]])


def write_forecast_hashes(paths: list[Path], out: Path) -> None:
    """SHA-256 of the forecast files, committed to git BEFORE any odds are obtained, so
    anyone can later check the forecasts were not changed after seeing prices."""
    import hashlib
    out.parent.mkdir(parents=True, exist_ok=True)
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.exists()}
    out.write_text(json.dumps(hashes, indent=2, sort_keys=True) + "\n")


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--matches", type=Path, default=ROOT / "data/clean/matches.csv")
    p.add_argument("--holdout-season", default=None,
                   help="default: latest season with no matches still scheduled")
    p.add_argument("--report", type=Path, default=ROOT / "docs/evaluation_report.md")
    p.add_argument("--comparison", type=Path, default=ROOT / "reports/model_comparison.md")
    p.add_argument("--forecasts", type=Path, default=ROOT / "data/clean/forecasts.csv")
    a = p.parse_args(argv)

    ev = evaluate(load_matches_csv(a.matches), a.holdout_season)
    info_path = a.matches.parent / "build_info.json"
    build_info = json.loads(info_path.read_text()) if info_path.exists() else {}
    for path, text in ((a.report, render(ev)), (a.comparison, render_comparison(ev, build_info))):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    write_forecasts(ev, a.forecasts)
    write_forecast_hashes([a.forecasts, a.forecasts.with_name(a.forecasts.stem + "_validation.csv")],
                          ROOT / "reports/forecast_hashes.json")
    s = ev["split"]
    print(f"holdout {s.holdout_season}: train {len(s.train)}, test {len(s.test)} -> {a.report}, {a.comparison}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
