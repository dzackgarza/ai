from __future__ import annotations

"""mixins.py — Low-level permission rule builders and mixin functions.

These are the atomic building blocks. Combine them via presets.py.
"""
from src.models import (
    ALL_TOOLS,
    SERENA_FILE_READ_TOOLS,
    SERENA_FILE_WRITE_TOOLS,
)

# ---------------------------------------------------------------------------
# Core utilities
# ---------------------------------------------------------------------------


def deep_merge(*dicts: dict) -> dict:
    """Merge dicts left-to-right; nested dicts are merged at key level."""
    result: dict = {}
    for d in dicts:
        for key, value in d.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = {**result[key], **value}
            else:
                result[key] = value
    return result


def make_path_rule(allow_globs: list[str], deny_globs: list[str] | None = None) -> dict:
    """Build a path-scoped rule dict from allow/deny glob lists."""
    deny_globs = deny_globs or []
    if allow_globs == ["*"]:
        rule: dict = {"*": "allow"}
    elif allow_globs == []:
        rule = {"*": "deny"}
    else:
        rule = {"*": "deny"}
        for g in allow_globs:
            rule[g] = "allow"
    for g in deny_globs:
        rule[g] = "deny"
    return rule


def read_only_in(allow_globs: list[str], deny_globs: list[str] | None = None) -> dict:
    """Return read-tool permissions scoped to the given path globs."""
    rule = make_path_rule(allow_globs, deny_globs)
    return {tool: rule for tool in ["read", "glob", "grep", *SERENA_FILE_READ_TOOLS]}


def write_only_in(allow_globs: list[str], deny_globs: list[str] | None = None) -> dict:
    """Return write-tool permissions scoped to the given path globs."""
    rule = make_path_rule(allow_globs, deny_globs)
    perms: dict = {
        "edit": rule,
        "apply_patch": rule,
    }
    for tool in [
        *SERENA_FILE_WRITE_TOOLS,
        "cut-copy-paste-mcp_cut",
        "cut-copy-paste-mcp_copy",
        "cut-copy-paste-mcp_paste",
    ]:
        perms[tool] = rule
    return perms


# ---------------------------------------------------------------------------
# Atomic mixin functions
# ---------------------------------------------------------------------------


def mixin_interactive() -> dict:
    """Full file read/write access."""
    return deep_merge(read_only_in(["*"]), write_only_in(["*"]))


def mixin_planner() -> dict:
    """Read all, write plans only."""
    return deep_merge(
        read_only_in(["*"]),
        write_only_in(["*.serena/plans*"]),
    )


def mixin_orchestrator() -> dict:
    """Can dispatch tasks and manage todos."""
    return {"task": "allow", "todowrite": "allow"}


def mixin_code_writer() -> dict:
    """Read src+plans (not tests/docs), write src."""
    return deep_merge(
        read_only_in(
            ["*src*", "*.serena/plans*"], deny_globs=["*test*", "*tests*", "*docs*"]
        ),
        write_only_in(["*src*"]),
    )


def mixin_test_writer() -> dict:
    """Read tests+plans (not src/docs), write tests."""
    return deep_merge(
        read_only_in(
            ["*tests*", "*test*", "*.serena/plans*"], deny_globs=["*src*", "*docs*"]
        ),
        write_only_in(["*tests*", "*test*"]),
    )


def mixin_docs_writer() -> dict:
    """Read docs+plans (not src/tests), write docs."""
    return deep_merge(
        read_only_in(
            ["*docs*", "*.serena/plans*"], deny_globs=["*src*", "*test*", "*tests*"]
        ),
        write_only_in(["*docs*"]),
    )


def mixin_reviewer() -> dict:
    """Read all, write nothing."""
    return deep_merge(read_only_in(["*"]), write_only_in([]))


def mixin_researcher() -> dict:
    """Read all, write nothing."""
    return deep_merge(read_only_in(["*"]), write_only_in([]))


def mixin_bash_standard() -> dict:
    """Allow a curated set of safe bash commands."""
    return {
        "bash": {
            "*sudo*": "deny",
            "du*": "allow",
            "file *": "allow",
            "ls*": "allow",
            "pwd*": "allow",
            "stat*": "allow",
            "tree*": "allow",
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
            "find *": "allow",
            "find * -delete*": "ask",
            "find * -exec*": "ask",
            "just*": "allow",
            "pytest*": "allow",
            "uv*": "allow",
            "cat*": "deny",
            "*": "deny",
        }
    }


def mixin_bash_unrestricted() -> dict:
    """Allow all bash commands."""
    return {"bash": "allow"}


def mixin_session_tools() -> dict:
    """Allow introspection, session listing, transcript reading."""
    return {
        "introspection": "allow",
        "list_sessions": "allow",
        "read_transcript": "allow",
    }


def mixin_allow_all_permissions() -> dict:
    """Allow every known tool."""
    return {tool: "allow" for tool in ALL_TOOLS}
