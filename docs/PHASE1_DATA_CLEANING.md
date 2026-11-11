# Phase 1 – Data cleaning (plain English)

## What it does

Takes the raw England league files (Premier League, Championship, League One,
League Two; `en.1`–`en.4`) from openfootball/football.json and produces one
clean table of matches: `data/clean/matches.csv`. It also writes a report on
data quality: `docs/data_quality_report.md`.

## How to run

```bash
pip install -e ".[dev]"
python scripts/fetch_openfootball.py      # download raw files (pinned commit)
python -m openbetlab.data.build           # clean + report
pytest                                    # tests
```

## The rules

**1. One name per club.**
The source calls the same club different things in different years
("Stoke City" until 2019-20, "Stoke City FC" after). The file
`data/team_names/england.csv` lists every spelling seen and the one name
we use. Rule: we always use the full official form (with FC / AFC).
- A name that is not in the file is kept as-is and listed as *unknown* in
  the report, so a new club is never silently mixed up with another.
- A safety check looks for names that still look alike after mapping
  (e.g. same name with and without "FC"). It must report "none".
- The original spelling is kept in `home_team_raw` / `away_team_raw`.

**2. Missing values are reported, never invented.**
If a value is missing or unreadable, the cell is left empty and counted in
the report. No guessing, no averages, no 0-0 defaults. Every match gets a
`status` that says why a score is or isn't there:

| status | meaning |
|---|---|
| played | full-time score present |
| awarded | result decided off the pitch; official score kept |
| cancelled / postponed / abandoned | marked so by the source; no score |
| scheduled | no score, match date is after the as-of date |
| result_missing | match date has passed but the source has no score |

Dates that fall outside a season's normal window are kept as published and
flagged (`date_outside_season`), not corrected.

**3. Duplicates.**
A duplicate is the same league, season, date, home team and away team.
- Identical copies: keep one, count the rest as removed.
- Copies that disagree (e.g. different scores): drop all of them and list
  them, because we can't know which is right.
- Same teams on a *different* date (e.g. play-off rematch) is a real match,
  not a duplicate.

## What the current report shows (data as of 2026-11-11)

- 26,875 rows read → 26,863 clean matches.
- 12 exact duplicates removed (League Two 2025-26).
- 39 old club spellings merged into the full names; 0 unknown names.
- 605 past matches have no result in the source (League One/Two 2025-26,
  early 2026-27 Premier League/Championship) – the upstream data hasn't been
  updated yet.
- 276 League One 2025-26 matches are dated in early 2025 instead of 2026
  (upstream year typo) – flagged.
- Half-time scores missing for some played matches in every season.
- No files upstream for League One/Two in 2016-17, 2017-18, 2021-22 to
  2023-24, 2026-27, nor the Championship in 2016-17/2017-18.
- 2019-20: League One/Two had 218 matches cancelled (COVID); League One
  has 23 teams (Bury expelled).

## Files

- `openbetlab/data/team_names.py` – name mapping + look-alike check
- `openbetlab/data/cleaning.py` – parsing, statuses, duplicates
- `openbetlab/data/quality_report.py` – the report
- `openbetlab/data/build.py` – runs everything
- `scripts/fetch_openfootball.py` – download raw data
- `tests/` – 26 tests on small hand-made examples
