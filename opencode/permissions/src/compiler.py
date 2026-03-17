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
    "read": "allow", "glob": "allow", "grep": "allow",
    # Write
    "edit": "deny", "apply_patch": "deny",
    # Shell
    "bash": "deny",
    # Web
    "webfetch": "allow", "websearch": "allow",
    # Task / todo
    "todowrite": "allow", "task": "allow",
    # General
    "question": "allow",
    "external_directory": {
        "*": "ask",
        "/home/dzack/ai/*": "allow",
        "/home/dzack/.agents/*": "allow",
        "/tmp/*": "allow",
    },
    # Session
    "list_sessions": "allow", "introspection": "allow", "read_transcript": "allow",
    # Memory
    "remember": "allow", "forget": "allow", "list_memories": "allow",
    # Reminders
    "schedule_reminder": "allow", "cancel_reminder": "allow", "list_reminders": "allow",
    # Skills & timing
    "skill": "allow", "sleep": "allow", "sleep_until": "allow",
    # Code navigation
    "codesearch": "allow", "lsp": "allow",
    # Improved task/todo variants
    "improved_task": "allow", "improved_todowrite": "allow", "improved_todoread": "allow",
    # PTY (terminal — spawn/kill/write denied; list/read allowed)
    "pty_list": "allow", "pty_read": "allow",
    "pty_spawn": "deny", "pty_kill": "deny", "pty_write": "deny",
    # Plannotator (primary-only tools, controlled by plugin's primary_tools config)
    "submit_plan": "allow", "plannotator_review": "allow", "plannotator_annotate": "allow",
    # Core write (write tool = create new files)
    "write": "allow",
    # Token scope inspection
    "tokenscope": "allow",
    # Zotero plugin tools
    "zotero_search": "allow", "zotero_get_item": "allow", "zotero_import": "allow",
    "zotero_batch_add": "allow", "zotero_update_item": "allow", "zotero_trash_items": "allow",
    "zotero_export": "allow", "zotero_tags": "allow", "zotero_stats": "allow",
    "zotero_collections": "allow", "zotero_count": "allow", "zotero_children": "allow",
    "zotero_check_pdfs": "allow", "zotero_fetch_pdfs": "allow",
    "zotero_find_dois": "allow", "zotero_crossref": "allow",
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
    "serena_read_file": "deny", "serena_list_dir": "deny",
    "serena_find_file": "deny", "serena_search_for_pattern": "deny",
    "serena_get_symbols_overview": "deny", "serena_find_symbol": "deny",
    "serena_find_referencing_symbols": "allow",
    # Serena write
    "serena_create_text_file": "deny", "serena_replace_content": "allow",
    "serena_replace_symbol_body": "allow", "serena_insert_after_symbol": "allow",
    "serena_insert_before_symbol": "allow", "serena_rename_symbol": "allow",
    # Serena memory
    "serena_read_memory": "deny", "serena_list_memories": "deny",
    "serena_write_memory": "deny", "serena_edit_memory": "deny",
    "serena_delete_memory": "deny", "serena_rename_memory": "deny",
    # Serena session / meta
    "serena_activate_project": "allow",
    "serena_check_onboarding_performed": "deny",
    "serena_get_current_config": "deny",
    # Serena workflow (always disabled)
    "serena_onboarding": "deny", "serena_prepare_for_new_conversation": "deny",
    "serena_initial_instructions": "deny",
    "serena_think_about_collected_information": "deny",
    "serena_think_about_task_adherence": "deny",
    "serena_think_about_whether_you_are_done": "deny",
    # Serena shell bypass
    "serena_execute_shell_command": "deny",
    # Serena modes
    "serena_switch_modes": "deny",
}

# ---------------------------------------------------------------------------
# Base-type permission adjustments
# ---------------------------------------------------------------------------

_PURE_AGENT_BASE: dict = {
    "task": "allow", "todowrite": "allow",
}

_SUBAGENT_BASE: dict = {
    "task": "deny", "todowrite": "deny",
    "improved_task": "deny", "improved_todowrite": "deny",
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
