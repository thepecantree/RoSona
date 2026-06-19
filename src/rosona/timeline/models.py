from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


TimelineSource = Literal[
    "public_inventory",
    "pseudo_inventory",
    "rolimons_history",
    "granted_access",
]


TimelineConfidence = Literal[
    "confirmed",
    "strong_inference",
    "weak_inference",
]


SegmentStatus = Literal[
    "open",
    "closed",
    "unknown",
]


@dataclass(frozen=True, slots=True)
class OwnershipSegment:
    user_id: int
    asset_id: int
    uaid: int | None

    started_at: str | None
    ended_at: str | None

    source: TimelineSource
    confidence: TimelineConfidence
    evidence: str

    status: SegmentStatus = "unknown"


@dataclass(frozen=True, slots=True)
class OwnershipTimeline:
    asset_id: int
    uaid: int | None
    segments: list[OwnershipSegment]