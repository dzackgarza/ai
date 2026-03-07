#!/usr/bin/env python3
"""manage_permissions.py -- Tag-based composable permission system for OpenCode agents.

Architecture:
    TAG_RULES (ordered layers)    ->  applied by tag membership
  + CAPABILITIES (composable)     ->  small named functions returning perm dicts
  + OVERRIDES (per-agent)         ->  explicit exceptions
  + NON_OVERRIDABLE_DENIES        ->  safety floor, always last
  = compiled permission dict
"""
import json
import os
import sys
import argparse
from dataclasses import dataclass, field

base_dir = os.path.expanduser("~/.config/opencode")
skeleton_path = os.path.join(base_dir, "configs", "config_skeleton.json")
#
# IMPORTANT:
# Keep this file aligned with docs/PERMISSION_SPEC.md in this repository.
# Use the spec as the authority for role boundaries, inheritance layers,
# recursion controls, and path-isolation rules.

"""
===============================================================================
OPENCODE PERMISSIONS: THE DEFINITIVE GUIDE
===============================================================================

1. THE "EDIT" UMBRELLA (The biggest gotcha)
-------------------------------------------------------------------------------
The `edit` permission is NOT just a single tool. It is a MACRO that governs ALL
built-in file modifications (specifically `edit`, `write`, `patch`, and `apply_patch`).

COMMON MISTAKE:
Writing `"write": {"*": "deny"}` or `"default_api:write": {"*": "deny"}`.
Result: OpenCode completely ignores it. The write tool will still succeed!
Fix: You MUST use `"edit"` to control writing, editing, and patching files.

2. MCP TOOLS CROSS-EVALUATION
-------------------------------------------------------------------------------
If you use custom MCP tools to modify files, they
require their own explicit permission blocks in the config.

COMMON MISTAKE:
Allowing the MCP tool, but setting `"edit": {"*": "deny"}` globally.
Result: The MCP tool is BLOCKED. OpenCode's engine evaluates the global `edit`
restriction against the file path first, before checking the MCP tool's rule.
Fix: The allow/deny path patterns for `edit` and ALL file-modifying MCP tools
MUST be perfectly synchronized to avoid contradictory evaluations.

3. GLOBBING RULES (picomatch/minimatch quirks)
-------------------------------------------------------------------------------
OpenCode evaluates permissions against the ABSOLUTE file path
(e.g., `/home/dzack/ai/src/file.ts`).

- `*` matches ANYTHING, including slashes `/`.
- `**` is NOT supported as a recursive globstar (it is treated as literal `*`).
- Relative paths (e.g., `src/*`) DO NOT MATCH because the path starts with `/`.
- Rules are evaluated sequentially: the LAST matching rule overrides previous ones.

COMMON MISTAKE:
Using `"**/.serena/plans/**/*.md"`.
Result: Fails to match because `**` is invalid syntax for this primitive globber.

COMMON MISTAKE:
Using `"src/*"`.
Result: Fails to match because it doesn't account for `/home/dzack/ai/`.

Fix: Use a trailing and leading asterisk to absorb the absolute path prefix
and any nested subdirectories.
Correct: `"*src*"`, `"*.serena/plans*"`, or `"*tests*"`

===============================================================================
ABSTRACTIONS: read_only_in and write_only_in
===============================================================================
These abstraction functions automatically generate synchronized tool blocks
and enforce path isolation properly via OpenCode's last-rule-wins engine.
"""

