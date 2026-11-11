# Phase 3 – Model vs market (plain English)

## How to run

```bash
python -m openbetlab.evaluation.run --holdout-season 2025-26   # saves data/clean/forecasts.csv
python -m openbetlab.odds.build                                 # needs Betfair files
python -m openbetlab.odds.compare                               # --model elo, --snapshot 2h ...
```

Outputs (contain Betfair prices → gitignored, personal use only):
- `data/odds/model_vs_market.csv` – every held-out match × outcome
- `reports/private/model_vs_market.md` – the report

## What is compared

For every held-out match (2025-26) that has a complete Betfair price:

| Column | Meaning |
|---|---|
| model_prob | the model's forecast, made only from earlier matches |
| market_fair_prob | Betfair closing price turned into a probability, margin removed |
| difference | model − market |
| edge | model probability × odds − 1 |
| edge_after_commission | same, but winnings reduced by commission (`config/settings.toml`) |

**Edge is just arithmetic on the model's own numbers.** If the model says
50% and the odds are 2.2, edge = 0.5 × 2.2 − 1 = +0.10. That only means the
model disagrees with the price. It is **not** a value bet: the model has
not been shown to beat the market, and nothing has been backtested.

## Which model

Chosen automatically by the lowest log loss on the **validation season**
(2024-25, training data), before looking at the held-out season or the
market. Currently **Poisson** (1.0371; Dixon-Coles 1.0376; Elo 1.0385).
Picking the model that happens to look best against the market would be
cheating. Every other model is also scored on the same matches for
reference.

## Is the model better than the market?

The report scores model and market on exactly the same matches (Brier and
log loss) and gives the per-match difference with its standard error:
- beyond −2 SE: model more accurate than the closing market;
- beyond +2 SE: model less accurate;
- otherwise: no clear difference.

Expect the market to win. Closing exchange prices pull in team news,
injuries and lots of money; our models only know past scores.

## Disagreements

Matches where model and market differ by at least 10 percentage points on
any outcome (`[compare] disagreement_threshold` in settings), largest gap
first, with both probabilities, the odds, the edge and the actual result.
These are places to investigate (e.g. a key injury the model can't know),
not bets.

## Files

- `openbetlab/odds/compare.py` – join, edge, scores, disagreements, report
- `openbetlab/evaluation/run.py` – now also writes `data/clean/forecasts.csv`
  and `forecasts.json` (validation scores)
- `tests/test_model_vs_market.py`
