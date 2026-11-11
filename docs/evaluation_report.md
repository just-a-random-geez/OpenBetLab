# Evaluation Report

## Split (by time, never shuffled)

- Train: 23671 played matches, seasons 2010-11 to 2024-25
- Test (out-of-sample): 1569 played matches, season 2025-26
- Later seasons not used: 145 matches
- Test-season actual rates: home 0.437, draw 0.258, away 0.305

## Scores on the test season

Lower is better. Reference: always 1/3 each = Brier 0.6667, log loss 1.0986.

| Model | League | Matches | Brier | Log loss |
|---|---|---|---|---|
| league_average | ALL | 1569 | 0.6503 | 1.0747 |
| league_average | en.1 | 380 | 0.6551 | 1.0823 |
| league_average | en.2 | 557 | 0.6560 | 1.0829 |
| league_average | en.3 | 356 | 0.6322 | 1.0483 |
| league_average | en.4 | 276 | 0.6553 | 1.0819 |
| uniform | ALL | 1569 | 0.6667 | 1.0986 |
| uniform | en.1 | 380 | 0.6667 | 1.0986 |
| uniform | en.2 | 557 | 0.6667 | 1.0986 |
| uniform | en.3 | 356 | 0.6667 | 1.0986 |
| uniform | en.4 | 276 | 0.6667 | 1.0986 |

In-sample (train) scores, for comparison only - not a test of skill:

| Model | Matches | Brier | Log loss |
|---|---|---|---|
| league_average | 23671 | 0.6514 | 1.0762 |
| uniform | 23671 | 0.6667 | 1.0986 |

## Calibration: league_average on the test season

Forecasts grouped by predicted probability; *actual* = how often that outcome happened. Well calibrated means actual ≈ predicted.

| Outcome | Bucket | Matches | Mean predicted | Actual | Gap |
|---|---|---|---|---|---|
| home | 0.4-0.5 | 1569 | 0.430 | 0.437 | +0.006 |
| draw | 0.2-0.3 | 1569 | 0.263 | 0.258 | -0.004 |
| away | 0.2-0.3 | 557 | 0.299 | 0.318 | +0.019 |
| away | 0.3-0.4 | 1012 | 0.311 | 0.298 | -0.013 |

League rates learned from the train seasons:

| League | Home | Draw | Away |
|---|---|---|---|
| en.1 | 0.449 | 0.240 | 0.311 |
| en.2 | 0.429 | 0.272 | 0.299 |
| en.3 | 0.425 | 0.260 | 0.314 |
| en.4 | 0.415 | 0.277 | 0.307 |
