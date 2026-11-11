# Research Plan v1 (pre-registered) — DRAFT, NOT YET FROZEN

> Status: DRAFT. Becomes binding when committed with status FROZEN.
> After that, this file must not be edited. Any change = a new file (v2) with a new
> out-of-sample period.

## 1. Question

Does the OpenBetLab model produce a positive return, after commission, when
betting against the Betfair exchange on English league football — beyond what
chance would produce?

## 2. Strategy rules (proposed)

| Rule | Value |
|---|---|
| Market | Betfair Exchange, Match Odds (home/draw/away), football |
| Competitions | en.1–en.4 (Premier League, Championship, League One, League Two) |
| Bet type | **Back** bets, **singles only**. No lays, no parlays/accumulators |
| Model | `poisson` (chosen by validation log loss on 2024-25, see `data/clean/forecasts.json`), probabilities exactly as written to `data/clean/forecasts.csv` |
| Price taken | Betfair last traded price at **2 hours before kick-off** (`2h` snapshot). Closing price used only to measure closing-line value |
| Edge definition | edge after commission = p·(odds−1)·(1−c) − (1−p) |
| Minimum edge | ≥ **0.05** (5%) after commission |
| Odds range | **1.50 ≤ odds ≤ 5.00** |
| Commission c | **5%** (`config/settings.toml`); also reported at 2% as a sensitivity check, not a pass criterion |
| Bets per match | At most **one**: the outcome with the largest qualifying edge |
| Staking | **Flat 1 unit** per bet. No Kelly, no compounding |
| Missing price | No bet (never use another snapshot as a substitute) |
| Matches excluded | Unmatched Betfair markets, matches with an untrustworthy date, matches without a complete 2h price |

## 3. Out-of-sample period (proposed)

- **Primary:** season **2025-26**, all matches in en.1–en.4 with Betfair data,
  kick-off 2025-07-01 to 2026-06-30.
- Rationale: the model settings and calibration were fixed using seasons up to
  2024-25 only. The 2025-26 Betfair prices have **not** been looked at by anyone.
- Model accuracy on 2025-26 (Brier/log loss) has already been seen. Model-vs-odds
  results have not.
- No parameter, rule or threshold may be changed after the backtest is run.

## 4. Gate 1 pass/fail criteria

> **TO BE COPIED VERBATIM FROM THE GUIDE — not yet provided.**

## 5. What counts as "no edge" (proposed)

The result is **"no edge"** if ANY of these hold:
1. Fewer than **[N from Gate 1]** bets qualify (too few to judge).
2. ROI after commission ≤ 0.
3. The 95% confidence interval for ROI (bootstrap over bets, 10,000 resamples,
   fixed seed) includes 0.
4. Average closing-line value ≤ 0 (bets were not, on average, taken at better
   prices than the closing price).

Reported regardless of outcome: number of bets, hit rate, ROI, profit in units,
max drawdown, CLV, results per league and per odds band. A "no edge" result is
reported as such, without re-tuning.

## 6. Already known before freezing (honest disclosure)

- On 2025-26 the model's log loss is 1.0404 (Poisson). The closing market has
  not been scored yet.
- No Betfair data has been loaded or seen.
