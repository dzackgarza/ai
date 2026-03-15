---
name: opencode-cli
description: Use when running OpenCode CLI commands, starting repo-local OpenCode servers, inspecting models or agents, or driving sessions through opencode-manager
---

# OpenCode CLI

Basic OpenCode and `opencode-manager` usage.

For plugin-development policy, proof rules, and audit criteria, use `opencode-plugin-development`.

## Navigation

- Stay in this file for the global config model, basic CLI commands, repo-local server
  setup, and manager command forms.
- Read `PLUGINS.md` for plugin structure, event hooks, and plugin-specific debugging
  patterns.
- Read `async-injection.md` for background task and callback delivery patterns.
- Read `REFERENCE.md` for exhaustive command and schema reference.
- Switch to `opencode-plugin-development` when the task becomes plugin policy, witness
  design, or audit work.

## Global Config Model

The canonical OpenCode workspace is `~/ai/opencode`, symlinked to `~/.config/opencode`.

| Location | Purpose |
| --- | --- |
| `~/ai/opencode/opencode.json` | Effective global config |
| `~/ai/opencode/configs/config_skeleton.json` | Source of truth for generated global config |
| `~/ai/opencode/plugins/` | Global plugins loaded across sessions |
| `~/ai/opencode/skills/` | Shared OpenCode-facing skills |

All agents are defined in `~/ai/opencode/opencode.json` with prompts in `~/ai/prompts/`.

Do not assume a project-local `.opencode/` directory is the main config surface. Use it
only when you deliberately need a per-repo override.

In this workspace, do not hand-edit `~/ai/opencode/opencode.json`. Rebuild it from
`~/ai/opencode/configs/config_skeleton.json` with `just rebuild` from `~/ai/opencode/`.

## Core Rules

- Use `command opencode`, not a shell alias.
- Resolve the binary from PATH. Do not introduce `OPENCODE_BIN` or hardcoded local binary paths.
- Use `opencode-manager` for multi-turn session orchestration, transcript rendering, and debug traces.
- Transcript parsing goes through `opx transcript --json` only. If that surface is
  insufficient, file an issue instead of inventing a local fallback parser.
- If a workflow depends on repo-local config or env, start a repo-local `command opencode serve` inside that repo's `direnv`.
- `opencode` is not stale. Config is reread on each invocation, so do not blame cache or
  restart loops.

## Basic Inspection Commands

```bash
command opencode agent list
command opencode models
command opencode session list
```

Use these to inspect the currently visible agents, available models, and known sessions
before reasoning from failures.

## Simple One-Shot CLI Usage

```bash
command opencode run "Your prompt"
command opencode run -m provider/model "Your prompt"
command opencode run -s <session-id> "Follow-up prompt"
```

Use plain `opencode run` for ordinary CLI work, not for plugin proof workflows.

If a prompt that should be straightforward produces no output or provider/model errors,
check `command opencode models` first.

## Repo-Local Server Setup

```bash
cd /path/to/repo
direnv allow
direnv exec . command opencode serve --hostname 127.0.0.1 --port 4198
```

Then point `opencode-manager` at that server:

```bash
MANAGER="npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git"

OPENCODE_BASE_URL=http://127.0.0.1:4198 \
  $MANAGER opx begin-session "Your prompt" --agent Minimal --json
```

## Manager Commands

```bash
MANAGER="npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git"

$MANAGER opx one-shot --agent Minimal --prompt "Your prompt"
$MANAGER opx begin-session "Your prompt" --agent Minimal --json
$MANAGER opx chat --session ses_123 --prompt "Follow-up prompt"
$MANAGER opx system --session ses_123 --prompt "System follow-up"
$MANAGER opx transcript --session ses_123 --json
$MANAGER opx final --session ses_123 --prompt "Wrap up" --transcript
$MANAGER opx delete --session ses_123
$MANAGER opx debug trace --session ses_123 --verbose
```

## Attached Server Notes

- `command opencode run --attach ...` talks to an existing server. It is not a proof
  harness.
- `--attach` plus `--agent` is a known broken combination upstream. If you need a
  specific non-default agent, prefer a non-attached one-shot run or drive the session
  through `opencode-manager` against a repo-local server.

## Debugging Order

- If a run fails with provider or model errors, check `command opencode models` first.
- If the wrong tools or agents appear, check `command opencode agent list` and the active config surface.
- If repo-local behavior matters, verify which `OPENCODE_BASE_URL` and repo-local server you are talking to.
- If a command or flag is uncertain, check `command opencode --help` before guessing.
- If `opx transcript --json` or another manager surface is wrong, file an issue rather
  than adding a transcript parsing fallback.
- If you need proof or audit rules, switch to `opencode-plugin-development`.
