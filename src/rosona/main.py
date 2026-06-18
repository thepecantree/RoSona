from __future__ import annotations

import asyncio

import aiohttp

from rosona.core.config import Config
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

        user = await users.resolve("builderman")

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
        print(f"Headshot: {user.headshot}")
        print(f"Previous Usernames: {user.previous_usernames}")
        print(f"Last Online: {user.last_online}")
        print(f"Profile URL: {user.profile_url}")
        print(f"Avatar: {user.avatar}")


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()