from __future__ import annotations

import asyncio

import aiohttp

from rosona.core.config import Config
from rosona.roblox.client import RobloxClient


async def run() -> None:
    config = Config.from_env()

    print(f"RoSona starting in {config.environment} mode")

    async with aiohttp.ClientSession() as session:
        roblox = RobloxClient(session)

        user = await roblox.get_user_by_username("Builderman")

        print(f"{user.username} ({user.display_name}) -> {user.id}")


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()