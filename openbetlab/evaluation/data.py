"""Load clean matches for evaluation and split them by time."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import datetime as dt

from openbetlab.data.cleaning import PLAYED, SCHEDULED, season_window


@dataclass(frozen=True)
class Result:
    league: str
    season: str
    date: str
    home_team: str
    away_team: str
    outcome: str  # "H", "D", "A"
    home_goals: int | None = None
    away_goals: int | None = None


def outcome(ft_home: int, ft_away: int) -> str:
    return "H" if ft_home > ft_away else "A" if ft_home < ft_away else "D"


def season_sort_key(season: str) -> tuple[int, str]:
    return int(season[:4]), season


def load_matches_csv(path: Path) -> list[dict]:
    with Path(path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def date_is_trustworthy(row: dict) -> bool:
    """Date present and inside the season's normal window.

    Matches with an out-of-season date (upstream typo) can't be placed in time, so a
    model could see them "before" matches they actually came after. They are excluded.
    """
    if not row["date"]:
        return False
    window = season_window(row["season"])
    return window is None or window[0] <= dt.date.fromisoformat(row["date"]) <= window[1]


def results_from_rows(rows: list[dict], skipped: dict | None = None) -> list[Result]:
    """Matches usable for evaluation: status 'played', full-time score, trustworthy date.

    Awarded matches (decided off the pitch), anything without a score and matches
    with an untrustworthy date are left out (counted in ``skipped`` if given).
    Sorted by season, then date - never shuffled.
    """
    out = []
    for r in rows:
        if r["status"] != PLAYED or r["ft_home"] == "" or r["ft_away"] == "":
            continue
        if not date_is_trustworthy(r):
            if skipped is not None:
                skipped["bad_date"] = skipped.get("bad_date", 0) + 1
            continue
        gh, ga = int(r["ft_home"]), int(r["ft_away"])
        out.append(Result(r["league"], r["season"], r["date"], r["home_team"],
                          r["away_team"], outcome(gh, ga), gh, ga))
    out.sort(key=lambda m: (season_sort_key(m.season), m.date, m.league, m.home_team))
    return out


def latest_complete_season(rows: list[dict]) -> str:
    """Most recent season with no matches still to be played ('scheduled').

    A season that is still in progress is not a fair test set, so it is skipped.
    """
    seasons = {r["season"] for r in rows}
    in_progress = {r["season"] for r in rows if r["status"] == SCHEDULED}
    done = sorted(seasons - in_progress, key=season_sort_key)
    if not done:
        raise ValueError("no completed season available")
    return done[-1]


@dataclass
class TimeSplit:
    train: list[Result]
    test: list[Result]
    holdout_season: str
    excluded_later: int  # matches from seasons after the holdout (not used at all)


def time_split(results: list[Result], holdout_season: str) -> TimeSplit:
    """Train = every season strictly before the holdout; test = the holdout season.

    Later seasons are dropped so the future can never leak into training.
    """
    hk = season_sort_key(holdout_season)
    train = [m for m in results if season_sort_key(m.season) < hk]
    test = [m for m in results if m.season == holdout_season]
    later = sum(season_sort_key(m.season) > hk for m in results)
    if not test:
        raise ValueError(f"no played matches in holdout season {holdout_season}")
    if not train:
        raise ValueError(f"no seasons before {holdout_season} to train on")
    return TimeSplit(train, test, holdout_season, later)
