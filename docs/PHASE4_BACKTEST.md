# Phase 4 – Walk-forward backtest (plain English)

## Status

The engine is built and tested. **It has not been run on real data**, and it
refuses to run until `docs/RESEARCH_PLAN_v1.md` is marked `Status: FROZEN`
(currently a DRAFT waiting for the Gate 1 criteria). No Betfair data has been
loaded yet.

## How to run (after freezing the plan and adding Betfair files)

```bash
python -m openbetlab.data.build --as-of 2026-11-11
python -m openbetlab.evaluation.run --holdout-season 2025-26
python -m openbetlab.odds.build
python -m openbetlab.backtest.run
```

Outputs (contain Betfair prices → gitignored):
`reports/private/backtest_v1.md`, `reports/private/bankroll_v1.svg`,
`data/odds/backtest_bets.csv`. The report records the plan file's SHA-256 so
anyone can check the plan was not edited afterwards.

## What happens, match day by match day

1. **Refit**: the model is refitted using only matches played on earlier
   dates (same walk-forward as Phase 2).
2. **Price**: the Betfair last traded price at the plan's pick time
   (2 hours before kick-off). A price traded at or after kick-off is
   rejected with an error. The **closing price is never used to pick**.
3. **Pick** (rules from the plan): back bets only; odds 1.50–5.00; edge after
   5% commission of at least 5%; at most one bet per match (the biggest edge).
   No price → no bet.
4. **Settle**: win → stake × (odds − 1) less commission; lose → −stake.

## What is tracked

| Metric | Meaning |
|---|---|
| Bets, hit rate | how many bets, share that won |
| ROI | profit after commission ÷ total staked |
| ROI 95% CI | bootstrap over bets (10,000 resamples, fixed seed) |
| Average CLV | closing-line value: odds taken × fair closing probability − 1. Positive = we usually got a better price than the market's final view |
| Worst drawdown | biggest fall from a bankroll peak, in £ and % |
| Longest losing run | most losing bets in a row |
| Bankroll curve | virtual £100, £1 flat stakes; betting stops if it can't cover a stake |

## Proof that no future data is used (tests)

`tests/test_backtest.py`:
- **Change the future, keep the past**: every result *and* every price after a
  cut-off date is replaced with nonsense; every bet on or before that date
  stays exactly the same (selection, odds, edge, model probability).
- Every model refit only sees matches dated before the refit date.
- Changing closing prices changes CLV only, never which bets are made.
- A pick price traded at or after kick-off raises an error.
- The rules can't be set to pick at the closing price.
- The code's rules must match the numbers written in the plan file.

## Parlays

Built only from single bets that each passed the rule (top-edge legs on the
same date, 2 legs by default). **Switched off**, because the draft plan says
singles only. They are also **hypothetical**: the Betfair Exchange has no
multiples, so a parlay price is just the product of the leg prices. To include
them, the plan must say so before it is frozen.
