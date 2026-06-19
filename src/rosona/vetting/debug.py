from __future__ import annotations

from rosona.inventory.simulate import make_test_delta
from rosona.vetting.report import VettingReportBuilder
from rosona.vetting.service import VettingService


def debug_vetting_report() -> None:
    delta = make_test_delta()

    report = VettingService().evaluate_delta(
        user_id=delta.new_snapshot.user_id,
        delta=delta,
    )

    print()
    print("Debug Vetting Report")
    print("-" * 50)
    print(VettingReportBuilder().build(report))