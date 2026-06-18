from __future__ import annotations

from rosona.roblox.client import RobloxClient
from rosona.roblox.errors import RobloxRateLimited
from rosona.roblox.models import RobloxUser


class UserService:
    def __init__(self, client: RobloxClient):
        self.client = client

    async def resolve(self, username: str) -> RobloxUser:
        stub = await self.client.get_user_by_username(username)

        user = await self.client.get_user(stub.id)

        try:
            user = await self.client.populate_counts(user)
        except RobloxRateLimited:
            pass

        try:
            user = await self.client.populate_previous_usernames(user)
        except RobloxRateLimited:
            pass

        try:
            user = await self.client.populate_headshot(user)
        except RobloxRateLimited:
            pass

        try:
            user = await self.client.populate_avatar(user)
        except RobloxRateLimited:
            pass

        return user