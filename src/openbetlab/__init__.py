"""OpenBetLab: a small, transparent research foundation for odds and probability.

OpenBetLab does NOT predict football (or any other) outcomes, does NOT connect
to bookmakers and does NOT place bets. It provides well-tested arithmetic for
converting between odds and probabilities so that research can be done
carefully and reproducibly.
"""

from openbetlab.odds import (
    bookmaker_margin,
    break_even_probability,
    expected_value,
    implied_probability,
    potential_profit,
    potential_return,
    probability_to_decimal_odds,
)
from openbetlab.parlay import combined_decimal_odds, joint_probability_independent
from openbetlab.probability import (
    complement,
    probability_to_percent,
    validate_probability,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "bookmaker_margin",
    "break_even_probability",
    "combined_decimal_odds",
    "complement",
    "expected_value",
    "implied_probability",
    "joint_probability_independent",
    "potential_profit",
    "potential_return",
    "probability_to_decimal_odds",
    "probability_to_percent",
    "validate_probability",
]
