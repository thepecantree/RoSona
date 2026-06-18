from __future__ import annotations

import aiohttp

from rosona.roblox.errors import (
    RobloxNotFound,
    RobloxRateLimited,
    RobloxServerError,
    RobloxUnauthorized,
)
from rosona.roblox.models import RobloxUser


class RobloxClient:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def request(
        self,
        method: str,
        subdomain: str,
        path: str,
        **kwargs,
    ) -> dict:
        url = f"https://{subdomain}.roblox.com/{path}"

        async with self.session.request(method, url, **kwargs) as response:
            if response.status == 404:
                raise RobloxNotFound(url)

            if response.status == 401:
                raise RobloxUnauthorized(url)

            if response.status == 429:
                raise RobloxRateLimited(url)

            if response.status >= 500:
                raise RobloxServerError(url)

            return await response.json()

    async def get_user_by_username(self, username: str) -> RobloxUser:
        data = await self.request(
            "POST",
            "users",
            "v1/usernames/users",
            json={
                "usernames": [username],
                "excludeBannedUsers": False,
            },
        )

        users = data["data"]

        if not users:
            raise RobloxNotFound(username)

        user = users[0]

        return RobloxUser(
            id=user["id"],
            username=user["name"],
            display_name=user["displayName"],
            verified=user["hasVerifiedBadge"],
        )