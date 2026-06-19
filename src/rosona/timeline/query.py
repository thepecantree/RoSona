from __future__ import annotations

from rosona.timeline.history import HistoryService
from rosona.timeline.merger import TimelineMerger
from rosona.timeline.models import OwnershipTimeline


class TimelineQueryService:
    def __init__(
        self,
        history: HistoryService,
        merger: TimelineMerger,
    ) -> None:
        self.history = history
        self.merger = merger

    def uaid_timeline(
        self,
        uaid: int,
    ) -> OwnershipTimeline:
        events = self.history.uaid_history(uaid)

        asset_id = (
            events[-1].asset_id
            if events
            else 0
        )

        return self.merger.merge_events(
            asset_id=asset_id,
            uaid=uaid,
            events=events,
        )

    def asset_timeline(
        self,
        asset_id: int,
    ) -> OwnershipTimeline:
        events = self.history.asset_history(asset_id)

        return self.merger.merge_events(
            asset_id=asset_id,
            uaid=None,
            events=events,
        )

    def user_timeline(
        self,
        user_id: int,
    ) -> list:
        return self.history.user_history(user_id)