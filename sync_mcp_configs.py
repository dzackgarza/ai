#!/usr/bin/env python3
"""
MCP Configuration Synchronizer
==============================
Reads mcp-servers.yml and propagates MCP server configurations to all harnesses.
Only updates the MCP section - preserves all other config data.

Supports:
- JSON configs (opencode, amp, claude, kilo)
- TOML configs (codex)

Usage:
    just sync-mcp-configs [--dry-run] [--harness <name>]
    python3 sync_mcp_configs.py [--dry-run] [--harness <name>]
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Installing PyYAML...")
    os.system("pip install pyyaml -q")
    import yaml

try:
    import tomlkit
except ImportError:
    print("Installing tomlkit...")
    os.system("pip install tomlkit -q")
    import tomlkit


def expand_path(path: str) -> Path:
    """Expand ~ and environment variables in path."""
    return Path(os.path.expandvars(os.path.expanduser(path)))


ENV_TOKEN_PATTERN = re.compile(r"\{env:([^}]+)\}")
RECOMMENDED_SYNC_RECIPE = "just sync-mcp-configs"


def resolve_env_tokens(value: Any) -> Any:
    """Resolve {env:VAR_NAME} placeholders in string values."""
    if not isinstance(value, str):
        return value

    def replacer(match: re.Match[str]) -> str:
        env_name = match.group(1).strip()
        env_value = os.environ.get(env_name)
        if env_value is None:
            raise ValueError(f"Required environment variable is not set: {env_name}")
        return env_value

    return ENV_TOKEN_PATTERN.sub(replacer, value)


def resolve_local_server_fields(config: dict) -> tuple[str, list[str], dict[str, str] | None]:
    """Resolve command, args, and env for a local MCP server."""
    command = resolve_env_tokens(config.get('command', ''))
    args = [resolve_env_tokens(arg) for arg in config.get('args', [])]
    env_config = config.get('env')
    env = None if not env_config else {
        key: resolve_env_tokens(value) for key, value in env_config.items()
    }
    return command, args, env


def load_yaml_config(config_path: str) -> dict:
    """Load the centralized YAML configuration."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def ensure_required_sync_environment() -> None:
    """Fail fast when the expected ~/.envrc-derived environment is missing."""
    if os.environ.get("SEARXNG_SERVER_URL"):
        return

    print(
        "Error: SEARXNG_SERVER_URL is not set.\n"
        "This is a canary that ~/.envrc was not loaded before syncing MCP configs.\n"
        f"Run this script via `{RECOMMENDED_SYNC_RECIPE}` so direnv loads the required environment.",
        file=sys.stderr,
    )
    sys.exit(1)


def build_mcp_config_for_harness(yaml_config: dict, harness_name: str, builder_func: callable) -> dict:
    """Build the MCP configuration for a specific harness.

    Args:
        yaml_config: The loaded YAML configuration
        harness_name: Name of the harness (for logging)
        builder_func: Function to build server config in harness-specific format
    """
    mcp_servers = {}

    # Add all common servers (no harness-specific servers - all harnesses get the same tools)
    for name, server_config in yaml_config.get('common', {}).items():
        if not server_config.get('enabled', True):
            continue
        
        # Check if this server should be excluded from this harness
        exclude_harnesses = server_config.get('exclude_harnesses', [])
        if harness_name in exclude_harnesses:
            continue
        
        server_type = server_config.get('type', 'local')
        try:
            mcp_servers[name] = builder_func(server_config, server_type)
        except ValueError as exc:
            raise ValueError(f"{harness_name}.{name}: {exc}") from exc

    return mcp_servers


def build_opencode_server_config(config: dict, server_type: str) -> dict:
    """Build a server configuration in OpenCode format."""
    if server_type == 'remote':
        return {
            'type': 'remote',
            'url': resolve_env_tokens(config.get('url', ''))
        }
    else:
        command, args, _ = resolve_local_server_fields(config)
        return {
            'type': 'local',
            'command': [command] + args
        }


def build_claude_server_config(config: dict, server_type: str) -> dict:
    """Build a server configuration in Claude Code format.
    
    Claude uses:
    - type: "stdio" for local servers (not "local")
    - type: "http" for remote servers (not "remote")
    - command: string (not array)
    """
    if server_type == 'remote':
        return {
            'type': 'http',
            'url': resolve_env_tokens(config.get('url', ''))
        }
    else:
        # Claude expects command as a single string, args as separate array
        command, cmd_args, env = resolve_local_server_fields(config)
        server_config = {
            'type': 'stdio',
            'command': command,
            'args': cmd_args if cmd_args else []
        }
        if env:
            server_config['env'] = env
        return server_config


