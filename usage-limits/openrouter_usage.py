#!/usr/bin/env python3
"""OpenRouter usage limits checker via Langfuse observability.

OpenRouter does NOT expose free tier request counts via its API.
This script queries Langfuse (which receives traces via OpenRouter Broadcast)
to count requests and track the 50 requests/day free tier limit.

Setup:
1. Create Langfuse account at https://cloud.langfuse.com (free, no credit card)
2. Get API keys from Settings > API Keys
3. Enable OpenRouter Broadcast: OpenRouter Settings > Observability > Langfuse
4. Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY in environment

Note: Langfuse free tier limits Metrics API to 100 requests/day.
"""

import argparse
import base64
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

from usage_base import UsageProvider
from usage_table import UsageRow


class OpenRouterProvider(UsageProvider):
    """OpenRouter usage checker via Langfuse.

    OpenRouter free tier: 50 requests/day (resets at UTC midnight).
    Langfuse receives traces via OpenRouter Broadcast and exposes Metrics API.
    """

    name = "OpenRouter"
    state_dir = "openrouter_usage"
    ntfy_topic = "usage-updates"
    ntfy_server = "http://localhost"

    FREE_DAILY_LIMIT = 1000  # 1000/day if purchased credits, 50/day if never paid

    def __init__(self) -> None:
        super().__init__()
        self.langfuse_public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
        self.langfuse_secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
        self.langfuse_host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")

    def provider_name(self) -> str:
        return "OpenRouter"

    def get_basic_auth(self) -> str:
        """Get Basic Auth header value."""
        if not self.langfuse_public_key or not self.langfuse_secret_key:
            print(
                "Error: LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY not set.\n"
                "\nSetup:\n"
                "1. Create Langfuse account at https://cloud.langfuse.com (free, no credit card)\n"
                "2. Get keys from Settings > API Keys\n"
                "3. Enable OpenRouter Broadcast: OpenRouter Settings > Observability > Langfuse\n"
                "4. Add to ~/.envrc:\n"
                "   export LANGFUSE_PUBLIC_KEY=pk-lf-...\n"
                "   export LANGFUSE_SECRET_KEY=sk-lf-...",
                file=sys.stderr,
            )
            sys.exit(1)
        credentials = f"{self.langfuse_public_key}:{self.langfuse_secret_key}"
        return base64.b64encode(credentials.encode()).decode()

    def fetch_raw(self) -> dict:
        """Fetch today's OpenRouter traces from Langfuse API.

        The traces endpoint has much higher rate limits (1000 req/min for Hobby)
        compared to the metrics endpoint (100 req/day).

        Returns dict with 'count' key containing today's trace count.
        """
        auth_header = self.get_basic_auth()

        # Calculate today's UTC start
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        try:
            # Query traces filtered by name and date
            url = f"{self.langfuse_host}/api/public/traces"
            params = {
                "name": "OpenRouter Request",
                "page": 1,
                "limit": 100,
            }
            resp = requests.get(
                url,
                headers={"Authorization": f"Basic {auth_header}"},
                params=params,
                timeout=30,
            )
            if resp.status_code == 401:
                print("Error: Invalid Langfuse API keys", file=sys.stderr)
                sys.exit(1)
            resp.raise_for_status()
            data = resp.json()

            # Count traces from today
            traces = data.get("data", [])
            today_count = sum(
                1 for t in traces
                if t.get("timestamp", "") > today_start.isoformat().replace("+00:00", "Z")
            )

            return {"count": today_count}
        except requests.RequestException as e:
            print(f"Error querying Langfuse: {e}", file=sys.stderr)
            sys.exit(1)

    def to_rows(self, raw: Any) -> list[UsageRow]:
        """Convert trace count to UsageRow list.

        raw is {"count": N} where N is today's OpenRouter request count.
        """
        rows = []

        request_count = raw.get("count", 0)

        # Calculate percentage of daily limit used
        pct_used = (request_count / self.FREE_DAILY_LIMIT * 100) if self.FREE_DAILY_LIMIT > 0 else 0.0

        # Calculate reset time (next UTC midnight)
        now = datetime.now(timezone.utc)
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        rows.append(UsageRow(
            identifier="OpenRouter (daily)",
            pct_used=pct_used,
            reset_at=tomorrow,
        ))

        return rows

    def should_anchor(self, rows: list[UsageRow]) -> bool:
        """OpenRouter daily limit resets automatically at UTC midnight — no anchoring."""
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
    parser = argparse.ArgumentParser(description="OpenRouter usage limits checker (via Langfuse)")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--no-notify", action="store_true", help="Disable auto-notification")
    parser.add_argument("--availability", "-a", action="store_true", help="Output availability data as JSON")
    args = parser.parse_args()

    OpenRouterProvider().run(args)


if __name__ == "__main__":
    main()
