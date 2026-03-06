# GAPS

Date: 2026-03-06  
Scope: current plugin workspace and active OpenCode wiring

## Remaining Gaps

1. Human TUI verification is still required for task observability Phase 1/2 behavior (live child-session visibility, parent tool metrics, async polling display updates).

## Validation Status (Completed)

1. `improved-task` is now wired in global plugin config (`file:///home/dzack/opencode-plugins/improved-task/src/index.ts`).
2. Local `task-plugin` toggle is now disabled in `plugins.json` to match local source state (`task.ts` removed).
3. Hermetic shadow harness is green with local project config and explicit plugin loading:
   - `just shadow-test-websearch` passed.
   - `just shadow-test-webfetch` passed.
4. Harness assertions are now strict on final output line (`passphrase-only` check).
5. Deterministic unit tests now cover previously open non-TUI gaps:
   - `tests/unit/searxng-search.test.ts` validates batched `search_query[]` handling with per-query separation/pagination.
   - `tests/unit/searxng-search.test.ts` validates `webfetch` overflow behavior (save-to-`/tmp` when token count exceeds inline threshold).
   - `tests/unit/searxng-search.test.ts` asserts `context.ask` invocation for both `websearch` and `webfetch`.
   - `tests/unit/callback-integration.test.ts` validates consolidated callback semantics across `task` (async terminal callback), `sleep`, and `async_command`.
