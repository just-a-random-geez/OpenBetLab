"""Monte Carlo risk simulation of the betting strategy.

A "season" is a fixed list of betting opportunities (matches with model probabilities,
market fair probabilities and the pick-time odds). Bets are chosen by the strategy using
the MODEL's probabilities and the odds - exactly like the backtest. Only the match results
are random: each simulated season draws every result again from a "truth":

- truth = "model":  results follow the model's probabilities (optionally the model is
  ``overconfidence`` too optimistic about the outcomes it bets on);
- truth = "market": results follow the market's fair probabilities.

This measures RISK (spread of outcomes, drawdowns, ruin) under an ASSUMED truth.
It cannot show that an edge exists: under "model" truth the edge is assumed, not proven.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field, replace

import numpy as np

SEED = 20261111
MIN_STAKE = 1.0   # GBP; Betfair minimum. Smaller stakes are raised to this.
                  # Bankroll below this = ruin (can't bet any more).


@dataclass(frozen=True)
class Opportunity:
    date: str
    model: tuple[float, float, float]
    market: tuple[float, float, float]     # fair (margin-free) probabilities
    odds: tuple[float, float, float]       # price available at pick time


@dataclass(frozen=True)
class Scenario:
    name: str
    truth: str = "model"                   # "model" or "market"
    staking: str = "flat"                  # "flat" or "kelly"
    kelly_fraction: float = 0.25
    rollover: bool = False                 # stakes sized on CURRENT bankroll (compounding)
    parlay_legs: int = 1                   # 1 = singles
    min_odds: float = 1.50
    max_odds: float = 5.00
    min_edge: float = 0.05                 # after commission, by the model's own numbers
    overconfidence: float = 0.0            # true p of a backed outcome = model p x (1 - this)
    commission: float = 0.05
    start_bankroll: float = 100.0
    flat_stake: float = 1.0                # GBP (no rollover) or share of bankroll x 100

    def __post_init__(self):
        if self.truth not in ("model", "market") or self.staking not in ("flat", "kelly"):
            raise ValueError("bad scenario")
        if not 1 <= self.parlay_legs <= 4 or not 0 <= self.overconfidence < 1:
            raise ValueError("bad scenario")


@dataclass
class PlannedBet:
    day: int
    legs: list[tuple[int, float]]          # (match index, TRUE win probability of the leg)
    odds: float
    model_p: float                         # model's win probability for the whole bet


def edge_after_commission(p, odds, c):
    return p * (odds - 1) * (1 - c) - (1 - p)


def kelly_fraction(p: float, odds: float, commission: float) -> float:
    """Full-Kelly share of bankroll for a back bet, using net odds after commission."""
    b = (odds - 1) * (1 - commission)
    return max(0.0, (p * b - (1 - p)) / b)


def plan_bets(opps: list[Opportunity], sc: Scenario) -> list[PlannedBet]:
    """Pick at most one outcome per match (largest qualifying edge), then group same-day
    picks into parlays of ``parlay_legs`` (highest edges first; leftovers not bet)."""
    days = {d: i for i, d in enumerate(sorted({o.date for o in opps}))}
    by_day: dict[int, list] = defaultdict(list)
    for idx, o in enumerate(opps):
        best = None
        for k in range(3):
            if not sc.min_odds <= o.odds[k] <= sc.max_odds:
                continue
            e = edge_after_commission(o.model[k], o.odds[k], sc.commission)
            if e >= sc.min_edge and (best is None or e > best[0]):
                best = (e, k)
        if best is None:
            continue
        e, k = best
        if sc.truth == "model":
            true_p = o.model[k] * (1 - sc.overconfidence)
        else:
            true_p = o.market[k]
        by_day[days[o.date]].append((e, idx, true_p, o.odds[k], o.model[k]))
    planned = []
    for day in sorted(by_day):
        picks = sorted(by_day[day], key=lambda x: -x[0])
        n = sc.parlay_legs
        for g in range(0, len(picks) - n + 1, n):
            group = picks[g:g + n]
            planned.append(PlannedBet(day, [(x[1], x[2]) for x in group],
                                      float(np.prod([x[3] for x in group])),
                                      float(np.prod([x[4] for x in group]))))
    return planned


def uniforms(match_indices, n_seasons: int, seed: int = SEED) -> dict[int, np.ndarray]:
    """One column of uniforms per match, generated from (seed, match index) only - so a
    match's simulated results are identical in every scenario (fair comparisons) and
    reproducible regardless of which scenarios are run."""
    return {m: np.random.default_rng([seed, m]).random(n_seasons) for m in match_indices}


@dataclass
class ScenarioResult:
    scenario: Scenario
    bets_per_season: int
    final: np.ndarray = field(repr=False)        # final bankroll per season
    max_dd_pct: np.ndarray = field(repr=False)   # worst drawdown per season (share of peak)
    lost_half: np.ndarray = field(repr=False)    # bankroll ever <= 50% of start
    ruined: np.ndarray = field(repr=False)       # bankroll ever < minimum stake

    def summary(self) -> dict:
        start = self.scenario.start_bankroll
        p5, p50, p95 = np.percentile(self.final, [5, 50, 95])
        return {"bets": self.bets_per_season, "median": p50 - start, "p5": p5 - start,
                "p95": p95 - start, "p_lose_half": float(self.lost_half.mean()),
                "p_ruin": float(self.ruined.mean()),
                "median_max_dd": float(np.median(self.max_dd_pct)),
                "p_profit": float((self.final > start).mean())}


def simulate(opps: list[Opportunity], sc: Scenario, n_seasons: int = 10_000,
             seed: int = SEED) -> ScenarioResult:
    bets = plan_bets(opps, sc)
    used = sorted({m for b in bets for m, _ in b.legs})
    u = uniforms(used, n_seasons, seed)
    start = sc.start_bankroll
    bank = np.full(n_seasons, start)
    peak = bank.copy()
    max_dd = np.zeros(n_seasons)
    lost_half = np.zeros(n_seasons, bool)
    ruined = np.zeros(n_seasons, bool)

    by_day: dict[int, list[PlannedBet]] = defaultdict(list)
    for b in bets:
        by_day[b.day].append(b)
    for day in sorted(by_day):
        day_bets = by_day[day]
        base = bank if sc.rollover else np.full(n_seasons, start)
        # Betfair's minimum stake is £1: any wanted stake below £1 is raised to £1. Bets are
        # placed in edge order while the money not yet committed today still covers them;
        # the rest of the day's bets are not placed.
        committed = np.zeros(n_seasons)
        stakes = []
        for b in day_bets:
            if sc.staking == "flat":
                s = base * (sc.flat_stake / 100) if sc.rollover else np.full(n_seasons, sc.flat_stake)
            else:
                s = base * sc.kelly_fraction * kelly_fraction(b.model_p, b.odds, sc.commission)
            s = np.maximum(s, MIN_STAKE)
            s = np.where(bank - committed >= s, s, 0.0)
            committed += s
            stakes.append(s)
        for b, s in zip(day_bets, stakes):
            won = np.ones(n_seasons, bool)
            for m, tp in b.legs:
                won &= u[m] < tp
            bank = bank + np.where(won, s * (b.odds - 1) * (1 - sc.commission), -s)
        peak = np.maximum(peak, bank)
        max_dd = np.maximum(max_dd, (peak - bank) / peak)
        lost_half |= bank <= 0.5 * start
        ruined |= bank < MIN_STAKE
    return ScenarioResult(sc, len(bets), bank, max_dd, lost_half, ruined)


def default_scenarios() -> list[Scenario]:
    """One-change-at-a-time around a base case (the research-plan rules), for each truth."""
    out = []
    for truth in ("market", "model"):    # no-edge case first: it is the sober baseline
        b = Scenario(f"{truth}: base (flat £1, singles, odds 1.5-5)", truth=truth)
        out += [
            b,
            replace(b, name=f"{truth}: flat 1% of bankroll, rollover", rollover=True),
            replace(b, name=f"{truth}: Kelly 25%, no rollover", staking="kelly"),
            replace(b, name=f"{truth}: Kelly 25%, rollover", staking="kelly", rollover=True),
            replace(b, name=f"{truth}: Kelly 50%, rollover", staking="kelly",
                    kelly_fraction=0.5, rollover=True),
            *(replace(b, name=f"{truth}: parlay {n} legs", parlay_legs=n) for n in (2, 3, 4)),
            replace(b, name=f"{truth}: odds 1.5-3.0", max_odds=3.0),
            replace(b, name=f"{truth}: odds 2.0-10.0", min_odds=2.0, max_odds=10.0),
        ]
        if truth == "model":
            out += [replace(b, name=f"model {d:.0%} overconfident", overconfidence=d)
                    for d in (0.02, 0.05)]
            out += [replace(b, name=f"model {d:.0%} overconfident, Kelly 25% rollover",
                            overconfidence=d, staking="kelly", rollover=True)
                    for d in (0.02, 0.05)]
    return out


def synthetic_season(n_matches: int = 2000, seed: int = 7) -> list[Opportunity]:
    """ILLUSTRATION ONLY - not real data. Market fair probabilities look like English
    league football; exchange prices carry ~1% overround; the model = market + noise
    (so the model often 'disagrees' with the market)."""
    rng = np.random.default_rng(seed)
    out = []
    day = 0
    for i in range(n_matches):
        strength = rng.normal(0, 0.6)
        draw = np.clip(0.27 - 0.05 * abs(strength), 0.18, 0.30)
        home = (1 - draw) / (1 + np.exp(-(strength + 0.25)))
        market = np.array([home, draw, 1 - draw - home])
        noise = np.exp(rng.normal(0, 0.12, 3))
        model = market * noise / (market * noise).sum()
        odds = np.round(1 / (market * 1.01), 2)
        if i % 30 == 0:
            day += 1
        out.append(Opportunity(f"d{day:04d}", tuple(model), tuple(market), tuple(odds)))
    return out
