from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PseudoInventorySource = Literal[
    "wearing_avatar",
    "profile_collection",
    "rolimons_hidden_owner_inference",
    "granted_access",
]


OwnershipConfidence = Literal[
    "confirmed_at_observation",
    "strong_inference",
    "inferred_interval",
]


@dataclass(frozen=True, slots=True)
class PseudoInventoryItem:
    user_id: int
    asset_id: int
    uaid: int | None
    observed_at: str
    source: PseudoInventorySource
    confidence: OwnershipConfidence
    evidence: str


@dataclass(frozen=True, slots=True)
class OwnershipInterval:
    user_id: int
    uaid: int
    asset_id: int

    known_owned_after: str | None
    known_not_owned_after: str | None

    source: PseudoInventorySource
    confidence: OwnershipConfidence
    evidence: str