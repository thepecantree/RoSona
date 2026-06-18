import json
from pathlib import Path

from rosona.presence.models import LastSeenSignal


class PresenceStore:
    def __init__(self, path: str = "data/presence.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[int, list[LastSeenSignal]]:
        if not self.path.exists():
            return {}

        raw = json.loads(self.path.read_text(encoding="utf-8"))

        data: dict[int, list[LastSeenSignal]] = {}

        for user_id, signals in raw.items():
            data[int(user_id)] = [LastSeenSignal(**signal) for signal in signals]

        return data

    def save(self, data: dict[int, list[LastSeenSignal]]) -> None:
        raw = {
            str(user_id): [
                {
                    "user_id": signal.user_id,
                    "timestamp": signal.timestamp,
                    "source": signal.source,
                    "confidence": signal.confidence,
                    "evidence": signal.evidence,
                }
                for signal in signals
            ]
            for user_id, signals in data.items()
        }

        self.path.write_text(
            json.dumps(raw, indent=2, sort_keys=True),
            encoding="utf-8",
        )

    def add_signal(self, signal: LastSeenSignal) -> None:
        data = self.load()
        data.setdefault(signal.user_id, []).append(signal)
        self.save(data)

    def get_signals(self, user_id: int) -> list[LastSeenSignal]:
        return self.load().get(user_id, [])