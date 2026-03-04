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
    python3 sync_mcp_configs.py [--dry-run] [--harness <name>]
"""

import argparse
import json
import os
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


def load_yaml_config(config_path: str) -> dict:
    """Load the centralized YAML configuration."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def build_mcp_config_for_harness(yaml_config: dict, harness_name: str) -> dict:
    """Build the MCP configuration for a specific harness in OpenCode format."""
    mcp_servers = {}
    
    # Add common servers
    for name, server_config in yaml_config.get('common', {}).items():
        if server_config.get('enabled', True):
            mcp_servers[name] = build_opencode_server_config(server_config, 'local')
    
    # Add harness-specific servers
    harness_specific = yaml_config.get('harness_specific', {}).get(harness_name, {})
    for name, server_config in harness_specific.items():
        if server_config.get('enabled', True):
            server_type = server_config.get('type', 'local')
            mcp_servers[name] = build_opencode_server_config(server_config, server_type)
    
    return mcp_servers


def build_opencode_server_config(config: dict, server_type: str) -> dict:
    """Build a server configuration in OpenCode format."""
    if server_type == 'remote':
        return {
            'type': 'remote',
            'url': config.get('url', '')
        }
    else:
        return {
            'type': 'local',
            'command': [config.get('command', '')] + config.get('args', [])
        }


def build_amp_server_config(config: dict) -> dict:
    """Build a server configuration in Amp format."""
    command = config.get('command', '')
    args = config.get('args', [])
    return {
        'command': command,
        'args': args
    }


def build_codex_server_config(config: dict) -> dict:
    """Build a server configuration in Codex TOML format."""
    command = config.get('command', '')
    args = config.get('args', [])
    return {
        'command': command,
        'args': args,
        'enabled': True
    }


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
    """Sync MCP configuration to Codex harness (preserves all other config)."""
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = tomlkit.parse(f.read())
    else:
        print(f"  ERROR: Config file not found: {config_path}")
        return False
    
    # Remove existing mcp_servers section
    if 'mcp_servers' in config:
        del config['mcp_servers']
    
    # Create new mcp_servers section
    mcp_section = tomlkit.table()
    for name, server_config in mcp_servers.items():
        mcp_section[name] = build_codex_server_config(server_config)
    
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
    """Sync MCP configuration to Amp harness (preserves all other config)."""
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    
    # Convert to Amp's format
    amp_mcp_servers = {}
    for name, server_config in mcp_servers.items():
        amp_mcp_servers[name] = build_amp_server_config(server_config)
    
    # Amp uses "amp.mcpServers" as a literal key, not nested
    config['amp.mcpServers'] = amp_mcp_servers
    
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
        
        # Build MCP config for this harness
        mcp_servers = build_mcp_config_for_harness(yaml_config, harness_name)
        
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
            success = sync_opencode_harness(config_file_path, mcp_servers, args.dry_run)
        
        if not success:
            print(f"  ✗ Failed to sync {harness_name}")
        
        print()
    
    print("Done!" if not args.dry_run else "Dry run complete!")


if __name__ == '__main__':
    main()
