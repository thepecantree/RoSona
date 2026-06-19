from __future__ import annotations

from rosona.inventory.simulate import make_test_delta
from rosona.timeline.service import TimelineService


def debug_timeline_events() -> None:
    delta = make_test_delta()
    service = TimelineService()

    events = service.events_from_delta(delta)

    print("Debug Timeline Events")
    print("-" * 50)

    for event in events:
        print(
            f"{event.timestamp} | "
            f"{event.event_type} | "
            f"Asset {event.asset_id} | "
            f"UAID {event.uaid} | "
            f"{event.evidence}"
        )