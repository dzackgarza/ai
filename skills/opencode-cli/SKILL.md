---
name: opencode-cli
description: Use when running OpenCode CLI commands, selecting models, managing sessions, or configuring MCP servers
---

# OpenCode CLI

Terminal-based AI coding assistant for non-interactive tasks.

## Global Config Directory (ALWAYS use this)

The global OpenCode config lives at `~/ai/opencode`, which is symlinked to `~/.config/opencode`.

**All configuration, plugins, and skills go here — not in a local `.opencode/` directory.**

| Location                      | Purpose                                                         |
| ----------------------------- | --------------------------------------------------------------- |
| `~/ai/opencode/opencode.json` | Global config (models, MCP, permissions, etc.)                  |
| `~/ai/opencode/plugins/`      | Global plugins (always loaded, regardless of working directory) |
| `~/ai/opencode/skills/`       | Global agent skills                                             |

**Never create a local `.opencode/` directory** unless you have a specific, deliberate reason to override global config for a single project. Almost every use case belongs in the global config.

The reason: plugins, config, and skills in `~/ai/opencode/` are active in every OpenCode session. A local `.opencode/` only applies to sessions run from that project directory, which is almost never what you want.

## Agents

All agents are defined in `~/ai/opencode/opencode.json` with prompts loaded from text files in `~/ai/prompts/`. Primary agents (e.g., "Repository Steward", "Minimal", "Interactive") and subagents (e.g., "code-reviewer", "Refactorer", "Repo Explorer") are version-controlled there. Agent definitions include the prompt file path, permissions, and default model.

## Quick Start

```bash
# Simple one-shot run (plugins active, exits on idle)
opencode run --thinking --print-logs "Your prompt"
```

**Common flags:**

- `--thinking` - Enable reasoning output
- `--print-logs` - Show logs for debugging
- `--attach http://localhost:4096` - Attach to a running `opencode serve` instance (skips MCP warmup only — no other behavioral difference)

**`opencode serve` is purely a warmup cache.** Starting a background server with `opencode serve &` and using `--attach` makes subsequent `opencode run` calls faster by avoiding MCP server restarts. It has no effect on session persistence, plugin behavior, or async lifecycle. The first run is slow (MCP warmup ~10s); subsequent attached runs skip that.

## Known Bug: `run --attach` + `--agent`

Issue: https://github.com/anomalyco/opencode/issues/8094

### Symptom

```bash
opencode run --attach http://127.0.0.1:4096 --agent plan "test"
# instance: No context found for instance
```

### Notes

- Reported as a bug in OpenCode (`#8094`), with related fixes discussed upstream.
- `--attach` is still useful and typically works.
- The problematic case is selecting a specific non-default agent with `--agent` while attached.

### Workarounds

```bash
# 1) Fast path: use --attach and rely on server/default agent
opencode run --attach http://localhost:4096 --thinking --print-logs "Your prompt"

# 2) If you need a specific non-default agent, run without --attach
opencode run --agent <agent> --thinking --print-logs "Your prompt"
```

## One-Shot Testing

### Simple case: just use `opencode run`

**Default for all one-shot tests.** Plugins are active, output goes to stdout, session completes and exits cleanly. No parsing, no timeouts, no events.jsonl.

```bash
opencode run "Your prompt here"
```

No output = model/connectivity issue (99% of cases). Check your model config or API key.

### Multi-turn and async workflows: use `opencode-manager`

Do **not** use rendered CLI/TUI output as your workflow harness or evidence source.
For multi-turn, async, resume, or post-idle behavior, orchestrate the real session
through `opencode-manager` and inspect the resulting session data or transcript.

```bash
MANAGER="npx --yes --package=git+ssh://git@github.com/dzackgarza/opencode-manager.git"
TRANSCRIPT="uvx --from git+ssh://git@github.com/dzackgarza/opencode-transcripts.git opencode-transcript"

# Create or target a session, then prompt without blocking
$MANAGER opx-session create --title "test"
$MANAGER opx-session prompt ses_abc123 "Your prompt" --no-reply

# Inspect the real session instead of scraping the TUI
$MANAGER opx-session messages ses_abc123 --json
$MANAGER opx debug trace --session ses_abc123 --verbose
$TRANSCRIPT ses_abc123
```

The `echo` / `printf` stdin trick is only a compatibility escape hatch for starting a
real interactive session. If you must use it, discard the TUI output and inspect the
session afterward through `opencode-manager`, `opencode-transcripts`, `opencode export`,
or raw session data.

