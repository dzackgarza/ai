#!/usr/bin/env python3
"""main.py — CLI entry point for the OpenCode permission system.

Responsibilities:
  - Parse CLI arguments
  - Write compiled permissions to agent config files
  - Delegate display to src/display.py

To add an agent: create a file in agents/primary/ or agents/subagents/,
subclass PureAgent or Subagent, and assign AGENT = YourClass().
Internals live in src/; rulesets in src/rulesets/.
"""
import json
import logging
import os
from pathlib import Path
import subprocess
import sys
from typing import Optional

# Ensure sibling modules are importable when run directly.
sys.path.insert(0, os.path.dirname(__file__))

import typer
from agents import AGENTS
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from src.agent_markdown import (
    PROMPT_TOKEN_WARNING_THRESHOLD,
    GeneratedAgentArtifact,
    load_static_markdown_artifact,
    render_agent_artifact,
    write_markdown_artifact,
)
from src.compiler import GLOBAL_DEFAULTS
from src.validate_inventory import validate_tool_inventory, UndeclaredToolError
from src.display import load_agent_rulesets, show_effective, show_agents, show_rulesets, console
from src.models import UNMANAGED_AGENTS

# ---------------------------------------------------------------------------
# File paths
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_BASE_DIR = Path(os.path.expanduser("~/.config/opencode"))
_SKELETON = _BASE_DIR / "configs" / "config_skeleton.json"
_MARKDOWN_AGENTS_DIR = _BASE_DIR / "agents"

# Ensure we can import build_config
sys.path.insert(0, str(_PROJECT_ROOT / "scripts"))
from build_config import build_config as run_build_config

AGENT_MAP = {a.name: a for a in AGENTS}
BUILTIN_SHADOWS = {
    "build": "interactive-agents/opencode-build",
    "explore": "sub-agents/opencode-explore",
    "compaction": "micro-agents/opencode-compaction",
    "title": "micro-agents/opencode-title",
    "summary": "micro-agents/opencode-summary",
}

_build_console = Console(stderr=True)
_handler = RichHandler(console=_build_console, markup=True, show_path=False, rich_tracebacks=True)
_handler.setFormatter(logging.Formatter("%(message)s"))
logger = logging.getLogger("opencode.permissions.build")
if not logger.handlers:
    logger.addHandler(_handler)
logger.setLevel(logging.INFO)
logger.propagate = False


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def _read_json(path: str | Path) -> dict:
    with open(path) as f:
        return json.load(f)


