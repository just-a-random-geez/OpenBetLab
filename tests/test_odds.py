import math

import pytest

from openbetlab.odds import (
    bookmaker_margin,
    break_even_probability,
    expected_value,
    implied_probability,
    potential_profit,
    potential_return,
    probability_to_decimal_odds,
    validate_decimal_odds,
)

# --- validation -------------------------------------------------------------


@pytest.mark.parametrize("odds", [1.01, 2, 2.5, 1000])
def test_validate_decimal_odds_accepts_valid(odds):
    assert validate_decimal_odds(odds) == float(odds)


@pytest.mark.parametrize("odds", [1.0, 1, 0.5, 0, -2])
def test_validate_decimal_odds_rejects_one_or_below(odds):
    with pytest.raises(ValueError, match="greater than 1.0"):
        validate_decimal_odds(odds)


@pytest.mark.parametrize("odds", [math.nan, math.inf, -math.inf])
def test_validate_decimal_odds_rejects_nan_and_infinity(odds):
    with pytest.raises(ValueError, match="finite"):
        validate_decimal_odds(odds)


@pytest.mark.parametrize("odds", ["2.5", None, True])
def test_validate_decimal_odds_rejects_non_numbers(odds):
    with pytest.raises(TypeError):
        validate_decimal_odds(odds)


# --- implied / break-even probability ----------------------------------------


@pytest.mark.parametrize(
    ("odds", "expected"),
    [(2.0, 0.5), (4.0, 0.25), (1.25, 0.8), (10.0, 0.1), (3.0, 1 / 3)],
)
def test_break_even_probability(odds, expected):
    assert break_even_probability(odds) == pytest.approx(expected)


def test_break_even_equals_implied_probability():
    assert break_even_probability(2.75) == implied_probability(2.75)


def test_break_even_rejects_invalid_odds():
    with pytest.raises(ValueError):
        break_even_probability(1.0)


def test_break_even_gives_zero_expected_value():
    """At the break-even probability, expected profit should be exactly zero."""
    for odds in [1.5, 2.0, 3.3, 7.25]:
        p = break_even_probability(odds)
        assert expected_value(p, odds, stake=10) == pytest.approx(0.0, abs=1e-12)


# --- probability -> odds ----------------------------------------------------


@pytest.mark.parametrize(("p", "expected"), [(0.5, 2.0), (0.25, 4.0), (0.8, 1.25)])
def test_probability_to_decimal_odds(p, expected):
    assert probability_to_decimal_odds(p) == pytest.approx(expected)


@pytest.mark.parametrize("p", [0.0, 1.0])
def test_probability_to_decimal_odds_rejects_zero_and_one(p):
    with pytest.raises(ValueError, match="strictly between 0 and 1"):
        probability_to_decimal_odds(p)


def test_probability_to_decimal_odds_rejects_out_of_range():
    with pytest.raises(ValueError):
        probability_to_decimal_odds(1.5)


@pytest.mark.parametrize("odds", [1.1, 2.0, 3.75, 51.0])
def test_odds_probability_round_trip(odds):
    assert probability_to_decimal_odds(implied_probability(odds)) == pytest.approx(odds)


# --- returns, profit, expected value ----------------------------------------


def test_potential_return_and_profit():
    assert potential_return(10, 2.5) == pytest.approx(25.0)
    assert potential_profit(10, 2.5) == pytest.approx(15.0)


def test_zero_stake_is_allowed():
    assert potential_return(0, 3.0) == 0.0
    assert potential_profit(0, 3.0) == 0.0


@pytest.mark.parametrize("func", [potential_return, potential_profit])
def test_negative_stake_rejected(func):
    with pytest.raises(ValueError, match="stake"):
        func(-1, 2.0)


@pytest.mark.parametrize(
    ("p", "odds", "stake", "expected"),
    [
        (0.5, 2.0, 1.0, 0.0),  # fair bet
        (0.6, 2.0, 1.0, 0.2),  # positive under the assumption
        (0.4, 2.0, 10.0, -2.0),  # negative under the assumption
        (0.0, 5.0, 1.0, -1.0),  # certain loss
        (1.0, 5.0, 1.0, 4.0),  # certain win
    ],
)
def test_expected_value(p, odds, stake, expected):
    assert expected_value(p, odds, stake) == pytest.approx(expected)


def test_expected_value_validates_inputs():
    with pytest.raises(ValueError):
        expected_value(1.2, 2.0)
    with pytest.raises(ValueError):
        expected_value(0.5, 0.9)
    with pytest.raises(ValueError):
        expected_value(0.5, 2.0, stake=-5)


# --- bookmaker margin -------------------------------------------------------


def test_bookmaker_margin_fair_market_is_zero():
    assert bookmaker_margin([2.0, 2.0]) == pytest.approx(0.0)
    assert bookmaker_margin([3.0, 3.0, 3.0]) == pytest.approx(0.0)


def test_bookmaker_margin_typical_market():
    # 1/1.9 + 1/1.9 = 1.0526...
    assert bookmaker_margin([1.9, 1.9]) == pytest.approx(2 / 1.9 - 1)


def test_bookmaker_margin_accepts_generator():
    assert bookmaker_margin(o for o in [2.0, 2.0]) == pytest.approx(0.0)


@pytest.mark.parametrize("odds", [[], [2.0]])
def test_bookmaker_margin_needs_two_outcomes(odds):
    with pytest.raises(ValueError, match="at least two"):
        bookmaker_margin(odds)


def test_bookmaker_margin_rejects_invalid_leg():
    with pytest.raises(ValueError, match=r"odds\[1\]"):
        bookmaker_margin([2.0, 1.0])


@pytest.mark.parametrize("func", [potential_return, potential_profit])
def test_returns_reject_invalid_odds(func):
    with pytest.raises(ValueError, match="odds"):
        func(10, 1.0)


def test_bookmaker_margin_can_be_negative_for_inconsistent_prices():
    # Implied probabilities sum to below 100%: the function reports it honestly.
    assert bookmaker_margin([2.2, 2.2]) < 0
