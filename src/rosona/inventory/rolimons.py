from __future__ import annotations

import aiohttp


class RolimonsCatalog:
    def __init__(self, items: dict[str, list]):
        self.items = items

    @classmethod
    async def fetch(cls, session: aiohttp.ClientSession) -> "RolimonsCatalog":
        async with session.get("https://www.rolimons.com/itemapi/itemdetails") as response:
            response.raise_for_status()
            data = await response.json()

        return cls(items=data["items"])

    def get_item_name(self, asset_id: int) -> str:
        item = self.items.get(str(asset_id))
        return item[0] if item else "Unknown Item"

    def is_limited(self, asset_id: int) -> bool:
        return str(asset_id) in self.items

    def get_item_value(self, asset_id: int) -> int:
        item = self.items.get(str(asset_id))
        if not item:
            return 0

        value = item[4]
        return value if isinstance(value, int) else 0