# OpenBetLab Research Report v1

Date: 2026-11-11

## The answer, first

**No betting edge has been shown. Gate 1 is NOT PASSED.**

- The betting backtest has **never been run**. No Betfair odds have been loaded, and the
  research plan (`docs/RESEARCH_PLAN_v1.md`) is still a draft. The Gate 1 criteria have
  not been supplied, so it can't be frozen.
- What *has* been shown: the models predict match results better than simple league
  averages, by a clear and repeatable margin. That is **not** an edge against the betting
  market. The market has not been scored yet, and published experience suggests it is
  more accurate than these models.
- Even when the backtest runs, one season (~500–650 bets) can only detect a very large
  edge (return above ~10–15%). See section 7.

## 1. Data used

| Data | Source | Licence | Used for |
|---|---|---|---|
| Match results, English leagues 1–4 (en.1–en.4), 2010-11 to 2026-27 | openfootball/football.json @ `e6744429` | CC0-1.0 (public domain) | Models, evaluation |
| Betfair Exchange match odds, BASIC tier | Betfair Historic Data | Personal use only | Odds handling and backtest. **Not yet loaded** |

Data cleaning (`docs/data_quality_report.md`):
- 26,875 rows read, giving 26,863 clean matches. 12 exact duplicates were removed and 39 club spellings merged.
- Missing values are left empty and never invented. 605 past matches have no result upstream.
- **Untrustworthy dates are flagged and excluded from evaluation:**
  - 276 League One 2025-26 matches dated 2025 instead of 2026 (85 of them have results).
  - 143 Premier League / Championship 2019-20 restart games dated July 2019 instead of July 2020. These were found by the independent review.
- **Gaps upstream:** no League One/Two files for 2016-18 and 2021-24, and no Championship files for 2016-18.

## 2. Models

All models forecast home / draw / away probabilities. Each forecast uses only matches
played on **earlier dates**. Settings were chosen on the **2024-25** season, which is part
of the training data.

| Model | Idea | Chosen settings |
|---|---|---|
| League average (baseline) | each league's past home/draw/away rates | – |
| Poisson | team attack/defence → expected goals → score probabilities | half-life 365 days, prior 10 goals |
| Poisson, no time decay | same, all past matches weighted equally | prior 10 goals |
| Dixon-Coles | Poisson + low-score correction | half-life 365 days, prior 10 goals |
| Elo | team ratings → rating gap → probabilities | K 30, home advantage 100, promotion gap 50, season pull-back 40% |
| + calibration | 3-number correction fitted on 2024-25 forecasts | – |

The pre-registered model is **Poisson**, because it had the lowest validation log loss
(1.0371 vs Dixon-Coles 1.0376 and Elo 1.0385).

## 3. Strategy rules (draft plan, not yet frozen)

- **Bets:** back bets on Betfair Match Odds, en.1–en.4, singles only.
- **Price:** the last traded price **2 hours before kick-off**. All three prices must exist, each traded at most 60 minutes before the pick time, and the pick time must fall on the match day.
- **Which bets:** at least 5% edge after 5% commission, odds 1.50–5.00, at most one bet per match, flat £1 stakes from a £100 bankroll.
- **What it would take:** ROI after commission above 0, a 95% CI that excludes 0, and positive average closing-line value. The Gate 1 criteria are still to be copied in.

## 4. Out-of-sample results: prediction accuracy (held-out season 2025-26)

1,484 played matches: Premier League (en.1) 380, Championship (en.2) 557, League One (en.3) 271, League Two (en.4) 276.
Lower is better. The 95% ranges are ±1.96 standard errors over matches.

| Model | Log loss [95% range] | Brier [95% range] |
|---|---|---|
| 1/3 each | 1.0986 | 0.6667 |
| League average | 1.0754 [1.0645, 1.0864] | 0.6508 [0.6433, 0.6583] |
| Poisson, no decay | 1.0569 [1.0394, 1.0745] | 0.6371 [0.6247, 0.6495] |
| **Poisson** (plan model) | **1.0404 [1.0239, 1.0568]** | **0.6254 [0.6137, 0.6371]** |
| Dixon-Coles | 1.0401 [1.0237, 1.0564] | 0.6252 [0.6135, 0.6368] |
| Elo | 1.0360 [1.0199, 1.0520] | 0.6228 [0.6113, 0.6343] |
| Poisson calibrated | 1.0404 [1.0241, 1.0568] | 0.6256 [0.6140, 0.6372] |
| Elo calibrated | 1.0358 [1.0195, 1.0522] | 0.6227 [0.6110, 0.6344] |

Paired differences (same matches; negative = first model better):

| Comparison | Log loss difference [95% range] | Verdict |
|---|---|---|
| Poisson − league average | −0.0351 [−0.0466, −0.0235] | Poisson clearly better |
| Elo − league average | −0.0395 [−0.0512, −0.0277] | Elo clearly better |
| Elo − Poisson | −0.0044 [−0.0120, +0.0032] | no clear difference |
| Dixon-Coles − Poisson | −0.0003 [−0.0013, +0.0006] | no clear difference |
| Poisson − Poisson without time decay | −0.0166 [−0.0268, −0.0063] | time decay clearly helps |
| Calibrated − raw (all three models) | within ±0.0002 | calibration changes nothing |

**What this means:**
- The models are useful forecasters compared with a naive baseline.
- The ranges assume matches are independent. Real uncertainty is a bit wider, but the
  "clearly better" results have a large margin.
- None of this says the models beat the betting market.

## 5. Out-of-sample results: betting

**None.** No Betfair odds have been loaded and the plan is not frozen. The backtest
command refuses to run until the plan is FROZEN.

