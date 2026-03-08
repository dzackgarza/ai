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
import os
import sys
import argparse

# Ensure sibling modules are importable when run directly.
sys.path.insert(0, os.path.dirname(__file__))

from agents import AGENTS
from src.agent_markdown import write_agent_markdown
from src.compiler import GLOBAL_DEFAULTS
from src.display import show_effective, show_agents, show_rulesets, console
from src.models import UNMANAGED_AGENTS

# ---------------------------------------------------------------------------
# File paths
# ---------------------------------------------------------------------------

_BASE_DIR     = os.path.expanduser("~/.config/opencode")
_SKELETON     = os.path.join(_BASE_DIR, "configs", "config_skeleton.json")
_MARKDOWN_AGENTS_DIR = os.path.join(_BASE_DIR, "agents")

AGENT_MAP = {a.name: a for a in AGENTS}


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def _read_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def _write_json(path: str, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def apply_agents() -> None:
    """Write compiled permissions to all managed markdown agent files."""
    # Global defaults → skeleton
    if os.path.exists(_SKELETON):
        data = _read_json(_SKELETON)
        data["permission"] = GLOBAL_DEFAULTS
        _write_json(_SKELETON, data)
        console.print("Applied global defaults to [bold]config_skeleton.json[/bold]")
    else:
        console.print("[yellow]Warning:[/yellow] config_skeleton.json not found; skipped.")

    for agent in sorted(AGENTS, key=lambda item: item.name):
        if agent.name in UNMANAGED_AGENTS:
            continue
        output_path = write_agent_markdown(agent, _MARKDOWN_AGENTS_DIR)
        console.print(
            f"  [green]✓[/green] {agent.name}  [dim]({agent.base_type} → {output_path.name})[/dim]"
        )


def dump_agent(name: str) -> None:
    """Print compiled permissions for one agent as raw JSON."""
    if name not in AGENT_MAP:
        console.print(f"[red]Error:[/red] '{name}' not found.\nAvailable: {', '.join(sorted(AGENT_MAP))}")
        sys.exit(1)
    print(json.dumps(AGENT_MAP[name].compile(), indent=2, sort_keys=True))


def dry_run() -> None:
    """Compile all agents and report key counts without writing files."""
    from rich.table import Table
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

def main() -> None:
    parser = argparse.ArgumentParser(description="Manage OpenCode agent permissions (v2).")
    parser.add_argument("--apply",          action="store_true",
                        help="Write compiled permissions to agent config files")
    parser.add_argument("--dry-run",        action="store_true",
                        help="Compile all agents and report without writing files")
    parser.add_argument("--dump",           metavar="AGENT",
                        help="Print one agent's compiled permissions as raw JSON")
    parser.add_argument("--show-effective", metavar="AGENT",
                        help="Print effective permission for every tool (via opencode agent list)")
    parser.add_argument("--path",           metavar="PATH", default="*",
                        help="Input path/command for --show-effective evaluation (default: *)")
    parser.add_argument("--list-agents",    action="store_true",
                        help="List all managed agents")
    parser.add_argument("--list-rulesets",  action="store_true",
                        help="List available rulesets (abstract rule combinations)")
    args = parser.parse_args()

    if args.apply:
        apply_agents()
    elif args.dry_run:
        dry_run()
    elif args.dump:
        dump_agent(args.dump)
    elif args.show_effective:
        agent = AGENT_MAP.get(args.show_effective)
        show_effective(args.show_effective, path=args.path, agent=agent)
    elif args.list_agents:
        show_agents(AGENTS)
    elif args.list_rulesets:
        show_rulesets()
    else:
        parser.print_help()
        console.print(f"\n[dim]Managed agents: {len(AGENTS)} | Unmanaged: {', '.join(sorted(UNMANAGED_AGENTS))}[/dim]")


if __name__ == "__main__":
    main()
