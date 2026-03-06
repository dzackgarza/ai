# style and conventions
- Treat `opencode.json` as a generated build artifact.
- Do not manually edit permission blocks in `configs/agents/*.json` or `configs/subagents/*.json`; regenerate them from `manage_permissions.py --apply`.
- Permission logic is capability-first and layered; `PERMISSION_SPEC.md` is the policy authority.
- Prefer reusable profile/capability composition over per-agent one-offs.
- Keep prompt text external and referenced from config JSON files.
- In plugins, every behavior-changing plugin should have a killswitch/default-off gating pattern.
- Plugin docs emphasize proof-of-delivery tests for model-visible injections before behavior tests.
- Plugin domain-specific webfetch logic belongs in `plugins/webfetch-handlers/domains/`; `index.ts` is the registry surface.