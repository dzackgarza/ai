#!/usr/bin/env python3
"""manage_permissions_v2.py -- Layered permission system for OpenCode agents.

Architecture:
    GLOBAL_DEFAULTS (all agents)
  + BASE_TYPE (pure_agent or subagent)
  + MIXINS (ordered list: interactive, planner, code_writer, etc.)
  = compiled permission dict
"""
import json
import os
import sys
import argparse
from dataclasses import dataclass, field
from typing import Literal

base_dir = os.path.expanduser("~/.config/opencode")
skeleton_path = os.path.join(base_dir, "configs", "config_skeleton.json")
agents_dir = os.path.join(base_dir, "configs", "agents")
subagents_dir = os.path.join(base_dir, "configs", "subagents")

# =============================================================================
# SERENA TOOL INVENTORY
# =============================================================================

SERENA_FILE_READ_TOOLS = [
    "serena_read_file",
    "serena_list_dir",
    "serena_find_file",
    "serena_search_for_pattern",
    "serena_get_symbols_overview",
    "serena_find_symbol",
    "serena_find_referencing_symbols",
]

SERENA_FILE_WRITE_TOOLS = [
    "serena_create_text_file",
    "serena_replace_content",
    "serena_replace_symbol_body",
    "serena_insert_after_symbol",
    "serena_insert_before_symbol",
    "serena_rename_symbol",
    "serena_delete_lines",
    "serena_insert_at_line",
    "serena_replace_lines",
]

SERENA_MEMORY_TOOLS = [
    "serena_read_memory",
    "serena_list_memories",
    "serena_write_memory",
    "serena_edit_memory",
    "serena_delete_memory",
    "serena_rename_memory",
]

SERENA_SESSION_META_TOOLS = [
    "serena_activate_project",
    "serena_check_onboarding_performed",
    "serena_get_current_config",
]

SERENA_DISABLED_WORKFLOW_TOOLS = [
    "serena_onboarding",
    "serena_prepare_for_new_conversation",
    "serena_initial_instructions",
    "serena_think_about_collected_information",
    "serena_think_about_task_adherence",
    "serena_think_about_whether_you_are_done",
]

SERENA_DENY_TOOLS = [
    "serena_execute_shell_command",
    *SERENA_DISABLED_WORKFLOW_TOOLS,
]

# =============================================================================
# PATH RULE BUILDERS
# =============================================================================

def make_path_rule(allow_globs, deny_globs=None):
    """Build a path-scoped rule dict."""
    deny_globs = deny_globs or []
    rule = {}

    if allow_globs == ["*"]:
        rule["*"] = "allow"
    elif allow_globs == []:
        rule["*"] = "deny"
    else:
        rule["*"] = "deny"
        for g in allow_globs:
            rule[g] = "allow"

    for g in deny_globs:
        rule[g] = "deny"

    return rule


def read_only_in(allow_globs, deny_globs=None):
    """Return read tool permissions scoped to paths."""
    rule = make_path_rule(allow_globs, deny_globs)
    perms = {}
    read_tools = [
        "read", "glob", "grep", "list",
        *SERENA_FILE_READ_TOOLS,
    ]
    for tool in read_tools:
        perms[tool] = rule
    return perms


def write_only_in(allow_globs, deny_globs=None):
    """Return write tool permissions scoped to paths."""
    rule = make_path_rule(allow_globs, deny_globs)
    perms = {}
    perms["edit"] = rule
    perms["apply_patch"] = rule
    perms["patch"] = rule

    mutation_tools = [
        *SERENA_FILE_WRITE_TOOLS,
        "cut-copy-paste-mcp_cut",
        "cut-copy-paste-mcp_copy",
        "cut-copy-paste-mcp_paste",
    ]
    for tool in mutation_tools:
        perms[tool] = rule

    return perms


# =============================================================================
# MERGE UTILITIES
# =============================================================================

def deep_merge(*dicts):
    """Merge dicts: nested sub-dicts are merged at key level, flat values overwrite."""
    result = {}
    for d in dicts:
        for key, value in d.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = {**result[key], **value}
            else:
                result[key] = value
    return result


