# Subagents

This directory no longer holds the active subagent definitions.

## Active Source Of Truth

- `ai-prompts`: canonical prompt library resolved by slug
- `../../agents/*.md`: generated OpenCode markdown agents
- `../../permissions/`: permission compiler and agent registry

## Historical Material

Legacy JSON subagent configs may still exist here for history or migration
reference. They are not the runtime source of truth.

## Update Flow

1. Edit the prompt in `ai-prompts`.
2. If the change affects permissions, update `../../permissions/`.
3. Run `uv run --python .venv/bin/python permissions/main.py --apply` from `opencode/`.
4. Run `uv run --python .venv/bin/python scripts/build_config.py`.
