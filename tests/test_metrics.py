import math

import pytest

from openbetlab.evaluation.metrics import brier_score, calibration_table, log_loss

U = (1 / 3, 1 / 3, 1 / 3)


def test_brier_perfect_worst_uniform():
    assert brier_score([(1, 0, 0)], ["H"]) == 0
    assert brier_score([(0, 0, 1)], ["H"]) == 2
    assert brier_score([U], ["D"]) == pytest.approx(2 / 3)


def test_brier_hand_computed():
    # (0.5-1)^2 + 0.3^2 + 0.2^2 = 0.38 ; (0.2)^2 + (0.3-1)^2 + 0.5^2 = 0.78 ; mean 0.58
    assert brier_score([(0.5, 0.3, 0.2), (0.2, 0.3, 0.5)], ["H", "D"]) == pytest.approx(0.58)


def test_log_loss_values():
    assert log_loss([U], ["A"]) == pytest.approx(math.log(3))
    assert log_loss([(0.5, 0.3, 0.2), (0.2, 0.3, 0.5)], ["H", "A"]) == pytest.approx(math.log(2))
    assert log_loss([(1, 0, 0)], ["H"]) == pytest.approx(0)


def test_log_loss_zero_probability_is_finite_but_huge():
    v = log_loss([(1, 0, 0)], ["A"])
    assert math.isfinite(v) and v > 30


def test_better_forecast_scores_better():
    outs = ["H", "H", "D"]
    good = [(0.7, 0.2, 0.1), (0.7, 0.2, 0.1), (0.3, 0.5, 0.2)]
    assert brier_score(good, outs) < brier_score([U] * 3, outs)
    assert log_loss(good, outs) < log_loss([U] * 3, outs)


@pytest.mark.parametrize("probs,outs", [
    ([(0.5, 0.5, 0.5)], ["H"]),        # doesn't sum to 1
    ([(1.2, -0.2, 0)], ["H"]),         # out of range
    ([(0.5, 0.5)], ["H"]),             # wrong length
    ([U], ["X"]),                      # bad outcome
    ([U, U], ["H"]),                   # length mismatch
    ([], []),                          # nothing
])
def test_invalid_input_rejected(probs, outs):
    with pytest.raises(ValueError):
        brier_score(probs, outs)
    with pytest.raises(ValueError):
        log_loss(probs, outs)


def test_calibration_table():
    probs = [(0.45, 0.25, 0.30), (0.45, 0.25, 0.30), (0.62, 0.20, 0.18), (1.0, 0.0, 0.0)]
    outs = ["H", "D", "H", "H"]
    rows = {(r.outcome, r.bucket_low): r for r in calibration_table(probs, outs)}
    r = rows[("H", 0.4)]
    assert (r.n, r.mean_predicted, r.actual_rate) == (2, pytest.approx(0.45), 0.5)
    assert r.gap == pytest.approx(0.05)
    assert rows[("H", 0.6)].actual_rate == 1.0
    assert rows[("H", 0.9)].n == 1                 # p = 1.0 lands in the top bucket
    assert rows[("D", 0.2)].n == 3 and rows[("D", 0.2)].actual_rate == pytest.approx(1 / 3)
    assert ("H", 0.0) not in rows                  # empty buckets omitted
    assert sum(r.n for r in calibration_table(probs, outs) if r.outcome == "A") == 4