# =============================================================================
# ALL KNOWN TOOLS (exhaustive list)
# =============================================================================

# Core OpenCode tools
CORE_TOOLS = [
    "read", "glob", "grep", "list",
    "edit", "patch", "apply_patch",
    "bash",
    "webfetch", "websearch",
    "todoread", "todowrite",
    "question",
    "external_directory",
]

# Local custom plugins (plugins/*.ts)
PLUGIN_TOOLS = [
    "task",
    "plan_exit",
    "async_subagent",
    "async_command",
    "list_sessions",
    "introspection",
    "write_plan",
    "read_transcript",
    "git_add",
    "git_commit",
]

# MCP: cut-copy-paste
CUT_COPY_PASTE_TOOLS = [
    "cut-copy-paste-mcp_cut",
    "cut-copy-paste-mcp_copy",
    "cut-copy-paste-mcp_paste",
]

# All Serena tools
ALL_SERENA_TOOLS = [
    *SERENA_FILE_READ_TOOLS,
    *SERENA_FILE_WRITE_TOOLS,
    *SERENA_MEMORY_TOOLS,
    *SERENA_SESSION_META_TOOLS,
    *SERENA_DISABLED_WORKFLOW_TOOLS,
    "serena_execute_shell_command",
]

# Complete tool inventory
ALL_TOOLS = [
    *CORE_TOOLS,
    *PLUGIN_TOOLS,
    *CUT_COPY_PASTE_TOOLS,
    *ALL_SERENA_TOOLS,
]


# =============================================================================
# GLOBAL DEFAULTS (explicit permission for EVERY known tool)
# =============================================================================

GLOBAL_DEFAULTS = {
    # -------------------------------------------------------------------------
    # READ TOOLS
    # -------------------------------------------------------------------------
    "read": "allow",
    "glob": "allow",
    "grep": "allow",
    "list": "allow",

    # -------------------------------------------------------------------------
    # WRITE TOOLS
    # -------------------------------------------------------------------------
    "edit": "deny",
    "patch": "deny",
    "apply_patch": "deny",

    # -------------------------------------------------------------------------
    # BASH / SHELL ACCESS
    # -------------------------------------------------------------------------
    "bash": "deny",

    # -------------------------------------------------------------------------
    # WEB ACCESS
    # -------------------------------------------------------------------------
    "webfetch": "allow",
    "websearch": "allow",

    # -------------------------------------------------------------------------
    # TASK & TODO MANAGEMENT
    # -------------------------------------------------------------------------
    "todoread": "allow",
    "todowrite": "allow",
    "task": "allow",

    # -------------------------------------------------------------------------
    # GENERAL TOOLS
    # -------------------------------------------------------------------------
    "question": "allow",
    "external_directory": "deny",

    # -------------------------------------------------------------------------
    # PLANNING & WORKFLOW
    # -------------------------------------------------------------------------
    "plan_exit": "deny",
    "write_plan": "deny",

    # -------------------------------------------------------------------------
    # ASYNC OPERATIONS
    # -------------------------------------------------------------------------
    "async_subagent": "deny",
    "async_command": "deny",

    # -------------------------------------------------------------------------
    # SESSION INTROSPECTION
    # -------------------------------------------------------------------------
    "list_sessions": "allow",
    "introspection": "allow",
    "read_transcript": "allow",

    # -------------------------------------------------------------------------
    # GIT OPERATIONS
    # -------------------------------------------------------------------------
    "git_add": "deny",
    "git_commit": "deny",

    # -------------------------------------------------------------------------
    # CUT-COPY-PASTE MCP
    # -------------------------------------------------------------------------
    "cut-copy-paste-mcp_cut": "deny",
    "cut-copy-paste-mcp_copy": "deny",
    "cut-copy-paste-mcp_paste": "deny",

    # -------------------------------------------------------------------------
    # SERENA TOOLS
    # -------------------------------------------------------------------------
    # --- Serena File Read Tools ---
    "serena_read_file": "deny",
    "serena_list_dir": "deny",
    "serena_find_file": "deny",
    "serena_search_for_pattern": "deny",
    "serena_get_symbols_overview": "deny",
    "serena_find_symbol": "deny",
    "serena_find_referencing_symbols": "deny",

    # --- Serena File Write Tools ---
    "serena_create_text_file": "deny",
    "serena_replace_content": "deny",
    "serena_replace_symbol_body": "deny",
    "serena_insert_after_symbol": "deny",
    "serena_insert_before_symbol": "deny",
    "serena_rename_symbol": "deny",
    "serena_delete_lines": "deny",
    "serena_insert_at_line": "deny",
    "serena_replace_lines": "deny",

    # --- Serena Memory Tools ---
    "serena_read_memory": "allow",
    "serena_list_memories": "allow",
    "serena_write_memory": "allow",
    "serena_edit_memory": "allow",
    "serena_delete_memory": "allow",
    "serena_rename_memory": "allow",

    # --- Serena Session & Meta Tools ---
    "serena_activate_project": "allow",
    "serena_check_onboarding_performed": "allow",
    "serena_get_current_config": "allow",

    # --- Serena Workflow Tools (Disabled) ---
    "serena_onboarding": "deny",
    "serena_prepare_for_new_conversation": "deny",
    "serena_initial_instructions": "deny",
    "serena_think_about_collected_information": "deny",
    "serena_think_about_task_adherence": "deny",
    "serena_think_about_whether_you_are_done": "deny",

    # --- Serena Shell Bypass ---
    "serena_execute_shell_command": "deny",
}


