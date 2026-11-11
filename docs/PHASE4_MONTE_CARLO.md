# Phase 4 – Monte Carlo risk simulation (plain English)

## The one thing to remember

**A simulation measures RISK. It does not prove an edge.**

It takes one season's worth of betting opportunities and replays it 10,000
times, each time drawing the match results at random from an **assumed**
truth. It answers "if the truth were X, how bumpy would the ride be, and how
likely is it to go badly wrong?" It cannot answer "is the truth X?". Only
the pre-registered backtest (Phase 4) speaks to that.

## The two truths

| Truth | Meaning | What it shows |
|---|---|---|
| **model** | results happen with the model's probabilities | the *best case*: the edge is assumed, so a profit here is built in, not found |
| **market** | results happen with the market's fair probabilities | what happens if the model has *no* edge: commission and noise eat the bankroll |

Reality is unknown and probably closer to "market" (the closing market beat
nearly every simple model in published research).

## What is varied (one change at a time from the base case)

- **Base** = the research-plan rules: singles, £1 flat stakes, odds 1.50–5.00,
  edge ≥ 5% after 5% commission, one bet per match, £100 start.
- **Staking**: flat £1; flat 1% of current bankroll; Kelly 25% / 50%.
  Kelly sizes each bet from the model's own probability and the odds after
  commission, so it bets more when the model is more confident.
- **Rollover vs no rollover**: rollover = stakes sized on the *current*
  bankroll (winnings re-staked, losses shrink stakes); no rollover = sized on
  the starting £100.
- **Parlays 1–4 legs**: same-day qualifying picks combined (hypothetical,
  Betfair Exchange has no multiples).
- **Odds range**: 1.50–3.00 and 2.00–10.00 as well as the base 1.50–5.00.
- **Overconfident model**: when the model backs an outcome, its true chance
  is 2% or 5% lower (relative) than claimed – e.g. "50%" is really 49% / 47.5%.

## What is reported per scenario

Median profit after a season, 5th / 95th percentile, chance of finishing in
profit, chance of the bankroll ever dropping to £50 or below, chance of ruin
(below £1, Betfair's minimum stake), and the typical (median) worst drawdown.

## Reproducible

Fixed seed (20261111). Each match's random results come from the seed and
the match number only, so the same match has the same luck in every
scenario (fair comparisons) and re-running gives identical numbers.

## How to run

```bash
python -m openbetlab.simulation.run --source synthetic   # works now, made-up data
python -m openbetlab.simulation.run                      # 2024-25 odds (validation season)
python -m openbetlab.simulation.run --source holdout     # 2025-26 - only after the plan is frozen
```

Real-odds runs need Betfair files and write to `reports/private/`
(gitignored). The default uses **2024-25** (a training season) on purpose:
looking at 2025-26 prices before the plan is frozen would weaken the
pre-registration. The held-out option refuses to run until then.

## Synthetic illustration (`reports/monte_carlo_synthetic.md`)

Made-up season, so the numbers mean nothing about our model. They show the
*shape* of the risks:
- Under "market" truth (no edge) the base strategy loses money in ~81% of
  seasons and has ~52% chance of halving the bankroll.
- Parlays raise the risk sharply: with 4 legs, ruin chance is 26% even when
  the model is assumed right, and 53% when it isn't.
- Half-Kelly with rollover has the biggest upside under "model" truth and the
  worst downside under "market" truth (90% chance of halving the bankroll).
- A model only 5% overconfident cuts the median profit roughly in half.

## Limitations

- Results are independent between matches (no shared shocks like weather or
  a bad weekend for favourites).
- Prices are taken as available in full (no liquidity limit, no slippage).
- With proportional staking, stakes can fall below Betfair's £1 minimum
  without the simulation stopping; ruin is only declared below £1 bankroll.
- Same-day bets are sized from that morning's bankroll and settled together.

## Files

- `openbetlab/simulation/montecarlo.py` – scenarios, bet planning, simulation
- `openbetlab/simulation/run.py` – inputs, report
- `tests/test_montecarlo.py` – reproducibility, no-edge-at-fair-odds check,
  profit equals model edge under model truth, overconfidence, parlays,
  Kelly, ruin, guard for held-out season
