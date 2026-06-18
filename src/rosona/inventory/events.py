from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InventoryEvent:
    user_id: int
    timestamp: str
    event_type: str
    description: str