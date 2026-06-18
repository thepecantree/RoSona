from __future__ import annotations

from datetime import UTC, datetime

from rosona.inventory.models import InventoryItem, InventorySnapshot
from rosona.inventory.rolimons import RolimonsCatalog
from rosona.inventory.store import InventorySnapshotStore
from rosona.roblox.client import RobloxClient


class InventoryService:
    def __init__(
        self,
        client: RobloxClient,
        rolimons: RolimonsCatalog,
        store: InventorySnapshotStore,
    ):
        self.client = client
        self.rolimons = rolimons
        self.store = store

    async def create_snapshot(self, user_id: int) -> InventorySnapshot:
        raw_items = await self.client.get_limited_inventory(user_id)

        items: list[InventoryItem] = []

        for raw_item in raw_items:
            asset_id = int(raw_item["assetId"])

            rap = raw_item.get("recentAveragePrice") or 0
            value = self.rolimons.get_item_value(asset_id)
            name = self.rolimons.get_item_name(asset_id)

            uaid = raw_item.get("userAssetId") or raw_item.get("instanceId")
            serial = raw_item.get("serialNumber")

            items.append(
                InventoryItem(
                    asset_id=asset_id,
                    name=name,
                    uaid=int(uaid) if uaid is not None else None,
                    serial=int(serial) if serial is not None else None,
                    rap=int(rap),
                    value=int(value),
                )
            )

        snapshot = InventorySnapshot(
            user_id=user_id,
            captured_at=datetime.now(UTC).isoformat(),
            total_rap=sum(item.rap for item in items),
            total_value=sum(item.value for item in items),
            items=items,
        )

        self.store.add_snapshot(snapshot)

        return snapshot

    def get_history(self, user_id: int) -> list[InventorySnapshot]:
        return self.store.get_snapshots(user_id)