from __future__ import annotations

from rosona.timeline.events import OwnershipEvent
from rosona.timeline.store import TimelineStore


class HistoryService:
    def __init__(self, store: TimelineStore):
        self.store = store

    def user_history(self, user_id: int) -> list[OwnershipEvent]:
        return sorted(
            self.store.get_events_for_user(user_id),
            key=lambda event: event.timestamp,
        )

    def asset_history(self, asset_id: int) -> list[OwnershipEvent]:
        return sorted(
            self.store.get_events_for_asset(asset_id),
            key=lambda event: event.timestamp,
        )

    def uaid_history(self, uaid: int) -> list[OwnershipEvent]:
        return sorted(
            self.store.get_events_for_uaid(uaid),
            key=lambda event: event.timestamp,
        )