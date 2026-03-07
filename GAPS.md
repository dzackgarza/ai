# GAPS

Date: 2026-03-07
Scope: current plugin workspace and active OpenCode wiring

1. Human TUI verification still required for task observability Phase 1/2 behavior (live child-session visibility, parent tool metrics, async polling display updates).
2. `webfetch` domain handlers for Stack Exchange, `pypi.org`, `npmjs.com`, `crates.io`, and `huggingface.co` not yet implemented in `improved-webtools`.
3. No background cache pruning pass — cache expiry is lazy (on read only); stale entries accumulate indefinitely.
4. In-repo unit suites (`prompt-router`, `command-interceptor`, `callback-integration`) use synthetic inputs, not pinned real fixtures.
5. Several command/API assumptions in non-webtools plugins rely on mocks and inferred behavior rather than doc+live verification.
6. `improved-task` MCP server wrapper not yet implemented — planned in `MCP-WRAPPERS-PLAN.md` but never built. No MCP exposure for the task plugin yet.
