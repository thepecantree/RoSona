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

        user_id = await roblox.username_to_user_id("Builderman")

        print(f"Builderman -> {user_id}")


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()