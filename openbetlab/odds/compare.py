"""Compare model forecasts with the Betfair market on the held-out season.

    python -m openbetlab.odds.compare [--model poisson] [--snapshot close]

Inputs : data/clean/forecasts.csv (+ .json)   from `python -m openbetlab.evaluation.run`
         data/odds/betfair_match_probs.csv    from `python -m openbetlab.odds.build`
Outputs (gitignored - contain Betfair prices, personal use only):
         data/odds/model_vs_market.csv        one row per match x outcome
         reports/private/model_vs_market.md

Definitions (per match and outcome):
- model probability: the chosen model's forecast (made from earlier matches only)
- fair market probability: implied probabilities with the margin removed (proportional)
- difference: model - market
- edge = model probability x odds - 1  (odds = market price at the snapshot)
- edge after commission = p*(odds-1)*(1-c) - (1-p)
"Edge" here is only arithmetic on the model's own numbers. It is NOT a value-bet signal:
the model is not shown to be better than the market, and nothing has been backtested.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path

from openbetlab.evaluation.metrics import (brier_per_match, calibration_table,
                                           log_loss_per_match, paired_difference)
from openbetlab.settings import ROOT, Settings, load_settings

SEL = ("home", "draw", "away")
_OUT = {"H": "home", "D": "draw", "A": "away"}


@dataclass
class Joined:
    key: tuple                  # (league, season, date, home, away)
    outcome: str                # "H" / "D" / "A"
    model: tuple[float, float, float]
    market: tuple[float, float, float]     # fair (margin removed)
    odds: tuple[float, float, float]
    overround: float


def pick_model(meta: dict) -> str:
    """Model with the lowest VALIDATION log loss (training data only, never the test set)."""
    vll = meta.get("validation_log_loss") or {}
    if not vll:
        raise ValueError("forecasts metadata has no validation scores; pass --model")
    return min(vll, key=vll.get)


def _f(x: str) -> float | None:
    return float(x) if x not in ("", None) else None


def join(forecast_rows: list[dict], market_rows: list[dict], model: str,
         snapshot: str = "close") -> tuple[list[Joined], dict]:
    """Held-out matches that have both a model forecast and a complete market price."""
    if forecast_rows and f"{model}_home" not in forecast_rows[0]:
        raise ValueError(f"model {model!r} not in forecasts file")
    market = {}
    for r in market_rows:
        if r["snapshot"] != snapshot or not r.get("home_team"):
            continue
        odds = tuple(_f(r[f"odds_{k}"]) for k in SEL)
        fair = tuple(_f(r[f"fair_prob_{k}"]) for k in SEL)
        if None in odds or None in fair:
            continue
        market[(r["league"], r["season"], r["match_date"], r["home_team"], r["away_team"])] = \
            (fair, odds, _f(r["overround"]))
    joined, no_price = [], 0
    for r in forecast_rows:
        key = (r["league"], r["season"], r["date"], r["home_team"], r["away_team"])
        if key not in market:
            no_price += 1
            continue
        fair, odds, ovr = market[key]
        joined.append(Joined(key, r["outcome"], tuple(float(r[f"{model}_{k}"]) for k in SEL),
                             fair, odds, ovr))
    return joined, {"held_out": len(forecast_rows), "with_market": len(joined),
                    "without_market": no_price}


def edge(p: float, odds: float) -> float:
    """Model probability x odds - 1: expected return per 1 unit staked IF p were true."""
    return p * odds - 1


def edge_after_commission(p: float, odds: float, commission: float) -> float:
    return p * (odds - 1) * (1 - commission) - (1 - p)


def per_outcome_rows(joined: list[Joined], commission: float) -> list[dict]:
    rows = []
    for j in joined:
        for i, k in enumerate(SEL):
            rows.append({
                "league": j.key[0], "season": j.key[1], "date": j.key[2],
                "home_team": j.key[3], "away_team": j.key[4], "outcome": k,
                "happened": int(_OUT[j.outcome] == k),
                "model_prob": round(j.model[i], 6), "market_fair_prob": round(j.market[i], 6),
                "difference": round(j.model[i] - j.market[i], 6), "odds": j.odds[i],
                "edge": round(edge(j.model[i], j.odds[i]), 6),
                "edge_after_commission": round(edge_after_commission(j.model[i], j.odds[i],
                                                                     commission), 6)})
    return rows


def scores(joined: list[Joined]) -> dict:
    outs = [j.outcome for j in joined]
    model, market = [j.model for j in joined], [j.market for j in joined]
    res = {}
    for name, fn in (("brier", brier_per_match), ("log_loss", log_loss_per_match)):
        a, b = fn(model, outs), fn(market, outs)
        diff, se = paired_difference(a, b)
        res[name] = {"model": sum(a) / len(a), "market": sum(b) / len(b), "diff": diff, "se": se}
    return res


def verdict(s: dict) -> str:
    d, se = s["diff"], s["se"]
    if d < -2 * se:
        return "model better than market"
    if d > 2 * se:
        return "model worse than market"
    return "no clear difference"


def disagreements(joined: list[Joined], threshold: float) -> list[tuple[float, Joined]]:
    out = []
    for j in joined:
        gap = max(abs(m - k) for m, k in zip(j.model, j.market))
        if gap >= threshold:
            out.append((gap, j))
    return sorted(out, key=lambda x: (-x[0], x[1].key))


def _table(headers, rows) -> str:
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
                     + ["| " + " | ".join(str(v) for v in r) + " |" for r in rows])


def render(joined: list[Joined], counts: dict, model: str, snapshot: str, settings: Settings,
           meta: dict, all_models: dict[str, list[Joined]] | None = None) -> str:
    sc = scores(joined)
    lines = [
        "# Model vs Market (PRIVATE - contains Betfair prices, personal use only)", "",
        "> No pick in this report is a value bet. 'Edge' is the model's own arithmetic "
        "(model probability x odds - 1). A positive number only means the model disagrees "
        "with the price; it says nothing about whether the model is right.", "",
        f"- Model: `{model}` (chosen by lowest validation log loss on "
        f"{meta.get('validation_season', '?')}, before looking at the market)",
        f"- Market: Betfair last traded prices at snapshot `{snapshot}`, margin removed "
        "proportionally",
        f"- Held-out season {meta.get('holdout_season', '?')}: {counts['held_out']} matches, "
        f"{counts['with_market']} with a complete market price, "
        f"{counts['without_market']} without (not scored)",
        f"- Commission used for 'edge after commission': {settings.commission:.1%}", "",
        "## Who is more accurate?", "",
        "Same matches for both. Lower is better. Difference = model minus market; beyond "
        "±2 standard errors is unlikely to be chance.", "",
        _table(["Score", "Model", "Market", "Difference", "Std. error", "Verdict"],
               [[n, f"{s['model']:.4f}", f"{s['market']:.4f}", f"{s['diff']:+.4f}",
                 f"{s['se']:.4f}", verdict(s)] for n, s in (("Brier", sc["brier"]),
                                                            ("Log loss", sc["log_loss"]))]),
    ]
    if all_models:
        rows = []
        for name, js in all_models.items():
            s = scores(js)
            rows.append([f"`{name}`", f"{s['brier']['model']:.4f}", f"{s['log_loss']['model']:.4f}",
                         f"{s['log_loss']['diff']:+.4f} ({s['log_loss']['diff'] / s['log_loss']['se']:+.1f} SE)",
                         verdict(s["log_loss"])])
        rows.append(["market", f"{sc['brier']['market']:.4f}", f"{sc['log_loss']['market']:.4f}",
                     "-", "-"])
        lines += ["", "### Every model on the same matches", "",
                  _table(["Model", "Brier", "Log loss", "Log loss vs market", "Verdict"], rows)]

    ovr = [j.overround for j in joined if j.overround is not None]
    if ovr:
        lines += ["", f"Market overround at this snapshot: mean {sum(ovr) / len(ovr):+.4f}, "
                  f"min {min(ovr):+.4f}, max {max(ovr):+.4f}."]

    label = dict(zip("HDA", SEL))
    lines += ["", "## Market calibration (same matches)", "",
              _table(["Outcome", "Bucket", "Matches", "Mean predicted", "Actual", "Gap"],
                     [[label[r.outcome], f"{r.bucket_low:.1f}-{r.bucket_high:.1f}", r.n,
                       f"{r.mean_predicted:.3f}", f"{r.actual_rate:.3f}", f"{r.gap:+.3f}"]
                      for r in calibration_table([j.market for j in joined],
                                                 [j.outcome for j in joined])])]

    dis = disagreements(joined, settings.disagreement_threshold)
    lines += ["", f"## Matches where model and market disagree "
              f"(≥ {settings.disagreement_threshold:.0%} on any outcome): {len(dis)}", "",
              "Probabilities as model / market. Edge = model probability × odds − 1 for the "
              "outcome with the biggest gap. Not value bets.", ""]
    rows = []
    for gap, j in dis:
        i = max(range(3), key=lambda k: abs(j.model[k] - j.market[k]))
        rows.append([j.key[2], j.key[0], f"{j.key[3]} v {j.key[4]}",
                     *(f"{j.model[k]:.2f} / {j.market[k]:.2f}" for k in range(3)),
                     SEL[i], f"{j.model[i] - j.market[i]:+.2f}", f"{j.odds[i]:.2f}",
                     f"{edge(j.model[i], j.odds[i]):+.3f}", _OUT[j.outcome]])
    lines.append(_table(["Date", "League", "Match", "Home", "Draw", "Away", "Biggest gap on",
                         "Gap", "Odds", "Edge", "Result"], rows) if rows else "None.")
    return "\n".join(lines) + "\n"


def _read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--forecasts", type=Path, default=ROOT / "data/clean/forecasts.csv")
    p.add_argument("--market", type=Path, default=ROOT / "data/odds/betfair_match_probs.csv")
    p.add_argument("--model", default=None, help="default: best validation log loss")
    p.add_argument("--snapshot", default="close")
    p.add_argument("--out-csv", type=Path, default=ROOT / "data/odds/model_vs_market.csv")
    p.add_argument("--report", type=Path, default=ROOT / "reports/private/model_vs_market.md")
    p.add_argument("--settings", type=Path, default=ROOT / "config/settings.toml")
    a = p.parse_args(argv)
    for path, how in ((a.forecasts, "python -m openbetlab.evaluation.run"),
                      (a.market, "python -m openbetlab.odds.build")):
        if not path.exists():
            print(f"Missing {path}. Run: {how}")
            return 1
    settings = load_settings(a.settings)
    meta_path = a.forecasts.with_suffix(".json")
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    model = a.model or pick_model(meta)
    fc, mk = _read(a.forecasts), _read(a.market)
    joined, counts = join(fc, mk, model, a.snapshot)
    if not joined:
        print("No held-out match has both a forecast and a complete market price.")
        return 1
    others = [c[:-5] for c in fc[0] if c.endswith("_home")]
    all_models = {m: join(fc, mk, m, a.snapshot)[0] for m in others}
    a.out_csv.parent.mkdir(parents=True, exist_ok=True)
    rows = per_outcome_rows(joined, settings.commission)
    with a.out_csv.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(render(joined, counts, model, a.snapshot, settings, meta, all_models),
                        encoding="utf-8")
    print(f"{counts['with_market']} matches compared -> {a.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
