# Phase 2 – Calibration step and model report (plain English)

## What calibration means

A forecast is *calibrated* if things it calls "40%" happen about 40% of
the time. A model can rank teams well and still be systematically too
confident, too cautious, or under-rate draws. A calibration step is a small
correction applied on top of a model's probabilities.

## The step we added

```
calibrated probability ∝ exp(b + w × log(original probability))
```

Three numbers per model:
- **w** – confidence dial. Above 1: push forecasts further from 1/3.
  Below 1: pull them towards 1/3. Exactly 1: no change.
- **b draw, b away** – move a little probability towards / away from
  draws or away wins.

## Fitted only on training data

The correction must learn from forecasts the model made *without* knowing
the answer. So it is fitted on each model's walk-forward forecasts for
**2024-25** (the last training season, each forecast made from earlier
matches only), then applied **unchanged** to 2025-26. The held-out season
is never used to fit it. A test checks this.

## Result: no measurable change

| Model | w | b draw | b away | Log loss before → after |
|---|---|---|---|---|
| Poisson | 1.017 | +0.041 | −0.041 | 1.0404 → 1.0404 |
| Dixon-Coles | 1.009 | +0.036 | −0.043 | 1.0401 → 1.0402 |
| Elo | 1.035 | +0.025 | −0.014 | 1.0360 → 1.0358 |

The fitted corrections are almost "do nothing" (w ≈ 1, tiny biases). On
2024-25 the models were already well calibrated, so there was little to
fix, and the differences on 2025-26 are well inside noise (≤ 0.4 standard
errors). The step is kept because it is cheap and would catch a model that
*is* badly calibrated. The slight over-caution on strong home favourites
seen in the 2025-26 tables did not show up in 2024-25, so it may just be
noise.

## The model report

`reports/model_comparison.md` lists every model's Brier score, log loss,
paired comparisons and calibration table on the held-out season, plus the
exact commands and data version used.

**No betting edge is claimed.** These scores measure probability accuracy
against results only. Nothing has been compared with bookmaker odds, and
beating a naive baseline does not mean making a profit.

## Reproduce

```bash
pip install -e ".[dev]"
python scripts/fetch_openfootball.py
python -m openbetlab.data.build --as-of 2026-11-11
python -m openbetlab.evaluation.run --holdout-season 2025-26
```

## Files

- `openbetlab/evaluation/calibration.py` – the calibrator
- `openbetlab/evaluation/comparison.py` – writes `reports/model_comparison.md`
- `tests/test_calibration.py` – leaves good forecasts alone, fixes
  over-confidence and draw bias on new data, valid outputs
