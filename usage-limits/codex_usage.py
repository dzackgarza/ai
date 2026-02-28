#!/usr/bin/env python3
"""Codex CLI usage limits checker."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests
from usage_common import UsageChecker


class CodexChecker(UsageChecker):
    """Codex CLI usage checker."""

    def __init__(self):
        super().__init__(
            name="Codex",
            state_dir="codex_usage",
            ntfy_topic="usage-updates",
        )
        self.auth_file = Path.home() / ".codex" / "auth.json"

    def get_credentials(self) -> dict:
        """Load auth credentials."""
        if not self.auth_file.exists():
            return {}
        try:
            data = json.loads(self.auth_file.read_text())
            return data.get("tokens", {})
        except (json.JSONDecodeError, IOError):
            return {}

    def fetch_usage(self, token: str) -> dict:
        """Fetch usage from WHAM API."""
        resp = requests.get(
            "https://chatgpt.com/backend-api/wham/usage",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30
        )
        if resp.status_code == 401:
            raise PermissionError("Authentication failed")
        resp.raise_for_status()
        return resp.json()

    def get_windows(self, usage: dict) -> dict[str, tuple[float, Optional[str]]]:
        """Extract windows dict from usage data."""
        rate_limit = usage.get("rate_limit", {})
        primary = rate_limit.get("primary_window", {})
        secondary = rate_limit.get("secondary_window", {})
        return {
            "5h": (primary.get("used_percent", 0), self._ts_to_iso(primary.get("reset_at"))),
            "7d": (secondary.get("used_percent", 0) if secondary else 0, self._ts_to_iso(secondary.get("reset_at")) if secondary else None),
        }

    def render_summary(self, usage: dict) -> None:
        """Render rich summary."""
        windows = self.get_windows(usage)
        super().render_summary("Codex Usage Limits", windows)

    def get_summary_text(self, usage: dict) -> str:
        """Get plain text summary for notifications."""
        windows = self.get_windows(usage)
        lines = [f"{label}: {util:.0f}%" for label, (util, _) in windows.items()]
        return "\n".join(lines)

    def _ts_to_iso(self, ts: int | None) -> str | None:
        """Convert unix timestamp to ISO format."""
        if ts is None:
            return None
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def main():
    parser = argparse.ArgumentParser(description="Codex usage limits checker")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--no-notify", action="store_true", help="Disable auto-notification")
    args = parser.parse_args()

    checker = CodexChecker()

    # Load credentials
    creds = checker.get_credentials()
    if not creds:
        print("Error: Not logged in. Run 'codex login'", file=sys.stderr)
        sys.exit(1)

    token = creds.get("access_token")
    if not token:
        print("Error: No access token", file=sys.stderr)
        sys.exit(1)

    # Fetch usage
    try:
        usage = checker.fetch_usage(token)
    except PermissionError:
        print("Error: Authentication failed. Run 'codex login'", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.json:
        print(json.dumps(usage, indent=2))
    else:
        summary = checker.get_summary_text(usage)
        windows = checker.get_windows(usage)
        checker.render_summary(usage)

        # Notify when fresh window available (0% with no reset)
        if not args.no_notify:
            five_hour = windows.get("5h", (0, None))
            if five_hour[0] == 0 and not five_hour[1]:
                message = "Codex session window open!\n\nFresh 5-hour window available for work."
                if checker.send_ntfy_notification("Codex Window Open", message, at=None, tags="white_check_mark,rocket"):
                    print("\n🔔 Fresh window notification sent")
        
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
                        title="Codex Session Reset",
                    )
                    if success:
                        print(f"🔔 Notification scheduled for {msg}")
                    else:
                        print(f"✗ Failed to schedule: {msg}")
                        sys.exit(1)


if __name__ == "__main__":
    main()
