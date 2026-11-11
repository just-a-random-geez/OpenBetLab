import csv
import json

import pytest

from openbetlab.odds import compare as C
from openbetlab.settings import Settings


def fc_row(date, home, away, outcome, poisson, elo):
    r = {"league": "en.1", "season": "2025-26", "date": date, "home_team": home,
         "away_team": away, "outcome": outcome}
    for name, probs in (("poisson", poisson), ("elo", elo)):
        for k, p in zip(C.SEL, probs):
            r[f"{name}_{k}"] = str(p)
    return r


def mk_row(date, home, away, odds, snapshot="close"):
    imp = [1 / o for o in odds]
    tot = sum(imp)
    r = {"league": "en.1", "season": "2025-26", "match_date": date, "home_team": home,
         "away_team": away, "snapshot": snapshot, "overround": str(tot - 1)}
    for k, o, p in zip(C.SEL, odds, imp):
        r[f"odds_{k}"] = str(o)
        r[f"fair_prob_{k}"] = str(p / tot)
    return r


FC = [fc_row("2025-08-16", "A", "B", "H", (0.60, 0.25, 0.15), (0.50, 0.30, 0.20)),
      fc_row("2025-08-16", "C", "D", "A", (0.30, 0.30, 0.40), (0.35, 0.30, 0.35)),
      fc_row("2025-08-23", "E", "F", "D", (0.45, 0.30, 0.25), (0.40, 0.30, 0.30)),
      fc_row("2025-08-23", "G", "H", "H", (0.50, 0.30, 0.20), (0.50, 0.30, 0.20))]
MK = [mk_row("2025-08-16", "A", "B", (2.0, 4.0, 4.0)),          # fair .5/.25/.25
      mk_row("2025-08-16", "C", "D", (3.0, 3.0, 3.0)),
      mk_row("2025-08-23", "E", "F", (2.5, 3.2, 3.4)),
      mk_row("2025-08-16", "A", "B", (1.5, 5.0, 8.0), snapshot="24h"),
      {**mk_row("2025-08-23", "G", "H", (2.0, 3.0, 5.0)), "odds_draw": ""}]   # incomplete


def test_pick_model_uses_validation_scores_only():
    assert C.pick_model({"validation_log_loss": {"poisson": 1.037, "elo": 1.039}}) == "poisson"
    with pytest.raises(ValueError):
        C.pick_model({})


def test_join_uses_snapshot_and_skips_incomplete_prices():
    joined, counts = C.join(FC, MK, "poisson")
    assert counts == {"held_out": 4, "with_market": 3, "without_market": 1}
    ab = joined[0]
    assert ab.odds == (2.0, 4.0, 4.0) and ab.market == pytest.approx((0.5, 0.25, 0.25))
    early, _ = C.join(FC, MK, "poisson", snapshot="24h")
    assert len(early) == 1 and early[0].odds == (1.5, 5.0, 8.0)
    with pytest.raises(ValueError):
        C.join(FC, MK, "nonexistent")


def test_edge_formula():
    assert C.edge(0.6, 2.0) == pytest.approx(0.2)
    assert C.edge(0.5, 2.0) == pytest.approx(0.0)
    # after 5% commission: 0.6*1*0.95 - 0.4 = 0.17
    assert C.edge_after_commission(0.6, 2.0, 0.05) == pytest.approx(0.17)
    assert C.edge_after_commission(0.6, 2.0, 0.0) == pytest.approx(C.edge(0.6, 2.0))


def test_per_outcome_rows():
    joined, _ = C.join(FC, MK, "poisson")
    rows = C.per_outcome_rows(joined, 0.05)
    assert len(rows) == 9
    home = rows[0]
    assert (home["outcome"], home["happened"]) == ("home", 1)
    assert home["difference"] == pytest.approx(0.10)
    assert home["edge"] == pytest.approx(0.2)
    assert sum(r["happened"] for r in rows) == 3


def test_scores_compare_on_same_matches():
    joined, _ = C.join(FC, MK, "poisson")
    s = C.scores(joined)
    # Brier for A v B: model (0.4^2+0.25^2+0.15^2)=0.245, market (0.25+0.0625+0.0625)=0.375
    assert s["brier"]["model"] < s["brier"]["market"]
    assert s["brier"]["diff"] == pytest.approx(s["brier"]["model"] - s["brier"]["market"])


def test_verdict():
    assert C.verdict({"diff": -0.03, "se": 0.01}) == "model better than market"
    assert C.verdict({"diff": 0.03, "se": 0.01}) == "model worse than market"
    assert C.verdict({"diff": 0.01, "se": 0.01}) == "no clear difference"


def test_disagreements_threshold_and_order():
    joined, _ = C.join(FC, MK, "poisson")
    dis = C.disagreements(joined, 0.08)
    # A v B gap 0.10; E v F: fair ~ .385/.300/.283 vs .45/.30/.25 -> gap .065 (below)
    assert [j.key[3] for _, j in dis] == ["A"]
    assert C.disagreements(joined, 0.5) == []


def test_report_wording_never_says_value_bet():
    joined, counts = C.join(FC, MK, "poisson")
    text = C.render(joined, counts, "poisson", "close", Settings(disagreement_threshold=0.08),
                    {"validation_season": "2024-25", "holdout_season": "2025-26"},
                    {"poisson": joined, "elo": C.join(FC, MK, "elo")[0]})
    assert "No pick in this report is a value bet" in text
    lowered = text.lower().replace("no pick in this report is a value bet", "")
    lowered = lowered.replace("not value bets", "")
    assert "value bet" not in lowered
    assert "A v B" in text and "| `elo` |" in text and "PRIVATE" in text


def test_cli_end_to_end(tmp_path):
    def write(path, rows):
        with path.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    fpath, mpath = tmp_path / "forecasts.csv", tmp_path / "mk.csv"
    write(fpath, FC)
    keys = list(MK[0])
    write(mpath, [{k: r.get(k, "") for k in keys} for r in MK])
    fpath.with_suffix(".json").write_text(json.dumps(
        {"validation_log_loss": {"poisson": 1.0, "elo": 1.1}}))
    out, rep = tmp_path / "o.csv", tmp_path / "r.md"
    assert C.main(["--forecasts", str(fpath), "--market", str(mpath), "--out-csv", str(out),
                   "--report", str(rep)]) == 0
    assert "Model: `poisson`" in rep.read_text()
    assert len(list(csv.DictReader(out.open()))) == 9


def test_cli_missing_inputs(tmp_path):
    assert C.main(["--forecasts", str(tmp_path / "x.csv"), "--market", str(tmp_path / "y.csv")]) == 1
