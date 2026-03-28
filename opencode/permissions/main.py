#!/usr/bin/env python3
"""CLI entry point for OpenCode permission diagnostics.

Managed markdown agents are no longer written from this module. Agent population
is owned by the top-level `just build-agents` workflow, which fetches published
`ai-prompts` slugs and pipes them through the external
`opencode-permission-policy-compiler`.
"""

from __future__ import annotations

import sys

import typer

from src.compiler import GLOBAL_DEFAULTS
from src.display import console, show_rulesets
from src.validate_inventory import UndeclaredToolError, validate_tool_inventory

app = typer.Typer(help="Inspect OpenCode permission defaults and rulesets.")


@app.command(name="list-rulesets")
def list_rulesets_cmd() -> None:
    """List available rulesets (abstract rule combinations)."""
    show_rulesets()


@app.command(name="validate-tools")
def validate_tools_cmd() -> None:
    """Validate GLOBAL_DEFAULTS covers exactly the known tool set (static + MCP)."""
    try:
        validate_tool_inventory(GLOBAL_DEFAULTS)
    except UndeclaredToolError as exc:
        console.print(f"[bold red]{exc}[/bold red]")
        sys.exit(1)
    console.print(
        "[green]Tool inventory OK — GLOBAL_DEFAULTS matches all known tools.[/green]"
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
