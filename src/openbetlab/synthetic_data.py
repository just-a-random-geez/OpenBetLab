"""Load the bundled SYNTHETIC football match data.

The data ships inside the package (``openbetlab/data/synthetic_matches.csv``),
so loading it never touches the internet. Every row is invented. See
``openbetlab/data/README.md``.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from importlib import resources

from openbetlab.odds import validate_decimal_odds

DATA_FILE_NAME = "synthetic_matches.csv"


@dataclass(frozen=True)
class SyntheticMatch:
    """One invented match.

    ``is_synthetic`` is always ``True`` and cannot be set by the caller, so the
    synthetic label cannot be switched off by accident.
    """

    match_id: str
    date: str
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int
    odds_home: float
    odds_draw: float
    odds_away: float
    is_synthetic: bool = field(default=True, init=False)

    @property
    def result(self) -> str:
        """``"H"`` for a home win, ``"D"`` for a draw, ``"A"`` for an away win."""
        if self.home_goals > self.away_goals:
            return "H"
        if self.home_goals < self.away_goals:
            return "A"
        return "D"


def _parse_goals(raw: str, column: str, match_id: str) -> int:
    goals = int(raw)
    if goals < 0:
        raise ValueError(f"{match_id}: {column} must not be negative, got {goals}")
    return goals


def load_synthetic_matches() -> list[SyntheticMatch]:
    """Read and validate every row of the bundled synthetic data file.

    Lines starting with ``#`` are comments (the "this is synthetic" warning)
    and are skipped.
    """
    text = (
        resources.files("openbetlab")
        .joinpath("data", DATA_FILE_NAME)
        .read_text(encoding="utf-8")
    )
    lines = [line for line in text.splitlines() if not line.startswith("#")]
    matches = []
    for row in csv.DictReader(lines):
        match_id = row["match_id"]
        matches.append(
            SyntheticMatch(
                match_id=match_id,
                date=row["date"],
                home_team=row["home_team"],
                away_team=row["away_team"],
                home_goals=_parse_goals(row["home_goals"], "home_goals", match_id),
                away_goals=_parse_goals(row["away_goals"], "away_goals", match_id),
                odds_home=validate_decimal_odds(float(row["odds_home"]), "odds_home"),
                odds_draw=validate_decimal_odds(float(row["odds_draw"]), "odds_draw"),
                odds_away=validate_decimal_odds(float(row["odds_away"]), "odds_away"),
            )
        )
    return matches
