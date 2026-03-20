"""compiler.py — Global defaults, base-type permissions, and agent compiler."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml

from src.mixins import (
    deep_merge,
    mixin_allow_all_permissions,
    mixin_bash_standard,
    mixin_bash_unrestricted,
    mixin_code_writer,
    mixin_docs_writer,
    mixin_interactive,
    mixin_orchestrator,
    mixin_planner,
    mixin_researcher,
    mixin_reviewer,
    mixin_session_tools,
    mixin_test_writer,
)

if TYPE_CHECKING:
    from base import Agent

# ---------------------------------------------------------------------------
# YAML Ruleset Loader
# ---------------------------------------------------------------------------

_RULESETS_CACHE: dict[str, list[str]] | None = None


def _load_rulesets_yaml() -> dict[str, list[str]]:
    """Load ruleset definitions from rulesets.yaml."""
    global _RULESETS_CACHE
    if _RULESETS_CACHE is not None:
        return _RULESETS_CACHE

    rulesets_file = Path(__file__).parent / "rulesets.yaml"
    with open(rulesets_file) as f:
        data = yaml.safe_load(f) or {}
    _RULESETS_CACHE = data
    return _RULESETS_CACHE


_MIXIN_REGISTRY: dict[str, callable] = {
    "mixin_interactive": mixin_interactive,
    "mixin_planner": mixin_planner,
    "mixin_orchestrator": mixin_orchestrator,
    "mixin_code_writer": mixin_code_writer,
    "mixin_test_writer": mixin_test_writer,
    "mixin_docs_writer": mixin_docs_writer,
    "mixin_reviewer": mixin_reviewer,
    "mixin_researcher": mixin_researcher,
    "mixin_bash_unrestricted": mixin_bash_unrestricted,
    "mixin_bash_standard": mixin_bash_standard,
    "mixin_session_tools": mixin_session_tools,
    "mixin_allow_all": mixin_allow_all_permissions,
}


def resolve_ruleset(ruleset_name: str) -> list[dict]:
    """Resolve a ruleset name to a list of permission dicts (layers)."""
    rulesets = _load_rulesets_yaml()
    if ruleset_name not in rulesets:
        raise ValueError(
            f"Unknown ruleset: {ruleset_name}. Available: {list(rulesets.keys())}"
        )

    mixin_names = rulesets[ruleset_name]
    layers = []
    for mixin_name in mixin_names:
        if mixin_name not in _MIXIN_REGISTRY:
            raise ValueError(
                f"Unknown mixin: {mixin_name}. Available: {list(_MIXIN_REGISTRY.keys())}"
            )
        layers.append(_MIXIN_REGISTRY[mixin_name]())
    return layers


# ---------------------------------------------------------------------------
# Global defaults — explicit action for every known tool
# ---------------------------------------------------------------------------

GLOBAL_DEFAULTS: dict[str, Any] = {
    # Read
    "read": "allow",
    "glob": "allow",
    "grep": "allow",
    # Write
    "edit": "deny",
    "apply_patch": "deny",
    # Shell
    "bash": {"*sudo*": "deny", "*": "deny"},
    # Web
    "webfetch": "allow",
    "websearch": "allow",
    # Task / todo
    "todowrite": "allow",
    "task": "allow",
    # General
    "question": "allow",
    "external_directory": {
        "*": "ask",
        "/home/dzack/ai/*": "allow",
        "/home/dzack/.agents/*": "allow",
        "/home/dzack/.plannotator/*": "allow",
        "/tmp/*": "allow",
    },
    # Session
    "list_sessions": "allow",
    "introspection": "allow",
    "read_transcript": "allow",
    # Memory
    "remember": "allow",
    "forget": "allow",
    "list_memories": "allow",
    # Skills & timing
    "skill": "allow",
    "sleep": "allow",
    "sleep_until": "allow",
    # Code navigation
    "codesearch": "allow",
    "lsp": "allow",
    # PTY (terminal — spawn/kill/write denied; list/read allowed)
    "pty_list": "allow",
    "pty_read": "allow",
    "pty_spawn": "deny",
    "pty_kill": "deny",
    "pty_write": "deny",
    # Plannotator (primary-only tools, controlled by plugin's primary_tools config)
    "submit_plan": "allow",
    "plannotator_review": "allow",
    "plannotator_annotate": "allow",
    # Core write (write tool = create new files)
    "write": "allow",
    # Token scope inspection
    "tokenscope": "allow",
    # Misc
    "invalid": "deny",
    # Cut-copy-paste MCP
    "cut-copy-paste-mcp_cut_lines": "allow",
    "cut-copy-paste-mcp_copy_lines": "allow",
    "cut-copy-paste-mcp_paste_lines": "allow",
    "cut-copy-paste-mcp_get_operation_history": "allow",
    "cut-copy-paste-mcp_show_clipboard": "allow",
    "cut-copy-paste-mcp_undo_last_paste": "allow",
    # Serena read
    "serena_read_file": "deny",
    "serena_list_dir": "deny",
    "serena_find_file": "deny",
    "serena_search_for_pattern": "deny",
    "serena_get_symbols_overview": "deny",
    "serena_find_symbol": "deny",
    "serena_find_referencing_symbols": "allow",
    # Serena write
    "serena_create_text_file": "deny",
    "serena_replace_content": "deny",
    "serena_replace_symbol_body": "allow",
    "serena_insert_after_symbol": "allow",
    "serena_insert_before_symbol": "allow",
    "serena_rename_symbol": "allow",
    # Serena memory
    "serena_read_memory": "deny",
    "serena_list_memories": "deny",
    "serena_write_memory": "deny",
    "serena_edit_memory": "deny",
    "serena_delete_memory": "deny",
    "serena_rename_memory": "deny",
    # Serena session / meta
    "serena_activate_project": "allow",
    "serena_check_onboarding_performed": "deny",
    "serena_get_current_config": "deny",
    # Serena workflow (always disabled)
    "serena_onboarding": "deny",
    "serena_prepare_for_new_conversation": "deny",
    "serena_initial_instructions": "deny",
    "serena_think_about_collected_information": "deny",
    "serena_think_about_task_adherence": "deny",
    "serena_think_about_whether_you_are_done": "deny",
    # Serena shell bypass
    "serena_execute_shell_command": "deny",
    # Serena modes
    "serena_switch_modes": "deny",
    # Provider Quotas
    "gemini_quota": "allow",
}

# ---------------------------------------------------------------------------
# Base-type permission adjustments
# ---------------------------------------------------------------------------

_PURE_AGENT_BASE: dict[str, str] = {
    "task": "allow",
    "todowrite": "allow",
}

_SUBAGENT_BASE: dict[str, str] = {
    "task": "deny",
    "todowrite": "deny",
}

_BASE_TYPE_PERMS: dict[str, dict[str, str]] = {
    "pure_agent": _PURE_AGENT_BASE,
    "subagent": _SUBAGENT_BASE,
}

# ---------------------------------------------------------------------------
# Compiler
# ---------------------------------------------------------------------------


def compile_agent(agent: Agent) -> dict[str, Any]:
    """Compile an Agent into a flat permission dict.

    Layer order (lowest → highest precedence):
      1. GLOBAL_DEFAULTS
      2. Base-type adjustments (pure_agent vs subagent)
      3. Agent's permission_layers() in order
      4. Agent's overrides
    """
    layers = [
        GLOBAL_DEFAULTS,
        _BASE_TYPE_PERMS[agent.base_type],
        *agent.permission_layers(),
    ]
    if agent.overrides:
        layers.append(agent.overrides)
    return deep_merge(*layers)


def compile_from_ruleset(
    ruleset_name: str,
    base_type: str = "pure_agent",
    overrides: dict | None = None,
) -> dict[str, Any]:
    """Compile permissions from a YAML ruleset name.

    Layer order (lowest → highest precedence):
      1. GLOBAL_DEFAULTS
      2. Base-type adjustments (pure_agent vs subagent)
      3. Ruleset layers (from rulesets.yaml)
      4. Optional overrides

    Args:
        ruleset_name: Name of ruleset from rulesets.yaml
        base_type: 'pure_agent' or 'subagent'
        overrides: Final permission overrides (optional)
    """
    layers = [
        GLOBAL_DEFAULTS,
        _BASE_TYPE_PERMS.get(base_type, _PURE_AGENT_BASE),
        *resolve_ruleset(ruleset_name),
    ]
    if overrides:
        layers.append(overrides)
    return deep_merge(*layers)
