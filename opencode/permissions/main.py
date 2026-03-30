#!/usr/bin/env python3
"""CLI entry point for OpenCode permission diagnostics and config policy writes.

Managed markdown agents are no longer written from this module. Agent population
is owned by the top-level `just build-agents` workflow, which fetches published
`ai-prompts` slugs and pipes them through the external
`opencode-permission-policy-compiler`. This CLI remains the canonical entry
point for inspecting permission state and writing the global baseline into the
compiled `opencode.json`.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import typer

from manage_permissions import GLOBAL_PERMISSION
from src.compiler import GLOBAL_DEFAULTS
from src.display import console, show_rulesets
from src.validate_inventory import UndeclaredToolError, validate_tool_inventory

app = typer.Typer(help="Inspect OpenCode permission defaults and rulesets.")
BASE_DIR = Path(os.path.expanduser("~/.config/opencode"))
OUTPUT_PATH = BASE_DIR / "opencode.json"


def _minimize_global_policy(policy: dict[str, Any]) -> dict[str, Any]:
    """Drop top-level allow entries because the compiled config defaults to allow."""
    return {
        key: value
        for key, value in policy.items()
        if not (isinstance(value, str) and value == "allow")
    }


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


@app.command(name="write-global-policy")
def write_global_policy_cmd(
    output_path: Path = typer.Argument(
        OUTPUT_PATH,
        exists=True,
        dir_okay=False,
        writable=True,
        readable=True,
        resolve_path=True,
        help="Compiled OpenCode config file to update.",
    ),
) -> None:
    """Write the global permission baseline into a compiled OpenCode config."""
    with output_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)

    config["permission"] = _minimize_global_policy(GLOBAL_PERMISSION)

    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(config, handle, indent=2)
        handle.write("\n")

    console.print(
        f"[green]Wrote global permission baseline to {output_path}[/green]"
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
