# OpenCode Automation Harness (`opx`)

SDK-first CLI for OpenCode session automation against a long-lived `opencode serve` instance.

## Why this exists

- Avoids fragile `opencode run --attach` automation paths.
- Keeps sessions alive independently of CLI idle/exit behavior.
- Provides a deterministic run→wait→transcript→cleanup cycle for testing.

## Prerequisites

1. Running `opencode serve` instance (recommended via user systemd service).
2. Bun installed (`~/.bun/bin/bun`).
3. Optional auth env vars when server password is enabled.

## Install and run

```bash
cd /home/dzack/ai/opencode/plugins/utilities/harness
bun install
bun run opx --help
```

## Environment

| Variable                   | Default                 | Description                         |
| -------------------------- | ----------------------- | ----------------------------------- |
| `OPENCODE_BASE_URL`        | `http://127.0.0.1:4096` | Server URL                          |
| `OPENCODE_SERVER_USERNAME` | `opencode`              | Basic auth username                 |
| `OPENCODE_SERVER_PASSWORD` | _(none)_                | Basic auth password                 |
| `OPX_TRANSCRIPT_SCRIPT`    | _(bundled path)_        | Path to transcript generator script |

## Commands

### Primary

```bash
# Run a one-shot prompt and print transcript when done
bun run opx run --prompt "Reply with ONLY: OK" --model github-copilot/claude-sonnet-4.6

# Resume an existing session with a new prompt
bun run opx resume --session ses_xxx --prompt "continue" --model github-copilot/claude-sonnet-4.6

# Options for run/resume:
#   --model provider/model       (default: server default)
#   --agent <name>               (default: server default)
#   --linger <sec>               wait N extra seconds after first idle (default: 0)
#   --keep                       keep session after transcript (default: delete)
#   --timeout <sec>              hard timeout (default: 180)
```

### Session management

```bash
bun run opx session delete --session ses_xxx
bun run opx session messages --session ses_xxx
```

Use `opencode session list` to browse all sessions on the server.

### Provider

```bash
bun run opx provider list
bun run opx provider health --provider github-copilot --model github-copilot/claude-sonnet-4.6
```

### Debug / probes

```bash
# Tail session events with service log interleaving
bun run opx debug trace --session ses_xxx --timeout 45

# Show error events for a session
bun run opx debug errors --session ses_xxx

# Show rate-limit error events matched against known patterns
bun run opx debug limit-errors --session ses_xxx

# Probe a model for rate limit behavior
bun run opx debug probe-limit --model opencode/minimax-m2.5-free --agent Minimal

# Probe a known-pattern provider (strict, deterministic)
bun run opx debug probe-limit-known --provider anthropic
bun run opx debug probe-limit-known --provider opencode-minimax
bun run opx debug probe-limit-known --provider opencode-big-pickle

# Full limit trace with event stream
bun run opx debug probe-limit-trace --model opencode/minimax-m2.5-free --agent Minimal --timeout 45

# Plugin probes
bun run opx debug probe-async-command --model github-copilot/claude-sonnet-4.6
bun run opx debug probe-async-subagent --model github-copilot/claude-sonnet-4.6
```

## Exit codes

| Code | Meaning                                   |
| ---- | ----------------------------------------- |
| `0`  | Success                                   |
| `1`  | Failure (error or timeout)                |
| `2`  | Provider unavailable (rate limit / quota) |

## Known-pattern mode

`probe-limit-known` is strict and deterministic: it matches error messages against
`config/known_limit_patterns.json`. If provider phrasing changes, the command fails
with `KNOWN_PATTERN_NOT_FOUND` — update the JSON file to fix it.
