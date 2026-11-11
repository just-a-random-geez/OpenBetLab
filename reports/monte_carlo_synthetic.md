# Monte Carlo Risk Simulation (synthetic)

> **This simulation measures RISK, not edge.** It replays the strategy on the same set of matches 10,000 times with results drawn at random from an *assumed* truth. Under "model" truth the model is assumed to be right, so a profit there is built in, not discovered. Under "market" truth the market is assumed right - the model then has no edge, and the result shows what that costs. Only the pre-registered backtest can say anything about a real edge.

- Seasons simulated per scenario: 10,000; random seed 20261111 (fixed - re-running gives identical numbers)
- Every scenario uses the same simulated results for the same match, so scenarios are compared on equal luck.
- Start bankroll £100. Ruin = bankroll below £1 (Betfair's minimum stake). Stakes below £1 are raised to £1. Bets placed on the same day are sized from that morning's bankroll and must fit in it together.
- **Read the 'market' rows first**: they show the strategy when the model has no edge. 'Model' rows assume the model is right, so their profit is built in.
- Commission: 5%
- **SYNTHETIC season (2,000 made-up matches)**: illustrates the method only; says nothing about the real model or market.

Profit columns are £ at the end of the season (median and 5th / 95th percentile). 'Worst drawdown' = median across seasons of the biggest fall from a peak.

| Scenario | Bets/season | Median £ | 5th pct £ | 95th pct £ | P(profit) | P(lose 50%) | P(ruin) | Typical worst drawdown |
|---|---|---|---|---|---|---|---|---|
| market: base (flat £1, singles, odds 1.5-5) | 872 | -38.82 | -99.48 | +33.11 | 18.9% | 52.1% | 11.0% | 57.3% |
| market: flat 1% of bankroll, rollover | 872 | -40.49 | -99.49 | +29.98 | 16.1% | 54.2% | 11.4% | 59.0% |
| market: Kelly 25%, no rollover | 872 | -55.20 | -99.89 | +48.63 | 19.4% | 68.6% | 32.1% | 77.1% |
| market: Kelly 25%, rollover | 872 | -53.34 | -99.69 | +38.99 | 13.9% | 68.3% | 18.4% | 71.4% |
| market: Kelly 50%, rollover | 872 | -89.25 | -99.87 | +29.85 | 8.2% | 90.4% | 45.1% | 96.1% |
| market: parlay 2 legs | 418 | -29.26 | -99.74 | +78.50 | 32.7% | 55.7% | 20.3% | 62.9% |
| market: parlay 3 legs | 266 | -38.52 | -100.00 | +144.92 | 36.5% | 66.5% | 34.5% | 78.7% |
| market: parlay 4 legs | 196 | -99.29 | -100.00 | +266.76 | 31.3% | 76.0% | 53.4% | 99.4% |
| market: odds 1.5-3.0 | 310 | -12.05 | -45.09 | +21.63 | 27.7% | 4.2% | 0.0% | 24.5% |
| market: odds 2.0-10.0 | 858 | -38.51 | -99.54 | +33.92 | 19.6% | 53.0% | 12.1% | 58.1% |
| model: base (flat £1, singles, odds 1.5-5) | 872 | +92.08 | +17.94 | +166.83 | 97.8% | 0.6% | 0.0% | 16.2% |
| model: flat 1% of bankroll, rollover | 872 | +127.54 | +11.46 | +371.85 | 97.1% | 0.7% | 0.0% | 22.3% |
| model: Kelly 25%, no rollover | 872 | +146.73 | +39.93 | +252.72 | 98.9% | 1.9% | 0.1% | 19.0% |
| model: Kelly 25%, rollover | 872 | +240.64 | +26.53 | +798.62 | 97.9% | 1.4% | 0.0% | 27.6% |
| model: Kelly 50%, rollover | 872 | +682.74 | +10.54 | +5268.88 | 96.0% | 9.9% | 0.2% | 49.8% |
| model: parlay 2 legs | 418 | +106.51 | -10.70 | +230.35 | 93.2% | 6.9% | 0.4% | 25.6% |
| model: parlay 3 legs | 266 | +112.59 | -99.25 | +329.58 | 82.7% | 27.5% | 6.5% | 41.0% |
| model: parlay 4 legs | 196 | +85.91 | -100.00 | +510.36 | 62.8% | 53.8% | 26.3% | 63.0% |
| model: odds 1.5-3.0 | 310 | +29.18 | -3.95 | +62.91 | 92.5% | 0.0% | 0.0% | 10.7% |
| model: odds 2.0-10.0 | 858 | +92.91 | +15.46 | +169.03 | 97.5% | 0.9% | 0.0% | 16.8% |
| model 2% overconfident | 872 | +72.89 | -2.55 | +147.50 | 94.4% | 1.7% | 0.0% | 18.7% |
| model 5% overconfident | 872 | +43.77 | -30.95 | +117.34 | 83.6% | 5.6% | 0.2% | 23.8% |
| model 2% overconfident, Kelly 25% rollover | 872 | +163.81 | -3.23 | +597.53 | 94.4% | 3.0% | 0.1% | 30.4% |
| model 5% overconfident, Kelly 25% rollover | 872 | +79.23 | -39.10 | +375.63 | 83.3% | 9.2% | 0.4% | 35.9% |

Definitions: *rollover* = stakes sized on the current bankroll (winnings are re-staked); *no rollover* = stakes sized on the starting £100. Flat = £1 (or 1% of bankroll with rollover). Kelly x% = x% of the Kelly stake computed from the MODEL's probability and the odds after commission. Parlays are hypothetical (Betfair Exchange has no multiples): same-day qualifying picks grouped by highest edge. Overconfident x% = when the model backs an outcome, its true chance is x% lower (relative) than the model says.
