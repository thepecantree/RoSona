from __future__ import annotations

import json
from pathlib import Path

from rosona.inventory.models import InventoryItem, InventorySnapshot


class InventorySnapshotStore:
    def __init__(self, path: str = "data/inventory_snapshots.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[int, list[InventorySnapshot]]:
        if not self.path.exists():
            return {}

        raw = json.loads(self.path.read_text(encoding="utf-8"))
        snapshots: dict[int, list[InventorySnapshot]] = {}

        for user_id, user_snapshots in raw.items():
            snapshots[int(user_id)] = [
                InventorySnapshot(
                    user_id=snapshot["user_id"],
                    captured_at=snapshot["captured_at"],
                    visibility=snapshot.get("visibility", "public"),
                    retention=snapshot.get("retention", "temporary"),
                    total_rap=snapshot["total_rap"],
                    total_value=snapshot["total_value"],
                    items=[InventoryItem(**item) for item in snapshot["items"]],
                )
                for snapshot in user_snapshots
            ]

        return snapshots

    def save(self, snapshots: dict[int, list[InventorySnapshot]]) -> None:
        raw = {
            str(user_id): [
                {
                    "user_id": snapshot.user_id,
                    "captured_at": snapshot.captured_at,
                    "visibility": snapshot.visibility,
                    "retention": snapshot.retention,
                    "total_rap": snapshot.total_rap,
                    "total_value": snapshot.total_value,
                    "items": [
                        {
                            "asset_id": item.asset_id,
                            "name": item.name,
                            "uaid": item.uaid,
                            "serial": item.serial,
                            "rap": item.rap,
                            "value": item.value,
                        }
                        for item in snapshot.items
                    ],
                }
                for snapshot in user_snapshots
            ]
            for user_id, user_snapshots in snapshots.items()
        }

        self.path.write_text(json.dumps(raw, indent=2, sort_keys=True), encoding="utf-8")

    def add_snapshot(self, snapshot: InventorySnapshot) -> None:
        snapshots = self.load()
        snapshots.setdefault(snapshot.user_id, []).append(snapshot)
        self.save(snapshots)

    def get_snapshots(self, user_id: int) -> list[InventorySnapshot]:
        return self.load().get(user_id, [])