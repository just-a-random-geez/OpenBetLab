from importlib import resources

import pytest

from openbetlab.odds import bookmaker_margin
from openbetlab.synthetic_data import SyntheticMatch, load_synthetic_matches


def test_loads_all_rows():
    matches = load_synthetic_matches()
    assert len(matches) == 8
    assert all(isinstance(m, SyntheticMatch) for m in matches)


def test_every_row_is_flagged_synthetic():
    assert all(m.is_synthetic for m in load_synthetic_matches())


def test_match_ids_are_unique_and_prefixed():
    ids = [m.match_id for m in load_synthetic_matches()]
    assert len(ids) == len(set(ids))
    assert all(i.startswith("SYN-") for i in ids)


def test_data_file_starts_with_synthetic_warning():
    text = resources.files("openbetlab").joinpath("data", "synthetic_matches.csv")
    first_line = text.read_text(encoding="utf-8").splitlines()[0]
    assert first_line.startswith("# SYNTHETIC DATA - NOT REAL")


def test_each_market_has_a_small_positive_margin():
    for m in load_synthetic_matches():
        margin = bookmaker_margin([m.odds_home, m.odds_draw, m.odds_away])
        assert 0 < margin < 0.15, m.match_id


def test_result_property():
    def make(home, away):
        return SyntheticMatch("X", "2025-01-01", "A", "B", home, away, 2.0, 3.0, 4.0)

    assert make(2, 1).result == "H"
    assert make(1, 1).result == "D"
    assert make(0, 3).result == "A"


def test_synthetic_flag_cannot_be_switched_off():
    with pytest.raises(TypeError):
        SyntheticMatch(
            "X", "2025-01-01", "A", "B", 1, 0, 2.0, 3.0, 4.0, is_synthetic=False
        )


def test_negative_goals_rejected():
    from openbetlab.synthetic_data import _parse_goals

    with pytest.raises(ValueError, match="must not be negative"):
        _parse_goals("-1", "home_goals", "SYN-X")
