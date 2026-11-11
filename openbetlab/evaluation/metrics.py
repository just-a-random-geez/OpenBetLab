"""Scoring rules for 1X2 (home / draw / away) probability forecasts.

A forecast is a tuple (p_home, p_draw, p_away) that sums to 1.
An outcome is one of "H", "D", "A".
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

OUTCOMES = ("H", "D", "A")
Probs = Sequence[float]


def _check(probs: Sequence[Probs], outcomes: Sequence[str]) -> None:
    if len(probs) != len(outcomes):
        raise ValueError(f"{len(probs)} forecasts but {len(outcomes)} outcomes")
    if not probs:
        raise ValueError("no forecasts to score")
    for p, o in zip(probs, outcomes):
        if o not in OUTCOMES:
            raise ValueError(f"unknown outcome {o!r}")
        if len(p) != 3 or any(x < 0 or x > 1 for x in p) or abs(sum(p) - 1) > 1e-6:
            raise ValueError(f"invalid probabilities {tuple(p)}: need 3 values in [0,1] summing to 1")


def brier_per_match(probs: Sequence[Probs], outcomes: Sequence[str]) -> list[float]:
    _check(probs, outcomes)
    return [sum((pk - (k == o)) ** 2 for pk, k in zip(p, OUTCOMES))
            for p, o in zip(probs, outcomes)]


def log_loss_per_match(probs: Sequence[Probs], outcomes: Sequence[str],
                       eps: float = 1e-15) -> list[float]:
    _check(probs, outcomes)
    return [-math.log(max(p[OUTCOMES.index(o)], eps)) for p, o in zip(probs, outcomes)]


def paired_difference(a: Sequence[float], b: Sequence[float]) -> tuple[float, float]:
    """Mean of (a - b) per match and its standard error.

    Negative mean = model a scored lower (better). If |mean| > 2 * SE the gap is
    unlikely to be luck (roughly 95% confidence).
    """
    if len(a) != len(b) or len(a) < 2:
        raise ValueError("need two equal-length lists with at least 2 values")
    d = [x - y for x, y in zip(a, b)]
    mean = sum(d) / len(d)
    var = sum((x - mean) ** 2 for x in d) / (len(d) - 1)
    return mean, math.sqrt(var / len(d))


def brier_score(probs: Sequence[Probs], outcomes: Sequence[str]) -> float:
    """Mean over matches of sum_k (p_k - y_k)^2. 0 = perfect, 2 = worst, 2/3 = always 1/3 each."""
    return sum(brier_per_match(probs, outcomes)) / len(probs)


def log_loss(probs: Sequence[Probs], outcomes: Sequence[str], eps: float = 1e-15) -> float:
    """Mean of -ln(probability given to what happened). Lower is better; ln 3 ≈ 1.0986 = always 1/3.

    A probability of 0 on the actual outcome is clipped to ``eps`` so the score stays finite
    (it is still a huge penalty).
    """
    return sum(log_loss_per_match(probs, outcomes, eps)) / len(probs)


@dataclass
class CalibrationRow:
    outcome: str        # "H", "D" or "A"
    bucket_low: float
    bucket_high: float
    n: int              # forecasts in this bucket
    mean_predicted: float
    actual_rate: float  # how often the outcome actually happened

    @property
    def gap(self) -> float:
        return self.actual_rate - self.mean_predicted


def calibration_table(probs: Sequence[Probs], outcomes: Sequence[str],
                      n_buckets: int = 10) -> list[CalibrationRow]:
    """For each outcome, group forecasts into equal-width probability buckets and compare
    the average forecast with how often the outcome actually happened. Empty buckets are omitted.
    """
    _check(probs, outcomes)
    rows = []
    for k, name in enumerate(OUTCOMES):
        buckets: dict[int, list[tuple[float, int]]] = {}
        for p, o in zip(probs, outcomes):
            b = min(int(p[k] * n_buckets), n_buckets - 1)  # p == 1.0 goes in the top bucket
            buckets.setdefault(b, []).append((p[k], int(o == name)))
        for b in sorted(buckets):
            items = buckets[b]
            rows.append(CalibrationRow(
                outcome=name, bucket_low=b / n_buckets, bucket_high=(b + 1) / n_buckets,
                n=len(items), mean_predicted=sum(x for x, _ in items) / len(items),
                actual_rate=sum(y for _, y in items) / len(items)))
    return rows
