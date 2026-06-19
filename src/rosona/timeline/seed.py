from __future__ import annotations

from datetime import UTC, datetime, timedelta

from rosona.timeline.events import OwnershipEvent


def make_seed_events(
    user_id: int,
    asset_id: int,
    uaid: int,
) -> list[OwnershipEvent]:
    now = datetime.now(UTC)

    return [
        OwnershipEvent(
            timestamp=(now - timedelta(days=7)).isoformat(),
            event_type="item_added",
            source="inventory_snapshot",
            user_id=user_id,
            asset_id=asset_id,
            uaid=uaid,
            evidence="Seeded test event: item entered inventory.",
        ),
        OwnershipEvent(
            timestamp=now.isoformat(),
            event_type="item_removed",
            source="inventory_snapshot",
            user_id=user_id,
            asset_id=asset_id,
            uaid=uaid,
            evidence="Seeded test event: item left inventory.",
        ),
    ]