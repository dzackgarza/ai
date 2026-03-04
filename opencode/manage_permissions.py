#!/usr/bin/env python3
import json
import os
import argparse

base_dir = os.path.expanduser("~/.config/opencode")
skeleton_path = os.path.join(base_dir, "configs", "config_skeleton.json")
#
# IMPORTANT:
# Keep this file aligned with PERMISSION_SPEC.md in this repository.
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


def merge_perms(*perm_dicts):
    result = {}
    for pd in perm_dicts:
        result.update(pd)
    return result


ALLOW_PURE_AGENT_COORDINATION_TOOLS = {
    "task": "allow",
    "todoread": "allow",
    "todowrite": "allow",
}
DENY_SUBAGENT_COORDINATION_TOOLS = {
    "task": "deny",
    "todoread": "deny",
    "todowrite": "deny",
}
DENY_PLAN_EXIT = {"plan_exit": "deny"}
ALLOW_PLAN_EXIT = {"plan_exit": "allow"}
ALLOW_QUESTION = {"question": "allow"}

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

ALLOW_PURE_AGENT_SESSION_TOOLS = {
    "introspection": "allow",
    "list_sessions": "allow",
    "read_transcript": "allow",
}

DENY_SUBAGENT_SESSION_TOOLS = {
    "introspection": "deny",
    "list_sessions": "deny",
    "read_transcript": "deny",
}

DENY_SUBAGENT_ASYNC_TOOLS = {
    "async_command": "deny",
    "async_subagent": "deny",
}

ALLOW_GIT_MUTATION_TOOLS = {
    "git_add": "allow",
    "git_commit": "allow",
}

# Layered baselines (see PERMISSION_SPEC.md section 6.A)
ALL_AGENTS_BASELINE = merge_perms(
    ALLOW_STANDARD_CORE,
    ALLOW_QUESTION,
    {"bash": "deny"},
    BASELINE_PLUGIN_DENIES,
)
PURE_AGENTS_BASELINE = merge_perms(
    ALLOW_PURE_AGENT_COORDINATION_TOOLS,
    ALLOW_PURE_AGENT_SESSION_TOOLS,
)
SUBAGENTS_BASELINE = merge_perms(
    PURE_AGENTS_BASELINE,
    DENY_SUBAGENT_COORDINATION_TOOLS,
    DENY_PLAN_EXIT,
    DENY_SUBAGENT_SESSION_TOOLS,
    DENY_SUBAGENT_ASYNC_TOOLS,
)
TOP_LEVEL_AGENTS_BASELINE = {"todoread": "allow", "todowrite": "allow"}


def enforce_non_overridable_denies(perms):
    return merge_perms(perms, NON_OVERRIDABLE_DENIES)


GLOBAL_PERMISSION = enforce_non_overridable_denies(ALL_AGENTS_BASELINE)

def make_bash_rules(*command_blocks, default="deny", default_first=False):
    """
    Build a `{"bash": {...}}` permission block from reusable command fragments.
    """
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

PROFILES = {
    # NOTE: Profile composition here should remain consistent with
    # PERMISSION_SPEC.md (especially baseline layering and role intent).
    "builder": merge_perms(
        TOP_LEVEL_AGENTS_BASELINE,
        read_only_in(["*"]),
        write_only_in(["*"]),
        {
            "task": "allow",
            "webfetch": "deny",
            "websearch": "deny",
            "write_plan": "deny",
        },
        DENY_PLAN_EXIT,
        ALLOW_GIT_MUTATION_TOOLS,
    ),
    "planning": merge_perms(
        TOP_LEVEL_AGENTS_BASELINE,
        read_only_in(["*"]),
        write_only_in(["*.serena/plans*"]),
        {"task": "allow", "write_plan": "allow"},
        ALLOW_PLAN_EXIT,
    ),
    "interactive_general": merge_perms(
        TOP_LEVEL_AGENTS_BASELINE,
        PURE_AGENTS_BASELINE,
        read_only_in(["*"]),
        write_only_in(["*src*", "*docs*", "*tests*", "*test*", "*.serena/plans*"]),
        DENY_PLAN_EXIT,
        ALLOW_STANDARD_BASH,
    ),
    "src_writer_strict": merge_perms(
        SUBAGENTS_BASELINE,
        read_only_in(
            ["*src*", "*.serena/plans*"],
            deny_globs=["*test*", "*tests*", "*docs*"],
        ),
        write_only_in(["*src*"]),
        ALLOW_GIT_MUTATION_TOOLS,
    ),
    "test_writer_strict": merge_perms(
        SUBAGENTS_BASELINE,
        read_only_in(
            ["*tests*", "*test*", "*.serena/plans*"],
            deny_globs=["*src*", "*docs*"],
        ),
        write_only_in(["*tests*", "*test*"]),
        ALLOW_GIT_MUTATION_TOOLS,
    ),
    "docs_writer_strict": merge_perms(
        SUBAGENTS_BASELINE,
        read_only_in(
            ["*docs*", "*.serena/plans*"],
            deny_globs=["*src*", "*test*", "*tests*"],
        ),
        write_only_in(["*docs*"]),
        ALLOW_GIT_MUTATION_TOOLS,
    ),
    "pure_readonly": merge_perms(
        PURE_AGENTS_BASELINE,
        read_only_in(["*"]),
        write_only_in([]),
    ),
    "readonly": merge_perms(
        SUBAGENTS_BASELINE,
        read_only_in(["*"]),
        write_only_in([]),
    ),
    "minimal": {
        "bash": "allow",
        "task": "allow",
        "todoread": "allow",
        "todowrite": "allow",
        "plan_exit": "deny",
        "external_directory": {"/tmp/opencode_test/*": "allow"},
        "question": "allow",
    },
}

