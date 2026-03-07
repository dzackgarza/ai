"""Abstract base class for all usage-limit providers."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import requests

from usage_limits.table import ModelAvailability, UsageRow, UsageTable

__all__ = ["UsageProvider"]


class UsageProvider(ABC):
    """Abstract base for all usage-limit checkers.

    Subclasses MUST implement:
        fetch_raw()      — retrieve raw data from API or CLI
        to_rows()        — convert raw data to list[UsageRow]
        provider_name()  — return a short display name string
        should_anchor()  — decide whether to anchor the usage window
        notify_always()  — fire immediate "window newly ready" notifications

    Subclasses MAY override:
        anchor_command()         — shell command for anchoring; None = no subprocess
        availability()           — per-model availability list (default: single entry)
        _handle_notifications()  — scheduled reset notifications
    """

    # ── Class-level config (set in subclass) ─────────────────────────────────

    name: str  # Provider display name, e.g. "Claude Code"
    state_dir: str  # State directory name under ~/.local/state/
    ntfy_topic: str = "usage-updates"
    ntfy_server: str = "http://localhost"

    def __init__(self) -> None:
        self._state_path = Path.home() / ".local" / "state" / self.state_dir
        self._state_path.mkdir(parents=True, exist_ok=True)

    # ── ABSTRACT — must implement ─────────────────────────────────────────────

    @abstractmethod
    def fetch_raw(self) -> Any:
        """Fetch raw usage data from API or CLI subprocess."""

    @abstractmethod
    def to_rows(self, raw: Any) -> list[UsageRow]:
        """Convert raw data to a uniform list of UsageRow."""

    @abstractmethod
    def provider_name(self) -> str:
        """Return a short provider name, e.g. 'Claude', 'Codex', 'Ollama'."""

    @abstractmethod
    def should_anchor(self, rows: list[UsageRow]) -> bool:
        """Return True when the provider's usage window should be started/refreshed."""

    @abstractmethod
    def notify_always(self, rows: list[UsageRow]) -> None:
        """Fire immediate notifications when a fresh usage window is detected."""

    # ── OPTIONAL overrides ────────────────────────────────────────────────────

    def anchor_command(self) -> list[str] | None:
        """Shell command to anchor an idle window. Return None if not applicable."""
        return None

    # ── Availability helpers ──────────────────────────────────────────────────

    def _available_now(self, rows: list[UsageRow]) -> bool:
        """Default availability check for 5h/7d window providers.

        Returns False if either the 7d or 5h window is exhausted.
        """
        five_hour = next((r for r in rows if "5h" in r.identifier), None)
        seven_day = next((r for r in rows if "7d" in r.identifier), None)
        if seven_day and seven_day.is_exhausted:
            return False
        return not (five_hour and five_hour.is_exhausted)

    def _available_when(self, rows: list[UsageRow]) -> datetime | None:
        """Default next-available time for 5h/7d window providers."""
        five_hour = next((r for r in rows if "5h" in r.identifier), None)
        seven_day = next((r for r in rows if "7d" in r.identifier), None)
        if seven_day and seven_day.is_exhausted and seven_day.reset_at:
            return seven_day.reset_at
        if five_hour and five_hour.is_exhausted and five_hour.reset_at:
            return five_hour.reset_at
        return None

    def availability(self, rows: list[UsageRow]) -> list[ModelAvailability]:
        """Return per-provider availability.

        Default returns a single entry. Providers with multiple independent
        models (e.g. Antigravity) should override this method.
        """
        available_now = self._available_now(rows)
        available_when = None if available_now else self._available_when(rows)
        return [
            ModelAvailability(
                name=self.provider_name(),
                available_now=available_now,
                available_when=available_when,
            )
        ]

    # ── Orchestration entrypoint ──────────────────────────────────────────────

    def run(self, args: argparse.Namespace) -> None:
        """Standard entrypoint: fetch → anchor → display → notify."""
        raw = self.fetch_raw()
        rows = self.to_rows(raw)

        if getattr(args, "availability", False):
            avail_list = self.availability(rows)
            output = [
                {
                    "name": a.name,
                    "available_now": a.available_now,
                    "available_when": (a.available_when.isoformat() if a.available_when else None),
                }
                for a in avail_list
            ]
            print(json.dumps(output, indent=2))
            return

        if not getattr(args, "no_anchor", False) and self.should_anchor(rows):
            cmd = self.anchor_command()
            if cmd:
                if not getattr(args, "json", False):
                    print("🔓 Window idle — anchoring...")
                if self._anchor_window(cmd):
                    raw = self.fetch_raw()
                    rows = self.to_rows(raw)
                    if not getattr(args, "json", False):
                        print("✓ Window anchored\n")
                else:
                    if not getattr(args, "json", False):
                        print("✗ Failed to anchor window\n")

        if getattr(args, "json", False):
            print(json.dumps(raw, indent=2))
            return

        self.render(rows)

        if not getattr(args, "no_notify", False):
            self.notify_always(rows)
            self._handle_notifications(rows)

    # ── Rendering ─────────────────────────────────────────────────────────────

    def render(self, rows: list[UsageRow], title: str | None = None) -> None:
        """Render the uniform 4-column table."""
        UsageTable().render(rows, title=title or self.name)

    # ── Anchoring ─────────────────────────────────────────────────────────────

    def _anchor_window(self, command: list[str]) -> bool:
        """Run anchoring command in a temp dir. Returns True on success."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                command,
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.returncode == 0

    # ── Notifications ─────────────────────────────────────────────────────────

    def _handle_notifications(self, rows: list[UsageRow]) -> None:
        """Schedule an ntfy notification for the blocking reset window."""
        do_notify, blocking_reset = self.should_notify(rows)
        if not do_notify or blocking_reset is None:
            return

        notif_id = self._notification_id(rows)
        if self._notification_scheduled(notif_id):
            print("i  Notification already scheduled")
            return

        success, msg = self._schedule_notification(
            reset_dt=blocking_reset,
            summary=f"{self.name} quota exhausted",
            notif_id=notif_id,
            title=f"{self.name} Session Reset",
        )
        if success:
            print(f"🔔 Notification scheduled for {msg}")
        else:
            print(f"✗ Failed to schedule: {msg}")

    def should_notify(self, rows: list[UsageRow]) -> tuple[bool, datetime | None]:
        """Determine if a reset notification should be scheduled.

        Notifies when ANY row is exhausted. Targets the LATEST exhausted
        reset_at (the true blocking constraint).

        Truth table:
        | 5h    | 7d    | Notify? | Target     |
        |-------|-------|---------|------------|
        | 100   | 0     | ✅      | 5h         |
        | 100   | 0<x   | ✅      | 5h         |
        | 100   | 100   | ✅      | max(5h,7d) |
        | 0<x   | 100   | ✅      | 7d         |
        | 0     | 100   | ✅      | 7d         |
        | *     | *<100 | ❌      | —          |
        """
        exhausted_resets = [r.reset_at for r in rows if r.is_exhausted and r.reset_at is not None]
        if not exhausted_resets:
            return False, None
        return True, max(exhausted_resets)

    def send_ntfy(
        self,
        title: str,
        message: str,
        priority: str = "high",
        tags: str = "",
        at: str | None = None,
    ) -> tuple[bool, str | None]:
        """Send an ntfy notification (immediate or scheduled)."""
        url = f"{self.ntfy_server}/{self.ntfy_topic}"
        headers: dict[str, str] = {
            "Title": title.encode("latin-1", "ignore").decode("latin-1").strip(),
            "Priority": priority,
        }
        if tags:
            headers["Tags"] = tags
        if at:
            headers["At"] = at
        try:
            resp = requests.post(url, data=message.encode("utf-8"), headers=headers, timeout=10)
            resp.raise_for_status()
            return True, None
        except requests.RequestException as e:
            return False, str(e)

    def _schedule_notification(
        self,
        reset_dt: datetime,
        summary: str,
        notif_id: str,
        title: str = "Session Reset",
        tags: str = "white_check_mark,clock",
    ) -> tuple[bool, str]:
        """Schedule an ntfy notification at reset_dt + 1 minute."""
        notify_dt = reset_dt + timedelta(minutes=1)
        at_time = str(int(notify_dt.timestamp()))
        full_tags = f"{tags},notif_id:{notif_id}" if notif_id else tags

        success, error = self.send_ntfy(
            title=title,
            message=f"{self.name} session reset!\n\n{summary}",
            priority="high",
            tags=full_tags,
            at=at_time,
        )
        if success:
            return True, notify_dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        return False, error or "Unknown error"

    def _notification_id(self, rows: list[UsageRow]) -> str:
        """Deterministic notification ID from exhausted rows (for deduplication)."""
        exhausted = sorted(
            (int(r.reset_at.timestamp()), r.identifier)
            for r in rows
            if r.is_exhausted and r.reset_at is not None
        )
        if not exhausted:
            return ""
        ts, _ = exhausted[-1]
        return f"{self.name.lower().replace(' ', '-')}-{ts}"

    def _notification_scheduled(self, notif_id: str) -> bool:
        """Return True if ntfy already has a scheduled message with this ID."""
        if not notif_id:
            return False
        url = f"{self.ntfy_server}/{self.ntfy_topic}/json"
        try:
            resp = requests.get(url, params={"poll": "1", "sched": "1"}, timeout=10)
            resp.raise_for_status()
            for line in resp.text.strip().split("\n"):
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    if msg.get("event") == "message" and f"notif_id:{notif_id}" in msg.get(
                        "tags", []
                    ):
                        return True
                except json.JSONDecodeError:
                    continue
        except requests.RequestException:
            pass
        return False

    # ── State helpers ─────────────────────────────────────────────────────────

    def _state_file(self, name: str) -> Path:
        return self._state_path / f"{name}.json"

    def load_state(self, name: str) -> dict[str, Any]:
        """Load a named JSON state file. Returns empty dict if missing or corrupt."""
        path = self._state_file(name)
        if path.exists():
            try:
                return json.loads(path.read_text())  # type: ignore[no-any-return]
            except (json.JSONDecodeError, OSError):
                pass
        return {}

    def save_state(self, name: str, state: dict[str, Any]) -> None:
        """Persist a named JSON state file."""
        self._state_file(name).write_text(json.dumps(state, indent=2))
