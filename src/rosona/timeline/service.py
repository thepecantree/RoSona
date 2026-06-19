from __future__ import annotations

from rosona.inventory.delta import InventoryDelta
from rosona.timeline.events import OwnershipEvent
from rosona.timeline.models import OwnershipSegment, OwnershipTimeline


class TimelineService:
    def events_from_delta(
        self,
        delta: InventoryDelta,
    ) -> list[OwnershipEvent]:
        events: list[OwnershipEvent] = []

        timestamp = delta.new_snapshot.captured_at
        user_id = delta.new_snapshot.user_id

        for item in delta.added_items:
            events.append(
                OwnershipEvent(
                    timestamp=timestamp,
                    event_type="item_added",
                    source="inventory_snapshot",
                    user_id=user_id,
                    asset_id=item.asset_id,
                    uaid=item.uaid,
                    evidence=(
                        f"Item appeared in public inventory snapshot. "
                        f"Name: {item.name}. Value: {item.value}."
                    ),
                )
            )

        for item in delta.removed_items:
            events.append(
                OwnershipEvent(
                    timestamp=timestamp,
                    event_type="item_removed",
                    source="inventory_snapshot",
                    user_id=user_id,
                    asset_id=item.asset_id,
                    uaid=item.uaid,
                    evidence=(
                        f"Item disappeared from public inventory snapshot. "
                        f"Name: {item.name}. Value: {item.value}."
                    ),
                )
            )

        return events

    def build_timeline(
        self,
        asset_id: int,
        uaid: int | None,
        events: list[OwnershipEvent],
    ) -> OwnershipTimeline:
        events = sorted(events, key=lambda event: event.timestamp)
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
                if active_start is not None and active_user_id is not None:
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

        if active_start is not None and active_user_id is not None:
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