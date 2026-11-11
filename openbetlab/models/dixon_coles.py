"""Dixon-Coles (1997) adjustment to the Poisson model.

Plain Poisson treats home and away goals as independent. In real football,
0-0 and 1-1 happen a bit more often and 1-0 / 0-1 a bit less (or vice versa)
than independence predicts. Dixon & Coles multiply the four low scores by

    tau(0,0) = 1 - lambda*mu*rho     tau(0,1) = 1 + lambda*rho
    tau(1,0) = 1 + mu*rho            tau(1,1) = 1 - rho
    (every other score: 1)

rho < 0 -> more 0-0 and 1-1, fewer 1-0 and 0-1 (more draws).
rho = 0 -> plain Poisson. The adjusted probabilities still add up to 1.

Their second idea, down-weighting old matches (time decay), is already in
PoissonModel (``half_life_days``), so this class adds only rho.

Fitting is two-step: attack/defence/home rates exactly as PoissonModel (time-weighted),
then rho per league by weighted maximum likelihood with those rates held fixed.
(The original paper fits everything jointly; with rho small the strengths barely move.)
"""

from __future__ import annotations

import math

import numpy as np

from .poisson import MAX_GOALS, PoissonModel, poisson_pmf

RHO_LIMIT = 0.5  # search range [-0.5, 0.5], further narrowed so every tau stays > 0


def tau(x: int, y: int, lam: float, mu: float, rho: float) -> float:
    if x == 0 and y == 0:
        return 1 - lam * mu * rho
    if x == 0 and y == 1:
        return 1 + lam * rho
    if x == 1 and y == 0:
        return 1 + mu * rho
    if x == 1 and y == 1:
        return 1 - rho
    return 1.0


def rho_bounds(lam, mu) -> tuple[float, float]:
    """Range of rho keeping every tau positive for all given (lambda, mu)."""
    lam, mu = np.atleast_1d(lam), np.atleast_1d(mu)
    lo = max(-RHO_LIMIT, float(np.max(-1 / np.maximum(lam, 1e-9))),
             float(np.max(-1 / np.maximum(mu, 1e-9))))
    hi = min(RHO_LIMIT, float(np.min(1 / np.maximum(lam * mu, 1e-9))), 1.0)
    return lo + 1e-6, hi - 1e-6


def score_matrix(lam: float, mu: float, rho: float, max_goals: int = MAX_GOALS) -> np.ndarray:
    """P(home scores i, away scores j), Dixon-Coles adjusted, renormalised after the cut-off."""
    ph = np.array([poisson_pmf(k, lam) for k in range(max_goals + 1)])
    pa = np.array([poisson_pmf(k, mu) for k in range(max_goals + 1)])
    m = np.outer(ph, pa)
    for x in (0, 1):
        for y in (0, 1):
            m[x, y] *= tau(x, y, lam, mu, rho)
    return m / m.sum()


def outcome_probs_dc(lam: float, mu: float, rho: float) -> tuple[float, float, float]:
    m = score_matrix(lam, mu, rho)
    return float(np.tril(m, -1).sum()), float(np.trace(m)), float(np.triu(m, 1).sum())


def fit_rho(lam, mu, gh, ga, w) -> float:
    """Weighted MLE of rho given each match's expected goals (lam, mu) and actual score.

    Only the tau terms depend on rho, so we maximise sum(w * log tau). The function is
    concave in rho, so golden-section search finds the maximum.
    """
    lam, mu, gh, ga, w = map(np.asarray, (lam, mu, gh, ga, w))
    low = (gh <= 1) & (ga <= 1)
    if not low.any():
        return 0.0
    lam, mu, gh, ga, w = lam[low], mu[low], gh[low], ga[low], w[low]
    c00 = (gh == 0) & (ga == 0)
    c01 = (gh == 0) & (ga == 1)
    c10 = (gh == 1) & (ga == 0)
    c11 = (gh == 1) & (ga == 1)

    def ll(rho):
        t = np.where(c00, 1 - lam * mu * rho, np.where(c01, 1 + lam * rho,
                     np.where(c10, 1 + mu * rho, np.where(c11, 1 - rho, 1.0))))
        return float((w * np.log(t)).sum())

    a, b = rho_bounds(lam, mu)
    g = (math.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = ll(c), ll(d)
    for _ in range(80):
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = ll(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = ll(d)
    return (a + b) / 2


class DixonColesModel(PoissonModel):
    name = "dixon_coles"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rho: dict[str, float] = {}

    def _after_fit(self) -> None:
        self.rho = {}
        for lg, ms in self.fit_data.items():
            p = self.params[lg]
            lam = [p.home_rate * p.attack[h] * p.defence[a] for h, a, _, _, _ in ms]
            mu = [p.away_rate * p.attack[a] * p.defence[h] for h, a, _, _, _ in ms]
            self.rho[lg] = fit_rho(lam, mu, [m[2] for m in ms], [m[3] for m in ms],
                                   [m[4] for m in ms])

    def predict(self, match):
        if self.as_of is None:
            raise ValueError("fit() first")
        super().predict(match)  # same date checks
        lam, mu = self.expected_goals(match)
        lo, hi = rho_bounds(lam, mu)
        return outcome_probs_dc(lam, mu, min(max(self.rho[match.league], lo), hi))
