# Repo Organization

This workspace is both a git repo subtree and the live OpenCode config
directory. Cleanup should preserve runtime-discovered paths while reducing root
sprawl.

## Keep At Root

- `README.md`
- `build_config.py`
- `manage_permissions.py`
- `PERMISSION_SPEC.md`
- `opencode.json`
- `plugins.json`
- `rate-limit-fallback.json`
- `configs/`
- `plugins/`
- `harness/`
- `scripts/`

## Move Near The Owning Subtree

- Provider maintenance scripts belong in `configs/providers/scripts/`
- Provider operational notes belong in `configs/providers/notes/`
- Provider-specific shims belong in `configs/providers/shims/`
- Config-adjacent plugin support files like the safety-net config belong in `configs/`
- Historical subagent migration helpers belong in `configs/subagents/archive/migrations/`
- Neutral maintenance helpers belong in `scripts/maintenance/`
- Harness-specific operational notes belong in `harness/docs/`

## Archive

- One-off probes superseded by canonical recipes
- Runtime artifacts like transcripts and logs
- Binaries or scratch files not required by the live config

## Practical Rule

When adding support for a new provider, model, subagent, skill, or MCP:

1. Put the source-of-truth config next to its peers.
2. Add one maintained recipe for the canonical pathway.
3. Keep any helper script adjacent to the subtree it serves.
4. Archive the experiment once the pathway is codified.
