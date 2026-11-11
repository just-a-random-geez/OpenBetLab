import numpy as np
import pytest

from openbetlab.evaluation.calibration import Calibrator
from openbetlab.evaluation.metrics import log_loss


def _true_probs(n, seed):
    rng = np.random.default_rng(seed)
    z = rng.normal(0, 0.8, size=(n, 3)) + np.array([0.4, 0.0, 0.1])
    p = np.exp(z)
    return p / p.sum(axis=1, keepdims=True), rng


def _draw(p, rng):
    u = rng.random(len(p))
    c = p.cumsum(axis=1)
    return [("H", "D", "A")[int((u[i] > c[i]).sum())] for i in range(len(p))]


def _distort(p, w, b):
    q = np.exp(np.asarray(b) + w * np.log(p))
    return q / q.sum(axis=1, keepdims=True)


def test_already_calibrated_forecasts_are_left_almost_alone():
    p, rng = _true_probs(20000, 0)
    cal = Calibrator().fit([tuple(r) for r in p], _draw(p, rng))
    assert cal.w == pytest.approx(1, abs=0.05)
    assert cal.b == pytest.approx([0, 0, 0], abs=0.05)


def test_fixes_overconfidence_and_draw_bias():
    p, rng = _true_probs(20000, 1)
    outs = _draw(p, rng)
    shown = _distort(p, 2.0, [0, -0.3, 0])        # too confident, draws under-rated
    cal = Calibrator().fit([tuple(r) for r in shown], outs)
    assert cal.w == pytest.approx(0.5, abs=0.05)
    assert cal.b[1] == pytest.approx(0.15, abs=0.06)   # undoes -0.3 scaled by w
    # Apply to NEW data from the same process: log loss improves.
    p2, rng2 = _true_probs(20000, 2)
    outs2 = _draw(p2, rng2)
    shown2 = [tuple(r) for r in _distort(p2, 2.0, [0, -0.3, 0])]
    assert log_loss(cal.transform(shown2), outs2) < log_loss(shown2, outs2) - 0.01


def test_identity_parameters_change_nothing():
    cal = Calibrator()
    cal.w, cal.b = 1.0, np.zeros(3)
    probs = [(0.5, 0.3, 0.2), (0.1, 0.2, 0.7)]
    assert np.allclose(cal.transform(probs), probs)


def test_outputs_are_valid_probabilities():
    p, rng = _true_probs(2000, 3)
    cal = Calibrator().fit([tuple(r) for r in p], _draw(p, rng))
    out = cal.transform([(0.98, 0.01, 0.01), (1 / 3, 1 / 3, 1 / 3), (0.0, 0.5, 0.5)])
    for row in out:
        assert sum(row) == pytest.approx(1) and all(0 <= x <= 1 for x in row)


def test_errors():
    with pytest.raises(RuntimeError):
        Calibrator().transform([(0.5, 0.3, 0.2)])
    with pytest.raises(ValueError):
        Calibrator().fit([(0.5, 0.3, 0.2)], ["H", "D"])
