"""Backtest summary statistics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

BOOTSTRAP_SEED = 20261111
BOOTSTRAP_RESAMPLES = 10_000


@dataclass
class Summary:
    bets: int                    # bets actually placed (before any ruin)
    wins: int
    hit_rate: float | None
    staked: float
    profit: float
    roi: float | None
    roi_ci95: tuple[float, float] | None   # bootstrap by match DAY (bets on a day move together)
    roi_all_bets: float | None   # ROI over every qualifying bet, ignoring ruin
    qualifying_bets: int
    avg_clv: float | None        # before commission
    clv_bets: int
    max_drawdown: float          # GBP, largest peak-to-trough fall
    max_drawdown_pct: float      # largest fall as a share of the peak it fell from
    longest_losing_run: int
    final_bankroll: float
    ruined: bool                 # bankroll fell below one stake; betting stopped
    curve: list[float]           # bankroll after each placed bet, starting value first


def bankroll_curve(profits: list[float], start: float, stake: float,
                   groups: list | None = None):
    """Bankroll after each bet.

    Bets sharing a group key (same kick-off) are placed at the same time, so together
    they must fit in the bankroll: within a group a bet is placed only if the money not
    yet committed covers its stake. Betting stops for good (ruin) once the bankroll is
    below one stake. Returns (curve, indices of placed bets, ruined).
    """
    groups = groups if groups is not None else list(range(len(profits)))
    curve, bank, placed, ruined = [start], start, [], False
    i = 0
    while i < len(profits):
        j = i
        while j < len(profits) and groups[j] == groups[i]:
            j += 1
        if bank < stake:
            ruined = True
            break
        committed, group_placed = 0.0, []
        for k in range(i, j):
            if bank - committed >= stake:
                committed += stake
                group_placed.append(k)
        for k in group_placed:
            bank += profits[k]
            curve.append(bank)
            placed.append(k)
        i = j
    if not ruined and bank < stake and len(placed) < len(profits):
        ruined = True
    return curve, placed, ruined


def max_drawdown(curve: list[float]) -> tuple[float, float]:
    """(largest fall in GBP, largest fall as a share of its peak) - tracked separately,
    because the biggest GBP fall need not be the biggest percentage fall."""
    peak, worst, worst_pct = curve[0], 0.0, 0.0
    for v in curve:
        peak = max(peak, v)
        worst = max(worst, peak - v)
        if peak > 0:
            worst_pct = max(worst_pct, (peak - v) / peak)
    return worst, worst_pct


def longest_losing_run(results: list[bool]) -> int:
    best = cur = 0
    for won in results:
        cur = 0 if won else cur + 1
        best = max(best, cur)
    return best


def bootstrap_roi_ci(profits: list[float], stake: float, clusters: list | None = None,
                     resamples: int = BOOTSTRAP_RESAMPLES, seed: int = BOOTSTRAP_SEED):
    """95% interval for ROI by resampling whole clusters (default: each bet its own
    cluster; the backtest passes match DATES, because results on one day are not
    independent). Fixed seed."""
    if len(profits) < 2:
        return None
    clusters = clusters if clusters is not None else list(range(len(profits)))
    keys = sorted(set(clusters))
    idx = {k: i for i, k in enumerate(keys)}
    prof = np.zeros(len(keys))
    count = np.zeros(len(keys))
    for p, c in zip(profits, clusters):
        prof[idx[c]] += p
        count[idx[c]] += 1
    rng = np.random.default_rng(seed)
    pick = rng.integers(0, len(keys), size=(resamples, len(keys)))
    rois = prof[pick].sum(axis=1) / (stake * count[pick].sum(axis=1))
    return float(np.percentile(rois, 2.5)), float(np.percentile(rois, 97.5))


def summarise(profits: list[float], wins: list[bool], clvs: list[float | None],
              stake: float, start: float, groups: list | None = None,
              clusters: list | None = None) -> Summary:
    """``groups``: kick-off time per bet (simultaneous bets); ``clusters``: match date
    per bet (for the bootstrap)."""
    n_all = len(profits)
    roi_all = sum(profits) / (stake * n_all) if n_all else None
    curve, placed, ruined = bankroll_curve(profits, start, stake, groups)
    p = [profits[k] for k in placed]
    w = [wins[k] for k in placed]
    c = [clvs[k] for k in placed]
    cl = [clusters[k] for k in placed] if clusters is not None else None
    n = len(p)
    clv_vals = [x for x in c if x is not None]
    dd, dd_pct = max_drawdown(curve)
    return Summary(
        bets=n, wins=sum(w), hit_rate=sum(w) / n if n else None, staked=stake * n,
        profit=sum(p), roi=sum(p) / (stake * n) if n else None,
        roi_ci95=bootstrap_roi_ci(p, stake, cl), roi_all_bets=roi_all, qualifying_bets=n_all,
        avg_clv=sum(clv_vals) / len(clv_vals) if clv_vals else None, clv_bets=len(clv_vals),
        max_drawdown=dd, max_drawdown_pct=dd_pct, longest_losing_run=longest_losing_run(w),
        final_bankroll=curve[-1], ruined=ruined, curve=curve)
