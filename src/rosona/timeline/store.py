from __future__ import annotations

import json
from pathlib import Path

from rosona.timeline.events import OwnershipEvent


class TimelineStore:
    def __init__(self, path: str = "data/timeline_events.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[OwnershipEvent]:
        if not self.path.exists():
            return []

        raw = json.loads(self.path.read_text(encoding="utf-8"))

        return [
            OwnershipEvent(**event)
            for event in raw
        ]

    def save(self, events: list[OwnershipEvent]) -> None:
        raw = [
            {
                "timestamp": event.timestamp,
                "event_type": event.event_type,
                "source": event.source,
                "user_id": event.user_id,
                "asset_id": event.asset_id,
                "uaid": event.uaid,
                "evidence": event.evidence,
            }
            for event in events
        ]

        self.path.write_text(
            json.dumps(raw, indent=2, sort_keys=True),
            encoding="utf-8",
        )

    def append(self, new_events: list[OwnershipEvent]) -> None:
        events = self.load()
        events.extend(new_events)
        self.save(events)

    def get_events_for_user(self, user_id: int) -> list[OwnershipEvent]:
        return [
            event
            for event in self.load()
            if event.user_id == user_id
        ]

    def get_events_for_uaid(self, uaid: int) -> list[OwnershipEvent]:
        return [
            event
            for event in self.load()
            if event.uaid == uaid
        ]

    def get_events_for_asset(self, asset_id: int) -> list[OwnershipEvent]:
        return [
            event
            for event in self.load()
            if event.asset_id == asset_id
        ]