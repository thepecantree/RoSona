from __future__ import annotations

import json
from pathlib import Path

from rosona.inventory.pseudo import OwnershipInterval, PseudoInventoryItem


class PseudoInventoryStore:
    def __init__(self, path: str = "data/pseudo_inventory.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict:
        if not self.path.exists():
            return {
                "items": [],
                "intervals": [],
            }

        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, data: dict) -> None:
        self.path.write_text(
            json.dumps(data, indent=2, sort_keys=True),
            encoding="utf-8",
        )

    def add_item(self, item: PseudoInventoryItem) -> None:
        data = self.load()

        record = {
            "user_id": item.user_id,
            "asset_id": item.asset_id,
            "uaid": item.uaid,
            "observed_at": item.observed_at,
            "source": item.source,
            "confidence": item.confidence,
            "evidence": item.evidence,
        }

        if record not in data["items"]:
            data["items"].append(record)

        self.save(data)

    def add_interval(self, interval: OwnershipInterval) -> None:
        data = self.load()

        record = {
            "user_id": interval.user_id,
            "uaid": interval.uaid,
            "asset_id": interval.asset_id,
            "known_owned_after": interval.known_owned_after,
            "known_not_owned_after": interval.known_not_owned_after,
            "source": interval.source,
            "confidence": interval.confidence,
            "evidence": interval.evidence,
        }

        if record not in data["intervals"]:
            data["intervals"].append(record)

        self.save(data)

    def get_items(self, user_id: int) -> list[PseudoInventoryItem]:
        data = self.load()

        return [
            PseudoInventoryItem(**item)
            for item in data["items"]
            if item["user_id"] == user_id
        ]

    def get_intervals(self, user_id: int) -> list[OwnershipInterval]:
        data = self.load()

        return [
            OwnershipInterval(**interval)
            for interval in data["intervals"]
            if interval["user_id"] == user_id
        ]