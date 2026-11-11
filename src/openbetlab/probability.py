"""Small utilities for working with probabilities.

A probability is a number between 0 and 1 (inclusive):

* 0 means "impossible"
* 1 means "certain"
* 0.25 means "happens one time in four, on average"
"""

from __future__ import annotations

from openbetlab._validation import require_real_number


def validate_probability(probability: float, name: str = "probability") -> float:
    """Check that ``probability`` is a real number in the range [0, 1].

    Returns the value as a float so callers can use it directly.

    >>> validate_probability(0.25)
    0.25
    """
    value = require_real_number(probability, name)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1 inclusive, got {value}")
    return value


def complement(probability: float) -> float:
    """Return the probability that an event does NOT happen (``1 - p``).

    >>> complement(0.25)
    0.75
    """
    return 1.0 - validate_probability(probability)


def probability_to_percent(probability: float) -> float:
    """Convert a probability (0 to 1) into a percentage (0 to 100).

    >>> probability_to_percent(0.4)
    40.0
    """
    return validate_probability(probability) * 100.0
