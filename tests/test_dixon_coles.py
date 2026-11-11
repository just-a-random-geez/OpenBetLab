import datetime as dt

import numpy as np
import pytest

from openbetlab.evaluation.data import Result, outcome
from openbetlab.models.dixon_coles import (DixonColesModel, fit_rho, outcome_probs_dc,
                                           rho_bounds, score_matrix, tau)
from openbetlab.models.poisson import PoissonModel, outcome_probs, walk_forward


def test_tau_values():
    lam, mu, rho = 1.4, 1.1, -0.1
    assert tau(0, 0, lam, mu, rho) == pytest.approx(1 + 1.4 * 1.1 * 0.1)
    assert tau(0, 1, lam, mu, rho) == pytest.approx(1 - 0.14)
    assert tau(1, 0, lam, mu, rho) == pytest.approx(1 - 0.11)
    assert tau(1, 1, lam, mu, rho) == pytest.approx(1.1)
    assert tau(2, 1, lam, mu, rho) == 1.0


def test_rho_zero_is_plain_poisson():
    assert outcome_probs_dc(1.5, 1.1, 0.0) == pytest.approx(outcome_probs(1.5, 1.1))


def test_adjustment_keeps_total_probability_at_one():
    # Unnormalised DC matrix (large cut-off) must already sum to 1.
    m = score_matrix(1.3, 1.0, -0.15, max_goals=30)
    assert m.sum() == pytest.approx(1.0)
    assert sum(outcome_probs_dc(1.3, 1.0, -0.15)) == pytest.approx(1.0)


def test_negative_rho_means_more_low_draws():
    plain, dc = score_matrix(1.3, 1.0, 0.0), score_matrix(1.3, 1.0, -0.15)
    assert dc[0, 0] > plain[0, 0] and dc[1, 1] > plain[1, 1]
    assert dc[1, 0] < plain[1, 0] and dc[0, 1] < plain[0, 1]
    assert outcome_probs_dc(1.3, 1.0, -0.15)[1] > outcome_probs(1.3, 1.0)[1]


def test_rho_bounds_keep_tau_positive():
    lo, hi = rho_bounds([2.0, 0.5], [3.0, 0.4])
    for lam, mu in ((2.0, 3.0), (0.5, 0.4)):
        for x in (0, 1):
            for y in (0, 1):
                assert tau(x, y, lam, mu, lo) > 0 and tau(x, y, lam, mu, hi) > 0


def _simulate(rho, n, lam=1.4, mu=1.1, seed=0):
    rng = np.random.default_rng(seed)
    m = score_matrix(lam, mu, rho, max_goals=12)
    flat = rng.choice(m.size, size=n, p=m.ravel())
    return np.divmod(flat, m.shape[1])


@pytest.mark.parametrize("true_rho", [-0.15, 0.0, 0.1])
def test_fit_rho_recovers_true_value(true_rho):
    gh, ga = _simulate(true_rho, 60000)
    n = len(gh)
    est = fit_rho([1.4] * n, [1.1] * n, gh, ga, [1.0] * n)
    assert est == pytest.approx(true_rho, abs=0.03)


def test_fit_rho_uses_weights():
    gh_a, ga_a = _simulate(-0.15, 30000, seed=1)
    gh_b, ga_b = _simulate(0.1, 30000, seed=2)
    gh, ga = np.concatenate([gh_a, gh_b]), np.concatenate([ga_a, ga_b])
    n = len(gh)
    w = np.r_[np.ones(30000), np.full(30000, 1e-3)]   # only the first half really counts
    assert fit_rho([1.4] * n, [1.1] * n, gh, ga, w) == pytest.approx(-0.15, abs=0.04)


def res(date, h, a, gh, ga):
    return Result("en.1", "2020-21", date, h, a, outcome(gh, ga), gh, ga)


def _history():
    teams = ["A", "B", "C", "D"]
    rng = np.random.default_rng(3)
    out, day = [], dt.date(2020, 8, 1)
    for _ in range(6):
        for h in teams:
            for a in teams:
                if h != a:
                    out.append(res(day.isoformat(), h, a, int(rng.poisson(1.4)),
                                   int(rng.poisson(1.1))))
                    day += dt.timedelta(days=1)
    return out


def test_model_fits_rho_and_predicts():
    hist = _history()
    m = DixonColesModel(365, 5).fit(hist, dt.date(2021, 1, 1))
    assert "en.1" in m.rho and -0.5 <= m.rho["en.1"] <= 0.5
    p = m.predict(res("2021-01-01", "A", "B", 0, 0))
    assert sum(p) == pytest.approx(1)
    # Same strengths as plain Poisson - only the low scores differ.
    plain = PoissonModel(365, 5).fit(hist, dt.date(2021, 1, 1))
    assert m.expected_goals(res("2021-01-01", "A", "B", 0, 0)) == pytest.approx(
        plain.expected_goals(res("2021-01-01", "A", "B", 0, 0)))


def test_dixon_coles_cannot_see_the_future():
    hist = _history()
    with pytest.raises(ValueError, match="leak"):
        DixonColesModel().fit(hist, dt.date.fromisoformat(hist[-1].date))
    targets = [res("2021-02-01", "A", "B", 1, 0), res("2021-02-08", "B", "A", 0, 0)]
    alt = [targets[0], res("2021-02-08", "B", "A", 7, 0)]
    assert walk_forward(DixonColesModel(), hist, targets) == \
        walk_forward(DixonColesModel(), hist, alt)


def test_rho_bounds_use_all_matches_not_only_low_scores():
    # reviewer case: a 3-1 match with lam=3, mu=1 limits rho < 1/3 even though it is not
    # a low score; rho must respect it so tau(0,0) stays positive for that match too
    gh, ga = _simulate(0.3, 20000, lam=1.0, mu=1.0, seed=4)
    n = len(gh)
    lam = [1.0] * n + [3.0]
    mu = [1.0] * n + [1.0]
    est = fit_rho(lam, mu, list(gh) + [3], list(ga) + [1], [1.0] * (n + 1))
    assert est < 1 / 3 and tau(0, 0, 3.0, 1.0, est) > 0
