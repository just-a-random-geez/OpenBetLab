"""A small command-line demonstration of OpenBetLab.

Examples (after installing the project):

    openbetlab demo
    openbetlab odds 2.5
    openbetlab parlay 2.0 1.8 3.1
    openbetlab joint 0.5 0.6

Nothing here connects to the internet, contacts a bookmaker or places a bet.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from openbetlab import __version__
from openbetlab.odds import bookmaker_margin, break_even_probability
from openbetlab.parlay import combined_decimal_odds, joint_probability_independent
from openbetlab.synthetic_data import load_synthetic_matches

DISCLAIMER = (
    "OpenBetLab is a research and education tool. It does not predict match "
    "outcomes and does not place bets."
)

INDEPENDENCE_WARNING = (
    "Note: this assumes the events are INDEPENDENT. It is wrong for related "
    "events, e.g. two outcomes from the same match."
)


def _percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def _cmd_odds(args: argparse.Namespace) -> None:
    odds = args.odds
    break_even = break_even_probability(odds)  # validates before printing anything
    print(f"Decimal odds:            {odds:.2f}")
    print(f"Break-even probability:  {_percent(break_even)}")
    print(
        "(If the true chance of winning is above this, the bet has positive "
        "expected value; below it, negative.)"
    )


def _cmd_parlay(args: argparse.Namespace) -> None:
    combined = combined_decimal_odds(args.odds)
    legs = " x ".join(f"{o:.2f}" for o in args.odds)
    print(f"Legs:                    {legs}")
    print(f"Combined decimal odds:   {combined:.2f}")
    print(f"Break-even probability:  {_percent(break_even_probability(combined))}")


def _cmd_joint(args: argparse.Namespace) -> None:
    joint = joint_probability_independent(args.probabilities)
    print(f"Joint probability:       {_percent(joint)}")
    print(INDEPENDENCE_WARNING)


def _cmd_demo(args: argparse.Namespace) -> None:
    matches = load_synthetic_matches()
    print("=" * 72)
    print("OpenBetLab demo, using SYNTHETIC (made-up) match data")
    print(DISCLAIMER)
    print("=" * 72)
    print()
    print("1) Break-even probability and bookmaker margin for each synthetic match")
    print()
    header = (
        f"{'Match':<40} {'Home':>7} {'Draw':>7} {'Away':>7} {'Margin':>7} {'Res':>4}"
    )
    print(header)
    print("-" * len(header))
    for m in matches:
        name = f"{m.home_team} v {m.away_team}"
        margin = bookmaker_margin([m.odds_home, m.odds_draw, m.odds_away])
        print(
            f"{name:<40} "
            f"{_percent(break_even_probability(m.odds_home)):>7} "
            f"{_percent(break_even_probability(m.odds_draw)):>7} "
            f"{_percent(break_even_probability(m.odds_away)):>7} "
            f"{_percent(margin):>7} "
            f"{m.result:>4}"
        )
    print()
    print("   Home/Draw/Away columns are break-even probabilities (1 / odds).")
    print("   Margin = how much the three add up to above 100%.")
    print()

    legs = matches[:3]
    print("2) Example parlay: home win in the first three synthetic matches")
    print()
    for m in legs:
        print(f"   {m.home_team:<20} @ {m.odds_home:.2f}")
    combined = combined_decimal_odds(m.odds_home for m in legs)
    print(f"   Combined decimal odds:  {combined:.2f}")
    print(f"   Break-even probability: {_percent(break_even_probability(combined))}")
    print()

    assumed = [0.45, 0.35, 0.55]
    print("3) Joint probability, using probabilities WE MADE UP for illustration")
    print()
    print(f"   Assumed probabilities: {', '.join(_percent(p) for p in assumed)}")
    joint = joint_probability_independent(assumed)
    print(f"   Joint probability:     {_percent(joint)}")
    print(f"   {INDEPENDENCE_WARNING}")
    print()
    print("All numbers above come from synthetic data or invented assumptions.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openbetlab",
        description=f"OpenBetLab command-line demo. {DISCLAIMER}",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser(
        "demo", help="walk through the calculations on synthetic data"
    )
    demo.set_defaults(func=_cmd_demo)

    odds = sub.add_parser("odds", help="show the break-even probability for odds")
    odds.add_argument("odds", type=float, help="decimal odds, e.g. 2.5")
    odds.set_defaults(func=_cmd_odds)

    parlay = sub.add_parser("parlay", help="combine the decimal odds of several legs")
    parlay.add_argument("odds", type=float, nargs="+", help="decimal odds of each leg")
    parlay.set_defaults(func=_cmd_parlay)

    joint = sub.add_parser(
        "joint", help="joint probability of independent events (see warning)"
    )
    joint.add_argument(
        "probabilities",
        type=float,
        nargs="+",
        help="probabilities between 0 and 1, e.g. 0.5 0.6",
    )
    joint.set_defaults(func=_cmd_joint)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI. Returns 0 on success and 2 on invalid input."""
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except (ValueError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
