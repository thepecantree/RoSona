from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OwnershipInterval:
    user_id: int
    asset_id: int
    uaid: int | None

    started_at: str | None
    ended_at: str | None

    source: str
    confidence: str
    status: str
    evidence: str

    @property
    def is_open(self) -> bool:
        return self.ended_at is None