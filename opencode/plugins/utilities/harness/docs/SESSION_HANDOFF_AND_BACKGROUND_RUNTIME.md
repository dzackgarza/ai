## Session Handoff and Background Runtime

### Current `plan_exit` behavior

- `plan_exit` creates a new orchestrator session and primes it with the Orchestrator agent prompt.
- It returns the orchestrator `Session ID` and `Title` so the user can switch sessions manually.
- This is intentional for now.

### Automatic session switch capability (documented, not enabled)

- OpenCode SDK supports TUI session switching programmatically.
- Relevant SDK endpoints/types:
  - `tui.selectSession({ sessionID })`
  - `tui.publish({ body: { type: "tui.session.select", properties: { sessionID } } })`
- This means a future `plan_exit` can auto-switch the active TUI session.

### Background continuation after idle: feasibility

- Verified with an SDK harness (no `opencode run`):
  - Create session via SDK.
  - Prompt agent to schedule `async_command` callback.
  - Keep process alive and poll messages.
  - Callback arrives and agent continues (`CALLBACK_CONTINUED` observed).
- Result: background continuation after idle is possible.

### Does this require `opencode serve`?

- Not strictly.
- Requirement is a live server instance while waiting for async callbacks.
- You have three valid runtime modes:
  1. `createOpencode()` in SDK (starts server + client in-process).
  2. Long-running `opencode serve` and connect via `createOpencodeClient(...)`.
  3. Running TUI session (server exists as long as TUI process is alive).

### SDK vs raw server API for harness

- Recommendation: use SDK as primary harness interface.
  - Type-safe session/message/TUI/event calls.
  - Fewer ad-hoc HTTP payload mistakes.
  - Easier event/subscription handling.
- Use raw server API only when debugging protocol-level behavior or integrating from non-JS runtimes.

### Service and harness artifacts

- User service unit path: `~/.config/systemd/user/opencode-serve.service`
- Service env file path: `~/.config/opencode/opencode-serve.env`
- Harness location: `opencode/plugins/utilities/harness`
- Harness command wrapper: `opencode/plugins/utilities/harness/opx`
- Validation results: `opencode/plugins/utilities/harness/docs/VALIDATION_REPORT.md`