# =============================================================================
# BASE TYPE PERMISSIONS
# =============================================================================

PURE_AGENT_BASE = {
    # Primary agents can use coordination tools
    "task": "allow",
    "todoread": "allow",
    "todowrite": "allow",
}

SUBAGENT_BASE = {
    # Subagents cannot coordinate or use workflow tools
    "task": "deny",
    "todoread": "deny",
    "todowrite": "deny",
    "plan_exit": "deny",
    "async_command": "deny",
    "async_subagent": "deny",
}


# =============================================================================
# MIXINS (reusable permission patterns)
# =============================================================================

def mixin_interactive():
    """Interactive agent: full file access, unrestricted bash."""
    return deep_merge(
        read_only_in(["*"]),
        write_only_in(["*"]),
        {"bash": "allow"},
    )


def mixin_planner():
    """Planner agent: read all, write plans only, can exit plan mode."""
    return deep_merge(
        read_only_in(["*"]),
        write_only_in(["*.serena/plans*"]),
        {"write_plan": "allow", "plan_exit": "allow"},
    )


def mixin_orchestrator():
    """Orchestrator: can dispatch tasks, read/write todos."""
    return {
        "task": "allow",
        "todoread": "allow",
        "todowrite": "allow",
    }


def mixin_code_writer():
    """Code writer: read src+plans, write src."""
    return deep_merge(
        read_only_in(["*src*", "*.serena/plans*"], deny_globs=["*test*", "*tests*", "*docs*"]),
        write_only_in(["*src*"]),
    )


def mixin_test_writer():
    """Test writer: read tests+plans, write tests."""
    return deep_merge(
        read_only_in(["*tests*", "*test*", "*.serena/plans*"], deny_globs=["*src*", "*docs*"]),
        write_only_in(["*tests*", "*test*"]),
    )


def mixin_docs_writer():
    """Docs writer: read docs+plans, write docs."""
    return deep_merge(
        read_only_in(["*docs*", "*.serena/plans*"], deny_globs=["*src*", "*test*", "*tests*"]),
        write_only_in(["*docs*"]),
    )


def mixin_reviewer():
    """Reviewer: read all, write none."""
    return deep_merge(
        read_only_in(["*"]),
        write_only_in([]),
    )


def mixin_researcher():
    """Researcher: read all, write none."""
    return deep_merge(
        read_only_in(["*"]),
        write_only_in([]),
    )


def mixin_git():
    """Allow git staging and commit."""
    return {"git_add": "allow", "git_commit": "allow"}


