from __future__ import annotations

from rosona.timeline.history import HistoryService
from rosona.timeline.merger import TimelineMerger
from rosona.timeline.query import TimelineQueryService
from rosona.timeline.report import TimelineReportBuilder
from rosona.timeline.store import TimelineStore


def print_asset_report(asset_id: int) -> None:
    store = TimelineStore()

    history = HistoryService(store)

    query = TimelineQueryService(
        history=history,
        merger=TimelineMerger(),
    )

    timeline = query.asset_timeline(asset_id)

    report = TimelineReportBuilder().build(
        timeline
    )

    print()
    print("Timeline Report")
    print("-" * 50)
    print(report)