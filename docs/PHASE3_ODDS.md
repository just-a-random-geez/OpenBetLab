# Phase 3 – Odds handling (plain English)

Betfair data is **personal use only**. Raw files live in `data/raw/betfair/`;
all outputs go to `data/odds/`. Both are gitignored and must never be
committed or shared.

## How to run

```bash
# put the BASIC downloads (.bz2 files or .tar archives) in data/raw/betfair/
python -m openbetlab.data.build --as-of 2026-11-11   # openfootball matches (Phase 1)
python -m openbetlab.odds.build
```

Outputs:
- `data/odds/betfair_prices.csv` – one row per match × selection
  (home / draw / away) with the price at each snapshot and when it traded.
- `data/odds/betfair_match_probs.csv` – one row per match × snapshot with
  odds, implied probabilities, overround, margin-free probabilities and
  break-even probabilities after commission.
- `data/odds/odds_report.md` – what was read, skipped, matched, and checks.

## 1. Reading Betfair files

Each BASIC file is one market, a list of time-stamped messages: market
details (teams, scheduled start, whether it's in-play, final winner) and
**last traded prices** (the price at which the most recent bet was matched),
sampled each minute. Only football "Match Odds" markets are used.
Home / away come from the event name "Home v Away"; "The Draw" is the draw.

## 2. Which price, when

- **Kick-off** = the moment Betfair switched the market to in-play. If that
  moment isn't recorded, or is more than 10 minutes early / 30 minutes late
  vs the scheduled start (e.g. the flag only appears in the final settlement
  message), the scheduled start is used instead. `kickoff_source` says which.
- **Closing price** = the last traded price strictly *before* kick-off.
  Nothing traded in-play is ever used.
- **Early prices** = the last traded price at or before 24 hours and 2 hours
  before kick-off (change in `config/settings.toml`).
- If nothing had traded by then, the price is **empty** – never filled in.
  The time of the trade is stored, so you can see how stale a price is.

## 3. Matching to openfootball

Betfair writes "Man Utd", openfootball "Manchester United FC".
1. **Mapping file** `data/team_names/betfair/england.csv`: Betfair name →
   our name. Exact and trusted.
2. **Fuzzy fallback**: only among openfootball matches on the same UK date
   (Betfair times are UTC; converted to London time). Both team names must
   be similar enough (score ≥ 0.8) and the best candidate must clearly beat
   the next one. Home and away must be the same way round.
3. Otherwise **unmatched** – listed in the report, never guessed.

Every fuzzy match is listed in the report: check it, then add the names to
the mapping file. As a safety check, Betfair's settled winner is compared
with the openfootball result; disagreements are listed.

## 4. Odds → probabilities

- **Implied probability** = 1 / decimal odds. Odds 2.0 → 50%.
- **Overround** = sum of the three implied probabilities − 1. A bookmaker's
  is positive (their margin, e.g. +5%). On an exchange using last traded
  prices it is close to zero and can even be negative, because the three
  prices were matched at slightly different moments.
- **Removing the margin – proportional method (used)**: divide each implied
  probability by their sum so they add up to 100%. Example: 1.80 / 3.60 /
  4.50 → 55.6% + 27.8% + 22.2% = 105.6% → 52.6% / 26.3% / 21.1%.

Alternatives (not implemented yet):
- **Additive**: subtract the same amount from each outcome. Simple, but
  can give negative probabilities for big outsiders.
- **Power method**: raise each implied probability to a power k chosen so
  they sum to 1. Takes more margin off long shots.
- **Shin's method**: models the bookmaker protecting against insiders;
  also loads more of the margin on long shots. Popular in research.
- **Odds-ratio method**: similar effect, a single scaling on the odds-ratio
  scale.
Bookmakers usually put more margin on long shots ("favourite–longshot
bias"), which the last three try to capture. On a low-margin exchange the
methods give almost the same answer.

## 5. Commission

Betfair takes commission from your **net winnings on each market** (all
your bets on that match's market added up), only if positive. Losses pay
nothing. The rate is set once in `config/settings.toml`
(`[betfair] commission = 0.05`) and every profit function
(`openbetlab/odds/profit.py`) requires it – there is no hidden default.

- Back £10 at 3.0, wins: +£20 before commission, **+£19** at 5%.
- Lay £10 at 3.0, selection loses: +£10 → **+£9.50**; selection wins: −£20.
- **Break-even probability** of a back bet after commission:
  1 / (1 + (odds − 1) × (1 − commission)). At 2.0 and 5% that's 51.3%,
  not 50%.

No profitability is claimed here; this phase only prepares the odds.

## Files

- `openbetlab/odds/betfair.py` – read files, kick-off, snapshot prices
- `openbetlab/odds/matching.py` – Betfair ↔ openfootball matching
- `openbetlab/odds/probabilities.py` – implied, overround, proportional
- `openbetlab/odds/profit.py` – back/lay/market profit with commission
- `openbetlab/odds/build.py` – runs it all
- `openbetlab/settings.py`, `config/settings.toml` – commission, snapshots
- `tests/test_betfair.py`, `tests/test_odds_matching.py`,
  `tests/test_odds_maths.py` (synthetic Betfair files; no real data in repo)
