# OpenCode Automation Harness (`opx`)

SDK-first CLI for OpenCode session automation and plugin testing against a long-lived `opencode serve` instance.

## Why this exists

- Avoids fragile `opencode run --attach --agent ...` automation paths.
- Keeps sessions alive independently of CLI idle/exit behavior.
- Provides direct commands for session create/send/wait/tail/delete.

## Prerequisites

1. Running `opencode serve` instance (recommended via user systemd service).
2. Bun installed.
3. Optional auth env vars when server auth is enabled.

## Install and run

```bash
cd /home/dzack/ai/opencode/harness
bun install
bun run opx --help
```

## Environment

- `OPENCODE_BASE_URL` default: `http://127.0.0.1:4096`
- `OPENCODE_SERVER_USERNAME` default: `opencode`
- `OPENCODE_SERVER_PASSWORD` optional

## Commands

```bash
bun run opx health
bun run opx list
bun run opx new --title test --prompt "hello" --agent Minimal --model opencode/big-pickle
bun run opx send --session ses_xxx --prompt "continue" --agent Minimal --model opencode/big-pickle
bun run opx tail --session ses_xxx --lines 60
bun run opx limit-errors --session ses_xxx
bun run opx trace --session ses_xxx --timeout 45
bun run opx wait --session ses_xxx --contains CALLBACK_CONTINUED --timeout 120
bun run opx delete --session ses_xxx
```

Plugin probes:

```bash
bun run opx probe-async-command --model opencode/big-pickle --agent Minimal
bun run opx probe-async-subagent --model opencode/big-pickle --agent Minimal
bun run opx probe-limit --model opencode/minimax-m2.5-free --agent Minimal
bun run opx probe-limit-known --provider opencode-minimax
bun run opx probe-limit-known --provider opencode-big-pickle
bun run opx probe-limit-known --provider anthropic
bun run opx probe-limit-trace --model opencode/minimax-m2.5-free --agent Minimal --timeout 45

# SDK-native limit trace (no opencode run log scraping)
bun run opx probe-limit-trace --model opencode/minimax-m2.5-free --agent Minimal --timeout 45

# Strict known-pattern limit checks (authoritative for known cases)
bun run opx probe-limit-known --provider anthropic

Known-pattern mode is strict and deterministic: if provider phrasing changes,
the command fails with `KNOWN_PATTERN_NOT_FOUND` and you must update
`config/known_limit_patterns.json`.
```

## Notes

- `plan_exit` currently returns build session ID/title for manual switching.
- TUI auto-switch is technically available via SDK TUI APIs, but not enabled in this workflow.
- For automation, prefer SDK/API calls with explicit `agent` and `model`.
