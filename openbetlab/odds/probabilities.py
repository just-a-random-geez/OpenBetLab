"""Odds -> probabilities, overround and margin removal."""

from __future__ import annotations

from typing import Sequence


def implied_probability(odds: float) -> float:
    if odds is None or odds <= 1:
        raise ValueError(f"decimal odds must be > 1, got {odds}")
    return 1 / odds


def overround(odds: Sequence[float]) -> float:
    """Sum of implied probabilities minus 1.

    Bookmaker: positive (their margin). Exchange last-traded prices: close to 0 and can be
    negative, because the three prices are traded at different moments by different people.
    """
    return sum(implied_probability(o) for o in odds) - 1


def remove_margin_proportional(odds: Sequence[float]) -> list[float]:
    """Proportional (basic normalisation): divide each implied probability by their sum.

    Assumes the margin is spread in proportion to each outcome's probability.
    Works for negative overround too (probabilities are scaled up).
    """
    imp = [implied_probability(o) for o in odds]
    total = sum(imp)
    return [p / total for p in imp]
