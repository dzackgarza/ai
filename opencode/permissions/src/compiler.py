"""compiler.py — Global defaults, base-type permissions, and agent compiler."""
from __future__ import annotations

from typing import TYPE_CHECKING

from src.mixins import deep_merge

if TYPE_CHECKING:
    from base import Agent

# ---------------------------------------------------------------------------
# Global defaults — explicit action for every known tool
# ---------------------------------------------------------------------------

GLOBAL_DEFAULTS: dict = {
    # Read
    "read": "allow", "glob": "allow", "grep": "allow", "list": "allow",
    # Write
    "edit": "deny", "patch": "deny", "apply_patch": "deny",
    # Shell
    "bash": "deny",
    # Web
    "webfetch": "allow", "websearch": "allow",
    # Task / todo
    "todoread": "allow", "todowrite": "allow", "task": "allow",
    # General
    "question": "allow", "external_directory": "deny",
    # Planning
    "plan_exit": "deny", "write_plan": "deny",
    # Async
    "async_subagent": "deny", "async_command": "deny",
    # Session
    "list_sessions": "allow", "introspection": "allow", "read_transcript": "allow",
    # Git
    "git_add": "deny", "git_commit": "deny",
    # Cut-copy-paste MCP
    "cut-copy-paste-mcp_cut": "deny",
    "cut-copy-paste-mcp_copy": "deny",
    "cut-copy-paste-mcp_paste": "deny",
    # Serena read
    "serena_read_file": "deny", "serena_list_dir": "deny",
    "serena_find_file": "deny", "serena_search_for_pattern": "deny",
    "serena_get_symbols_overview": "deny", "serena_find_symbol": "deny",
    "serena_find_referencing_symbols": "deny",
    # Serena write
    "serena_create_text_file": "deny", "serena_replace_content": "deny",
    "serena_replace_symbol_body": "deny", "serena_insert_after_symbol": "deny",
    "serena_insert_before_symbol": "deny", "serena_rename_symbol": "deny",
    "serena_delete_lines": "deny", "serena_insert_at_line": "deny",
    "serena_replace_lines": "deny",
    # Serena memory
    "serena_read_memory": "allow", "serena_list_memories": "allow",
    "serena_write_memory": "allow", "serena_edit_memory": "allow",
    "serena_delete_memory": "allow", "serena_rename_memory": "allow",
    # Serena session / meta
    "serena_activate_project": "allow",
    "serena_check_onboarding_performed": "allow",
    "serena_get_current_config": "allow",
    # Serena workflow (always disabled)
    "serena_onboarding": "deny", "serena_prepare_for_new_conversation": "deny",
    "serena_initial_instructions": "deny",
    "serena_think_about_collected_information": "deny",
    "serena_think_about_task_adherence": "deny",
    "serena_think_about_whether_you_are_done": "deny",
    # Serena shell bypass
    "serena_execute_shell_command": "deny",
}

# ---------------------------------------------------------------------------
# Base-type permission adjustments
# ---------------------------------------------------------------------------

_PURE_AGENT_BASE: dict = {
    "task": "allow", "todoread": "allow", "todowrite": "allow",
}

_SUBAGENT_BASE: dict = {
    "task": "deny", "todoread": "deny", "todowrite": "deny",
    "plan_exit": "deny", "async_command": "deny", "async_subagent": "deny",
}

_BASE_TYPE_PERMS: dict = {
    "pure_agent": _PURE_AGENT_BASE,
    "subagent":   _SUBAGENT_BASE,
}

# ---------------------------------------------------------------------------
# Compiler
# ---------------------------------------------------------------------------

def compile_agent(agent: Agent) -> dict:
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
