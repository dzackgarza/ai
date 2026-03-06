# opencode overview
- Purpose: global OpenCode configuration workspace containing source-of-truth config fragments, permission compiler, config builder, plugins, and an automation harness.
- Main areas: `configs/` for providers/agents/subagents and config docs, `plugins/` for global Bun/TypeScript plugins plus tests/tiers/domain handlers, `harness/` for SDK-first session automation CLI, top-level Python scripts for config assembly, validation, migrations, and diagnostics.
- Generated artifact: `opencode.json` is built output, not source of truth.
- Key source-of-truth files: `manage_permissions.py`, `build_config.py`, `PERMISSION_SPEC.md`, `configs/providers/*.json`, `configs/agents/*.json`, `configs/subagents/*.json`, plugin source files under `plugins/`.
- Important rule: keep prompts external to JSON agent configs; do not inline prompts in configs.