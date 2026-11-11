# Data Quality Report

- Generated: 2026-11-11
- As-of date (decides *scheduled* vs *result missing*): 2026-11-11
- Source: https://github.com/openfootball/football.json @ `e6744429ee395bc86f247348c6184bb08d4eb361`
- Leagues: en.1, en.2, en.3, en.4

## Summary

- Rows read: **26875**
- Exact duplicates removed: **12**
- Conflicting duplicates excluded: **0**
- Rows rejected (no team name): **0**
- Clean matches: **26863** (played 25385, awarded 1, cancelled/postponed/abandoned 220, scheduled 652, **result missing 605**)
- Team spellings merged: **39** raw names -> 39 canonical names
- Unknown team names (not in mapping): **0**

Status meanings: *played* = full-time score present; *awarded* = result given off the pitch (official score kept); *void* = cancelled/postponed/abandoned (no score, none invented); *scheduled* = no score and date after the as-of date; *result missing* = date already passed but the source has no score.

## Matches per league / season

| League | Season | Raw | Dup removed | Conflicts | Rejected | Clean | Played | Awarded | Void | Scheduled | Result missing | Teams |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| en.1 | 2010-11 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2011-12 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2012-13 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2013-14 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2014-15 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2015-16 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2016-17 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2017-18 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2018-19 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2019-20 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2020-21 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2021-22 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2022-23 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2023-24 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2024-25 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2025-26 | 380 | 0 | 0 | 0 | 380 | 380 | 0 | 0 | 0 | 0 | 20 |
| en.1 | 2026-27 | 380 | 0 | 0 | 0 | 380 | 50 | 0 | 0 | 280 | 50 | 20 |
| en.2 | 2010-11 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.2 | 2011-12 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.2 | 2012-13 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.2 | 2013-14 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.2 | 2014-15 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.2 | 2015-16 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.2 | 2018-19 | 552 | 0 | 0 | 0 | 552 | 551 | 1 | 0 | 0 | 0 | 24 |
| en.2 | 2019-20 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.2 | 2020-21 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.2 | 2021-22 | 557 | 0 | 0 | 0 | 557 | 557 | 0 | 0 | 0 | 0 | 24 |
| en.2 | 2022-23 | 557 | 0 | 0 | 0 | 557 | 557 | 0 | 0 | 0 | 0 | 24 |
| en.2 | 2023-24 | 557 | 0 | 0 | 0 | 557 | 557 | 0 | 0 | 0 | 0 | 24 |
| en.2 | 2024-25 | 557 | 0 | 0 | 0 | 557 | 557 | 0 | 0 | 0 | 0 | 24 |
| en.2 | 2025-26 | 557 | 0 | 0 | 0 | 557 | 557 | 0 | 0 | 0 | 0 | 24 |
| en.2 | 2026-27 | 552 | 0 | 0 | 0 | 552 | 95 | 0 | 0 | 372 | 85 | 24 |
| en.3 | 2010-11 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.3 | 2011-12 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.3 | 2012-13 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.3 | 2013-14 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.3 | 2014-15 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.3 | 2015-16 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.3 | 2018-19 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.3 | 2019-20 | 506 | 0 | 0 | 0 | 506 | 400 | 0 | 106 | 0 | 0 | 23 |
| en.3 | 2020-21 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.3 | 2024-25 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.3 | 2025-26 | 552 | 0 | 0 | 0 | 552 | 356 | 0 | 2 | 0 | 194 | 24 |
| en.4 | 2010-11 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.4 | 2011-12 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.4 | 2012-13 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.4 | 2013-14 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.4 | 2014-15 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.4 | 2015-16 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.4 | 2018-19 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.4 | 2019-20 | 552 | 0 | 0 | 0 | 552 | 440 | 0 | 112 | 0 | 0 | 24 |
| en.4 | 2020-21 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.4 | 2024-25 | 552 | 0 | 0 | 0 | 552 | 552 | 0 | 0 | 0 | 0 | 24 |
| en.4 | 2025-26 | 564 | 12 | 0 | 0 | 552 | 276 | 0 | 0 | 0 | 276 | 24 |

## Missing values

Counted on clean matches. Nothing is filled in; missing stays empty in the output.

| League | Season | Result missing | HT score missing (played) | Kick-off time missing | Date missing | Round missing |
|---|---|---|---|---|---|---|
| en.1 | 2010-11 | 0 | 25 | 0 | 0 | 0 |
| en.1 | 2011-12 | 0 | 27 | 0 | 0 | 0 |
| en.1 | 2012-13 | 0 | 35 | 0 | 0 | 0 |
| en.1 | 2013-14 | 0 | 27 | 0 | 0 | 0 |
| en.1 | 2014-15 | 0 | 31 | 0 | 0 | 0 |
| en.1 | 2015-16 | 0 | 32 | 0 | 0 | 0 |
| en.1 | 2016-17 | 0 | 27 | 0 | 0 | 0 |
| en.1 | 2017-18 | 0 | 32 | 0 | 0 | 0 |
| en.1 | 2018-19 | 0 | 22 | 0 | 0 | 0 |
| en.1 | 2019-20 | 0 | 21 | 0 | 0 | 0 |
| en.1 | 2020-21 | 0 | 30 | 0 | 0 | 0 |
| en.1 | 2021-22 | 0 | 22 | 0 | 0 | 0 |
| en.1 | 2022-23 | 0 | 23 | 0 | 0 | 0 |
| en.1 | 2023-24 | 0 | 11 | 0 | 0 | 0 |
| en.1 | 2024-25 | 0 | 16 | 0 | 0 | 0 |
| en.1 | 2025-26 | 0 | 27 | 0 | 0 | 0 |
| en.1 | 2026-27 | 50 | 5 | 0 | 0 | 0 |
| en.2 | 2010-11 | 0 | 40 | 0 | 0 | 0 |
| en.2 | 2011-12 | 0 | 41 | 0 | 0 | 0 |
| en.2 | 2012-13 | 0 | 37 | 0 | 0 | 0 |
| en.2 | 2013-14 | 0 | 40 | 0 | 0 | 0 |
| en.2 | 2014-15 | 0 | 46 | 0 | 0 | 0 |
| en.2 | 2015-16 | 0 | 57 | 0 | 0 | 0 |
| en.2 | 2018-19 | 0 | 40 | 0 | 0 | 0 |
| en.2 | 2019-20 | 0 | 32 | 0 | 0 | 0 |
| en.2 | 2020-21 | 0 | 53 | 0 | 0 | 0 |
| en.2 | 2021-22 | 0 | 44 | 0 | 0 | 5 |
| en.2 | 2022-23 | 0 | 49 | 0 | 0 | 5 |
| en.2 | 2023-24 | 0 | 37 | 0 | 0 | 0 |
| en.2 | 2024-25 | 0 | 44 | 0 | 0 | 0 |
| en.2 | 2025-26 | 0 | 37 | 0 | 0 | 0 |
| en.2 | 2026-27 | 85 | 7 | 264 | 0 | 0 |
| en.3 | 2010-11 | 0 | 32 | 0 | 0 | 0 |
| en.3 | 2011-12 | 0 | 45 | 0 | 0 | 0 |
| en.3 | 2012-13 | 0 | 38 | 0 | 0 | 0 |
| en.3 | 2013-14 | 0 | 39 | 0 | 0 | 0 |
| en.3 | 2014-15 | 0 | 36 | 0 | 0 | 0 |
| en.3 | 2015-16 | 0 | 44 | 0 | 0 | 0 |
| en.3 | 2018-19 | 0 | 46 | 0 | 0 | 0 |
| en.3 | 2019-20 | 0 | 36 | 106 | 0 | 0 |
| en.3 | 2020-21 | 0 | 38 | 0 | 0 | 0 |
| en.3 | 2024-25 | 0 | 46 | 0 | 0 | 0 |
| en.3 | 2025-26 | 194 | 95 | 2 | 0 | 0 |
| en.4 | 2010-11 | 0 | 48 | 0 | 0 | 0 |
| en.4 | 2011-12 | 0 | 35 | 0 | 0 | 0 |
| en.4 | 2012-13 | 0 | 49 | 0 | 0 | 0 |
| en.4 | 2013-14 | 0 | 56 | 0 | 0 | 0 |
| en.4 | 2014-15 | 0 | 43 | 0 | 0 | 0 |
| en.4 | 2015-16 | 0 | 40 | 0 | 0 | 0 |
| en.4 | 2018-19 | 0 | 43 | 0 | 0 | 0 |
| en.4 | 2019-20 | 0 | 36 | 112 | 0 | 0 |
| en.4 | 2020-21 | 0 | 57 | 0 | 0 | 0 |
| en.4 | 2024-25 | 0 | 48 | 0 | 0 | 0 |
| en.4 | 2025-26 | 276 | 15 | 0 | 0 | 0 |

<details><summary>605 matches whose result is missing</summary>

