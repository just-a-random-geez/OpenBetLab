# Model Comparison

> **No betting edge is claimed.** These numbers measure how accurate the probabilities are against actual results. They were not compared with bookmaker odds, include no margins, staking or costs, and a better score than a naive baseline does not imply profit.

## Reproduce

```bash
pip install -e ".[dev]"
python scripts/fetch_openfootball.py
python -m openbetlab.data.build --as-of 2026-11-11
python -m openbetlab.evaluation.run --holdout-season 2025-26
```

- Data: openfootball/football.json @ `e6744429ee395bc86f247348c6184bb08d4eb361` (CC0-1.0), leagues en.1, en.2, en.3, en.4, built with as-of date 2026-11-11
- Python 3.13.18, numpy 2.5.3
- Deterministic: no random numbers are used, so the same inputs give the same output.

## Setup

- Held-out (test) season: **2025-26**, 1484 played matches (home 43.4%, draw 25.7%, away 30.9%)
- Train: 23671 matches, 2010-11 to 2024-25. Model settings and calibration were chosen using 2024-25 (a train season) only.
- Every forecast uses only matches played before that match's date.

## Scores on the held-out season

Lower is better for both. Brier: 0 perfect, 2 worst. Log loss: penalises confident mistakes most.

| Model | What it is | Brier | Log loss |
|---|---|---|---|
| `uniform` | 1/3 each - knows nothing | 0.6667 | 1.0986 |
| `league_average` | each league's home/draw/away rates from the train seasons | 0.6508 | 1.0754 |
| `poisson_no_decay` | Poisson goals model, all past matches weighted equally | 0.6372 | 1.0571 |
| `poisson` | Poisson goals model with time decay (walk-forward) | 0.6254 | 1.0404 |
| `poisson_calibrated` | poisson + calibration step | 0.6256 | 1.0404 |
| `dixon_coles` | Poisson + Dixon-Coles low-score correction (walk-forward) | 0.6252 | 1.0401 |
| `dixon_coles_calibrated` | dixon_coles + calibration step | 0.6254 | 1.0402 |
| `elo` | Elo ratings + ordered-logit probabilities | 0.6228 | 1.0360 |
| `elo_calibrated` | elo + calibration step | 0.6227 | 1.0358 |

### Paired differences

Mean per-match difference (first minus second; negative = first better) and how many standard errors that is. Beyond ±2 SE is unlikely to be chance.

| Comparison | Brier diff | Log loss diff | Verdict (log loss) |
|---|---|---|---|
| poisson vs league_average | -0.0254 (-5.9 SE) | -0.0350 (-5.9 SE) | poisson better |
| elo vs league_average | -0.0280 (-6.5 SE) | -0.0394 (-6.6 SE) | elo better |
| elo vs poisson | -0.0026 (-1.0 SE) | -0.0044 (-1.1 SE) | no clear difference |
| dixon_coles vs poisson | -0.0002 (-0.9 SE) | -0.0003 (-0.6 SE) | no clear difference |
| poisson vs poisson_no_decay | -0.0118 (-3.2 SE) | -0.0167 (-3.2 SE) | poisson better |
| poisson_calibrated vs poisson | +0.0002 (+0.4 SE) | +0.0001 (+0.1 SE) | no clear difference |
| dixon_coles_calibrated vs dixon_coles | +0.0002 (+0.5 SE) | +0.0002 (+0.2 SE) | no clear difference |
| elo_calibrated vs elo | -0.0001 (-0.3 SE) | -0.0001 (-0.4 SE) | no clear difference |

## Calibration step

calibrated p ∝ exp(b + w · log p), fitted by maximum likelihood on each model's walk-forward forecasts for the validation season only. w > 1 = make forecasts more confident; b shifts probability towards draw / away.

| Model | Fitted on | Matches | w | b draw | b away |
|---|---|---|---|---|---|
| `poisson` | 2024-25 | 2041 | 1.017 | +0.041 | -0.041 |
| `dixon_coles` | 2024-25 | 2041 | 1.009 | +0.036 | -0.043 |
| `elo` | 2024-25 | 2041 | 1.035 | +0.025 | -0.014 |

## Calibration tables (held-out season)

Forecasts grouped into 10%-wide buckets per outcome. *Actual* = how often the outcome happened. Buckets with few matches are noisy.

### `uniform`

