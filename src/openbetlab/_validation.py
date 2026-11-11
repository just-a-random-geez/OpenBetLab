"""Shared input checks used by every calculation module.

Keeping validation in one place means every public function rejects bad input
in the same way and with the same kind of error message.
"""

from __future__ import annotations

import math
from numbers import Real


def require_real_number(value: object, name: str) -> float:
    """Return ``value`` as a float, or raise if it is not a usable real number.

    Rejected inputs:

    * anything that is not a real number (strings, ``None``, lists, ...) -> TypeError
    * booleans (``True``/``False`` are technically ints in Python) -> TypeError
    * NaN ("not a number") and positive/negative infinity -> ValueError
    * integers too large to fit in a float (e.g. ``10**400``) -> ValueError
    """
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number, got {type(value).__name__}")
    try:
        number = float(value)
    except OverflowError:
        raise ValueError(f"{name} is too large to be a finite number") from None
    if math.isnan(number) or math.isinf(number):
        raise ValueError(f"{name} must be a finite number, got {value!r}")
    return number
