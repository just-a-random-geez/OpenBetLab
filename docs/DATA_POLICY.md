# Data Policy

## Summary

OpenBetLab ships **only synthetic (made-up) data**, never downloads data from
anywhere, and never contains personal data.

## Data included in this repository

| File | What it is | Real? |
| ---- | ---------- | ----- |
| `src/openbetlab/data/synthetic_matches.csv` | 8 invented football matches with invented odds | **No, synthetic** |

Rules for any data added to this repository:

1. It must be **synthetic**, or created by the contributor with the clear
   right to release it under the project's licence.
2. Synthetic data must be **clearly labelled** as synthetic in the file itself
   (a comment header), in an accompanying README, and in code that loads it.
   Team names and IDs should be obviously fictional (e.g. `SYN-001`,
   "Synthetic Rovers").
3. It must contain **no personal data**: no names of real people, no
   account details, no betting histories.
4. It must be **small**, a few kilobytes and enough to demonstrate and test.

## What the code must never do

- Download third-party datasets.
- Scrape websites or connect to bookmaker or exchange APIs.
- Require API keys, passwords or other credentials.

## Using your own data

Researchers may of course use OpenBetLab's functions on data they hold
locally. When doing so, it is **your** responsibility to:

- have the legal right to use the data (check licences and terms of use);
- keep that data out of this repository;
- follow the [Research Protocol](RESEARCH_PROTOCOL.md).

## Synthetic data is not evidence

Results calculated on the bundled synthetic data demonstrate that the code
works. They say **nothing** about real football or real betting markets.
