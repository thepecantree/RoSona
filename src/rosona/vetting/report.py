from __future__ import annotations

from rosona.vetting.models import VettingReport


class VettingReportBuilder:
    def build(self, report: VettingReport) -> str:
        lines: list[str] = []

        lines.append(f"User ID: {report.user_id}")
        lines.append(f"Risk Level: {report.level}")
        lines.append(f"Score: {report.score}")
        lines.append("")
        lines.append("Indicators")
        lines.append("-" * 50)

        if not report.indicators:
            lines.append("No risk indicators detected.")
            return "\n".join(lines)

        for indicator in report.indicators:
            lines.append(f"Code: {indicator.code}")
            lines.append(f"Level: {indicator.level}")
            lines.append(f"Confidence: {indicator.confidence}")
            lines.append(f"Summary: {indicator.summary}")
            lines.append(f"Evidence: {indicator.evidence}")
            lines.append("")

        return "\n".join(lines)