# ---------------------------------------------------------------------------
# KNOWN TOOL INVENTORY (KEEP UPDATED WITH TOOLING CHANGES)
# ---------------------------------------------------------------------------
# This is the canonical human-maintained inventory used while authoring
# permission profiles. Groupings are intentionally separated by source.
#
# 1) OpenCode internals (permission keys used directly in profiles)
#    - read, glob, grep, list
#    - edit, patch, apply_patch
#    - bash
#    - webfetch, websearch
#    - todoread, todowrite
#    - question
#    - external_directory
#
# 2) Local custom plugins in this repo (plugins/*.ts)
#    - task
#    - plan_exit
#    - async_subagent
#    - async_command
#    - list_sessions
#    - introspection
#    - write_plan
#    - read_transcript
#    - sleep, sleep_until
#    - git_add, git_commit
#
# 3) MCP-provided tools (split by configured server / naming prefix)
#    - serena:
#      serena_activate_project, serena_check_onboarding_performed,
#      serena_initial_instructions, serena_read_memory,
#      serena_list_memories, serena_get_current_config,
#      serena_execute_shell_command,
#      serena_read_file, serena_list_dir, serena_find_file,
#      serena_search_for_pattern, serena_get_symbols_overview,
#      serena_find_symbol, serena_find_referencing_symbols,
#      serena_create_text_file, serena_replace_content,
#      serena_replace_symbol_body, serena_insert_after_symbol,
#      serena_insert_before_symbol, serena_rename_symbol,
#      serena_delete_lines, serena_insert_at_line, serena_replace_lines,
#      serena_onboarding, serena_prepare_for_new_conversation,
#      serena_write_memory, serena_edit_memory, serena_delete_memory,
#      serena_rename_memory
#    - cut-copy-paste-mcp:
#      cut-copy-paste-mcp_cut, cut-copy-paste-mcp_copy,
#      cut-copy-paste-mcp_paste
#    - context7 (configured MCP server; add to permission map when used):
#      context7_resolve-library-id, context7_query-docs
#    - tavily-remote (configured MCP server; tool names are server-defined,
#      not currently pinned as explicit permission keys in this file)
#
# IMPORTANT: Every Serena tool listed below must be explicitly routed as one of:
#   1) path-scoped read tool
#   2) path-scoped write tool
#   3) global allow/deny non-file tool
# See validate_serena_routing() for guardrails.
# ---------------------------------------------------------------------------

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

# These are process scaffolding tools we intentionally disable:
# - onboarding/initialization should be handled by repo skills and harness policy
# - think* prompts are better expressed as explicit skills/checklists because
#   most agents do not invoke them reliably as tools.
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
SERENA_DOCUMENTED_TOOLS = set(
    SERENA_FILE_READ_TOOLS
    + SERENA_FILE_WRITE_TOOLS
    + SERENA_MEMORY_TOOLS
    + SERENA_SESSION_META_TOOLS
    + SERENA_DISABLED_WORKFLOW_TOOLS
    + SERENA_DENY_TOOLS
)


# ---------------------------------------------------------------------------
# Path Rule Builders
# ---------------------------------------------------------------------------

def make_path_rule(allow_globs, deny_globs=None):
    deny_globs = deny_globs or []
    rule = {}

    # Baseline
    if allow_globs == ["*"]:
        rule["*"] = "allow"
    elif allow_globs == []:
        rule["*"] = "deny"
    else:
        rule["*"] = "deny"
        for g in allow_globs:
            rule[g] = "allow"

    # Explicit Denies
    for g in deny_globs:
        rule[g] = "deny"

    return rule


def write_only_in(allow_globs, deny_globs=None):
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


def read_only_in(allow_globs, deny_globs=None):
    rule = make_path_rule(allow_globs, deny_globs)
    perms = {}
    read_tools = [
        "read",
        "glob",
        "grep",
        "list",
        *SERENA_FILE_READ_TOOLS,
    ]
    for tool in read_tools:
        perms[tool] = rule
    return perms


# ---------------------------------------------------------------------------
# Merge
# ---------------------------------------------------------------------------

def deep_merge(*dicts):
    """Merge dicts: nested sub-dicts are merged at the key level, flat values overwrite."""
    result = {}
    for d in dicts:
        for key, value in d.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = {**result[key], **value}
            else:
                result[key] = value
    return result


# ---------------------------------------------------------------------------
# Core Permission Constants
# ---------------------------------------------------------------------------

ALLOW_STANDARD_CORE = {
    **{tool: "allow" for tool in SERENA_SESSION_META_TOOLS},
    **{tool: "allow" for tool in SERENA_MEMORY_TOOLS},
    "serena_*": "deny",
}

NON_OVERRIDABLE_DENIES = {
    # Serena shell bypasses command safety controls; never permit it.
    **{tool: "deny" for tool in SERENA_DENY_TOOLS},
}


