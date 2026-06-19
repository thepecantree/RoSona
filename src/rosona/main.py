from __future__ import annotations

import asyncio

import aiohttp

from rosona.core.config import Config
from rosona.inventory.avatar_scanner import AvatarLimitedScanner
from rosona.inventory.pseudo_service import PseudoInventoryService
from rosona.inventory.pseudo_store import PseudoInventoryStore
from rosona.inventory.rolimons import RolimonsCatalog
from rosona.inventory.service import InventoryService
from rosona.inventory.store import InventorySnapshotStore
from rosona.presence.service import PresenceService
from rosona.presence.store import PresenceStore
from rosona.roblox.client import RobloxClient
from rosona.roblox.users import UserService
from rosona.timeline.history import HistoryService
from rosona.timeline.interval_builder import OwnershipIntervalBuilder
from rosona.timeline.service import TimelineService
from rosona.timeline.store import TimelineStore
from rosona.vetting.report import VettingReportBuilder
from rosona.vetting.service import VettingService


async def run() -> None:
    config = Config.from_env()

    print("=" * 50)
    print("RoSona")
    print(f"Environment: {config.environment}")
    print("=" * 50)

    async with aiohttp.ClientSession() as session:
        roblox = RobloxClient(session)
        users = UserService(roblox)

        user = await users.resolve("Sanajagaq")

        presence = PresenceService(
            client=roblox,
            store=PresenceStore(),
        )

        await presence.observe_now(user.id)
        last_seen = presence.estimate(user.id)

        rolimons = await RolimonsCatalog.fetch(session)

        pseudo_inventory = PseudoInventoryService(
            store=PseudoInventoryStore(),
        )

        avatar_scanner = AvatarLimitedScanner(
            client=roblox,
            rolimons=rolimons,
            pseudo_inventory=pseudo_inventory,
        )

        inventory = InventoryService(
            client=roblox,
            rolimons=rolimons,
            store=InventorySnapshotStore(),
        )

        snapshot = await inventory.create_snapshot(user.id)
        delta = inventory.compare_latest(user.id)

        timeline_store = TimelineStore()
        timeline_service = TimelineService()
        history = HistoryService(timeline_store)
        interval_builder = OwnershipIntervalBuilder()

        timeline_events = []

        if delta is not None:
            timeline_events = timeline_service.events_from_delta(delta)
            timeline_store.append(timeline_events)

        user_timeline_events = history.user_history(user.id)

        vetting_report = VettingService().evaluate_delta(
            user_id=user.id,
            delta=delta,
        )

        public_asset_ids = {
            item.asset_id
            for item in snapshot.items
        }

        pseudo_inventory.close_reigns_covered_by_public_inventory(
            user_id=user.id,
            asset_ids=public_asset_ids,
            closed_at=snapshot.captured_at,
        )

        worn_limiteds = await avatar_scanner.scan_worn_limiteds(
            user.id,
            public_snapshot=snapshot,
        )

        pseudo_items = pseudo_inventory.get_pseudo_inventory(user.id)
        ownership_intervals = pseudo_inventory.get_ownership_intervals(user.id)

        event_intervals = interval_builder.from_events(
            user_timeline_events
        )

        pseudo_intervals = interval_builder.from_pseudo_reigns(
            pseudo_items
        )

        all_intervals = [
            *event_intervals,
            *pseudo_intervals,
        ]

        print()
        print("User Lookup Test")
        print("-" * 50)
        print(f"ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Display Name: {user.display_name}")
        print(f"Verified: {user.verified}")
        print(f"Friends: {user.friends}")
        print(f"Followers: {user.followers}")
        print(f"Following: {user.following}")
        print(f"Profile URL: {user.profile_url}")
        print(f"Headshot: {user.headshot}")
        print(f"Avatar: {user.avatar}")

        print()
        print("Last Seen Estimate")
        print("-" * 50)
        print(f"Timestamp: {last_seen.best_estimate.timestamp}")
        print(f"Source: {last_seen.best_estimate.source}")
        print(f"Confidence: {last_seen.best_estimate.confidence}")
        print(f"Evidence: {last_seen.best_estimate.evidence}")

        print()
        print("Inventory Snapshot")
        print("-" * 50)
        print(f"Captured At: {snapshot.captured_at}")
        print(f"Limited Items: {len(snapshot.items)}")
        print(f"Total RAP: {snapshot.total_rap:,}")
        print(f"Total Value: {snapshot.total_value:,}")

        if snapshot.items:
            print()
            print("Top 10 Most Valuable Items")
            print("-" * 50)
            print(f"Showing top 10 of {len(snapshot.items)} limited items")

            top_items = sorted(
                snapshot.items,
                key=lambda item: item.value,
                reverse=True,
            )[:10]

            for item in top_items:
                print(
                    f"{item.name} | "
                    f"Value {item.value:,} | "
                    f"RAP {item.rap:,} | "
                    f"UAID {item.uaid} | "
                    f"Serial {item.serial}"
                )

        if delta is not None:
            print()
            print("Inventory Delta")
            print("-" * 50)
            print(f"RAP Change: {delta.rap_change:+,}")
            print(f"Value Change: {delta.value_change:+,}")
            print(f"Ownership RAP Flow: {delta.ownership_rap_flow:+,}")
            print(f"Ownership Value Flow: {delta.ownership_value_flow:+,}")
            print(f"Market RAP Movement: {delta.market_rap_movement:+,}")
            print(f"Market Value Movement: {delta.market_value_movement:+,}")
            print(f"Added Items: {len(delta.added_items)}")
            print(f"Removed Items: {len(delta.removed_items)}")
            print(f"Retained Items: {len(delta.retained_items)}")

        print()
        print("Worn Limited Scan")
        print("-" * 50)
        print(f"Detected Limiteds: {len(worn_limiteds)}")

        for item in worn_limiteds[:10]:
            print(
                f"Asset {item.asset_id} | "
                f"Source {item.source} | "
                f"Confidence {item.confidence}"
            )

        print()
        print("Pseudo Inventory Evidence")
        print("-" * 50)
        print(f"Observed Reigns: {len(pseudo_items)}")
        print(f"Ownership Intervals: {len(ownership_intervals)}")

        for item in pseudo_items[:10]:
            print(
                f"Asset {item.asset_id} | "
                f"UAID {item.uaid} | "
                f"Source {item.source} | "
                f"Confidence {item.confidence} | "
                f"First {item.first_observed_at} | "
                f"Last {item.last_observed_at} | "
                f"Status {item.status}"
            )

        print()
        print("Timeline Events")
        print("-" * 50)
        print(f"New Events This Run: {len(timeline_events)}")
        print(f"Stored Events For User: {len(user_timeline_events)}")

        for event in user_timeline_events[-10:]:
            print(
                f"{event.timestamp} | "
                f"{event.event_type} | "
                f"Asset {event.asset_id} | "
                f"UAID {event.uaid} | "
                f"{event.source}"
            )

        print()
        print("Ownership Intervals")
        print("-" * 50)
        print(f"Event Intervals: {len(event_intervals)}")
        print(f"Pseudo Intervals: {len(pseudo_intervals)}")
        print(f"Total Intervals: {len(all_intervals)}")

        for interval in all_intervals[:10]:
            print(
                f"Asset {interval.asset_id} | "
                f"UAID {interval.uaid} | "
                f"Start {interval.started_at} | "
                f"End {interval.ended_at or 'Present'} | "
                f"Source {interval.source} | "
                f"Status {interval.status}"
            )

        print()
        print("Vetting Report")
        print("-" * 50)
        print(VettingReportBuilder().build(vetting_report))


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()