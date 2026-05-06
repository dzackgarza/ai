"""compiler.py — Global defaults, base-type permissions, and agent compiler."""

from __future__ import annotations

from importlib import import_module
from typing import Any

from src.mixins import deep_merge

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
# Ruleset Resolver — imports Python ruleset classes by name
# ---------------------------------------------------------------------------

_RULESET_CACHE: dict[str, type] = {}


def resolve_ruleset(ruleset_name: str) -> list[dict]:
    """Resolve a ruleset name to a list of permission dicts (layers).

    Imports the ruleset class from src.rulesets.<name> and calls .layers().
    Ruleset name is normalized: 'interactive' → 'Interactive' class.
    """
    if ruleset_name in _RULESET_CACHE:
        ruleset_class = _RULESET_CACHE[ruleset_name]
    else:
        # Normalize: 'interactive' → 'Interactive', 'code_writer' → 'CodeWriter'
        class_name = "".join(part.capitalize() for part in ruleset_name.split("_"))

        try:
            module = import_module(f"src.rulesets.{ruleset_name}")
            ruleset_class = getattr(module, class_name)
            _RULESET_CACHE[ruleset_name] = ruleset_class
        except (ImportError, AttributeError) as e:
            raise ValueError(
                f"Unknown ruleset: {ruleset_name} (expected class {class_name} in src/rulesets/{ruleset_name}.py)"
            ) from e

    return ruleset_class.layers()


def compile_from_tags(
    permission_tags: list[str],
    base_type: str = "pure_agent",
    overrides: dict | None = None,
) -> dict[str, Any]:
    """Compile permissions from a list of permission tags.

    Layer order (lowest → highest precedence):
      1. GLOBAL_DEFAULTS
      2. Base-type adjustments (pure_agent vs subagent)
      3. Ruleset layers for each tag (in order)
      4. Optional overrides

    Args:
        permission_tags: List of tags matching ruleset names
        base_type: 'pure_agent' or 'subagent'
        overrides: Final permission overrides (optional)
    """
    layers = [
        GLOBAL_DEFAULTS,
        _BASE_TYPE_PERMS.get(base_type, _PURE_AGENT_BASE),
    ]

    # Apply ruleset layers for each tag in order
    for tag in permission_tags:
        layers.extend(resolve_ruleset(tag))

    if overrides:
        layers.append(overrides)

    return deep_merge(*layers)