def validate_serena_routing():
    globally_allowed = {
        key
        for key, value in ALLOW_STANDARD_CORE.items()
        if key.startswith("serena_") and key != "serena_*" and value == "allow"
    }
    globally_denied = set(NON_OVERRIDABLE_DENIES.keys())
    path_read = set(SERENA_FILE_READ_TOOLS)
    path_write = set(SERENA_FILE_WRITE_TOOLS)

    overlap = sorted(path_read & path_write)
    if overlap:
        raise ValueError(f"Serena tools cannot be both read and write routed: {overlap}")

    covered = globally_allowed | globally_denied | path_read | path_write
    missing = sorted(SERENA_DOCUMENTED_TOOLS - covered)
    extra = sorted(covered - SERENA_DOCUMENTED_TOOLS)
    if missing or extra:
        raise ValueError(
            f"Serena routing mismatch. missing={missing}, unexpected={extra}"
        )


validate_serena_routing()


# ---------------------------------------------------------------------------
# Bash Command Capabilities
# ---------------------------------------------------------------------------

def make_bash_rules(*command_blocks, default="deny", default_first=False):
    """Build a `{"bash": {...}}` permission block from reusable command fragments."""
    rules = {}
    if default_first:
        rules["*"] = default
    for block in command_blocks:
        rules.update(block)
    if not default_first:
        rules["*"] = default
    return {"bash": rules}


# Independent command capabilities (single source of truth)
BASH_CAP_FILESYSTEM_METADATA = {
    "du*": "allow",
    "file *": "allow",
    "ls*": "allow",
    "pwd*": "allow",
    "stat*": "allow",
    "tree*": "allow",
}

BASH_CAP_TEXT_INSPECTION = {
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
}

BASH_CAP_FIND_DISCOVERY = {"find *": "allow"}

BASH_CAP_FIND_WITH_GUARDRAILS = {
    "find * -delete*": "ask",
    "find * -exec*": "ask",
    **BASH_CAP_FIND_DISCOVERY,
}

BASH_CAP_SHALLOW_FIND = {
    "find * -type f -maxdepth 3*": "allow",
    "find * -type d -maxdepth 3*": "allow",
}

BASH_CAP_FILE_CONTENT_READ = {"cat*": "allow"}
BASH_CAP_BINARY_DISCOVERY = {"command -v *": "allow"}

BASH_CAP_TEST_RUNNERS = {
    "just*": "allow",
    "pytest*": "allow",
    "uv*": "allow",
}

ALLOW_STANDARD_BASH = make_bash_rules(
    BASH_CAP_FILESYSTEM_METADATA,
    BASH_CAP_TEXT_INSPECTION,
    BASH_CAP_FIND_WITH_GUARDRAILS,
    BASH_CAP_TEST_RUNNERS,
    {"cat*": "deny"},
)


# ---------------------------------------------------------------------------
# Agent Definition
# ---------------------------------------------------------------------------

@dataclass
class AgentDef:
    """Defines an agent's permissions via tags, capabilities, and overrides.

    tags:           Set of category labels (e.g. {"primary", "builder"}).
                    TAG_RULES matching these tags are applied in order.
    caps:           List of permission dicts (from capability functions).
                    Applied after TAG_RULES.
    overrides:      Per-agent exceptions applied after caps.
    skip_tag_rules: If True, TAG_RULES are not applied (for unconstrained agents).
    """
    tags: set[str]
    caps: list[dict]
    overrides: dict = field(default_factory=dict)
    skip_tag_rules: bool = False


# ---------------------------------------------------------------------------
# Capability Functions
# ---------------------------------------------------------------------------

def read_all():
    """Allow reading all files."""
    return read_only_in(["*"])


def read_in(*globs, deny=None):
    """Allow reading files matching globs, deny others."""
    return read_only_in(list(globs), deny_globs=deny or [])


def write_all():
    """Allow writing all files."""
    return write_only_in(["*"])


def write_in(*globs):
    """Allow writing files matching globs, deny others."""
    return write_only_in(list(globs))


def write_none():
    """Deny all file writes."""
    return write_only_in([])


def src_read_write():
    """Read src + plans (deny test/docs), write src."""
    return deep_merge(
        read_in("*src*", "*.serena/plans*", deny=["*test*", "*tests*", "*docs*"]),
        write_in("*src*"),
    )


def test_read_write():
    """Read tests + plans (deny src/docs), write tests."""
    return deep_merge(
        read_in("*tests*", "*test*", "*.serena/plans*", deny=["*src*", "*docs*"]),
        write_in("*tests*", "*test*"),
    )


def docs_read_write():
    """Read docs + plans (deny src/tests), write docs."""
    return deep_merge(
        read_in("*docs*", "*.serena/plans*", deny=["*src*", "*test*", "*tests*"]),
        write_in("*docs*"),
    )


