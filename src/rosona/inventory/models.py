from dataclasses import dataclass


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

    total_rap: int
    total_value: int

    items: list[InventoryItem]