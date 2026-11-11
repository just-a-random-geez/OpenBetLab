"""Build the clean match table and the data-quality report.

    python -m openbetlab.data.build [--as-of YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import datetime as dt
import json
from pathlib import Path

from .cleaning import Match, clean
from .quality_report import render
from .team_names import TeamNameMapper

ROOT = Path(__file__).resolve().parents[2]


def write_csv(matches: list[Match], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [f.name for f in dataclasses.fields(Match)]
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for m in matches:
            w.writerow(dataclasses.asdict(m))  # None -> empty cell


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--raw-dir", type=Path, default=ROOT / "data/raw/football.json")
    p.add_argument("--names-dir", type=Path, default=ROOT / "data/team_names")
    p.add_argument("--out-csv", type=Path, default=ROOT / "data/clean/matches.csv")
    p.add_argument("--report", type=Path, default=ROOT / "docs/data_quality_report.md")
    p.add_argument("--as-of", type=dt.date.fromisoformat, default=dt.date.today())
    a = p.parse_args(argv)

    manifest_path = a.raw_dir / "manifest.json"
    source = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    leagues = set(source["leagues"]) if source.get("leagues") else None

    mapper = TeamNameMapper.from_csv_dir(a.names_dir)
    result = clean(a.raw_dir, mapper, a.as_of, leagues)
    write_csv(result.matches, a.out_csv)
    info = {"as_of": a.as_of.isoformat(), "source_commit": source.get("commit"),
            "leagues": source.get("leagues"), "clean_matches": len(result.matches)}
    (a.out_csv.parent / "build_info.json").write_text(json.dumps(info, indent=2) + "\n")
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(render(result, as_of=a.as_of, source=source), encoding="utf-8")
    print(f"{len(result.matches)} clean matches -> {a.out_csv}\nreport -> {a.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
