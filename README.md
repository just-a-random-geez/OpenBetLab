# OpenBetLab

[![Tests](https://github.com/just-a-random-geez/OpenBetLab/actions/workflows/tests.yml/badge.svg)](https://github.com/just-a-random-geez/OpenBetLab/actions/workflows/tests.yml)

**OpenBetLab is an open-source research foundation for studying betting odds
and probability, carefully and transparently.**

Version 0.1 is deliberately small. It gives you well-tested arithmetic for:

- converting decimal odds to probabilities (including the **break-even
  probability**);
- combining the odds of several selections into a **parlay** (accumulator);
- calculating a **joint probability**, with its **independence assumption**
  stated clearly;
- measuring the **bookmaker margin** of a market;
- trying all of the above on a small **synthetic** (made-up) football dataset.

## What OpenBetLab is NOT

- It does **not** predict football (or any other) results.
- It does **not** connect to bookmakers, place bets or handle money.
- It does **not** download third-party datasets or need API keys.
- It is **not** betting advice. Gambling carries a real risk of financial
  loss and can be addictive. If gambling is causing you problems, please seek
  help from a local support service.

## Quick example

```python
from openbetlab import (
    break_even_probability,
    combined_decimal_odds,
    joint_probability_independent,
)

break_even_probability(2.5)  # 0.4  -> 40%
combined_decimal_odds([2.0, 1.5, 3.0])  # 9.0
joint_probability_independent([0.5, 0.6])  # 0.3  (ONLY if the events are independent)
```

## Setting up on a Mac (step by step)

You only need to do steps 1 to 4 once.

### 1. Open Terminal

Press `Cmd + Space`, type **Terminal**, and press Enter. Type each command
below into Terminal and press Enter after each one.

### 2. Check that Python 3.11 or newer is installed

```bash
python3 --version
```

If it prints `Python 3.11` or any higher number (3.12, 3.13, ...), you're
ready. If it says "command not found" or shows an older version, download the
latest Python installer for macOS from <https://www.python.org/downloads/>,
run it, then **close and reopen Terminal** and check again.

### 3. Download the project and go into its folder

If you have Git (type `git --version` to check; macOS offers to install it if
missing):

```bash
cd ~/Documents
git clone https://github.com/just-a-random-geez/OpenBetLab.git
cd OpenBetLab
```

If you already have the folder on your Mac, just `cd` into it instead, for
example `cd ~/Documents/GitHub/OpenBetLab`.

### 4. Create a virtual environment and install the project

A *virtual environment* is a private box of Python packages just for this
project, so nothing on the rest of your Mac is changed.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

After `source .venv/bin/activate`, your Terminal prompt starts with `(.venv)`.
That means the environment is switched on.

### 5. Use it

Every time you open a new Terminal window, go to the folder and switch the
environment back on first:

```bash
cd ~/Documents/OpenBetLab          # or wherever your copy lives
source .venv/bin/activate
```

Then try:

```bash
openbetlab demo                    # guided tour using synthetic data
openbetlab odds 2.5                # break-even probability of odds 2.5
openbetlab parlay 2.0 1.8 3.1      # combined odds of a 3-leg parlay
openbetlab joint 0.5 0.6           # joint probability (independence assumed)
openbetlab --help                  # list all commands
```

Run the automated tests and the code-style checker:

```bash
pytest
ruff check .
ruff format --check .
```

When you're finished, type `deactivate` to switch the environment off.

## Project layout

```text
OpenBetLab/
├── src/openbetlab/        # the Python package
│   ├── probability.py     # basic probability helpers
│   ├── odds.py            # decimal odds, break-even, margin, expected value
│   ├── parlay.py          # combined parlay odds, joint probability
│   ├── synthetic_data.py  # loads the bundled made-up match data
│   ├── cli.py             # the `openbetlab` command
│   └── data/              # SYNTHETIC match data (not real)
├── tests/                 # automated tests (pytest)
├── docs/                  # vision, architecture, roadmap, policies
└── .github/workflows/     # runs the tests automatically on GitHub
```

## Documentation

- [Vision](docs/VISION.md): why the project exists
- [Architecture](docs/ARCHITECTURE.md): how the code is organised
- [Roadmap](docs/ROADMAP.md): what might come next
- [Research protocol](docs/RESEARCH_PROTOCOL.md): how research should be done
- [Data policy](docs/DATA_POLICY.md): what data is and isn't allowed

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and
our [Code of Conduct](CODE_OF_CONDUCT.md). To report a security problem, see
[SECURITY.md](SECURITY.md).

## Licence

Apache License 2.0. See [LICENSE](LICENSE).
