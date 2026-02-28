#!/usr/bin/env python3
"""Shared usage table rendering for all harnesses."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.table import Table


@dataclass
class ModelRow:
    """A single row in the usage table."""
    family: str  # "Claude", "Gemini", "Amp", etc.
    model: str   # "5h", "7d", model name, etc.
    pct_used: float  # 0.0 to 100.0
    reset_time: str  # "in 4h 59m", "now", etc.
    is_exhausted: bool = False  # For coloring


class UsageTable:
    """Renders a uniform usage table across all harnesses."""

    # Fixed column widths (calculated from format specs)
    PCT_WIDTH = 5  # "XXX%"
    TIME_WIDTH = 11  # "in XXXh XXm"
    BAR_MIN_WIDTH = 20  # Minimum bar width

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()

    def calculate_bar_width(self, max_label_len: int) -> int:
        """Calculate bar width based on terminal width."""
        # Total: label + pct + bar + time + padding
        # Padding: 2 (left) + 1 (between cols) * 3 = 5
        available = self.console.width - max_label_len - self.PCT_WIDTH - self.TIME_WIDTH - 6
        return max(self.BAR_MIN_WIDTH, available)

    def render(self, rows: list[ModelRow], title: str = "Usage Limits") -> None:
        """Render the usage table."""
        if not rows:
            self.console.print("[yellow]No data available[/yellow]")
            return

        # Group by family
        families: dict[str, list[ModelRow]] = {}
        for row in rows:
            if row.family not in families:
                families[row.family] = []
            families[row.family].append(row)

        # Header panel
        self.console.print(Panel(f"[bold]{title}[/bold]", border_style="cyan"))
        self.console.print()

        # Render each family
        for family, family_rows in families.items():
            self.console.print(f"[bold]{family}[/bold]")
            self.console.print()

            # Calculate column widths from data
            max_label_len = max(len(r.model) for r in family_rows)
            bar_width = self.calculate_bar_width(max_label_len)

            # Create table with fixed width columns
            table = Table(show_header=False, box=None, padding=(0, 1))
            table.add_column("Model", style="bold", width=max_label_len, overflow="ellipsis")
            table.add_column("Pct", width=self.PCT_WIDTH, justify="right")
            table.add_column("Bar", width=bar_width)
            table.add_column("Time", width=self.TIME_WIDTH)

            # Add rows
            for row in family_rows:
                bar_color = self._get_bar_color(row.pct_used)
                progress = ProgressBar(
                    total=100,
                    completed=row.pct_used,
                    width=bar_width,
                    style="dim",
                    complete_style=bar_color,
                    finished_style=bar_color,
                )
                table.add_row(row.model, f"{int(row.pct_used):>4}%", progress, row.reset_time)

            self.console.print(table)
            self.console.print()

    def _get_bar_color(self, pct: float) -> str:
        """Get bar color based on usage percentage."""
        if pct >= 100:
            return "red"
        elif pct >= 80:
            return "yellow"
        else:
            return "green"

    @staticmethod
    def format_reset_time(reset_at: str) -> str:
        """Format reset timestamp as relative time string.
        
        Args:
            reset_at: ISO 8601 timestamp string (must be valid)
            
        Returns:
            Formatted string like "in 4h 59m", "in 1d 2h", or "now"
            
        Raises:
            ValueError: If reset_at is not a valid ISO 8601 timestamp
        """
        if not reset_at:
            raise ValueError("reset_at cannot be empty")
        
        reset_dt = datetime.fromisoformat(reset_at.replace("Z", "+00:00"))
        delta = reset_dt - datetime.now(timezone.utc)
        
        if delta.total_seconds() <= 0:
            return "now"
        
        total_hrs = int(delta.total_seconds() / 3600)
        mins = int((delta.total_seconds() % 3600) / 60)
        
        # Format: "in XXh XXm" (consistent format, no days)
        return f"in {total_hrs}h {mins}m"
