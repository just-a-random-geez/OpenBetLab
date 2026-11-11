"""Team-name mapping: every spelling of a club -> one canonical name.

The mapping lives in CSV files under ``data/team_names/`` with columns
``raw_name,canonical_name``. Every known spelling is listed, including the
canonical spelling itself, so a name that is *not* in the file is a genuinely
new/unknown team and gets reported instead of silently passing through.
"""

from __future__ import annotations

import csv
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# Legal-form words that clubs add or drop ("Stoke City" vs "Stoke City FC").
# Used only to *detect* suspicious variants, never to rename automatically.
_LEGAL_FORM_TOKENS = {
    "fc", "afc", "cf", "sc", "ac", "bc", "cd", "ud", "rc", "ss", "as", "us",
    "ssc", "sv", "fk", "sk", "the", "club",
}


def normalize_whitespace(name: str) -> str:
    """Unicode-normalise (NFC), trim and collapse internal whitespace."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", name)).strip()


def variant_key(name: str) -> str:
    """Loose key: lowercase, no accents/punctuation, no legal-form words."""
    ascii_name = (
        unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    )
    tokens = re.sub(r"[^a-z0-9 ]", " ", ascii_name).split()
    return " ".join(t for t in tokens if t not in _LEGAL_FORM_TOKENS)


def find_suspected_variants(names: Iterable[str]) -> list[list[str]]:
    """Groups of distinct names that look like the same club.

    After mapping, this should return nothing; any group means the mapping
    file needs a new row.
    """
    groups: dict[str, set[str]] = {}
    for n in names:
        groups.setdefault(variant_key(n), set()).add(n)
    return sorted(sorted(g) for g in groups.values() if len(g) > 1)


@dataclass
class TeamNameMapper:
    mapping: dict[str, str]
    unknown: set[str] = field(default_factory=set)

    @classmethod
    def from_csv_dir(cls, directory: Path) -> "TeamNameMapper":
        mapping: dict[str, str] = {}
        for path in sorted(Path(directory).glob("*.csv")):
            with path.open(newline="", encoding="utf-8") as fh:
                for row in csv.DictReader(fh):
                    raw = normalize_whitespace(row["raw_name"])
                    canon = normalize_whitespace(row["canonical_name"])
                    if raw in mapping and mapping[raw] != canon:
                        raise ValueError(
                            f"{path.name}: '{raw}' mapped to both "
                            f"'{mapping[raw]}' and '{canon}'"
                        )
                    mapping[raw] = canon
        # Canonical names must map to themselves, otherwise chains appear.
        for canon in set(mapping.values()):
            if mapping.get(canon, canon) != canon:
                raise ValueError(f"canonical name '{canon}' is itself remapped")
        return cls(mapping)

    def canonical(self, raw_name: str) -> str:
        """Canonical name; unknown names are kept as-is and remembered."""
        name = normalize_whitespace(raw_name)
        if name in self.mapping:
            return self.mapping[name]
        self.unknown.add(name)
        return name
