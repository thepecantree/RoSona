from __future__ import annotations

from dataclasses import replace

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

    async def request(self, method: str, subdomain: str, path: str, **kwargs) -> dict:
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
            json={"usernames": [username], "excludeBannedUsers": False},
        )

        users = data.get("data", [])
        if not users:
            raise RobloxNotFound(username)

        user = users[0]

        return RobloxUser(
            id=user["id"],
            username=user["name"],
            display_name=user["displayName"],
            description=None,
            created=None,
            verified=user.get("hasVerifiedBadge", False),
            banned=False,
        )

    async def get_user(self, user_id: int) -> RobloxUser:
        data = await self.request("GET", "users", f"v1/users/{user_id}")

        return RobloxUser(
            id=data["id"],
            username=data["name"],
            display_name=data["displayName"],
            description=data.get("description"),
            created=data.get("created"),
            verified=data.get("hasVerifiedBadge", False),
            banned=data.get("isBanned", False),
        )

    async def get_user_by_id(self, user_id: int) -> RobloxUser:
        return await self.get_user(user_id)

    async def populate_counts(self, user: RobloxUser) -> RobloxUser:
        followers_data = await self.request(
            "GET",
            "friends",
            f"v1/users/{user.id}/followers/count",
        )

        following_data = await self.request(
            "GET",
            "friends",
            f"v1/users/{user.id}/followings/count",
        )

        friends_data = await self.request(
            "GET",
            "friends",
            f"v1/users/{user.id}/friends/count",
        )

        return replace(
            user,
            friends=friends_data["count"],
            followers=followers_data["count"],
            following=following_data["count"],
        )

    async def populate_previous_usernames(self, user: RobloxUser) -> RobloxUser:
        names: list[str] = []
        cursor: str | None = None

        while True:
            path = f"v1/users/{user.id}/username-history?limit=100&sortOrder=Asc"

            if cursor:
                path += f"&cursor={cursor}"

            data = await self.request("GET", "users", path)

            names.extend(entry["name"] for entry in data.get("data", []))

            cursor = data.get("nextPageCursor")
            if not cursor:
                break

        return replace(user, previous_usernames=names)
    
    async def get_limited_inventory(self, user_id: int) -> list[dict]:
        items: list[dict] = []
        cursor = ""

        while True:
            path = (
                f"v1/users/{user_id}/assets/collectibles"
                f"?limit=100&sortOrder=Asc&cursor={cursor}"
            )

            data = await self.request("GET", "inventory", path)

            items.extend(data.get("data", []))

            cursor = data.get("nextPageCursor")
            if not cursor:
                break

        return items
    
    async def populate_last_online(self, user: RobloxUser) -> RobloxUser:
        try:
            data = await self.request(
                "POST",
                "presence",
                "v1/presence/last-online",
                json={"userIds": [user.id]},
            )
        except RobloxNotFound:
            return replace(user, last_online=None)

        timestamps = data.get("lastOnlineTimestamps", [])
        last_online = timestamps[0]["lastOnline"] if timestamps else None

        return replace(user, last_online=last_online)

    async def populate_headshot(self, user: RobloxUser) -> RobloxUser:
        data = await self.request(
            "GET",
            "thumbnails",
            (
                "v1/users/avatar-headshot"
                f"?userIds={user.id}"
                "&size=420x420"
                "&format=Png"
                "&isCircular=false"
            ),
        )

        image_url = data["data"][0]["imageUrl"] if data.get("data") else None

        return replace(user, headshot=image_url)

    async def populate_avatar(self, user: RobloxUser) -> RobloxUser:
        data = await self.request(
            "GET",
            "thumbnails",
            (
                "v1/users/avatar"
                f"?userIds={user.id}"
                "&size=420x420"
                "&format=Png"
                "&isCircular=false"
            ),
        )

        image_url = data["data"][0]["imageUrl"] if data.get("data") else None

        return replace(user, avatar=image_url)