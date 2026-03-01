#!/usr/bin/env python3
"""Abstract base class for all usage-limit providers."""

import argparse
import json
import subprocess
import tempfile
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import requests

from usage_table import UsageRow, UsageTable, ModelAvailability


class UsageProvider(ABC):
    """Abstract base for all usage-limit checkers.

    Subclasses MUST implement:
        fetch_raw()      — retrieve raw data from API or CLI
        to_rows()        — convert raw data to list[UsageRow]
        should_anchor()  — decide whether to anchor right now
        notify_always()  — fire immediate "window newly ready" notifications

    Subclasses MAY override:
        anchor_command()         — shell command to run when anchoring; None = no subprocess
        _handle_notifications()  — scheduled reset notifications (base covers exhaustion case)

    Everything else (rendering, notifications, orchestration) is centralized here.
    """

    # ── Class-level config (set in subclass) ──────────────────────────────────

    name: str        # Provider display name, e.g. "Claude Code"
    state_dir: str   # State directory name under ~/.local/state/
    ntfy_topic: str = "usage-updates"
    ntfy_server: str = "http://localhost"

    def __init__(self) -> None:
        self._state_path = Path.home() / ".local" / "state" / self.state_dir
        self._state_path.mkdir(parents=True, exist_ok=True)
        self._console_obj: Optional[object] = None  # lazy UsageTable

    # ── ABSTRACT — must implement ─────────────────────────────────────────────

    @abstractmethod
    def fetch_raw(self) -> Any:
        """Fetch raw usage data from API or CLI subprocess."""

    @abstractmethod
    def to_rows(self, raw: Any) -> list[UsageRow]:
        """Convert raw data to a uniform list of UsageRow."""

    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name (e.g., 'Claude', 'Codex', 'Ollama')."""

    # ── ABSTRACT — must implement ─────────────────────────────────────────────

    @abstractmethod
    def should_anchor(self, rows: list[UsageRow]) -> bool:
        """Anchoring decision — every provider must define its own logic.

        Return True when the provider's usage window should be started/refreshed.
        The base run() calls this unconditionally; anchor_command() is only invoked
        when this returns True.
        """

    @abstractmethod
    def notify_always(self, rows: list[UsageRow]) -> None:
        """Fire immediate "window newly available" notifications.

        Called whenever a display run happens (not gated by --no-notify alone;
        see run()). Each provider defines its own fresh-window condition:
          Claude/Codex: 5h window idle and 7d not exhausted
          Amp:          credits at $10 (reset_at is None)
          Antigravity:  all models < 1% (background wakeup already fired)
        """

    # ── OPTIONAL overrides ────────────────────────────────────────────────────

    def anchor_command(self) -> Optional[list[str]]:
        """Shell command to anchor an idle window. Return None if no subprocess is needed."""
        return None

    # ── ABC-level convenience methods ─────────────────────────────────────────

    def _available_now(self, rows: list[UsageRow]) -> bool:
        """Internal helper: check if 5h window is open and 7d is not exhausted.
        
        Default logic for 5h/7d window providers:
        - 7d=100% always blocks
        - 5h=100% blocks
        - Otherwise available
        """
        five_hour = next((r for r in rows if "5h" in r.identifier), None)
        seven_day = next((r for r in rows if "7d" in r.identifier), None)
        
        if seven_day and seven_day.is_exhausted:
            return False
        if five_hour and five_hour.is_exhausted:
            return False
        return True

    def _available_when(self, rows: list[UsageRow]) -> datetime | None:
        """Internal helper: get when the provider becomes available.
        
        Default logic for 5h/7d window providers:
        - 7d=100% → return 7d reset
        - 5h=100% → return 5h reset
        - Otherwise → None (available now)
        """
        five_hour = next((r for r in rows if "5h" in r.identifier), None)
        seven_day = next((r for r in rows if "7d" in r.identifier), None)
        
        if seven_day and seven_day.is_exhausted and seven_day.reset_at:
            return seven_day.reset_at
        if five_hour and five_hour.is_exhausted and five_hour.reset_at:
            return five_hour.reset_at
        return None

    def availability(self, rows: list[UsageRow]) -> list[ModelAvailability]:
        """Get availability for each model/provider.

        Default implementation returns a single entry for the provider.
        Subclasses with multiple models (e.g., Antigravity) should override.
        
        Returns a list of ModelAvailability with:
        - name: provider name from provider_name()
        - available_now: True if usable right now
        - available_when: when it becomes available (None if available now)
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

        # Handle --availability flag
        if getattr(args, "availability", False):
            avail_list = self.availability(rows)
            output = [
                {
                    "name": a.name,
                    "available_now": a.available_now,
                    "available_when": a.available_when.isoformat() if a.available_when else None,
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

    def render(self, rows: list[UsageRow], title: Optional[str] = None) -> None:
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
        """Schedule ntfy notification for the blocking reset window."""
        do_notify, blocking_reset = self.should_notify(rows)
        if not do_notify or blocking_reset is None:
            return

        notif_id = self._notification_id(rows)
        if self._notification_scheduled(notif_id):
            print("ℹ️  Notification already scheduled")
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

    def should_notify(self, rows: list[UsageRow]) -> tuple[bool, Optional[datetime]]:
        """Determine if a notification should be sent, and for which reset time.

        Notify if ANY row is exhausted (≥100%). Target the LATEST reset_at
        among exhausted rows (the true blocking constraint).

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
        exhausted_resets = [
            r.reset_at for r in rows if r.is_exhausted and r.reset_at is not None
        ]
        if not exhausted_resets:
            return False, None
        return True, max(exhausted_resets)

    def send_ntfy(
        self,
        title: str,
        message: str,
        priority: str = "high",
        tags: str = "",
        at: Optional[str] = None,
    ) -> tuple[bool, Optional[str]]:
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
        """Schedule ntfy notification for reset_dt + 1 minute."""
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
        """Deterministic notification ID from exhausted rows — enables deduplication."""
        exhausted = sorted(
            (int(r.reset_at.timestamp()), r.identifier)
            for r in rows
            if r.is_exhausted and r.reset_at is not None
        )
        if not exhausted:
            return ""
        ts, _ = exhausted[-1]  # latest blocking reset
        return f"{self.name.lower().replace(' ', '-')}-{ts}"

    def _notification_scheduled(self, notif_id: str) -> bool:
        """Check if ntfy already has a scheduled message with this ID."""
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
                    if msg.get("event") == "message":
                        if f"notif_id:{notif_id}" in msg.get("tags", []):
                            return True
                except json.JSONDecodeError:
                    continue
        except requests.RequestException:
            pass
        return False

    # ── State helpers ─────────────────────────────────────────────────────────

    def _state_file(self, name: str) -> Path:
        return self._state_path / f"{name}.json"

    def load_state(self, name: str) -> dict:
        path = self._state_file(name)
        if path.exists():
            try:
                return json.loads(path.read_text())
            except (json.JSONDecodeError, IOError):
                pass
        return {}

    def save_state(self, name: str, state: dict) -> None:
        self._state_file(name).write_text(json.dumps(state, indent=2))
