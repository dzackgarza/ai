"""validate_inventory.py — Validate that GLOBAL_DEFAULTS covers exactly the known tool set.

Known tools = live tool IDs from the opencode API + MCP tools queried live via mcp2cli.
Any symmetric difference between known tools and GLOBAL_DEFAULTS keys is an error:
  - In GLOBAL_DEFAULTS but not known  → stale permission entry (cruft from removed tool)
  - Known but not in GLOBAL_DEFAULTS  → undeclared tool (inherits no explicit permission)

Requires a running opencode server (default: http://127.0.0.1:4096).
Override with the OPENCODE_BASE_URL environment variable.
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
import urllib.request
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger("opencode.permissions.build")

OPENCODE_DEFAULT_BASE_URL = "http://127.0.0.1:4096"

MCP_YAML_PATH = Path("~/ai/mcp/mcp-servers.yml").expanduser()
OPENCODE_HARNESS = "opencode"


# ---------------------------------------------------------------------------
# Live tool discovery via opencode API
# ---------------------------------------------------------------------------

def discover_opencode_tools() -> list[str]:
    """Return all tool IDs from a running opencode server via GET /experimental/tool/ids.

    Includes built-in tools, plugin-registered tools, and any other tools the
    server has loaded — the complete live registry.
    """
    base_url = os.environ.get("OPENCODE_BASE_URL", OPENCODE_DEFAULT_BASE_URL).rstrip("/")
    url = f"{base_url}/experimental/tool/ids"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as exc:
        raise RuntimeError(
            f"Failed to query opencode tool IDs from {url}: {exc}\n"
            f"Ensure opencode is running (command opencode serve) or set OPENCODE_BASE_URL."
        ) from exc


# ---------------------------------------------------------------------------
# MCP tool discovery
# ---------------------------------------------------------------------------

def _opencode_mcp_servers() -> dict[str, dict[str, Any]]:
    """Return servers from mcp-servers.yml that are enabled for the opencode harness."""
    data = yaml.safe_load(MCP_YAML_PATH.read_text())
    result = {}
    for name, cfg in data.get("common", {}).items():
        if not cfg.get("enabled", True):
            continue
        if OPENCODE_HARNESS in cfg.get("exclude_harnesses", []):
            continue
        result[name] = cfg
    return result


def _mcp2cli_command(cfg: dict[str, Any]) -> str:
    command = cfg.get("command", "")
    args = cfg.get("args", [])
    return " ".join([command, *[str(a) for a in args]])


def _parse_tool_names(mcp2cli_output: str) -> list[str]:
    """Extract tool names from `mcp2cli --list --toon` stdout."""
    tools = []
    for line in mcp2cli_output.splitlines():
        # Lines with tools are indented with 2 spaces, tool name is the first token
        if line.startswith("  ") and not line.startswith("   "):
            name = line.split()[0]
            if name:
                tools.append(name)
    return tools


def _permission_key(server_name: str, tool_name: str) -> str:
    """Convert MCP server name + tool name to a permission key.

    Server name keeps its original form (e.g. cut-copy-paste-mcp).
    Tool name has hyphens converted to underscores (e.g. read-file -> read_file).
    Result: cut-copy-paste-mcp_cut, serena_read_file, etc.
    """
    return f"{server_name}_{tool_name.replace('-', '_')}"


def discover_mcp_tools() -> dict[str, list[str]]:
    """Return {server_name: [permission_key, ...]} for all opencode MCP servers."""
    servers = _opencode_mcp_servers()
    result = {}
    for name, cfg in servers.items():
        cmd = _mcp2cli_command(cfg)
        try:
            proc = subprocess.run(
                ["uvx", "mcp2cli", "--mcp-stdio", cmd, "--list", "--toon"],
                capture_output=True, text=True, timeout=60,
            )
            tool_names = _parse_tool_names(proc.stdout)
            result[name] = [_permission_key(name, t) for t in tool_names]
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"mcp2cli timed out querying server '{name}'")
        except Exception as exc:
            raise RuntimeError(f"Failed to query MCP server '{name}': {exc}") from exc
    return result


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_tool_inventory(global_defaults: dict) -> None:
    """Raise ValueError if GLOBAL_DEFAULTS keys don't exactly match known tools.

    Prints an informative diff — stale entries and missing entries — before raising.
    """
    # These are permission categories (not tool IDs) and are intentionally
    # absent from the API's tool registry. Exclude them from the stale check.
    PERMISSION_CATEGORIES: frozenset[str] = frozenset({"external_directory"})

    permissioned: set[str] = set(global_defaults.keys()) - PERMISSION_CATEGORIES

    api_tools: set[str] = set(discover_opencode_tools())
    mcp_by_server = discover_mcp_tools()
    mcp_tools: set[str] = {key for keys in mcp_by_server.values() for key in keys}

    known: set[str] = api_tools | mcp_tools

    stale = sorted(permissioned - known)
    undeclared = sorted(known - permissioned)

    if not stale and not undeclared:
        logger.info(
            "Tool inventory OK — %d tools matched (%d from API, %d MCP across %d server(s)): %s",
            len(known),
            len(api_tools),
            len(mcp_tools),
            len(mcp_by_server),
            ", ".join(sorted(known)),
        )
        return

    lines = ["Tool inventory mismatch detected.\n"]
    if stale:
        lines.append("  STALE (in GLOBAL_DEFAULTS but tool no longer exists):")
        for t in stale:
            lines.append(f"    - {t}")
    if undeclared:
        lines.append("  UNDECLARED (tool exists but has no explicit permission):")
        for t in undeclared:
            origin = next(
                (srv for srv, keys in mcp_by_server.items() if t in keys),
                "api",
            )
            lines.append(f"    - {t}  [{origin}]")

    raise ValueError("\n".join(lines))
