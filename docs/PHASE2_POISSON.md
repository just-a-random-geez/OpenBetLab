# Phase 2 – Poisson goals model (plain English)

## The idea

Goals in football are rare, roughly independent events, so the number of
goals a team scores in a match is well described by a **Poisson
distribution**: tell it the *expected* goals and it gives the chance of
0, 1, 2, 3… goals.

For each match we estimate expected goals:

```
home expected goals = league home rate × home attack × away defence
away expected goals = league away rate × away attack × home defence
```

- **attack** 1.3 = scores 30% more than an average team in that league.
- **defence** 1.3 = concedes 30% more than average (a weak defence).
- **home / away rate** = average goals for home and away sides; the gap
  between them is home advantage.

From the two expected goals we get the chance of every score (0-0, 1-0,
2-1, …, up to 10 each), then add them up: home win = all scores where the
home side has more goals, etc. That gives the home / draw / away
probabilities.

## How strengths are estimated

- Per league, from that league's past matches.
- **Recent matches count more**: a match's weight halves every *half-life*
  days. Chosen half-life: **365 days**.
- **Shrinkage**: each team starts with 10 "average" pseudo-goals of
  evidence (the *prior*). A team with little data, e.g. just promoted,
  stays close to average instead of being judged on two lucky games.
  A team never seen in that league is treated as exactly average.
- If a league has no recent history (upstream has no League One/Two files
  for 2021-24), older matches are used, heavily down-weighted.

## No peeking at the future

- **Walk-forward**: before each match date we refit the model on every
  match played on *earlier* dates (including earlier test-season matches),
  then predict that day's matches. Matches on the same day are not used.
- Fitting on a match dated on/after the prediction date raises an error.
- A test proves forecasts don't change when a *later* result changes.
- Matches with an untrustworthy date (outside their season) are excluded.

## How the settings were chosen (without touching the test season)

Half-life (90/180/365/730 days) and prior (5/10/20 goals) were picked by
walk-forward on **2024-25**, the last *training* season, using only seasons
before it. Best: 365 days, 10 goals. Then the model was scored **once** on
2025-26.

## Result on the held-out season (2025-26, 1,484 matches)

| Model | Brier | Log loss |
|---|---|---|
| **Poisson** | **0.6254** | **1.0404** |
| League average (baseline) | 0.6508 | 1.0754 |
| 1/3 each | 0.6667 | 1.0986 |

Poisson is better in every league. The per-match improvement is about 6
standard errors, so it is not luck.

Calibration (see report): mid-range forecasts are accurate. At the
extremes the model is a bit too cautious – home sides given 60–80% won
72–85% of the time; home sides given 10–30% won less than predicted. The
shrinkage pulls teams towards average a little too much there. The model
also doesn't model draws specially (scores are assumed independent).

## Limitations (next steps)

- Teams' strength doesn't carry over between leagues: a promoted team
  starts as "average" in its new league, but promoted teams are usually
  below average.
- Home and away goals assumed independent (no draw adjustment, e.g.
  Dixon–Coles).
- Same home advantage for every team; play-off finals at neutral venues
  still get home advantage.

## Files

- `openbetlab/models/poisson.py` – model, fitting, walk-forward
- `openbetlab/evaluation/run.py` – tuning on 2024-25, scoring on 2025-26
- `tests/test_poisson.py` – maths, recovering known strengths from
  simulated data, shrinkage, time decay, no-future-leakage checks
