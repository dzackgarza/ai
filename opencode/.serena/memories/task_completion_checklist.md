# task completion checklist
- For permission changes: edit `manage_permissions.py`, validate against `PERMISSION_SPEC.md`, run `python3 manage_permissions.py --apply`, then `python3 build_config.py`, then review `git diff`.
- For provider/agent/subagent config changes: edit source files in `configs/`, run `python3 build_config.py`, and review generated diffs including `opencode.json`.
- For plugin changes: run `cd plugins && just check`; run targeted classifier/behavior tests when routing or message-shaping logic changes.
- For harness changes: run the relevant Bun command from `harness/` and verify CLI behavior.
- Avoid hand-editing generated outputs or scattering workflow docs away from the owning directory.