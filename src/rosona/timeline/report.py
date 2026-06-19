from __future__ import annotations

from rosona.timeline.models import OwnershipSegment, OwnershipTimeline


class TimelineReportBuilder:
    def build(self, timeline: OwnershipTimeline) -> str:
        lines: list[str] = []

        lines.append(f"Asset ID: {timeline.asset_id}")
        lines.append(f"UAID: {timeline.uaid}")
        lines.append("")
        lines.append("Ownership Segments")
        lines.append("-" * 50)

        if not timeline.segments:
            lines.append("No ownership evidence found.")
            return "\n".join(lines)

        for segment in timeline.segments:
            lines.extend(self._segment_lines(segment))

        return "\n".join(lines)

    def _segment_lines(self, segment: OwnershipSegment) -> list[str]:
        return [
            f"User ID: {segment.user_id}",
            f"Start: {segment.started_at}",
            f"End: {segment.ended_at or 'Present'}",
            f"Source: {segment.source}",
            f"Confidence: {segment.confidence}",
            f"Status: {segment.status}",
            f"Evidence: {segment.evidence}",
            "",
        ]