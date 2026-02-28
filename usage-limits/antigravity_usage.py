#!/usr/bin/env python3
"""Antigravity usage limits checker - wraps antigravity-usage CLI with notifications."""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone

from rich.console import Console
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.table import Table

from usage_common import UsageChecker


NTFY_TOPIC = "usage-updates"
NTFY_SERVER = "http://localhost"


class AntigravityChecker(UsageChecker):
    """Antigravity usage checker."""

    def __init__(self):
        super().__init__(
            name="Antigravity",
            state_dir="antigravity_usage",
            ntfy_topic=NTFY_TOPIC,
            ntfy_server=NTFY_SERVER,
        )

    def fetch_usage(self) -> dict:
        """Fetch usage data from antigravity-usage CLI."""
        cmd = ["npx", "antigravity-usage", "quota", "--all-models", "--refresh", "--json"]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                if "not logged in" in result.stderr.lower():
                    print("Error: Not logged in. Run: npx antigravity-usage login", file=sys.stderr)
                else:
                    print(f"Error: {result.stderr}", file=sys.stderr)
                sys.exit(1)
            return json.loads(result.stdout)
        except FileNotFoundError:
            print("Error: npx not found. Install Node.js.", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON output: {e}", file=sys.stderr)
            sys.exit(1)
        except subprocess.TimeoutExpired:
            print("Error: Command timed out", file=sys.stderr)
            sys.exit(1)

    def get_windows(self, data: dict) -> dict[str, tuple[float, str | None]]:
        """Extract 5h/7d windows from model list."""
        models = data.get("models", [])
        
        max_usage = 0
        all_resets = []
        
        for model in models:
            is_exhausted = model.get("isExhausted", False)
            reset_time = model.get("resetTime")
            remaining_pct = model.get("remainingPercentage")
            
            if is_exhausted:
                used = 100
            elif remaining_pct is not None:
                used = (100 - remaining_pct)
            else:
                used = 0
            
            max_usage = max(max_usage, used)
            
            if reset_time:
                all_resets.append(reset_time)
        
        if all_resets:
            sorted_resets = sorted(all_resets)
            earliest_reset = sorted_resets[0]
            latest_reset = sorted_resets[-1]
        else:
            earliest_reset = None
            latest_reset = None
        
        return {
            "5h": (max_usage, earliest_reset),
            "7d": (max_usage, latest_reset),
        }

    def format_summary(self, data: dict) -> None:
        """Format usage data as rich summary - matches Claude/Codex/Amp format."""
        console = Console()
        
        email = data.get("email", "Unknown")
        method = data.get("method", "unknown")
        models = data.get("models", [])

        console.print(Panel(f"[bold]{email}[/bold] ({method})", border_style="cyan"))
        console.print()

        # Group by model family
        families = {"Claude": [], "Gemini": [], "Other": []}
        for model in models:
            model_id = model.get("modelId", "")
            label = model.get("label", model_id)
            is_exhausted = model.get("isExhausted", False)
            remaining_pct = model.get("remainingPercentage")
            reset_time = model.get("resetTime")
            
            if "claude" in model_id.lower():
                family = "Claude"
            elif "gemini" in model_id.lower():
                family = "Gemini"
            else:
                family = "Other"
            
            families[family].append({
                "label": label,
                "is_exhausted": is_exhausted,
                "remaining_pct": remaining_pct,
                "reset_time": reset_time,
            })

        for family, models_list in families.items():
            if not models_list:
                continue

            console.print(f"[bold]{family}[/bold]")
            console.print()

            # Calculate exact column widths from data
            max_label_len = max(len(m["label"]) for m in models_list)
            pct_width = 6  # "XXX%" (e.g., "100%") with space
            time_width = 11  # "in XXXh XXm" max = 11 chars
            bar_width = max(20, console.width - max_label_len - pct_width - time_width - 6)  # Remaining width for bar
            
            # Create table with EXACT fixed width columns
            table = Table(show_header=False, box=None, padding=(0, 1))
            table.add_column("Model", style="bold", width=max_label_len, overflow="ellipsis")
            table.add_column("Pct", width=pct_width, justify="right")
            table.add_column("Bar", width=bar_width)
            table.add_column("Time", width=time_width)

            for m in models_list:
                is_exhausted = m["is_exhausted"]
                remaining_pct = m["remaining_pct"]
                reset_time = m["reset_time"]
                label = m["label"]

                if is_exhausted:
                    pct_used = 100
                elif remaining_pct is not None:
                    pct_used = 100 - remaining_pct
                else:
                    pct_used = 0

                # Calculate time until reset - format: "in XXh XXm" (exactly 9 chars)
                if reset_time:
                    try:
                        reset_dt = datetime.fromisoformat(reset_time.replace("Z", "+00:00"))
                        delta = reset_dt - datetime.now(timezone.utc)
                        if delta.total_seconds() <= 0:
                            time_str = "now"
                        else:
                            total_hrs = int(delta.total_seconds() / 3600)
                            mins = int((delta.total_seconds() % 3600) / 60)
                            # Format: "in XXh XXm" = exactly 9 chars
                            time_str = f"in {total_hrs}h {mins}m"
                    except:
                        time_str = ""
                else:
                    time_str = ""

                # Use Rich's ProgressBar - 0% correctly shows no bar
                bar_color = "green" if pct_used < 60 else "yellow" if pct_used < 100 else "red"
                progress = ProgressBar(
                    total=100,
                    completed=pct_used,
                    width=bar_width,
                    style="dim",
                    complete_style=bar_color,
                    finished_style=bar_color,
                )

                # Add row: label | pct% | bar | time (no tenths)
                table.add_row(label, f"{int(pct_used):>4}%", progress, time_str)

            console.print(table)
            console.print()


def main():
    parser = argparse.ArgumentParser(description="Antigravity usage limits checker")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--no-notify", action="store_true", help="Disable auto-notification")
    args = parser.parse_args()

    checker = AntigravityChecker()

    # Fetch usage data
    data = checker.fetch_usage()

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        windows = checker.get_windows(data)
        checker.format_summary(data)

        # Check for fresh window (0% usage)
        five_hour = windows.get("5h", (0, None))
        if not args.no_notify and five_hour[0] == 0:
            message = "Antigravity window open!\n\nFresh quota available for all models."
            if checker.send_ntfy_notification("Antigravity Window Open", message, at=None, tags="white_check_mark,rocket"):
                print("\n🔔 Fresh window notification sent")

        # Auto-schedule notification for blocking window
        if not args.no_notify:
            do_notify, blocking_reset = checker.should_notify(windows)

            if do_notify:
                notif_id = checker.get_notification_id(windows)

                if checker.check_notification_scheduled(notif_id):
                    print("\nℹ️  Notification already scheduled")
                else:
                    success, msg = checker.schedule_notification(
                        reset_dt=blocking_reset,
                        summary="Antigravity quota exhausted",
                        state_name="notify",
                        notif_id=notif_id,
                        title="Antigravity Quota Reset",
                    )
                    if success:
                        print(f"\n🔔 Notification scheduled for {msg}")
                    else:
                        print(f"\n✗ Failed to schedule: {msg}")
                        sys.exit(1)


if __name__ == "__main__":
    main()
