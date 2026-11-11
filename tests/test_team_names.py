import csv
from pathlib import Path

import pytest

from openbetlab.data.team_names import (TeamNameMapper, find_suspected_variants,
                                        normalize_whitespace)

NAMES_DIR = Path(__file__).resolve().parents[1] / "data" / "team_names"


def test_normalize_whitespace():
    assert normalize_whitespace("  Stoke   City\tFC ") == "Stoke City FC"


def test_alias_and_canonical_map_to_same_name(mapper):
    assert mapper.canonical("Stoke City") == "Stoke City FC"
    assert mapper.canonical("Stoke City FC") == "Stoke City FC"
    assert mapper.canonical(" Stoke  City ") == "Stoke City FC"
    assert mapper.unknown == set()


def test_unknown_name_kept_and_reported(mapper):
    assert mapper.canonical("Brand New Town") == "Brand New Town"
    assert mapper.unknown == {"Brand New Town"}


def _write_csv(tmp_path, rows):
    p = tmp_path / "x.csv"
    with p.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["raw_name", "canonical_name"])
        w.writerows(rows)
    return tmp_path


def test_csv_with_contradicting_rows_is_rejected(tmp_path):
    d = _write_csv(tmp_path, [["A", "A FC"], ["A", "A AFC"], ["A FC", "A FC"], ["A AFC", "A AFC"]])
    with pytest.raises(ValueError, match="mapped to both"):
        TeamNameMapper.from_csv_dir(d)


def test_csv_with_chained_mapping_is_rejected(tmp_path):
    d = _write_csv(tmp_path, [["A", "A FC"], ["A FC", "A AFC"]])
    with pytest.raises(ValueError, match="remapped"):
        TeamNameMapper.from_csv_dir(d)


def test_suspected_variants():
    assert find_suspected_variants(["Stoke City", "Stoke City FC", "Burnley FC", "Barnsley FC"]) \
        == [["Stoke City", "Stoke City FC"]]


def test_england_mapping_is_consistent():
    mapper = TeamNameMapper.from_csv_dir(NAMES_DIR)  # raises if contradictory/chained
    canon = set(mapper.mapping.values())
    assert find_suspected_variants(canon) == []        # one name per club
    assert mapper.canonical("Manchester City") == mapper.canonical("Manchester City FC")
    assert mapper.canonical("Hull City") == "Hull City AFC"
    # Different clubs must stay different.
    assert mapper.canonical("Manchester City") != mapper.canonical("Manchester United")
    assert mapper.canonical("AFC Wimbledon") != mapper.canonical("Milton Keynes Dons")
