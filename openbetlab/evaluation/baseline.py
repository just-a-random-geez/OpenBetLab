"""Naive baseline: predict each league's historical home / draw / away rates."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Iterable

from .data import Result
from .metrics import OUTCOMES


def _rates(counts: Counter) -> tuple[float, float, float]:
    n = sum(counts.values())
    return tuple(counts[o] / n for o in OUTCOMES)  # type: ignore[return-value]


class LeagueAverageModel:
    """Every match in a league gets the same forecast: that league's past H/D/A frequencies.

    Ignores the teams completely - it is the bar any real model must beat.
    Leagues not seen in training get the all-league average.
    """

    name = "league_average"

    def __init__(self) -> None:
        self.league_rates: dict[str, tuple[float, float, float]] = {}
        self.overall_rates: tuple[float, float, float] | None = None

    def fit(self, train: Iterable[Result]) -> "LeagueAverageModel":
        per_league: dict[str, Counter] = defaultdict(Counter)
        overall: Counter = Counter()
        for m in train:
            per_league[m.league][m.outcome] += 1
            overall[m.outcome] += 1
        if not overall:
            raise ValueError("cannot fit on zero matches")
        self.league_rates = {lg: _rates(c) for lg, c in per_league.items()}
        self.overall_rates = _rates(overall)
        return self

    def predict(self, match: Result) -> tuple[float, float, float]:
        if self.overall_rates is None:
            raise RuntimeError("fit() first")
        return self.league_rates.get(match.league, self.overall_rates)


class UniformModel:
    """1/3 each - a 'knows nothing' reference point."""

    name = "uniform"

    def fit(self, train: Iterable[Result]) -> "UniformModel":
        return self

    def predict(self, match: Result) -> tuple[float, float, float]:
        return (1 / 3, 1 / 3, 1 / 3)