def mixin_bash_standard():
    """Allow standard safe bash commands."""
    return {
        "bash": {
            # Filesystem metadata
            "du*": "allow",
            "file *": "allow",
            "ls*": "allow",
            "pwd*": "allow",
            "stat*": "allow",
            "tree*": "allow",
            # Text inspection
            "cut*": "allow",
            "diff*": "allow",
            "grep*": "allow",
            "rg*": "allow",
            "head*": "allow",
            "tail*": "allow",
            "less*": "allow",
            "sort*": "allow",
            "wc*": "allow",
            "jq": "allow",
            # Find with guardrails
            "find *": "allow",
            "find * -delete*": "ask",
            "find * -exec*": "ask",
            # Test runners
            "just*": "allow",
            "pytest*": "allow",
            "uv*": "allow",
            # Content read
            "cat*": "deny",
            "*": "deny",
        }
    }


def mixin_bash_unrestricted():
    """Allow all bash commands."""
    return {"bash": "allow"}


def mixin_session_tools():
    """Allow introspection, session listing, transcript reading."""
    return {
        "introspection": "allow",
        "list_sessions": "allow",
        "read_transcript": "allow",
    }


def mixin_external_directory(*paths):
    """Allow access to external directories."""
    return {"external_directory": {p: "allow" for p in paths}}


# Mixin registry for validation
MIXIN_REGISTRY = {
    "interactive": mixin_interactive,
    "planner": mixin_planner,
    "orchestrator": mixin_orchestrator,
    "code_writer": mixin_code_writer,
    "test_writer": mixin_test_writer,
    "docs_writer": mixin_docs_writer,
    "reviewer": mixin_reviewer,
    "researcher": mixin_researcher,
    "git": mixin_git,
    "bash_standard": mixin_bash_standard,
    "bash_unrestricted": mixin_bash_unrestricted,
    "session_tools": mixin_session_tools,
}


# =============================================================================
# AGENT DEFINITIONS
# =============================================================================

@dataclass
class AgentDef:
    """Defines an agent's permissions.

    base_type: Either "pure_agent" or "subagent"
    mixins: Ordered list of mixin names to apply
    overrides: Final overrides applied after all layers
    """
    base_type: Literal["pure_agent", "subagent"]
    mixins: list[str]
    overrides: dict = field(default_factory=dict)


