from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RobloxUser:
    id: int
    username: str
    display_name: str
    verified: bool