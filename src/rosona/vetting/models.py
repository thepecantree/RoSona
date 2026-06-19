from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


RiskLevel = Literal[
    "low",
    "watch",
    "elevated",
    "high",
]


@dataclass(frozen=True, slots=True)
class VettingIndicator:
    code: str
    level: RiskLevel
    confidence: float
    summary: str
    evidence: str


@dataclass(frozen=True, slots=True)
class VettingReport:
    user_id: int
    level: RiskLevel
    indicators: list[VettingIndicator]

    @property
    def score(self) -> int:
        weights = {
            "low": 0,
            "watch": 25,
            "elevated": 50,
            "high": 80,
        }

        if not self.indicators:
            return 0

        return min(
            100,
            sum(weights[indicator.level] for indicator in self.indicators),
        )