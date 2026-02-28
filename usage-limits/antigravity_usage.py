#!/usr/bin/env python3
"""Antigravity usage limits checker — wraps the antigravity-usage CLI."""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

from usage_base import UsageProvider
from usage_table import UsageRow


class AntigravityProvider(UsageProvider):
    """Antigravity usage checker.

    Wraps `antigravity-usage quota --all-models --refresh --json` (global install).
    Per-model quota is tracked individually; each model gets its own table row.

    Anchoring is handled entirely by the antigravity-usage npm package (wakeup cron).
    This script detects fresh quota and sends notifications.
    """

    name = "Antigravity"
    state_dir = "antigravity_usage"
    ntfy_topic = "usage-updates"
    ntfy_server = "http://localhost"

    def fetch_raw(self) -> dict:
        """Run antigravity-usage CLI and return parsed JSON."""
        cmd = ["antigravity-usage", "quota", "--all-models", "--refresh", "--json"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                if "not logged in" in result.stderr.lower():
                    print("Error: Not logged in. Run: antigravity-usage login", file=sys.stderr)
                else:
                    print(f"Error: {result.stderr}", file=sys.stderr)
                sys.exit(1)
            return json.loads(result.stdout)
        except FileNotFoundError:
            print("Error: antigravity-usage not found. Run: npm install -g antigravity-usage", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON output: {e}", file=sys.stderr)
            sys.exit(1)
        except subprocess.TimeoutExpired:
            print("Error: Command timed out", file=sys.stderr)
            sys.exit(1)

    def to_rows(self, raw: Any) -> list[UsageRow]:
        """Convert per-model quota data to UsageRow list."""
        rows = []

        for model in raw.get("models", []):
            label = model.get("label", model.get("modelId", ""))
            is_exhausted = model.get("isExhausted", False)
            remaining_pct = model.get("remainingPercentage")
            reset_time = model.get("resetTime")

            if is_exhausted:
                pct_used = 100.0
            elif remaining_pct is not None:
                pct_used = 100.0 - remaining_pct
            else:
                pct_used = 0.0

            reset_at = None
            if reset_time:
                try:
                    reset_at = datetime.fromisoformat(
                        reset_time.replace("Z", "+00:00")
                    ).astimezone(timezone.utc)
                except ValueError:
                    pass

            rows.append(UsageRow(
                identifier=f"Antigravity: {label}",
                pct_used=pct_used,
                reset_at=reset_at,
            ))

        return rows

    def should_anchor(self, rows: list[UsageRow]) -> bool:
        """Antigravity anchoring handled by the npm package — no action needed."""
        return False

    def notify_always(self, rows: list[UsageRow]) -> None:
        """Fire when all models are at < 1% — background wakeup already triggered."""
        if rows and all(r.pct_used < 1.0 for r in rows):
            self.send_ntfy(
                "Antigravity Quota Fresh",
                "All models at <1% — quota freshly available.",
                tags="white_check_mark,rocket",
            )

    # _handle_notifications() not overridden — base class schedules notifications
    # for the latest exhausted reset_at, which covers per-model quota exhaustion.


def main() -> None:
    parser = argparse.ArgumentParser(description="Antigravity usage limits checker")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--no-notify", action="store_true", help="Suppress all notifications (testing)")
    args = parser.parse_args()

    AntigravityProvider().run(args)


if __name__ == "__main__":
    main()