| Outcome | Bucket | Matches | Mean predicted | Actual | Gap |
|---|---|---|---|---|---|
| home | 0.3-0.4 | 1484 | 0.333 | 0.434 | +0.101 |
| draw | 0.3-0.4 | 1484 | 0.333 | 0.257 | -0.076 |
| away | 0.3-0.4 | 1484 | 0.333 | 0.309 | -0.025 |

### `league_average`

| Outcome | Bucket | Matches | Mean predicted | Actual | Gap |
|---|---|---|---|---|---|
| home | 0.4-0.5 | 1484 | 0.431 | 0.434 | +0.003 |
| draw | 0.2-0.3 | 1484 | 0.263 | 0.257 | -0.005 |
| away | 0.2-0.3 | 557 | 0.299 | 0.318 | +0.019 |
| away | 0.3-0.4 | 927 | 0.311 | 0.303 | -0.008 |

### `poisson_no_decay`

| Outcome | Bucket | Matches | Mean predicted | Actual | Gap |
|---|---|---|---|---|---|
| home | 0.1-0.2 | 22 | 0.166 | 0.227 | +0.061 |
| home | 0.2-0.3 | 130 | 0.260 | 0.292 | +0.032 |
| home | 0.3-0.4 | 424 | 0.358 | 0.356 | -0.002 |
| home | 0.4-0.5 | 551 | 0.449 | 0.468 | +0.019 |
| home | 0.5-0.6 | 238 | 0.542 | 0.529 | -0.013 |
| home | 0.6-0.7 | 90 | 0.640 | 0.522 | -0.117 |
| home | 0.7-0.8 | 26 | 0.743 | 0.615 | -0.127 |
| home | 0.8-0.9 | 3 | 0.819 | 1.000 | +0.181 |
| draw | 0.1-0.2 | 71 | 0.175 | 0.254 | +0.078 |
| draw | 0.2-0.3 | 1413 | 0.255 | 0.258 | +0.002 |
| away | 0.0-0.1 | 15 | 0.079 | 0.133 | +0.054 |
| away | 0.1-0.2 | 158 | 0.164 | 0.234 | +0.071 |
| away | 0.2-0.3 | 524 | 0.257 | 0.235 | -0.022 |
| away | 0.3-0.4 | 536 | 0.344 | 0.345 | +0.001 |
| away | 0.4-0.5 | 179 | 0.443 | 0.425 | -0.018 |
| away | 0.5-0.6 | 58 | 0.536 | 0.483 | -0.053 |
| away | 0.6-0.7 | 14 | 0.654 | 0.500 | -0.154 |

### `poisson`

| Outcome | Bucket | Matches | Mean predicted | Actual | Gap |
|---|---|---|---|---|---|
| home | 0.1-0.2 | 18 | 0.171 | 0.111 | -0.060 |
| home | 0.2-0.3 | 121 | 0.264 | 0.207 | -0.057 |
| home | 0.3-0.4 | 448 | 0.358 | 0.371 | +0.013 |
| home | 0.4-0.5 | 548 | 0.448 | 0.438 | -0.010 |
| home | 0.5-0.6 | 260 | 0.542 | 0.558 | +0.016 |
| home | 0.6-0.7 | 75 | 0.636 | 0.720 | +0.084 |
| home | 0.7-0.8 | 13 | 0.745 | 0.846 | +0.102 |
| home | 0.8-0.9 | 1 | 0.802 | 1.000 | +0.198 |
| draw | 0.1-0.2 | 42 | 0.179 | 0.238 | +0.059 |
| draw | 0.2-0.3 | 1383 | 0.256 | 0.258 | +0.003 |
| draw | 0.3-0.4 | 59 | 0.310 | 0.254 | -0.056 |
| away | 0.0-0.1 | 9 | 0.086 | 0.000 | -0.086 |
| away | 0.1-0.2 | 141 | 0.169 | 0.163 | -0.006 |
| away | 0.2-0.3 | 560 | 0.257 | 0.255 | -0.001 |
| away | 0.3-0.4 | 532 | 0.344 | 0.335 | -0.009 |
| away | 0.4-0.5 | 182 | 0.438 | 0.456 | +0.018 |
| away | 0.5-0.6 | 48 | 0.537 | 0.479 | -0.057 |
| away | 0.6-0.7 | 11 | 0.634 | 0.636 | +0.002 |
| away | 0.7-0.8 | 1 | 0.727 | 1.000 | +0.273 |

### `poisson_calibrated`

