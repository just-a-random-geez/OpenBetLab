# Phase 2 – Dixon-Coles adjustment (plain English)

## What Dixon-Coles adds to the Poisson model

Dixon & Coles (1997) proposed two changes:

1. **Low-score correction.** Plain Poisson assumes home and away goals are
   independent. In practice 0-0 and 1-1 can be a bit more common (and 1-0 /
   0-1 a bit less) than that predicts. A single number per league, **rho**,
   nudges those four scores:
   - rho below 0 → more 0-0 and 1-1, fewer 1-0 / 0-1 (more draws);
   - rho = 0 → plain Poisson.
   All other scores are unchanged and total probability stays 100%.
2. **Time-decay weighting.** Recent matches count more than old ones.
   Our Poisson model **already had this** (weight halves every 365 days),
   so the new part is the low-score correction.

## How it's fitted (past data only)

- Attack / defence / home rates: exactly as the Poisson model.
- rho: chosen per league to best explain the low scores in the same
  time-weighted past matches (weighted maximum likelihood, strengths held
  fixed). The original paper fits everything at once; with rho this small
  the difference is negligible.
- Walk-forward like Poisson: refit before every match date using earlier
  matches only. Settings (half-life, prior) tuned on 2024-25; scored once
  on 2025-26.

## Does it help? Honest answer: **no, not measurably.**

Held-out season 2025-26, 1,484 matches:

| Model | Brier | Log loss |
|---|---|---|
| Poisson (with time decay) | 0.6254 | 1.0404 |
| **Dixon-Coles** (Poisson + low-score correction) | 0.6252 | 1.0401 |
| Poisson **without** time decay | 0.6372 | 1.0571 |
| Elo (for reference) | 0.6228 | 1.0360 |
| League average baseline | 0.6508 | 1.0754 |

Per-match paired comparison:

| Change | Log loss gain | Std. errors | Verdict |
|---|---|---|---|
| Low-score correction (DC vs Poisson) | 0.0003 | 0.6 | **no clear difference** |
| Time decay (Poisson vs no decay) | 0.0167 | 3.2 | **clearly better** |

- The low-score correction makes almost no difference. The fitted rho
  values are small (en.1 −0.07, en.2 −0.04, en.3 +0.09, en.4 −0.02) and
  don't even agree in sign across leagues. On the 2024-25 validation
  season it was slightly *worse* than plain Poisson.
- Draw calibration barely changes (main bucket: 25.6% predicted vs 25.7%
  actual for both).
- **Time decay is the part of Dixon-Coles that matters.** Treating a match
  from 2011 the same as last month clearly hurts.
- Elo is still the best single model, but its lead over Poisson /
  Dixon-Coles is within noise.

Why so little effect: the correction only touches the four lowest scores,
and only changes their probabilities by a few percent. Win/draw/loss
probabilities move by tenths of a percentage point. It would matter more
for correct-score or under/over-goals markets than for 1X2.

## Files

- `openbetlab/models/dixon_coles.py` – tau correction, rho fit, model
- `openbetlab/models/poisson.py` – time-decay fit (unchanged maths;
  added a hook so subclasses can fit extra parameters)
- `openbetlab/evaluation/run.py` – tuning, held-out scoring, ablation
- `tests/test_dixon_coles.py` – tau values, probabilities still sum to 1,
  rho=0 equals Poisson, rho recovered from simulated data, weights
  respected, no future leakage

The full evaluation now takes ~4 minutes (`python -m openbetlab.evaluation.run`).