AGENTS = {
    # --- Primary Agents ---
    "Interactive": AgentDef(
        base_type="pure_agent",
        mixins=["orchestrator", "session_tools", "interactive", "bash_unrestricted"],
    ),
    "Plan (Custom)": AgentDef(
        base_type="pure_agent",
        mixins=["planner"],
    ),
    "plan": AgentDef(
        base_type="pure_agent",
        mixins=["planner"],
    ),
    "Ralph Planner": AgentDef(
        base_type="pure_agent",
        mixins=["planner"],
    ),
    "Repository Steward": AgentDef(
        base_type="pure_agent",
        mixins=["planner"],
    ),
    "Build (Custom)": AgentDef(
        base_type="pure_agent",
        mixins=["orchestrator", "interactive", "git"],
        overrides={"write_plan": "deny"},
    ),
    "build": AgentDef(
        base_type="pure_agent",
        mixins=["orchestrator", "interactive", "git"],
        overrides={"write_plan": "deny"},
    ),
    "(Lattice) Build": AgentDef(
        base_type="pure_agent",
        mixins=["orchestrator", "interactive", "git"],
        overrides={"write_plan": "deny"},
    ),
    "Zotero Librarian": AgentDef(
        base_type="pure_agent",
        mixins=["orchestrator", "session_tools"],
        overrides={
            "edit": {"*": "deny"},
            "apply_patch": {"*": "deny"},
            "patch": {"*": "deny"},
        },
    ),
    "Minimal": AgentDef(
        base_type="pure_agent",
        mixins=["bash_unrestricted", "orchestrator"],
        overrides={
            "plan_exit": "deny",
            "external_directory": {"/tmp/opencode_test/*": "allow"},
        },
    ),

    # --- Subagents: Writers ---
    "Writer: General Code": AgentDef(
        base_type="subagent",
        mixins=["code_writer", "git"],
    ),
    "Writer: Python": AgentDef(
        base_type="subagent",
        mixins=["code_writer", "git"],
    ),
    "Writer: TypeScript": AgentDef(
        base_type="subagent",
        mixins=["code_writer", "git"],
    ),
    "Writer: SageMath": AgentDef(
        base_type="subagent",
        mixins=["code_writer", "git"],
    ),
    "Writer: Refactorer": AgentDef(
        base_type="subagent",
        mixins=["code_writer", "git"],
    ),
    "Writer: Tests": AgentDef(
        base_type="subagent",
        mixins=["test_writer", "git"],
    ),
    "Writer: Documentation": AgentDef(
        base_type="subagent",
        mixins=["docs_writer", "git"],
    ),

    # --- Subagents: Reviewers ---
    "Reviewer: Code": AgentDef(
        base_type="subagent",
        mixins=["reviewer"],
    ),
    "Reviewer: Plans": AgentDef(
        base_type="subagent",
        mixins=["reviewer"],
    ),
    "Reviewer: Test Compliance": AgentDef(
        base_type="subagent",
        mixins=["reviewer"],
    ),
    "Reviewer: Semantic Audit": AgentDef(
        base_type="subagent",
        mixins=["reviewer"],
    ),
    "Reviewer: Plan Contract": AgentDef(
        base_type="subagent",
        mixins=["reviewer"],
    ),

    # --- Subagents: Researchers ---
    "Researcher: Code Base": AgentDef(
        base_type="subagent",
        mixins=["researcher"],
    ),
    "Researcher: Documentation": AgentDef(
        base_type="subagent",
        mixins=["researcher"],
    ),
    "Researcher: Repo Explorer": AgentDef(
        base_type="subagent",
        mixins=["researcher"],
    ),
    "general": AgentDef(
        base_type="subagent",
        mixins=["researcher"],
    ),

    # --- Subagents: Lattice ---
    "(Lattice) Researcher: Documentation": AgentDef(
        base_type="subagent",
        mixins=["researcher"],
    ),
    "(Lattice) Reviewer: Documentation Librarian": AgentDef(
        base_type="subagent",
        mixins=["reviewer"],
    ),
    "(Lattice) Reviewer: Checklist Completionist": AgentDef(
        base_type="subagent",
        mixins=["reviewer"],
    ),
    "(Lattice) Reviewer: Test Coverage": AgentDef(
        base_type="subagent",
        mixins=["reviewer"],
    ),
    "(Lattice) Writer: Test Methods": AgentDef(
        base_type="subagent",
        mixins=["test_writer", "git"],
    ),
    "(Lattice) Writer: Interface Designer": AgentDef(
        base_type="subagent",
        mixins=["code_writer", "git"],
    ),
    "(Lattice) Writer: Interface Implementer": AgentDef(
        base_type="subagent",
        mixins=["code_writer", "git"],
    ),
    "(Lattice) Writer: TDD": AgentDef(
        base_type="subagent",
        mixins=["test_writer", "git"],
    ),
    "(Lattice) Writer: Algorithm Porter": AgentDef(
        base_type="subagent",
        mixins=["code_writer", "git"],
    ),
}

UNMANAGED_AGENTS = {"summary", "title", "compaction", "explore"}


# =============================================================================
# COMPILER
# =============================================================================

def compile_agent(name, agent_def):
    """Compile an AgentDef into a flat permission dict.

    Order: GLOBAL_DEFAULTS -> BASE_TYPE -> MIXINS (in order) -> OVERRIDES
    """
    layers = []

    # 1. Global defaults (all agents)
    layers.append(GLOBAL_DEFAULTS)

    # 2. Base type (pure_agent or subagent)
    if agent_def.base_type == "pure_agent":
        layers.append(PURE_AGENT_BASE)
    elif agent_def.base_type == "subagent":
        layers.append(SUBAGENT_BASE)
    else:
        raise ValueError(f"Unknown base_type: {agent_def.base_type}")

    # 3. Mixins in order
    for mixin_name in agent_def.mixins:
        if mixin_name not in MIXIN_REGISTRY:
            raise ValueError(f"Unknown mixin: {mixin_name}")
        layers.append(MIXIN_REGISTRY[mixin_name]())

    # 4. Overrides last
    if agent_def.overrides:
        layers.append(agent_def.overrides)

    return deep_merge(*layers)


