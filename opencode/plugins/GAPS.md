# GAPS

Date: 2026-03-06  
Scope: current plugin workspace and active OpenCode wiring

## Remaining Gaps

1. Human TUI verification is still required for task observability Phase 1/2 behavior (live child-session visibility, parent tool metrics, async polling display updates).
2. `websearch` batch mode (`search_query[]`) still needs an explicit behavioral test that confirms per-query separation and pagination behavior in one run.
3. `webfetch` overflow path (write full content to `/tmp` when >20k tokens) still needs a deterministic test fixture.
4. Permission-path behavior (`context.ask`) for both shadowed tools is still unasserted in the harness.
5. Cross-plugin callback interaction (`task`, `sleep`, `async-command`) still lacks one consolidated end-to-end verification run.

## Open Questions

1. Should passphrase instrumentation remain always-on in tool output, or be gated behind a dedicated test flag?
2. For resumable task sessions, should the plugin enforce subagent/model consistency or remain permissive as currently implemented?

## Validation Status (Completed)

1. `improved-task` is now wired in global plugin config (`file:///home/dzack/opencode-plugins/improved-task/src/index.ts`).
2. Local `task-plugin` toggle is now disabled in `plugins.json` to match local source state (`task.ts` removed).
3. Hermetic shadow harness is green with local project config and explicit plugin loading:
   - `just shadow-test-websearch` passed.
   - `just shadow-test-webfetch` passed.
4. Harness assertions are now strict on final output line (`passphrase-only` check).
