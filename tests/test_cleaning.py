import datetime as dt

from conftest import m

from openbetlab.data import cleaning as C
from openbetlab.data.cleaning import clean

AS_OF = dt.date(2021, 1, 1)


def run(raw, mapper, as_of=AS_OF):
    return clean(raw, mapper, as_of)


def one(result):
    assert len(result.matches) == 1
    return result.matches[0]


def test_dict_score_and_team_mapping(write_raw, mapper):
    r = run(write_raw("2020-21", "en.1", [m(score={"ht": [1, 0], "ft": [2, 1]})]), mapper)
    x = one(r)
    assert (x.home_team, x.away_team) == ("Stoke City FC", "Hull City AFC")
    assert (x.home_team_raw, x.away_team_raw) == ("Stoke City", "Hull City")
    assert (x.ft_home, x.ft_away, x.ht_home, x.ht_away) == (2, 1, 1, 0)
    assert x.status == C.PLAYED
    assert r.renamed[("Stoke City", "Stoke City FC")] == 1


def test_list_score_is_full_time(write_raw, mapper):
    x = one(run(write_raw("2020-21", "en.1", [m(score=[3, 0])]), mapper))
    assert (x.ft_home, x.ft_away, x.ht_home) == (3, 0, None)


def test_extra_time_and_penalties(write_raw, mapper):
    s = {"ft": [1, 1], "et": [1, 1], "p": [5, 6]}
    x = one(run(write_raw("2020-21", "en.2", [m(score=s)]), mapper))
    assert (x.et_home, x.et_away, x.pen_home, x.pen_away) == (1, 1, 5, 6)


def test_missing_ht_is_left_empty_not_invented(write_raw, mapper):
    x = one(run(write_raw("2020-21", "en.1", [m(score={"ft": [0, 0]})]), mapper))
    assert x.ht_home is None and x.ht_away is None


def test_no_score_past_date_is_result_missing(write_raw, mapper):
    x = one(run(write_raw("2020-21", "en.1", [m(date="2020-12-01")]), mapper))
    assert x.status == C.RESULT_MISSING and x.ft_home is None


def test_no_score_future_date_is_scheduled(write_raw, mapper):
    x = one(run(write_raw("2020-21", "en.1", [m(date="2021-03-01", score=None)]), mapper))
    assert x.status == C.SCHEDULED and x.ft_home is None


def test_source_statuses(write_raw, mapper):
    raw = write_raw("2019-20", "en.3", [
        m(date="2020-03-14", score={}, status="cancelled"),
        m(date="2020-03-15", status="canceled"),
        m(date="2020-03-16", score={}, status="postponed"),
        m(date="2020-03-17", status="abandoned"),
        m(date="2020-03-18", score={"ft": [0, 3]}, status="awarded"),
    ])
    r = run(raw, mapper)
    assert [x.status for x in r.matches] == [C.CANCELLED, C.CANCELLED, C.POSTPONED,
                                             C.ABANDONED, C.AWARDED]
    assert [x.ft_home for x in r.matches] == [None, None, None, None, 0]


def test_invalid_values_become_missing_and_are_reported(write_raw, mapper):
    raw = write_raw("2020-21", "en.1", [
        m(date="2020-13-45", time="25:99", score={"ft": [-1, "two"]}),
    ])
    r = run(raw, mapper)
    x = one(r)
    assert (x.date, x.time, x.ft_home, x.ft_away) == (None, None, None, None)
    assert {i.kind for i in r.issues} == {"invalid_date", "invalid_time", "invalid_score"}


def test_row_without_team_is_rejected(write_raw, mapper):
    r = run(write_raw("2020-21", "en.1", [m(team2=None, score=[1, 0])]), mapper)
    assert r.matches == []
    assert r.rejected[("en.1", "2020-21")] == 1
    assert r.issues[0].kind == "missing_team"


def test_exact_duplicate_removed_once(write_raw, mapper):
    r = run(write_raw("2020-21", "en.4", [m(score=[1, 1]), m(score=[1, 1]), m(score=[1, 1])]),
            mapper)
    one(r)
    assert r.duplicates_removed[("en.4", "2020-21")] == 2


def test_duplicate_written_with_different_spelling_is_still_duplicate(write_raw, mapper):
    r = run(write_raw("2020-21", "en.1", [m(score=[1, 1]),
                                          m(team1="Stoke City FC", score=[1, 1])]), mapper)
    one(r)
    assert r.duplicates_removed[("en.1", "2020-21")] == 1


def test_conflicting_duplicate_excluded_and_reported(write_raw, mapper):
    r = run(write_raw("2020-21", "en.1", [m(score=[1, 0]), m(score=[0, 1])]), mapper)
    assert r.matches == []
    assert r.conflicts_excluded[("en.1", "2020-21")] == 2
    assert any(i.kind == "conflicting_duplicate" for i in r.issues)


def test_playoff_rematch_on_other_date_is_kept(write_raw, mapper):
    r = run(write_raw("2020-21", "en.2", [m(date="2020-10-01", score=[1, 0]),
                                          m(date="2021-05-15", score=[2, 2], round="Semifinals")]),
            mapper, as_of=dt.date(2021, 6, 1))
    assert len(r.matches) == 2 and sum(r.duplicates_removed.values()) == 0


def test_only_league_files_are_read(write_raw, mapper):
    write_raw("2020-21", "en.1", [m(score=[1, 0])])
    raw = write_raw("2020-21", "en.1", [m(score=[1, 0])], filename="en.1-full.json")
    r = run(raw, mapper)
    one(r)
    assert sum(r.duplicates_removed.values()) == 0


def test_unknown_team_reported(write_raw, mapper):
    r = run(write_raw("2020-21", "en.1", [m(team1="Mystery Town", score=[1, 0])]), mapper)
    assert r.unknown_teams == {"Mystery Town"}


def test_season_window():
    assert C.season_window("2019-20") == (dt.date(2019, 7, 1), dt.date(2020, 8, 31))
    assert C.season_window("2025") == (dt.date(2025, 1, 1), dt.date(2025, 12, 31))
    assert C.season_window("weird") is None


def test_date_outside_season_is_flagged_not_changed(write_raw, mapper):
    r = run(write_raw("2025-26", "en.3", [m(date="2025-03-01", score=None)]), mapper,
            as_of=dt.date(2026, 11, 11))
    x = one(r)
    assert x.date == "2025-03-01"
    assert [i.kind for i in r.issues] == ["date_outside_season"]
