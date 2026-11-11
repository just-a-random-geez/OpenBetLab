"""Decimal odds calculations.

Decimal odds (also called "European odds") describe the TOTAL amount returned
for each 1 unit staked if the selection wins, including the original stake.

Example: decimal odds of 2.50 with a stake of 10 return 25 in total
(10 stake back + 15 profit) if the selection wins, and 0 if it loses.

In this project decimal odds must be strictly greater than 1.0. Odds of exactly
1.0 would return only the stake (no possible profit), which carries no useful
information for research, so it is treated as invalid input.

Important: these functions are arithmetic only. A probability passed in to
:func:`expected_value` is an *assumption supplied by the user*; OpenBetLab does
not estimate or predict it.
"""

from __future__ import annotations

from collections.abc import Iterable

from openbetlab._validation import require_real_number
from openbetlab.probability import validate_probability


def validate_decimal_odds(odds: float, name: str = "odds") -> float:
    """Check that ``odds`` is a finite real number strictly greater than 1.0."""
    value = require_real_number(odds, name)
    if value <= 1.0:
        raise ValueError(f"{name} must be decimal odds greater than 1.0, got {value}")
    return value


def _validate_stake(stake: float) -> float:
    value = require_real_number(stake, "stake")
    if value < 0:
        raise ValueError(f"stake must not be negative, got {value}")
    return value


def implied_probability(odds: float) -> float:
    """Return the probability implied by decimal odds: ``1 / odds``.

    This is the "raw" implied probability. It still contains the bookmaker's
    margin, so implied probabilities for all outcomes of one event usually add
    up to slightly MORE than 1 (see :func:`bookmaker_margin`).

    >>> implied_probability(4.0)
    0.25
    """
    return 1.0 / validate_decimal_odds(odds)


def break_even_probability(odds: float) -> float:
    """Return the win probability at which a bet at these odds breaks even.

    If the true chance of winning were exactly this number, the average
    (expected) profit over many identical bets would be zero. Mathematically it
    equals ``1 / odds``, the same as :func:`implied_probability`; the separate
    name exists because the *question being asked* is different.

    >>> break_even_probability(2.0)
    0.5
    """
    return implied_probability(odds)


def probability_to_decimal_odds(probability: float) -> float:
    """Return the "fair" decimal odds for a probability: ``1 / probability``.

    "Fair" means odds with no bookmaker margin. The probability must be strictly
    between 0 and 1: a probability of 0 has no finite odds, and a probability of
    1 would give odds of 1.0, which this project treats as invalid.

    >>> probability_to_decimal_odds(0.25)
    4.0
    """
    value = validate_probability(probability)
    if value in (0.0, 1.0):
        raise ValueError(
            "probability must be strictly between 0 and 1 to convert to odds, "
            f"got {value}"
        )
    return 1.0 / value


def potential_return(stake: float, odds: float) -> float:
    """Total amount returned if the selection wins (stake included).

    >>> potential_return(10, 2.5)
    25.0
    """
    return _validate_stake(stake) * validate_decimal_odds(odds)


def potential_profit(stake: float, odds: float) -> float:
    """Profit if the selection wins (stake NOT included).

    >>> potential_profit(10, 2.5)
    15.0
    """
    return _validate_stake(stake) * (validate_decimal_odds(odds) - 1.0)


def expected_value(probability: float, odds: float, stake: float = 1.0) -> float:
    """Average profit per bet, IF ``probability`` were the true win chance.

    Formula: ``stake * (probability * odds - 1)``.

    A positive result means the bet would make money on average under the
    stated assumption; negative means it would lose money on average. The
    result is only as good as the probability you supply. OpenBetLab does not
    estimate it for you.

    >>> expected_value(0.5, 2.0)
    0.0
    """
    p = validate_probability(probability)
    o = validate_decimal_odds(odds)
    s = _validate_stake(stake)
    return s * (p * o - 1.0)


def bookmaker_margin(odds_for_all_outcomes: Iterable[float]) -> float:
    """Return the bookmaker margin (the "overround") for one market.

    Pass the decimal odds for EVERY possible outcome of one event, e.g. the
    home win, draw and away win odds of a football match. The margin is::

        sum(1 / odds) - 1

    A result of 0.05 means the implied probabilities add up to 105%, i.e. a
    5% margin built into the prices. A NEGATIVE result means the implied
    probabilities add up to less than 100%, which usually signals a data
    error or odds taken from different sources or times.

    The result is only meaningful if the odds cover every outcome of the
    event exactly once; this function cannot check that for you.

    >>> round(bookmaker_margin([2.0, 2.0]), 10)
    0.0
    """
    odds_list = list(odds_for_all_outcomes)
    if len(odds_list) < 2:
        raise ValueError("a market needs the odds of at least two outcomes")
    total = sum(
        implied_probability(validate_decimal_odds(o, f"odds[{i}]"))
        for i, o in enumerate(odds_list)
    )
    return total - 1.0