def build_amp_server_config(config: dict, server_type: str) -> dict:
    """Build a server configuration in Amp format.
    
    Amp uses:
    - No 'type' field
    - command: string (not array)
    - args: array
    - For remote: just 'url' field
    """
    if server_type == 'remote':
        return {
            'url': resolve_env_tokens(config.get('url', ''))
        }
    else:
        command, args, env = resolve_local_server_fields(config)
        server_config = {
            'command': command,
            'args': args
        }
        if env:
            server_config['env'] = env
        return server_config


def build_kilo_server_config(config: dict, server_type: str) -> dict:
    """Build a server configuration in Kilo Code format.
    
    Kilo uses (same as Cline/Roo Code):
    - No 'type' field
    - command: string (not array)
    - args: array
    - For remote: just 'url' field
    """
    if server_type == 'remote':
        return {
            'url': resolve_env_tokens(config.get('url', ''))
        }
    else:
        command, args, env = resolve_local_server_fields(config)
        server_config = {
            'command': command,
            'args': args
        }
        if env:
            server_config['env'] = env
        return server_config


def build_gemini_server_config(config: dict, server_type: str) -> dict:
    """Build a server configuration in Gemini/Qwen format.

    Gemini/Qwen uses:
    - No 'type' field for local servers
    - command: string, args: array
    - For remote: uses 'httpUrl' field (not 'url' or 'type')
    """
    if server_type == 'remote':
        return {
            'httpUrl': resolve_env_tokens(config.get('url', ''))
        }
    else:
        command, args, env = resolve_local_server_fields(config)
        server_config = {
            'command': command,
            'args': args
        }
        if env:
            server_config['env'] = env
        return server_config


def build_codex_server_config(config: dict, server_type: str) -> dict:
    """Build a server configuration in Codex TOML format."""
    if server_type == 'remote':
        return {
            'url': resolve_env_tokens(config.get('url', '')),
            'enabled': True
        }
    else:
        command, args, env = resolve_local_server_fields(config)
        server_config = {
            'command': command,
            'args': args,
            'enabled': True
        }
        if env:
            server_config['env'] = env
        return server_config


def sync_opencode_harness(config_path: Path, mcp_servers: dict, dry_run: bool = False) -> bool:
    """Sync MCP configuration to OpenCode harness (preserves all other config)."""
    if not config_path.exists():
        print(f"  ERROR: Config file not found: {config_path}")
        return False
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Only update the 'mcp' section, preserve everything else
    config['mcp'] = mcp_servers
    
    if dry_run:
        print(f"  Would update {config_path}")
        print(f"  MCP servers: {list(mcp_servers.keys())}")
        return True
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
        f.write('\n')
    
    print(f"  ✓ Updated {config_path}")
    print(f"  MCP servers: {list(mcp_servers.keys())}")
    return True


def sync_opencode_skeleton(config_path: Path, mcp_servers: dict, dry_run: bool = False) -> bool:
    """Sync MCP configuration to OpenCode config skeleton (preserves all other config)."""
    if not config_path.exists():
        print(f"  ERROR: Config file not found: {config_path}")
        return False
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Only update the 'mcp' section, preserve everything else
    config['mcp'] = mcp_servers
    
    if dry_run:
        print(f"  Would update {config_path}")
        print(f"  MCP servers: {list(mcp_servers.keys())}")
        return True
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
        f.write('\n')
    
    print(f"  ✓ Updated {config_path}")
    print(f"  MCP servers: {list(mcp_servers.keys())}")
    return True


def sync_codex_harness(config_path: Path, mcp_servers: dict, dry_run: bool = False) -> bool:
    """Sync MCP configuration to Codex harness (preserves all other config).
    
    The mcp_servers dict is already in Codex's TOML-ready format.
    """
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = tomlkit.parse(f.read())
    else:
        print(f"  ERROR: Config file not found: {config_path}")
        return False

    # Build new mcp_servers section (already in correct format)
    mcp_section = tomlkit.table()
    for name, server_config in mcp_servers.items():
        mcp_section[name] = server_config

    # Update only mcp_servers, preserve all other sections
    config['mcp_servers'] = mcp_section

    if dry_run:
        print(f"  Would update {config_path}")
        print(f"  MCP servers: {list(mcp_servers.keys())}")
        return True

    with open(config_path, 'w') as f:
        f.write(tomlkit.dumps(config))

    print(f"  ✓ Updated {config_path}")
    print(f"  MCP servers: {list(mcp_servers.keys())}")
    return True


