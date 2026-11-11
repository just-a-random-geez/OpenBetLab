"""Markdown data-quality report for a CleanResult."""

from __future__ import annotations

import datetime as dt
from collections import Counter, defaultdict

from .cleaning import (ABANDONED, AWARDED, CANCELLED, PLAYED, POSTPONED, RESULT_MISSING,
                       SCHEDULED, CleanResult)
from .team_names import find_suspected_variants


def _table(headers: list[str], rows: list[list]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join("" if v is None else str(v) for v in r) + " |" for r in rows]
    return "\n".join(out)


def missing_value_counts(result: CleanResult) -> dict[tuple, Counter]:
    """(league, season) -> counts of each kind of missing value."""
    counts: dict[tuple, Counter] = defaultdict(Counter)
    for m in result.matches:
        c = counts[(m.league, m.season)]
        c["date"] += m.date is None
        c["time"] += m.time is None
        c["round"] += m.round is None
        if m.status in (PLAYED, AWARDED):
            c["ht_score"] += m.ht_home is None
        c["result_missing"] += m.status == RESULT_MISSING
    return counts


def render(result: CleanResult, *, as_of: dt.date, source: dict | None = None) -> str:
    source = source or {}
    keys = sorted(set(result.raw_counts) | {(m.league, m.season) for m in result.matches})
    status_counts: dict[tuple, Counter] = defaultdict(Counter)
    teams: dict[tuple, set] = defaultdict(set)
    for m in result.matches:
        status_counts[(m.league, m.season)][m.status] += 1
        teams[(m.league, m.season)].update((m.home_team, m.away_team))
    missing = missing_value_counts(result)

    tot = Counter()
    rows = []
    for k in keys:
        s = status_counts[k]
        row = [k[0], k[1], result.raw_counts[k], result.duplicates_removed[k],
               result.conflicts_excluded[k], result.rejected[k], sum(s.values()),
               s[PLAYED], s[AWARDED], s[CANCELLED] + s[POSTPONED] + s[ABANDONED],
               s[SCHEDULED], s[RESULT_MISSING], len(teams[k])]
        rows.append(row)
        for i, name in enumerate(["raw", "dup", "conf", "rej", "clean", "played", "awarded",
                                  "void", "sched", "missing"], start=2):
            tot[name] += row[i]

    lines = [
        "# Data Quality Report",
        "",
        f"- Generated: {dt.date.today().isoformat()}",
        f"- As-of date (decides *scheduled* vs *result missing*): {as_of.isoformat()}",
    ]
    if source:
        lines += [f"- Source: {source.get('repo', '')} @ `{source.get('commit', '')}`",
                  f"- Leagues: {', '.join(source.get('leagues', []))}"]
    lines += [
        "",
        "## Summary",
        "",
        f"- Rows read: **{tot['raw']}**",
        f"- Exact duplicates removed: **{tot['dup']}**",
        f"- Conflicting duplicates excluded: **{tot['conf']}**",
        f"- Rows rejected (no team name): **{tot['rej']}**",
        f"- Clean matches: **{tot['clean']}** "
        f"(played {tot['played']}, awarded {tot['awarded']}, cancelled/postponed/abandoned "
        f"{tot['void']}, scheduled {tot['sched']}, **result missing {tot['missing']}**)",
        f"- Team spellings merged: **{len({r for r, _ in result.renamed})}** raw names "
        f"-> {len({c for _, c in result.renamed})} canonical names",
        f"- Unknown team names (not in mapping): **{len(result.unknown_teams)}**",
        "",
        "Status meanings: *played* = full-time score present; *awarded* = result given "
        "off the pitch (official score kept); *void* = cancelled/postponed/abandoned (no "
        "score, none invented); *scheduled* = no score and date after the as-of date; "
        "*result missing* = date already passed but the source has no score.",
        "",
        "## Matches per league / season",
        "",
        _table(["League", "Season", "Raw", "Dup removed", "Conflicts", "Rejected", "Clean",
                "Played", "Awarded", "Void", "Scheduled", "Result missing", "Teams"], rows),
        "",
        "## Missing values",
        "",
        "Counted on clean matches. Nothing is filled in; missing stays empty in the output.",
        "",
    ]
    mrows = [[k[0], k[1], missing[k]["result_missing"], missing[k]["ht_score"],
              missing[k]["time"], missing[k]["date"], missing[k]["round"]]
             for k in keys if any(missing[k].values())]
    lines.append(_table(["League", "Season", "Result missing", "HT score missing (played)",
                         "Kick-off time missing", "Date missing", "Round missing"], mrows)
                 if mrows else "None.")

    gone = [m for m in result.matches if m.status == RESULT_MISSING]
    if gone:
        lines += ["", f"<details><summary>{len(gone)} matches whose result is missing</summary>",
                  "", _table(["League", "Season", "Date", "Home", "Away"],
                             [[m.league, m.season, m.date, m.home_team, m.away_team]
                              for m in gone]), "", "</details>"]

    lines += ["", "## Coverage gaps", ""]
    gaps = source.get("missing_files", [])
    lines.append("Files not present upstream (league/season not available):\n\n"
                 + "\n".join(f"- `{g}`" for g in gaps) if gaps else "None recorded.")

    lines += ["", "## Data issues", ""]
    by_kind = Counter(i.kind for i in result.issues)
    if by_kind:
        lines.append(_table(["Issue", "Count"], sorted(by_kind.items())))
        lines += ["", "<details><summary>All issues</summary>", ""]
        lines += ["Issue kinds: `date_outside_season` = date outside the season's normal "
                  "window (kept as published, likely an upstream typo); `invalid_*` = value "
                  "unreadable, stored as empty; `conflicting_duplicate` = same fixture listed "
                  "with different data, all copies excluded.", ""]
        lines += [f"- {i.league} {i.season} `{i.kind}`: {i.detail}" for i in result.issues]
        lines += ["", "</details>"]
    else:
        lines.append("None.")

    lines += ["", "## Team names", ""]
    lines.append(_table(["Raw name", "Canonical name", "Rows"],
                        [[r, c, n] for (r, c), n in sorted(result.renamed.items())])
                 if result.renamed else "No renames applied.")
    lines += ["", "Unknown names (add to `data/team_names/`): "
              + (", ".join(sorted(result.unknown_teams)) or "none")]
    canon = {m.home_team for m in result.matches} | {m.away_team for m in result.matches}
    suspects = find_suspected_variants(canon)
    lines += ["", "Suspected variants still present after mapping: "
              + ("; ".join(" / ".join(g) for g in suspects) if suspects else "none")]
    return "\n".join(lines) + "\n"
