# Evaluation Report

## Split (by time, never shuffled)

- Train: 23671 played matches, seasons 2010-11 to 2024-25
- Test (out-of-sample): 1484 played matches, season 2025-26
- Later seasons not used: 145 matches
- Played matches excluded for an out-of-season date (can't be placed in time): 85
- Test-season actual rates: home 0.434, draw 0.257, away 0.309

## Scores on the test season

Lower is better. Reference: always 1/3 each = Brier 0.6667, log loss 1.0986.
Poisson forecasts are walk-forward: refitted before each match date on earlier matches only. The league-average baseline uses the train seasons only.

| Model | League | Matches | Brier | Log loss |
|---|---|---|---|---|
| poisson | ALL | 1484 | 0.6254 | 1.0404 |
| poisson | en.1 | 380 | 0.6161 | 1.0273 |
| poisson | en.2 | 557 | 0.6446 | 1.0668 |
| poisson | en.3 | 271 | 0.6015 | 1.0069 |
| poisson | en.4 | 276 | 0.6230 | 1.0379 |
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

## Is Poisson really better than the baseline?

Per-match score difference (Poisson minus league average). Negative = Poisson better. A gap larger than 2 standard errors is unlikely to be luck.

| Score | Mean difference | Std. error | Difference / SE | Clearly better? |
|---|---|---|---|---|
| Brier | -0.0254 | 0.0043 | -5.9 | yes |
| Log loss | -0.0350 | 0.0059 | -5.9 | yes |

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
