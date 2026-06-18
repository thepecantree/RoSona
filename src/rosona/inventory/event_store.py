from __future__ import annotations

import json
from pathlib import Path

from rosona.inventory.events import InventoryEvent


class InventoryEventStore:
    def __init__(self, path: str = "data/inventory_events.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[InventoryEvent]:
        if not self.path.exists():
            return []

        raw = json.loads(
            self.path.read_text(encoding="utf-8")
        )

        return [
            InventoryEvent(**event)
            for event in raw
        ]

    def save(
        self,
        events: list[InventoryEvent],
    ) -> None:
        raw = [
            {
                "user_id": event.user_id,
                "timestamp": event.timestamp,
                "event_type": event.event_type,
                "description": event.description,
            }
            for event in events
        ]

        self.path.write_text(
            json.dumps(raw, indent=2),
            encoding="utf-8",
        )

    def add(
        self,
        event: InventoryEvent,
    ) -> None:
        events = self.load()
        events.append(event)
        self.save(events)

    def get_user_events(
        self,
        user_id: int,
    ) -> list[InventoryEvent]:
        return [
            event
            for event in self.load()
            if event.user_id == user_id
        ]