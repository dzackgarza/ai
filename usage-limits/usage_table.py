#!/usr/bin/env python3
"""Shared usage table rendering for all providers."""

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict, computed_field
from rich.console import Console
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.table import Table


class UsageRow(BaseModel):
    """A single row in the unified usage table."""

    identifier: str          # e.g. "Claude (5h)", "Amp", "Antigravity: Claude Sonnet 4-5"
    pct_used: float          # 0.0–100.0
    reset_at: Optional[datetime] = None  # UTC datetime; None = not applicable / already full

    model_config = ConfigDict(frozen=True)

    @computed_field  # type: ignore[misc]
    @property
    def is_exhausted(self) -> bool:
        return self.pct_used >= 100.0

    @computed_field  # type: ignore[misc]
    @property
    def time_until_reset(self) -> str:
        """Human-readable time until reset_at, or empty string if not set."""
        if self.reset_at is None:
            return ""
        delta = self.reset_at - datetime.now(timezone.utc)
        if delta.total_seconds() <= 0:
            return "now"
        total_hrs = int(delta.total_seconds() / 3600)
        mins = int((delta.total_seconds() % 3600) / 60)
        if total_hrs >= 24:
            days = total_hrs // 24
            hrs = total_hrs % 24
            return f"in {days}d {hrs}h"
        return f"in {total_hrs}h {mins}m"


class UsageTable:
    """Renders a uniform 4-column usage table for any provider."""

    PCT_WIDTH = 5    # " 99%" + leading space
    TIME_WIDTH = 12  # "in 30d 12h"
    PADDING = 8      # padding=(0,1) × 4 columns × 2 sides

    def __init__(self, console: Optional[Console] = None) -> None:
        self.console = console or Console()

    def render(self, rows: list[UsageRow], title: str = "Usage Limits") -> None:
        """Render the usage table with header panel."""
        if not rows:
            self.console.print("[yellow]No data available[/yellow]")
            return

        self.console.print(Panel(f"[bold]{title}[/bold]", border_style="cyan"))
        self.console.print()

        max_id_len = max(len(r.identifier) for r in rows)
        # Let bar shrink to 0 rather than forcing a minimum and overflowing the terminal.
        bar_width = max(
            0,
            self.console.width - max_id_len - self.PCT_WIDTH - self.TIME_WIDTH - self.PADDING,
        )

        table = Table(show_header=False, box=None, padding=(0, 1))
        # no_wrap=True ensures long identifiers get ellipsized, not wrapped to the next line.
        table.add_column("Identifier", style="bold", width=max_id_len, overflow="ellipsis", no_wrap=True)
        table.add_column("Pct", width=self.PCT_WIDTH, justify="right", no_wrap=True)
        if bar_width:
            table.add_column("Bar", width=bar_width, no_wrap=True)
        table.add_column("Time", width=self.TIME_WIDTH, no_wrap=True)

        for row in rows:
            color = self._bar_color(row.pct_used)
            pct_str = f"{int(row.pct_used):>4}%"
            if bar_width:
                bar = ProgressBar(
                    total=100,
                    completed=row.pct_used,
                    width=bar_width,
                    style="dim",
                    complete_style=color,
                    finished_style=color,
                )
                table.add_row(row.identifier, pct_str, bar, row.time_until_reset)
            else:
                table.add_row(row.identifier, pct_str, row.time_until_reset)

        self.console.print(table)
        self.console.print()

    @staticmethod
    def _bar_color(pct: float) -> str:
        if pct >= 100:
            return "red"
        if pct >= 80:
            return "yellow"
        return "green"