MCP warmup is at most ~10s and is never the bottleneck. If a session times out or produces unexpected results, the cause is almost always model connectivity, rate limits, or model behavior — not MCP.

## Core Commands

| Command                            | Purpose                   |
| ---------------------------------- | ------------------------- |
| `opencode run "prompt"`            | Non-interactive task      |
| `opencode run -c "prompt"`         | Continue last session     |
| `opencode run -s <id> "prompt"`    | Continue specific session |
| `opencode run -m <model> "prompt"` | Use specific model        |
| `opencode run -f file "prompt"`    | Attach file               |
| `opencode models`                  | List available models     |
| `opencode session list`            | List sessions             |
| `opencode stats`                   | Token usage statistics    |
| `opencode auth login`              | Configure API keys        |
| `opencode mcp list`                | List MCP servers          |

### Exporting Readable Transcripts

When agents need readable session transcripts, use the dedicated transcript package:

```bash
uvx --from git+ssh://git@github.com/dzackgarza/opencode-transcripts.git opencode-transcript ses_YOUR_ID_HERE
```

Fallback only when you explicitly need raw JSON post-processing:

```bash
opencode export ses_YOUR_ID_HERE | sed '1d' | jq -r '.messages[]? | "[\(.info.role | ascii_upcase)]\n" + (if .parts then (.parts[] | select(.type=="text") | .text) else "" end) + "\n\n---\n"' > transcript.md
```

## Model Format

Always `provider/model` (e.g., `openai/gpt-5.2`, `anthropic/claude-sonnet-4-5`)

## Common Mistakes

| Tried                       | Error                        | Correct                                     |
| --------------------------- | ---------------------------- | ------------------------------------------- |
| `opencode "prompt"`         | "Failed to change directory" | `opencode run "prompt"`                     |
| `--model claude-3.5-sonnet` | "Provider not found"         | `-m openrouter/anthropic/claude-3.7-sonnet` |
| `opencode --prompt "..."`   | Launches TUI                 | `opencode run "..."`                        |

## Operational Notes

- **Use `command opencode`, not `opencode`** — the bare alias auto-attaches to a server, which interferes with investigations and fresh testing.
- **Opencode is never stale.** Config files are read fresh on every invocation. No cache to clear, no process to restart, nothing to recompile. If something isn't working, the cause is never "stale state."
- **Test a fresh instance in <10s:** `command opencode run --agent Minimal 'Hello world'`
- **The `~/ai` repo is canonical.** All config lives under `~/ai/opencode/`, symlinked to system locations. Edit here only — never in project-local `.opencode/` directories unless deliberately overriding.
- **You do not know opencode internals.** It evolves rapidly. Do not claim or assume functionality or configuration behavior without reading current docs first.

## Red Flags - STOP and Check Help

If you're about to:

- Query databases or guess file paths directly
- Use flags or subcommands you haven't verified

**STOP** and run `opencode --help` first.

## Free Models (Verified Feb 2026)

| Model                               | Provider     | Notes                        |
| ----------------------------------- | ------------ | ---------------------------- |
| `opencode/big-pickle`               | OpenCode Zen | General reasoning            |
| `opencode/glm-5-free`               | OpenCode Zen | General tasks                |
| `google/antigravity-gemini-3-flash` | Antigravity  | Fast, capable                |
| `openai/gpt-5.2-codex`              | OpenAI Codex | Frontier coding (via plugin) |

**Avoid:** OpenRouter free models often have "No endpoints" - test before relying.

## Plugins

For creating and using OpenCode plugins with concrete examples:

→ See [PLUGINS.md](./PLUGINS.md)

Contains:

- Plugin locations (local + npm)
- Basic plugin structure
- All events reference (session, tool, file, shell, TUI, etc.)
- 7 copy-pasteable examples (notifications, env protection, custom tools, etc.)
- TypeScript support
- External dependencies

## Full Reference

For comprehensive documentation including all commands, flags, tools, agents, configuration, permissions, MCP servers, skills, environment variables, and providers:

→ See [REFERENCE.md](./REFERENCE.md)

Contains:

- All CLI commands with complete flag tables
- 15 built-in tools with parameters
- 7 built-in agents (primary + subagents)
- Full configuration schema
- Permissions system with granular examples
- MCP servers (local/remote/OAuth)
- Skills system
- 40+ environment variables
- Provider/model configuration
- File structure (project + global)
