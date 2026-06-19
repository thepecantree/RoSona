from __future__ import annotations

from rosona.inventory.models import InventorySnapshot
from rosona.inventory.pseudo import PseudoInventoryItem
from rosona.inventory.pseudo_service import PseudoInventoryService
from rosona.inventory.rolimons import RolimonsCatalog
from rosona.roblox.client import RobloxClient


class CollectionLimitedScanner:
    def __init__(
        self,
        client: RobloxClient,
        rolimons: RolimonsCatalog,
        pseudo_inventory: PseudoInventoryService,
    ):
        self.client = client
        self.rolimons = rolimons
        self.pseudo_inventory = pseudo_inventory

    async def scan_collection_limiteds(
        self,
        user_id: int,
        public_snapshot: InventorySnapshot | None = None,
    ) -> list[PseudoInventoryItem]:
        collection_items = await self.client.get_user_collections(user_id)

        publicly_confirmed_asset_ids: set[int] = set()

        if public_snapshot is not None:
            publicly_confirmed_asset_ids = {
                item.asset_id
                for item in public_snapshot.items
            }

        observed: list[PseudoInventoryItem] = []

        for item in collection_items:
            asset = item.get("asset") or item
            asset_id = int(asset["id"])

            if not self.rolimons.is_limited(asset_id):
                continue

            if asset_id in publicly_confirmed_asset_ids:
                continue

            observed_item = self.pseudo_inventory.observe_collection_limited(
                user_id=user_id,
                asset_id=asset_id,
                uaid=None,
            )

            observed.append(observed_item)

        return observed