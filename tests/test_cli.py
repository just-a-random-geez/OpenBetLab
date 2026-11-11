import pytest

from openbetlab import __version__
from openbetlab.cli import main


def test_odds_command(capsys):
    assert main(["odds", "2.5"]) == 0
    out = capsys.readouterr().out
    assert "40.00%" in out


def test_parlay_command(capsys):
    assert main(["parlay", "2.0", "1.5", "3.0"]) == 0
    out = capsys.readouterr().out
    assert "9.00" in out
    assert "11.11%" in out


def test_joint_command_shows_independence_warning(capsys):
    assert main(["joint", "0.5", "0.6"]) == 0
    out = capsys.readouterr().out
    assert "30.00%" in out
    assert "INDEPENDENT" in out


def test_demo_command_mentions_synthetic_data(capsys):
    assert main(["demo"]) == 0
    out = capsys.readouterr().out
    assert "SYNTHETIC" in out
    assert "does not predict" in out
    assert "Synthetic Rovers" in out


@pytest.mark.parametrize(
    "argv",
    [["odds", "1.0"], ["odds", "-2"], ["parlay", "2.0", "0.5"], ["joint", "1.5"]],
)
def test_invalid_input_returns_error_code(argv, capsys):
    assert main(argv) == 2
    captured = capsys.readouterr()
    assert "Error:" in captured.err
    assert captured.out == ""  # no half-finished output before the error


def test_non_numeric_input_is_rejected_by_argparse(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["odds", "abc"])
    assert exc.value.code == 2


def test_version_flag(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_version_matches_installed_package_metadata():
    from importlib.metadata import version

    assert __version__ == version("openbetlab")
