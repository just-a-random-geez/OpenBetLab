# Roadmap

This roadmap is a set of ideas, not promises. Anything that conflicts with the
[Vision](VISION.md) or [Data Policy](DATA_POLICY.md) will not be built.

## 0.1: Foundation (this release)

- [x] Clean `src/` package layout, `pyproject.toml`, pytest and Ruff
- [x] Probability helpers with input validation
- [x] Decimal odds: implied and break-even probability, returns, profit,
      expected value, bookmaker margin
- [x] Parlay combined odds
- [x] Joint probability with a clearly documented independence assumption
- [x] Synthetic, clearly labelled football match data
- [x] Command-line demonstration
- [x] Automated tests and GitHub Actions

## 0.2: More odds formats (ideas)

- Conversions between decimal, fractional (e.g. 5/2) and American (e.g. +150)
  odds
- Methods for removing the bookmaker margin to estimate "fair" probabilities
  (for example proportional normalisation), each with its assumptions
  documented

## 0.3: Evaluation tools (ideas)

- Scoring rules for comparing probability estimates with outcomes
  (Brier score, log loss)
- Calibration tables
- All demonstrated on synthetic data only

## Later (ideas, needs discussion)

- A documented format for users to load *their own* local data files, subject
  to the Data Policy
- Worked educational notebooks

## Never

- Connecting to bookmakers or exchanges, or placing bets
- Downloading third-party datasets automatically
- Requiring API keys
- Marketing the project as a prediction or profit tool
