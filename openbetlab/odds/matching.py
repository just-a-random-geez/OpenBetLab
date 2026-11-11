"""Match Betfair markets to openfootball matches.

1. Exact: both Betfair names are in the mapping file (data/team_names/betfair/*.csv,
   columns raw_name,canonical_name) and a match between those canonical teams exists
   on the same UK date (Betfair times are UTC, openfootball dates are UK local).
2. Fuzzy (fallback): among openfootball matches on that UK date, pick the one whose
   home AND away names are most similar to the Betfair names. Accepted only if both
   similarities reach ``min_score`` and the winner is clearly ahead of the runner-up.
   Every fuzzy match is reported so it can be checked and added to the mapping file.
3. Otherwise: unmatched (reported, never guessed).
Home/away must agree: a Betfair "A v B" is never matched to openfootball "B v A".
"""

from __future__ import annotations

import csv
import datetime as dt
import difflib
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo

UK = ZoneInfo("Europe/London")

# Common abbreviations in Betfair names -> full words (used only for fuzzy similarity).
_ABBREV = {"utd": "united", "man": "manchester", "nottm": "nottingham", "sheff": "sheffield",
           "wed": "wednesday", "co": "county", "brom": "bromwich", "qpr": "queens park rangers",
           "mk": "milton keynes", "wolves": "wolverhampton wanderers", "dag": "dagenham",
           "red": "redbridge", "spurs": "tottenham hotspur"}
_DROP = {"fc", "afc", "the", "and", "&"}


def normalise(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    tokens = re.sub(r"[^a-z0-9 ]", " ", s).split()
    out = []
    for t in tokens:
        if t in _DROP:
            continue
        out.extend(_ABBREV.get(t, t).split())
    return " ".join(out)


def similarity(a: str, b: str) -> float:
    """0-1 similarity of two team names after normalisation.

    Max of:
    - 0.9 x character similarity of the normalised names;
    - containment: share of the SHORTER name's words found in the longer one, where a
      word also counts if one is a prefix (>= 4 letters) of the other
      ("Brighton" ~ "Brighton & Hove Albion", "Wolves" ~ "Wolverhampton Wanderers").
    """
    na, nb = normalise(a), normalise(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    char = difflib.SequenceMatcher(None, na, nb).ratio()
    short, long_ = sorted((na.split(), nb.split()), key=len)

    def shared(x):
        return any(x == y or (min(len(x), len(y)) >= 4 and (x.startswith(y) or y.startswith(x)))
                   for y in long_)
    contained = sum(map(shared, short)) / len(short)
    # Character similarity is discounted: "Man Utd" vs "Manchester City" look alike as text.
    return max(0.9 * char, contained)


def load_mapping(directory: Path, pattern: str = "*.csv") -> dict[str, str]:
    mapping: dict[str, str] = {}
    for path in sorted(Path(directory).glob(pattern)):
        with path.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                raw, canon = row["raw_name"].strip(), row["canonical_name"].strip()
                if raw in mapping and mapping[raw] != canon:
                    raise ValueError(f"{path.name}: '{raw}' mapped to two names")
                mapping[raw] = canon
    return mapping


@dataclass(frozen=True)
class FixtureRef:
    league: str
    season: str
    date: str
    home_team: str
    away_team: str
    ft_home: int | None = None
    ft_away: int | None = None

    def outcome(self) -> str | None:
        if self.ft_home is None or self.ft_away is None:
            return None
        return ("home" if self.ft_home > self.ft_away else
                "away" if self.ft_home < self.ft_away else "draw")


@dataclass
class MatchResult:
    fixture: FixtureRef | None
    method: str              # "mapping", "fuzzy" or "unmatched"
    score: float | None = None
    reason: str = ""


def uk_date(kickoff_utc: dt.datetime) -> str:
    return kickoff_utc.astimezone(UK).date().isoformat()


class Matcher:
    def __init__(self, fixtures: list[FixtureRef], mapping: dict[str, str],
                 min_score: float = 0.6, margin: float = 0.1):
        self.mapping = mapping
        self.min_score = min_score
        self.margin = margin
        self.by_date: dict[str, list[FixtureRef]] = defaultdict(list)
        for f in fixtures:
            self.by_date[f.date].append(f)

    def match(self, home_name: str, away_name: str, kickoff_utc: dt.datetime) -> MatchResult:
        day = uk_date(kickoff_utc)
        candidates = self.by_date.get(day, [])
        if not candidates:
            return MatchResult(None, "unmatched", reason=f"no openfootball match on {day}")

        h, a = self.mapping.get(home_name), self.mapping.get(away_name)
        if h and a:
            hits = [f for f in candidates if f.home_team == h and f.away_team == a]
            if len(hits) == 1:
                return MatchResult(hits[0], "mapping", 1.0)
            if [f for f in candidates if f.home_team == a and f.away_team == h]:
                return MatchResult(None, "unmatched", reason="home/away reversed vs openfootball")

        scored = sorted(((min(similarity(home_name, f.home_team),
                              similarity(away_name, f.away_team)), f) for f in candidates),
                        key=lambda x: -x[0])
        best_score, best = scored[0]
        runner_up = scored[1][0] if len(scored) > 1 else 0.0
        if best_score < self.min_score:
            return MatchResult(None, "unmatched", best_score,
                               f"best candidate {best.home_team} v {best.away_team} "
                               f"only {best_score:.2f}")
        if best_score - runner_up < self.margin:
            return MatchResult(None, "unmatched", best_score, "ambiguous: two similar candidates")
        return MatchResult(best, "fuzzy", best_score)
