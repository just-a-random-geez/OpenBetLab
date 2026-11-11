"""Post-hoc probability calibration for 1X2 forecasts.

Model:  calibrated p_k  ∝  exp(b_k + w * log p_k)      (b_home fixed at 0)

- w (temperature): w > 1 makes forecasts more confident, w < 1 less confident.
- b_draw, b_away: shift probability between outcomes (e.g. the model under-rates draws).
- w = 1, b = 0 leaves forecasts unchanged.

Only 3 numbers, fitted by maximum likelihood (Newton's method, the problem is convex).
It must be fitted on forecasts the model made *out of sample* (e.g. walk-forward over a
training season), never on the season it will be evaluated on.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .metrics import OUTCOMES, _check

_EPS = 1e-12


class Calibrator:
    def __init__(self) -> None:
        self.w: float | None = None
        self.b: np.ndarray | None = None  # [b_home=0, b_draw, b_away]
        self.n_fit = 0
        self.converged = False

    @staticmethod
    def _features(probs) -> np.ndarray:
        return np.log(np.clip(np.asarray(probs, dtype=float), _EPS, None))   # (n, 3)

    @staticmethod
    def _softmax(z: np.ndarray) -> np.ndarray:
        z = z - z.max(axis=1, keepdims=True)
        e = np.exp(z)
        return e / e.sum(axis=1, keepdims=True)

    def fit(self, probs: Sequence, outcomes: Sequence[str], max_iter: int = 50) -> "Calibrator":
        _check(probs, outcomes)
        x = self._features(probs)
        y = np.zeros_like(x)
        y[np.arange(len(outcomes)), [OUTCOMES.index(o) for o in outcomes]] = 1
        n = len(x)
        # Per-class feature vectors for theta = (w, b_draw, b_away): f[i, k, :]
        f = np.zeros((n, 3, 3))
        f[:, :, 0] = x
        f[:, 1, 1] = 1
        f[:, 2, 2] = 1
        theta = np.array([1.0, 0.0, 0.0])
        self.converged = False
        for _ in range(max_iter):
            q = self._softmax(np.einsum("nkj,j->nk", f, theta))
            grad = np.einsum("nk,nkj->j", q - y, f)
            mean_f = np.einsum("nk,nkj->nj", q, f)
            hess = (np.einsum("nk,nkj,nkl->jl", q, f, f)
                    - np.einsum("nj,nl->jl", mean_f, mean_f))
            step = np.linalg.solve(hess + 1e-9 * np.eye(3), grad)
            theta = theta - step
            if np.abs(step).max() < 1e-10:
                self.converged = True
                break
        if not self.converged or not np.isfinite(theta).all():
            import warnings
            warnings.warn("Calibrator did not converge; check the data (too few or extreme "
                          "forecasts?)", RuntimeWarning)
        self.w = float(theta[0])
        self.b = np.array([0.0, theta[1], theta[2]])
        self.n_fit = n
        return self

    def transform(self, probs: Sequence) -> list[tuple[float, float, float]]:
        if self.w is None:
            raise RuntimeError("fit() first")
        q = self._softmax(self.b + self.w * self._features(probs))
        return [tuple(map(float, row)) for row in q]
