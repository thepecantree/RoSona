from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


EventType = Literal[
    "item_added",
    "item_removed",
    "item_observed",
    "item_publicly_confirmed",
]


EventSource = Literal[
    "inventory_snapshot",
    "pseudo_inventory",
    "rolimons_history",
    "granted_access",
]


@dataclass(frozen=True, slots=True)
class OwnershipEvent:
    timestamp: str

    event_type: EventType
    source: EventSource

    user_id: int

    asset_id: int
    uaid: int | None

    evidence: str