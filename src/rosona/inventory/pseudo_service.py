from __future__ import annotations

from datetime import UTC, datetime

from rosona.inventory.pseudo import OwnershipInterval, PseudoInventoryItem
from rosona.inventory.pseudo_store import PseudoInventoryStore


class PseudoInventoryService:
    def __init__(self, store: PseudoInventoryStore):
        self.store = store

    def observe_worn_limited(
        self,
        user_id: int,
        asset_id: int,
        uaid: int | None = None,
    ) -> PseudoInventoryItem:
        observed_at = datetime.now(UTC).isoformat()

        item = PseudoInventoryItem(
            user_id=user_id,
            asset_id=asset_id,
            uaid=uaid,
            first_observed_at=observed_at,
            last_observed_at=observed_at,
            source="wearing_avatar",
            confidence="confirmed_at_observation",
            evidence="Limited item was observed being worn by the user.",
            status="open",
            ended_reason="currently_open",
        )

        self.store.add_item(item)
        return item

    def observe_collection_limited(
        self,
        user_id: int,
        asset_id: int,
        uaid: int | None = None,
    ) -> PseudoInventoryItem:
        observed_at = datetime.now(UTC).isoformat()

        item = PseudoInventoryItem(
            user_id=user_id,
            asset_id=asset_id,
            uaid=uaid,
            first_observed_at=observed_at,
            last_observed_at=observed_at,
            source="profile_collection",
            confidence="strong_inference",
            evidence="Limited item was observed in the user's profile collection.",
            status="open",
            ended_reason="currently_open",
        )

        self.store.add_item(item)
        return item

    def infer_hidden_owner_interval(
        self,
        user_id: int,
        asset_id: int,
        uaid: int,
        known_owned_after: str | None,
        known_not_owned_after: str | None = None,
    ) -> OwnershipInterval:
        interval = OwnershipInterval(
            user_id=user_id,
            asset_id=asset_id,
            uaid=uaid,
            known_owned_after=known_owned_after,
            known_not_owned_after=known_not_owned_after,
            source="rolimons_hidden_owner_inference",
            confidence="inferred_interval",
            evidence=(
                "Ownership interval inferred from Rolimon's history, "
                "hidden-owner transition, and UAID exclusivity."
            ),
        )

        self.store.add_interval(interval)
        return interval

    def get_pseudo_inventory(self, user_id: int) -> list[PseudoInventoryItem]:
        return self.store.get_items(user_id)

    def get_ownership_intervals(self, user_id: int) -> list[OwnershipInterval]:
        return self.store.get_intervals(user_id)