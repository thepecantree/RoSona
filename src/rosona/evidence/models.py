from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


EvidenceTier = Literal[
    "external_reference",
    "runtime_state",
    "observed_inference",
    "granted_access",
    "risk_conclusion",
]

RetentionPolicy = Literal[
    "do_not_persist",
    "latest_only",
    "persist_meaningful",
    "persist_full",
    "persist_cautiously",
]


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    tier: EvidenceTier
    retention: RetentionPolicy
    source: str
    summary: str
    observed_at: str | None = None
    confidence: float | None = None
    user_id: int | None = None
    asset_id: int | None = None
    uaid: int | None = None