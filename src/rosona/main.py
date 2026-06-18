from __future__ import annotations

import asyncio

import aiohttp

from rosona.core.config import Config
from rosona.inventory.rolimons import RolimonsCatalog
from rosona.inventory.service import InventoryService
from rosona.inventory.store import InventorySnapshotStore
from rosona.presence.service import PresenceService
from rosona.presence.store import PresenceStore
from rosona.roblox.client import RobloxClient
from rosona.roblox.users import UserService


async def run() -> None:
    config = Config.from_env()

    print("=" * 50)
    print("RoSona")
    print(f"Environment: {config.environment}")
    print("=" * 50)

    async with aiohttp.ClientSession() as session:
        roblox = RobloxClient(session)
        users = UserService(roblox)

        user = await users.resolve("Sanajagaq")

        presence = PresenceService(
            client=roblox,
            store=PresenceStore(),
        )

        await presence.observe_now(user.id)
        last_seen = presence.estimate(user.id)

        rolimons = await RolimonsCatalog.fetch(session)
        inventory = InventoryService(
            client=roblox,
            rolimons=rolimons,
            store=InventorySnapshotStore(),
        )

        snapshot = await inventory.create_snapshot(user.id)

        print()
        print("User Lookup Test")
        print("-" * 50)
        print(f"ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Display Name: {user.display_name}")
        print(f"Verified: {user.verified}")
        print(f"Friends: {user.friends}")
        print(f"Followers: {user.followers}")
        print(f"Following: {user.following}")
        print(f"Profile URL: {user.profile_url}")
        print(f"Headshot: {user.headshot}")
        print(f"Avatar: {user.avatar}")

        print()
        print("Last Seen Estimate")
        print("-" * 50)
        print(f"Timestamp: {last_seen.best_estimate.timestamp}")
        print(f"Source: {last_seen.best_estimate.source}")
        print(f"Confidence: {last_seen.best_estimate.confidence}")
        print(f"Evidence: {last_seen.best_estimate.evidence}")

        print()
        print("Inventory Snapshot")
        print("-" * 50)
        print(f"Captured At: {snapshot.captured_at}")
        print(f"Limited Items: {len(snapshot.items)}")
        print(f"Total RAP: {snapshot.total_rap}")
        print(f"Total Value: {snapshot.total_value}")

        if snapshot.items:
            print()
            print("Items")
            print("-" * 50)
            for item in snapshot.items[:10]:
                print(
                    f"{item.name} | "
                    f"Asset {item.asset_id} | "
                    f"UAID {item.uaid} | "
                    f"Serial {item.serial} | "
                    f"RAP {item.rap} | "
                    f"Value {item.value}"
                )


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()