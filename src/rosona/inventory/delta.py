from __future__ import annotations

from dataclasses import dataclass

from rosona.inventory.models import InventoryItem, InventorySnapshot


@dataclass(frozen=True, slots=True)
class InventoryDelta:
    old_snapshot: InventorySnapshot
    new_snapshot: InventorySnapshot

    added_items: list[InventoryItem]
    removed_items: list[InventoryItem]
    retained_items: list[InventoryItem]

    rap_change: int
    value_change: int

    added_rap: int
    added_value: int

    removed_rap: int
    removed_value: int

    retained_rap_change: int
    retained_value_change: int

    @property
    def ownership_rap_flow(self) -> int:
        return self.added_rap - self.removed_rap

    @property
    def ownership_value_flow(self) -> int:
        return self.added_value - self.removed_value

    @property
    def market_rap_movement(self) -> int:
        return self.retained_rap_change

    @property
    def market_value_movement(self) -> int:
        return self.retained_value_change


def compare_snapshots(
    old_snapshot: InventorySnapshot,
    new_snapshot: InventorySnapshot,
) -> InventoryDelta:
    old_by_uaid = {
        item.uaid: item
        for item in old_snapshot.items
        if item.uaid is not None
    }

    new_by_uaid = {
        item.uaid: item
        for item in new_snapshot.items
        if item.uaid is not None
    }

    old_uaids = set(old_by_uaid)
    new_uaids = set(new_by_uaid)

    added_uaids = new_uaids - old_uaids
    removed_uaids = old_uaids - new_uaids
    retained_uaids = old_uaids & new_uaids

    added_items = [new_by_uaid[uaid] for uaid in added_uaids]
    removed_items = [old_by_uaid[uaid] for uaid in removed_uaids]
    retained_items = [new_by_uaid[uaid] for uaid in retained_uaids]

    retained_rap_change = sum(
        new_by_uaid[uaid].rap - old_by_uaid[uaid].rap
        for uaid in retained_uaids
    )

    retained_value_change = sum(
        new_by_uaid[uaid].value - old_by_uaid[uaid].value
        for uaid in retained_uaids
    )

    return InventoryDelta(
        old_snapshot=old_snapshot,
        new_snapshot=new_snapshot,
        added_items=added_items,
        removed_items=removed_items,
        retained_items=retained_items,
        rap_change=new_snapshot.total_rap - old_snapshot.total_rap,
        value_change=new_snapshot.total_value - old_snapshot.total_value,
        added_rap=sum(item.rap for item in added_items),
        added_value=sum(item.value for item in added_items),
        removed_rap=sum(item.rap for item in removed_items),
        removed_value=sum(item.value for item in removed_items),
        retained_rap_change=retained_rap_change,
        retained_value_change=retained_value_change,
    )