def allow_git():
    """Allow git staging and commit tools."""
    return {"git_add": "allow", "git_commit": "allow"}


def allow_planning():
    """Allow plan writing and plan-mode exit."""
    return {"write_plan": "allow", "plan_exit": "allow"}


def deny_plan_exit():
    """Deny plan-mode exit."""
    return {"plan_exit": "deny"}


def allow_bash_standard():
    """Allow standard bash commands (filesystem, text, find, test runners)."""
    return ALLOW_STANDARD_BASH


def allow_bash_unrestricted():
    """Allow all bash commands."""
    return {"bash": "allow"}


def allow_coordination():
    """Allow task dispatch, todo read/write."""
    return {"task": "allow", "todoread": "allow", "todowrite": "allow"}


def allow_session_tools():
    """Allow introspection, session listing, transcript reading."""
    return {"introspection": "allow", "list_sessions": "allow", "read_transcript": "allow"}


def allow_external_directory(*paths):
    """Allow access to external directories."""
    return {"external_directory": {p: "allow" for p in paths}}


# ---------------------------------------------------------------------------
# Tag Rules -- applied in order to agents matching each tag
# ---------------------------------------------------------------------------
# Adding a universal deny: add to ("*", {...})
# Adding a category rule: add a new (tag, {...}) entry

TAG_RULES = [
    ("primary", {
        "todoread": "allow",
        "todowrite": "allow",
    }),
    ("subagent", {
        "task": "deny",
        "todoread": "deny",
        "todowrite": "deny",
        "plan_exit": "deny",
        "introspection": "deny",
        "list_sessions": "deny",
        "read_transcript": "deny",
        "async_command": "deny",
        "async_subagent": "deny",
    }),
]


# ---------------------------------------------------------------------------
# Global Permission (applied to config_skeleton.json)
# ---------------------------------------------------------------------------

BASELINE_PLUGIN_DENIES = {
    "async_command": "deny",
    "async_subagent": "deny",
    "introspection": "deny",
    "list_sessions": "deny",
    "read_transcript": "deny",
    "git_add": "deny",
    "git_commit": "deny",
    "write_plan": "deny",
}

GLOBAL_PERMISSION = deep_merge(
    ALLOW_STANDARD_CORE,
    {"question": "allow"},
    {"bash": "deny"},
    BASELINE_PLUGIN_DENIES,
    NON_OVERRIDABLE_DENIES,
)


# ---------------------------------------------------------------------------
# Agent Registry
# ---------------------------------------------------------------------------

