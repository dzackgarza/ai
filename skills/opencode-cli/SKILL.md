---
name: opencode-cli
description: Use when running OpenCode CLI commands, selecting models, managing sessions, or configuring MCP servers
---

# OpenCode CLI

Terminal-based AI coding assistant for non-interactive tasks.

## Quick Start

```bash
# Start background server (once per session)
opencode serve &

# Run tasks (fast after MCP warmup)
opencode run --attach http://localhost:4096 --thinking --print-logs "Your prompt"
```

**Required flags for agent calls:**
- `--attach http://localhost:4096` - Connect to background server
- `--thinking` - Enable reasoning output  
- `--print-logs` - Show logs for debugging

**First run is slow** (MCP warmup). Subsequent runs are fast.

## Core Commands

| Command | Purpose |
|---------|---------|
| `opencode run "prompt"` | Non-interactive task |
| `opencode run -c "prompt"` | Continue last session |
| `opencode run -s <id> "prompt"` | Continue specific session |
| `opencode run -m <model> "prompt"` | Use specific model |
| `opencode run -f file "prompt"` | Attach file |
| `opencode models` | List available models |
| `opencode session list` | List sessions |
| `opencode stats` | Token usage statistics |
| `opencode auth login` | Configure API keys |
| `opencode mcp list` | List MCP servers |

## Model Format

Always `provider/model` (e.g., `openai/gpt-5.2`, `anthropic/claude-sonnet-4-5`)

## Common Mistakes

| Tried | Error | Correct |
|-------|-------|---------|
| `opencode "prompt"` | "Failed to change directory" | `opencode run "prompt"` |
| `--model claude-3.5-sonnet` | "Provider not found" | `-m openrouter/anthropic/claude-3.7-sonnet` |
| `opencode --prompt "..."` | Launches TUI | `opencode run "..."` |

## Red Flags - STOP and Check Help

If you're about to:
- Query databases or guess file paths directly
- Use flags or subcommands you haven't verified

**STOP** and run `opencode --help` first.

## Free Models (Verified Feb 2026)

| Model | Provider | Notes |
|-------|----------|-------|
| `opencode/big-pickle` | OpenCode Zen | General reasoning |
| `opencode/glm-5-free` | OpenCode Zen | General tasks |
| `google/antigravity-gemini-3-flash` | Antigravity | Fast, capable |
| `openai/gpt-5.2-codex` | OpenAI Codex | Frontier coding (via plugin) |

**Avoid:** OpenRouter free models often have "No endpoints" - test before relying.

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
