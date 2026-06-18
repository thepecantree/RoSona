from __future__ import annotations

from rosona.inventory.models import InventorySnapshot
from rosona.inventory.pseudo import PseudoInventoryItem
from rosona.inventory.pseudo_service import PseudoInventoryService
from rosona.inventory.rolimons import RolimonsCatalog
from rosona.roblox.client import RobloxClient


class AvatarLimitedScanner:
    def __init__(
        self,
        client: RobloxClient,
        rolimons: RolimonsCatalog,
        pseudo_inventory: PseudoInventoryService,
    ):
        self.client = client
        self.rolimons = rolimons
        self.pseudo_inventory = pseudo_inventory

    async def scan_worn_limiteds(
        self,
        user_id: int,
        public_snapshot: InventorySnapshot | None = None,
    ) -> list[PseudoInventoryItem]:
        assets = await self.client.get_avatar_assets(user_id)

        publicly_confirmed_asset_ids: set[int] = set()

        if public_snapshot is not None:
            publicly_confirmed_asset_ids = {
                item.asset_id
                for item in public_snapshot.items
            }

        observed: list[PseudoInventoryItem] = []

        for asset in assets:
            asset_id = int(asset["id"])

            if not self.rolimons.is_limited(asset_id):
                continue

            if asset_id in publicly_confirmed_asset_ids:
                continue

            item = self.pseudo_inventory.observe_worn_limited(
                user_id=user_id,
                asset_id=asset_id,
                uaid=None,
            )

            observed.append(item)

        return observed