| Outcome | Bucket | Matches | Mean predicted | Actual | Gap |
|---|---|---|---|---|---|
| home | 0.1-0.2 | 18 | 0.171 | 0.111 | -0.060 |
| home | 0.2-0.3 | 118 | 0.264 | 0.195 | -0.069 |
| home | 0.3-0.4 | 441 | 0.358 | 0.372 | +0.014 |
| home | 0.4-0.5 | 545 | 0.449 | 0.433 | -0.016 |
| home | 0.5-0.6 | 268 | 0.542 | 0.560 | +0.018 |
| home | 0.6-0.7 | 80 | 0.637 | 0.713 | +0.075 |
| home | 0.7-0.8 | 12 | 0.744 | 0.833 | +0.089 |
| home | 0.8-0.9 | 2 | 0.803 | 1.000 | +0.197 |
| draw | 0.1-0.2 | 31 | 0.176 | 0.226 | +0.050 |
| draw | 0.2-0.3 | 1310 | 0.262 | 0.255 | -0.007 |
| draw | 0.3-0.4 | 143 | 0.313 | 0.287 | -0.026 |
| away | 0.0-0.1 | 12 | 0.084 | 0.000 | -0.084 |
| away | 0.1-0.2 | 169 | 0.168 | 0.166 | -0.002 |
| away | 0.2-0.3 | 615 | 0.255 | 0.270 | +0.015 |
| away | 0.3-0.4 | 483 | 0.343 | 0.342 | -0.001 |
| away | 0.4-0.5 | 156 | 0.438 | 0.455 | +0.017 |
| away | 0.5-0.6 | 39 | 0.537 | 0.538 | +0.002 |
| away | 0.6-0.7 | 9 | 0.631 | 0.667 | +0.035 |
| away | 0.7-0.8 | 1 | 0.720 | 1.000 | +0.280 |

### `dixon_coles`

| Outcome | Bucket | Matches | Mean predicted | Actual | Gap |
|---|---|---|---|---|---|
| home | 0.1-0.2 | 19 | 0.169 | 0.105 | -0.064 |
| home | 0.2-0.3 | 121 | 0.263 | 0.207 | -0.057 |
| home | 0.3-0.4 | 450 | 0.357 | 0.369 | +0.012 |
| home | 0.4-0.5 | 546 | 0.448 | 0.438 | -0.010 |
| home | 0.5-0.6 | 260 | 0.542 | 0.565 | +0.023 |
| home | 0.6-0.7 | 74 | 0.635 | 0.716 | +0.081 |
| home | 0.7-0.8 | 14 | 0.748 | 0.857 | +0.109 |
| draw | 0.1-0.2 | 38 | 0.179 | 0.237 | +0.057 |
| draw | 0.2-0.3 | 1377 | 0.256 | 0.257 | +0.001 |
| draw | 0.3-0.4 | 69 | 0.311 | 0.275 | -0.035 |
| away | 0.0-0.1 | 10 | 0.087 | 0.000 | -0.087 |
| away | 0.1-0.2 | 138 | 0.169 | 0.152 | -0.016 |
| away | 0.2-0.3 | 567 | 0.257 | 0.263 | +0.006 |
| away | 0.3-0.4 | 528 | 0.344 | 0.331 | -0.012 |
| away | 0.4-0.5 | 180 | 0.437 | 0.456 | +0.018 |
| away | 0.5-0.6 | 51 | 0.535 | 0.471 | -0.065 |
| away | 0.6-0.7 | 9 | 0.638 | 0.667 | +0.029 |
| away | 0.7-0.8 | 1 | 0.721 | 1.000 | +0.279 |

### `dixon_coles_calibrated`

| Outcome | Bucket | Matches | Mean predicted | Actual | Gap |
|---|---|---|---|---|---|
| home | 0.1-0.2 | 18 | 0.169 | 0.056 | -0.113 |
| home | 0.2-0.3 | 116 | 0.263 | 0.216 | -0.048 |
| home | 0.3-0.4 | 450 | 0.358 | 0.367 | +0.009 |
| home | 0.4-0.5 | 544 | 0.449 | 0.434 | -0.015 |
| home | 0.5-0.6 | 268 | 0.543 | 0.567 | +0.024 |
| home | 0.6-0.7 | 74 | 0.637 | 0.716 | +0.079 |
| home | 0.7-0.8 | 14 | 0.750 | 0.857 | +0.107 |
| draw | 0.1-0.2 | 27 | 0.177 | 0.222 | +0.045 |
| draw | 0.2-0.3 | 1307 | 0.263 | 0.259 | -0.004 |
| draw | 0.3-0.4 | 150 | 0.313 | 0.247 | -0.067 |
| away | 0.0-0.1 | 12 | 0.084 | 0.000 | -0.084 |
| away | 0.1-0.2 | 169 | 0.168 | 0.166 | -0.002 |
| away | 0.2-0.3 | 622 | 0.255 | 0.270 | +0.015 |
| away | 0.3-0.4 | 479 | 0.343 | 0.340 | -0.002 |
| away | 0.4-0.5 | 156 | 0.438 | 0.474 | +0.037 |
| away | 0.5-0.6 | 36 | 0.534 | 0.500 | -0.034 |
| away | 0.6-0.7 | 9 | 0.626 | 0.667 | +0.041 |
| away | 0.7-0.8 | 1 | 0.711 | 1.000 | +0.289 |

