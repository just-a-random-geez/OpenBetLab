# Data Sources

## openfootball/football.json

- URL: https://github.com/openfootball/football.json
- Use: match fixtures and results (JSON)
- Licence: **CC0-1.0** (public domain dedication)
- Licence file: `LICENSE.md` (full CC0 1.0 Universal text)
  - https://github.com/openfootball/football.json/blob/master/LICENSE.md
  - SHA-256: `36ffd9dc085d529a7e60e1276d73ae5a030b020313e6c5408593a6ae2af39673`
- README statement: "The football.json schema, data and scripts are dedicated to the public domain. Use as you please with no restrictions whatsoever."
- Upstream commit checked: `e6744429ee395bc86f247348c6184bb08d4eb361`
- Checked: 2026-11-11

## openfootball/england

- URL: https://github.com/openfootball/england
- Use: England (and Wales) league data in Football.TXT format (upstream of football.json England files)
- Licence: **CC0-1.0** — confirmed from the repo's own `LICENSE.md` (full CC0 1.0 Universal text, byte-identical to football.json's)
  - https://github.com/openfootball/england/blob/master/LICENSE.md
  - SHA-256: `36ffd9dc085d529a7e60e1276d73ae5a030b020313e6c5408593a6ae2af39673`
- README statement: "The football.db schema, data and scripts are dedicated to the public domain. Use as you please with no restrictions whatsoever."
- Upstream commit checked: `9ee7a0c351805c99cc334478a9bf04b7d0432fec`
- Checked: 2026-11-11

## Notes

- CC0 waives copyright and database rights (incl. EU Directive 96/9/EC); commercial use allowed; no attribution required (we credit anyway).
- CC0 §4: no warranty of accuracy; no trademark rights granted (club names/crests are not covered).
- Re-check licence files when bumping the pinned upstream commit.

## Betfair Historic Data – BASIC tier (odds)

- URL: https://historicdata.betfair.com/
- Use: football match odds (MATCH_ODDS markets), last traded prices at 1-minute
  intervals before and during the match.
- Tier: BASIC (free).
- Licence: **personal use only** (recorded 2026-11-11, as stated by the project owner;
  check the current terms on the Betfair Historic Data site before any other use).
- Storage rules:
  - Raw files go in `data/raw/betfair/` and are **never committed** (gitignored).
  - Everything derived from them (`data/odds/` tables and `data/odds/odds_report.md`,
    `reports/private/`) is also gitignored and must not be committed or shared.
  - A test (`tests/test_betfair.py`) fails if any of these paths become tracked.
- Recorded: 2026-11-11
