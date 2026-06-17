from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class AppState:
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    heartbeat: bool = False
    rolimons_data: dict = field(default_factory=dict)