| League | Season | Date | Home | Away |
|---|---|---|---|---|
| en.1 | 2026-27 | 2026-10-10 | Arsenal FC | Leeds United FC |
| en.1 | 2026-27 | 2026-10-10 | Aston Villa FC | Brentford FC |
| en.1 | 2026-27 | 2026-10-10 | Chelsea FC | AFC Bournemouth |
| en.1 | 2026-27 | 2026-10-10 | Ipswich Town FC | Fulham FC |
| en.1 | 2026-27 | 2026-10-10 | Manchester United FC | Tottenham Hotspur FC |
| en.1 | 2026-27 | 2026-10-10 | Sunderland AFC | Brighton & Hove Albion FC |
| en.1 | 2026-27 | 2026-10-11 | Crystal Palace FC | Nottingham Forest FC |
| en.1 | 2026-27 | 2026-10-11 | Hull City AFC | Everton FC |
| en.1 | 2026-27 | 2026-10-11 | Liverpool FC | Manchester City FC |
| en.1 | 2026-27 | 2026-10-12 | Coventry City FC | Newcastle United FC |
| en.1 | 2026-27 | 2026-10-17 | Brentford FC | Liverpool FC |
| en.1 | 2026-27 | 2026-10-17 | Everton FC | Chelsea FC |
| en.1 | 2026-27 | 2026-10-17 | Fulham FC | Hull City AFC |
| en.1 | 2026-27 | 2026-10-17 | Manchester City FC | Ipswich Town FC |
| en.1 | 2026-27 | 2026-10-17 | Newcastle United FC | Aston Villa FC |
| en.1 | 2026-27 | 2026-10-18 | AFC Bournemouth | Sunderland AFC |
| en.1 | 2026-27 | 2026-10-18 | Brighton & Hove Albion FC | Crystal Palace FC |
| en.1 | 2026-27 | 2026-10-18 | Leeds United FC | Manchester United FC |
| en.1 | 2026-27 | 2026-10-18 | Nottingham Forest FC | Arsenal FC |
| en.1 | 2026-27 | 2026-10-19 | Tottenham Hotspur FC | Coventry City FC |
| en.1 | 2026-27 | 2026-10-23 | Ipswich Town FC | Nottingham Forest FC |
| en.1 | 2026-27 | 2026-10-24 | Arsenal FC | Everton FC |
| en.1 | 2026-27 | 2026-10-24 | Aston Villa FC | Manchester City FC |
| en.1 | 2026-27 | 2026-10-24 | Chelsea FC | Tottenham Hotspur FC |
| en.1 | 2026-27 | 2026-10-24 | Coventry City FC | Fulham FC |
| en.1 | 2026-27 | 2026-10-25 | Crystal Palace FC | Newcastle United FC |
| en.1 | 2026-27 | 2026-10-25 | Hull City AFC | Brentford FC |
| en.1 | 2026-27 | 2026-10-25 | Liverpool FC | Brighton & Hove Albion FC |
| en.1 | 2026-27 | 2026-10-25 | Manchester United FC | AFC Bournemouth |
| en.1 | 2026-27 | 2026-10-25 | Sunderland AFC | Leeds United FC |
| en.1 | 2026-27 | 2026-10-31 | AFC Bournemouth | Leeds United FC |
| en.1 | 2026-27 | 2026-10-31 | Aston Villa FC | Fulham FC |
| en.1 | 2026-27 | 2026-10-31 | Brentford FC | Nottingham Forest FC |
| en.1 | 2026-27 | 2026-10-31 | Chelsea FC | Manchester United FC |
| en.1 | 2026-27 | 2026-10-31 | Coventry City FC | Sunderland AFC |
| en.1 | 2026-27 | 2026-10-31 | Hull City AFC | Ipswich Town FC |
| en.1 | 2026-27 | 2026-10-31 | Manchester City FC | Brighton & Hove Albion FC |
| en.1 | 2026-27 | 2026-10-31 | Tottenham Hotspur FC | Crystal Palace FC |
| en.1 | 2026-27 | 2026-11-01 | Liverpool FC | Arsenal FC |
| en.1 | 2026-27 | 2026-11-02 | Newcastle United FC | Everton FC |
| en.1 | 2026-27 | 2026-11-07 | Arsenal FC | Hull City AFC |
| en.1 | 2026-27 | 2026-11-07 | Brighton & Hove Albion FC | Brentford FC |
| en.1 | 2026-27 | 2026-11-07 | Crystal Palace FC | Liverpool FC |
| en.1 | 2026-27 | 2026-11-07 | Everton FC | Coventry City FC |
| en.1 | 2026-27 | 2026-11-07 | Fulham FC | Newcastle United FC |
| en.1 | 2026-27 | 2026-11-07 | Ipswich Town FC | AFC Bournemouth |
| en.1 | 2026-27 | 2026-11-07 | Leeds United FC | Tottenham Hotspur FC |
| en.1 | 2026-27 | 2026-11-07 | Manchester United FC | Aston Villa FC |
| en.1 | 2026-27 | 2026-11-07 | Nottingham Forest FC | Manchester City FC |
| en.1 | 2026-27 | 2026-11-07 | Sunderland AFC | Chelsea FC |
| en.2 | 2026-27 | 2026-10-09 | West Ham United FC | Queens Park Rangers FC |
| en.2 | 2026-27 | 2026-10-10 | Blackburn Rovers FC | Cardiff City FC |
| en.2 | 2026-27 | 2026-10-10 | Bolton Wanderers FC | Stoke City FC |
| en.2 | 2026-27 | 2026-10-10 | Charlton Athletic FC | Bristol City FC |
| en.2 | 2026-27 | 2026-10-10 | Derby County FC | Wrexham AFC |
| en.2 | 2026-27 | 2026-10-10 | Middlesbrough FC | Wolverhampton Wanderers FC |
| en.2 | 2026-27 | 2026-10-10 | Preston North End FC | Millwall FC |
| en.2 | 2026-27 | 2026-10-10 | Sheffield United FC | Lincoln City FC |
| en.2 | 2026-27 | 2026-10-10 | Swansea City AFC | Norwich City FC |
| en.2 | 2026-27 | 2026-10-10 | Watford FC | Burnley FC |
| en.2 | 2026-27 | 2026-10-10 | West Bromwich Albion FC | Birmingham City FC |
| en.2 | 2026-27 | 2026-10-11 | Southampton FC | Portsmouth FC |
| en.2 | 2026-27 | 2026-10-13 | Birmingham City FC | Preston North End FC |
| en.2 | 2026-27 | 2026-10-13 | Bristol City FC | Blackburn Rovers FC |
| en.2 | 2026-27 | 2026-10-13 | Burnley FC | Charlton Athletic FC |
| en.2 | 2026-27 | 2026-10-13 | Cardiff City FC | Watford FC |
| en.2 | 2026-27 | 2026-10-13 | Millwall FC | Swansea City AFC |
| en.2 | 2026-27 | 2026-10-13 | Stoke City FC | Middlesbrough FC |
| en.2 | 2026-27 | 2026-10-13 | Wolverhampton Wanderers FC | Bolton Wanderers FC |
| en.2 | 2026-27 | 2026-10-13 | Wrexham AFC | West Bromwich Albion FC |
| en.2 | 2026-27 | 2026-10-14 | Lincoln City FC | West Ham United FC |
| en.2 | 2026-27 | 2026-10-14 | Norwich City FC | Southampton FC |
| en.2 | 2026-27 | 2026-10-14 | Portsmouth FC | Sheffield United FC |
| en.2 | 2026-27 | 2026-10-14 | Queens Park Rangers FC | Derby County FC |
| en.2 | 2026-27 | 2026-10-16 | Burnley FC | Wolverhampton Wanderers FC |
| en.2 | 2026-27 | 2026-10-17 | Birmingham City FC | Queens Park Rangers FC |
| en.2 | 2026-27 | 2026-10-17 | Bristol City FC | Sheffield United FC |
| en.2 | 2026-27 | 2026-10-17 | Derby County FC | Stoke City FC |
| en.2 | 2026-27 | 2026-10-17 | Middlesbrough FC | Cardiff City FC |
| en.2 | 2026-27 | 2026-10-17 | Millwall FC | Lincoln City FC |
| en.2 | 2026-27 | 2026-10-17 | Norwich City FC | Portsmouth FC |
| en.2 | 2026-27 | 2026-10-17 | Southampton FC | Bolton Wanderers FC |
| en.2 | 2026-27 | 2026-10-17 | Swansea City AFC | West Ham United FC |
| en.2 | 2026-27 | 2026-10-17 | Watford FC | Charlton Athletic FC |
| en.2 | 2026-27 | 2026-10-17 | West Bromwich Albion FC | Blackburn Rovers FC |
| en.2 | 2026-27 | 2026-10-17 | Wrexham AFC | Preston North End FC |
| en.2 | 2026-27 | 2026-10-20 | Wolverhampton Wanderers FC | Portsmouth FC |
| en.2 | 2026-27 | 2026-10-23 | Bolton Wanderers FC | Middlesbrough FC |
| en.2 | 2026-27 | 2026-10-24 | Blackburn Rovers FC | Wrexham AFC |
| en.2 | 2026-27 | 2026-10-24 | Cardiff City FC | Birmingham City FC |
| en.2 | 2026-27 | 2026-10-24 | Charlton Athletic FC | Norwich City FC |
| en.2 | 2026-27 | 2026-10-24 | Lincoln City FC | Burnley FC |
| en.2 | 2026-27 | 2026-10-24 | Portsmouth FC | Millwall FC |
| en.2 | 2026-27 | 2026-10-24 | Preston North End FC | West Bromwich Albion FC |
| en.2 | 2026-27 | 2026-10-24 | Queens Park Rangers FC | Swansea City AFC |
| en.2 | 2026-27 | 2026-10-24 | Sheffield United FC | Derby County FC |
| en.2 | 2026-27 | 2026-10-24 | Stoke City FC | Bristol City FC |
| en.2 | 2026-27 | 2026-10-24 | West Ham United FC | Southampton FC |
| en.2 | 2026-27 | 2026-10-24 | Wolverhampton Wanderers FC | Watford FC |
| en.2 | 2026-27 | 2026-10-30 | Sheffield United FC | Wrexham AFC |
| en.2 | 2026-27 | 2026-10-31 | Bolton Wanderers FC | Bristol City FC |
| en.2 | 2026-27 | 2026-10-31 | Burnley FC | Portsmouth FC |
| en.2 | 2026-27 | 2026-10-31 | Lincoln City FC | Birmingham City FC |
| en.2 | 2026-27 | 2026-10-31 | Middlesbrough FC | Charlton Athletic FC |
| en.2 | 2026-27 | 2026-10-31 | Millwall FC | Derby County FC |
| en.2 | 2026-27 | 2026-10-31 | Norwich City FC | Watford FC |
| en.2 | 2026-27 | 2026-10-31 | Southampton FC | Queens Park Rangers FC |
| en.2 | 2026-27 | 2026-10-31 | Stoke City FC | Preston North End FC |
| en.2 | 2026-27 | 2026-10-31 | Swansea City AFC | Blackburn Rovers FC |
| en.2 | 2026-27 | 2026-10-31 | West Ham United FC | West Bromwich Albion FC |
| en.2 | 2026-27 | 2026-10-31 | Wolverhampton Wanderers FC | Cardiff City FC |
| en.2 | 2026-27 | 2026-11-03 | Birmingham City FC | Millwall FC |
| en.2 | 2026-27 | 2026-11-03 | Blackburn Rovers FC | Stoke City FC |
| en.2 | 2026-27 | 2026-11-03 | Charlton Athletic FC | Bolton Wanderers FC |
| en.2 | 2026-27 | 2026-11-03 | Derby County FC | Norwich City FC |
| en.2 | 2026-27 | 2026-11-03 | Portsmouth FC | Swansea City AFC |
| en.2 | 2026-27 | 2026-11-03 | Preston North End FC | Sheffield United FC |
| en.2 | 2026-27 | 2026-11-03 | Queens Park Rangers FC | Burnley FC |
| en.2 | 2026-27 | 2026-11-03 | Watford FC | Lincoln City FC |
| en.2 | 2026-27 | 2026-11-03 | West Bromwich Albion FC | Southampton FC |
| en.2 | 2026-27 | 2026-11-04 | Bristol City FC | Wolverhampton Wanderers FC |
| en.2 | 2026-27 | 2026-11-04 | Cardiff City FC | West Ham United FC |
| en.2 | 2026-27 | 2026-11-04 | Wrexham AFC | Middlesbrough FC |
| en.2 | 2026-27 | 2026-11-06 | Derby County FC | Bolton Wanderers FC |
| en.2 | 2026-27 | 2026-11-07 | Birmingham City FC | Swansea City AFC |
| en.2 | 2026-27 | 2026-11-07 | Blackburn Rovers FC | West Ham United FC |
| en.2 | 2026-27 | 2026-11-07 | Bristol City FC | Norwich City FC |
| en.2 | 2026-27 | 2026-11-07 | Cardiff City FC | Burnley FC |
| en.2 | 2026-27 | 2026-11-07 | Charlton Athletic FC | Sheffield United FC |
| en.2 | 2026-27 | 2026-11-07 | Portsmouth FC | Stoke City FC |
| en.2 | 2026-27 | 2026-11-07 | Preston North End FC | Southampton FC |
| en.2 | 2026-27 | 2026-11-07 | Queens Park Rangers FC | Lincoln City FC |
| en.2 | 2026-27 | 2026-11-07 | Watford FC | Middlesbrough FC |
| en.2 | 2026-27 | 2026-11-07 | West Bromwich Albion FC | Millwall FC |
| en.2 | 2026-27 | 2026-11-07 | Wrexham AFC | Wolverhampton Wanderers FC |
| en.3 | 2025-26 | 2025-01-04 | Doncaster Rovers | Luton Town FC |
| en.3 | 2025-26 | 2025-01-04 | Port Vale FC | Barnsley FC |
| en.3 | 2025-26 | 2025-01-04 | Rotherham United FC | Mansfield Town |
| en.3 | 2025-26 | 2025-01-04 | Stevenage FC | Leyton Orient |
| en.3 | 2025-26 | 2025-01-10 | AFC Wimbledon | Blackpool FC |
| en.3 | 2025-26 | 2025-01-10 | Barnsley FC | Wycombe Wanderers FC |
| en.3 | 2025-26 | 2025-01-10 | Bradford City | Rotherham United FC |
| en.3 | 2025-26 | 2025-01-10 | Exeter City | Lincoln City FC |
| en.3 | 2025-26 | 2025-01-10 | Mansfield Town | Reading FC |
| en.3 | 2025-26 | 2025-01-10 | Northampton Town | Port Vale FC |
| en.3 | 2025-26 | 2025-01-10 | Wigan Athletic FC | Plymouth Argyle FC |
| en.3 | 2025-26 | 2025-02-14 | Barnsley FC | AFC Wimbledon |
| en.3 | 2025-26 | 2025-02-14 | Blackpool FC | Plymouth Argyle FC |
| en.3 | 2025-26 | 2025-02-14 | Bradford City | Peterborough United FC |
| en.3 | 2025-26 | 2025-02-14 | Burton Albion | Stockport County |
| en.3 | 2025-26 | 2025-02-14 | Cardiff City FC | Luton Town FC |
| en.3 | 2025-26 | 2025-02-14 | Doncaster Rovers | Port Vale FC |
| en.3 | 2025-26 | 2025-02-14 | Exeter City | Northampton Town |
| en.3 | 2025-26 | 2025-02-14 | Leyton Orient | Mansfield Town |
| en.3 | 2025-26 | 2025-02-14 | Lincoln City FC | Bolton Wanderers FC |
| en.3 | 2025-26 | 2025-02-14 | Reading FC | Wycombe Wanderers FC |
| en.3 | 2025-26 | 2025-02-14 | Stevenage FC | Huddersfield Town AFC |
| en.3 | 2025-26 | 2025-02-14 | Wigan Athletic FC | Rotherham United FC |
| en.3 | 2025-26 | 2025-02-17 | Barnsley FC | Peterborough United FC |
| en.3 | 2025-26 | 2025-02-17 | Blackpool FC | Mansfield Town |
| en.3 | 2025-26 | 2025-02-17 | Bradford City | Stockport County |
| en.3 | 2025-26 | 2025-02-17 | Burton Albion | Rotherham United FC |
| en.3 | 2025-26 | 2025-02-17 | Cardiff City FC | AFC Wimbledon |
| en.3 | 2025-26 | 2025-02-17 | Doncaster Rovers | Huddersfield Town AFC |
| en.3 | 2025-26 | 2025-02-17 | Exeter City | Wycombe Wanderers FC |
| en.3 | 2025-26 | 2025-02-17 | Leyton Orient | Plymouth Argyle FC |
| en.3 | 2025-26 | 2025-02-17 | Lincoln City FC | Northampton Town |
| en.3 | 2025-26 | 2025-02-17 | Reading FC | Bolton Wanderers FC |
| en.3 | 2025-26 | 2025-02-17 | Stevenage FC | Port Vale FC |
| en.3 | 2025-26 | 2025-02-17 | Wigan Athletic FC | Luton Town FC |
| en.3 | 2025-26 | 2025-02-21 | AFC Wimbledon | Bradford City |
| en.3 | 2025-26 | 2025-02-21 | Bolton Wanderers FC | Blackpool FC |
| en.3 | 2025-26 | 2025-02-21 | Huddersfield Town AFC | Barnsley FC |
| en.3 | 2025-26 | 2025-02-21 | Luton Town FC | Burton Albion |
| en.3 | 2025-26 | 2025-02-21 | Mansfield Town | Lincoln City FC |
| en.3 | 2025-26 | 2025-02-21 | Northampton Town | Leyton Orient |
| en.3 | 2025-26 | 2025-02-21 | Peterborough United FC | Exeter City |
| en.3 | 2025-26 | 2025-02-21 | Plymouth Argyle FC | Cardiff City FC |
| en.3 | 2025-26 | 2025-02-21 | Port Vale FC | Reading FC |
| en.3 | 2025-26 | 2025-02-21 | Rotherham United FC | Doncaster Rovers |
| en.3 | 2025-26 | 2025-02-21 | Stockport County | Wigan Athletic FC |
| en.3 | 2025-26 | 2025-02-21 | Wycombe Wanderers FC | Stevenage FC |
| en.3 | 2025-26 | 2025-02-28 | Doncaster Rovers | Cardiff City FC |
| en.3 | 2025-26 | 2025-02-28 | Exeter City | Bolton Wanderers FC |
| en.3 | 2025-26 | 2025-02-28 | Leyton Orient | Barnsley FC |
| en.3 | 2025-26 | 2025-02-28 | Lincoln City FC | Blackpool FC |
| en.3 | 2025-26 | 2025-02-28 | Mansfield Town | AFC Wimbledon |
| en.3 | 2025-26 | 2025-02-28 | Northampton Town | Peterborough United FC |
| en.3 | 2025-26 | 2025-02-28 | Port Vale FC | Luton Town FC |
| en.3 | 2025-26 | 2025-02-28 | Reading FC | Bradford City |
| en.3 | 2025-26 | 2025-02-28 | Rotherham United FC | Plymouth Argyle FC |
| en.3 | 2025-26 | 2025-02-28 | Stevenage FC | Stockport County |
| en.3 | 2025-26 | 2025-02-28 | Wigan Athletic FC | Huddersfield Town AFC |
| en.3 | 2025-26 | 2025-02-28 | Wycombe Wanderers FC | Burton Albion |
| en.3 | 2025-26 | 2025-03-07 | AFC Wimbledon | Northampton Town |
| en.3 | 2025-26 | 2025-03-07 | Barnsley FC | Exeter City |
| en.3 | 2025-26 | 2025-03-07 | Blackpool FC | Wigan Athletic FC |
| en.3 | 2025-26 | 2025-03-07 | Bolton Wanderers FC | Wycombe Wanderers FC |
| en.3 | 2025-26 | 2025-03-07 | Bradford City | Leyton Orient |
| en.3 | 2025-26 | 2025-03-07 | Burton Albion | Stevenage FC |
| en.3 | 2025-26 | 2025-03-07 | Cardiff City FC | Lincoln City FC |
| en.3 | 2025-26 | 2025-03-07 | Huddersfield Town AFC | Rotherham United FC |
| en.3 | 2025-26 | 2025-03-07 | Luton Town FC | Reading FC |
| en.3 | 2025-26 | 2025-03-07 | Peterborough United FC | Port Vale FC |
| en.3 | 2025-26 | 2025-03-07 | Plymouth Argyle FC | Doncaster Rovers |
| en.3 | 2025-26 | 2025-03-07 | Stockport County | Mansfield Town |
| en.3 | 2025-26 | 2025-03-14 | Doncaster Rovers | Blackpool FC |
| en.3 | 2025-26 | 2025-03-14 | Exeter City | Cardiff City FC |
| en.3 | 2025-26 | 2025-03-14 | Leyton Orient | Peterborough United FC |
| en.3 | 2025-26 | 2025-03-14 | Lincoln City FC | Stockport County |
| en.3 | 2025-26 | 2025-03-14 | Mansfield Town | Barnsley FC |
| en.3 | 2025-26 | 2025-03-14 | Northampton Town | Burton Albion |
| en.3 | 2025-26 | 2025-03-14 | Port Vale FC | Huddersfield Town AFC |
| en.3 | 2025-26 | 2025-03-14 | Reading FC | Plymouth Argyle FC |
| en.3 | 2025-26 | 2025-03-14 | Rotherham United FC | Bolton Wanderers FC |
| en.3 | 2025-26 | 2025-03-14 | Stevenage FC | AFC Wimbledon |
| en.3 | 2025-26 | 2025-03-14 | Wigan Athletic FC | Bradford City |
| en.3 | 2025-26 | 2025-03-14 | Wycombe Wanderers FC | Luton Town FC |
| en.3 | 2025-26 | 2025-03-17 | AFC Wimbledon | Leyton Orient |
| en.3 | 2025-26 | 2025-03-17 | Barnsley FC | Wigan Athletic FC |
| en.3 | 2025-26 | 2025-03-17 | Blackpool FC | Port Vale FC |
| en.3 | 2025-26 | 2025-03-17 | Bolton Wanderers FC | Doncaster Rovers |
| en.3 | 2025-26 | 2025-03-17 | Bradford City | Mansfield Town |
| en.3 | 2025-26 | 2025-03-17 | Burton Albion | Reading FC |
| en.3 | 2025-26 | 2025-03-17 | Cardiff City FC | Wycombe Wanderers FC |
| en.3 | 2025-26 | 2025-03-17 | Huddersfield Town AFC | Lincoln City FC |
| en.3 | 2025-26 | 2025-03-17 | Luton Town FC | Exeter City |
| en.3 | 2025-26 | 2025-03-17 | Peterborough United FC | Rotherham United FC |
| en.3 | 2025-26 | 2025-03-17 | Plymouth Argyle FC | Stevenage FC |
| en.3 | 2025-26 | 2025-03-17 | Stockport County | Northampton Town |
| en.3 | 2025-26 | 2025-03-21 | AFC Wimbledon | Peterborough United FC |
| en.3 | 2025-26 | 2025-03-21 | Barnsley FC | Doncaster Rovers |
| en.3 | 2025-26 | 2025-03-21 | Burton Albion | Bradford City |
| en.3 | 2025-26 | 2025-03-21 | Cardiff City FC | Blackpool FC |
| en.3 | 2025-26 | 2025-03-21 | Leyton Orient | Wycombe Wanderers FC |
| en.3 | 2025-26 | 2025-03-21 | Lincoln City FC | Rotherham United FC |
| en.3 | 2025-26 | 2025-03-21 | Luton Town FC | Stockport County |
| en.3 | 2025-26 | 2025-03-21 | Mansfield Town | Northampton Town |
| en.3 | 2025-26 | 2025-03-21 | Plymouth Argyle FC | Huddersfield Town AFC |
| en.3 | 2025-26 | 2025-03-21 | Port Vale FC | Bolton Wanderers FC |
| en.3 | 2025-26 | 2025-03-21 | Stevenage FC | Reading FC |
| en.3 | 2025-26 | 2025-03-21 | Wigan Athletic FC | Exeter City |
| en.3 | 2025-26 | 2025-03-28 | Blackpool FC | Burton Albion |
| en.3 | 2025-26 | 2025-03-28 | Bolton Wanderers FC | Stevenage FC |
| en.3 | 2025-26 | 2025-03-28 | Bradford City | Plymouth Argyle FC |
| en.3 | 2025-26 | 2025-03-28 | Doncaster Rovers | Lincoln City FC |
| en.3 | 2025-26 | 2025-03-28 | Exeter City | Leyton Orient |
| en.3 | 2025-26 | 2025-03-28 | Huddersfield Town AFC | Cardiff City FC |
| en.3 | 2025-26 | 2025-03-28 | Northampton Town | Barnsley FC |
| en.3 | 2025-26 | 2025-03-28 | Peterborough United FC | Mansfield Town |
| en.3 | 2025-26 | 2025-03-28 | Reading FC | Wigan Athletic FC |
| en.3 | 2025-26 | 2025-03-28 | Rotherham United FC | Luton Town FC |
| en.3 | 2025-26 | 2025-03-28 | Stockport County | AFC Wimbledon |
| en.3 | 2025-26 | 2025-03-28 | Wycombe Wanderers FC | Port Vale FC |
| en.3 | 2025-26 | 2025-04-03 | Blackpool FC | Exeter City |
| en.3 | 2025-26 | 2025-04-03 | Bradford City | Northampton Town |
| en.3 | 2025-26 | 2025-04-03 | Burton Albion | Barnsley FC |
| en.3 | 2025-26 | 2025-04-03 | Cardiff City FC | Port Vale FC |
| en.3 | 2025-26 | 2025-04-03 | Doncaster Rovers | Mansfield Town |
| en.3 | 2025-26 | 2025-04-03 | Huddersfield Town AFC | Reading FC |
| en.3 | 2025-26 | 2025-04-03 | Lincoln City FC | AFC Wimbledon |
| en.3 | 2025-26 | 2025-04-03 | Luton Town FC | Peterborough United FC |
| en.3 | 2025-26 | 2025-04-03 | Plymouth Argyle FC | Bolton Wanderers FC |
| en.3 | 2025-26 | 2025-04-03 | Rotherham United FC | Stevenage FC |
| en.3 | 2025-26 | 2025-04-03 | Stockport County | Wycombe Wanderers FC |
| en.3 | 2025-26 | 2025-04-03 | Wigan Athletic FC | Leyton Orient |
| en.3 | 2025-26 | 2025-04-06 | AFC Wimbledon | Luton Town FC |
| en.3 | 2025-26 | 2025-04-06 | Barnsley FC | Plymouth Argyle FC |
| en.3 | 2025-26 | 2025-04-06 | Bolton Wanderers FC | Stockport County |
| en.3 | 2025-26 | 2025-04-06 | Exeter City | Doncaster Rovers |
| en.3 | 2025-26 | 2025-04-06 | Leyton Orient | Huddersfield Town AFC |
| en.3 | 2025-26 | 2025-04-06 | Mansfield Town | Burton Albion |
| en.3 | 2025-26 | 2025-04-06 | Northampton Town | Wigan Athletic FC |
| en.3 | 2025-26 | 2025-04-06 | Peterborough United FC | Cardiff City FC |
| en.3 | 2025-26 | 2025-04-06 | Port Vale FC | Rotherham United FC |
| en.3 | 2025-26 | 2025-04-06 | Reading FC | Lincoln City FC |
| en.3 | 2025-26 | 2025-04-06 | Stevenage FC | Blackpool FC |
| en.3 | 2025-26 | 2025-04-06 | Wycombe Wanderers FC | Bradford City |
| en.3 | 2025-26 | 2025-04-11 | Blackpool FC | Peterborough United FC |
| en.3 | 2025-26 | 2025-04-11 | Bradford City | Stevenage FC |
| en.3 | 2025-26 | 2025-04-11 | Burton Albion | AFC Wimbledon |
| en.3 | 2025-26 | 2025-04-11 | Cardiff City FC | Bolton Wanderers FC |
| en.3 | 2025-26 | 2025-04-11 | Doncaster Rovers | Reading FC |
| en.3 | 2025-26 | 2025-04-11 | Huddersfield Town AFC | Wycombe Wanderers FC |
| en.3 | 2025-26 | 2025-04-11 | Lincoln City FC | Leyton Orient |
| en.3 | 2025-26 | 2025-04-11 | Luton Town FC | Northampton Town |
| en.3 | 2025-26 | 2025-04-11 | Plymouth Argyle FC | Exeter City |
| en.3 | 2025-26 | 2025-04-11 | Rotherham United FC | Barnsley FC |
| en.3 | 2025-26 | 2025-04-11 | Stockport County | Port Vale FC |
| en.3 | 2025-26 | 2025-04-11 | Wigan Athletic FC | Mansfield Town |
| en.3 | 2025-26 | 2025-04-18 | AFC Wimbledon | Plymouth Argyle FC |
| en.3 | 2025-26 | 2025-04-18 | Barnsley FC | Bradford City |
| en.3 | 2025-26 | 2025-04-18 | Bolton Wanderers FC | Huddersfield Town AFC |
| en.3 | 2025-26 | 2025-04-18 | Exeter City | Stockport County |
| en.3 | 2025-26 | 2025-04-18 | Leyton Orient | Rotherham United FC |
| en.3 | 2025-26 | 2025-04-18 | Mansfield Town | Luton Town FC |
| en.3 | 2025-26 | 2025-04-18 | Northampton Town | Doncaster Rovers |
| en.3 | 2025-26 | 2025-04-18 | Peterborough United FC | Burton Albion |
| en.3 | 2025-26 | 2025-04-18 | Port Vale FC | Wigan Athletic FC |
| en.3 | 2025-26 | 2025-04-18 | Reading FC | Cardiff City FC |
| en.3 | 2025-26 | 2025-04-18 | Stevenage FC | Lincoln City FC |
| en.3 | 2025-26 | 2025-04-18 | Wycombe Wanderers FC | Blackpool FC |
| en.3 | 2025-26 | 2025-04-25 | Blackpool FC | Leyton Orient |
| en.3 | 2025-26 | 2025-04-25 | Bradford City | Bolton Wanderers FC |
| en.3 | 2025-26 | 2025-04-25 | Burton Albion | Exeter City |
| en.3 | 2025-26 | 2025-04-25 | Cardiff City FC | Northampton Town |
| en.3 | 2025-26 | 2025-04-25 | Doncaster Rovers | Stevenage FC |
| en.3 | 2025-26 | 2025-04-25 | Huddersfield Town AFC | Mansfield Town |
| en.3 | 2025-26 | 2025-04-25 | Lincoln City FC | Wycombe Wanderers FC |
| en.3 | 2025-26 | 2025-04-25 | Luton Town FC | Barnsley FC |
| en.3 | 2025-26 | 2025-04-25 | Plymouth Argyle FC | Port Vale FC |
| en.3 | 2025-26 | 2025-04-25 | Rotherham United FC | Reading FC |
| en.3 | 2025-26 | 2025-04-25 | Stockport County | Peterborough United FC |
| en.3 | 2025-26 | 2025-04-25 | Wigan Athletic FC | AFC Wimbledon |
| en.3 | 2025-26 | 2025-05-02 | AFC Wimbledon | Huddersfield Town AFC |
| en.3 | 2025-26 | 2025-05-02 | Barnsley FC | Stockport County |
| en.3 | 2025-26 | 2025-05-02 | Bolton Wanderers FC | Luton Town FC |
| en.3 | 2025-26 | 2025-05-02 | Exeter City | Bradford City |
| en.3 | 2025-26 | 2025-05-02 | Leyton Orient | Burton Albion |
| en.3 | 2025-26 | 2025-05-02 | Mansfield Town | Cardiff City FC |
| en.3 | 2025-26 | 2025-05-02 | Northampton Town | Plymouth Argyle FC |
| en.3 | 2025-26 | 2025-05-02 | Peterborough United FC | Doncaster Rovers |
| en.3 | 2025-26 | 2025-05-02 | Port Vale FC | Lincoln City FC |
| en.3 | 2025-26 | 2025-05-02 | Reading FC | Blackpool FC |
| en.3 | 2025-26 | 2025-05-02 | Stevenage FC | Wigan Athletic FC |
| en.3 | 2025-26 | 2025-05-02 | Wycombe Wanderers FC | Rotherham United FC |
| en.3 | 2025-26 | 2025-11-04 | Rotherham United FC | Burton Albion |
| en.3 | 2025-26 | 2025-11-25 | Luton Town FC | Huddersfield Town AFC |
| en.3 | 2025-26 | 2025-11-25 | Peterborough United FC | Stevenage FC |
| en.4 | 2025-26 | 2026-01-01 | Barnet FC | Crawley Town |
| en.4 | 2025-26 | 2026-01-01 | Barrow AFC | Salford City |
| en.4 | 2025-26 | 2026-01-01 | Bromley FC | Newport County |
| en.4 | 2025-26 | 2026-01-01 | Cambridge United | Walsall FC |
| en.4 | 2025-26 | 2026-01-01 | Colchester United | Milton Keynes Dons |
| en.4 | 2025-26 | 2026-01-01 | Crewe Alexandra | Cheltenham Town |
| en.4 | 2025-26 | 2026-01-01 | Fleetwood Town | Grimsby Town |
| en.4 | 2025-26 | 2026-01-01 | Harrogate Town | Tranmere Rovers |
| en.4 | 2025-26 | 2026-01-01 | Notts County | Accrington Stanley |
| en.4 | 2025-26 | 2026-01-01 | Oldham Athletic | Chesterfield FC |
| en.4 | 2025-26 | 2026-01-01 | Shrewsbury Town | Bristol Rovers |
| en.4 | 2025-26 | 2026-01-01 | Swindon Town | Gillingham FC |
| en.4 | 2025-26 | 2026-01-04 | Barnet FC | Crewe Alexandra |
| en.4 | 2025-26 | 2026-01-04 | Barrow AFC | Bristol Rovers |
| en.4 | 2025-26 | 2026-01-04 | Bromley FC | Oldham Athletic |
| en.4 | 2025-26 | 2026-01-04 | Cambridge United | Grimsby Town |
| en.4 | 2025-26 | 2026-01-04 | Cheltenham Town | Crawley Town |
| en.4 | 2025-26 | 2026-01-04 | Colchester United | Accrington Stanley |
| en.4 | 2025-26 | 2026-01-04 | Harrogate Town | Swindon Town |
| en.4 | 2025-26 | 2026-01-04 | Milton Keynes Dons | Chesterfield FC |
| en.4 | 2025-26 | 2026-01-04 | Newport County | Tranmere Rovers |
| en.4 | 2025-26 | 2026-01-04 | Notts County | Gillingham FC |
| en.4 | 2025-26 | 2026-01-04 | Salford City | Shrewsbury Town |
| en.4 | 2025-26 | 2026-01-04 | Walsall FC | Fleetwood Town |
| en.4 | 2025-26 | 2026-01-10 | Accrington Stanley | Barnet FC |
| en.4 | 2025-26 | 2026-01-10 | Bristol Rovers | Walsall FC |
| en.4 | 2025-26 | 2026-01-10 | Chesterfield FC | Colchester United |
| en.4 | 2025-26 | 2026-01-10 | Crawley Town | Cambridge United |
| en.4 | 2025-26 | 2026-01-10 | Crewe Alexandra | Harrogate Town |
| en.4 | 2025-26 | 2026-01-10 | Fleetwood Town | Cheltenham Town |
| en.4 | 2025-26 | 2026-01-10 | Gillingham FC | Milton Keynes Dons |
| en.4 | 2025-26 | 2026-01-10 | Grimsby Town | Salford City |
| en.4 | 2025-26 | 2026-01-10 | Oldham Athletic | Notts County |
| en.4 | 2025-26 | 2026-01-10 | Shrewsbury Town | Barrow AFC |
| en.4 | 2025-26 | 2026-01-10 | Swindon Town | Newport County |
| en.4 | 2025-26 | 2026-01-10 | Tranmere Rovers | Bromley FC |
| en.4 | 2025-26 | 2026-01-17 | Accrington Stanley | Milton Keynes Dons |
| en.4 | 2025-26 | 2026-01-17 | Bristol Rovers | Colchester United |
| en.4 | 2025-26 | 2026-01-17 | Chesterfield FC | Bromley FC |
| en.4 | 2025-26 | 2026-01-17 | Crawley Town | Notts County |
| en.4 | 2025-26 | 2026-01-17 | Crewe Alexandra | Barrow AFC |
| en.4 | 2025-26 | 2026-01-17 | Fleetwood Town | Cambridge United |
| en.4 | 2025-26 | 2026-01-17 | Gillingham FC | Newport County |
| en.4 | 2025-26 | 2026-01-17 | Grimsby Town | Barnet FC |
| en.4 | 2025-26 | 2026-01-17 | Oldham Athletic | Cheltenham Town |
| en.4 | 2025-26 | 2026-01-17 | Shrewsbury Town | Harrogate Town |
| en.4 | 2025-26 | 2026-01-17 | Swindon Town | Salford City |
| en.4 | 2025-26 | 2026-01-17 | Tranmere Rovers | Walsall FC |
| en.4 | 2025-26 | 2026-01-24 | Barnet FC | Oldham Athletic |
| en.4 | 2025-26 | 2026-01-24 | Barrow AFC | Crawley Town |
| en.4 | 2025-26 | 2026-01-24 | Bromley FC | Swindon Town |
| en.4 | 2025-26 | 2026-01-24 | Cambridge United | Tranmere Rovers |
| en.4 | 2025-26 | 2026-01-24 | Cheltenham Town | Grimsby Town |
| en.4 | 2025-26 | 2026-01-24 | Colchester United | Fleetwood Town |
| en.4 | 2025-26 | 2026-01-24 | Harrogate Town | Gillingham FC |
| en.4 | 2025-26 | 2026-01-24 | Milton Keynes Dons | Shrewsbury Town |
| en.4 | 2025-26 | 2026-01-24 | Newport County | Chesterfield FC |
| en.4 | 2025-26 | 2026-01-24 | Notts County | Crewe Alexandra |
| en.4 | 2025-26 | 2026-01-24 | Salford City | Bristol Rovers |
| en.4 | 2025-26 | 2026-01-24 | Walsall FC | Accrington Stanley |
| en.4 | 2025-26 | 2026-01-27 | Barnet FC | Tranmere Rovers |
| en.4 | 2025-26 | 2026-01-27 | Barrow AFC | Oldham Athletic |
| en.4 | 2025-26 | 2026-01-27 | Bromley FC | Crewe Alexandra |
| en.4 | 2025-26 | 2026-01-27 | Cambridge United | Shrewsbury Town |
| en.4 | 2025-26 | 2026-01-27 | Cheltenham Town | Gillingham FC |
| en.4 | 2025-26 | 2026-01-27 | Colchester United | Grimsby Town |
| en.4 | 2025-26 | 2026-01-27 | Harrogate Town | Fleetwood Town |
| en.4 | 2025-26 | 2026-01-27 | Milton Keynes Dons | Bristol Rovers |
| en.4 | 2025-26 | 2026-01-27 | Newport County | Accrington Stanley |
| en.4 | 2025-26 | 2026-01-27 | Notts County | Swindon Town |
| en.4 | 2025-26 | 2026-01-27 | Salford City | Chesterfield FC |
| en.4 | 2025-26 | 2026-01-27 | Walsall FC | Crawley Town |
| en.4 | 2025-26 | 2026-01-31 | Accrington Stanley | Cheltenham Town |
| en.4 | 2025-26 | 2026-01-31 | Bristol Rovers | Newport County |
| en.4 | 2025-26 | 2026-01-31 | Chesterfield FC | Walsall FC |
| en.4 | 2025-26 | 2026-01-31 | Crawley Town | Harrogate Town |
| en.4 | 2025-26 | 2026-01-31 | Crewe Alexandra | Colchester United |
| en.4 | 2025-26 | 2026-01-31 | Fleetwood Town | Notts County |
| en.4 | 2025-26 | 2026-01-31 | Gillingham FC | Bromley FC |
| en.4 | 2025-26 | 2026-01-31 | Grimsby Town | Milton Keynes Dons |
| en.4 | 2025-26 | 2026-01-31 | Oldham Athletic | Cambridge United |
| en.4 | 2025-26 | 2026-01-31 | Shrewsbury Town | Barnet FC |
| en.4 | 2025-26 | 2026-01-31 | Swindon Town | Barrow AFC |
| en.4 | 2025-26 | 2026-01-31 | Tranmere Rovers | Salford City |
| en.4 | 2025-26 | 2026-02-07 | Accrington Stanley | Salford City |
| en.4 | 2025-26 | 2026-02-07 | Bristol Rovers | Chesterfield FC |
| en.4 | 2025-26 | 2026-02-07 | Cheltenham Town | Milton Keynes Dons |
| en.4 | 2025-26 | 2026-02-07 | Colchester United | Shrewsbury Town |
| en.4 | 2025-26 | 2026-02-07 | Crawley Town | Crewe Alexandra |
| en.4 | 2025-26 | 2026-02-07 | Fleetwood Town | Bromley FC |
| en.4 | 2025-26 | 2026-02-07 | Gillingham FC | Tranmere Rovers |
| en.4 | 2025-26 | 2026-02-07 | Harrogate Town | Cambridge United |
| en.4 | 2025-26 | 2026-02-07 | Newport County | Grimsby Town |
| en.4 | 2025-26 | 2026-02-07 | Notts County | Barrow AFC |
| en.4 | 2025-26 | 2026-02-07 | Swindon Town | Oldham Athletic |
| en.4 | 2025-26 | 2026-02-07 | Walsall FC | Barnet FC |
| en.4 | 2025-26 | 2026-02-14 | Barnet FC | Cheltenham Town |
| en.4 | 2025-26 | 2026-02-14 | Barrow AFC | Colchester United |
| en.4 | 2025-26 | 2026-02-14 | Bromley FC | Notts County |
| en.4 | 2025-26 | 2026-02-14 | Cambridge United | Bristol Rovers |
| en.4 | 2025-26 | 2026-02-14 | Chesterfield FC | Harrogate Town |
| en.4 | 2025-26 | 2026-02-14 | Crewe Alexandra | Gillingham FC |
| en.4 | 2025-26 | 2026-02-14 | Grimsby Town | Accrington Stanley |
| en.4 | 2025-26 | 2026-02-14 | Milton Keynes Dons | Newport County |
| en.4 | 2025-26 | 2026-02-14 | Oldham Athletic | Fleetwood Town |
| en.4 | 2025-26 | 2026-02-14 | Salford City | Walsall FC |
| en.4 | 2025-26 | 2026-02-14 | Shrewsbury Town | Swindon Town |
| en.4 | 2025-26 | 2026-02-14 | Tranmere Rovers | Crawley Town |
| en.4 | 2025-26 | 2026-02-17 | Barnet FC | Swindon Town |
| en.4 | 2025-26 | 2026-02-17 | Barrow AFC | Harrogate Town |
| en.4 | 2025-26 | 2026-02-17 | Bromley FC | Cheltenham Town |
| en.4 | 2025-26 | 2026-02-17 | Cambridge United | Colchester United |
| en.4 | 2025-26 | 2026-02-17 | Chesterfield FC | Gillingham FC |
| en.4 | 2025-26 | 2026-02-17 | Crewe Alexandra | Fleetwood Town |
| en.4 | 2025-26 | 2026-02-17 | Grimsby Town | Walsall FC |
| en.4 | 2025-26 | 2026-02-17 | Milton Keynes Dons | Crawley Town |
| en.4 | 2025-26 | 2026-02-17 | Oldham Athletic | Bristol Rovers |
| en.4 | 2025-26 | 2026-02-17 | Salford City | Newport County |
| en.4 | 2025-26 | 2026-02-17 | Shrewsbury Town | Notts County |
| en.4 | 2025-26 | 2026-02-17 | Tranmere Rovers | Accrington Stanley |
| en.4 | 2025-26 | 2026-02-21 | Accrington Stanley | Shrewsbury Town |
| en.4 | 2025-26 | 2026-02-21 | Bristol Rovers | Grimsby Town |
| en.4 | 2025-26 | 2026-02-21 | Cheltenham Town | Salford City |
| en.4 | 2025-26 | 2026-02-21 | Colchester United | Barnet FC |
| en.4 | 2025-26 | 2026-02-21 | Crawley Town | Chesterfield FC |
| en.4 | 2025-26 | 2026-02-21 | Fleetwood Town | Barrow AFC |
| en.4 | 2025-26 | 2026-02-21 | Gillingham FC | Oldham Athletic |
| en.4 | 2025-26 | 2026-02-21 | Harrogate Town | Bromley FC |
| en.4 | 2025-26 | 2026-02-21 | Newport County | Cambridge United |
| en.4 | 2025-26 | 2026-02-21 | Notts County | Tranmere Rovers |
| en.4 | 2025-26 | 2026-02-21 | Swindon Town | Crewe Alexandra |
| en.4 | 2025-26 | 2026-02-21 | Walsall FC | Milton Keynes Dons |
| en.4 | 2025-26 | 2026-02-28 | Barnet FC | Chesterfield FC |
| en.4 | 2025-26 | 2026-02-28 | Barrow AFC | Gillingham FC |
| en.4 | 2025-26 | 2026-02-28 | Bromley FC | Accrington Stanley |
| en.4 | 2025-26 | 2026-02-28 | Cambridge United | Milton Keynes Dons |
| en.4 | 2025-26 | 2026-02-28 | Colchester United | Salford City |
| en.4 | 2025-26 | 2026-02-28 | Crewe Alexandra | Tranmere Rovers |
| en.4 | 2025-26 | 2026-02-28 | Fleetwood Town | Newport County |
| en.4 | 2025-26 | 2026-02-28 | Harrogate Town | Cheltenham Town |
| en.4 | 2025-26 | 2026-02-28 | Notts County | Grimsby Town |
| en.4 | 2025-26 | 2026-02-28 | Oldham Athletic | Crawley Town |
| en.4 | 2025-26 | 2026-02-28 | Shrewsbury Town | Walsall FC |
| en.4 | 2025-26 | 2026-02-28 | Swindon Town | Bristol Rovers |
| en.4 | 2025-26 | 2026-03-07 | Accrington Stanley | Cambridge United |
| en.4 | 2025-26 | 2026-03-07 | Bristol Rovers | Crewe Alexandra |
| en.4 | 2025-26 | 2026-03-07 | Cheltenham Town | Barrow AFC |
| en.4 | 2025-26 | 2026-03-07 | Chesterfield FC | Shrewsbury Town |
| en.4 | 2025-26 | 2026-03-07 | Crawley Town | Swindon Town |
| en.4 | 2025-26 | 2026-03-07 | Gillingham FC | Fleetwood Town |
| en.4 | 2025-26 | 2026-03-07 | Grimsby Town | Bromley FC |
| en.4 | 2025-26 | 2026-03-07 | Milton Keynes Dons | Harrogate Town |
| en.4 | 2025-26 | 2026-03-07 | Newport County | Colchester United |
| en.4 | 2025-26 | 2026-03-07 | Salford City | Barnet FC |
| en.4 | 2025-26 | 2026-03-07 | Tranmere Rovers | Oldham Athletic |
| en.4 | 2025-26 | 2026-03-07 | Walsall FC | Notts County |
| en.4 | 2025-26 | 2026-03-14 | Barnet FC | Newport County |
| en.4 | 2025-26 | 2026-03-14 | Barrow AFC | Accrington Stanley |
| en.4 | 2025-26 | 2026-03-14 | Bromley FC | Bristol Rovers |
| en.4 | 2025-26 | 2026-03-14 | Cambridge United | Gillingham FC |
| en.4 | 2025-26 | 2026-03-14 | Colchester United | Crawley Town |
| en.4 | 2025-26 | 2026-03-14 | Crewe Alexandra | Walsall FC |
| en.4 | 2025-26 | 2026-03-14 | Fleetwood Town | Tranmere Rovers |
| en.4 | 2025-26 | 2026-03-14 | Harrogate Town | Salford City |
| en.4 | 2025-26 | 2026-03-14 | Notts County | Chesterfield FC |
| en.4 | 2025-26 | 2026-03-14 | Oldham Athletic | Grimsby Town |
| en.4 | 2025-26 | 2026-03-14 | Shrewsbury Town | Cheltenham Town |
| en.4 | 2025-26 | 2026-03-14 | Swindon Town | Milton Keynes Dons |
| en.4 | 2025-26 | 2026-03-17 | Accrington Stanley | Notts County |
| en.4 | 2025-26 | 2026-03-17 | Bristol Rovers | Shrewsbury Town |
| en.4 | 2025-26 | 2026-03-17 | Cheltenham Town | Crewe Alexandra |
| en.4 | 2025-26 | 2026-03-17 | Chesterfield FC | Oldham Athletic |
| en.4 | 2025-26 | 2026-03-17 | Crawley Town | Barnet FC |
| en.4 | 2025-26 | 2026-03-17 | Gillingham FC | Swindon Town |
| en.4 | 2025-26 | 2026-03-17 | Grimsby Town | Fleetwood Town |
| en.4 | 2025-26 | 2026-03-17 | Milton Keynes Dons | Colchester United |
| en.4 | 2025-26 | 2026-03-17 | Newport County | Bromley FC |
| en.4 | 2025-26 | 2026-03-17 | Salford City | Barrow AFC |
| en.4 | 2025-26 | 2026-03-17 | Tranmere Rovers | Harrogate Town |
| en.4 | 2025-26 | 2026-03-17 | Walsall FC | Cambridge United |
| en.4 | 2025-26 | 2026-03-21 | Accrington Stanley | Chesterfield FC |
| en.4 | 2025-26 | 2026-03-21 | Bromley FC | Colchester United |
| en.4 | 2025-26 | 2026-03-21 | Cambridge United | Salford City |
| en.4 | 2025-26 | 2026-03-21 | Fleetwood Town | Crawley Town |
| en.4 | 2025-26 | 2026-03-21 | Gillingham FC | Bristol Rovers |
| en.4 | 2025-26 | 2026-03-21 | Grimsby Town | Barrow AFC |
| en.4 | 2025-26 | 2026-03-21 | Milton Keynes Dons | Barnet FC |
| en.4 | 2025-26 | 2026-03-21 | Notts County | Cheltenham Town |
| en.4 | 2025-26 | 2026-03-21 | Oldham Athletic | Harrogate Town |
| en.4 | 2025-26 | 2026-03-21 | Shrewsbury Town | Crewe Alexandra |
| en.4 | 2025-26 | 2026-03-21 | Tranmere Rovers | Swindon Town |
| en.4 | 2025-26 | 2026-03-21 | Walsall FC | Newport County |
| en.4 | 2025-26 | 2026-03-28 | Barnet FC | Cambridge United |
| en.4 | 2025-26 | 2026-03-28 | Barrow AFC | Bromley FC |
| en.4 | 2025-26 | 2026-03-28 | Bristol Rovers | Accrington Stanley |
| en.4 | 2025-26 | 2026-03-28 | Cheltenham Town | Tranmere Rovers |
| en.4 | 2025-26 | 2026-03-28 | Chesterfield FC | Grimsby Town |
| en.4 | 2025-26 | 2026-03-28 | Colchester United | Walsall FC |
| en.4 | 2025-26 | 2026-03-28 | Crawley Town | Gillingham FC |
| en.4 | 2025-26 | 2026-03-28 | Crewe Alexandra | Oldham Athletic |
| en.4 | 2025-26 | 2026-03-28 | Harrogate Town | Notts County |
| en.4 | 2025-26 | 2026-03-28 | Newport County | Shrewsbury Town |
| en.4 | 2025-26 | 2026-03-28 | Salford City | Milton Keynes Dons |
| en.4 | 2025-26 | 2026-03-28 | Swindon Town | Fleetwood Town |
| en.4 | 2025-26 | 2026-04-03 | Accrington Stanley | Crewe Alexandra |
| en.4 | 2025-26 | 2026-04-03 | Barnet FC | Bromley FC |
| en.4 | 2025-26 | 2026-04-03 | Bristol Rovers | Fleetwood Town |
| en.4 | 2025-26 | 2026-04-03 | Cambridge United | Swindon Town |
| en.4 | 2025-26 | 2026-04-03 | Chesterfield FC | Cheltenham Town |
| en.4 | 2025-26 | 2026-04-03 | Colchester United | Oldham Athletic |
| en.4 | 2025-26 | 2026-04-03 | Grimsby Town | Harrogate Town |
| en.4 | 2025-26 | 2026-04-03 | Milton Keynes Dons | Barrow AFC |
| en.4 | 2025-26 | 2026-04-03 | Newport County | Crawley Town |
| en.4 | 2025-26 | 2026-04-03 | Salford City | Notts County |
| en.4 | 2025-26 | 2026-04-03 | Shrewsbury Town | Tranmere Rovers |
| en.4 | 2025-26 | 2026-04-03 | Walsall FC | Gillingham FC |
| en.4 | 2025-26 | 2026-04-06 | Barrow AFC | Chesterfield FC |
| en.4 | 2025-26 | 2026-04-06 | Bromley FC | Shrewsbury Town |
| en.4 | 2025-26 | 2026-04-06 | Cheltenham Town | Cambridge United |
| en.4 | 2025-26 | 2026-04-06 | Crawley Town | Grimsby Town |
| en.4 | 2025-26 | 2026-04-06 | Crewe Alexandra | Salford City |
| en.4 | 2025-26 | 2026-04-06 | Fleetwood Town | Barnet FC |
| en.4 | 2025-26 | 2026-04-06 | Gillingham FC | Accrington Stanley |
| en.4 | 2025-26 | 2026-04-06 | Harrogate Town | Bristol Rovers |
| en.4 | 2025-26 | 2026-04-06 | Notts County | Newport County |
| en.4 | 2025-26 | 2026-04-06 | Oldham Athletic | Milton Keynes Dons |
| en.4 | 2025-26 | 2026-04-06 | Swindon Town | Walsall FC |
| en.4 | 2025-26 | 2026-04-06 | Tranmere Rovers | Colchester United |
| en.4 | 2025-26 | 2026-04-11 | Accrington Stanley | Fleetwood Town |
| en.4 | 2025-26 | 2026-04-11 | Barnet FC | Barrow AFC |
| en.4 | 2025-26 | 2026-04-11 | Bristol Rovers | Crawley Town |
| en.4 | 2025-26 | 2026-04-11 | Cambridge United | Notts County |
| en.4 | 2025-26 | 2026-04-11 | Chesterfield FC | Tranmere Rovers |
| en.4 | 2025-26 | 2026-04-11 | Colchester United | Swindon Town |
| en.4 | 2025-26 | 2026-04-11 | Grimsby Town | Crewe Alexandra |
| en.4 | 2025-26 | 2026-04-11 | Milton Keynes Dons | Bromley FC |
| en.4 | 2025-26 | 2026-04-11 | Newport County | Harrogate Town |
| en.4 | 2025-26 | 2026-04-11 | Salford City | Gillingham FC |
| en.4 | 2025-26 | 2026-04-11 | Shrewsbury Town | Oldham Athletic |
| en.4 | 2025-26 | 2026-04-11 | Walsall FC | Cheltenham Town |
| en.4 | 2025-26 | 2026-04-18 | Barrow AFC | Walsall FC |
| en.4 | 2025-26 | 2026-04-18 | Bromley FC | Cambridge United |
| en.4 | 2025-26 | 2026-04-18 | Cheltenham Town | Newport County |
| en.4 | 2025-26 | 2026-04-18 | Crawley Town | Shrewsbury Town |
| en.4 | 2025-26 | 2026-04-18 | Crewe Alexandra | Milton Keynes Dons |
| en.4 | 2025-26 | 2026-04-18 | Fleetwood Town | Chesterfield FC |
| en.4 | 2025-26 | 2026-04-18 | Gillingham FC | Grimsby Town |
| en.4 | 2025-26 | 2026-04-18 | Harrogate Town | Colchester United |
| en.4 | 2025-26 | 2026-04-18 | Notts County | Barnet FC |
| en.4 | 2025-26 | 2026-04-18 | Oldham Athletic | Salford City |
| en.4 | 2025-26 | 2026-04-18 | Swindon Town | Accrington Stanley |
| en.4 | 2025-26 | 2026-04-18 | Tranmere Rovers | Bristol Rovers |
| en.4 | 2025-26 | 2026-04-25 | Accrington Stanley | Crawley Town |
| en.4 | 2025-26 | 2026-04-25 | Barnet FC | Gillingham FC |
| en.4 | 2025-26 | 2026-04-25 | Bristol Rovers | Cheltenham Town |
| en.4 | 2025-26 | 2026-04-25 | Cambridge United | Barrow AFC |
| en.4 | 2025-26 | 2026-04-25 | Chesterfield FC | Crewe Alexandra |
| en.4 | 2025-26 | 2026-04-25 | Colchester United | Notts County |
| en.4 | 2025-26 | 2026-04-25 | Grimsby Town | Swindon Town |
| en.4 | 2025-26 | 2026-04-25 | Milton Keynes Dons | Tranmere Rovers |
| en.4 | 2025-26 | 2026-04-25 | Newport County | Oldham Athletic |
| en.4 | 2025-26 | 2026-04-25 | Salford City | Bromley FC |
| en.4 | 2025-26 | 2026-04-25 | Shrewsbury Town | Fleetwood Town |
| en.4 | 2025-26 | 2026-04-25 | Walsall FC | Harrogate Town |
| en.4 | 2025-26 | 2026-05-02 | Barrow AFC | Newport County |
| en.4 | 2025-26 | 2026-05-02 | Bromley FC | Walsall FC |
| en.4 | 2025-26 | 2026-05-02 | Cheltenham Town | Colchester United |
| en.4 | 2025-26 | 2026-05-02 | Crawley Town | Salford City |
| en.4 | 2025-26 | 2026-05-02 | Crewe Alexandra | Cambridge United |
| en.4 | 2025-26 | 2026-05-02 | Fleetwood Town | Milton Keynes Dons |
| en.4 | 2025-26 | 2026-05-02 | Gillingham FC | Shrewsbury Town |
| en.4 | 2025-26 | 2026-05-02 | Harrogate Town | Barnet FC |
| en.4 | 2025-26 | 2026-05-02 | Notts County | Bristol Rovers |
| en.4 | 2025-26 | 2026-05-02 | Oldham Athletic | Accrington Stanley |
| en.4 | 2025-26 | 2026-05-02 | Swindon Town | Chesterfield FC |
| en.4 | 2025-26 | 2026-05-02 | Tranmere Rovers | Grimsby Town |

