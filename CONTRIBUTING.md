# Contributing to OpenBetLab

Thank you for your interest in improving OpenBetLab! Contributions of every
size are welcome: typo fixes, clearer explanations, new tests and new
calculations.

## Ground rules

Before you start, please read:

- the [Code of Conduct](CODE_OF_CONDUCT.md);
- the [Vision](docs/VISION.md), especially what the project will **not** do;
- the [Data Policy](docs/DATA_POLICY.md).

In particular, pull requests will not be accepted if they:

- connect to bookmakers or betting exchanges, or place bets;
- download third-party datasets or require API keys;
- claim, in code or documentation, that OpenBetLab predicts outcomes;
- add real personal data.

## Setting up

Follow the Mac setup steps in the [README](README.md). On Linux the steps are
the same. On Windows, activate the environment with `.venv\Scripts\activate`.

## Making a change

1. Fork the repository and create a branch:
   `git checkout -b my-improvement`.
2. Make your change.
3. Add or update tests in `tests/` for any calculation you add or change.
4. Run the checks:

   ```bash
   ruff format .
   ruff check .
   pytest
   ```

5. Commit with a clear message explaining *why* the change is needed.
6. Open a pull request. GitHub Actions will run the tests automatically.

## Code guidelines

- **Keep it simple.** Prefer the Python standard library. New runtime
  dependencies need a strong reason and should be discussed in an issue first.
- **Validate inputs.** Every public function should reject invalid input with
  a clear `ValueError` or `TypeError`. Use the helpers in `_validation.py`,
  `probability.py` and `odds.py`.
- **State assumptions.** If a calculation relies on an assumption (such as
  independence), say so plainly in its docstring.
- **Explain for beginners.** Docstrings should make sense to someone new to
  both Python and probability.
- **Test edge cases:** zero, one, empty lists, NaN, infinity, negative numbers
  and wrong types.

## Reporting bugs and suggesting ideas

Open a GitHub issue. For bugs, include what you ran, what you expected and what
happened instead. For security problems, follow [SECURITY.md](SECURITY.md)
instead of opening a public issue.