### `elo`

| Outcome | Bucket | Matches | Mean predicted | Actual | Gap |
|---|---|---|---|---|---|
| home | 0.1-0.2 | 18 | 0.164 | 0.167 | +0.003 |
| home | 0.2-0.3 | 142 | 0.260 | 0.183 | -0.077 |
| home | 0.3-0.4 | 439 | 0.356 | 0.353 | -0.002 |
| home | 0.4-0.5 | 534 | 0.445 | 0.478 | +0.032 |
| home | 0.5-0.6 | 254 | 0.542 | 0.528 | -0.015 |
| home | 0.6-0.7 | 83 | 0.636 | 0.723 | +0.087 |
| home | 0.7-0.8 | 12 | 0.740 | 0.833 | +0.093 |
| home | 0.8-0.9 | 2 | 0.831 | 0.500 | -0.331 |
| draw | 0.1-0.2 | 33 | 0.173 | 0.212 | +0.039 |
| draw | 0.2-0.3 | 1451 | 0.266 | 0.258 | -0.007 |
| away | 0.0-0.1 | 8 | 0.083 | 0.000 | -0.083 |
| away | 0.1-0.2 | 162 | 0.167 | 0.160 | -0.007 |
| away | 0.2-0.3 | 556 | 0.255 | 0.234 | -0.021 |
| away | 0.3-0.4 | 535 | 0.343 | 0.376 | +0.032 |
| away | 0.4-0.5 | 168 | 0.440 | 0.417 | -0.024 |
| away | 0.5-0.6 | 46 | 0.534 | 0.543 | +0.009 |
| away | 0.6-0.7 | 6 | 0.635 | 0.667 | +0.032 |
| away | 0.7-0.8 | 3 | 0.719 | 0.667 | -0.052 |

### `elo_calibrated`

| Outcome | Bucket | Matches | Mean predicted | Actual | Gap |
|---|---|---|---|---|---|
| home | 0.1-0.2 | 19 | 0.161 | 0.158 | -0.003 |
| home | 0.2-0.3 | 146 | 0.259 | 0.185 | -0.074 |
| home | 0.3-0.4 | 422 | 0.355 | 0.344 | -0.011 |
| home | 0.4-0.5 | 525 | 0.445 | 0.484 | +0.039 |
| home | 0.5-0.6 | 262 | 0.541 | 0.523 | -0.018 |
| home | 0.6-0.7 | 93 | 0.636 | 0.688 | +0.052 |
| home | 0.7-0.8 | 14 | 0.736 | 0.857 | +0.121 |
| home | 0.8-0.9 | 3 | 0.828 | 0.667 | -0.162 |
| draw | 0.0-0.1 | 1 | 0.097 | 1.000 | +0.903 |
| draw | 0.1-0.2 | 33 | 0.174 | 0.212 | +0.038 |
| draw | 0.2-0.3 | 1450 | 0.270 | 0.258 | -0.012 |
| away | 0.0-0.1 | 10 | 0.081 | 0.000 | -0.081 |
| away | 0.1-0.2 | 197 | 0.167 | 0.147 | -0.020 |
| away | 0.2-0.3 | 570 | 0.255 | 0.251 | -0.005 |
| away | 0.3-0.4 | 493 | 0.343 | 0.385 | +0.042 |
| away | 0.4-0.5 | 160 | 0.440 | 0.412 | -0.028 |
| away | 0.5-0.6 | 45 | 0.536 | 0.533 | -0.002 |
| away | 0.6-0.7 | 6 | 0.638 | 0.667 | +0.029 |
| away | 0.7-0.8 | 3 | 0.724 | 0.667 | -0.057 |
