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
| Missing price | No bet unless all three outcomes have a 2h price (never use another snapshot as a substitute) |
| Stale price | No bet if any of the three 2h prices last traded more than **60 minutes** before the pick time |
| Pick time | Kick-off minus 2h, where kick-off = the earlier of the scheduled start and the first in-play time; must fall on the match day (UK time), after every result the model has used |
| Spread check | Results also reported with prices 1 and 2 Betfair ticks worse (sensitivity only, not a pass criterion) |
| Matches excluded | Unmatched Betfair markets, matches with an untrustworthy date (outside the season or inconsistent with their matchday), matches without a complete, fresh 2h price |

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
3. The 95% confidence interval for ROI (bootstrap over match days, 10,000 resamples,
   fixed seed) includes 0.
4. Average closing-line value ≤ 0 (bets were not, on average, taken at better
   prices than the closing price). CLV is measured before commission.

Reported regardless of outcome: number of bets, hit rate, ROI, profit in units,
max drawdown, CLV, results per league and per odds band. A "no edge" result is
reported as such, without re-tuning.

## 6. Open decisions before freezing (from the independent review, reports/review_v1.md)

1. **Sample size.** One season gives roughly 500–650 bets. That only detects an ROI
   above about 10–15%. A realistic 2–3% edge needs 6,000–28,000 bets. Choose:
   (a) accept that v1 can only detect a large edge; (b) pool several seasons;
   (c) make CLV the primary measure (lower noise).
2. **Gate 1 minimum number of bets.** Set it from the power table in the review.
3. **Play-off matches** (neutral venue, two legs): exclude them.
4. **Exact match list.** List the held-out matches (or a rule for them) before any
   odds are seen. League One/Two 2025-26 currently have results only to about
   December 2025.
5. **Market check first.** Score the closing market's probabilities on the same
   matches. If the model's log loss is not better, stop (no edge) without betting.
6. **Subgroups** (per league, odds band) and every Monte Carlo variant are
   exploratory only. No pass can come from them.
7. **Versions.** At most one later version (v2), and only with a new, untouched
   period.

## 7. Already known before freezing (honest disclosure)

- On 2025-26 the model's log loss is 1.0404 (Poisson). The closing market has
  not been scored yet.
- No Betfair data has been loaded or seen.
- The forecasts' SHA-256 hashes are committed in `reports/forecast_hashes.json`,
  so they can be checked against later runs.
- Model accuracy on the held-out season was recomputed several times during
  development (Phases 2–4), and Elo scored slightly better than Poisson there. The
  model choice (Poisson) was made on the validation season, not on that result.
