from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RobloxUser:
    id: int
    username: str
    display_name: str
    description: str | None
    created: str | None
    verified: bool
    banned: bool
    friends: int | None = None
    followers: int | None = None
    following: int | None = None
    previous_usernames: list[str] | None = None
    last_online: str | None = None
    headshot: str | None = None
    avatar: str | None = None

    @property
    def profile_url(self) -> str:
        return f"https://www.roblox.com/users/{self.id}/profile"