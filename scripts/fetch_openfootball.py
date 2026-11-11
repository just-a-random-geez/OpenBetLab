"""Download league files from openfootball/football.json at a pinned commit.

    python scripts/fetch_openfootball.py

Writes data/raw/football.json/<season>/<league>.json plus manifest.json
(commit, leagues, files fetched, files not available upstream).
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

REPO = "openfootball/football.json"
COMMIT = "e6744429ee395bc86f247348c6184bb08d4eb361"  # licence checked 2026-11-11 (CC0-1.0)
LEAGUES = ["en.1", "en.2", "en.3", "en.4"]
SEASONS = [f"{y}-{str(y + 1)[2:]}" for y in range(2010, 2027)]  # 2010-11 .. 2026-27
OUT = Path(__file__).resolve().parents[1] / "data/raw/football.json"


def main() -> int:
    fetched, missing = [], []
    for season in SEASONS:
        for league in LEAGUES:
            rel = f"{season}/{league}.json"
            url = f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/{rel}"
            try:
                with urllib.request.urlopen(url, timeout=30) as r:
                    body = r.read()
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    missing.append(rel)
                    continue
                raise
            json.loads(body)  # fail fast on corrupt downloads
            dest = OUT / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(body)
            fetched.append(rel)
    manifest = {"repo": f"https://github.com/{REPO}", "commit": COMMIT, "licence": "CC0-1.0",
                "leagues": LEAGUES, "fetched_files": fetched, "missing_files": missing}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"fetched {len(fetched)}, not available {len(missing)} -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
