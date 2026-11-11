# Phase 2 – Elo rating model (plain English)

## The idea

Every team has one number, its **rating** (everyone starts at 1500).
Bigger number = stronger team.

**After each match** ratings move:
- Before kick-off we work out how many "points" the home side is expected
  to take (win = 1, draw = ½, loss = 0) from the rating gap, plus a home
  advantage bonus. Equal teams → 0.5 (+ home bonus).
- Result better than expected → home rating goes up, away rating goes
  down by the same amount. Worse than expected → the opposite.
- How far ratings move is set by **K** (chosen: 30). A shock result
  moves ratings a lot; an expected result barely moves them.

**Between seasons and leagues**
- New season: every rating is pulled 40% of the way back to the league
  average (squads change over the summer).
- Leagues never play each other, so a rating in League Two isn't
  comparable with one in the Premier League. When a team changes league
  it is reset to its new league's average, **minus 50** points if
  promoted, **plus 50** if relegated. A brand-new team starts at the
  league average.

## From ratings to home / draw / away

Elo only gives "expected points", not a draw chance. So we look at past
matches: for each rating gap, how often did home / draw / away happen?
A small curve (ordered logistic regression, 3 numbers) is fitted on the
**training seasons only** and turns any rating gap into three
probabilities. Example: equal ratings → home 42.1%, draw 27.6%, away
30.3%. The bigger the gap, the more the favourite's chance grows. The
first season (2010-11) is skipped for this fit because everyone starts
at 1500.

## Past data only

- Matches are processed in date order. Every match on a given date is
  predicted with ratings from **earlier dates**; that day's results are
  applied afterwards.
- The test season's results never touch the probability curve.
- Tests check that changing a later result never changes an earlier
  forecast.

## Settings

K, home advantage, promotion gap and season pull-back were chosen from
144 combinations on **2024-25** (a training season), predicting it from
earlier seasons only. Many settings score almost the same, so the choice
isn't fragile.

## Result on the held-out season (2025-26, 1,484 matches)

| Model | Brier | Log loss |
|---|---|---|
| **Elo** | **0.6228** | **1.0360** |
| Poisson | 0.6254 | 1.0404 |
| League average (baseline) | 0.6508 | 1.0754 |
| 1/3 each | 0.6667 | 1.0986 |

- Elo clearly beats the baseline (about 6.5 standard errors).
- Elo vs Poisson: Elo is slightly better, but the gap is about 1
  standard error. **That's within noise – treat them as equally good**
  on this data.
- Calibration (see `docs/evaluation_report.md`): good in the middle.
  Like Poisson it is a little too cautious on strong home favourites
  (given 60–80%, they won 72–91% – few matches, so noisy). Draw
  probabilities stay in a narrow 17–31% band; the draw rate itself is
  well matched (26.6% predicted vs 25.8% actual in the main bucket).

## Limitations

- Ignores goal margin (a 5-0 counts the same as 1-0).
- One home advantage for all teams; play-off finals at neutral venues
  still get it.
- Promotion/relegation adjustment is one number for every league.

## Files

- `openbetlab/models/elo.py` – ratings, league changes, probability curve
- `openbetlab/evaluation/run.py` – tuning on 2024-25, scoring on 2025-26
- `tests/test_elo.py`
