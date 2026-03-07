#!/usr/bin/env python3
"""OpenRouter usage limits checker.

OpenRouter does NOT expose free tier request counts via its API (only credits
are tracked). fetch_raw() is not yet implemented — a mechanism to count daily
requests is needed that does not rely on third-party observability tooling.

Known constraints:
- Free tier: 50 req/day if credits were never purchased; 1000 req/day otherwise.
- Daily limit resets at UTC midnight.
- OpenRouter API tracks credits, not request counts.

TODO: Implement fetch_raw() with a request-counting mechanism that does not
depend on third-party observability infrastructure.
"""

import argparse
from datetime import datetime, timedelta, timezone
from typing import Any

from usage_base import UsageProvider
from usage_table import UsageRow


class OpenRouterProvider(UsageProvider):
    """OpenRouter daily request quota tracker.

    Free tier: 50 req/day (never purchased credits) or 1000 req/day (credits
    purchased at least once). Resets at UTC midnight.
    """

    name = "OpenRouter"
    state_dir = "openrouter_usage"
    ntfy_topic = "usage-updates"
    ntfy_server = "http://localhost"

    FREE_DAILY_LIMIT = 1000  # 1000/day if credits ever purchased; 50/day if never paid

    def fetch_raw(self) -> dict:
        """Fetch today's OpenRouter request count.

        NOT IMPLEMENTED. Must return {"count": N} where N is the number of
        free-tier model requests made today (UTC).

        The count must distinguish free-tier model calls (model ID contains
        ":free") from paid calls. Reset boundary is UTC midnight.
        """
        raise NotImplementedError(
            "OpenRouter does not expose request counts via its API. "
            "A tracking mechanism needs to be implemented."
        )

    def to_rows(self, raw: Any) -> list[UsageRow]:
        request_count = raw.get("count", 0)
        pct_used = (request_count / self.FREE_DAILY_LIMIT * 100) if self.FREE_DAILY_LIMIT > 0 else 0.0
        now = datetime.now(timezone.utc)
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        return [UsageRow(identifier="OpenRouter (daily)", pct_used=pct_used, reset_at=tomorrow)]

    def should_anchor(self, rows: list[UsageRow]) -> bool:
        """Daily limit resets automatically at UTC midnight — no anchoring needed."""
        return False

    def notify_always(self, rows: list[UsageRow]) -> None:
        """Fire when daily limit is fresh (0 requests used)."""
        daily_row = next((r for r in rows if "daily" in r.identifier), None)
        if daily_row and daily_row.pct_used == 0:
            self.send_ntfy(
                "OpenRouter Daily Reset",
                f"OpenRouter daily limit reset!\n\n{self.FREE_DAILY_LIMIT} requests available.",
                tags="white_check_mark,rocket",
            )

    def _handle_notifications(self, rows: list[UsageRow]) -> None:
        """Schedule notification when daily limit exhausted."""
        daily_row = next((r for r in rows if "daily" in r.identifier), None)
        if not daily_row or not daily_row.is_exhausted or not daily_row.reset_at:
            return
        notif_id = f"openrouter-daily-{int(daily_row.reset_at.timestamp())}"
        if self._notification_scheduled(notif_id):
            print("ℹ️  Notification already scheduled")
            return
        success, msg = self._schedule_notification(
            reset_dt=daily_row.reset_at,
            summary=f"Daily request limit reset ({self.FREE_DAILY_LIMIT} requests)",
            notif_id=notif_id,
            title="OpenRouter Daily Reset",
        )
        if success:
            print(f"🔔 Notification scheduled for {msg}")
        else:
            print(f"✗ Failed to schedule: {msg}")


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenRouter usage limits checker")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--no-notify", action="store_true", help="Disable auto-notification")
    args = parser.parse_args()
    OpenRouterProvider().run(args)


if __name__ == "__main__":
    main()