AGENTS = {
    # --- Primary Agents ---
    "Interactive": AgentDef(
        tags={"primary", "interactive"},
        caps=[allow_coordination(), allow_session_tools(), read_all(),
              write_in("*src*", "*docs*", "*tests*", "*test*", "*.serena/plans*"),
              deny_plan_exit(), allow_bash_unrestricted()],
    ),
    "Plan (Custom)": AgentDef(
        tags={"primary", "planner"},
        caps=[read_all(), write_in("*.serena/plans*"),
              {"task": "allow", "write_plan": "allow"}, {"plan_exit": "allow"}],
    ),
    "plan": AgentDef(
        tags={"primary", "planner"},
        caps=[read_all(), write_in("*.serena/plans*"),
              {"task": "allow", "write_plan": "allow"}, {"plan_exit": "allow"}],
    ),
    "Ralph Planner": AgentDef(
        tags={"primary", "planner"},
        caps=[read_all(), write_in("*.serena/plans*"),
              {"task": "allow", "write_plan": "allow"}, {"plan_exit": "allow"}],
    ),
    "Repository Steward": AgentDef(
        tags={"primary", "planner"},
        caps=[read_all(), write_in("*.serena/plans*"),
              {"task": "allow", "write_plan": "allow"}, {"plan_exit": "allow"}],
    ),
    "Build (Custom)": AgentDef(
        tags={"primary", "builder"},
        caps=[read_all(), write_all(), {"task": "allow"}, allow_git(), deny_plan_exit()],
        overrides={"webfetch": "deny", "websearch": "deny", "write_plan": "deny"},
    ),
    "build": AgentDef(
        tags={"primary", "builder"},
        caps=[read_all(), write_all(), {"task": "allow"}, allow_git(), deny_plan_exit()],
        overrides={"webfetch": "deny", "websearch": "deny", "write_plan": "deny"},
    ),
    "(Lattice) Build": AgentDef(
        tags={"primary", "builder", "lattice"},
        caps=[read_all(), write_all(), {"task": "allow"}, allow_git(), deny_plan_exit()],
        overrides={"webfetch": "deny", "websearch": "deny", "write_plan": "deny"},
    ),
    "Zotero Librarian": AgentDef(
        tags={"primary"},
        caps=[allow_coordination(), allow_session_tools(), read_all(), write_none()],
    ),
    "Minimal": AgentDef(
        tags={"primary", "minimal"},
        caps=[allow_bash_unrestricted(), allow_coordination(), deny_plan_exit(),
              allow_external_directory("/tmp/opencode_test/*"),
              {"question": "allow"}],
        skip_tag_rules=True,
    ),
    # --- Subagents: Writers ---
    "Writer: General Code": AgentDef(
        tags={"subagent", "writer", "src_scope"},
        caps=[src_read_write(), allow_git()],
    ),
    "Writer: Python": AgentDef(
        tags={"subagent", "writer", "src_scope"},
        caps=[src_read_write(), allow_git()],
    ),
    "Writer: TypeScript": AgentDef(
        tags={"subagent", "writer", "src_scope"},
        caps=[src_read_write(), allow_git()],
    ),
    "Writer: SageMath": AgentDef(
        tags={"subagent", "writer", "src_scope"},
        caps=[src_read_write(), allow_git()],
    ),
    "Writer: Refactorer": AgentDef(
        tags={"subagent", "writer", "src_scope"},
        caps=[src_read_write(), allow_git()],
    ),
    "Writer: Tests": AgentDef(
        tags={"subagent", "writer", "test_scope"},
        caps=[test_read_write(), allow_git()],
    ),
    "Writer: Documentation": AgentDef(
        tags={"subagent", "writer", "docs_scope"},
        caps=[docs_read_write(), allow_git()],
    ),
    # --- Subagents: Reviewers ---
    "Reviewer: Code": AgentDef(
        tags={"subagent", "reviewer"},
        caps=[read_all(), write_none()],
    ),
    "Reviewer: Plans": AgentDef(
        tags={"subagent", "reviewer"},
        caps=[read_all(), write_none()],
    ),
    "Reviewer: Test Compliance": AgentDef(
        tags={"subagent", "reviewer"},
        caps=[read_all(), write_none()],
    ),
    "Reviewer: Semantic Audit": AgentDef(
        tags={"subagent", "reviewer"},
        caps=[read_all(), write_none()],
    ),
    "Reviewer: Plan Contract": AgentDef(
        tags={"subagent", "reviewer"},
        caps=[read_all(), write_none()],
    ),
    # --- Subagents: Researchers ---
    "Researcher: Code Base": AgentDef(
        tags={"subagent", "researcher"},
        caps=[read_all(), write_none()],
    ),
    "Researcher: Documentation": AgentDef(
        tags={"subagent", "researcher"},
        caps=[read_all(), write_none()],
    ),
    "Researcher: Repo Explorer": AgentDef(
        tags={"subagent", "researcher"},
        caps=[read_all(), write_none()],
    ),
    "general": AgentDef(
        tags={"subagent", "researcher"},
        caps=[read_all(), write_none()],
    ),
    # --- Subagents: Lattice ---
    "(Lattice) Researcher: Documentation": AgentDef(
        tags={"subagent", "researcher", "lattice"},
        caps=[read_all(), write_none()],
    ),
    "(Lattice) Reviewer: Documentation Librarian": AgentDef(
        tags={"subagent", "reviewer", "lattice"},
        caps=[read_all(), write_none()],
    ),
    "(Lattice) Reviewer: Checklist Completionist": AgentDef(
        tags={"subagent", "reviewer", "lattice"},
        caps=[read_all(), write_none()],
    ),
    "(Lattice) Reviewer: Test Coverage": AgentDef(
        tags={"subagent", "reviewer", "lattice"},
        caps=[read_all(), write_none()],
    ),
    "(Lattice) Writer: Test Methods": AgentDef(
        tags={"subagent", "writer", "test_scope", "lattice"},
        caps=[test_read_write(), allow_git()],
    ),
    "(Lattice) Writer: Interface Designer": AgentDef(
        tags={"subagent", "writer", "src_scope", "lattice"},
        caps=[src_read_write(), allow_git()],
    ),
    "(Lattice) Writer: Interface Implementer": AgentDef(
        tags={"subagent", "writer", "src_scope", "lattice"},
        caps=[src_read_write(), allow_git()],
    ),
    "(Lattice) Writer: TDD": AgentDef(
        tags={"subagent", "writer", "test_scope", "lattice"},
        caps=[test_read_write(), allow_git()],
    ),
    "(Lattice) Writer: Algorithm Porter": AgentDef(
        tags={"subagent", "writer", "src_scope", "lattice"},
        caps=[src_read_write(), allow_git()],
    ),
}

