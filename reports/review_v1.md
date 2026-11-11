# Independent Review v1

Date: 2026-11-11. Code reviewed at commit `f331677` (end of Phase 4).

## How the review was done

Three reviewers worked separately and did not see each other's conclusions:

1. **Math auditor**: checked every probability, odds, margin, Kelly and ROI formula,
   and recomputed key numbers by hand.
2. **Leakage hunter**: looked for any way future information (results, closing odds,
   later data) could reach a prediction or a pick. Ran perturbation tests on the real data.
3. **Devil's advocate**: argued that any result is luck or overfitting. Checked sample
   size, multiple testing, and whether the odds were really available at bet time.

Each reviewer worked read-only. Their findings were combined here. Only genuine issues
were fixed. Decisions that belong in the research plan were not changed by me; they are
listed for the owner to decide.

## Important context

- **No Betfair data exists yet**, and the research plan is still a **draft**. The
  backtest has never been run, so there was no betting result that could change.
- What *was* rerun after the fixes: the full model evaluation (held-out season
  2025-26), the synthetic Monte Carlo, and all tests (now 180, all passing).

## Findings and what was done

Severity: C = critical, M = major, m = minor, n = note.

### Fixed

| # | Found by | Sev. | Issue | Fix |
|---|---|---|---|---|
| 1 | Leakage | M | If a market went in-play *before* a later-updated scheduled start, in-play trades could become the "closing" or "2h" price. | Kick-off is now the **earlier** of first in-play time and scheduled start. New test with the reviewer's example. |
| 2 | Leakage | M | 143 games from the 2019-20 COVID restart were dated July 2019 instead of July 2020, which put future results into training. The dates passed the season-window check. | Cleaning flags any match dated more than 180 days before an earlier matchday (`date_inconsistent_with_round`). Evaluation excludes flagged matches. Exactly these 143 are flagged. |
| 3 | Leakage | M | `odds.compare` could produce held-out model-vs-market results before the plan is frozen. | It now defaults to the validation season and refuses the held-out season until the plan is FROZEN, like the backtest and the simulation. |
| 4 | Leakage + Devil | m/M | A pick price could be hours or days old. A 24h snapshot could use results the model knew that came after the price. The engine allowed partial prices, contradicting the plan. | A pick now needs **all three** prices, each traded ≤ 60 min before pick time, with pick time on the match day (after the model's knowledge cut-off). |
| 5 | Devil | M | Last traded price is not necessarily a price you could back. | Spread sensitivity: results also shown with prices 1 and 2 Betfair ticks worse, and with 2% commission. Sensitivity only. |
| 6 | Math | M | Monte Carlo ignored Betfair's £1 minimum stake, so rollover and Kelly could never be ruined (they bet pennies). | Stakes below £1 are raised to £1, and a day's stakes must fit in the bankroll together. Under the no-edge case, Kelly 25% with rollover ruin went from 0% to 18.4%, and half-Kelly from 0.9% to 45.1%. |
| 7 | Math | m | Worst drawdown % was the % of the biggest £ fall, not the biggest % fall. Example: [100, 50, 300, 240] gave 20% instead of 50%. | Tracked separately. Test uses the reviewer's example. |
| 8 | Math | m | Backtest bets at the same kick-off were settled one by one, so they could over-commit the bankroll. | Same-kick-off bets must fit in the bankroll together. |
| 9 | Math | m | Dixon-Coles ρ bounds were computed on low-score matches only. | Bounds now come from all matches. |
| 10 | Devil | m | Bootstrap CI treated bets as independent. | The CI now resamples whole match days. Test shows a wider interval when same-day bets move together. |
| 11 | Devil | m | ROI was only computed on bets placed before ruin. | ROI on all qualifying bets is also reported. |
| 12 | Math | n | The calibrator's Newton fit had no convergence check. | It now warns when the fit doesn't converge. |
| 13 | Leakage | n | Some no-leak tests changed only one future match. | New tests change *every* result on/after several cut-off dates, including the same day, for the backtest, Poisson and Elo. |
| 14 | Devil | m | "Nobody has seen the forecasts vs prices" couldn't be verified. | SHA-256 of both forecast files committed in `reports/forecast_hashes.json` before any odds exist. |
| 15 | Devil | m | Monte Carlo table invited misreading of the "model truth" rows. | "Market truth" (no-edge) rows are now listed first, with an explicit note. |
| 16 | Math | n | CLV is before commission, edge is after. A positive CLV can still lose money. | Stated in the backtest report and plan. |

### Not fixed (decisions for the plan owner)

These are research-design choices, not bugs. They are recorded in
`docs/RESEARCH_PLAN_v1.md` §6 "Open decisions".

| # | Sev. | Issue |
|---|---|---|
| A | **C** | **Sample size.** One season gives ~500–650 bets. A 95% CI on ROI is then about ±9–10%, so only a very large edge (ROI > ~10–15%) could pass. A realistic 2–3% edge needs 6,000–28,000 bets (table below). A one-season pass would most likely be luck. |
| B | M | Held-out season is lopsided. League One/Two results upstream stop around December 2025 (about 470 matches missing), and the Championship includes play-offs. |
| C | M | Many options were explored: 168 model settings, 9 forecast variants, 3 snapshots, 24 simulation scenarios. Held-out *accuracy* was recomputed often during development. Model choice was made on the validation season, so no overfitting is visible, but all subgroups must be labelled exploratory. |
| D | M | Market not yet scored. If the closing market's log loss beats the model's (typical values ~0.97–0.99 against our 1.040), most "edges" are model error. Recommended: score the market first and stop if the model is not better. |
| E | m | Paired SEs in the model comparison assume matches are independent; true SEs are somewhat larger. The ~6 SE "better than baseline" result survives. The ~1 SE Elo-vs-Poisson difference stays "no clear difference". |
| F | m | Calibrator and model choice both use the 2024-25 season (mild optimism). Harmless here because calibration changed nothing. |
| G | n | Betfair BASIC has no back/lay prices or volumes. Liquidity in League One/Two can't be checked. Results can't be scaled up from £1 stakes. |

**Power table** (devil's advocate; flat bets at odds ~2.5, 5% commission, SD ≈ 1.2 units per bet):

| True ROI | Bets for 50% power | Bets for 80% power |
|---|---|---|
| 2% | 13,800 | 28,100 |
| 3% | 6,100 | 12,500 |
| 5% | 2,200 | 4,500 |
| 10% | 560 | 1,140 |

## Verified correct (summary)

- **Math auditor**: Brier, log loss, calibration buckets and paired SE are correct. So are the calibrator gradient and Hessian, the Poisson probabilities and fit updates, Dixon-Coles τ, ρ fit and score matrix, and the Elo expected score and updates. The ordered logit, implied probability, overround and proportional margin removal are correct, as are back/lay profit, commission on net winnings and break-even probability. Edge, CLV, ROI, bootstrap, losing run, Kelly fraction with commission and parlay maths were all checked by hand.
- **Leakage hunter**: randomising every 2025-26 result from a cut-off date onwards changed zero earlier forecasts (Elo at 5 cut-offs; Poisson and Dixon-Coles on en.1). Tuning and calibration never see the held-out season. Team-name mappings contain spellings only. Betfair results are used only as a cross-check. The closing price is never used for picks.

## Did conclusions change after the fixes?

| Result | Before | After | Changed? |
|---|---|---|---|
| Training matches | 23,671 | 23,528 (143 misdated removed) | Data only |
| Held-out log loss: Poisson / Dixon-Coles / Elo | 1.0404 / 1.0401 / 1.0360 | 1.0404 / 1.0401 / 1.0360 | No |
| Poisson vs baseline | −0.0350 (−5.9 SE) | −0.0351 (−5.9 SE) | No |
| Elo vs Poisson | −0.0044 (−1.1 SE), no clear difference | same | No |
| Time decay helps | −0.0167 (−3.2 SE) | −0.0166 (−3.2 SE) | No |
| Calibration step | no effect | no effect | No |
| Model chosen on validation | Poisson | Poisson | No |
| Monte Carlo, Kelly/rollover ruin (no-edge case) | 0–1% | 11–45% | **Yes**: rollover and Kelly are much riskier than first reported |
| Backtest | never run | never run (no Betfair data, plan not frozen) | n/a |

**Bottom line:** the model-accuracy conclusions are unchanged. The risk conclusions got
worse: once the minimum stake is respected, compounding and Kelly staking carry a real ruin
risk when there is no edge. Nothing in this project shows a betting edge.
Under the current design, a single season could not reliably show a realistic one.

## Reproduce

```bash
pip install -e ".[dev]"
python scripts/fetch_openfootball.py
python -m openbetlab.data.build --as-of 2026-11-11
python -m openbetlab.evaluation.run --holdout-season 2025-26
python -m openbetlab.simulation.run --source synthetic
pytest
```
