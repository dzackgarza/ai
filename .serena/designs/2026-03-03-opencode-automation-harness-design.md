# OpenCode Service + Automation Harness

## Problem

Current plugin and async testing relies on CLI paths (`opencode run`, transcript parsing hacks, attach behavior) that are brittle for autonomous workflows. We need a stable runtime and a dedicated automation harness that:

- works without `opencode run --attach --agent`;
- supports background continuation after idle;
- creates one-shot sessions and returns session IDs;
- can continue existing sessions, inspect outputs, and clean up sessions;
- supports plugin development/testing with minimal friction.

## Approach

Adopt a two-layer architecture:

1. **Stable runtime layer**: a user-level `systemd` service runs `opencode serve` on localhost with authentication.
2. **Automation harness layer**: a standalone SDK-driven CLI (TypeScript preferred) connects to that server and exposes high-level commands for session lifecycle and plugin testing.

This avoids the known `run --attach --agent` bug by never using that path in automation.

## Components

1. **systemd user service**
   - Unit file in `~/.config/systemd/user/opencode-serve.service`.
   - Runs `opencode serve --hostname 127.0.0.1 --port 4096`.
   - Uses env file for `OPENCODE_SERVER_PASSWORD` (and optional username).
   - Restart policy: `Restart=always`, bounded restart delay.
   - `systemctl --user enable --now opencode-serve`.

2. **Shell integration**
   - Add a safe alias in `~/.zshrc` for interactive use (if desired), but keep automation explicitly on SDK CLI.
   - Document that alias usage is for human interactive flows, not harness internals.

3. **Harness CLI (`opx`)**
   - Location: `opencode/harness/`.
   - Language: TypeScript using `@opencode-ai/sdk`.
   - Client mode: `createOpencodeClient({ baseUrl })` (connect to external server).
   - Commands:
     - `new` (create session; optional title/agent/model/prompt; return session ID)
     - `send` (send prompt to existing session with agent/model)
     - `tail` (show parsed transcript tail for a session)
     - `messages` (structured message dump)
     - `status` (session status map)
     - `list` (list sessions with title/updated)
     - `delete` (delete one/all by filter)
     - `wait` (block until idle/completion/event condition)
     - `abort` (abort running session)
     - `plugin-probe` (preset flows for async callback/background tool testing)

4. **Transcript adapter (in-house)**
   - Replace external parsing dependency with harness-native parser.
   - Input: `session.messages()` or `opencode export` fallback.
   - Output: concise transcript text with role markers and selected tool events.

5. **Plan/build orchestration support**
   - Keep `plan_exit` as session handoff message with ID/title for manual switch.
   - Future optional mode: automatic TUI switch via `tui.selectSession`.

## Trade-offs

- **Pros**
  - Removes fragile CLI attach path from automation.
  - Gives deterministic session lifecycle operations.
  - Better async testing and observability through SDK event/status APIs.
- **Cons**
  - Adds a long-running service dependency.
  - Requires auth/env management and service health checks.
  - Introduces a new local CLI to maintain.

## Tasks

1. **Service Foundation**
   - Create and install `systemd` user service + env file.
   - Add docs for start/stop/status/logs and restart policy.
   - Verify persistence across shell exits and reboots.

2. **Harness Scaffold**
   - Create `opencode/harness/` package structure.
   - Implement shared SDK client factory and config loader.
   - Implement command framework and JSON/plain output modes.

3. **Core Session Commands**
   - Implement `new`, `send`, `list`, `messages`, `status`, `delete`, `abort`.
   - Ensure all commands return stable machine-readable output including session IDs.

4. **Async/Background Validation Commands**
   - Implement `wait` and `plugin-probe` commands.
   - Add idle->callback->continued assertions for async tools and background subagents.

5. **Transcript Support**
   - Implement transcript tail rendering from SDK message data.
   - Add filters for tool calls/results and assistant-only views.

6. **Docs + Operator Playbook**
   - Document service lifecycle, harness usage, and known caveats.
   - Explicitly document the attach+agent bug and that harness bypasses it.

7. **Test Matrix Against Real `opencode serve`**
   - Smoke: service health + auth.
   - Session lifecycle: create/send/list/delete.
   - Async continuity: callback after idle causes new assistant action.
   - Plugin flows: async_command, async_subagent, plan_exit handoff.
   - Failure paths: bad model, permission deny, service restart mid-run.
