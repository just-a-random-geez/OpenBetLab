# Synthetic data

**Everything in this folder is SYNTHETIC (made up). None of it is real.**

`synthetic_matches.csv` contains eight invented football matches between
invented teams ("Synthetic Rovers", "Example Athletic", ...), with invented
scores and invented decimal odds for home win / draw / away win.

The odds were chosen by hand so that each match has a small bookmaker-style
margin (roughly 5%). That makes the data useful for testing the calculations,
but it says nothing about real football or real bookmakers.

The data exists only so that:

- the automated tests have something realistic-looking to check;
- the command-line demo has something to show.

Do not use it to draw conclusions about real matches. See
[`docs/DATA_POLICY.md`](../../../docs/DATA_POLICY.md) for the project's data rules.
