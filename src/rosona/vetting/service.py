from __future__ import annotations

from rosona.inventory.delta import InventoryDelta
from rosona.vetting.models import VettingIndicator, VettingReport


class VettingService:
    def evaluate_delta(
        self,
        user_id: int,
        delta: InventoryDelta | None,
    ) -> VettingReport:
        indicators: list[VettingIndicator] = []

        if delta is None:
            return VettingReport(
                user_id=user_id,
                level="low",
                indicators=[],
            )

        if delta.ownership_value_flow >= 250_000:
            indicators.append(
                VettingIndicator(
                    code="UNBALANCED_VALUE_INFLOW",
                    level="elevated",
                    confidence=0.8,
                    summary="Large ownership value inflow detected.",
                    evidence=(
                        f"Ownership value flow increased by "
                        f"{delta.ownership_value_flow:,}. "
                        f"Added value: {delta.added_value:,}. "
                        f"Removed value: {delta.removed_value:,}."
                    ),
                )
            )

        if delta.ownership_value_flow <= -250_000:
            indicators.append(
                VettingIndicator(
                    code="UNBALANCED_VALUE_OUTFLOW",
                    level="elevated",
                    confidence=0.8,
                    summary="Large ownership value outflow detected.",
                    evidence=(
                        f"Ownership value flow decreased by "
                        f"{abs(delta.ownership_value_flow):,}. "
                        f"Added value: {delta.added_value:,}. "
                        f"Removed value: {delta.removed_value:,}."
                    ),
                )
            )

        if (
            abs(delta.value_change) >= 250_000
            and abs(delta.ownership_value_flow) < 25_000
        ):
            indicators.append(
                VettingIndicator(
                    code="MARKET_REVALUATION_ONLY",
                    level="low",
                    confidence=0.95,
                    summary="Large value movement appears market-driven.",
                    evidence=(
                        f"Total value changed by {delta.value_change:,}, "
                        f"but ownership value flow was only "
                        f"{delta.ownership_value_flow:,}."
                    ),
                )
            )

        level = self._overall_level(indicators)

        return VettingReport(
            user_id=user_id,
            level=level,
            indicators=indicators,
        )

    def _overall_level(
        self,
        indicators: list[VettingIndicator],
    ) -> str:
        if any(indicator.level == "high" for indicator in indicators):
            return "high"

        if any(indicator.level == "elevated" for indicator in indicators):
            return "elevated"

        if any(indicator.level == "watch" for indicator in indicators):
            return "watch"

        return "low"