# =============================================================================
# CLI
# =============================================================================

def apply_agents():
    """Apply compiled permissions to agent config files."""
    # Update skeleton
    if os.path.exists(skeleton_path):
        with open(skeleton_path, "r") as f:
            skeleton_data = json.load(f)

        skeleton_data["permission"] = GLOBAL_DEFAULTS

        with open(skeleton_path, "w") as f:
            json.dump(skeleton_data, f, indent=2)
            f.write("\n")

        print("Applied global defaults to config_skeleton.json")
    else:
        print("Warning: config_skeleton.json not found; skipped global defaults update.")

    # Update agent files
    for directory in [agents_dir, subagents_dir]:
        if not os.path.exists(directory):
            continue

        for filename in os.listdir(directory):
            if not filename.endswith(".json"):
                continue

            agent_name = filename[:-5]
            if agent_name in AGENTS:
                filepath = os.path.join(directory, filename)
                compiled = compile_agent(agent_name, AGENTS[agent_name])

                with open(filepath, "r") as f:
                    data = json.load(f)

                data["permission"] = compiled

                with open(filepath, "w") as f:
                    json.dump(data, f, indent=2)

                mixins = ",".join(agent_def.mixins)
                print(f"Applied [{agent_def.base_type} | {mixins}] to '{agent_name}'")
            elif agent_name in UNMANAGED_AGENTS:
                pass
            else:
                print(f"Warning: '{agent_name}' has no AgentDef and is not in UNMANAGED_AGENTS.")


def dump_agent(name):
    """Print compiled permissions for a single agent."""
    if name not in AGENTS:
        print(f"Error: '{name}' not found. Available: {', '.join(sorted(AGENTS.keys()))}")
        sys.exit(1)
    compiled = compile_agent(name, AGENTS[name])
    print(json.dumps(compiled, indent=2, sort_keys=True))


def list_mixins():
    """Print available mixins."""
    print("Available mixins:")
    for name in sorted(MIXIN_REGISTRY.keys()):
        print(f"  {name}")


def list_agents():
    """Print agent -> (base_type, mixins) mapping."""
    print("Agent definitions:")
    for name in sorted(AGENTS.keys()):
        agent_def = AGENTS[name]
        mixins = ",".join(agent_def.mixins)
        print(f"  {name}: {agent_def.base_type} | {mixins}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage OpenCode agent permissions (v2).")
    parser.add_argument(
        "--apply", action="store_true",
        help="Apply compiled permissions to agent config files",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Compile and validate all agents without writing files",
    )
    parser.add_argument(
        "--dump", metavar="AGENT",
        help="Print compiled permissions for one agent",
    )
    parser.add_argument(
        "--list-mixins", action="store_true",
        help="Show available mixins",
    )
    parser.add_argument(
        "--list-agents", action="store_true",
        help="Show agent definitions",
    )
    args = parser.parse_args()

    if args.dump:
        dump_agent(args.dump)
    elif args.list_mixins:
        list_mixins()
    elif args.list_agents:
        list_agents()
    elif args.dry_run:
        print("All agents compile and validate successfully.")
        for name in sorted(AGENTS.keys()):
            agent_def = AGENTS[name]
            mixins = ",".join(agent_def.mixins)
            compiled = compile_agent(name, agent_def)
            print(f"  {name} [{agent_def.base_type} | {mixins}]: {len(compiled)} permission keys")
    elif args.apply:
        apply_agents()
        print("\nNow run scripts/build_config.py to compile these changes into opencode.json")
    else:
        print("Run with --apply to enforce permissions across agents.")
        print("  --dry-run      Compile and validate without writes")
        print("  --dump AGENT   Print one agent's compiled permissions")
        print("  --list-mixins  Show available mixins")
        print("  --list-agents  Show agent definitions")
        print(f"\nManaged agents: {len(AGENTS)}")
        print(f"Unmanaged agents: {', '.join(sorted(UNMANAGED_AGENTS))}")
