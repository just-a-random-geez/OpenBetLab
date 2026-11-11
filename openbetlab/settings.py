"""Project settings from config/settings.toml."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = ROOT / "config" / "settings.toml"


@dataclass(frozen=True)
class Settings:
    commission: float = 0.05
    early_snapshots_hours: tuple[float, ...] = (24, 2)
    fuzzy_min_score: float = 0.8
    disagreement_threshold: float = 0.10

    def __post_init__(self):
        if not 0 <= self.commission < 1:
            raise ValueError(f"commission must be in [0, 1), got {self.commission}")


def load_settings(path: Path = DEFAULT_PATH) -> Settings:
    data = tomllib.loads(Path(path).read_text()) if Path(path).exists() else {}
    bf, odds, cmp_ = data.get("betfair", {}), data.get("odds", {}), data.get("compare", {})
    return Settings(
        commission=float(bf.get("commission", Settings.commission)),
        early_snapshots_hours=tuple(float(h) for h in
                                    odds.get("early_snapshots_hours", Settings.early_snapshots_hours)),
        fuzzy_min_score=float(odds.get("fuzzy_min_score", Settings.fuzzy_min_score)),
        disagreement_threshold=float(cmp_.get("disagreement_threshold",
                                              Settings.disagreement_threshold)),
    )