</details>

## Coverage gaps

Files not present upstream (league/season not available):

- `2016-17/en.2.json`
- `2016-17/en.3.json`
- `2016-17/en.4.json`
- `2017-18/en.2.json`
- `2017-18/en.3.json`
- `2017-18/en.4.json`
- `2021-22/en.3.json`
- `2021-22/en.4.json`
- `2022-23/en.3.json`
- `2022-23/en.4.json`
- `2023-24/en.3.json`
- `2023-24/en.4.json`
- `2026-27/en.3.json`
- `2026-27/en.4.json`

## Data issues

| Issue | Count |
|---|---|
| date_inconsistent_with_round | 143 |
| date_outside_season | 276 |

<details><summary>All issues</summary>

Issue kinds: `date_outside_season` = date outside the season's normal window (kept as published, likely an upstream typo); `date_inconsistent_with_round` = dated over 180 days before an earlier matchday (year typo inside the window; kept, flagged, excluded from evaluation); `invalid_*` = value unreadable, stored as empty; `conflicting_duplicate` = same fixture listed with different data, all copies excluded.

- en.3 2025-26 `date_outside_season`: 2025-01-01 Doncaster Rovers v Bolton Wanderers
- en.3 2025-26 `date_outside_season`: 2025-01-01 Exeter City v Luton Town
- en.3 2025-26 `date_outside_season`: 2025-01-01 Leyton Orient v AFC Wimbledon
- en.3 2025-26 `date_outside_season`: 2025-01-01 Lincoln City v Huddersfield Town
- en.3 2025-26 `date_outside_season`: 2025-01-01 Mansfield Town v Bradford City
- en.3 2025-26 `date_outside_season`: 2025-01-01 Northampton Town v Stockport County
- en.3 2025-26 `date_outside_season`: 2025-01-01 Port Vale FC v Blackpool FC
- en.3 2025-26 `date_outside_season`: 2025-01-01 Reading FC v Burton Albion
- en.3 2025-26 `date_outside_season`: 2025-01-01 Rotherham United v Peterborough United
- en.3 2025-26 `date_outside_season`: 2025-01-01 Stevenage FC v Plymouth Argyle
- en.3 2025-26 `date_outside_season`: 2025-01-01 Wigan Athletic v Barnsley FC
- en.3 2025-26 `date_outside_season`: 2025-01-01 Wycombe Wanderers v Cardiff City
- en.3 2025-26 `date_outside_season`: 2025-01-04 Bolton Wanderers v Northampton Town
- en.3 2025-26 `date_outside_season`: 2025-01-04 Lincoln City v Peterborough United
- en.3 2025-26 `date_outside_season`: 2025-01-04 Blackpool FC v Bradford City
- en.3 2025-26 `date_outside_season`: 2025-01-04 Cardiff City v Wigan Athletic
- en.3 2025-26 `date_outside_season`: 2025-01-04 Doncaster Rovers v Luton Town
- en.3 2025-26 `date_outside_season`: 2025-01-04 Huddersfield Town v Exeter City
- en.3 2025-26 `date_outside_season`: 2025-01-04 Plymouth Argyle v Burton Albion
- en.3 2025-26 `date_outside_season`: 2025-01-04 Port Vale FC v Barnsley FC
- en.3 2025-26 `date_outside_season`: 2025-01-04 Reading FC v Stockport County
- en.3 2025-26 `date_outside_season`: 2025-01-04 Rotherham United v Mansfield Town
- en.3 2025-26 `date_outside_season`: 2025-01-04 Stevenage FC v Leyton Orient
- en.3 2025-26 `date_outside_season`: 2025-01-04 Wycombe Wanderers v AFC Wimbledon
- en.3 2025-26 `date_outside_season`: 2025-01-10 AFC Wimbledon v Blackpool FC
- en.3 2025-26 `date_outside_season`: 2025-01-10 Barnsley FC v Wycombe Wanderers
- en.3 2025-26 `date_outside_season`: 2025-01-10 Bradford City v Rotherham United
- en.3 2025-26 `date_outside_season`: 2025-01-10 Burton Albion v Doncaster Rovers
- en.3 2025-26 `date_outside_season`: 2025-01-10 Exeter City v Lincoln City
- en.3 2025-26 `date_outside_season`: 2025-01-10 Leyton Orient v Cardiff City
- en.3 2025-26 `date_outside_season`: 2025-01-10 Luton Town v Stevenage FC
- en.3 2025-26 `date_outside_season`: 2025-01-10 Mansfield Town v Reading FC
- en.3 2025-26 `date_outside_season`: 2025-01-10 Northampton Town v Port Vale FC
- en.3 2025-26 `date_outside_season`: 2025-01-10 Peterborough United v Bolton Wanderers
- en.3 2025-26 `date_outside_season`: 2025-01-10 Stockport County v Huddersfield Town
- en.3 2025-26 `date_outside_season`: 2025-01-10 Wigan Athletic v Plymouth Argyle
- en.3 2025-26 `date_outside_season`: 2025-01-17 Wigan Athletic v Bolton Wanderers
- en.3 2025-26 `date_outside_season`: 2025-01-17 AFC Wimbledon v Doncaster Rovers
- en.3 2025-26 `date_outside_season`: 2025-01-17 Barnsley FC v Blackpool FC
- en.3 2025-26 `date_outside_season`: 2025-01-17 Bradford City v Cardiff City
- en.3 2025-26 `date_outside_season`: 2025-01-17 Burton Albion v Huddersfield Town
- en.3 2025-26 `date_outside_season`: 2025-01-17 Exeter City v Stevenage FC
- en.3 2025-26 `date_outside_season`: 2025-01-17 Leyton Orient v Reading FC
- en.3 2025-26 `date_outside_season`: 2025-01-17 Luton Town v Lincoln City
- en.3 2025-26 `date_outside_season`: 2025-01-17 Mansfield Town v Port Vale FC
- en.3 2025-26 `date_outside_season`: 2025-01-17 Northampton Town v Wycombe Wanderers
- en.3 2025-26 `date_outside_season`: 2025-01-17 Peterborough United v Plymouth Argyle
- en.3 2025-26 `date_outside_season`: 2025-01-17 Stockport County v Rotherham United
- en.3 2025-26 `date_outside_season`: 2025-01-24 Blackpool FC v Northampton Town
- en.3 2025-26 `date_outside_season`: 2025-01-24 Bolton Wanderers v Leyton Orient
- en.3 2025-26 `date_outside_season`: 2025-01-24 Cardiff City v Stockport County
- en.3 2025-26 `date_outside_season`: 2025-01-24 Doncaster Rovers v Wigan Athletic
- en.3 2025-26 `date_outside_season`: 2025-01-24 Huddersfield Town v Bradford City
- en.3 2025-26 `date_outside_season`: 2025-01-24 Lincoln City v Burton Albion
- en.3 2025-26 `date_outside_season`: 2025-01-24 Plymouth Argyle v Luton Town
- en.3 2025-26 `date_outside_season`: 2025-01-24 Port Vale FC v Exeter City
- en.3 2025-26 `date_outside_season`: 2025-01-24 Reading FC v Barnsley FC
- en.3 2025-26 `date_outside_season`: 2025-01-24 Rotherham United v AFC Wimbledon
- en.3 2025-26 `date_outside_season`: 2025-01-24 Stevenage FC v Mansfield Town
- en.3 2025-26 `date_outside_season`: 2025-01-24 Wycombe Wanderers v Peterborough United
- en.3 2025-26 `date_outside_season`: 2025-01-27 Blackpool FC v Stockport County
- en.3 2025-26 `date_outside_season`: 2025-01-27 Bolton Wanderers v Burton Albion
- en.3 2025-26 `date_outside_season`: 2025-01-27 Cardiff City v Barnsley FC
- en.3 2025-26 `date_outside_season`: 2025-01-27 Doncaster Rovers v Leyton Orient
- en.3 2025-26 `date_outside_season`: 2025-01-27 Huddersfield Town v Luton Town
- en.3 2025-26 `date_outside_season`: 2025-01-27 Lincoln City v Bradford City
- en.3 2025-26 `date_outside_season`: 2025-01-27 Plymouth Argyle v Mansfield Town
- en.3 2025-26 `date_outside_season`: 2025-01-27 Port Vale FC v AFC Wimbledon
- en.3 2025-26 `date_outside_season`: 2025-01-27 Rotherham United v Northampton Town
- en.3 2025-26 `date_outside_season`: 2025-01-27 Stevenage FC v Peterborough United
- en.3 2025-26 `date_outside_season`: 2025-01-27 Wycombe Wanderers v Wigan Athletic
- en.3 2025-26 `date_outside_season`: 2025-01-27 Reading FC v Exeter City
- en.3 2025-26 `date_outside_season`: 2025-01-31 AFC Wimbledon v Bolton Wanderers
- en.3 2025-26 `date_outside_season`: 2025-01-31 Barnsley FC v Stevenage FC
- en.3 2025-26 `date_outside_season`: 2025-01-31 Bradford City v Doncaster Rovers
- en.3 2025-26 `date_outside_season`: 2025-01-31 Burton Albion v Cardiff City
- en.3 2025-26 `date_outside_season`: 2025-01-31 Exeter City v Rotherham United
- en.3 2025-26 `date_outside_season`: 2025-01-31 Leyton Orient v Port Vale FC
- en.3 2025-26 `date_outside_season`: 2025-01-31 Luton Town v Blackpool FC
- en.3 2025-26 `date_outside_season`: 2025-01-31 Mansfield Town v Wycombe Wanderers
- en.3 2025-26 `date_outside_season`: 2025-01-31 Northampton Town v Reading FC
- en.3 2025-26 `date_outside_season`: 2025-01-31 Peterborough United v Huddersfield Town
- en.3 2025-26 `date_outside_season`: 2025-01-31 Stockport County v Plymouth Argyle
- en.3 2025-26 `date_outside_season`: 2025-01-31 Wigan Athletic v Lincoln City
- en.3 2025-26 `date_outside_season`: 2025-02-07 AFC Wimbledon v Reading FC
- en.3 2025-26 `date_outside_season`: 2025-02-07 Bolton Wanderers v Barnsley FC
- en.3 2025-26 `date_outside_season`: 2025-02-07 Huddersfield Town v Blackpool FC
- en.3 2025-26 `date_outside_season`: 2025-02-07 Luton Town v Bradford City
- en.3 2025-26 `date_outside_season`: 2025-02-07 Mansfield Town v Exeter City
- en.3 2025-26 `date_outside_season`: 2025-02-07 Northampton Town v Stevenage FC
- en.3 2025-26 `date_outside_season`: 2025-02-07 Peterborough United v Wigan Athletic
- en.3 2025-26 `date_outside_season`: 2025-02-07 Plymouth Argyle v Lincoln City
- en.3 2025-26 `date_outside_season`: 2025-02-07 Port Vale FC v Burton Albion
- en.3 2025-26 `date_outside_season`: 2025-02-07 Rotherham United v Cardiff City
- en.3 2025-26 `date_outside_season`: 2025-02-07 Stockport County v Leyton Orient
- en.3 2025-26 `date_outside_season`: 2025-02-07 Wycombe Wanderers v Doncaster Rovers
- en.3 2025-26 `date_outside_season`: 2025-02-14 Barnsley FC v AFC Wimbledon
- en.3 2025-26 `date_outside_season`: 2025-02-14 Blackpool FC v Plymouth Argyle
- en.3 2025-26 `date_outside_season`: 2025-02-14 Bradford City v Peterborough United
- en.3 2025-26 `date_outside_season`: 2025-02-14 Burton Albion v Stockport County
- en.3 2025-26 `date_outside_season`: 2025-02-14 Cardiff City v Luton Town
- en.3 2025-26 `date_outside_season`: 2025-02-14 Doncaster Rovers v Port Vale FC
- en.3 2025-26 `date_outside_season`: 2025-02-14 Exeter City v Northampton Town
- en.3 2025-26 `date_outside_season`: 2025-02-14 Leyton Orient v Mansfield Town
- en.3 2025-26 `date_outside_season`: 2025-02-14 Lincoln City v Bolton Wanderers
- en.3 2025-26 `date_outside_season`: 2025-02-14 Reading FC v Wycombe Wanderers
- en.3 2025-26 `date_outside_season`: 2025-02-14 Stevenage FC v Huddersfield Town
- en.3 2025-26 `date_outside_season`: 2025-02-14 Wigan Athletic v Rotherham United
- en.3 2025-26 `date_outside_season`: 2025-02-17 Barnsley FC v Peterborough United
- en.3 2025-26 `date_outside_season`: 2025-02-17 Blackpool FC v Mansfield Town
- en.3 2025-26 `date_outside_season`: 2025-02-17 Bradford City v Stockport County
- en.3 2025-26 `date_outside_season`: 2025-02-17 Burton Albion v Rotherham United
- en.3 2025-26 `date_outside_season`: 2025-02-17 Cardiff City v AFC Wimbledon
- en.3 2025-26 `date_outside_season`: 2025-02-17 Doncaster Rovers v Huddersfield Town
- en.3 2025-26 `date_outside_season`: 2025-02-17 Exeter City v Wycombe Wanderers
- en.3 2025-26 `date_outside_season`: 2025-02-17 Leyton Orient v Plymouth Argyle
- en.3 2025-26 `date_outside_season`: 2025-02-17 Lincoln City v Northampton Town
- en.3 2025-26 `date_outside_season`: 2025-02-17 Stevenage FC v Port Vale FC
- en.3 2025-26 `date_outside_season`: 2025-02-17 Wigan Athletic v Luton Town
- en.3 2025-26 `date_outside_season`: 2025-02-17 Reading FC v Bolton Wanderers
- en.3 2025-26 `date_outside_season`: 2025-02-21 AFC Wimbledon v Bradford City
- en.3 2025-26 `date_outside_season`: 2025-02-21 Bolton Wanderers v Blackpool FC
- en.3 2025-26 `date_outside_season`: 2025-02-21 Huddersfield Town v Barnsley FC
- en.3 2025-26 `date_outside_season`: 2025-02-21 Luton Town v Burton Albion
- en.3 2025-26 `date_outside_season`: 2025-02-21 Mansfield Town v Lincoln City
- en.3 2025-26 `date_outside_season`: 2025-02-21 Northampton Town v Leyton Orient
- en.3 2025-26 `date_outside_season`: 2025-02-21 Peterborough United v Exeter City
- en.3 2025-26 `date_outside_season`: 2025-02-21 Plymouth Argyle v Cardiff City
- en.3 2025-26 `date_outside_season`: 2025-02-21 Port Vale FC v Reading FC
- en.3 2025-26 `date_outside_season`: 2025-02-21 Rotherham United v Doncaster Rovers
- en.3 2025-26 `date_outside_season`: 2025-02-21 Stockport County v Wigan Athletic
- en.3 2025-26 `date_outside_season`: 2025-02-21 Wycombe Wanderers v Stevenage FC
- en.3 2025-26 `date_outside_season`: 2025-02-28 Doncaster Rovers v Cardiff City
- en.3 2025-26 `date_outside_season`: 2025-02-28 Exeter City v Bolton Wanderers
- en.3 2025-26 `date_outside_season`: 2025-02-28 Leyton Orient v Barnsley FC
- en.3 2025-26 `date_outside_season`: 2025-02-28 Lincoln City v Blackpool FC
- en.3 2025-26 `date_outside_season`: 2025-02-28 Mansfield Town v AFC Wimbledon
- en.3 2025-26 `date_outside_season`: 2025-02-28 Northampton Town v Peterborough United
- en.3 2025-26 `date_outside_season`: 2025-02-28 Port Vale FC v Luton Town
- en.3 2025-26 `date_outside_season`: 2025-02-28 Reading FC v Bradford City
- en.3 2025-26 `date_outside_season`: 2025-02-28 Rotherham United v Plymouth Argyle
- en.3 2025-26 `date_outside_season`: 2025-02-28 Stevenage FC v Stockport County
- en.3 2025-26 `date_outside_season`: 2025-02-28 Wigan Athletic v Huddersfield Town
- en.3 2025-26 `date_outside_season`: 2025-02-28 Wycombe Wanderers v Burton Albion
- en.3 2025-26 `date_outside_season`: 2025-03-07 AFC Wimbledon v Northampton Town
- en.3 2025-26 `date_outside_season`: 2025-03-07 Barnsley FC v Exeter City
- en.3 2025-26 `date_outside_season`: 2025-03-07 Blackpool FC v Wigan Athletic
- en.3 2025-26 `date_outside_season`: 2025-03-07 Bolton Wanderers v Wycombe Wanderers
- en.3 2025-26 `date_outside_season`: 2025-03-07 Bradford City v Leyton Orient
- en.3 2025-26 `date_outside_season`: 2025-03-07 Burton Albion v Stevenage FC
- en.3 2025-26 `date_outside_season`: 2025-03-07 Cardiff City v Lincoln City
- en.3 2025-26 `date_outside_season`: 2025-03-07 Huddersfield Town v Rotherham United
- en.3 2025-26 `date_outside_season`: 2025-03-07 Luton Town v Reading FC
- en.3 2025-26 `date_outside_season`: 2025-03-07 Peterborough United v Port Vale FC
- en.3 2025-26 `date_outside_season`: 2025-03-07 Plymouth Argyle v Doncaster Rovers
- en.3 2025-26 `date_outside_season`: 2025-03-07 Stockport County v Mansfield Town
- en.3 2025-26 `date_outside_season`: 2025-03-14 Doncaster Rovers v Blackpool FC
- en.3 2025-26 `date_outside_season`: 2025-03-14 Exeter City v Cardiff City
- en.3 2025-26 `date_outside_season`: 2025-03-14 Leyton Orient v Peterborough United
- en.3 2025-26 `date_outside_season`: 2025-03-14 Lincoln City v Stockport County
- en.3 2025-26 `date_outside_season`: 2025-03-14 Mansfield Town v Barnsley FC
- en.3 2025-26 `date_outside_season`: 2025-03-14 Northampton Town v Burton Albion
- en.3 2025-26 `date_outside_season`: 2025-03-14 Port Vale FC v Huddersfield Town
- en.3 2025-26 `date_outside_season`: 2025-03-14 Reading FC v Plymouth Argyle
- en.3 2025-26 `date_outside_season`: 2025-03-14 Rotherham United v Bolton Wanderers
- en.3 2025-26 `date_outside_season`: 2025-03-14 Stevenage FC v AFC Wimbledon
- en.3 2025-26 `date_outside_season`: 2025-03-14 Wigan Athletic v Bradford City
- en.3 2025-26 `date_outside_season`: 2025-03-14 Wycombe Wanderers v Luton Town
- en.3 2025-26 `date_outside_season`: 2025-03-17 AFC Wimbledon v Leyton Orient
- en.3 2025-26 `date_outside_season`: 2025-03-17 Barnsley FC v Wigan Athletic
- en.3 2025-26 `date_outside_season`: 2025-03-17 Blackpool FC v Port Vale FC
- en.3 2025-26 `date_outside_season`: 2025-03-17 Bolton Wanderers v Doncaster Rovers
- en.3 2025-26 `date_outside_season`: 2025-03-17 Bradford City v Mansfield Town
- en.3 2025-26 `date_outside_season`: 2025-03-17 Burton Albion v Reading FC
- en.3 2025-26 `date_outside_season`: 2025-03-17 Cardiff City v Wycombe Wanderers
- en.3 2025-26 `date_outside_season`: 2025-03-17 Huddersfield Town v Lincoln City
- en.3 2025-26 `date_outside_season`: 2025-03-17 Luton Town v Exeter City
- en.3 2025-26 `date_outside_season`: 2025-03-17 Peterborough United v Rotherham United
- en.3 2025-26 `date_outside_season`: 2025-03-17 Plymouth Argyle v Stevenage FC
- en.3 2025-26 `date_outside_season`: 2025-03-17 Stockport County v Northampton Town
- en.3 2025-26 `date_outside_season`: 2025-03-21 AFC Wimbledon v Peterborough United
- en.3 2025-26 `date_outside_season`: 2025-03-21 Barnsley FC v Doncaster Rovers
- en.3 2025-26 `date_outside_season`: 2025-03-21 Burton Albion v Bradford City
- en.3 2025-26 `date_outside_season`: 2025-03-21 Cardiff City v Blackpool FC
- en.3 2025-26 `date_outside_season`: 2025-03-21 Leyton Orient v Wycombe Wanderers
- en.3 2025-26 `date_outside_season`: 2025-03-21 Lincoln City v Rotherham United
- en.3 2025-26 `date_outside_season`: 2025-03-21 Luton Town v Stockport County
- en.3 2025-26 `date_outside_season`: 2025-03-21 Mansfield Town v Northampton Town
- en.3 2025-26 `date_outside_season`: 2025-03-21 Plymouth Argyle v Huddersfield Town
- en.3 2025-26 `date_outside_season`: 2025-03-21 Port Vale FC v Bolton Wanderers
- en.3 2025-26 `date_outside_season`: 2025-03-21 Stevenage FC v Reading FC
- en.3 2025-26 `date_outside_season`: 2025-03-21 Wigan Athletic v Exeter City
- en.3 2025-26 `date_outside_season`: 2025-03-28 Blackpool FC v Burton Albion
- en.3 2025-26 `date_outside_season`: 2025-03-28 Bolton Wanderers v Stevenage FC
- en.3 2025-26 `date_outside_season`: 2025-03-28 Bradford City v Plymouth Argyle
- en.3 2025-26 `date_outside_season`: 2025-03-28 Doncaster Rovers v Lincoln City
- en.3 2025-26 `date_outside_season`: 2025-03-28 Exeter City v Leyton Orient
- en.3 2025-26 `date_outside_season`: 2025-03-28 Huddersfield Town v Cardiff City
- en.3 2025-26 `date_outside_season`: 2025-03-28 Northampton Town v Barnsley FC
- en.3 2025-26 `date_outside_season`: 2025-03-28 Peterborough United v Mansfield Town
- en.3 2025-26 `date_outside_season`: 2025-03-28 Reading FC v Wigan Athletic
- en.3 2025-26 `date_outside_season`: 2025-03-28 Rotherham United v Luton Town
- en.3 2025-26 `date_outside_season`: 2025-03-28 Stockport County v AFC Wimbledon
- en.3 2025-26 `date_outside_season`: 2025-03-28 Wycombe Wanderers v Port Vale FC
- en.3 2025-26 `date_outside_season`: 2025-04-03 Blackpool FC v Exeter City
- en.3 2025-26 `date_outside_season`: 2025-04-03 Bradford City v Northampton Town
- en.3 2025-26 `date_outside_season`: 2025-04-03 Burton Albion v Barnsley FC
- en.3 2025-26 `date_outside_season`: 2025-04-03 Cardiff City v Port Vale FC
- en.3 2025-26 `date_outside_season`: 2025-04-03 Doncaster Rovers v Mansfield Town
- en.3 2025-26 `date_outside_season`: 2025-04-03 Huddersfield Town v Reading FC
- en.3 2025-26 `date_outside_season`: 2025-04-03 Lincoln City v AFC Wimbledon
- en.3 2025-26 `date_outside_season`: 2025-04-03 Luton Town v Peterborough United
- en.3 2025-26 `date_outside_season`: 2025-04-03 Plymouth Argyle v Bolton Wanderers
- en.3 2025-26 `date_outside_season`: 2025-04-03 Rotherham United v Stevenage FC
- en.3 2025-26 `date_outside_season`: 2025-04-03 Stockport County v Wycombe Wanderers
- en.3 2025-26 `date_outside_season`: 2025-04-03 Wigan Athletic v Leyton Orient
- en.3 2025-26 `date_outside_season`: 2025-04-06 AFC Wimbledon v Luton Town
- en.3 2025-26 `date_outside_season`: 2025-04-06 Barnsley FC v Plymouth Argyle
- en.3 2025-26 `date_outside_season`: 2025-04-06 Bolton Wanderers v Stockport County
- en.3 2025-26 `date_outside_season`: 2025-04-06 Exeter City v Doncaster Rovers
- en.3 2025-26 `date_outside_season`: 2025-04-06 Leyton Orient v Huddersfield Town
- en.3 2025-26 `date_outside_season`: 2025-04-06 Mansfield Town v Burton Albion
- en.3 2025-26 `date_outside_season`: 2025-04-06 Northampton Town v Wigan Athletic
- en.3 2025-26 `date_outside_season`: 2025-04-06 Peterborough United v Cardiff City
- en.3 2025-26 `date_outside_season`: 2025-04-06 Port Vale FC v Rotherham United
- en.3 2025-26 `date_outside_season`: 2025-04-06 Reading FC v Lincoln City
- en.3 2025-26 `date_outside_season`: 2025-04-06 Stevenage FC v Blackpool FC
- en.3 2025-26 `date_outside_season`: 2025-04-06 Wycombe Wanderers v Bradford City
- en.3 2025-26 `date_outside_season`: 2025-04-11 Blackpool FC v Peterborough United
- en.3 2025-26 `date_outside_season`: 2025-04-11 Bradford City v Stevenage FC
- en.3 2025-26 `date_outside_season`: 2025-04-11 Burton Albion v AFC Wimbledon
- en.3 2025-26 `date_outside_season`: 2025-04-11 Cardiff City v Bolton Wanderers
- en.3 2025-26 `date_outside_season`: 2025-04-11 Doncaster Rovers v Reading FC
- en.3 2025-26 `date_outside_season`: 2025-04-11 Huddersfield Town v Wycombe Wanderers
- en.3 2025-26 `date_outside_season`: 2025-04-11 Lincoln City v Leyton Orient
- en.3 2025-26 `date_outside_season`: 2025-04-11 Luton Town v Northampton Town
- en.3 2025-26 `date_outside_season`: 2025-04-11 Plymouth Argyle v Exeter City
- en.3 2025-26 `date_outside_season`: 2025-04-11 Rotherham United v Barnsley FC
- en.3 2025-26 `date_outside_season`: 2025-04-11 Stockport County v Port Vale FC
- en.3 2025-26 `date_outside_season`: 2025-04-11 Wigan Athletic v Mansfield Town
- en.3 2025-26 `date_outside_season`: 2025-04-18 AFC Wimbledon v Plymouth Argyle
- en.3 2025-26 `date_outside_season`: 2025-04-18 Barnsley FC v Bradford City
- en.3 2025-26 `date_outside_season`: 2025-04-18 Bolton Wanderers v Huddersfield Town
- en.3 2025-26 `date_outside_season`: 2025-04-18 Exeter City v Stockport County
- en.3 2025-26 `date_outside_season`: 2025-04-18 Leyton Orient v Rotherham United
- en.3 2025-26 `date_outside_season`: 2025-04-18 Mansfield Town v Luton Town
- en.3 2025-26 `date_outside_season`: 2025-04-18 Northampton Town v Doncaster Rovers
- en.3 2025-26 `date_outside_season`: 2025-04-18 Peterborough United v Burton Albion
- en.3 2025-26 `date_outside_season`: 2025-04-18 Port Vale FC v Wigan Athletic
- en.3 2025-26 `date_outside_season`: 2025-04-18 Reading FC v Cardiff City
- en.3 2025-26 `date_outside_season`: 2025-04-18 Stevenage FC v Lincoln City
- en.3 2025-26 `date_outside_season`: 2025-04-18 Wycombe Wanderers v Blackpool FC
- en.3 2025-26 `date_outside_season`: 2025-04-25 Blackpool FC v Leyton Orient
- en.3 2025-26 `date_outside_season`: 2025-04-25 Bradford City v Bolton Wanderers
- en.3 2025-26 `date_outside_season`: 2025-04-25 Burton Albion v Exeter City
- en.3 2025-26 `date_outside_season`: 2025-04-25 Cardiff City v Northampton Town
- en.3 2025-26 `date_outside_season`: 2025-04-25 Doncaster Rovers v Stevenage FC
- en.3 2025-26 `date_outside_season`: 2025-04-25 Huddersfield Town v Mansfield Town
- en.3 2025-26 `date_outside_season`: 2025-04-25 Lincoln City v Wycombe Wanderers
- en.3 2025-26 `date_outside_season`: 2025-04-25 Luton Town v Barnsley FC
- en.3 2025-26 `date_outside_season`: 2025-04-25 Plymouth Argyle v Port Vale FC
- en.3 2025-26 `date_outside_season`: 2025-04-25 Rotherham United v Reading FC
- en.3 2025-26 `date_outside_season`: 2025-04-25 Stockport County v Peterborough United
- en.3 2025-26 `date_outside_season`: 2025-04-25 Wigan Athletic v AFC Wimbledon
- en.3 2025-26 `date_outside_season`: 2025-05-02 AFC Wimbledon v Huddersfield Town
- en.3 2025-26 `date_outside_season`: 2025-05-02 Barnsley FC v Stockport County
- en.3 2025-26 `date_outside_season`: 2025-05-02 Bolton Wanderers v Luton Town
- en.3 2025-26 `date_outside_season`: 2025-05-02 Exeter City v Bradford City
- en.3 2025-26 `date_outside_season`: 2025-05-02 Leyton Orient v Burton Albion
- en.3 2025-26 `date_outside_season`: 2025-05-02 Mansfield Town v Cardiff City
- en.3 2025-26 `date_outside_season`: 2025-05-02 Northampton Town v Plymouth Argyle
- en.3 2025-26 `date_outside_season`: 2025-05-02 Peterborough United v Doncaster Rovers
- en.3 2025-26 `date_outside_season`: 2025-05-02 Port Vale FC v Lincoln City
- en.3 2025-26 `date_outside_season`: 2025-05-02 Reading FC v Blackpool FC
- en.3 2025-26 `date_outside_season`: 2025-05-02 Stevenage FC v Wigan Athletic
- en.3 2025-26 `date_outside_season`: 2025-05-02 Wycombe Wanderers v Rotherham United
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-01 AFC Bournemouth v Newcastle United FC (Matchday 32; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-01 Arsenal FC v Norwich City FC (Matchday 32; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-01 Everton FC v Leicester City FC (Matchday 32; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-01 West Ham United FC v Chelsea FC (Matchday 32; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-02 Manchester City FC v Liverpool FC (Matchday 32; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-02 Sheffield United FC v Tottenham Hotspur FC (Matchday 32; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-04 Norwich City FC v Brighton & Hove Albion FC (Matchday 33; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-04 Leicester City FC v Crystal Palace FC (Matchday 33; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-04 Manchester United FC v AFC Bournemouth (Matchday 33; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-04 Wolverhampton Wanderers FC v Arsenal FC (Matchday 33; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-04 Chelsea FC v Watford FC (Matchday 33; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-05 Newcastle United FC v West Ham United FC (Matchday 33; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-05 Liverpool FC v Aston Villa FC (Matchday 33; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-05 Southampton FC v Manchester City FC (Matchday 33; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-05 Burnley FC v Sheffield United FC (Matchday 33; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-06 Tottenham Hotspur FC v Everton FC (Matchday 33; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-07 Watford FC v Norwich City FC (Matchday 34; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-07 Arsenal FC v Leicester City FC (Matchday 34; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-07 Crystal Palace FC v Chelsea FC (Matchday 34; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-08 Manchester City FC v Newcastle United FC (Matchday 34; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-08 Sheffield United FC v Wolverhampton Wanderers FC (Matchday 34; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-08 West Ham United FC v Burnley FC (Matchday 34; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-08 Brighton & Hove Albion FC v Liverpool FC (Matchday 34; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-09 Everton FC v Southampton FC (Matchday 34; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-09 Aston Villa FC v Manchester United FC (Matchday 34; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-09 AFC Bournemouth v Tottenham Hotspur FC (Matchday 34; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-11 Watford FC v Newcastle United FC (Matchday 35; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-11 Liverpool FC v Burnley FC (Matchday 35; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-11 Sheffield United FC v Chelsea FC (Matchday 35; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-11 Brighton & Hove Albion FC v Manchester City FC (Matchday 35; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-11 Norwich City FC v West Ham United FC (Matchday 35; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-12 Wolverhampton Wanderers FC v Everton FC (Matchday 35; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-12 Aston Villa FC v Crystal Palace FC (Matchday 35; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-12 Tottenham Hotspur FC v Arsenal FC (Matchday 35; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-12 AFC Bournemouth v Leicester City FC (Matchday 35; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-13 Manchester United FC v Southampton FC (Matchday 35; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-14 Chelsea FC v Norwich City FC (Matchday 36; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-15 Manchester City FC v AFC Bournemouth (Matchday 36; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-15 Newcastle United FC v Tottenham Hotspur FC (Matchday 36; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-15 Arsenal FC v Liverpool FC (Matchday 36; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-15 Burnley FC v Wolverhampton Wanderers FC (Matchday 36; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-16 Everton FC v Aston Villa FC (Matchday 36; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-16 Leicester City FC v Sheffield United FC (Matchday 36; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-16 Crystal Palace FC v Manchester United FC (Matchday 36; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-16 Southampton FC v Brighton & Hove Albion FC (Matchday 36; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-17 West Ham United FC v Watford FC (Matchday 36; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-18 Norwich City FC v Burnley FC (Matchday 37; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-19 Tottenham Hotspur FC v Leicester City FC (Matchday 37; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-19 AFC Bournemouth v Southampton FC (Matchday 37; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-20 Brighton & Hove Albion FC v Newcastle United FC (Matchday 37; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-20 Sheffield United FC v Everton FC (Matchday 37; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-20 Wolverhampton Wanderers FC v Crystal Palace FC (Matchday 37; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-21 Aston Villa FC v Arsenal FC (Matchday 37; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-21 Watford FC v Manchester City FC (Matchday 37; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-22 Manchester United FC v West Ham United FC (Matchday 37; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-22 Liverpool FC v Chelsea FC (Matchday 37; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-26 Arsenal FC v Watford FC (Matchday 38; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-26 Burnley FC v Brighton & Hove Albion FC (Matchday 38; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-26 Chelsea FC v Wolverhampton Wanderers FC (Matchday 38; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-26 Crystal Palace FC v Tottenham Hotspur FC (Matchday 38; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-26 Everton FC v AFC Bournemouth (Matchday 38; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-26 Leicester City FC v Manchester United FC (Matchday 38; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-26 Manchester City FC v Norwich City FC (Matchday 38; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-26 Newcastle United FC v Liverpool FC (Matchday 38; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-26 Southampton FC v Sheffield United FC (Matchday 38; earlier matchdays ~2020-06-24)
- en.1 2019-20 `date_inconsistent_with_round`: 2019-07-26 West Ham United FC v Aston Villa FC (Matchday 38; earlier matchdays ~2020-06-24)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-01 Birmingham City FC v Huddersfield Town AFC (Matchday 40; earlier matchdays ~2020-06-27)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-01 Nottingham Forest FC v Bristol City FC (Matchday 40; earlier matchdays ~2020-06-27)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-01 Sheffield Wednesday FC v West Bromwich Albion FC (Matchday 40; earlier matchdays ~2020-06-27)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-01 Preston North End FC v Derby County FC (Matchday 40; earlier matchdays ~2020-06-27)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-02 Hull City AFC v Middlesbrough FC (Matchday 40; earlier matchdays ~2020-06-27)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-03 Charlton Athletic FC v Millwall FC (Matchday 41; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-04 Derby County FC v Nottingham Forest FC (Matchday 41; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-04 Blackburn Rovers FC v Leeds United FC (Matchday 41; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-04 Brentford FC v Wigan Athletic FC (Matchday 41; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-04 Bristol City FC v Cardiff City FC (Matchday 41; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-04 Fulham FC v Birmingham City FC (Matchday 41; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-04 Huddersfield Town AFC v Preston North End FC (Matchday 41; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-04 Luton Town FC v Reading FC (Matchday 41; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-04 Stoke City FC v Barnsley FC (Matchday 41; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-05 Middlesbrough FC v Queens Park Rangers FC (Matchday 41; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-05 West Bromwich Albion FC v Hull City AFC (Matchday 41; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-05 Swansea City AFC v Sheffield Wednesday FC (Matchday 41; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-07 Brentford FC v Charlton Athletic FC (Matchday 42; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-07 Luton Town FC v Barnsley FC (Matchday 42; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-07 Reading FC v Huddersfield Town AFC (Matchday 42; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-07 Cardiff City FC v Blackburn Rovers FC (Matchday 42; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-07 Nottingham Forest FC v Fulham FC (Matchday 42; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-08 Millwall FC v Middlesbrough FC (Matchday 42; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-08 West Bromwich Albion FC v Derby County FC (Matchday 42; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-08 Birmingham City FC v Swansea City AFC (Matchday 42; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-08 Bristol City FC v Hull City AFC (Matchday 42; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-08 Wigan Athletic FC v Queens Park Rangers FC (Matchday 42; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-08 Sheffield Wednesday FC v Preston North End FC (Matchday 42; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-09 Leeds United FC v Stoke City FC (Matchday 42; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-10 Fulham FC v Cardiff City FC (Matchday 43; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-10 Huddersfield Town AFC v Luton Town FC (Matchday 43; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-11 Charlton Athletic FC v Reading FC (Matchday 43; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-11 Derby County FC v Brentford FC (Matchday 43; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-11 Barnsley FC v Wigan Athletic FC (Matchday 43; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-11 Blackburn Rovers FC v West Bromwich Albion FC (Matchday 43; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-11 Hull City AFC v Millwall FC (Matchday 43; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-11 Middlesbrough FC v Bristol City FC (Matchday 43; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-11 Preston North End FC v Nottingham Forest FC (Matchday 43; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-11 Queens Park Rangers FC v Sheffield Wednesday FC (Matchday 43; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-12 Swansea City AFC v Leeds United FC (Matchday 43; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-12 Stoke City FC v Birmingham City FC (Matchday 43; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-14 West Bromwich Albion FC v Fulham FC (Matchday 44; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-14 Reading FC v Middlesbrough FC (Matchday 44; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-14 Wigan Athletic FC v Hull City AFC (Matchday 44; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-14 Cardiff City FC v Derby County FC (Matchday 44; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-14 Luton Town FC v Queens Park Rangers FC (Matchday 44; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-14 Millwall FC v Blackburn Rovers FC (Matchday 44; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-14 Sheffield Wednesday FC v Huddersfield Town AFC (Matchday 44; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-15 Bristol City FC v Stoke City FC (Matchday 44; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-15 Birmingham City FC v Charlton Athletic FC (Matchday 44; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-15 Nottingham Forest FC v Swansea City AFC (Matchday 44; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-15 Brentford FC v Preston North End FC (Matchday 44; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-16 Leeds United FC v Barnsley FC (Matchday 44; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-17 Huddersfield Town AFC v West Bromwich Albion FC (Matchday 45; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-18 Charlton Athletic FC v Wigan Athletic FC (Matchday 45; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-18 Stoke City FC v Brentford FC (Matchday 45; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-18 Blackburn Rovers FC v Reading FC (Matchday 45; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-18 Fulham FC v Sheffield Wednesday FC (Matchday 45; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-18 Hull City AFC v Luton Town FC (Matchday 45; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-18 Middlesbrough FC v Cardiff City FC (Matchday 45; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-18 Preston North End FC v Birmingham City FC (Matchday 45; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-18 Queens Park Rangers FC v Millwall FC (Matchday 45; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-18 Swansea City AFC v Bristol City FC (Matchday 45; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-19 Barnsley FC v Nottingham Forest FC (Matchday 45; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-19 Derby County FC v Leeds United FC (Matchday 45; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-22 Birmingham City FC v Derby County FC (Matchday 46; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-22 Brentford FC v Barnsley FC (Matchday 46; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-22 Bristol City FC v Preston North End FC (Matchday 46; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-22 Cardiff City FC v Hull City AFC (Matchday 46; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-22 Leeds United FC v Charlton Athletic FC (Matchday 46; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-22 Luton Town FC v Blackburn Rovers FC (Matchday 46; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-22 Millwall FC v Huddersfield Town AFC (Matchday 46; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-22 Nottingham Forest FC v Stoke City FC (Matchday 46; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-22 Reading FC v Swansea City AFC (Matchday 46; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-22 Sheffield Wednesday FC v Middlesbrough FC (Matchday 46; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-22 West Bromwich Albion FC v Queens Park Rangers FC (Matchday 46; earlier matchdays ~2020-06-30)
- en.2 2019-20 `date_inconsistent_with_round`: 2019-07-22 Wigan Athletic FC v Fulham FC (Matchday 46; earlier matchdays ~2020-06-30)

</details>

## Team names

| Raw name | Canonical name | Rows |
|---|---|---|
| Aston Villa | Aston Villa FC | 312 |
| Birmingham City | Birmingham City FC | 406 |
| Blackburn Rovers | Blackburn Rovers FC | 352 |
| Bolton Wanderers | Bolton Wanderers FC | 488 |
| Brighton & Hove Albion | Brighton & Hove Albion FC | 390 |
| Bristol City | Bristol City FC | 368 |
| Cardiff City | Cardiff City FC | 398 |
| Charlton Athletic | Charlton Athletic FC | 460 |
| Coventry City | Coventry City FC | 366 |
| Crystal Palace | Crystal Palace FC | 404 |
| Derby County | Derby County FC | 368 |
| Huddersfield Town | Huddersfield Town AFC | 490 |
| Hull City | Hull City AFC | 436 |
| Ipswich Town | Ipswich Town FC | 412 |
| Leeds United | Leeds United FC | 368 |
| Leicester City | Leicester City FC | 412 |
| Lincoln City | Lincoln City FC | 274 |
| Luton Town | Luton Town FC | 230 |
| Manchester City | Manchester City FC | 380 |
| Manchester United | Manchester United FC | 380 |
| Newcastle United | Newcastle United FC | 342 |
| Norwich City | Norwich City FC | 328 |
| Nottingham Forest | Nottingham Forest FC | 368 |
| Oxford United | Oxford United FC | 412 |
| Peterborough United | Peterborough United FC | 504 |
| Plymouth Argyle | Plymouth Argyle FC | 460 |
| Preston North End | Preston North End FC | 368 |
| Queens Park Rangers | Queens Park Rangers FC | 344 |
| Rotherham United | Rotherham United FC | 458 |
| Sheffield United | Sheffield United FC | 360 |
| Sheffield Wednesday | Sheffield Wednesday FC | 368 |
| Stoke City | Stoke City FC | 396 |
| Swansea City | Swansea City AFC | 404 |
| Tottenham Hotspur | Tottenham Hotspur FC | 380 |
| West Bromwich Albion | West Bromwich Albion FC | 396 |
| West Ham United | West Ham United FC | 388 |
| Wigan Athletic | Wigan Athletic FC | 482 |
| Wolverhampton Wanderers | Wolverhampton Wanderers FC | 336 |
| Wycombe Wanderers | Wycombe Wanderers FC | 458 |

Unknown names (add to `data/team_names/`): none

Suspected variants still present after mapping: none
