# Architecture

OpenBetLab 0.1 is intentionally simple: a single Python package of pure
functions, with no network access, no database and no runtime dependencies.

## Layout

```text
src/openbetlab/
├── __init__.py        Public API: re-exports the main functions + __version__
├── __main__.py        Lets `python -m openbetlab` run the CLI
├── _validation.py     Shared low-level checks (real, finite numbers)
├── probability.py     Probability checks and helpers
├── odds.py            Decimal odds: implied/break-even probability, returns,
│                      expected value, bookmaker margin
├── parlay.py          Combined parlay odds; joint probability (independence)
├── synthetic_data.py  Loads and validates the bundled synthetic CSV
├── cli.py             The `openbetlab` command-line demonstration
└── data/
    ├── synthetic_matches.csv   Made-up match data (clearly labelled)
    └── README.md               Explains that the data is synthetic
```

## How the modules depend on each other

```text
_validation  <-  probability  <-  odds  <-  parlay
                                   ^          ^
                                   |          |
                          synthetic_data      |
                                   ^          |
                                   +---- cli -+
```

Arrows point from a module to the modules it uses. Lower layers never import
higher layers, so the core maths (`probability`, `odds`, `parlay`) can be used
and tested on its own.

## Design decisions

- **src-layout.** The package lives in `src/` so tests run against the
  *installed* package, not files that happen to be in the current folder.
  This catches packaging mistakes early.
- **Pure functions.** Every calculation takes numbers in and returns a number
  out. No hidden state, so results are easy to test and reproduce.
- **Fail loudly.** Invalid input raises `TypeError` (wrong kind of value) or
  `ValueError` (right kind, impossible value). We never silently "fix" input.
- **Floats, not Decimals.** Research calculations use ordinary floating-point
  numbers. Tests compare with `pytest.approx` to allow for tiny rounding
  differences.
- **Assumptions in names.** `joint_probability_independent` carries its key
  assumption in its name so it cannot be overlooked.
- **Standard library only.** `csv`, `math`, `argparse`, `dataclasses` and
  `importlib.resources` are enough for 0.1.

## Conventions for odds

- Decimal odds must be **strictly greater than 1.0**.
- Probabilities must be between **0 and 1 inclusive**.
- Converting a probability to odds requires **0 < p < 1**.

## Tooling

- **pytest** runs the tests in `tests/` and the examples in the docstrings
  under `src/` (doctests).
- **Ruff** checks style and common mistakes, and formats code.
- **GitHub Actions** (`.github/workflows/tests.yml`) runs Ruff and pytest on
  Python 3.11, 3.12, 3.13 and 3.14 for every push and pull request.
