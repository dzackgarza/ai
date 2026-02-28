#!/usr/bin/env python3
"""Claude Code usage limits checker."""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import requests

from usage_common import UsageChecker
from usage_table import ModelRow, UsageTable


class ClaudeChecker(UsageChecker):
    """Claude Code usage checker."""

    def __init__(self):
        super().__init__(
            name="Claude Code",
            state_dir="claude_usage",
            ntfy_topic="usage-updates",
            ntfy_server="http://localhost",
        )
        self.cred_file = Path.home() / ".claude" / ".credentials.json"

    def get_credentials(self) -> dict:
        """Load OAuth credentials."""
        if not self.cred_file.exists():
            return {}
        try:
            data = json.loads(self.cred_file.read_text())
            return data.get("claudeAiOauth", {})
        except (json.JSONDecodeError, IOError):
            return {}

    def fetch_usage(self, token: str) -> dict:
        """Fetch usage from OAuth API."""
        resp = requests.get(
            "https://api.anthropic.com/api/oauth/usage",
            headers={
                "Authorization": f"Bearer {token}",
                "anthropic-beta": "oauth-2025-04-20",
            },
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()

    def anchor_command(self) -> list[str]:
        """Command to anchor idle window."""
        return ["claude", "--setting-sources", "", "Say hello and do nothing else"]

    def get_model_rows(self, usage: dict) -> list[ModelRow]:
        """Convert usage data to ModelRow list."""
        rows = []
        five_hour = usage.get("five_hour", {})
        seven_day = usage.get("seven_day", {})

        util_5h = five_hour.get("utilization", 0)
        reset_5h = five_hour.get("resets_at")
        reset_5h_str = UsageTable.format_reset_time(reset_5h) if reset_5h else ""
        rows.append(ModelRow(
            family="Claude",
            model="5h",
            pct_used=util_5h,
            reset_time=reset_5h_str,
            is_exhausted=util_5h >= 100,
        ))

        util_7d = seven_day.get("utilization", 0)
        reset_7d = seven_day.get("resets_at")
        reset_7d_str = UsageTable.format_reset_time(reset_7d) if reset_7d else ""
        rows.append(ModelRow(
            family="Claude",
            model="7d",
            pct_used=util_7d,
            reset_time=reset_7d_str,
            is_exhausted=util_7d >= 100,
        ))

        return rows

    def get_windows(self, rows: list[ModelRow]) -> dict[str, tuple[float, Optional[str]]]:
        """Extract windows dict from ModelRows."""
        windows = {}
        for row in rows:
            reset_at = None
            if row.reset_time and row.reset_time != "now":
                # Convert back to ISO format for scheduling
                # This is a simplification - in practice we'd store the original reset_at
                pass
            windows[row.model] = (row.pct_used, reset_at)
        return windows


def main():
    parser = argparse.ArgumentParser(description="Claude Code usage limits checker")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--no-notify", action="store_true", help="Disable auto-notification")
    parser.add_argument("--no-anchor", action="store_true", help="Disable auto-anchoring")
    args = parser.parse_args()

    checker = ClaudeChecker()

    # Load credentials
    creds = checker.get_credentials()
    if not creds:
        print("Error: Not logged in. Run 'claude login'", file=sys.stderr)
        sys.exit(1)

    token = creds.get("accessToken")
    if not token:
        print("Error: No access token", file=sys.stderr)
        sys.exit(1)
    if "user:profile" not in creds.get("scopes", []):
        print("Error: Token missing 'user:profile' scope", file=sys.stderr)
        sys.exit(1)

    # Fetch usage
    usage = checker.fetch_usage(token)

    # Auto-anchor window if idle and not exhausted
    five_hour = usage.get("five_hour", {})
    windows_data = {
        "5h": (five_hour.get("utilization", 0), five_hour.get("resets_at")),
        "7d": (seven_day.get("utilization", 0), seven_day.get("resets_at")) if (seven_day := usage.get("seven_day")) else (0, None),
    }
    
    if not args.no_anchor and checker.should_anchor(windows_data):
        if not args.json:
            print("🔓 Window idle — anchoring...")
        if checker.anchor_window(checker.anchor_command()):
            usage = checker.fetch_usage(token)
            if not args.json:
                print("✓ Window anchored\n")
        else:
            if not args.json:
                print("✗ Failed to anchor window\n")

    # Convert to ModelRows
    rows = checker.get_model_rows(usage)

    if args.json:
        print(json.dumps(usage, indent=2))
    else:
        # Render table
        table = UsageTable()
        table.render(rows, title="Claude Code Usage Limits")

        # Check for fresh window notification
        if not args.no_notify:
            five_hour_row = next((r for r in rows if r.model == "5h"), None)
            if five_hour_row and five_hour_row.pct_used == 0 and not five_hour_row.reset_time:
                message = "Claude Code session window open!\n\nFresh 5-hour window available for work."
                if checker.send_ntfy_notification("Claude Window Open", message, at=None, tags="white_check_mark,rocket"):
                    print("🔔 Fresh window notification sent")

        # Auto-schedule notification for blocking window
        if not args.no_notify:
            do_notify, blocking_reset = checker.should_notify(checker.get_windows(rows))
            if do_notify:
                notif_id = checker.get_notification_id(checker.get_windows(rows))
                if checker.check_notification_scheduled(notif_id):
                    print("ℹ️  Notification already scheduled")
                else:
                    success, msg = checker.schedule_notification(
                        reset_dt=blocking_reset,
                        summary="Claude Code quota exhausted",
                        state_name="notify",
                        notif_id=notif_id,
                        title="Claude Code Session Reset",
                    )
                    if success:
                        print(f"🔔 Notification scheduled for {msg}")
                    else:
                        print(f"✗ Failed to schedule: {msg}")
                        sys.exit(1)


if __name__ == "__main__":
    main()
