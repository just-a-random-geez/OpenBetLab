import json

import pytest

from openbetlab.evaluation import run
from openbetlab.evaluation.baseline import LeagueAverageModel, UniformModel
from openbetlab.evaluation.data import (Result, latest_complete_season, outcome,
                                        results_from_rows, time_split)


def row(season, date, h, a, status="played", league="en.1", home="A FC", away="B FC"):
    return {"league": league, "season": season, "date": date, "home_team": home,
            "away_team": away, "status": status,
            "ft_home": "" if h is None else str(h), "ft_away": "" if a is None else str(a)}


ROWS = [
    row("2022-23", "2023-01-01", 2, 0),
    row("2020-21", "2020-10-01", 1, 1),
    row("2021-22", "2021-10-01", 0, 1),
    row("2021-22", "2021-11-01", 3, 1),
    row("2022-23", "2022-09-01", 1, 0),
    row("2022-23", "2022-10-01", None, None, status="result_missing"),
    row("2022-23", "2022-11-01", 0, 3, status="awarded"),
    row("2023-24", "2023-09-01", 2, 2),
    row("2023-24", "2024-04-01", None, None, status="scheduled"),
]


def test_outcome():
    assert (outcome(2, 1), outcome(1, 1), outcome(0, 3)) == ("H", "D", "A")


def test_flagged_dates_are_excluded():
    r = row("2019-20", "2019-07-04", 1, 0)
    r["date_flag"] = "inconsistent_with_round"
    assert results_from_rows([r]) == []


def test_out_of_season_dates_are_excluded():
    skipped = {}
    rs = results_from_rows([row("2025-26", "2025-03-01", 1, 0), row("2025-26", "2025-09-01", 1, 0)],
                           skipped)
    assert [r.date for r in rs] == ["2025-09-01"] and skipped == {"bad_date": 1}


def test_only_played_matches_used_and_sorted_by_time():
    rs = results_from_rows(ROWS)
    assert len(rs) == 6                                   # no missing, no awarded, no scheduled
    assert [(r.season, r.date) for r in rs] == sorted((r.season, r.date) for r in rs)


def test_latest_complete_season_skips_in_progress():
    assert latest_complete_season(ROWS) == "2022-23"


def test_time_split_never_trains_on_holdout_or_future():
    s = time_split(results_from_rows(ROWS), "2022-23")
    assert {m.season for m in s.train} == {"2020-21", "2021-22"}
    assert {m.season for m in s.test} == {"2022-23"} and len(s.test) == 2
    assert s.excluded_later == 1
    assert max(m.date for m in s.train) < min(m.date for m in s.test)
    assert not set(s.train) & set(s.test)


def test_time_split_errors():
    rs = results_from_rows(ROWS)
    with pytest.raises(ValueError, match="no played matches"):
        time_split(rs, "1999-00")
    with pytest.raises(ValueError, match="no seasons before"):
        time_split(rs, "2020-21")


def r(league, o):
    return Result(league, "2020-21", "2020-10-01", "A", "B", o)


def test_league_average_model():
    train = [r("en.1", o) for o in "HHDA"] + [r("en.2", o) for o in "HDDA"]
    model = LeagueAverageModel().fit(train)
    assert model.predict(r("en.1", "H")) == (0.5, 0.25, 0.25)
    assert model.predict(r("en.2", "H")) == (0.25, 0.5, 0.25)
    assert model.predict(r("xx.9", "H")) == (0.375, 0.375, 0.25)   # unseen league -> overall
    assert sum(model.predict(r("en.1", "H"))) == pytest.approx(1)


def test_league_average_needs_data():
    with pytest.raises(ValueError):
        LeagueAverageModel().fit([])
    with pytest.raises(RuntimeError):
        LeagueAverageModel().predict(r("en.1", "H"))


def test_uniform_model():
    assert UniformModel().fit([]).predict(r("en.1", "H")) == pytest.approx((1 / 3,) * 3)


def test_run_end_to_end(tmp_path):
    import csv
    path = tmp_path / "m.csv"
    rows = [row(s, f"{s[:4]}-10-0{i}", *sc) for s in ("2020-21", "2021-22", "2022-23")
            for i, sc in enumerate([(1, 0), (0, 0), (0, 2), (3, 1)], start=1)]
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    ev = run.evaluate(rows, half_lives=(180,), priors=(5,), elo_grid=[(20, 75, 100, 0.2)])
    assert all(len(f) == 4 for f in ev["forecasts"].values())
    assert set(ev["forecasts"]) >= {"poisson", "dixon_coles", "poisson_no_decay", "elo",
                                    "poisson_calibrated", "dixon_coles_calibrated",
                                    "elo_calibrated"}
    # Calibration fitted only on the validation season (a train season), before the test.
    test_start = min(m.date for m in ev["split"].test)
    for c in ev["calibration"].values():
        assert c["seasons"] == ["2021-22"] and c["last_date"] < test_start
        assert c["calibrator"].n_fit == 4

    fpath = tmp_path / "fc.csv"
    run.write_forecasts(ev, fpath)
    saved = list(csv.DictReader(fpath.open()))
    assert len(saved) == 4 and saved[0]["season"] == "2022-23"
    assert float(saved[0]["elo_home"]) + float(saved[0]["elo_draw"]) + \
        float(saved[0]["elo_away"]) == pytest.approx(1, abs=1e-5)
    meta = json.loads(fpath.with_suffix(".json").read_text())
    assert set(meta["validation_log_loss"]) == {"poisson", "dixon_coles", "elo"}
    assert meta["validation_season"] == "2021-22"

    from openbetlab.evaluation.comparison import render_comparison
    comp = render_comparison(ev, {"as_of": "2026-11-11", "source_commit": "abc",
                                  "leagues": ["en.1"]})
    assert "No betting edge is claimed" in comp
    assert "python -m openbetlab.data.build --as-of 2026-11-11" in comp
    assert "python -m openbetlab.evaluation.run --holdout-season 2022-23" in comp
    for name in ev["forecasts"]:
        assert f"| `{name}` |" in comp and f"### `{name}`" in comp
    text = run.render(ev)
    assert "season 2022-23" in text and "seasons 2020-21 to 2021-22" in text
    assert "tuned on 2021-22" in text
    assert "| uniform | ALL | 4 | 0.6667 | 1.0986 |" in text
    # train rates H .5 D .25 A .25; test outcomes H D A H -> Brier = (0.375+0.875+0.875+0.375)/4
    assert "| league_average | ALL | 4 | 0.6250 |" in text
