from __future__ import annotations

from datetime import UTC, datetime, timedelta

from rosona.inventory.delta import compare_snapshots
from rosona.inventory.models import InventoryItem, InventorySnapshot


def make_test_snapshots() -> tuple[InventorySnapshot, InventorySnapshot]:
    old_time = datetime.now(UTC) - timedelta(days=1)
    new_time = datetime.now(UTC)

    old_snapshot = InventorySnapshot(
        user_id=123,
        captured_at=old_time.isoformat(),
        visibility="public",
        retention="temporary",
        total_rap=100_000,
        total_value=100_000,
        items=[
            InventoryItem(
                asset_id=1,
                name="Old Limited",
                uaid=111,
                serial=None,
                rap=100_000,
                value=100_000,
            ),
        ],
    )

    new_snapshot = InventorySnapshot(
        user_id=123,
        captured_at=new_time.isoformat(),
        visibility="public",
        retention="temporary",
        total_rap=250_000,
        total_value=250_000,
        items=[
            InventoryItem(
                asset_id=2,
                name="New Limited",
                uaid=222,
                serial=10,
                rap=250_000,
                value=250_000,
            ),
        ],
    )

    return old_snapshot, new_snapshot


def make_test_delta():
    old_snapshot, new_snapshot = make_test_snapshots()
    return compare_snapshots(old_snapshot, new_snapshot)