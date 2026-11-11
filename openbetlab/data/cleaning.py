"""Turn raw openfootball/football.json files into one clean match table.

Rules (see docs/PHASE1_DATA_CLEANING.md):
- Team names go through TeamNameMapper.
- Missing values stay missing (None). They are counted, never filled in.
- Every match gets a ``status`` explaining why a score is or isn't there.
- Exact duplicates are removed; conflicting duplicates are excluded and listed.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .team_names import TeamNameMapper

LEAGUE_FILE_RE = re.compile(r"^[a-z]+\.\d+\.json$")  # en.1.json, not en.1-full.json

# Match statuses
PLAYED = "played"
AWARDED = "awarded"            # result decided off the pitch; score is official
CANCELLED = "cancelled"
POSTPONED = "postponed"
ABANDONED = "abandoned"
SCHEDULED = "scheduled"        # no result yet, date is after the as-of date
RESULT_MISSING = "result_missing"  # date has passed but the source has no result
STATUSES = [PLAYED, AWARDED, CANCELLED, POSTPONED, ABANDONED, SCHEDULED, RESULT_MISSING]

_STATUS_ALIASES = {"canceled": CANCELLED, "cancelled": CANCELLED, "postponed": POSTPONED,
                   "abandoned": ABANDONED, "awarded": AWARDED}


@dataclass
class Match:
    league: str
    season: str
    source_file: str
    round: str | None
    date: str | None
    time: str | None
    home_team: str
    away_team: str
    home_team_raw: str
    away_team_raw: str
    status: str
    ft_home: int | None = None
    ft_away: int | None = None
    ht_home: int | None = None
    ht_away: int | None = None
    et_home: int | None = None
    et_away: int | None = None
    pen_home: int | None = None
    pen_away: int | None = None
    # "" = date looks fine; otherwise why it can't be trusted (kept as published, flagged)
    date_flag: str = ""

    def key(self) -> tuple:
        return (self.league, self.season, self.date, self.home_team, self.away_team)

    def content(self) -> tuple:
        d = asdict(self)
        d.pop("date_flag")
        for k in ("source_file", "home_team_raw", "away_team_raw"):
            d.pop(k)
        return tuple(d.items())


@dataclass
class Issue:
    league: str
    season: str
    kind: str
    detail: str


@dataclass
class CleanResult:
    matches: list[Match]
    issues: list[Issue] = field(default_factory=list)
    raw_counts: Counter = field(default_factory=Counter)        # (league, season) -> rows read
    duplicates_removed: Counter = field(default_factory=Counter)
    conflicts_excluded: Counter = field(default_factory=Counter)
    rejected: Counter = field(default_factory=Counter)          # rows unusable (no team)
    renamed: Counter = field(default_factory=Counter)           # (raw, canonical) -> count
    unknown_teams: set[str] = field(default_factory=set)


def _pair(value, issues: list[Issue], league: str, season: str, what: str):
    """Validate a [home, away] score pair. Invalid -> (None, None) + issue."""
    if value is None:
        return None, None
    if (isinstance(value, list) and len(value) == 2
            and all(isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in value)):
        return value[0], value[1]
    issues.append(Issue(league, season, "invalid_score", f"{what}={value!r}"))
    return None, None


def _valid_date(value, issues, league, season, where) -> str | None:
    if value is None:
        return None
    try:
        dt.date.fromisoformat(value)
        return value
    except (TypeError, ValueError):
        issues.append(Issue(league, season, "invalid_date", f"{where}: {value!r}"))
        return None


def _valid_time(value, issues, league, season, where) -> str | None:
    if value is None:
        return None
    if isinstance(value, str) and re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", value):
        return value
    issues.append(Issue(league, season, "invalid_time", f"{where}: {value!r}"))
    return None


def season_window(season: str) -> tuple[dt.date, dt.date] | None:
    """Plausible date range for a season folder name.

    "2019-20" -> 1 Jul 2019 .. 31 Aug 2020 (Aug covers the COVID-delayed 2019-20 finish).
    "2025"    -> calendar year.
    """
    if re.fullmatch(r"\d{4}-\d{2}", season):
        start = int(season[:4])
        return dt.date(start, 7, 1), dt.date(start + 1, 8, 31)
    if re.fullmatch(r"\d{4}", season):
        return dt.date(int(season), 1, 1), dt.date(int(season), 12, 31)
    return None


def parse_match(raw: dict, league: str, season: str, source_file: str,
                mapper: TeamNameMapper, as_of: dt.date, issues: list[Issue]) -> Match | None:
    t1, t2 = raw.get("team1"), raw.get("team2")
    if not t1 or not t2:
        issues.append(Issue(league, season, "missing_team", f"{source_file}: {raw!r}"))
        return None
    where = f"{t1} v {t2}"
    date = _valid_date(raw.get("date"), issues, league, season, where)
    window = season_window(season)
    if date is not None and window and not window[0] <= dt.date.fromisoformat(date) <= window[1]:
        # Kept as published (we don't guess the right date) but flagged.
        issues.append(Issue(league, season, "date_outside_season", f"{date} {where}"))
        date_flag = "outside_season"
    else:
        date_flag = ""
    time = _valid_time(raw.get("time"), issues, league, season, where)

    score = raw.get("score")
    ft = ht = et = pen = None
    if isinstance(score, list):            # newer files: bare [home, away] = full time
        ft = score
    elif isinstance(score, dict):
        ft, ht, et, pen = score.get("ft"), score.get("ht"), score.get("et"), score.get("p")
    elif score is not None:
        issues.append(Issue(league, season, "invalid_score", f"{where}: score={score!r}"))

    ft_h, ft_a = _pair(ft, issues, league, season, f"{where} ft")
    ht_h, ht_a = _pair(ht, issues, league, season, f"{where} ht")
    et_h, et_a = _pair(et, issues, league, season, f"{where} et")
    p_h, p_a = _pair(pen, issues, league, season, f"{where} p")

    raw_status = raw.get("status")
    if raw_status is not None:
        status = _STATUS_ALIASES.get(str(raw_status).lower())
        if status is None:
            issues.append(Issue(league, season, "unknown_status", f"{where}: {raw_status!r}"))
            status = RESULT_MISSING if ft_h is None else PLAYED
        elif status == AWARDED and ft_h is None:
            issues.append(Issue(league, season, "awarded_without_score", where))
    elif ft_h is not None:
        status = PLAYED
    elif date is not None and dt.date.fromisoformat(date) > as_of:
        status = SCHEDULED
    else:
        status = RESULT_MISSING

    return Match(
        league=league, season=season, source_file=source_file,
        round=raw.get("round") or None, date=date, time=time,
        home_team=mapper.canonical(t1), away_team=mapper.canonical(t2),
        home_team_raw=t1, away_team_raw=t2, status=status,
        ft_home=ft_h, ft_away=ft_a, ht_home=ht_h, ht_away=ht_a,
        et_home=et_h, et_away=et_a, pen_home=p_h, pen_away=p_a, date_flag=date_flag,
    )


ROUND_GAP_DAYS = 180


def round_number(round_name: str | None) -> int | None:
    """'Matchday 14', 'Regular, Matchday 14', '14. Round' -> 14; play-off rounds -> None."""
    if not round_name:
        return None
    nums = re.findall(r"\d+", round_name)
    return int(nums[-1]) if nums else None


def flag_dates_inconsistent_with_round(matches: list[Match], issues: list[Issue]) -> int:
    """Flag matches dated far too EARLY for their matchday (e.g. a year typo inside the
    season window: 2019-20 restart games dated 2019-07 instead of 2020-07).

    For each league-season, a match in matchday N is flagged when its date is more than
    ROUND_GAP_DAYS before the median date of some earlier matchday M < N. Re-arranged
    games are played LATER, never half a season earlier, so these can only be wrong dates.
    """
    from statistics import median_low
    by_ls: dict[tuple, dict[int, list[Match]]] = defaultdict(lambda: defaultdict(list))
    for m in matches:
        n = round_number(m.round)
        if m.date and n is not None:
            by_ls[(m.league, m.season)][n].append(m)
    flagged = 0
    for (league, season), rounds in by_ls.items():
        medians = {n: dt.date.fromisoformat(median_low(sorted(x.date for x in ms)))
                   for n, ms in rounds.items()}
        latest_earlier = None
        for n in sorted(rounds):
            if latest_earlier is not None:
                for m in rounds[n]:
                    if (latest_earlier - dt.date.fromisoformat(m.date)).days > ROUND_GAP_DAYS \
                            and not m.date_flag:
                        m.date_flag = "inconsistent_with_round"
                        flagged += 1
                        issues.append(Issue(league, season, "date_inconsistent_with_round",
                                            f"{m.date} {m.home_team} v {m.away_team} "
                                            f"({m.round}; earlier matchdays ~{latest_earlier})"))
            latest_earlier = max(filter(None, [latest_earlier, medians[n]]))
    return flagged


def iter_league_files(raw_dir: Path, leagues: set[str] | None = None):
    """Yield (season, league, path) for domestic-league files in raw_dir/<season>/."""
    for path in sorted(Path(raw_dir).glob("*/*.json")):
        if not LEAGUE_FILE_RE.match(path.name):
            continue
        league = path.name[:-5]
        if leagues is None or league in leagues:
            yield path.parent.name, league, path


def clean(raw_dir: Path, mapper: TeamNameMapper, as_of: dt.date,
          leagues: set[str] | None = None) -> CleanResult:
    issues: list[Issue] = []
    result = CleanResult(matches=[], issues=issues)
    parsed: list[Match] = []

    for season, league, path in iter_league_files(raw_dir, leagues):
        data = json.loads(path.read_text(encoding="utf-8"))
        raw_matches = data.get("matches")
        if raw_matches is None:  # older nested format
            raw_matches = [m for r in data.get("rounds", []) for m in r.get("matches", [])]
        source = f"{season}/{path.name}"
        for raw in raw_matches:
            result.raw_counts[(league, season)] += 1
            m = parse_match(raw, league, season, source, mapper, as_of, issues)
            if m is None:
                result.rejected[(league, season)] += 1
                continue
            for r, c in ((m.home_team_raw, m.home_team), (m.away_team_raw, m.away_team)):
                if r != c:
                    result.renamed[(r, c)] += 1
            parsed.append(m)

    # Duplicates: same league, season, date, home, away.
    by_key: dict[tuple, list[Match]] = defaultdict(list)
    for m in parsed:
        by_key[m.key()].append(m)
    for key, group in by_key.items():
        league, season = key[0], key[1]
        distinct = {m.content() for m in group}
        if len(distinct) == 1:
            result.matches.append(group[0])
            result.duplicates_removed[(league, season)] += len(group) - 1
        else:
            result.conflicts_excluded[(league, season)] += len(group)
            issues.append(Issue(league, season, "conflicting_duplicate",
                                f"{key[2]} {key[3]} v {key[4]}: {len(group)} different versions"))

    flag_dates_inconsistent_with_round(result.matches, issues)
    result.matches.sort(key=lambda m: (m.league, m.season, m.date or "", m.home_team))
    result.unknown_teams = set(mapper.unknown)
    return result
