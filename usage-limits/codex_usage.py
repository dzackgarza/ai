#!/usr/bin/env python3
"""Codex CLI usage limits checker."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

from usage_base import UsageProvider
from usage_table import UsageRow


class CodexProvider(UsageProvider):
    """Codex CLI usage checker."""

    name = "Codex"
    state_dir = "codex_usage"
    ntfy_topic = "usage-updates"

    def __init__(self) -> None:
        super().__init__()
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

    def fetch_raw(self) -> dict:
        """Fetch usage from WHAM API."""
        creds = self.get_credentials()
        if not creds:
            print("Error: Not logged in. Run 'codex login'", file=sys.stderr)
            sys.exit(1)
        token = creds.get("access_token")
        if not token:
            print("Error: No access token", file=sys.stderr)
            sys.exit(1)

        try:
            resp = requests.get(
                "https://chatgpt.com/backend-api/wham/usage",
                headers={"Authorization": f"Bearer {token}"},
                timeout=30,
            )
            if resp.status_code == 401:
                print("Error: Authentication failed. Run 'codex login'", file=sys.stderr)
                sys.exit(1)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    def to_rows(self, raw: Any) -> list[UsageRow]:
        """Convert WHAM API response to UsageRow list."""
        rate_limit = raw.get("rate_limit", {})
        primary = rate_limit.get("primary_window", {})
        secondary = rate_limit.get("secondary_window", {})

        rows = [
            UsageRow(
                identifier="Codex (5h)",
                pct_used=primary.get("used_percent", 0.0),
                reset_at=_ts_to_dt(primary.get("reset_at")),
            ),
        ]
        if secondary:
            rows.append(UsageRow(
                identifier="Codex (7d)",
                pct_used=secondary.get("used_percent", 0.0),
                reset_at=_ts_to_dt(secondary.get("reset_at")),
            ))
        return rows

    def should_anchor(self, rows: list[UsageRow]) -> bool:
        """Anchor when any window has never started (no reset_at) and none are exhausted.

        Same logic as Claude: both share the 5h/7d idle-window model.
        """
        if any(r.is_exhausted for r in rows):
            return False
        return any(r.reset_at is None for r in rows)

    def notify_always(self, rows: list[UsageRow]) -> None:
        """Fire when the 5h window is fresh and the 7d window isn't exhausted."""
        if self.should_anchor(rows):
            self.send_ntfy(
                "Codex Window Open",
                "Codex 5h window open!\n\nFresh session available for work.",
                tags="white_check_mark,rocket",
            )

    def anchor_command(self) -> list[str]:
        return ["codex", "exec", "-c", "project_doc_max_bytes=0", "Say hello and do nothing else"]


def _ts_to_dt(ts: int | None) -> datetime | None:
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Codex usage limits checker")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--no-notify", action="store_true", help="Disable auto-notification")
    parser.add_argument("--no-anchor", action="store_true", help="Disable auto-anchoring")
    args = parser.parse_args()

    CodexProvider().run(args)


if __name__ == "__main__":
    main()
