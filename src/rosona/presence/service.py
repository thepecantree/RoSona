from datetime import UTC, datetime

from rosona.presence.models import LastSeenEstimate, LastSeenSignal
from rosona.presence.store import PresenceStore
from rosona.roblox.client import RobloxClient


class PresenceService:
    def __init__(self, client: RobloxClient, store: PresenceStore):
        self.client = client
        self.store = store

    async def observe_now(self, user_id: int) -> LastSeenSignal | None:
        data = await self.client.request(
            "POST",
            "presence",
            "v1/presence/users",
            json={"userIds": [user_id]},
        )

        presences = data.get("userPresences", [])

        if not presences:
            return None

        presence = presences[0]
        presence_type = presence.get("userPresenceType")

        # Roblox presence types are typically:
        # 0 = offline, 1 = online, 2 = in game, 3 = in studio.
        if presence_type in (1, 2, 3):
            signal = LastSeenSignal(
                user_id=user_id,
                timestamp=datetime.now(UTC).isoformat(),
                source="official_presence_now",
                confidence=1.0,
                evidence=f"Observed current Roblox presence type {presence_type}.",
            )
            self.store.add_signal(signal)
            return signal

        return None

    def import_signal(
        self,
        user_id: int,
        timestamp: str,
        source: str = "third_party_observed",
        confidence: float = 0.8,
        evidence: str | None = None,
    ) -> LastSeenSignal:
        signal = LastSeenSignal(
            user_id=user_id,
            timestamp=timestamp,
            source=source,  # type: ignore[arg-type]
            confidence=confidence,
            evidence=evidence,
        )

        self.store.add_signal(signal)
        return signal

    def estimate(self, user_id: int) -> LastSeenEstimate:
        signals = self.store.get_signals(user_id)

        if not signals:
            unknown = LastSeenSignal(
                user_id=user_id,
                timestamp=None,
                source="unknown",
                confidence=0.0,
                evidence="No last-seen signals are available for this user yet.",
            )

            return LastSeenEstimate(
                user_id=user_id,
                best_estimate=unknown,
                signals=[unknown],
            )

        best = sorted(
            signals,
            key=lambda signal: (
                signal.confidence,
                signal.timestamp or "",
            ),
            reverse=True,
        )[0]

        return LastSeenEstimate(
            user_id=user_id,
            best_estimate=best,
            signals=signals,
        )