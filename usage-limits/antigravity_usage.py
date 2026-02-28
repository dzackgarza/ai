#!/usr/bin/env python3
"""Antigravity usage limits checker — wraps the antigravity-usage CLI."""

import argparse
import json
import subprocess
import sys
from typing import Any

from usage_base import UsageProvider
from usage_table import UsageRow


class AntigravityProvider(UsageProvider):
    """Antigravity usage checker.

    Wraps `npx antigravity-usage quota --all-models --refresh --json`.
    Per-model quota is tracked individually; each model gets its own table row.
    Anchoring semantics differ from Claude/Codex: anchor whenever ALL models
    are at 0% usage (fresh quota just reset).

    Note: The antigravity-usage CLI handles the actual "wakeup" scheduling via
    system cron. This script only detects fresh quota and sends notifications.
    """

    name = "Antigravity"
    state_dir = "antigravity_usage"
    ntfy_topic = "usage-updates"
    ntfy_server = "http://localhost"

    def fetch_raw(self) -> dict:
        """Run antigravity-usage CLI and return parsed JSON."""
        cmd = ["npx", "antigravity-usage", "quota", "--all-models", "--refresh", "--json"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                if "not logged in" in result.stderr.lower():
                    print("Error: Not logged in. Run: npx antigravity-usage login", file=sys.stderr)
                else:
                    print(f"Error: {result.stderr}", file=sys.stderr)
                sys.exit(1)
            return json.loads(result.stdout)
        except FileNotFoundError:
            print("Error: npx not found. Install Node.js.", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON output: {e}", file=sys.stderr)
            sys.exit(1)
        except subprocess.TimeoutExpired:
            print("Error: Command timed out", file=sys.stderr)
            sys.exit(1)

    def to_rows(self, raw: Any) -> list[UsageRow]:
        """Convert per-model quota data to UsageRow list."""
        email = raw.get("email", "")
        prefix = f"{email}: " if email else ""
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
                from datetime import datetime, timezone
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
        """Anchor when ALL models are at 0% usage (fresh quota just became available)."""
        return bool(rows) and all(r.pct_used == 0.0 for r in rows)

    def anchor_command(self) -> list[str]:
        """Trigger the antigravity wakeup to start the quota window."""
        return ["npx", "antigravity-usage", "wakeup", "test"]

    def _handle_notifications(self, rows: list[UsageRow]) -> None:
        """Send immediate notification on fresh quota; schedule for exhausted windows."""
        # Immediate: notify if all models fresh (0% used)
        if rows and all(r.pct_used == 0.0 for r in rows):
            message = "Antigravity quota fresh!\n\nAll models at 0% — optimal time to run tasks."
            success, _ = self.send_ntfy(
                "Antigravity Window Open", message, tags="white_check_mark,rocket"
            )
            if success:
                print("🔔 Fresh quota notification sent")

        # Scheduled: notify for blocking exhausted window
        do_notify, blocking_reset = self.should_notify(rows)
        if not do_notify or blocking_reset is None:
            return

        notif_id = self._notification_id(rows)
        if self._notification_scheduled(notif_id):
            print("ℹ️  Notification already scheduled")
            return

        success, msg = self._schedule_notification(
            reset_dt=blocking_reset,
            summary="Antigravity quota exhausted",
            notif_id=notif_id,
            title="Antigravity Quota Reset",
        )
        if success:
            print(f"🔔 Notification scheduled for {msg}")
        else:
            print(f"✗ Failed to schedule: {msg}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Antigravity usage limits checker")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--no-notify", action="store_true", help="Disable auto-notification")
    parser.add_argument("--no-anchor", action="store_true", help="Disable auto-anchoring")
    args = parser.parse_args()

    AntigravityProvider().run(args)


if __name__ == "__main__":
    main()
