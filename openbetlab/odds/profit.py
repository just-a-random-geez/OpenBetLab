"""Profit and loss on the Betfair exchange, with commission.

Betfair charges commission on your NET winnings in each market (all your bets on that
market added together), only when that net amount is positive. Losses are not refunded
and pay no commission. The rate is a required argument everywhere - take it from
``openbetlab.settings.load_settings().commission``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


def _check(odds: float, stake: float, commission: float) -> None:
    if odds <= 1:
        raise ValueError(f"decimal odds must be > 1, got {odds}")
    if stake < 0:
        raise ValueError(f"stake must be >= 0, got {stake}")
    if not 0 <= commission < 1:
        raise ValueError(f"commission must be in [0, 1), got {commission}")


@dataclass(frozen=True)
class Bet:
    selection: str     # "home", "draw" or "away"
    side: str          # "back" (bet for) or "lay" (bet against)
    odds: float        # decimal odds matched
    stake: float       # backer's stake (for a lay: the backer's stake you accept)

    def gross_profit(self, winner: str) -> float:
        """Profit before commission given the winning selection."""
        _check(self.odds, self.stake, 0)
        won_selection = self.selection == winner
        if self.side == "back":
            return self.stake * (self.odds - 1) if won_selection else -self.stake
        if self.side == "lay":
            return -self.stake * (self.odds - 1) if won_selection else self.stake
        raise ValueError(f"side must be 'back' or 'lay', got {self.side!r}")


def apply_commission(net: float, commission: float) -> float:
    """Commission is taken only from positive net market winnings."""
    if not 0 <= commission < 1:
        raise ValueError(f"commission must be in [0, 1), got {commission}")
    return net * (1 - commission) if net > 0 else net


def market_profit(bets: Iterable[Bet], winner: str, commission: float) -> float:
    """Net profit for all bets on ONE market after commission."""
    return apply_commission(sum(b.gross_profit(winner) for b in bets), commission)


def back_profit(odds: float, stake: float, won: bool, commission: float) -> float:
    """Single back bet: win -> stake*(odds-1) less commission; lose -> -stake."""
    _check(odds, stake, commission)
    return stake * (odds - 1) * (1 - commission) if won else -stake


def lay_profit(odds: float, stake: float, selection_won: bool, commission: float) -> float:
    """Single lay bet: selection loses -> +stake less commission; wins -> -stake*(odds-1)."""
    _check(odds, stake, commission)
    return -stake * (odds - 1) if selection_won else stake * (1 - commission)


def breakeven_probability(odds: float, commission: float) -> float:
    """Win probability at which a back bet at these odds breaks even after commission.

    p*(odds-1)*(1-c) = (1-p)  ->  p = 1 / (1 + (odds-1)*(1-c))
    """
    _check(odds, 1, commission)
    return 1 / (1 + (odds - 1) * (1 - commission))
