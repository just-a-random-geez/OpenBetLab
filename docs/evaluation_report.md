# Evaluation Report

## Split (by time, never shuffled)

- Train: 23671 played matches, seasons 2010-11 to 2024-25
- Test (out-of-sample): 1484 played matches, season 2025-26
- Later seasons not used: 145 matches
- Played matches excluded for an out-of-season date (can't be placed in time): 85
- Test-season actual rates: home 0.434, draw 0.257, away 0.309

## Scores on the test season

Lower is better. Reference: always 1/3 each = Brier 0.6667, log loss 1.0986.
Poisson forecasts are walk-forward: refitted before each match date on earlier matches only. Elo ratings are updated match by match, each match predicted with ratings from earlier dates only. The league-average baseline uses the train seasons only.

| Model | League | Matches | Brier | Log loss |
|---|---|---|---|---|
| poisson | ALL | 1484 | 0.6254 | 1.0404 |
| poisson | en.1 | 380 | 0.6161 | 1.0273 |
| poisson | en.2 | 557 | 0.6446 | 1.0668 |
| poisson | en.3 | 271 | 0.6015 | 1.0069 |
| poisson | en.4 | 276 | 0.6230 | 1.0379 |
| dixon_coles | ALL | 1484 | 0.6252 | 1.0401 |
| dixon_coles | en.1 | 380 | 0.6153 | 1.0258 |
| dixon_coles | en.2 | 557 | 0.6447 | 1.0670 |
| dixon_coles | en.3 | 271 | 0.6008 | 1.0065 |
| dixon_coles | en.4 | 276 | 0.6233 | 1.0383 |
| poisson_no_decay | ALL | 1484 | 0.6372 | 1.0571 |
| poisson_no_decay | en.1 | 380 | 0.6318 | 1.0494 |
| poisson_no_decay | en.2 | 557 | 0.6595 | 1.0871 |
| poisson_no_decay | en.3 | 271 | 0.5988 | 1.0052 |
| poisson_no_decay | en.4 | 276 | 0.6376 | 1.0580 |
| elo | ALL | 1484 | 0.6228 | 1.0360 |
| elo | en.1 | 380 | 0.6187 | 1.0290 |
| elo | en.2 | 557 | 0.6397 | 1.0592 |
| elo | en.3 | 271 | 0.5913 | 0.9936 |
| elo | en.4 | 276 | 0.6253 | 1.0404 |
| league_average | ALL | 1484 | 0.6508 | 1.0754 |
| league_average | en.1 | 380 | 0.6551 | 1.0823 |
| league_average | en.2 | 557 | 0.6560 | 1.0829 |
| league_average | en.3 | 271 | 0.6294 | 1.0439 |
| league_average | en.4 | 276 | 0.6553 | 1.0819 |
| uniform | ALL | 1484 | 0.6667 | 1.0986 |
| uniform | en.1 | 380 | 0.6667 | 1.0986 |
| uniform | en.2 | 557 | 0.6667 | 1.0986 |
| uniform | en.3 | 271 | 0.6667 | 1.0986 |
| uniform | en.4 | 276 | 0.6667 | 1.0986 |
| poisson_calibrated | ALL | 1484 | 0.6256 | 1.0404 |
| poisson_calibrated | en.1 | 380 | 0.6148 | 1.0249 |
| poisson_calibrated | en.2 | 557 | 0.6453 | 1.0678 |
| poisson_calibrated | en.3 | 271 | 0.6025 | 1.0085 |
| poisson_calibrated | en.4 | 276 | 0.6233 | 1.0380 |
| dixon_coles_calibrated | ALL | 1484 | 0.6254 | 1.0402 |
| dixon_coles_calibrated | en.1 | 380 | 0.6142 | 1.0239 |
| dixon_coles_calibrated | en.2 | 557 | 0.6454 | 1.0679 |
| dixon_coles_calibrated | en.3 | 271 | 0.6016 | 1.0078 |
| dixon_coles_calibrated | en.4 | 276 | 0.6238 | 1.0388 |
| elo_calibrated | ALL | 1484 | 0.6227 | 1.0358 |
| elo_calibrated | en.1 | 380 | 0.6185 | 1.0284 |
| elo_calibrated | en.2 | 557 | 0.6400 | 1.0597 |
| elo_calibrated | en.3 | 271 | 0.5908 | 0.9931 |
| elo_calibrated | en.4 | 276 | 0.6250 | 1.0399 |

## Are the differences real?

Per-match score difference (first model minus second). Negative = first model better. A gap larger than 2 standard errors is unlikely to be luck.

| Comparison | Score | Mean difference | Std. error | Difference / SE | Verdict |
|---|---|---|---|---|---|
| poisson vs league_average | Brier | -0.0254 | 0.0043 | -5.9 | poisson better |
| poisson vs league_average | Log loss | -0.0350 | 0.0059 | -5.9 | poisson better |
| elo vs league_average | Brier | -0.0280 | 0.0043 | -6.5 | elo better |
| elo vs league_average | Log loss | -0.0394 | 0.0060 | -6.6 | elo better |
| elo vs poisson | Brier | -0.0026 | 0.0027 | -1.0 | no clear difference |
| elo vs poisson | Log loss | -0.0044 | 0.0039 | -1.1 | no clear difference |
| dixon_coles vs poisson | Brier | -0.0002 | 0.0003 | -0.9 | no clear difference |
| dixon_coles vs poisson | Log loss | -0.0003 | 0.0005 | -0.6 | no clear difference |
| poisson vs poisson_no_decay | Brier | -0.0118 | 0.0037 | -3.2 | poisson better |
| poisson vs poisson_no_decay | Log loss | -0.0167 | 0.0052 | -3.2 | poisson better |

## Poisson settings (tuned on 2024-25, a train season)

Chosen: half-life **365 days**, prior **10 goals** (lowest validation log loss).

| Half-life (days) | Prior (goals) | Val. matches | Brier | Log loss |
|---|---|---|---|---|
| 90 | 5 | 2041 | 0.6293 | 1.0442 |
| 90 | 10 | 2041 | 0.6281 | 1.0429 |
| 90 | 20 | 2041 | 0.6301 | 1.0464 |
| 180 | 5 | 2041 | 0.6273 | 1.0415 |
| 180 | 10 | 2041 | 0.6259 | 1.0396 |
| 180 | 20 | 2041 | 0.6269 | 1.0416 |
| 365 | 5 | 2041 | 0.6253 | 1.0387 |
| 365 | 10 | 2041 | 0.6242 | 1.0371 |
| 365 | 20 | 2041 | 0.6245 | 1.0379 |
| 730 | 5 | 2041 | 0.6276 | 1.0422 |
| 730 | 10 | 2041 | 0.6267 | 1.0409 |
| 730 | 20 | 2041 | 0.6267 | 1.0411 |

## Dixon-Coles settings (tuned on 2024-25, a train season)

Chosen: half-life **365 days**, prior **10 goals**. Low-score correction rho per league (from the last fit, i.e. all matches before the final test date): en.1 -0.071, en.2 -0.039, en.3 +0.089, en.4 -0.017. rho near 0 = almost plain Poisson.

| Half-life (days) | Prior (goals) | Val. matches | Brier | Log loss |
|---|---|---|---|---|
| 90 | 5 | 2041 | 0.6306 | 1.0461 |
| 90 | 10 | 2041 | 0.6294 | 1.0449 |
| 90 | 20 | 2041 | 0.6314 | 1.0483 |
| 180 | 5 | 2041 | 0.6286 | 1.0434 |
| 180 | 10 | 2041 | 0.6273 | 1.0417 |
| 180 | 20 | 2041 | 0.6282 | 1.0436 |
| 365 | 5 | 2041 | 0.6256 | 1.0392 |
| 365 | 10 | 2041 | 0.6245 | 1.0376 |
| 365 | 20 | 2041 | 0.6249 | 1.0385 |
| 730 | 5 | 2041 | 0.6277 | 1.0424 |
| 730 | 10 | 2041 | 0.6268 | 1.0411 |
| 730 | 20 | 2041 | 0.6268 | 1.0413 |

`poisson_no_decay` = the Poisson model with every past match weighted equally (prior 10 goals), to measure what time decay adds.

## Elo settings (tuned on 2024-25, a train season)

Chosen: K **30**, home advantage **100**, promotion gap **50**, season regression **0.4** (lowest validation log loss of 144 combinations; top 10 shown).

| K | Home adv. | Promotion gap | Season regression | Val. matches | Brier | Log loss |
|---|---|---|---|---|---|---|
| 30 | 100 | 50 | 0.4 | 2041 | 0.6250 | 1.0385 |
| 30 | 75 | 50 | 0.4 | 2041 | 0.6250 | 1.0385 |
| 30 | 50 | 50 | 0.4 | 2041 | 0.6250 | 1.0386 |
| 40 | 100 | 100 | 0.2 | 2041 | 0.6251 | 1.0386 |
| 20 | 75 | 50 | 0.4 | 2041 | 0.6251 | 1.0386 |
| 30 | 100 | 50 | 0.2 | 2041 | 0.6251 | 1.0386 |
| 20 | 100 | 50 | 0.4 | 2041 | 0.6251 | 1.0387 |
| 20 | 50 | 50 | 0.4 | 2041 | 0.6251 | 1.0387 |
| 30 | 75 | 50 | 0.2 | 2041 | 0.6251 | 1.0387 |
| 40 | 100 | 100 | 0.4 | 2041 | 0.6252 | 1.0387 |

Rating gap -> probability mapping (fitted on train seasons): b = 0.5236 per 100 points, c1 = -0.8344, c2 = 0.3182. Equal ratings give home 0.421 / draw 0.276 / away 0.303.

## Calibration: poisson on the test season

*Actual* = how often that outcome happened. Well calibrated: actual ≈ predicted. Small buckets are noisy.

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

## Calibration: dixon_coles on the test season

*Actual* = how often that outcome happened. Well calibrated: actual ≈ predicted. Small buckets are noisy.

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

## Calibration: elo on the test season

*Actual* = how often that outcome happened. Well calibrated: actual ≈ predicted. Small buckets are noisy.

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

## Calibration: league_average on the test season

*Actual* = how often that outcome happened. Well calibrated: actual ≈ predicted. Small buckets are noisy.

| Outcome | Bucket | Matches | Mean predicted | Actual | Gap |
|---|---|---|---|---|---|
| home | 0.4-0.5 | 1484 | 0.431 | 0.434 | +0.003 |
| draw | 0.2-0.3 | 1484 | 0.263 | 0.257 | -0.005 |
| away | 0.2-0.3 | 557 | 0.299 | 0.318 | +0.019 |
| away | 0.3-0.4 | 927 | 0.311 | 0.303 | -0.008 |

League rates learned by the baseline from the train seasons:

| League | Home | Draw | Away |
|---|---|---|---|
| en.1 | 0.449 | 0.240 | 0.311 |
| en.2 | 0.429 | 0.272 | 0.299 |
| en.3 | 0.425 | 0.260 | 0.314 |
| en.4 | 0.415 | 0.277 | 0.307 |
