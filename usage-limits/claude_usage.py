#!/usr/bin/env python3
"""Claude Code usage limits checker."""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

from usage_base import UsageProvider
from usage_table import UsageRow


class ClaudeProvider(UsageProvider):
    """Claude Code usage checker."""

    name = "Claude Code"
    state_dir = "claude_usage"
    ntfy_topic = "usage-updates"
    ntfy_server = "http://localhost"

    def __init__(self) -> None:
        super().__init__()
        self.cred_file = Path.home() / ".claude" / ".credentials.json"

    def provider_name(self) -> str:
        return "Claude"

    def get_credentials(self) -> dict:
        """Load OAuth credentials."""
        if not self.cred_file.exists():
            return {}
        try:
            data = json.loads(self.cred_file.read_text())
            return data.get("claudeAiOauth", {})
        except (json.JSONDecodeError, IOError):
            return {}

    def fetch_raw(self) -> dict:
        """Fetch usage from Claude OAuth API."""
        creds = self.get_credentials()
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

        try:
            return self._fetch_usage(token)
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 401:
                # Token expired - re-initialize auth and retry
                print("Warning: Token expired (401). Re-initializing auth...", file=sys.stderr)
                subprocess.run(["timeout", "5", "claude"], capture_output=True)
                # Reload credentials after auth re-init
                creds = self.get_credentials()
                token = creds.get("accessToken") if creds else None
                if not token:
                    print("Error: No access token after auth re-init", file=sys.stderr)
                    sys.exit(1)
                return self._fetch_usage(token)
            raise

    def _fetch_usage(self, token: str) -> dict:
        """Make the actual API call."""
        resp = requests.get(
            "https://api.anthropic.com/api/oauth/usage",
            headers={
                "Authorization": f"Bearer {token}",
                "anthropic-beta": "oauth-2025-04-20",
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def to_rows(self, raw: Any) -> list[UsageRow]:
        """Convert API response to UsageRow list."""
        rows = []

        five_hour = raw.get("five_hour", {})
        util_5h = five_hour.get("utilization", 0.0)
        reset_5h = five_hour.get("resets_at")
        rows.append(UsageRow(
            identifier="Claude (5h)",
            pct_used=util_5h,
            reset_at=_parse_dt(reset_5h),
        ))

        seven_day = raw.get("seven_day", {})
        util_7d = seven_day.get("utilization", 0.0)
        reset_7d = seven_day.get("resets_at")
        rows.append(UsageRow(
            identifier="Claude (7d)",
            pct_used=util_7d,
            reset_at=_parse_dt(reset_7d),
        ))

        return rows

    def should_anchor(self, rows: list[UsageRow]) -> bool:
        """Anchor when any window has never started (no reset_at) and none are exhausted.

        | 5h          | 7d          | Anchor? |
        |-------------|-------------|---------|
        | no reset    | no reset    | Yes     |
        | no reset    | active      | Yes     |
        | no reset    | exhausted   | No      |
        | active      | no reset    | Yes     |
        | active      | active      | No      |
        | active      | exhausted   | No      |
        | exhausted   | any         | No      |
        """
        if any(r.is_exhausted for r in rows):
            return False
        return any(r.reset_at is None for r in rows)

    def notify_always(self, rows: list[UsageRow]) -> None:
        """Fire when the 5h window is fresh and the 7d window isn't exhausted."""
        if self.should_anchor(rows):
            self.send_ntfy(
                "Claude Window Open",
                "Claude Code 5h window open!\n\nFresh session available for work.",
                tags="white_check_mark,rocket",
            )

    def anchor_command(self) -> list[str]:
        return ["claude", "--setting-sources", "", "Say hello and do nothing else"]


def _parse_dt(ts: str | None) -> datetime | None:
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Claude Code usage limits checker")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--no-notify", action="store_true", help="Disable auto-notification")
    parser.add_argument("--no-anchor", action="store_true", help="Disable auto-anchoring")
    parser.add_argument("--availability", "-a", action="store_true", help="Output availability data as JSON")
    args = parser.parse_args()

    ClaudeProvider().run(args)


if __name__ == "__main__":
    main()
