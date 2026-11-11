import csv
import datetime as dt
import json

from conftest import m

from openbetlab.data import build
from openbetlab.data.cleaning import clean
from openbetlab.data.quality_report import render


def test_report_counts(write_raw, mapper):
    write_raw("2020-21", "en.1", [m(score=[1, 0]), m(score=[1, 0]),
                                  m(date="2020-10-01", team1="Arsenal FC")])
    r = clean(write_raw("2019-20", "en.1", [m(score={}, status="cancelled")]),
              mapper, dt.date(2021, 1, 1))
    text = render(r, as_of=dt.date(2021, 1, 1),
                  source={"missing_files": ["2016-17/en.2.json"]})
    assert "Rows read: **4**" in text
    assert "Exact duplicates removed: **1**" in text
    assert "result missing 1" in text
    assert "| en.1 | 2020-21 | 3 | 1 | 0 | 0 | 2 | 1 | 0 | 0 | 0 | 1 | 3 |" in text
    assert "| en.1 | 2020-21 | 2020-10-01 | Arsenal FC | Hull City AFC |" in text
    assert "`2016-17/en.2.json`" in text
    assert "Suspected variants still present after mapping: none" in text


def test_build_writes_csv_with_empty_missing_cells(write_raw, tmp_path):
    raw = write_raw("2020-21", "en.1", [m(score={"ft": [2, 0]})])
    (raw / "manifest.json").write_text(json.dumps({"leagues": ["en.1"]}))
    names = tmp_path / "names"
    names.mkdir()
    (names / "t.csv").write_text("raw_name,canonical_name\nStoke City,Stoke City FC\n"
                                 "Stoke City FC,Stoke City FC\nHull City,Hull City AFC\n"
                                 "Hull City AFC,Hull City AFC\n")
    out, rep = tmp_path / "out.csv", tmp_path / "rep.md"
    build.main(["--raw-dir", str(raw), "--names-dir", str(names), "--out-csv", str(out),
                "--report", str(rep), "--as-of", "2021-01-01"])
    rows = list(csv.DictReader(out.open()))
    assert rows[0]["home_team"] == "Stoke City FC"
    assert rows[0]["ft_home"] == "2" and rows[0]["ht_home"] == ""
    assert "Unknown team names (not in mapping): **0**" in rep.read_text()
    info = json.loads((out.parent / "build_info.json").read_text())
    assert info["as_of"] == "2021-01-01" and info["clean_matches"] == 1