| Measure | Result |
|---|---|
| Number of bets | not run |
| Hit rate | not run |
| ROI after commission [95% range] | not run |
| Average closing-line value | not run |
| Worst drawdown, longest losing run, £100 bankroll | not run |
| Model vs closing market (Brier, log loss) | not run |

## 6. Simulation results (risk, not edge)

The Monte Carlo ran on a **synthetic, made-up season**: 2,000 invented matches, 10,000
simulated seasons per scenario, seed 20261111. Its numbers say **nothing** about our model
or the real market. They only show the shape of the risks. A real-odds run needs Betfair
data.

| Scenario (synthetic) | If the market is right (no edge) | If the model is right |
|---|---|---|
| Base: flat £1, singles | median −£39; 52% chance of halving bankroll; 11% ruin | median +£92 |
| Kelly 25%, rollover | median −£53; 18% ruin | median +£241 |
| Half-Kelly, rollover | median −£89; 45% ruin | median +£683 |
| 4-leg parlays | 53% ruin | 26% ruin even with the edge assumed |
| Model 5% overconfident | – | median roughly halves (+£44) |

**Lessons:** with no edge, commission steadily drains the bankroll. Kelly, compounding
and parlays multiply the damage. A small overconfidence in the model wipes out much of
any assumed edge.

## 7. Reviewer findings (`reports/review_v1.md`)

Three independent reviewers (maths, data leakage, devil's advocate). 16 issues were fixed,
including:
- **An in-play price leak:** a market going in-play early could let in-play trades count as the closing or 2h price.
- **143 misdated training matches:** the 2019-20 restart games dated a year early.
- **Stale or partial pick prices** were allowed.
- **The Monte Carlo ignored Betfair's £1 minimum stake**, which hid the ruin risk of Kelly and compounding.

After the fixes, the accuracy conclusions are unchanged and the risk conclusions are worse.

**Open, critical: sample size.** Flat bets at odds ~2.5 vary by about ±1.2 units each.
Detecting a true ROI of 3% with 80% power needs ~12,500 bets. Detecting 5% needs ~4,500.
One season gives ~500–650 bets, which can only detect an ROI above ~10–15%. A "pass" from
one season would more likely be luck or optimistic prices than a real edge. Options are
listed in the plan (§6): pool seasons, make closing-line value the main measure, or accept
the limit openly.

Other open points:
- The held-out League One/Two results stop around December 2025.
- Play-off matches are still included.
- The market should be scored before any betting test.
- Betfair BASIC prices may not have been backable at that size.

## 8. Gate 1: PASS / FAIL

The Gate 1 criteria from the guide have **not been provided**, so they can't be quoted
here. Each criterion below is the draft plan's own "no edge" rule. Until the backtest runs,
every one is **NOT PASSED**.

| Criterion (draft plan §5) | Result | Status |
|---|---|---|
| Gate 1 criteria from the guide | not supplied | **NOT PASSED (cannot be evaluated)** |
| Enough qualifying bets (N from Gate 1) | no bets; N not set | **NOT PASSED** |
| ROI after commission > 0 | not run | **NOT PASSED** |
| 95% CI for ROI excludes 0 | not run | **NOT PASSED** |
| Average closing-line value > 0 | not run | **NOT PASSED** |
| **Overall** | | **FAIL: no edge shown** |

To get a real PASS/FAIL:
1. Paste the Gate 1 criteria.
2. Decide the open points in plan §6.
3. Freeze the plan.
4. Add the Betfair files to `data/raw/betfair/` and run the commands below.

## 9. Reproduce every number

```bash
pip install -e ".[dev]"
python scripts/fetch_openfootball.py                           # data, pinned upstream commit
python -m openbetlab.data.build --as-of 2026-11-11             # section 1 -> docs/data_quality_report.md
python -m openbetlab.evaluation.run --holdout-season 2025-26   # sections 2, 4 -> docs/evaluation_report.md,
                                                               #   reports/model_comparison.md, data/clean/forecasts*.csv
python -m openbetlab.simulation.run --source synthetic         # section 6 -> reports/monte_carlo_synthetic.md
pytest                                                         # 180 tests incl. no-leakage proofs
```

The 95% ranges in section 4 are mean ± 1.96 × SD/√n of the per-match scores in
`data/clean/forecasts.csv`. For any model or pair of models:

```bash
python - <<'EOF'
import csv, math
rows = list(csv.DictReader(open("data/clean/forecasts.csv")))
col = {"H": "home", "D": "draw", "A": "away"}
def ll(m, r): return -math.log(max(float(r[f"{m}_{col[r['outcome']]}"]), 1e-15))
def ci(v):
    mu = sum(v) / len(v); sd = (sum((x - mu) ** 2 for x in v) / (len(v) - 1)) ** .5
    return round(mu, 4), round(mu - 1.96 * sd / len(v) ** .5, 4), round(mu + 1.96 * sd / len(v) ** .5, 4)
print("poisson", ci([ll("poisson", r) for r in rows]))
print("elo - poisson", ci([ll("elo", r) - ll("poisson", r) for r in rows]))
EOF
```

Forecast files can be checked against `reports/forecast_hashes.json` (SHA-256).

After the plan is frozen and Betfair files are in `data/raw/betfair/`:

```bash
python -m openbetlab.odds.build                         # odds tables (private, gitignored)
python -m openbetlab.odds.compare --source holdout      # model vs closing market
python -m openbetlab.backtest.run                       # section 5 + Gate 1 inputs
python -m openbetlab.simulation.run --source holdout    # section 6 on real odds
```
