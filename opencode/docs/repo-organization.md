# Repo Organization

This workspace is both a git repo subtree and the live OpenCode config
directory. Cleanup should preserve runtime-discovered paths while reducing root
sprawl.

## Keep At Root

- `AGENTS.md`
- `justfile`
- `opencode.json`
- `configs/`
- `docs/`
- `scripts/`
- `plugins/`

## Move Near The Owning Subtree

- Global documentation belongs in `docs/`
- Provider maintenance scripts belong in `configs/providers/scripts/`
- Provider operational notes belong in `configs/providers/notes/`
- Provider-specific shims belong in `configs/providers/shims/`
- Config-adjacent plugin support files like the safety-net config belong in `configs/`
- Plugin toggle state belongs in `configs/local-plugins.json`
- Global maintenance helpers belong in `scripts/`
- Plugin-owned utilities belong under `plugins/utilities/`
- Harness-specific operational notes belong in `plugins/utilities/harness/docs/`
- One-off migrations, probes, logs, and scratch artifacts belong in git history, not the live tree

## Practical Rule

When adding support for a new provider, model, subagent, skill, or MCP:

1. Put the source-of-truth config next to its peers.
2. Add one maintained recipe for the canonical pathway.
3. Keep any helper script adjacent to the subtree it serves.
4. Delete superseded experiments once the pathway is codified.
