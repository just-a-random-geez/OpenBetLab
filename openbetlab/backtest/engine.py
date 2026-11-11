"""Walk-forward betting backtest.

For each match date d (in order):
1. the model is refitted on matches played on dates BEFORE d (walk_forward);
2. for each match on d, the pick uses the Betfair price at the plan's pick snapshot
   (e.g. 2h before kick-off), whose trade time must be before kick-off. The closing price
   is never used to make a pick - only afterwards, to measure closing-line value (CLV);
3. bets are settled with the actual result and Betfair commission.

All rules come from ``PlanRules`` (mirrors docs/RESEARCH_PLAN_v1.md).
"""

from __future__ import annotations

import datetime as dt
import itertools
from dataclasses import dataclass, field
from typing import Callable

from openbetlab.evaluation.data import Result
from openbetlab.odds.profit import back_profit

SEL = ("home", "draw", "away")
_OUT = {"H": "home", "D": "draw", "A": "away"}


@dataclass(frozen=True)
class PlanRules:
    """Strategy rules. Must match docs/RESEARCH_PLAN_v1.md (a test checks this)."""
    model: str = "poisson"
    pick_snapshot: str = "2h"
    close_snapshot: str = "close"
    min_edge: float = 0.05            # after commission
    min_odds: float = 1.50
    max_odds: float = 5.00
    commission: float = 0.05
    stake: float = 1.0                # GBP per bet (flat)
    start_bankroll: float = 100.0     # GBP, virtual
    parlays: bool = False             # plan v1: singles only
    parlay_legs: int = 2
    max_price_age_minutes: float = 60  # pick price must have traded within this before pick time
    price_haircut_ticks: int = 0      # sensitivity only: take the price N Betfair ticks worse

    @property
    def pick_hours(self) -> float:
        """'2h' -> 2.0: pick time = kick-off minus this."""
        return float(self.pick_snapshot.rstrip("h"))

    def __post_init__(self):
        if self.pick_snapshot == self.close_snapshot:
            raise ValueError("picks must not use the closing price")
        if not 0 <= self.commission < 1 or self.stake <= 0 or self.min_odds <= 1:
            raise ValueError("invalid rules")


@dataclass(frozen=True)
class Snapshot:
    odds: tuple[float, float, float]
    fair: tuple[float, float, float]
    times: tuple[str | None, str | None, str | None]   # trade time per selection (UTC ISO)


@dataclass(frozen=True)
class MarketPrices:
    kickoff_utc: str
    snapshots: dict      # snapshot label -> Snapshot


def edge_after_commission(p: float, odds: float, commission: float) -> float:
    return p * (odds - 1) * (1 - commission) - (1 - p)


@dataclass
class Bet:
    date: str
    kickoff_utc: str
    league: str
    match: str
    selection: str
    model_prob: float
    odds: float
    edge: float
    result: str               # what happened: home / draw / away
    won: bool
    profit: float             # GBP after commission
    close_odds: float | None
    clv: float | None         # odds taken x fair closing probability - 1


@dataclass
class Parlay:
    date: str
    legs: list[Bet]
    odds: float
    won: bool
    profit: float


@dataclass
class BacktestResult:
    bets: list[Bet]
    parlays: list[Parlay] = field(default_factory=list)
    skipped: dict = field(default_factory=dict)


def _utc(t: str) -> dt.datetime:
    d = dt.datetime.fromisoformat(t)
    return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)   # no zone given -> UTC


# Betfair price ladder: (upper bound of band, tick size)
_LADDER = [(2, 0.01), (3, 0.02), (4, 0.05), (6, 0.1), (10, 0.2), (20, 0.5), (30, 1),
           (50, 2), (100, 5), (1000, 10)]


def tick_down(odds: float, n: int = 1) -> float:
    """Price n ticks lower on the Betfair ladder (a worse price for a backer)."""
    for _ in range(n):
        step = next(t for upper, t in _LADDER if odds <= upper + 1e-9)
        odds = round(max(odds - step, 1.01), 2)
    return odds


