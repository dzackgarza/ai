#!/usr/bin/env python3
"""Ollama Cloud usage limits checker."""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from typing import Any

import requests
from bs4 import BeautifulSoup

from usage_base import UsageProvider
from usage_table import UsageRow


class OllamaProvider(UsageProvider):
    """Ollama Cloud usage checker."""

    name = "Ollama Cloud"
    state_dir = "ollama_usage"
    ntfy_topic = "usage-updates"
    ntfy_server = "http://localhost"

    def __init__(self) -> None:
        super().__init__()
        self.cookie = os.environ.get("OLLAMA_SESSION_COOKIE")

    def provider_name(self) -> str:
        return "Ollama"

    def get_session_cookie(self) -> str:
        """Get session cookie from environment."""
        if not self.cookie:
            print(
                "Error: OLLAMA_SESSION_COOKIE not set.\n"
                "Add it to ~/.envrc and run 'direnv allow' or export it manually.",
                file=sys.stderr,
            )
            sys.exit(1)
        return self.cookie

    def parse_cookie_string(self, cookie_str: str) -> dict:
        """Parse cookie string into dict."""
        cookies = {}
        for part in cookie_str.split(";"):
            part = part.strip()
            if "=" in part:
                key, value = part.split("=", 1)
                cookies[key.strip()] = value.strip()
        return cookies

    def fetch_raw(self) -> dict:
        """Fetch usage from Ollama Cloud settings page."""
        cookie_str = self.get_session_cookie()
        cookies = self.parse_cookie_string(cookie_str)

        response = requests.get(
            "https://ollama.com/settings",
            cookies=cookies,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml",
            },
            timeout=30,
            allow_redirects=False,
        )

        # Check if we were redirected (cookie expired)
        if response.status_code in (301, 302, 303, 307, 308):
            print(
                f"Error: Session cookie expired. Got redirect to: {response.headers.get('Location', 'unknown')}",
                file=sys.stderr,
            )
            sys.exit(1)

        # Check if response contains login form
        if "signin" in response.text.lower() and "ollama.com" in response.text.lower():
            print(
                "Error: Session cookie expired or invalid. The response contains a login page.\n"
                "Get a fresh cookie from your browser's DevTools.",
                file=sys.stderr,
            )
            sys.exit(1)

        response.raise_for_status()
        return {"html": response.text}

    def to_rows(self, raw: Any) -> list[UsageRow]:
        """Convert HTML to UsageRow list."""
        html = raw.get("html", "")
        soup = BeautifulSoup(html, "html.parser")
        rows = []

        # Extract plan from badge
        plan_badge = soup.find("span", class_=lambda x: x and "capitalize" in x)
        plan = plan_badge.get_text(strip=True) if plan_badge else "unknown"

        # Map Ollama's labels to standard 5h/7d naming
        # Session = 5h window, Weekly = 7d window (same as Claude/Codex)
        label_mapping = {
            "session usage": "5h",
            "weekly usage": "7d",
        }

        # Find all usage progress sections
        for label_text in ["Session usage", "Weekly usage"]:
            label_elem = soup.find(string=lambda x: x and label_text.lower() in x.lower())
            if not label_elem:
                continue

            # Find the parent div that contains both label and percentage
            flex_container = label_elem.find_parent(
                "div", class_=lambda x: x and "flex" in x and "justify-between" in x
            )
            if not flex_container:
                continue

            # Find percentage from sibling span (e.g., "0% used")
            percentage = None
            percentage_span = flex_container.find(
                "span", string=lambda x: x and "%" in x and "used" in x.lower()
            )
            if percentage_span:
                text = percentage_span.get_text(strip=True)
                match = re.search(r"(\d+(?:\.\d+)?)\s*%\s*used", text, re.I)
                if match:
                    percentage = float(match.group(1))

            # Navigate to the wrapper div containing progress bar and reset time
            wrapper = flex_container.find_parent("div")

            # Find reset time (div with class containing "local-time")
            reset_elem = None
            if wrapper:
                reset_elem = wrapper.find("div", class_=lambda x: x and "local-time" in x)
            reset_text = reset_elem.get_text(strip=True) if reset_elem else None
            reset_at = self._parse_reset_time(reset_text)

            # Use standard 5h/7d naming like Claude/Codex
            window_name = label_mapping.get(label_text.lower(), label_text.split()[0])
            identifier = f"Ollama ({window_name})"
            rows.append(
                UsageRow(
                    identifier=identifier,
                    pct_used=percentage if percentage is not None else 0.0,
                    reset_at=reset_at,
                )
            )

        return rows

    def _parse_reset_time(self, text: str | None) -> datetime | None:
        """Parse reset time from text like 'Resets in 5 hours' or 'Resets in 1 day'."""
        if not text:
            return None

        text_lower = text.lower().strip()
        match = re.search(r"resets in (\d+)\s*(second|minute|hour|day|week)s?", text_lower)
        if not match:
            return None

        value = int(match.group(1))
        unit = match.group(2)

        now = datetime.now(timezone.utc)
        if unit == "second":
            return now + timedelta(seconds=value)
        elif unit == "minute":
            return now + timedelta(minutes=value)
        elif unit == "hour":
            return now + timedelta(hours=value)
        elif unit == "day":
            return now + timedelta(days=value)
        elif unit == "week":
            return now + timedelta(weeks=value)

        return None

    def should_anchor(self, rows: list[UsageRow]) -> bool:
        """Anchor when 5h window has no reset_at and isn't exhausted.

        Same logic as Claude/Codex:
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
        five_hour = next((r for r in rows if "5h" in r.identifier), None)
        if not five_hour:
            return False
        if five_hour.is_exhausted:
            return False
        return five_hour.reset_at is None or any(r.reset_at is None for r in rows)

    def notify_always(self, rows: list[UsageRow]) -> None:
        """Fire when the 5h window is fresh (< 50% used)."""
        five_hour_rows = [r for r in rows if "5h" in r.identifier]
        for row in five_hour_rows:
            if row.pct_used < 50:
                self.send_ntfy(
                    "Ollama Window Open",
                    "Ollama Cloud 5h window open!\n\nFresh session available for work.",
                    tags="white_check_mark,rocket",
                )
                return

    def anchor_command(self) -> list[str]:
        """Run a minimal inference request to anchor the 5h window.

        Uses `ollama run` with a cloud model to start the session window.
        Uses glm-4.6:cloud (small, fast cloud model).
        """
        return [
            "ollama",
            "run",
            "glm-4.6:cloud",
            "hi",
        ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Ollama Cloud usage limits checker")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--no-notify", action="store_true", help="Disable auto-notification")
    parser.add_argument("--no-anchor", action="store_true", help="Disable auto-anchoring")
    parser.add_argument("--availability", "-a", action="store_true", help="Output availability data as JSON")
    args = parser.parse_args()

    OllamaProvider().run(args)


if __name__ == "__main__":
    main()
