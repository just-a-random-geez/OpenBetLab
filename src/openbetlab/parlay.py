"""Parlay (accumulator / multiple) calculations.

A parlay combines several selections ("legs") into one bet. It only wins if
EVERY leg wins.

Two separate questions are answered here:

1. **Combined odds** (:func:`combined_decimal_odds`): what does the parlay pay?
   This is pure arithmetic: multiply the decimal odds of every leg.

2. **Joint probability** (:func:`joint_probability_independent`): how likely is
   it that every leg wins? This is only a simple product of the individual
   probabilities UNDER AN INDEPENDENCE ASSUMPTION (explained below).
"""

from __future__ import annotations

import math
from collections.abc import Iterable

from openbetlab.odds import validate_decimal_odds
from openbetlab.probability import validate_probability


def combined_decimal_odds(leg_odds: Iterable[float]) -> float:
    """Return the combined decimal odds of a parlay: the product of all legs.

    Example: legs at 2.0, 1.5 and 3.0 combine to 2.0 * 1.5 * 3.0 = 9.0.

    Raises ``ValueError`` if no legs are given, any leg has invalid odds, or
    the product is too large to represent (it would otherwise become infinity).

    >>> combined_decimal_odds([2.0, 1.5, 3.0])
    9.0
    """
    legs = list(leg_odds)
    if not legs:
        raise ValueError("a parlay needs at least one leg")
    validated = [validate_decimal_odds(o, f"leg_odds[{i}]") for i, o in enumerate(legs)]
    combined = math.prod(validated)
    if math.isinf(combined):
        raise ValueError("combined odds are too large to represent as a finite number")
    return combined


def joint_probability_independent(probabilities: Iterable[float]) -> float:
    """Return the probability that ALL events happen, ASSUMING INDEPENDENCE.

    Formula: ``p1 * p2 * ... * pn``

    INDEPENDENCE ASSUMPTION (please read)
    -------------------------------------
    Multiplying probabilities is only correct when the events are
    *independent*: knowing that one event happened must not change the chance
    of any other event happening.

    * Reasonable approximation: results of different matches played in
      unrelated competitions.
    * NOT independent: two outcomes from the SAME match (e.g. "Team A wins"
      and "over 2.5 goals"), or matches whose results influence each other.
      For such "correlated" events this function will give a WRONG answer,
      sometimes badly wrong.

    This function cannot detect whether your events are independent. Checking
    that is the researcher's responsibility. The probabilities you supply are
    your own assumptions; OpenBetLab does not estimate them.

    >>> joint_probability_independent([0.5, 0.5])
    0.25
    """
    values = list(probabilities)
    if not values:
        raise ValueError("at least one probability is required")
    validated = [
        validate_probability(p, f"probabilities[{i}]") for i, p in enumerate(values)
    ]
    return math.prod(validated)