UNMANAGED_AGENTS = {"summary", "title", "compaction", "explore"}


# ---------------------------------------------------------------------------
# Compiler
# ---------------------------------------------------------------------------

def compile_agent(name, agent_def):
    """Compile an AgentDef into a flat permission dict.

    Order: TAG_RULES -> capabilities -> overrides -> NON_OVERRIDABLE_DENIES
    """
    layers = []

    # 1. Apply matching TAG_RULES (unless skip_tag_rules)
    if not agent_def.skip_tag_rules:
        for tag, rules in TAG_RULES:
            if tag == "*" or tag in agent_def.tags:
                layers.append(rules)

    # 2. Apply capabilities
    layers.extend(agent_def.caps)

    # 3. Apply overrides
    if agent_def.overrides:
        layers.append(agent_def.overrides)

    # 4. NON_OVERRIDABLE_DENIES always last
    layers.append(NON_OVERRIDABLE_DENIES)

    return deep_merge(*layers)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_agent_serena_path_routing():
    """Verify all non-minimal agents have Serena file tools properly path-scoped."""
    required = set(SERENA_FILE_READ_TOOLS + SERENA_FILE_WRITE_TOOLS)
    for name, agent_def in AGENTS.items():
        if agent_def.skip_tag_rules:
            continue
        compiled = compile_agent(name, agent_def)
        missing = sorted(required - set(compiled.keys()))
        if missing:
            raise ValueError(
                f"Agent '{name}' missing Serena path routing for: {missing}"
            )


validate_agent_serena_path_routing()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def apply_agents():
    agents_dir = os.path.join(base_dir, "configs", "agents")
    subagents_dir = os.path.join(base_dir, "configs", "subagents")

    if os.path.exists(skeleton_path):
        with open(skeleton_path, "r") as f:
            skeleton_data = json.load(f)

        skeleton_data["permission"] = GLOBAL_PERMISSION

        with open(skeleton_path, "w") as f:
            json.dump(skeleton_data, f, indent=2)
            f.write("\n")

        print("Applied global permission baseline to config_skeleton.json")
    else:
        print("Warning: config_skeleton.json not found; skipped global permission update.")

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

                tags = ",".join(sorted(AGENTS[agent_name].tags))
                print(f"Applied [{tags}] to '{agent_name}'")
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


def list_tags():
    """Print tag -> agents mapping."""
    tag_map = {}
    for name, agent_def in AGENTS.items():
        for tag in agent_def.tags:
            tag_map.setdefault(tag, []).append(name)
    for tag in sorted(tag_map.keys()):
        print(f"\n{tag}:")
        for name in sorted(tag_map[tag]):
            print(f"  {name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage OpenCode agent permissions.")
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
        "--list-tags", action="store_true",
        help="Show tag -> agents mapping",
    )
    args = parser.parse_args()

    if args.dump:
        dump_agent(args.dump)
    elif args.list_tags:
        list_tags()
    elif args.dry_run:
        print("All agents compile and validate successfully.")
        for name in sorted(AGENTS.keys()):
            tags = ",".join(sorted(AGENTS[name].tags))
            compiled = compile_agent(name, AGENTS[name])
            print(f"  {name} [{tags}]: {len(compiled)} permission keys")
    elif args.apply:
        apply_agents()
        print("\nNow run scripts/build_config.py to compile these changes into opencode.json")
    else:
        print("Run with --apply to enforce permissions across agents.")
        print("  --dry-run     Compile and validate without writes")
        print("  --dump AGENT  Print one agent's compiled permissions")
        print("  --list-tags   Show tag -> agents mapping")
        print(f"\nManaged agents: {len(AGENTS)}")
        print(f"Unmanaged agents: {', '.join(sorted(UNMANAGED_AGENTS))}")
