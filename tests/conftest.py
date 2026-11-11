import json
from pathlib import Path

import pytest

from openbetlab.data.team_names import TeamNameMapper


@pytest.fixture
def mapper():
    return TeamNameMapper({
        "Stoke City": "Stoke City FC", "Stoke City FC": "Stoke City FC",
        "Hull City": "Hull City AFC", "Hull City AFC": "Hull City AFC",
        "Arsenal FC": "Arsenal FC",
    })


@pytest.fixture
def write_raw(tmp_path):
    """write_raw("2020-21", "en.1", [matches...]) -> raw dir."""
    raw = tmp_path / "raw"

    def _write(season, league, matches, filename=None):
        path = raw / season / (filename or f"{league}.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"name": "test", "matches": matches}))
        return raw
    return _write


def m(team1="Stoke City", team2="Hull City", date="2020-09-12", score=None, **kw):
    d = {"round": "Matchday 1", "date": date, "time": "15:00", "team1": team1, "team2": team2}
    if score is not None:
        d["score"] = score
    d.update(kw)
    return d