# Apply non-overridable safety denies to every role profile so accidental
# role-level allow rules cannot re-enable restricted tools.
PROFILES = {
    profile_name: enforce_non_overridable_denies(profile_perms)
    for profile_name, profile_perms in PROFILES.items()
}


def validate_profile_serena_path_routing():
    # minimal is intentionally unconstrained for explicit user-driven bypass tests.
    exempt_profiles = {"minimal"}
    required = set(SERENA_FILE_READ_TOOLS + SERENA_FILE_WRITE_TOOLS)
    for profile_name, profile_perms in PROFILES.items():
        if profile_name in exempt_profiles:
            continue
        missing = sorted(required - set(profile_perms.keys()))
        if missing:
            raise ValueError(
                f"Profile '{profile_name}' missing Serena path routing for: {missing}"
            )


validate_profile_serena_path_routing()

AGENT_MAPPING = {
    # Primary Agents
    "Minimal": "minimal",
    "Plan (Custom)": "planning",
    "plan": "planning",
    "Build (Custom)": "builder",
    "build": "builder",
    "Interactive": "interactive_general",
    "Ralph Planner": "planning",
    "Repository Steward": "planning",
    "(Lattice) Build": "builder",
    "Zotero Librarian": "pure_readonly",
    # Subagents - Writers
    "Writer: General Code": "src_writer_strict",
    "Writer: Python": "src_writer_strict",
    "Writer: TypeScript": "src_writer_strict",
    "Writer: SageMath": "src_writer_strict",
    "Writer: Tests": "test_writer_strict",
    "Writer: Documentation": "docs_writer_strict",
    "Writer: Refactorer": "src_writer_strict",
    # Subagents - Reviewers
    "Reviewer: Code": "readonly",
    "Reviewer: Plans": "readonly",
    "Reviewer: Test Compliance": "readonly",
    "Reviewer: Semantic Audit": "readonly",
    "Reviewer: Plan Contract": "readonly",
    # Subagents - Researchers
    "Researcher: Code Base": "readonly",
    "Researcher: Documentation": "readonly",
    "Researcher: Repo Explorer": "readonly",
    "general": "readonly",
    # Subagents - Lattice
    "(Lattice) Researcher: Documentation": "readonly",
    "(Lattice) Reviewer: Documentation Librarian": "readonly",
    "(Lattice) Reviewer: Checklist Completionist": "readonly",
    "(Lattice) Reviewer: Test Coverage": "readonly",
    "(Lattice) Writer: Test Methods": "test_writer_strict",
    "(Lattice) Writer: Interface Designer": "src_writer_strict",
    "(Lattice) Writer: Interface Implementer": "src_writer_strict",
    "(Lattice) Writer: TDD": "test_writer_strict",
    "(Lattice) Writer: Algorithm Porter": "src_writer_strict",
}


def apply_profiles():
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
            if agent_name in AGENT_MAPPING:
                filepath = os.path.join(directory, filename)
                profile_name = AGENT_MAPPING[agent_name]
                profile_perms = PROFILES[profile_name]

                with open(filepath, "r") as f:
                    data = json.load(f)

                data["permission"] = profile_perms

                with open(filepath, "w") as f:
                    json.dump(data, f, indent=2)

                print(f"Applied '{profile_name}' profile to '{agent_name}'")
            else:
                print(f"Warning: '{agent_name}' has no profile mapped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage OpenCode agent permissions.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply permission profiles to agent config files",
    )
    args = parser.parse_args()

    if args.apply:
        apply_profiles()
        print("\nNow run build_config.py to compile these changes into opencode.json")
    else:
        print("Run with --apply to enforce profiles across agents.")
        print("Available profiles:", list(PROFILES.keys()))
