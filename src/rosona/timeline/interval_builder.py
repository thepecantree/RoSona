from __future__ import annotations

from rosona.inventory.pseudo import PseudoInventoryItem
from rosona.timeline.events import OwnershipEvent
from rosona.timeline.intervals import OwnershipInterval


class OwnershipIntervalBuilder:
    def from_events(
        self,
        events: list[OwnershipEvent],
    ) -> list[OwnershipInterval]:
        events = sorted(events, key=lambda event: event.timestamp)

        intervals: list[OwnershipInterval] = []

        active_start: str | None = None
        active_event: OwnershipEvent | None = None

        for event in events:
            if event.event_type in (
                "item_added",
                "item_observed",
                "item_publicly_confirmed",
            ):
                if active_start is None:
                    active_start = event.timestamp
                    active_event = event

            elif event.event_type == "item_removed":
                if active_start is not None and active_event is not None:
                    intervals.append(
                        OwnershipInterval(
                            user_id=active_event.user_id,
                            asset_id=active_event.asset_id,
                            uaid=active_event.uaid,
                            started_at=active_start,
                            ended_at=event.timestamp,
                            source=active_event.source,
                            confidence="confirmed",
                            status="closed",
                            evidence=(
                                "Ownership interval built from item_added "
                                "and item_removed events."
                            ),
                        )
                    )

                    active_start = None
                    active_event = None

        if active_start is not None and active_event is not None:
            intervals.append(
                OwnershipInterval(
                    user_id=active_event.user_id,
                    asset_id=active_event.asset_id,
                    uaid=active_event.uaid,
                    started_at=active_start,
                    ended_at=None,
                    source=active_event.source,
                    confidence="confirmed",
                    status="open",
                    evidence="Ownership interval is currently open.",
                )
            )

        return intervals

    def from_pseudo_reigns(
        self,
        pseudo_items: list[PseudoInventoryItem],
    ) -> list[OwnershipInterval]:
        intervals: list[OwnershipInterval] = []

        for item in pseudo_items:
            intervals.append(
                OwnershipInterval(
                    user_id=item.user_id,
                    asset_id=item.asset_id,
                    uaid=item.uaid,
                    started_at=item.first_observed_at,
                    ended_at=(
                        None
                        if item.status == "open"
                        else item.last_observed_at
                    ),
                    source=item.source,
                    confidence=item.confidence,
                    status=item.status,
                    evidence=item.evidence,
                )
            )

        return intervals