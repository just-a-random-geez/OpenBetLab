# Phase 2 – Evaluation framework (plain English)

Built *before* any real model, so every future model is judged the same way.

## How to run

```bash
python -m openbetlab.data.build          # Phase 1 output: data/clean/matches.csv
python -m openbetlab.evaluation.run      # writes docs/evaluation_report.md
pytest
```

## 1. Scores (how good is a forecast?)

A forecast is three probabilities: home win, draw, away win (they add up to 1).

- **Brier score** – for each match, add up the squared distance between each
  probability and what happened (1 for the outcome that happened, 0 for the
  others), then average over matches. 0 = perfect, 2 = totally wrong.
  Guessing 1/3 each always gives 0.667.
- **Log loss** – for each match, take the probability you gave to what
  actually happened and score `-ln(p)`, then average. It punishes confident
  mistakes very hard (giving 0% to something that happens is a near-infinite
  penalty). Guessing 1/3 each gives 1.099.
- **Calibration table** – groups forecasts into buckets (0–10%, 10–20%, …)
  and compares the average forecast with how often it actually happened.
  If we say "45%" a hundred times, it should happen about 45 times.
  Lower Brier/log loss = more accurate; small calibration gaps = honest
  probabilities. Both matter for betting.

## 2. Naive baseline

`LeagueAverageModel`: for each league, count how often home / draw / away
happened in the training seasons, and predict exactly those rates for
every match. It ignores the teams entirely. Any real model must beat it on
the test season, or it isn't adding anything. A `Uniform` model (1/3 each)
is reported too, as a "knows nothing" floor.

## 3. Time split (no peeking at the future)

- Matches are ordered by season and date – never shuffled.
- **Test season** = the most recent season with no fixtures still to be
  played (currently **2025-26**). It is held back and only used for scoring.
- **Train** = every season before it (2010-11 to 2024-25).
- Seasons after the test season (the in-progress 2026-27) are not used at all.
- Only matches with status *played* are used. Awarded results (decided off
  the pitch), cancelled games and missing results are left out.

## Current result

See `docs/evaluation_report.md` and `docs/PHASE2_POISSON.md`. On the 2025-26
test season the league-average baseline scores Brier 0.6508 / log loss 1.0754
(1/3 each: 0.6667 / 1.0986).

Matches whose date falls outside their season (upstream typo, 85 played
League One 2025-26 matches) are excluded from evaluation: their real date is
unknown, so we can't guarantee a model only used earlier matches.

## Files

- `openbetlab/evaluation/metrics.py` – Brier, log loss, calibration table
- `openbetlab/evaluation/data.py` – load results, time split
- `openbetlab/evaluation/baseline.py` – league-average and uniform models
- `openbetlab/evaluation/run.py` – runs it all, writes the report
- `tests/test_metrics.py`, `tests/test_split_and_baseline.py`
