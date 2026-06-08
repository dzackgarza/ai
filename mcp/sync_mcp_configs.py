#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml",
#     "tomlkit",
# ]
# ///
"""
MCP Configuration Synchronizer
==============================
Reads mcp-servers.yml and propagates MCP server configurations to all harnesses.
Only updates the MCP section - preserves all other config data.

Supports:
- JSON configs (opencode, amp, claude, kilo, gemini, qwen, antigravity)
- TOML configs (codex)

Usage:
    just sync-mcp-configs [--dry-run] [--harness <name>]
    python3 mcp/sync_mcp_configs.py [--dry-run] [--harness <name>]
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import yaml
import tomlkit


@dataclass
class HarnessFormat:
    """Descriptor for how a harness expects its MCP configuration."""

    name: str
    remote_url_key: str = "url"
    remote_type: Optional[str] = None
    remote_headers: bool = False
    local_type: Optional[str] = None
    command_as_list: bool = False
    args_key: Optional[str] = "args"
    include_enabled: bool = False
    json_path: str = "mcp"
    is_toml: bool = False


# Map of harness names to their formatting requirements
HARNESS_FORMATS = {
    "opencode": HarnessFormat(
        name="opencode",
        remote_type="remote",
        local_type="local",
        command_as_list=True,
        args_key=None,
    ),
    "claude": HarnessFormat(
        name="claude",
        remote_url_key="url",
        remote_type="http",
        local_type="stdio",
    ),
    "amp": HarnessFormat(
        name="amp",
        json_path="amp.mcpServers",  # Dotted but literal key support added below
    ),
    "kilo": HarnessFormat(
        name="kilo",
    ),
    "gemini": HarnessFormat(
        name="gemini",
        remote_url_key="httpUrl",
    ),
    "qwen": HarnessFormat(
        name="qwen",
        remote_url_key="httpUrl",
    ),
    "antigravity-cli": HarnessFormat(
        name="antigravity-cli",
        remote_url_key="serverUrl",
        remote_headers=True,
    ),
    "codex": HarnessFormat(
        name="codex",
        include_enabled=True,
        is_toml=True,
        json_path="mcp_servers",
    ),
}


def expand_path(path: str) -> Path:
    """Expand ~ and environment variables in path."""
    return Path(os.path.expandvars(os.path.expanduser(path)))


def resolve_env_tokens(value: Any) -> Any:
    """Resolve {env:VAR_NAME} placeholders in string values."""
    if isinstance(value, str):
        matches = ENV_TOKEN_PATTERN.findall(value)
        for var_name in matches:
            env_val = os.environ.get(var_name)
            if env_val is None:
                print(f"  WARNING: Environment variable {var_name} not set")
                env_val = ""
            value = value.replace(f"{{env:{var_name}}}", env_val)
        return value
    elif isinstance(value, list):
        return [resolve_env_tokens(item) for item in value]
    elif isinstance(value, dict):
        return {k: resolve_env_tokens(v) for k, v in value.items()}
    return value


def resolve_local_server_fields(config: dict) -> tuple[str, list[str], dict, str]:
    """Extract and resolve fields for a local server."""
    command = config.get("command", "")
    args = config.get("args", [])
    env = config.get("env", {})
    cwd = config.get("cwd", "")

    return (
        resolve_env_tokens(command),
        resolve_env_tokens(args),
        resolve_env_tokens(env),
        resolve_env_tokens(cwd),
    )


def build_server_config(config: dict, server_type: str, fmt: HarnessFormat) -> dict:
    """Unified builder for any harness format."""
    result = {}

    if server_type == "remote":
        if fmt.remote_type:
            result["type"] = fmt.remote_type
        result[fmt.remote_url_key] = resolve_env_tokens(config.get("url", ""))
        if fmt.remote_headers and config.get("headers"):
            result["headers"] = resolve_env_tokens(config["headers"])
    else:
        command, args, env, cwd = resolve_local_server_fields(config)

        if fmt.local_type:
            result["type"] = fmt.local_type

        if fmt.command_as_list:
            result["command"] = [command] + args
        else:
            result["command"] = command
            if fmt.args_key:
                result[fmt.args_key] = args

        if env:
            result["env"] = env
        if cwd:
            result["cwd"] = cwd

    if fmt.include_enabled:
        result["enabled"] = config.get("enabled", True)

    return result


def build_mcp_config_for_harness(
    yaml_config: dict, harness_name: str, fmt: HarnessFormat
) -> dict:
    """Build a complete MCP config dict for a specific harness."""
    mcp_servers = {}

    for name, server_config in yaml_config.get("common", {}).items():
        if not server_config.get("enabled", True):
            continue

        if harness_name in server_config.get("exclude_harnesses", []):
            continue

        server_type = server_config.get("type", "local")
        try:
            mcp_servers[name] = build_server_config(server_config, server_type, fmt)
        except ValueError as exc:
            raise ValueError(f"{harness_name}.{name}: {exc}") from exc

    return mcp_servers


def load_yaml_config(path: Path) -> dict:
    """Load and parse the master MCP YAML config."""
    with open(path) as f:
        return yaml.safe_load(f)


def ensure_required_sync_environment():
    """Ensure direnv has loaded the required env variables."""
    if os.environ.get("DIRENV_DIR") is None:
        print(
            "ERROR: direnv .envrc was not loaded before syncing MCP configs.\n"
            f"Run this script via `just sync-mcp-configs` so direnv loads the required environment.",
            file=sys.stderr,
        )
        sys.exit(1)


def set_nested_value(config: dict, json_path: str, value: Any) -> None:
    """Set a value in a nested dict using dot notation path.
    Supports literal keys with dots if they are already present.
    """
    # Special case: if the key exists literally, use it (Amp case)
    if json_path in config:
        config[json_path] = value
        return

    keys = json_path.split(".")
    current = config
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value


def sync_json_harness(
    config_path: Path, mcp_servers: dict, json_path: str, dry_run: bool = False
) -> bool:
    """Sync MCP configuration to a JSON harness (preserves all other config)."""
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
    else:
        config = {}

    set_nested_value(config, json_path, mcp_servers)

    if dry_run:
        print(f"  Would update {config_path}")
        print(f"  MCP servers: {list(mcp_servers.keys())}")
        return True

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

    print(f"  ✓ Updated {config_path}")
    print(f"  MCP servers: {list(mcp_servers.keys())}")
    return True


def sync_toml_harness(
    config_path: Path, mcp_servers: dict, toml_key: str, dry_run: bool = False
) -> bool:
    """Sync MCP configuration to a TOML harness."""
    if not config_path.exists():
        print(f"  ERROR: Config file not found: {config_path}")
        return False

    with open(config_path) as f:
        config = tomlkit.parse(f.read())

    mcp_section = tomlkit.table()
    for name, server_config in mcp_servers.items():
        mcp_section[name] = server_config

    config[toml_key] = mcp_section

    if dry_run:
        print(f"  Would update {config_path}")
        print(f"  MCP servers: {list(mcp_servers.keys())}")
        return True

    with open(config_path, "w") as f:
        f.write(tomlkit.dumps(config))

    print(f"  ✓ Updated {config_path}")
    print(f"  MCP servers: {list(mcp_servers.keys())}")
    return True


ENV_TOKEN_PATTERN = re.compile(r"\{env:([^}]+)\}")
RECOMMENDED_SYNC_RECIPE = "just sync-mcp-configs"


def main():
    parser = argparse.ArgumentParser(description="Sync MCP configurations")
    parser.add_argument("--dry-run", action="store_true", help="Dry run")
    parser.add_argument("--harness", type=str, help="Sync specific harness")
    parser.add_argument(
        "--config", type=str, default="mcp/mcp-servers.yml", help="YAML config"
    )
    args = parser.parse_args()

    ensure_required_sync_environment()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}")
        sys.exit(1)

    yaml_config = load_yaml_config(config_path)
    print(f"Loaded MCP configuration from {config_path}\n")

    for name, harness_config in yaml_config.get("harnesses", {}).items():
        if args.harness and args.harness != name:
            continue

        if not harness_config.get("enabled", True):
            print(f"⊘ Skipping {name} (disabled)")
            continue

        print(f"Syncing {name}...")

        # Get format descriptor
        fmt = HARNESS_FORMATS.get(name, HARNESS_FORMATS["opencode"])

        try:
            mcp_servers = build_mcp_config_for_harness(yaml_config, name, fmt)
        except ValueError as exc:
            print(f"  ERROR: {exc}\n")
            continue

        config_file_path = expand_path(harness_config["config_path"])
        json_path = harness_config.get("json_path", fmt.json_path)

        if fmt.is_toml:
            success = sync_toml_harness(config_file_path, mcp_servers, json_path, args.dry_run)
        else:
            success = sync_json_harness(config_file_path, mcp_servers, json_path, args.dry_run)

            # Special case for OpenCode skeleton
            if name == "opencode":
                skeleton = config_file_path.parent / "configs" / "config_skeleton.json"
                if skeleton.exists():
                    sync_json_harness(skeleton, mcp_servers, json_path, args.dry_run)

        if not success:
            print(f"  ✗ Failed to sync {name}")
        print()

    print("Done!" if not args.dry_run else "Dry run complete!")


if __name__ == "__main__":
    main()
