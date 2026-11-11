# Monte Carlo Risk Simulation (synthetic)

> **This simulation measures RISK, not edge.** It replays the strategy on the same set of matches 10,000 times with results drawn at random from an *assumed* truth. Under "model" truth the model is assumed to be right, so a profit there is built in, not discovered. Under "market" truth the market is assumed right - the model then has no edge, and the result shows what that costs. Only the pre-registered backtest can say anything about a real edge.

- Seasons simulated per scenario: 10,000; random seed 20261111 (fixed - re-running gives identical numbers)
- Every scenario uses the same simulated results for the same match, so scenarios are compared on equal luck.
- Start bankroll £100. Ruin = bankroll below £1 (Betfair's minimum stake). Bets placed on the same day are sized from that morning's bankroll.
- Commission: 5%
- **SYNTHETIC season (2,000 made-up matches)**: illustrates the method only; says nothing about the real model or market.

Profit columns are £ at the end of the season (median and 5th / 95th percentile). 'Worst drawdown' = median across seasons of the biggest fall from a peak.

| Scenario | Bets/season | Median £ | 5th pct £ | 95th pct £ | P(profit) | P(lose 50%) | P(ruin) | Typical worst drawdown |
|---|---|---|---|---|---|---|---|---|
| model: base (flat £1, singles, odds 1.5-5) | 872 | +92.08 | +17.94 | +166.83 | 97.8% | 0.6% | 0.0% | 16.2% |
| model: flat 1% of bankroll, rollover | 872 | +125.64 | +7.78 | +370.75 | 96.5% | 0.3% | 0.0% | 22.1% |
| model: Kelly 25%, no rollover | 872 | +139.80 | +40.33 | +239.87 | 98.9% | 1.4% | 0.0% | 18.1% |
| model: Kelly 25%, rollover | 872 | +234.58 | +25.06 | +786.85 | 97.7% | 0.7% | 0.0% | 27.1% |
| model: Kelly 50%, rollover | 872 | +681.69 | +10.00 | +5268.88 | 95.8% | 9.8% | 0.0% | 49.8% |
| model: parlay 2 legs | 418 | +106.51 | -10.65 | +230.35 | 93.2% | 6.9% | 0.4% | 25.6% |
| model: parlay 3 legs | 266 | +112.59 | -100.00 | +329.58 | 82.7% | 27.5% | 6.4% | 41.0% |
| model: parlay 4 legs | 196 | +85.91 | -100.00 | +510.36 | 62.8% | 53.8% | 26.2% | 63.0% |
| model: odds 1.5-3.0 | 310 | +29.18 | -3.95 | +62.91 | 92.5% | 0.0% | 0.0% | 10.7% |
| model: odds 2.0-10.0 | 858 | +92.91 | +15.46 | +169.03 | 97.5% | 0.9% | 0.0% | 16.8% |
| model 2% overconfident | 872 | +72.89 | -2.55 | +147.50 | 94.4% | 1.7% | 0.0% | 18.7% |
| model 5% overconfident | 872 | +43.77 | -30.96 | +117.34 | 83.6% | 5.6% | 0.1% | 23.8% |
| model 2% overconfident, Kelly 25% rollover | 872 | +158.62 | -4.18 | +584.99 | 94.3% | 1.5% | 0.0% | 29.7% |
| model 5% overconfident, Kelly 25% rollover | 872 | +76.73 | -34.49 | +366.12 | 83.0% | 5.1% | 0.0% | 34.7% |
| market: base (flat £1, singles, odds 1.5-5) | 872 | -38.82 | -99.31 | +33.11 | 18.9% | 52.1% | 9.0% | 57.3% |
| market: flat 1% of bankroll, rollover | 872 | -38.34 | -70.13 | +26.33 | 13.4% | 40.5% | 0.0% | 51.1% |
| market: Kelly 25%, no rollover | 872 | -49.65 | -99.74 | +47.53 | 20.1% | 64.9% | 23.0% | 72.0% |
| market: Kelly 25%, rollover | 872 | -48.15 | -80.42 | +35.31 | 12.8% | 59.7% | 0.0% | 61.8% |
| market: Kelly 50%, rollover | 872 | -81.33 | -97.47 | +29.04 | 7.8% | 90.3% | 0.9% | 88.9% |
| market: parlay 2 legs | 418 | -29.25 | -100.00 | +78.50 | 32.7% | 55.7% | 20.0% | 62.9% |
| market: parlay 3 legs | 266 | -38.22 | -100.00 | +144.92 | 36.5% | 66.5% | 34.1% | 78.7% |
| market: parlay 4 legs | 196 | -99.64 | -100.00 | +266.76 | 31.3% | 76.0% | 53.3% | 99.6% |
| market: odds 1.5-3.0 | 310 | -12.05 | -45.09 | +21.63 | 27.7% | 4.2% | 0.0% | 24.5% |
| market: odds 2.0-10.0 | 858 | -38.51 | -99.36 | +33.92 | 19.6% | 53.0% | 10.2% | 58.1% |

Definitions: *rollover* = stakes sized on the current bankroll (winnings are re-staked); *no rollover* = stakes sized on the starting £100. Flat = £1 (or 1% of bankroll with rollover). Kelly x% = x% of the Kelly stake computed from the MODEL's probability and the odds after commission. Parlays are hypothetical (Betfair Exchange has no multiples): same-day qualifying picks grouped by highest edge. Overconfident x% = when the model backs an outcome, its true chance is x% lower (relative) than the model says.
