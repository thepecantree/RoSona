from dataclasses import dataclass
from typing import Literal


LastSeenSource = Literal[
    "official_presence_now",
    "rosona_observed",
    "third_party_observed",
    "asset_activity",
    "inventory_activity",
    "avatar_activity",
    "unknown",
]


@dataclass(frozen=True, slots=True)
class LastSeenSignal:
    user_id: int
    timestamp: str | None
    source: LastSeenSource
    confidence: float
    evidence: str | None = None


@dataclass(frozen=True, slots=True)
class LastSeenEstimate:
    user_id: int
    best_estimate: LastSeenSignal
    signals: list[LastSeenSignal]