def _write_json(path: str | Path, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def _managed_agents() -> list:
    return [agent for agent in sorted(AGENTS, key=lambda item: item.name) if agent.name not in UNMANAGED_AGENTS]


def _build_artifacts() -> list[GeneratedAgentArtifact]:
    artifacts = [render_agent_artifact(agent) for agent in _managed_agents()]
    for agent_name, prompt_slug in BUILTIN_SHADOWS.items():
        artifacts.append(load_static_markdown_artifact(prompt_slug=prompt_slug, output_name=f"{agent_name}.md"))
    return artifacts


def _warn_for_large_prompts(artifacts: list[GeneratedAgentArtifact]) -> None:
    oversized = [
        artifact
        for artifact in artifacts
        if artifact.token_count > PROMPT_TOKEN_WARNING_THRESHOLD
    ]
    if not oversized:
        return
    table = Table(title="Prompt token warnings", show_header=True)
    table.add_column("Agent", style="bold")
    table.add_column("Tokens", justify="right")
    table.add_column("Model")
    table.add_column("Source template", style="dim")
    for artifact in sorted(oversized, key=lambda item: item.token_count, reverse=True):
        table.add_row(
            artifact.name,
            str(artifact.token_count),
            artifact.model or "-",
            artifact.source_template,
        )
    console.print(table)
    logger.warning(
        "[yellow]Prompt token threshold exceeded for %d agent(s) (limit=%d)[/yellow]",
        len(oversized),
        PROMPT_TOKEN_WARNING_THRESHOLD,
        extra={"markup": True},
    )


def _validate_written_artifacts(artifacts: list[GeneratedAgentArtifact]) -> None:
    missing = [
        artifact.output_filename
        for artifact in artifacts
        if not (_MARKDOWN_AGENTS_DIR / artifact.output_filename).exists()
    ]
    if missing:
        raise RuntimeError(f"Generated agent files missing after write: {missing}")


def apply_agents() -> list[GeneratedAgentArtifact]:
    """Write compiled permissions to all managed markdown agent files."""
    try:
        validate_tool_inventory(GLOBAL_DEFAULTS)
    except UndeclaredToolError as exc:
        console.print(f"[bold red]{exc}[/bold red]")
        sys.exit(1)

    # Global defaults → skeleton
    if _SKELETON.exists():
        data = _read_json(_SKELETON)
        data["permission"] = GLOBAL_DEFAULTS
        _write_json(_SKELETON, data)
        logger.info("Applied global defaults to [bold]config_skeleton.json[/bold]", extra={"markup": True})
    else:
        logger.warning(
            "[yellow]config_skeleton.json not found; skipped global default update[/yellow]",
            extra={"markup": True},
        )

    artifacts = _build_artifacts()
    for artifact in artifacts:
        output_path = write_markdown_artifact(artifact, _MARKDOWN_AGENTS_DIR)
        logger.info("wrote %s", output_path.name)

    _validate_written_artifacts(artifacts)
    _warn_for_large_prompts(artifacts)
    return artifacts


def _validate_runtime_agents(expected_names: set[str]) -> None:
    runtime_rulesets = load_agent_rulesets()
    runtime_names = set(runtime_rulesets)
    missing = sorted(expected_names - runtime_names)
    if missing:
        raise RuntimeError(f"Generated agents missing from runtime `opencode agent list`: {missing}")
    logger.info("Validated %d generated agents against `opencode agent list`", len(expected_names))


def build_agents() -> None:
    """Build markdown agents, rebuild opencode.json, then validate runtime visibility."""
    artifacts = apply_agents()
    logger.info("Running [bold]scripts/build_config.py[/bold] directly...", extra={"markup": True})
    run_build_config()
    expected_names = {artifact.name for artifact in artifacts}
    _validate_runtime_agents(expected_names)
    logger.info("Build complete: %d generated agents validated", len(expected_names))


def dump_agent(name: str) -> None:
    """Print compiled permissions for one agent as raw JSON."""
    if name not in AGENT_MAP:
        console.print(f"[red]Error:[/red] '{name}' not found.\nAvailable: {', '.join(sorted(AGENT_MAP))}")
        sys.exit(1)
    print(json.dumps(AGENT_MAP[name].compile(), indent=2, sort_keys=True))


def dry_run() -> None:
    """Compile all agents and report key counts without writing files."""
    from rich import box
    t = Table(box=box.SIMPLE, show_header=True, padding=(0, 1))
    t.add_column("Agent", style="bold")
    t.add_column("Base type", style="dim")
    t.add_column("Keys", justify="right")
    for agent in sorted(AGENTS, key=lambda a: a.name):
        t.add_row(agent.name, agent.base_type, str(len(agent.compile())))
    console.print(t)
    console.print(f"\n[green]All {len(AGENTS)} agents compiled successfully.[/green]")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

app = typer.Typer(help="Manage OpenCode agent permissions.")


@app.command()
def build() -> None:
    """Write markdown agents, rebuild opencode.json, and validate runtime visibility."""
    build_agents()


@app.command()
def apply() -> None:
    """Write compiled permissions to agent config files."""
    apply_agents()


@app.command(name="dry-run")
def dry_run_cmd() -> None:
    """Compile all agents and report without writing files."""
    dry_run()


@app.command()
def dump(agent: str = typer.Argument(help="Agent name")) -> None:
    """Print one agent's compiled permissions as raw JSON."""
    dump_agent(agent)


@app.command(name="show-effective")
def show_effective_cmd(
    agent: str = typer.Argument(help="Agent name"),
    path: str = typer.Option("*", help="Input path/command for permission evaluation"),
) -> None:
    """Print effective permission for every tool (via opencode agent list)."""
    show_effective(agent, path=path, agent=AGENT_MAP.get(agent))


@app.command(name="list-agents")
def list_agents_cmd() -> None:
    """List all managed agents."""
    show_agents(AGENTS)


@app.command(name="list-rulesets")
def list_rulesets_cmd() -> None:
    """List available rulesets (abstract rule combinations)."""
    show_rulesets()


@app.command(name="validate-tools")
def validate_tools_cmd() -> None:
    """Validate GLOBAL_DEFAULTS covers exactly the known tool set (static + MCP)."""
    validate_tool_inventory(GLOBAL_DEFAULTS)
    console.print("[green]Tool inventory OK — GLOBAL_DEFAULTS matches all known tools.[/green]")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