def price_problem(snap: Snapshot, kickoff_utc: str, match_date: str,
                  rules: PlanRules) -> str | None:
    """Why this pick-time price can't be used, or None if it can.

    - all three prices must exist (the plan requires a complete price);
    - a price traded at/after kick-off is an error (it would be in-play information);
    - every price must have traded within ``max_price_age_minutes`` before the pick time
      (a stale last-traded price was not really available);
    - the pick time must be on the match day (UK time): the model knows every result
      dated before that day, so picking earlier would use results not yet played.
    """
    from zoneinfo import ZoneInfo
    if any(o is None for o in snap.odds) or any(t is None for t in snap.times):
        return "incomplete pick-time price"
    ko = _utc(kickoff_utc)
    pick_time = ko - dt.timedelta(hours=rules.pick_hours)
    for t in snap.times:
        if _utc(t) >= ko:
            raise ValueError(f"pick price traded at {t}, not before kick-off {kickoff_utc}")
        if _utc(t) < pick_time - dt.timedelta(minutes=rules.max_price_age_minutes):
            return "stale pick-time price"
    if pick_time.astimezone(ZoneInfo("Europe/London")).date().isoformat() < match_date:
        return "pick time before the model's knowledge cut-off"
    return None


def choose_bet(probs, snap: Snapshot, kickoff_utc: str, rules: PlanRules):
    """Best qualifying back bet for one match, or None. Call ``price_problem`` first.
    Prices traded at/after kick-off are rejected outright."""
    ko = _utc(kickoff_utc)
    best = None
    for i, sel in enumerate(SEL):
        o, t = snap.odds[i], snap.times[i]
        if o is None or t is None:
            continue
        if _utc(t) >= ko:
            raise ValueError(f"pick price traded at {t}, not before kick-off {kickoff_utc}")
        o = tick_down(o, rules.price_haircut_ticks)
        if not rules.min_odds <= o <= rules.max_odds:
            continue
        e = edge_after_commission(probs[i], o, rules.commission)
        if e >= rules.min_edge and (best is None or e > best[2]):
            best = (sel, o, e, probs[i])
    return best


Forecaster = Callable[[list[Result], list[Result]], list]


def run_backtest(history: list[Result], targets: list[Result],
                 prices: dict[tuple, MarketPrices], forecaster: Forecaster,
                 rules: PlanRules) -> BacktestResult:
    """``forecaster(history, targets)`` must return walk-forward forecasts aligned with
    targets (each made from matches on earlier dates only), e.g. models.poisson.walk_forward."""
    probs = forecaster(history, targets)
    skipped = {"no market": 0, "no pick-snapshot price": 0, "incomplete pick-time price": 0,
               "stale pick-time price": 0, "pick time before the model's knowledge cut-off": 0,
               "no qualifying bet": 0}
    bets: list[Bet] = []
    for m, p in zip(targets, probs):
        key = (m.league, m.season, m.date, m.home_team, m.away_team)
        mp = prices.get(key)
        if mp is None:
            skipped["no market"] += 1
            continue
        snap = mp.snapshots.get(rules.pick_snapshot)
        if snap is None or all(o is None for o in snap.odds):
            skipped["no pick-snapshot price"] += 1
            continue
        problem = price_problem(snap, mp.kickoff_utc, m.date, rules)
        if problem:
            skipped[problem] += 1
            continue
        pick = choose_bet(p, snap, mp.kickoff_utc, rules)
        if pick is None:
            skipped["no qualifying bet"] += 1
            continue
        sel, odds, e, prob = pick
        result = _OUT[m.outcome]
        won = result == sel
        close = mp.snapshots.get(rules.close_snapshot)
        i = SEL.index(sel)
        close_odds = close.odds[i] if close else None
        clv = odds * close.fair[i] - 1 if close and close.fair[i] is not None else None
        bets.append(Bet(m.date, mp.kickoff_utc, m.league, f"{m.home_team} v {m.away_team}", sel,
                        prob, odds, e, result, won,
                        back_profit(odds, rules.stake, won, rules.commission), close_odds, clv))
    bets.sort(key=lambda b: (b.kickoff_utc, b.match))
    parlays = build_parlays(bets, rules) if rules.parlays else []
    return BacktestResult(bets, parlays, skipped)


def build_parlays(bets: list[Bet], rules: PlanRules) -> list[Parlay]:
    """HYPOTHETICAL multiples (the Betfair Exchange has none): per date, one
    ``parlay_legs``-fold from the highest-edge single bets that each passed the rule.
    Commission is applied to the multiple's net winnings."""
    out = []
    for date, day in itertools.groupby(sorted(bets, key=lambda b: b.date), key=lambda b: b.date):
        legs = sorted(day, key=lambda b: -b.edge)[:rules.parlay_legs]
        if len(legs) < rules.parlay_legs:
            continue
        odds = 1.0
        for b in legs:
            odds *= b.odds
        won = all(b.won for b in legs)
        profit = rules.stake * (odds - 1) * (1 - rules.commission) if won else -rules.stake
        out.append(Parlay(date, legs, odds, won, profit))
    return out
