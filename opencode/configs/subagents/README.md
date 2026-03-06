# Subagents

This directory holds the active subagent definitions that feed the generated
OpenCode config.

## Active Source Of Truth

- `*.json`: live subagent definitions
- prompts remain external to these JSON files

## Historical Material

- `archive/migrations/`: one-off rename and merge scripts kept for reference

Those migration helpers are not canonical workflows. Do not revive them unless
you are deliberately reconstructing prior state.

## Update Flow

1. Edit the subagent JSON source here.
2. If the change affects permissions, update `manage_permissions.py`.
3. Run `just rebuild` from the repo root.
4. Verify the generated diff in `opencode.json`.
