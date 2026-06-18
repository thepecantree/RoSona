from __future__ import annotations

from rosona.evidence.models import (
    EvidenceRecord,
)


class EvidencePolicy:
    """
    Central authority for deciding what RoSona keeps.

    If a future feature wants to persist something,
    it should go through this policy first.
    """

    @staticmethod
    def should_persist(
        evidence: EvidenceRecord,
    ) -> bool:
        return evidence.retention != "do_not_persist"

    @staticmethod
    def should_keep_latest_only(
        evidence: EvidenceRecord,
    ) -> bool:
        return evidence.retention == "latest_only"

    @staticmethod
    def should_keep_full_history(
        evidence: EvidenceRecord,
    ) -> bool:
        return evidence.retention in (
            "persist_meaningful",
            "persist_full",
            "persist_cautiously",
        )

    @staticmethod
    def is_external_reference(
        evidence: EvidenceRecord,
    ) -> bool:
        return evidence.tier == "external_reference"

    @staticmethod
    def is_runtime_state(
        evidence: EvidenceRecord,
    ) -> bool:
        return evidence.tier == "runtime_state"

    @staticmethod
    def is_observed_inference(
        evidence: EvidenceRecord,
    ) -> bool:
        return evidence.tier == "observed_inference"

    @staticmethod
    def is_granted_access(
        evidence: EvidenceRecord,
    ) -> bool:
        return evidence.tier == "granted_access"

    @staticmethod
    def is_risk_conclusion(
        evidence: EvidenceRecord,
    ) -> bool:
        return evidence.tier == "risk_conclusion"