def sync_amp_harness(config_path: Path, mcp_servers: dict, dry_run: bool = False) -> bool:
    """Sync MCP configuration to Amp harness (preserves all other config).
    
    The mcp_servers dict is already in Amp's format (no 'type' field, command as string).
    """
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {}

    # Amp uses "amp.mcpServers" as a literal key, not nested
    config['amp.mcpServers'] = mcp_servers

    if dry_run:
        print(f"  Would update {config_path}")
        print(f"  MCP servers: {list(mcp_servers.keys())}")
        return True

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
        f.write('\n')

    print(f"  ✓ Updated {config_path}")
    print(f"  MCP servers: {list(mcp_servers.keys())}")
    return True


def set_nested_value(config: dict, json_path: str, value: Any) -> None:
    """Set a value in a nested dict using dot notation path."""
    keys = json_path.split('.')
    current = config
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value


def sync_json_harness(config_path: Path, mcp_servers: dict, json_path: str, dry_run: bool = False) -> bool:
    """Sync MCP configuration to a generic JSON harness (preserves all other config)."""
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {}

    # Set the value at the specified JSON path
    set_nested_value(config, json_path, mcp_servers)

    if dry_run:
        print(f"  Would update {config_path}")
        print(f"  MCP servers: {list(mcp_servers.keys())}")
        return True

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
        f.write('\n')

    print(f"  ✓ Updated {config_path}")
    print(f"  MCP servers: {list(mcp_servers.keys())}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Sync MCP configurations to all harnesses')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without making changes')
    parser.add_argument('--harness', type=str, help='Sync only this specific harness')
    parser.add_argument('--config', type=str, default='mcp-servers.yml', help='Path to YAML config file')
    args = parser.parse_args()

    ensure_required_sync_environment()
    
    # Load YAML config
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}")
        sys.exit(1)
    
    yaml_config = load_yaml_config(config_path)
    print(f"Loaded MCP configuration from {config_path}")
    print(f"Common servers: {list(yaml_config.get('common', {}).keys())}")
    print()
    
    # Sync each harness
    for harness_name, harness_config in yaml_config.get('harnesses', {}).items():
        if args.harness and args.harness != harness_name:
            continue
        
        if not harness_config.get('enabled', True):
            print(f"⊘ Skipping {harness_name} (disabled)")
            continue
        
        print(f"Syncing {harness_name}...")

        # Select the appropriate builder function for this harness
        if harness_name == 'opencode':
            builder_func = build_opencode_server_config
        elif harness_name == 'claude':
            builder_func = build_claude_server_config
        elif harness_name == 'amp':
            builder_func = build_amp_server_config
        elif harness_name == 'kilo':
            builder_func = build_kilo_server_config
        elif harness_name == 'codex':
            builder_func = build_codex_server_config
        elif harness_name == 'gemini' or harness_name == 'qwen':
            # Qwen is forked from Gemini, uses same format
            builder_func = build_gemini_server_config
        else:
            # Default to OpenCode format for unknown harnesses
            builder_func = build_opencode_server_config

        # Build MCP config for this harness
        try:
            mcp_servers = build_mcp_config_for_harness(yaml_config, harness_name, builder_func)
        except ValueError as exc:
            print(f"  ERROR: {exc}")
            print()
            continue
        
        # Get the config path
        config_file_path = expand_path(harness_config['config_path'])
        
        # Sync based on harness type
        success = False

        if harness_name == 'opencode':
            # Sync main opencode.json
            success = sync_opencode_harness(config_file_path, mcp_servers, args.dry_run)
            # Also sync config skeleton
            skeleton_path = config_file_path.parent / 'configs' / 'config_skeleton.json'
            if skeleton_path.exists():
                sync_opencode_skeleton(skeleton_path, mcp_servers, args.dry_run)
        elif harness_name == 'codex':
            success = sync_codex_harness(config_file_path, mcp_servers, args.dry_run)
        elif harness_name == 'amp':
            success = sync_amp_harness(config_file_path, mcp_servers, args.dry_run)
        elif harness_config.get('format') == 'json':
            # Use generic JSON sync with json_path support
            json_path = harness_config.get('json_path', 'mcp')
            success = sync_json_harness(config_file_path, mcp_servers, json_path, args.dry_run)

        if not success:
            print(f"  ✗ Failed to sync {harness_name}")
        
        print()
    
    print("Done!" if not args.dry_run else "Dry run complete!")


if __name__ == '__main__':
    main()
