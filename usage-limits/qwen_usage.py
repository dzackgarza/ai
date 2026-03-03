#!/usr/bin/env python3
"""Qwen Code usage limits checker.

Qwen Code free tier: 1000 requests/day (resets at UTC midnight).
Usage is tracked via local OpenAI logging files in ~/qwen-logs/.

Setup:
1. Enable OpenAI logging in ~/.qwen/settings.json:
   {
     "model": {
       "enableOpenAILogging": true,
       "openAILoggingDir": "~/qwen-logs"
     }
   }
2. Logs will be created at ~/qwen-logs/openai-*.json
"""

import argparse
import glob
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from usage_base import UsageProvider
from usage_table import UsageRow


class QwenProvider(UsageProvider):
    """Qwen Code usage checker.

    Qwen Code free tier: 1000 requests/day (resets at UTC midnight).
    Counts requests by reading local log files.
    """

    name = "Qwen Code"
    state_dir = "qwen_usage"
    ntfy_topic = "usage-updates"
    ntfy_server = "http://localhost"

    FREE_DAILY_LIMIT = 1000  # 1000 requests/day free tier

    def __init__(self) -> None:
        super().__init__()
        self.log_dir = Path.home() / "qwen-logs"

    def provider_name(self) -> str:
        return "Qwen"

    def fetch_raw(self) -> dict:
        """Count today's requests from local log files.

        Each log file represents one API request. Files are named with
        timestamps: openai-YYYY-MM-DDTHH-MM-SS.mmmZ-*.json

        Returns dict with 'count' key containing today's request count.
        """
        if not self.log_dir.exists():
            print(
                f"Error: Log directory {self.log_dir} does not exist.\n"
                "\nSetup:\n"
                "1. Enable OpenAI logging in ~/.qwen/settings.json:\n"
                "   {\n"
                "     \"model\": {\n"
                "       \"enableOpenAILogging\": true,\n"
                "       \"openAILoggingDir\": \"~/qwen-logs\"\n"
                "     }\n"
                "   }",
                file=sys.stderr,
            )
            sys.exit(1)

        # Calculate today's UTC start
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        today_str = today_start.strftime("%Y-%m-%d")

        # Count log files from today
        pattern = str(self.log_dir / f"openai-{today_str}T*.json")
        log_files = glob.glob(pattern)

        return {"count": len(log_files)}

    def to_rows(self, raw: Any) -> list[UsageRow]:
        """Convert request count to UsageRow list.

        raw is {"count": N} where N is today's Qwen request count.
        """
        rows = []

        request_count = raw.get("count", 0)

        # Calculate percentage of daily limit used
        pct_used = (request_count / self.FREE_DAILY_LIMIT * 100) if self.FREE_DAILY_LIMIT > 0 else 0.0

        # Calculate reset time (next UTC midnight)
        now = datetime.now(timezone.utc)
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        rows.append(UsageRow(
            identifier="Qwen (daily)",
            pct_used=pct_used,
            reset_at=tomorrow,
        ))

        return rows

    def should_anchor(self, rows: list[UsageRow]) -> bool:
        """Qwen daily limit resets automatically at UTC midnight — no anchoring."""
        return False

    def notify_always(self, rows: list[UsageRow]) -> None:
        """Fire when daily limit is fresh (0 requests used)."""
        daily_row = next((r for r in rows if "daily" in r.identifier), None)
        if daily_row and daily_row.pct_used == 0:
            self.send_ntfy(
                "Qwen Daily Reset",
                f"Qwen Code daily limit reset!\n\n{self.FREE_DAILY_LIMIT} requests available.",
                tags="white_check_mark,rocket",
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Qwen Code usage limits checker")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--no-notify", action="store_true", help="Disable auto-notification")
    parser.add_argument("--no-anchor", action="store_true", help="Disable auto-anchoring")
    parser.add_argument("--availability", "-a", action="store_true", help="Output availability data as JSON")
    args = parser.parse_args()

    QwenProvider().run(args)


if __name__ == "__main__":
    main()
