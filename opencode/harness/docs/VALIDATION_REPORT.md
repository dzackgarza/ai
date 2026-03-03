# Validation Report

## Environment

- Harness path: `/home/dzack/ai/opencode/harness`
- SDK client mode: `createOpencodeClient(baseUrl)`
- Test model: `opencode/big-pickle`

## Results

### 1) Type safety

- Command: `bun run check`
- Result: pass

### 2) Smoke flow against live `opencode serve`

- Command sequence (port 4196):
  - `opencode serve --port 4196 ...`
  - `bun run opx health`
  - `bun run opx new --title opx-smoke-4196 ...`
  - `bun run opx wait --session <id> --timeout 30`
  - `bun run opx tail --session <id> --lines 40`
  - `bun run opx probe-async-command --model opencode/big-pickle --agent Minimal`
  - `bun run opx delete --session <id>`
- Result: pass
- Notable output:
  - Async probe returned `{ "ok": true, "sessionID": "ses_34aecd522ffei5aPhMTIKaCcUJ" }`

### 3) Async subagent probe

- Command sequence (port 4197):
  - `opencode serve --port 4197 ...`
  - `bun run opx probe-async-subagent --model opencode/big-pickle --agent Minimal`
- Result: pass
- Notable output:
  - Subagent probe returned `{ "ok": true, "sessionID": "ses_34aec8ee7ffeswONmuUK9LExy7" }`

### 4) User systemd service

- Unit file installed: `~/.config/systemd/user/opencode-serve.service`
- Env file installed: `~/.config/opencode/opencode-serve.env`
- Required shell env when missing:
  - `XDG_RUNTIME_DIR=/run/user/$(id -u)`
  - `DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus`
- Service status: active/running after fixing `ExecStart` to absolute binary path.

### 5) Sync vs async send behavior

- `send` in synchronous mode can time out for slower model/provider fallback paths.
- Harness supports `send --async` via `/session/:id/prompt_async` and `wait --contains ...` for robust background testing.
