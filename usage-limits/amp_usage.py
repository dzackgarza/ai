#!/usr/bin/env python3
"""Amp CLI usage checker - mirrors Claude/Codex usage display."""

import argparse
import json
import math
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table


NTFY_SERVER = "http://localhost"
NTFY_TOPIC = "usage-updates"


def send_ntfy(title: str, message: str, at: str, tags: str = "white_check_mark,clock") -> bool:
    """Send scheduled ntfy notification."""
    url = f"{NTFY_SERVER}/{NTFY_TOPIC}"
    headers = {
        "Title": title.encode("latin-1", "ignore").decode("latin-1"),
        "Priority": "high",
        "Tags": tags,
        "At": at,
    }
    try:
        resp = requests.post(url, data=message.encode("utf-8"), headers=headers, timeout=10)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def check_scheduled(notif_id: str) -> bool:
    """Check if notification already scheduled."""
    url = f"{NTFY_SERVER}/{NTFY_TOPIC}/json"
    try:
        resp = requests.get(url, params={"poll": "1", "sched": "1"}, timeout=10)
        for line in resp.text.strip().split("\n"):
            if not line:
                continue
            try:
                msg = json.loads(line)
                if msg.get("event") == "message":
                    tags = msg.get("tags", [])
                    if f"notif_id:{notif_id}" in tags:
                        return True
            except json.JSONDecodeError:
                continue
    except requests.RequestException:
        pass
    return False


def parse_amp_usage(output: str) -> dict:
    """Parse amp usage CLI output."""
    result = {}
    
    # Amp Free: $X.XX/$Y remaining (replenishes +$Z/hour)
    free_match = re.search(r"Amp Free: \$(\d+\.?\d*)/\$(\d+\.?\d*) remaining \(replenishes \+\$(\d+\.?\d*)/hour\)", output)
    if free_match:
        result["remaining"] = float(free_match.group(1))
        result["total"] = float(free_match.group(2))
        result["rate_per_hour"] = float(free_match.group(3))
    
    return result


def next_topup_time(remaining: float, total: float, rate_per_hour: float) -> tuple[datetime, int]:
    """Calculate next top-up time and hours needed to full.
    
    Returns:
        (next_topup_datetime, hours_needed)
    """
    needed = total - remaining
    if needed <= 0 or rate_per_hour <= 0:
        return datetime.now(timezone.utc), 0
    
    hours_needed = math.ceil(needed / rate_per_hour)
    
    now = datetime.now(timezone.utc)
    next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    
    # First top-up at next_hour, then hourly after
    # Return time of the top-up that will make us full
    topup_time = next_hour + timedelta(hours=hours_needed - 1)
    return topup_time, hours_needed


def format_time(td: timedelta) -> str:
    """Format timedelta."""
    secs = int(td.total_seconds())
    if secs <= 0:
        return "now"
    days, rem = divmod(secs, 86400)
    hrs, rem = divmod(rem, 3600)
    mins, _ = divmod(rem, 60)
    if days > 0:
        return f"in {days}d {hrs}h"
    if hrs > 0:
        return f"in {hrs}h {mins}m"
    if mins > 0:
        return f"in {mins}m"
    return "now"


def format_summary(usage: dict, schedule_notify: bool = False) -> None:
    """Format usage like Claude/Codex - single status bar."""
    console = Console()
    
    remaining = usage.get("remaining", 0)
    total = usage.get("total", 10)
    rate = usage.get("rate_per_hour", 0)
    
    used = total - remaining
    pct = (used / total * 100) if total > 0 else 0
    
    # Status bar
    bar_color = "green" if pct < 60 else "yellow" if pct < 100 else "red"
    bar_width = 40
    filled = int(bar_width * pct / 100)
    if pct > 0 and filled == 0:
        filled = 1
    bar_str = "━" * filled + "─" * (bar_width - filled)
    
    # Next top-up time
    topup_time, hours_needed = next_topup_time(remaining, total, rate)
    is_full = hours_needed == 0
    time_to_topup = topup_time - datetime.now(timezone.utc)
    
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("label", style="bold")
    table.add_column("value")
    
    status_text = "full" if is_full else format_time(time_to_topup)
    table.add_row(
        f"🟢 Amp Free:",
        f"[{bar_color}]{bar_str}[/{bar_color}] [bold]{pct:5.1f}%[/bold]"
    )
    table.add_row("", f"{status_text} ({topup_time.astimezone().strftime('%Y-%m-%d %H:%M')})")
    table.add_row("", f"${remaining:.2f}/${total:.2f} (+${rate:.2f}/hr)")
    
    console.print(Panel(console.render_str("Amp Usage Limits"), border_style="cyan"))
    console.print()
    console.print(table)
    
    # Schedule notification for next top-up
    if schedule_notify and not is_full:
        notif_id = f"amp-topup-{int(topup_time.timestamp())}"
        
        if check_scheduled(notif_id):
            console.print("\nℹ️  Top-up notification already scheduled")
        else:
            # Use relative time for ntfy (format: "X hours Y minutes")
            time_to_topup = topup_time - datetime.now(timezone.utc)
            total_secs = int(time_to_topup.total_seconds())
            hours = total_secs // 3600
            mins = (total_secs % 3600) // 60
            
            if hours > 0:
                at_time = f"{hours} hour{'s' if hours != 1 else ''}"
                if mins > 0:
                    at_time += f" {mins} minute{'s' if mins != 1 else ''}"
            else:
                at_time = f"{mins} minute{'s' if mins != 1 else ''}"
            
            message = f"Amp credits topped up!\n\n${remaining:.2f} → ${total:.2f}"
            
            if send_ntfy("Amp Top-Up", message, at_time):
                console.print(f"\n🔔 Notification scheduled for {topup_time.astimezone().strftime('%Y-%m-%d %H:%M')}")
            else:
                console.print("\n✗ Failed to schedule notification")


def main():
    parser = argparse.ArgumentParser(description="Amp usage checker")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--notify", action="store_true", help="Schedule notification for next top-up")
    args = parser.parse_args()

    result = subprocess.run(["amp", "usage"], capture_output=True, text=True, timeout=30)
    
    if result.returncode != 0:
        print("Error: Run 'amp login' first", file=sys.stderr)
        sys.exit(1)

    usage = parse_amp_usage(result.stdout)

    if args.json:
        print(json.dumps(usage, indent=2))
    else:
        format_summary(usage, schedule_notify=args.notify)


if __name__ == "__main__":
    main()
