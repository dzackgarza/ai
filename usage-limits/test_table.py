#!/usr/bin/env python3
from rich.console import Console
from rich.table import Table
from rich.progress_bar import ProgressBar

console = Console()

table = Table(show_header=False, box=None, padding=(0, 1))
table.add_column("Model", style="bold", width=2, overflow="ellipsis")
table.add_column("Pct", width=5, justify="right")
table.add_column("Bar", width=57)
table.add_column("Time", width=11)

progress = ProgressBar(total=100, completed=28, width=57, style="dim", complete_style="green")
table.add_row("5h", "   28%", progress, "in 1h 17m")

console.print(table)
