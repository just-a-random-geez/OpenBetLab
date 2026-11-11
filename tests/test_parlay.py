import math

import pytest

from openbetlab.odds import break_even_probability
from openbetlab.parlay import combined_decimal_odds, joint_probability_independent

# --- combined parlay odds ---------------------------------------------------


@pytest.mark.parametrize(
    ("legs", "expected"),
    [
        ([2.0], 2.0),
        ([2.0, 2.0], 4.0),
        ([2.0, 1.5, 3.0], 9.0),
        ([1.1, 1.1, 1.1, 1.1], 1.1**4),
    ],
)
def test_combined_decimal_odds(legs, expected):
    assert combined_decimal_odds(legs) == pytest.approx(expected)


def test_combined_odds_accepts_tuple_and_generator():
    assert combined_decimal_odds((2.0, 3.0)) == pytest.approx(6.0)
    assert combined_decimal_odds(o for o in [2.0, 3.0]) == pytest.approx(6.0)


def test_combined_odds_rejects_empty():
    with pytest.raises(ValueError, match="at least one leg"):
        combined_decimal_odds([])


@pytest.mark.parametrize("bad", [1.0, 0.5, -3, math.nan, math.inf])
def test_combined_odds_rejects_invalid_leg(bad):
    with pytest.raises(ValueError, match=r"leg_odds\[1\]"):
        combined_decimal_odds([2.0, bad])


def test_combined_odds_rejects_non_number_leg():
    with pytest.raises(TypeError):
        combined_decimal_odds([2.0, "3.0"])


def test_parlay_break_even_is_product_of_leg_break_evens():
    legs = [1.8, 2.4, 3.1]
    product_of_legs = math.prod(break_even_probability(o) for o in legs)
    assert break_even_probability(combined_decimal_odds(legs)) == pytest.approx(
        product_of_legs
    )


# --- joint probability (independence assumption) ----------------------------


@pytest.mark.parametrize(
    ("probs", "expected"),
    [
        ([0.5], 0.5),
        ([0.5, 0.5], 0.25),
        ([0.5, 0.6], 0.3),
        ([0.9, 0.9, 0.9], 0.729),
        ([1.0, 1.0], 1.0),
        ([0.7, 0.0], 0.0),
    ],
)
def test_joint_probability_independent(probs, expected):
    assert joint_probability_independent(probs) == pytest.approx(expected)


def test_joint_probability_never_exceeds_smallest_input():
    probs = [0.8, 0.3, 0.95]
    assert joint_probability_independent(probs) <= min(probs)


def test_joint_probability_rejects_empty():
    with pytest.raises(ValueError, match="at least one"):
        joint_probability_independent([])


@pytest.mark.parametrize("bad", [-0.1, 1.1, math.nan])
def test_joint_probability_rejects_invalid(bad):
    with pytest.raises(ValueError, match=r"probabilities\[1\]"):
        joint_probability_independent([0.5, bad])


def test_joint_probability_documents_independence_assumption():
    doc = joint_probability_independent.__doc__
    assert doc is not None
    assert "INDEPENDENCE" in doc
    assert "SAME match" in doc


def test_combined_odds_rejects_overflow_to_infinity():
    with pytest.raises(ValueError, match="too large"):
        combined_decimal_odds([1e200, 1e200])
