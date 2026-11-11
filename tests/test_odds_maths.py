import pytest

from openbetlab.odds.probabilities import (implied_probability, overround,
                                           remove_margin_proportional)
from openbetlab.odds.profit import (Bet, apply_commission, back_profit, breakeven_probability,
                                    lay_profit, market_profit)
from openbetlab.settings import Settings, load_settings


def test_implied_and_overround():
    assert implied_probability(2.0) == 0.5
    assert overround([2.0, 3.5, 4.0]) == pytest.approx(0.5 + 1 / 3.5 + 0.25 - 1)
    with pytest.raises(ValueError):
        implied_probability(1.0)


def test_proportional_margin_removal():
    odds = [1.8, 3.6, 4.5]   # implied 0.5556 + 0.2778 + 0.2222 = 1.0556
    fair = remove_margin_proportional(odds)
    assert sum(fair) == pytest.approx(1)
    assert fair == pytest.approx([0.5556 / 1.0556, 0.2778 / 1.0556, 0.2222 / 1.0556], abs=1e-4)
    # ratios between outcomes are kept
    assert fair[0] / fair[1] == pytest.approx(3.6 / 1.8)


def test_negative_overround_is_scaled_up():
    fair = remove_margin_proportional([2.2, 3.8, 4.4])   # sums to < 1
    assert overround([2.2, 3.8, 4.4]) < 0 and sum(fair) == pytest.approx(1)


def test_back_and_lay_profit_with_commission():
    assert back_profit(3.0, 10, True, 0.05) == pytest.approx(19.0)    # 20 * 0.95
    assert back_profit(3.0, 10, False, 0.05) == -10
    assert lay_profit(3.0, 10, False, 0.05) == pytest.approx(9.5)     # keep backer's 10, less 5%
    assert lay_profit(3.0, 10, True, 0.05) == -20                      # pay out 10 * (3-1)
    assert back_profit(3.0, 10, True, 0.0) == 20


def test_commission_is_on_net_market_winnings():
    bets = [Bet("home", "back", 2.0, 10), Bet("away", "back", 4.0, 5)]
    # home wins: +10 - 5 = +5 net -> 5 * 0.98
    assert market_profit(bets, "home", 0.02) == pytest.approx(4.9)
    # draw: -10 - 5 = -15 -> no commission on a loss
    assert market_profit(bets, "draw", 0.02) == -15
    assert apply_commission(-3, 0.05) == -3


def test_breakeven_probability():
    assert breakeven_probability(2.0, 0.0) == pytest.approx(0.5)
    assert breakeven_probability(2.0, 0.05) == pytest.approx(1 / 1.95)
    p = breakeven_probability(3.4, 0.05)
    assert p * 2.4 * 0.95 == pytest.approx(1 - p)   # expected profit exactly zero


@pytest.mark.parametrize("args", [(1.0, 10, True, 0.05), (2.0, -1, True, 0.05),
                                  (2.0, 10, True, 1.0), (2.0, 10, True, -0.1)])
def test_invalid_inputs(args):
    with pytest.raises(ValueError):
        back_profit(*args)


def test_bet_side_validated():
    with pytest.raises(ValueError):
        Bet("home", "sideways", 2.0, 1).gross_profit("home")


def test_settings_file(tmp_path):
    p = tmp_path / "s.toml"
    p.write_text("[betfair]\ncommission = 0.02\n[odds]\nearly_snapshots_hours = [48, 1]\n")
    s = load_settings(p)
    assert s.commission == 0.02 and s.early_snapshots_hours == (48.0, 1.0)
    assert load_settings(tmp_path / "missing.toml") == Settings()
    with pytest.raises(ValueError):
        Settings(commission=1.5)


def test_repo_settings_load():
    s = load_settings()
    assert 0 <= s.commission < 1
