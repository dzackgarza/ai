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

### Interactive mode: only when you need post-idle async behavior

`opencode run` exits the moment the session goes idle — any async work triggered *after* the idle event is cut off. This only matters if your plugin or tool does async work after the model finishes responding.

**When you need async work to complete** (e.g., a stop-hook that re-prompts the model, or an idle handler that fires an HTTP call):

```bash
# Run prompt with timeout, suppress TUI, parse transcript
mkdir -p /tmp/my-test && \
  (cd /tmp/my-test && timeout 90 sh -c 'echo "Your prompt" | opencode') >/dev/null 2>&1; \
  grep -o 'ses_[a-zA-Z0-9]*' /tmp/my-test/.opencode/events.jsonl | head -1 | \
    xargs -I{} python ~/.agents/skills/reading-transcripts/scripts/parse_transcript.py --harness opencode {}
```

**Important:** `echo "..." | opencode` starts a real interactive session that will **not** exit on its own — you **must** wrap it in `timeout <N>`. After the timeout kills the process, parse the transcript with the reading-transcripts skill.

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

When agents need to read past session transcripts (e.g., for recovery or context analysis), use this one-liner to parse the JSON export into clean, human-readable markdown (stripping out massive tool inputs/outputs and system metadata):

```bash
opencode export ses_YOUR_ID_HERE | sed '1d' | jq -r '.messages[]? | "[\(.info.role | ascii_upcase)]\n" + (if .parts then (.parts[] | select(.type=="text") | .text) else "" end) + "\n\n---\n"' > transcript.md
```

_(Add `| tail -n 150` instead of `> file` to quickly read recent messages)._

## Model Format

Always `provider/model` (e.g., `openai/gpt-5.2`, `anthropic/claude-sonnet-4-5`)

## Common Mistakes

| Tried                       | Error                        | Correct                                     |
| --------------------------- | ---------------------------- | ------------------------------------------- |
| `opencode "prompt"`         | "Failed to change directory" | `opencode run "prompt"`                     |
| `--model claude-3.5-sonnet` | "Provider not found"         | `-m openrouter/anthropic/claude-3.7-sonnet` |
| `opencode --prompt "..."`   | Launches TUI                 | `opencode run "..."`                        |

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
