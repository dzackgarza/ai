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


class ClaudeChecker(UsageChecker):
    """Claude Code usage checker."""

    def __init__(self):
        super().__init__(
            name="Claude Code",
            state_dir="claude_usage",
            ntfy_topic="usage-updates",
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

    def get_windows(self, usage: dict) -> dict[str, tuple[float, Optional[str]]]:
        """Extract windows dict from usage data."""
        five_hour = usage.get("five_hour", {})
        seven_day = usage.get("seven_day", {})
        return {
            "5h": (five_hour.get("utilization", 0), five_hour.get("resets_at")),
            "7d": (seven_day.get("utilization", 0), seven_day.get("resets_at")),
        }

    def render_summary(self, usage: dict) -> None:
        """Render rich summary."""
        windows = self.get_windows(usage)
        super().render_summary("Claude Code Usage Limits", windows)

    def get_summary_text(self, usage: dict) -> str:
        """Get plain text summary for notifications."""
        windows = self.get_windows(usage)
        lines = [f"{label}: {util:.0f}%" for label, (util, _) in windows.items()]
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Claude Code usage limits checker")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--no-notify", action="store_true", help="Disable auto-notification when exhausted")
    parser.add_argument("--no-anchor", action="store_true", help="Disable auto-anchoring idle windows")
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
    windows = checker.get_windows(usage)
    
    if not args.no_anchor and checker.should_anchor(windows):
        if not args.json:
            print("🔓 Window idle — anchoring...")
        if checker.anchor_window(checker.anchor_command()):
            usage = checker.fetch_usage(token)
            windows = checker.get_windows(usage)
            if not args.json:
                print("✓ Window anchored\n")
            
            # Notify that fresh window is available
            if not args.no_notify:
                message = "Claude Code session window open!\n\nFresh 5-hour window available for work."
                if checker.send_ntfy_notification("Claude Window Open", message, at=None, tags="white_check_mark,rocket"):
                    if not args.json:
                        print("🔔 Fresh window notification sent")
        else:
            if not args.json:
                print("✗ Failed to anchor window\n")

    # Output
    if args.json:
        print(json.dumps(usage, indent=2))
    else:
        summary = checker.get_summary_text(usage)
        checker.render_summary(usage)

        # Auto-schedule notification for blocking window
        if not args.no_notify:
            do_notify, blocking_reset = checker.should_notify(windows)
            
            if do_notify:
                notif_id = checker.get_notification_id(windows)
                
                # Check if already scheduled (via ntfy API)
                if checker.check_notification_scheduled(notif_id):
                    print("ℹ️  Notification already scheduled")
                else:
                    success, msg = checker.schedule_notification(
                        reset_dt=blocking_reset,
                        summary=summary,
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
