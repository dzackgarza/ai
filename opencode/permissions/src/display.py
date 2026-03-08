"""display.py — Rich terminal output for permission inspection."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from typing import TYPE_CHECKING

from rich import box
from rich.console import Console
from rich.table import Table

from src.models import DISPLAY_CATEGORIES

if TYPE_CHECKING:
    from src.base import Agent

console = Console(width=120)

ACTION_STYLE: dict[str, str] = {"allow": "green", "deny": "red", "ask": "yellow"}

EDIT_PERMISSION_TOOLS: frozenset[str] = frozenset({"edit", "write", "patch", "multiedit", "apply_patch"})

_HEADER_RE = re.compile(r"^(\S.*?)\s+\((?:primary|subagent)\)\s*$")

# Path prefixes injected by opencode's skills system — not managed by this script.
_INTERNAL_PREFIXES: tuple[str, ...] = tuple(
    os.path.expanduser(p) for p in (
        "~/.claude/skills/",
        "~/.agents/skills/",
        "~/.local/share/opencode/",
    )
)


def load_agent_rulesets() -> dict[str, list[dict]]:
    """Run `opencode agent list` and parse into {agent_name: ruleset} dict.

    The ruleset is the flat array of {permission, action, pattern} dicts as
    computed by opencode at runtime — the canonical source of truth.
    """
    result = subprocess.run(["opencode", "agent", "list"], capture_output=True, text=True)
    if result.returncode != 0:
        console.print(f"[red]Error:[/red] `opencode agent list` failed:\n{result.stderr}")
        sys.exit(1)

    agents: dict[str, list[dict]] = {}
    current_name: str | None = None
    json_lines: list[str] = []
    in_json = False

    for line in result.stdout.splitlines():
        m = _HEADER_RE.match(line)
        if m:
            current_name = m.group(1)
            json_lines = []
            in_json = False
            continue
        if current_name is None:
            continue
        stripped = line.strip()
        if stripped == "[":
            in_json = True
            json_lines = ["["]
        elif stripped == "]" and in_json:
            json_lines.append("]")
            agents[current_name] = json.loads("\n".join(json_lines))
            in_json = False
        elif in_json:
            json_lines.append(stripped)

    return agents


def wildcard_match(value: str, pattern: str) -> bool:
    """Mirror upstream opencode Wildcard.match semantics exactly.

    Source:
    - packages/opencode/src/util/wildcard.ts
    - packages/opencode/test/util/wildcard.test.ts
    """
    normalized_value = value.replace("\\", "/")
    normalized_pattern = pattern.replace("\\", "/")

    escaped = re.escape(normalized_pattern).replace(r"\*", ".*").replace(r"\?", ".")
    if escaped.endswith(r"\ .*"):
        escaped = escaped[:-4] + r"( .*)?"

    flags = re.S
    if sys.platform == "win32":
        flags |= re.I
    return re.fullmatch(escaped, normalized_value, flags=flags) is not None


def permission_key_for_tool(tool: str) -> str:
    """Map tool names to the permission key opencode evaluates."""
    if tool in EDIT_PERMISSION_TOOLS:
        return "edit"
    return tool


def findlast_action(ruleset: list[dict], tool: str, path: str = "*") -> str:
    """Evaluate opencode's findLast rule using upstream wildcard semantics.

    Returns "ask" if no rule matches (opencode's upstream default).
    """
    permission = permission_key_for_tool(tool)
    matched = "ask"
    for rule in ruleset:
        if wildcard_match(permission, rule["permission"]) and wildcard_match(path, rule["pattern"]):
            matched = rule["action"]
    return matched


def show_effective(name: str, path: str = "*", agent: Agent | None = None) -> None:
    """Print effective permission for every known tool as computed by opencode.

    Uses `opencode agent list` for the canonical ruleset, then evaluates via
    findLast matching — identical to opencode's runtime logic.
    """
    rulesets = load_agent_rulesets()
    if name not in rulesets:
        console.print(
            f"[red]Error:[/red] '{name}' not found.\n"
            f"Available: {', '.join(sorted(rulesets.keys()))}"
        )
        sys.exit(1)

    ruleset = rulesets[name]

    categories = list(DISPLAY_CATEGORIES)
    categorized = {t for _, tools in categories for t in tools}
    extra = sorted(
        p for p in {r["permission"] for r in ruleset}
        if p != "*" and not any(wildcard_match(permission_key_for_tool(t), p) for t in categorized)
    )
    if extra:
        categories.append(("Extra (live ruleset)", extra))

    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1), expand=False)
    table.add_column("tool", no_wrap=True)
    table.add_column("action", no_wrap=True)
    table.add_column("patterns", style="dim", no_wrap=True)

    for category, tools in categories:
        table.add_row(f"[bold]{category}[/bold]", "", "")
        for tool in tools:
            action = findlast_action(ruleset, tool, path)
            style = ACTION_STYLE.get(action, "")
            matching = [r for r in ruleset if wildcard_match(permission_key_for_tool(tool), r["permission"])]
            path_rules = [
                (r["pattern"], r["action"])
                for r in matching
                if r["pattern"] != "*" and not r["pattern"].startswith(_INTERNAL_PREFIXES)
            ]
            patterns_cell = "\n".join(
                f"{pat}  [{ACTION_STYLE.get(act, '')}]{act}[/]"
                for pat, act in path_rules
            )
            table.add_row(f"  {tool}", f"[{style}]{action}[/]", patterns_cell)
        table.add_row("", "", "")

    meta = f"[dim]via `opencode agent list` · path=[italic]{path}[/italic] · {len(ruleset)} rules[/dim]"
    if agent is not None:
        layers = ", ".join(type(l).__name__ for l in agent.permission_layers()) if hasattr(agent, '_preset_names') else agent.base_type
        meta += f"\n[dim]{agent.base_type}[/dim]"

    console.print()
    console.print(f"[bold]Effective permissions — {name}[/bold]  {meta}")
    console.print()
    console.print(table)


def show_agents(agents: list[Agent]) -> None:
    """Print a table of all managed agents."""
    t = Table(box=box.SIMPLE, show_header=True, padding=(0, 1))
    t.add_column("Agent", style="bold")
    t.add_column("Base type", style="dim")
    t.add_column("Class")
    for agent in sorted(agents, key=lambda a: a.name):
        t.add_row(agent.name, agent.base_type, type(agent).__name__)
    console.print(t)


def show_rulesets() -> None:
    """Print a table of available rulesets."""
    from src.rulesets import RULESET_REGISTRY
    t = Table(box=box.SIMPLE, show_header=True, padding=(0, 1))
    t.add_column("Ruleset")
    t.add_column("Description")
    for name, cls in sorted(RULESET_REGISTRY.items()):
        t.add_row(name, (cls.__doc__ or "").strip().splitlines()[0])
    console.print(t)
