from __future__ import annotations

from rosona.timeline.events import OwnershipEvent
from rosona.timeline.models import (
    OwnershipSegment,
    OwnershipTimeline,
)


class TimelineMerger:
    def merge_events(
        self,
        asset_id: int,
        uaid: int | None,
        events: list[OwnershipEvent],
    ) -> OwnershipTimeline:
        events = sorted(
            events,
            key=lambda event: event.timestamp,
        )

        segments: list[OwnershipSegment] = []

        active_start: str | None = None
        active_user_id: int | None = None

        for event in events:
            if event.event_type in (
                "item_added",
                "item_observed",
                "item_publicly_confirmed",
            ):
                if active_start is None:
                    active_start = event.timestamp
                    active_user_id = event.user_id

            elif event.event_type == "item_removed":
                if (
                    active_start is not None
                    and active_user_id is not None
                ):
                    segments.append(
                        OwnershipSegment(
                            user_id=active_user_id,
                            asset_id=asset_id,
                            uaid=uaid,
                            started_at=active_start,
                            ended_at=event.timestamp,
                            source="public_inventory",
                            confidence="confirmed",
                            evidence="Built from ownership events.",
                            status="closed",
                        )
                    )

                    active_start = None
                    active_user_id = None

        if (
            active_start is not None
            and active_user_id is not None
        ):
            segments.append(
                OwnershipSegment(
                    user_id=active_user_id,
                    asset_id=asset_id,
                    uaid=uaid,
                    started_at=active_start,
                    ended_at=None,
                    source="public_inventory",
                    confidence="confirmed",
                    evidence="Ownership currently active.",
                    status="open",
                )
            )

        return OwnershipTimeline(
            asset_id=asset_id,
            uaid=uaid,
            segments=segments,
        )