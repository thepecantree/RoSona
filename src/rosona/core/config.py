from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    environment: str
    discord_token: str | None
    roblox_cookie: str | None
    roblox_api_key: str | None

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            environment=getenv("ROSONA_ENV", "development"),
            discord_token=getenv("DISCORD_TOKEN"),
            roblox_cookie=getenv("ROBLOX_COOKIE"),
            roblox_api_key=getenv("ROBLOX_API_KEY"),
        )