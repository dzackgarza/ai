#!/usr/bin/env python3
import json
import os
import argparse

base_dir = os.path.expanduser("~/.config/opencode")

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
If you use custom MCP tools to modify files (e.g., `morph-mcp_edit_file`), they 
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
        "serena_create_text_file",
        "serena_replace_content",
        "serena_replace_symbol_body",
        "serena_insert_after_symbol",
        "serena_insert_before_symbol",
        "serena_rename_symbol",
        "serena_delete_lines",
        "serena_insert_at_line",
        "serena_replace_lines",
        "morph-mcp_edit_file",
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
        "serena_read_file",
        "serena_list_dir",
        "serena_find_file",
        "serena_search_for_pattern",
        "serena_get_symbols_overview",
        "serena_find_symbol",
        "serena_find_referencing_symbols",
        "morph-mcp_warpgrep_codebase_search",
    ]
    for tool in read_tools:
        perms[tool] = rule
    return perms


def merge_perms(*perm_dicts):
    result = {}
    for pd in perm_dicts:
        result.update(pd)
    return result


DENY_TASKS = {"task": "deny"}

ALLOW_STANDARD_CORE = {
    "serena_activate_project": "allow",
    "serena_check_onboarding_performed": "allow",
    "serena_initial_instructions": "allow",
    "serena_read_memory": "allow",
    "serena_list_memories": "allow",
    "serena_get_current_config": "allow",
    "serena_think_about_collected_information": "allow",
    "serena_think_about_task_adherence": "allow",
    "serena_think_about_whether_you_are_done": "allow",
    "serena_execute_shell_command": "deny",
    "serena_*": "deny",
}

ALLOW_STANDARD_BASH = {
    "bash": {
        "cut*": "allow",
        "diff*": "allow",
        "du*": "allow",
        "file *": "allow",
        "find * -delete*": "ask",
        "find * -exec*": "ask",
        "find *": "allow",
        "git status*": "allow",
        "git diff*": "allow",
        "git log*": "allow",
        "git show*": "allow",
        "git branch*": "allow",
        "grep*": "allow",
        "rg*": "allow",
        "head*": "allow",
        "tail*": "allow",
        "less*": "allow",
        "ls*": "allow",
        "pwd*": "allow",
        "sort*": "allow",
        "stat*": "allow",
        "tree*": "allow",
        "wc*": "allow",
        "jq": "allow",
        "just*": "allow",
        "pytest*": "allow",
        "uv*": "allow",
        "cat*": "deny",
        "*": "deny",
    }
}

RESTRICTIVE_BASH = {
    "bash": {
        "*": "deny",
        "just": "allow",
        "just *": "allow",
        "pytest*": "allow",
        "git add *": "allow",
        "git status": "allow",
        "git diff": "allow",
        "git diff --stat": "allow",
        "git commit -m *": "allow",
        "git commit --amend *": "allow",
        "ls*": "allow",
        "tree*": "allow",
        "find * -type f -maxdepth 3*": "allow",
        "find * -type d -maxdepth 3*": "allow",
        "wc*": "allow",
        "head*": "allow",
        "tail*": "allow",
        "cat*": "allow",
        "grep*": "allow",
        "rg*": "allow",
        "kpsewhich*": "allow",
        "command -v *": "allow",
        "uv*": "allow",
    }
}

PROFILES = {
    "builder": merge_perms(
        read_only_in(["*"], deny_globs=["*tests/*", "*test/*", "*tests*", "*test*"]),
        write_only_in([]),
        {
            "task": "allow",
            "todoread": "allow",
            "todowrite": "allow",
            "webfetch": "deny",
            "websearch": "deny",
        },
        {"bash": {"*": "ask"}},
        ALLOW_STANDARD_CORE,
    ),
    "planning": merge_perms(
        read_only_in(["*"]),
        write_only_in(["*.serena/plans*"]),
        ALLOW_STANDARD_CORE,
        ALLOW_STANDARD_BASH,
    ),
    "src_writer": merge_perms(
        read_only_in(["*src*"]),
        write_only_in(["*src*"]),
        DENY_TASKS,
        ALLOW_STANDARD_CORE,
        RESTRICTIVE_BASH,
        {
            "serena_onboarding": "allow",
            "serena_prepare_for_new_conversation": "allow",
            "serena_write_memory": "allow",
            "serena_edit_memory": "allow",
            "serena_delete_memory": "allow",
        },
    ),
    "test_writer": merge_perms(
        read_only_in(["*tests*", "*test*"]),
        write_only_in(["*tests*", "*test*"]),
        DENY_TASKS,
        ALLOW_STANDARD_CORE,
        RESTRICTIVE_BASH,
        {
            "serena_onboarding": "allow",
            "serena_prepare_for_new_conversation": "allow",
            "serena_write_memory": "allow",
            "serena_edit_memory": "allow",
            "serena_delete_memory": "allow",
        },
    ),
    "readonly": merge_perms(
        read_only_in(["*"]),
        write_only_in([]),
        DENY_TASKS,
        ALLOW_STANDARD_CORE,
        ALLOW_STANDARD_BASH,
    ),
    "minimal": {
        "bash": "allow",
        "external_directory": {"/tmp/opencode_test/*": "allow"},
    },
}

AGENT_MAPPING = {
    # Primary Agents
    "Minimal": "minimal",
    "Plan": "planning",
    "Build": "builder",
    "Interactive": "minimal",
    "Ralph Planner": "planning",
    "Repository Steward": "planning",
    "(Lattice) Build": "builder",
    "Zotero Librarian": "readonly",
    
    # Subagents - Writers
    "Writer: General Code": "src_writer",
    "Writer: Python": "src_writer",
    "Writer: TypeScript": "src_writer",
    "Writer: SageMath": "src_writer",
    "Writer: Tests": "test_writer",
    "Writer: Documentation": "src_writer",
    "Writer: Refactorer": "src_writer",
    
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
    
    # Subagents - Lattice
    "(Lattice) Researcher: Documentation": "readonly",
    "(Lattice) Reviewer: Documentation Librarian": "readonly",
    "(Lattice) Reviewer: Checklist Completionist": "readonly",
    "(Lattice) Reviewer: Test Coverage": "readonly",
    "(Lattice) Writer: Test Methods": "test_writer",
    "(Lattice) Writer: Interface Designer": "src_writer",
    "(Lattice) Writer: Interface Implementer": "src_writer",
    "(Lattice) Writer: TDD": "test_writer",
    "(Lattice) Writer: Algorithm Porter": "src_writer"
}

def apply_profiles():
    agents_dir = os.path.join(base_dir, "configs", "agents")
    subagents_dir = os.path.join(base_dir, "configs", "subagents")

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
