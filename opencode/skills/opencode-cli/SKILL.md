---
name: opencode-cli
description: Use when running OpenCode CLI commands, starting repo-local OpenCode servers, inspecting models or agents, or driving sessions through ocm
---

# OpenCode CLI

> **Home:** https://opencode.ai/  
> **GitHub:** https://github.com/anomalyco/opencode  
> **Deepwiki:** https://deepwiki.com/anomalyco/opencode (use MCP2CLI tools, avoid direct fetching)  
> **Config:** https://opencode.ai/docs/config/  
> **CLI:** https://opencode.ai/docs/cli/  
> **SDK:** https://opencode.ai/docs/sdk/  
> **API:** https://opencode.ai/docs/server/

Basic OpenCode and `ocm` usage.

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

## Critical: User Service on This System

There is a **running user service** on this system. **DO NOT reset it without asking.**  
**DO NOT use it for testing.** Use a repo-local `opencode serve` instance instead.

## Global Config Model

The canonical OpenCode workspace is `~/ai/opencode`, **symlinked to `~/.config/opencode`**.

**DO NOT assume project-local `.opencode/` directories are the main config surface.** These are not picked up by the main `serve` instance and should be avoided. Use them only for deliberate per-repo overrides.

| Location                                     | Purpose                                     |
| -------------------------------------------- | ------------------------------------------- |
| `~/ai/opencode/opencode.json`                | Effective global config                     |
| `~/ai/opencode/configs/config_skeleton.json` | Source of truth for generated global config |
| `~/ai/opencode/plugins/`                     | Global plugins loaded across sessions       |
| `~/ai/opencode/skills/`                      | Shared OpenCode-facing skills               |

All agents are defined in `~/ai/opencode/opencode.json` with prompts in `~/ai/prompts/`.

Do not hand-edit `~/ai/opencode/opencode.json`. Rebuild it from `~/ai/opencode/configs/config_skeleton.json` with `just rebuild` from `~/ai/opencode/`.

## Core Rules

- Use `command opencode`, not a shell alias.
- Resolve the binary from PATH. Do not introduce `OPENCODE_BIN` or hardcoded local binary paths.
- Use `ocm` for multi-turn session orchestration, transcript rendering, and diagnostics.
- Transcript parsing goes through `ocm transcript --json` only. If that surface is
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

Run `command opencode --help` to see all subcommands.

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

Then point `ocm` at that server:

```bash
OPENCODE_BASE_URL=http://127.0.0.1:4198 \
  uvx git+https://github.com/dzackgarza/opencode-manager.git ocm begin-session "Your prompt" --agent Minimal
```

## Manager Commands

```bash
uvx git+https://github.com/dzackgarza/opencode-manager.git ocm one-shot "Your prompt"
uvx git+https://github.com/dzackgarza/opencode-manager.git ocm begin-session "Your prompt" --agent Minimal
uvx git+https://github.com/dzackgarza/opencode-manager.git ocm chat ses_123 "Follow-up prompt"
uvx git+https://github.com/dzackgarza/opencode-manager.git ocm chat ses_123 "System follow-up" --system
uvx git+https://github.com/dzackgarza/opencode-manager.git ocm transcript ses_123 --json
uvx git+https://github.com/dzackgarza/opencode-manager.git ocm final ses_123 "Wrap up"
uvx git+https://github.com/dzackgarza/opencode-manager.git ocm delete ses_123
uvx git+https://github.com/dzackgarza/opencode-manager.git ocm wait ses_123 --json
uvx git+https://github.com/dzackgarza/opencode-manager.git ocm doctor --json
```

**Command semantics:**

- Session IDs and prompts are **positional arguments** (not `--session`/`--prompt` flags).
- `chat` resumes the live agent turn by default. `chat --no-reply` queues only a user message without triggering a new assistant turn.
- `chat --system` records an agent-only system prompt in the transcript; it is carried in session state but is not shown as a user-visible prompt line.
- `chat --system --no-reply` queues an idle system message for the next continued turn to carry into the request.
- `debug trace` has no `ocm` equivalent — use `ocm transcript` for diagnostics.
- `one-shot` takes only a prompt; the agent is determined by server config.
- `begin-session` `--json` flag was removed; use `ocm transcript` separately to inspect session state.

**Avoid using the OpenCode CLI for real LLM work.** Use `ocm` via `uvx` for chatting, testing, and session orchestration.

## Web UI

`opencode web` runs a Web UI frontend that hooks into the `serve` backend. This is part of OpenCode, not an external library.

## Attached Server Notes

- `command opencode run --attach ...` talks to an existing server. It is not a proof
  harness.
- `--attach` plus `--agent` is a known broken combination upstream. If you need a
  specific non-default agent, prefer a non-attached one-shot run or drive the session
  through `ocm` against a repo-local server.

## Debugging Order

- If a run fails with provider or model errors, check `command opencode models` first.
- If the wrong tools or agents appear, check `command opencode agent list` and the active config surface.
- If repo-local behavior matters, verify which `OPENCODE_BASE_URL` and repo-local server you are talking to.
- If a command or flag is uncertain, check `command opencode --help` before guessing.
- If `ocm transcript --json` or another manager surface is wrong, file an issue rather
  than adding a transcript parsing fallback.
- If you need proof or audit rules, switch to `opencode-plugin-development`.
