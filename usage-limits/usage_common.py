#!/usr/bin/env python3
"""Shared utilities for usage limit checkers."""

import json
import subprocess
import tempfile
from datetime import datetime, timedelta, timezone
from hashlib import md5
from pathlib import Path
from typing import Optional

import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table
from rich.text import Text


class UsageChecker:
    """Base class for usage limit checkers."""

    def __init__(
        self,
        name: str,
        state_dir: str,
        ntfy_topic: str = "usage-updates",
        ntfy_server: str = "http://localhost",
    ):
        self.name = name
        self.state_dir = Path.home() / ".local" / "state" / state_dir
        self.ntfy_topic = ntfy_topic
        self.ntfy_server = ntfy_server
        self.state_dir.mkdir(parents=True, exist_ok=True)

    # ── State Management ─────────────────────────────────────────────────────

    def _state_file(self, name: str) -> Path:
        return self.state_dir / f"{name}.json"

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

    def should_notify(self, reset_at: str, state: dict) -> bool:
        """Check if notification already scheduled for this reset time."""
        tracked = state.get("reset_at")
        if not tracked:
            return True
        # Normalize to minute precision
        def normalize(ts: str) -> str:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                return dt.strftime("%Y-%m-%d %H:%M")
            except:
                return ts
        return normalize(reset_at) != normalize(tracked)

    # ── Auto-Anchor ──────────────────────────────────────────────────────────

    def anchor_window(self, command: list[str]) -> bool:
        """Anchor a new window with minimal usage. Returns True if successful."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                command,
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0

    # ── Notifications ────────────────────────────────────────────────────────

    def send_ntfy_notification(
        self,
        title: str,
        message: str,
        priority: str = "high",
        tags: str = "",
        at: Optional[str] = None,
    ) -> tuple[bool, Optional[str]]:
        """Send notification via ntfy with optional scheduling."""
        priority_map = {
            "min": "min", "low": "low", "default": "default",
            "high": "high", "max": "urgent", "urgent": "urgent",
        }

        url = f"{self.ntfy_server}/{self.ntfy_topic}"
        headers = {
            "Title": self._sanitize_header(title),
            "Priority": priority_map.get(priority.lower(), "default"),
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

    def _sanitize_header(self, value: str) -> str:
        """Sanitize header value for ntfy (latin-1 encoding)."""
        return value.encode("latin-1", "ignore").decode("latin-1").strip()

    def schedule_notification(
        self,
        reset_dt: datetime,
        summary: str,
        state_name: str,
        notif_id: str,
        title: str = "Session Reset",
        tags: str = "white_check_mark,clock",
    ) -> tuple[bool, str]:
        """Schedule notification for reset time + 1 minute."""
        notify_dt = reset_dt + timedelta(minutes=1)
        at_time = str(int(notify_dt.timestamp()))
        
        # Include notification ID in tags for deduplication
        full_tags = f"{tags},notif_id:{notif_id}" if notif_id else tags

        success, error = self.send_ntfy_notification(
            title=title,
            message=f"{self.name} session reset!\n\n{summary}",
            priority="high",
            tags=full_tags,
            at=at_time,
        )

        if success:
            self.save_state(state_name, {
                "reset_at": reset_dt.isoformat(),
                "scheduled_at": datetime.now(timezone.utc).isoformat(),
                "notif_id": notif_id,
            })
            return True, notify_dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        return False, error or "Unknown error"

    def get_notification_id(self, windows: dict[str, tuple[float, Optional[str]]]) -> str:
        """Generate deterministic notification ID based on exhausted windows.
        
        Independent runs with same exhausted windows will generate same ID,
        enabling deduplication via scheduled message lookup.
        
        Format: {service}-{window_label}-{reset_timestamp}
        Example: claude-7d-1772570640
        """
        exhausted = []
        for label, (util, reset_at) in sorted(windows.items()):
            if util >= 100 and reset_at:
                # Convert to unix timestamp for stable ID
                reset_dt = datetime.fromisoformat(reset_at.replace("Z", "+00:00"))
                ts = int(reset_dt.timestamp())
                exhausted.append(f"{label}-{ts}")
        
        if not exhausted:
            return ""
        
        # Use latest (blocking) reset for ID
        return f"{self.name.lower().replace(' ', '-')}-{exhausted[-1]}"

    def check_notification_scheduled(self, notif_id: str) -> bool:
        """Check if a notification with given ID is already scheduled.
        
        Queries ntfy scheduled messages endpoint and checks for matching ID.
        """
        if not notif_id:
            return False
        
        url = f"{self.ntfy_server}/{self.ntfy_topic}/json"
        params = {"poll": "1", "sched": "1"}
        
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            
            # Parse NDJSON stream
            for line in resp.text.strip().split("\n"):
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    # Check if this is a scheduled message with our ID
                    if msg.get("event") == "message":
                        # Check tags for our notification ID
                        tags = msg.get("tags", [])
                        if f"notif_id:{notif_id}" in tags:
                            return True
                except json.JSONDecodeError:
                    continue
            
            return False
        except requests.RequestException:
            return False

    def get_blocking_reset(self, windows: dict[str, tuple[float, Optional[str]]]) -> Optional[datetime]:
        """Find the blocking (latest) reset time among exhausted windows.
        
        Returns datetime of latest reset among windows at 100%, or None if none exhausted.
        """
        exhausted_resets = []
        for label, (util, reset_at) in windows.items():
            if util >= 100 and reset_at:
                reset_dt = datetime.fromisoformat(reset_at.replace("Z", "+00:00"))
                exhausted_resets.append((label, reset_dt))
        
        if not exhausted_resets:
            return None
        
        return max(exhausted_resets, key=lambda x: x[1])[1]

    def should_notify(self, windows: dict[str, tuple[float, Optional[str]]]) -> tuple[bool, Optional[datetime]]:
        """Determine if auto-notification should happen.
        
        Notify logic (centralized):
        - Notify if ANY window is exhausted (≥100%)
        - Target the LATEST reset among exhausted windows (blocking constraint)
        
        Returns:
            (should_notify: bool, reset_dt: Optional[datetime])
            
        Cases:
        | 5h    | 7d    | Notify? | Target     |
        |-------|-------|---------|------------|
        | 0     | 0     | ❌      | —          |
        | 0     | 0<x   | ❌      | —          |
        | 0     | 100   | ✅      | 7d         |
        | 0<x   | 0     | ❌      | —          |
        | 0<x   | 0<x   | ❌      | —          |
        | 0<x   | 100   | ✅      | 7d         |
        | 100   | 0     | ✅      | 5h         |
        | 100   | 0<x   | ✅      | 5h         |
        | 100   | 100   | ✅      | max(5h,7d) |
        """
        blocking_reset = self.get_blocking_reset(windows)
        return (blocking_reset is not None, blocking_reset)

    def should_anchor(self, windows: dict[str, tuple[float, Optional[str]]]) -> bool:
        """Determine if auto-anchor should happen.
        
        Anchor logic (centralized):
        - Anchor if ANY window has no reset (never started)
        - BUT NOT if ANY window is exhausted (100%) - would be wasted
        
        Cases:
        | 5h    | 7d    | Anchor? | Reason                          |
        |-------|-------|---------|---------------------------------|
        | 0     | 0     | ✅      | Both idle                       |
        | 0     | 0<x   | ✅      | 7d active, 5h idle              |
        | 0     | 100   | ❌      | 7d exhausted - wasted           |
        | 0<x   | 0     | ✅      | 5h active, 7d never started     |
        | 0<x   | 0<x   | ❌      | Both active                     |
        | 0<x   | 100   | ❌      | 7d exhausted - wasted           |
        | 100   | 0     | ❌      | 5h exhausted - wasted           |
        | 100   | 0<x   | ❌      | 5h exhausted - wasted           |
        | 100   | 100   | ❌      | Both exhausted - wasted         |
        """
        # Don't anchor if any window exhausted
        for label, (util, reset_at) in windows.items():
            if util >= 100:
                return False
        
        # Anchor if any window never started (no reset time)
        for label, (util, reset_at) in windows.items():
            if not reset_at:
                return True
        
        return False

    # ── Formatting ───────────────────────────────────────────────────────────

    def format_reset_time(self, reset_at: Optional[str]) -> tuple[str, str]:
        """Format reset timestamp as (relative, absolute) tuple."""
        if not reset_at:
            return "open", ""

        reset_dt = datetime.fromisoformat(reset_at.replace("Z", "+00:00"))
        delta = reset_dt - datetime.now(timezone.utc)

        if delta.total_seconds() <= 0:
            return "now", reset_dt.astimezone().strftime("%Y-%m-%d %H:%M")

        hrs, rem = divmod(int(delta.total_seconds()), 3600)
        mins, _ = divmod(rem, 60)

        if hrs > 24:
            days = hrs // 24
            hrs %= 24
            time_str = f"in {days}d {hrs}h {mins}m"
        elif hrs > 0:
            time_str = f"in {hrs}h {mins}m"
        elif mins > 0:
            time_str = f"in {mins}m"
        else:
            return "now", reset_dt.astimezone().strftime("%Y-%m-%d %H:%M")

        return time_str, reset_dt.astimezone().strftime("%Y-%m-%d %H:%M")

    def status_emoji(self, utilization: float) -> str:
        """Get status emoji based on utilization."""
        if utilization >= 100:
            return "🔴"
        if utilization >= 80:
            return "🟠"
        if utilization >= 60:
            return "🟡"
        return "🟢"

    def format_reset_time(self, reset_at: Optional[str]) -> tuple[str, str]:
        """Format reset timestamp as (relative, absolute) tuple."""
        if not reset_at:
            return "open", ""

        reset_dt = datetime.fromisoformat(reset_at.replace("Z", "+00:00"))
        delta = reset_dt - datetime.now(timezone.utc)

        if delta.total_seconds() <= 0:
            return "now", reset_dt.astimezone().strftime("%Y-%m-%d %H:%M")

        hrs, rem = divmod(int(delta.total_seconds()), 3600)
        mins, _ = divmod(rem, 60)

        if hrs > 24:
            days = hrs // 24
            hrs %= 24
            time_str = f"in {days}d {hrs}h {mins}m"
        elif hrs > 0:
            time_str = f"in {hrs}h {mins}m"
        elif mins > 0:
            time_str = f"in {mins}m"
        else:
            return "now", reset_dt.astimezone().strftime("%Y-%m-%d %H:%M")

        return time_str, reset_dt.astimezone().strftime("%Y-%m-%d %H:%M")

    def format_summary_header(self, title: str) -> Text:
        """Format header as rich Text."""
        return Text(title, style="bold cyan")

    def format_window(self, label: str, utilization: float, reset_at: Optional[str]) -> Table:
        """Format a single usage window with progress bar."""
        emoji = self.status_emoji(utilization)
        time_str, at_str = self.format_reset_time(reset_at)

        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("label", style="bold")
        table.add_column("value")

        # Progress bar with color based on usage
        bar_color = "green" if utilization < 60 else "yellow" if utilization < 100 else "red"
        
        # Build bar manually for better visibility at low percentages
        bar_width = 40
        filled = int(bar_width * utilization / 100)
        if utilization > 0 and filled == 0:
            filled = 1  # Show at least something for >0%
        bar_str = "━" * filled + "─" * (bar_width - filled)
        
        table.add_row(f"{emoji} {label}:", f"[{bar_color}]{bar_str}[/{bar_color}] [bold]{utilization:5.1f}%[/bold]")
        if at_str:
            table.add_row("", f"Resets {time_str} ({at_str})")
        else:
            table.add_row("", f"Status: {time_str}")

        return table

    def render_summary(self, title: str, windows: dict[str, tuple[float, Optional[str]]]) -> None:
        """Render complete summary using rich."""
        console = Console()

        # Header panel
        console.print(Panel(self.format_summary_header(title), border_style="cyan"))
        console.print()

        # Usage windows
        for label, (util, reset_at) in windows.items():
            console.print(self.format_window(label, util, reset_at))
            console.print()
