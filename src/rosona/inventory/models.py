from dataclasses import dataclass
from typing import Literal


SnapshotVisibility = Literal[
    "public",
    "granted_access",
    "private_observed",
]

SnapshotRetention = Literal[
    "temporary",
    "permanent",
]


@dataclass(frozen=True, slots=True)
class InventoryItem:
    asset_id: int
    name: str
    uaid: int | None
    serial: int | None
    rap: int
    value: int


@dataclass(frozen=True, slots=True)
class InventorySnapshot:
    user_id: int
    captured_at: str

    visibility: SnapshotVisibility
    retention: SnapshotRetention

    total_rap: int
    total_value: int

    items: list[InventoryItem]

    @property
    def item_count(self) -> int:
        return len(self.items)

    @property
    def should_keep_full_snapshot(self) -> bool:
        return self.retention == "permanent"