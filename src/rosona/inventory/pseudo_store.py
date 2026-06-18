from __future__ import annotations

import json
from pathlib import Path

from rosona.inventory.pseudo import (
    OwnershipInterval,
    PseudoInventoryItem,
)


class PseudoInventoryStore:
    def __init__(
        self,
        path: str = "data/pseudo_inventory.json",
    ):
        self.path = Path(path)
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def load(self) -> dict:
        if not self.path.exists():
            return {
                "items": [],
                "intervals": [],
            }

        data = json.loads(
            self.path.read_text(
                encoding="utf-8",
            )
        )

        data.setdefault("items", [])
        data.setdefault("intervals", [])

        for item in data["items"]:
            observed_at = item.get("observed_at")

            item.setdefault(
                "first_observed_at",
                observed_at,
            )

            item.setdefault(
                "last_observed_at",
                observed_at,
            )

            item.setdefault(
                "status",
                "open",
            )

            item.setdefault(
                "ended_reason",
                "currently_open",
            )

            item.pop(
                "observed_at",
                None,
            )

        return data

    def save(
        self,
        data: dict,
    ) -> None:
        self.path.write_text(
            json.dumps(
                data,
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )

    def add_item(
        self,
        item: PseudoInventoryItem,
    ) -> None:
        data = self.load()

        for existing in data["items"]:
            if (
                existing["user_id"] == item.user_id
                and existing["asset_id"] == item.asset_id
                and existing["source"] == item.source
                and existing.get("status", "open")
                == "open"
            ):
                existing["last_observed_at"] = (
                    item.last_observed_at
                )

                self.save(data)
                return

        data["items"].append(
            {
                "user_id": item.user_id,
                "asset_id": item.asset_id,
                "uaid": item.uaid,
                "first_observed_at": item.first_observed_at,
                "last_observed_at": item.last_observed_at,
                "source": item.source,
                "confidence": item.confidence,
                "evidence": item.evidence,
                "status": item.status,
                "ended_reason": item.ended_reason,
            }
        )

        self.save(data)

    def add_interval(
        self,
        interval: OwnershipInterval,
    ) -> None:
        data = self.load()

        data["intervals"].append(
            {
                "user_id": interval.user_id,
                "uaid": interval.uaid,
                "asset_id": interval.asset_id,
                "known_owned_after": interval.known_owned_after,
                "known_not_owned_after": interval.known_not_owned_after,
                "source": interval.source,
                "confidence": interval.confidence,
                "evidence": interval.evidence,
            }
        )

        self.save(data)

    def get_items(
        self,
        user_id: int,
    ) -> list[PseudoInventoryItem]:
        data = self.load()

        return [
            PseudoInventoryItem(**item)
            for item in data["items"]
            if item["user_id"] == user_id
        ]

    def get_intervals(
        self,
        user_id: int,
    ) -> list[OwnershipInterval]:
        data = self.load()

        return [
            OwnershipInterval(**interval)
            for interval in data["intervals"]
            if interval["user_id"] == user_id
        ]