"""models.py — Pydantic types and canonical tool inventory."""
from typing import Annotated, Literal, Union

from pydantic import BaseModel, field_validator

# ---------------------------------------------------------------------------
# Permission types
# ---------------------------------------------------------------------------

PermissionAction = Literal["allow", "deny", "ask"]
PermissionRule = Union[PermissionAction, dict[str, PermissionAction]]
BaseType = Literal["pure_agent", "subagent"]


class PathRule(BaseModel):
    """Validated path-scoped permission map."""

    rules: dict[str, PermissionAction]

    @field_validator("rules")
    @classmethod
    def catchall_required(cls, v: dict) -> dict:
        if "*" not in v:
            raise ValueError("PathRule must contain a '*' catchall key")
        return v

    def to_dict(self) -> dict[str, PermissionAction]:
        return dict(self.rules)


# ---------------------------------------------------------------------------
# Tool inventory (single source of truth)
# ---------------------------------------------------------------------------

SERENA_FILE_READ_TOOLS: list[str] = [
    "serena_read_file",
    "serena_list_dir",
    "serena_find_file",
    "serena_search_for_pattern",
    "serena_get_symbols_overview",
    "serena_find_symbol",
    "serena_find_referencing_symbols",
]

SERENA_FILE_WRITE_TOOLS: list[str] = [
    "serena_create_text_file",
    "serena_replace_content",
    "serena_replace_symbol_body",
    "serena_insert_after_symbol",
    "serena_insert_before_symbol",
    "serena_rename_symbol",
]

SERENA_MEMORY_TOOLS: list[str] = [
    "serena_read_memory",
    "serena_list_memories",
    "serena_write_memory",
    "serena_edit_memory",
    "serena_delete_memory",
    "serena_rename_memory",
]

SERENA_SESSION_META_TOOLS: list[str] = [
    "serena_activate_project",
    "serena_check_onboarding_performed",
    "serena_get_current_config",
]

SERENA_DISABLED_WORKFLOW_TOOLS: list[str] = [
    "serena_onboarding",
    "serena_prepare_for_new_conversation",
    "serena_initial_instructions",
    "serena_think_about_collected_information",
    "serena_think_about_task_adherence",
    "serena_think_about_whether_you_are_done",
]

CORE_TOOLS: list[str] = [
    "read", "glob", "grep",
    "edit", "apply_patch",
    "bash",
    "webfetch", "websearch",
    "todowrite",
    "question",
]

PLUGIN_TOOLS: list[str] = [
    "task",
    "list_sessions",
    "introspection",
    "read_transcript",
]

ALL_SERENA_TOOLS: list[str] = [
    *SERENA_FILE_READ_TOOLS,
    *SERENA_FILE_WRITE_TOOLS,
    *SERENA_MEMORY_TOOLS,
    *SERENA_SESSION_META_TOOLS,
    *SERENA_DISABLED_WORKFLOW_TOOLS,
    "serena_execute_shell_command",
    "serena_switch_modes",
]

ALL_TOOLS: list[str] = [
    *CORE_TOOLS,
    *PLUGIN_TOOLS,
    *ALL_SERENA_TOOLS,
]

# ---------------------------------------------------------------------------
# Display categories (used by display.py)
# ---------------------------------------------------------------------------

DISPLAY_CATEGORIES: list[tuple[str, list[str]]] = [
    ("Core Read",       ["read", "glob", "grep"]),
    ("Core Write",      ["edit", "apply_patch"]),
    ("Bash / Shell",    ["bash"]),
    ("Web",             ["webfetch", "websearch"]),
    ("Task & Todo",     ["todowrite", "task"]),
    ("General",         ["question"]),
    ("Session",         ["list_sessions", "introspection", "read_transcript"]),
    ("Serena Read",     SERENA_FILE_READ_TOOLS),
    ("Serena Write",    SERENA_FILE_WRITE_TOOLS),
    ("Serena Memory",   SERENA_MEMORY_TOOLS),
    ("Serena Session",  SERENA_SESSION_META_TOOLS),
    ("Serena Workflow", SERENA_DISABLED_WORKFLOW_TOOLS),
    ("Serena Shell",    ["serena_execute_shell_command"]),
    ("Serena Modes",    ["serena_switch_modes"]),
]

# Agents whose config files exist but are managed entirely by opencode internals.
UNMANAGED_AGENTS: frozenset[str] = frozenset({"summary", "title", "compaction", "explore"})
