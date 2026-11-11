"""Backtest summary statistics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

BOOTSTRAP_SEED = 20261111
BOOTSTRAP_RESAMPLES = 10_000


@dataclass
class Summary:
    bets: int
    wins: int
    hit_rate: float | None
    staked: float
    profit: float
    roi: float | None
    roi_ci95: tuple[float, float] | None
    avg_clv: float | None
    clv_bets: int
    max_drawdown: float          # GBP, peak to trough
    max_drawdown_pct: float      # of the peak bankroll
    longest_losing_run: int
    final_bankroll: float
    ruined: bool                 # bankroll fell below one stake; betting stopped
    curve: list[float]           # bankroll after each bet, starting value first


def bankroll_curve(profits: list[float], start: float, stake: float):
    """Bankroll after each bet. Stops (ruin) when the bankroll can't cover a stake."""
    curve, bank, used, ruined = [start], start, 0, False
    for p in profits:
        if bank < stake:
            ruined = True
            break
        bank += p
        curve.append(bank)
        used += 1
    return curve, used, ruined


def max_drawdown(curve: list[float]) -> tuple[float, float]:
    peak, worst, worst_pct = curve[0], 0.0, 0.0
    for v in curve:
        peak = max(peak, v)
        if peak - v > worst:
            worst, worst_pct = peak - v, (peak - v) / peak if peak > 0 else 0.0
    return worst, worst_pct


def longest_losing_run(results: list[bool]) -> int:
    best = cur = 0
    for won in results:
        cur = 0 if won else cur + 1
        best = max(best, cur)
    return best


def bootstrap_roi_ci(profits: list[float], stake: float,
                     resamples: int = BOOTSTRAP_RESAMPLES, seed: int = BOOTSTRAP_SEED):
    """95% interval for ROI by resampling bets with replacement (fixed seed)."""
    if len(profits) < 2:
        return None
    rng = np.random.default_rng(seed)
    arr = np.asarray(profits)
    idx = rng.integers(0, len(arr), size=(resamples, len(arr)))
    rois = arr[idx].sum(axis=1) / (stake * len(arr))
    return float(np.percentile(rois, 2.5)), float(np.percentile(rois, 97.5))


def summarise(profits: list[float], wins: list[bool], clvs: list[float | None],
              stake: float, start: float) -> Summary:
    curve, used, ruined = bankroll_curve(profits, start, stake)
    profits, wins, clvs = profits[:used], wins[:used], clvs[:used]
    n = len(profits)
    staked = stake * n
    clv_vals = [c for c in clvs if c is not None]
    dd, dd_pct = max_drawdown(curve)
    return Summary(
        bets=n, wins=sum(wins), hit_rate=sum(wins) / n if n else None, staked=staked,
        profit=sum(profits), roi=sum(profits) / staked if n else None,
        roi_ci95=bootstrap_roi_ci(profits, stake), avg_clv=(sum(clv_vals) / len(clv_vals)
                                                            if clv_vals else None),
        clv_bets=len(clv_vals), max_drawdown=dd, max_drawdown_pct=dd_pct,
        longest_losing_run=longest_losing_run(wins), final_bankroll=curve[-1], ruined=ruined,
        curve=curve)
