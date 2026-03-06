# Subagents

This directory holds the active subagent definitions that feed the generated
OpenCode config.

## Active Source Of Truth

- `*.json`: live subagent definitions
- prompts remain external to these JSON files

## Historical Material

One-off subagent migration helpers are not kept in-tree. If you need prior
state, recover it from git history instead of reviving old scripts in the live
workspace.

## Update Flow

1. Edit the subagent JSON source here.
2. If the change affects permissions, update `scripts/manage_permissions.py`.
3. Run `just rebuild` from the repo root.
4. Verify the generated diff in `opencode.json`.
