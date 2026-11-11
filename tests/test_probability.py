import math

import pytest

from openbetlab.probability import (
    complement,
    probability_to_percent,
    validate_probability,
)


@pytest.mark.parametrize("value", [0, 0.0, 0.25, 0.5, 1, 1.0])
def test_validate_probability_accepts_values_in_range(value):
    assert validate_probability(value) == float(value)


def test_validate_probability_returns_float():
    assert isinstance(validate_probability(1), float)


@pytest.mark.parametrize("value", [-0.0001, -1, 1.0001, 2, 100])
def test_validate_probability_rejects_out_of_range(value):
    with pytest.raises(ValueError, match="between 0 and 1"):
        validate_probability(value)


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_validate_probability_rejects_nan_and_infinity(value):
    with pytest.raises(ValueError, match="finite"):
        validate_probability(value)


@pytest.mark.parametrize("value", ["0.5", None, [0.5], True, False])
def test_validate_probability_rejects_non_numbers(value):
    with pytest.raises(TypeError):
        validate_probability(value)


def test_error_message_uses_custom_name():
    with pytest.raises(ValueError, match="chance"):
        validate_probability(2, name="chance")


@pytest.mark.parametrize(
    ("p", "expected"), [(0.0, 1.0), (0.25, 0.75), (0.5, 0.5), (1.0, 0.0)]
)
def test_complement(p, expected):
    assert complement(p) == pytest.approx(expected)


def test_complement_rejects_invalid():
    with pytest.raises(ValueError):
        complement(1.5)


@pytest.mark.parametrize(("p", "expected"), [(0.0, 0.0), (0.4, 40.0), (1.0, 100.0)])
def test_probability_to_percent(p, expected):
    assert probability_to_percent(p) == pytest.approx(expected)


def test_probability_to_percent_rejects_invalid():
    with pytest.raises(ValueError):
        probability_to_percent(-0.5)


def test_integer_too_large_for_float_is_a_value_error():
    with pytest.raises(ValueError, match="too large"):
        validate_probability(10**400)
