# AI Configuration

## Harnesses

| Harness | Global Context File | Project Context File | System Prompt Override | Skills Directories | Source |
|---------|---------------------|----------------------|----------------------|-------------------|--------|
| claude | `~/.claude/CLAUDE.md` | `CLAUDE.md` in project root | — | custom slash commands | [docs](https://docs.anthropic.com/en/docs/claude-code/overview) |
| codex | `~/.codex/AGENTS.md` | `AGENTS.md` in project root | — | — | [docs](https://developers.openai.com/codex/guides/agents-md/) |
| gemini | `~/.gemini/GEMINI.md` | `GEMINI.md` in workspace | `GEMINI_SYSTEM_MD` env var | `~/.gemini/skills/`, `~/.agents/skills/` | [context](https://geminicli.com/docs/cli/gemini-md/), [skills](https://geminicli.com/docs/cli/skills/), [system](https://geminicli.com/docs/cli/system-prompt/) |
| qwen | `~/.qwen/QWEN.md` | `QWEN.md` in workspace | `QWEN_SYSTEM_MD` env var | `~/.qwen/skills/` | [docs](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/) |
| opencode | `~/.config/opencode/AGENTS.md` | `AGENTS.md` in project root | — | `~/.claude/skills/` (fallback) | [docs](https://opencode.ai/docs/rules/) |
| amp | `~/.config/amp/AGENTS.md`, `~/.config/AGENTS.md` | `AGENTS.md` in cwd, parent dirs, subtrees | — | `~/.config/agents/skills/`, `~/.config/amp/skills/`, `.agents/skills/`, `.claude/skills/`, `~/.claude/skills/` | [docs](https://ampcode.com/manual) |
| kilo | `~/.kilocode/` | — | — | `~/.kilocode/skills/` | local (docs TBD) |

**Master files (symlinked to all harnesses):**
- Context file: `~/ai/AGENTS.md`
- Skills: `~/ai/skills/` (29 skills)

### Verified Details

**Codex CLI** ([source](https://developers.openai.com/codex/guides/agents-md/)):
- Global scope: `~/.codex/AGENTS.md` or `~/.codex/AGENTS.override.md`
- Project scope: Walks from project root to cwd, reading `AGENTS.md` or `AGENTS.override.md`
- Fallback filenames configurable via `project_doc_fallback_filenames`

**Gemini CLI** ([context](https://geminicli.com/docs/cli/gemini-md/), [skills](https://geminicli.com/docs/cli/skills/), [system prompt](https://geminicli.com/docs/cli/system-prompt/)):
- Context hierarchy: Global (`~/.gemini/GEMINI.md`) → Workspace → JIT (auto-scans when accessing dirs)
- Custom filename via `context.fileName` setting: `{"context": {"fileName": ["AGENTS.md", "GEMINI.md"]}}`
- Skills precedence: Workspace > User > Extension; `.agents/skills/` takes precedence over `.gemini/skills/`
- System prompt override: See [System Prompt Override](#system-prompt-override) section

**Qwen Code** ([source](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/)):
- Forked from Gemini CLI, uses similar context system
- Default context file: `QWEN.md` (configurable via `context.fileName`)
- Skills from `.qwen/skills/` (workspace) and `~/.qwen/skills/` (user)
- System prompt override: See [System Prompt Override](#system-prompt-override) section

**OpenCode** ([source](https://opencode.ai/docs/rules/)):
- Global: `~/.config/opencode/AGENTS.md`
- Project: `AGENTS.md` in project root
- Fallback: `CLAUDE.md` (unless `OPENCODE_DISABLE_CLAUDE_CODE=1`)
- Skills: `~/.claude/skills/` (unless `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1`)

**Amp** ([source](https://ampcode.com/manual)):
- Global: `$HOME/.config/amp/AGENTS.md` or `$HOME/.config/AGENTS.md`
- Project: `AGENTS.md` in cwd, parent dirs (up to `$HOME`), subtrees
- Fallback: If no `AGENTS.md`, reads `AGENT.md` or `CLAUDE.md`
- Skills precedence (first wins): `~/.config/agents/skills/` → `~/.config/amp/skills/` → `.agents/skills/` → `.claude/skills/` → `~/.claude/skills/`

**Claude Code** ([source](https://docs.anthropic.com/en/docs/claude-code/overview)):
- Uses `CLAUDE.md` at project root and parent directories
- Skills via custom slash commands

### System Prompt Override

Some harnesses allow replacing their built-in system prompt entirely. This is different from context files (AGENTS.md, GEMINI.md) which are appended to the prompt.

**Gemini CLI** ([docs](https://geminicli.com/docs/cli/system-prompt/)):

Set `GEMINI_SYSTEM_MD` environment variable:
```bash
# Use .gemini/system.md in project
GEMINI_SYSTEM_MD=true gemini

# Use custom file
GEMINI_SYSTEM_MD=/path/to/my-system.md gemini

# Use file in home directory
GEMINI_SYSTEM_MD=~/prompts/system.md gemini

# Disable override (use built-in)
GEMINI_SYSTEM_MD=false gemini
```

Can also persist in `.gemini/.env`:
```
GEMINI_SYSTEM_MD=1
```

When active, Gemini shows `|⌐■_■|` indicator in the UI.

**Qwen Code**:

Forked from Gemini CLI - same mechanism with `QWEN_SYSTEM_MD`:
```bash
QWEN_SYSTEM_MD=/path/to/system.md qwen
```

## Prompts

### Interactive Agents (`~/ai/prompts/interactive_agents/`)

**Top-level agents - users invoke these directly in the coding harness.**

| Agent | Role | Temperature |
|-------|------|-------------|
| **interactive** | Default entry point, user-facing | 0.5 |
| **autonomous** | Execution engine (called by interactive) | 0.2 |

**Interactive handles all horizons:**

| Horizon | Criteria | Interactive's Action |
|---------|----------|---------------------|
| Trivial | < 2 min, obvious | Just do it |
| Small | Fits in head, clear path | Brief plan → execute |
| Complex | Multiple unknowns, design needed | Design doc → hand off to autonomous |

**Autonomous is not an entry point** - it receives plans from interactive and executes without user interaction.

**Workflow:**

```
User → interactive
         │
         ├─► trivial ──► just do it
         │
         ├─► small ──► plan briefly → execute
         │
         └─► complex ──► design doc → hand off to autonomous
                                          │
                                          └─► planner → executor → done
```

**Other:**
| Agent | Description |
|-------|-------------|
| executor | Executes implementation plans |
| minimal | Minimal agent template |

### Subagents (`~/ai/prompts/subagents/`)

**Internal agents - called by interactive/autonomous agents, not meant for direct user invocation.**

**Research (spawned in parallel):**

| Agent | Purpose |
|-------|---------|
| codebase-locator | Find WHERE files are |
| codebase-analyzer | Understand HOW code works |
| pattern-finder | Find existing patterns |
| artifact-searcher | Search past work |

**Execution (spawned sequentially):**

| Agent | Purpose |
|-------|---------|
| planner | Creates implementation plan |
| executor | Orchestrates implementer + reviewer |
| implementer | Writes code |
| reviewer | Verifies correctness |

**Utility:**

| Agent | Description |
|-------|-------------|
| project-initializer | Initializes new projects |
| code-compliance-reviewer | Reviews code against standards |
| code-smell-detector | Detects code smells |

### Worker Agents (`~/ai/prompts/worker_agents/`)

**Specialized agents with extra local tools - usable both interactively AND autonomously.**

Workers are domain-specific agents that can be:
- **Loaded interactively** when user wants careful, hands-on work
- **Used autonomously** for scheduled tasks, regular upkeep, or audits

| Worker | Interactive Use | Autonomous Use |
|--------|-----------------|----------------|
| librarian | Careful work on Zotero library | Regular upkeep/audits |
| test_engineer | Design test strategy with user | Run test coverage audits |
| documentation_specialist | Plan docs structure | Generate missing docs |

Each worker has `prompt.md` + `example_tasks/` showing autonomous work they can complete.

## MCP Servers

| Name | Command | Description | Link |
|------|---------|-------------|------|
| serena | `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --project-from-cwd` | Code intelligence, symbol navigation | https://github.com/oraios/serena |
| morph | `npx -y @morphllm/morphmcp` | Fast code edits via Morph LLM | https://github.com/morph-llm/morphmcp |
| kindly | `uvx --from git+https://github.com/Shelpuk-AI-Technology-Consulting/kindly-web-search-mcp-server kindly-web-search-mcp-server start-mcp-server` | Web search | https://github.com/Shelpuk-AI-Technology-Consulting/kindly-web-search-mcp-server |
| context7 | `npx -y @upstash/context7-mcp` | Documentation search (llms.txt) | https://github.com/upstash/context7 |
| cut-copy-paste-mcp | `npx -y @fastmcp-me/cut-copy-paste-mcp` | Clipboard operations | https://github.com/fastmcp-me/cut-copy-paste-mcp |

### Adding MCP Servers by Harness

**Claude Code** ([docs](https://docs.anthropic.com/en/docs/claude-code/mcp)):
```bash
# HTTP server
claude mcp add --transport http <name> <url>

# Stdio server
claude mcp add --transport stdio <name> -- <command> [args...]

# List servers
claude mcp list
```
Config files: `~/.claude.json` (user), `.mcp.json` (project)

**OpenCode** ([docs](https://opencode.ai/docs/mcp-servers/)):
Edit `opencode.json` directly (no CLI command):
```json
{
  "mcp": {
    "my-server": {
      "type": "local",
      "command": ["npx", "-y", "my-mcp-server"],
      "enabled": true
    },
    "remote-server": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp"
    }
  }
}
```
Config files: `~/.config/opencode/opencode.json` (global), `opencode.json` (project)

**Codex CLI** ([docs](https://developers.openai.com/codex/config-reference/)):
Edit `~/.codex/config.toml`:
```toml
[mcp_servers.my-server]
command = "npx"
args = ["-y", "my-mcp-server"]
env = { "API_KEY" = "value" }

[mcp_servers.remote-server]
url = "https://mcp.example.com/mcp"
```
Config file: `~/.codex/config.toml`

**Gemini CLI** ([docs](https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html)):
```bash
# Add server
gemini mcp add --transport http <name> <url>
gemini mcp add -s user <name> -- <command> [args...]
```
Or edit `settings.json`:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-server"]
    },
    "remote-server": {
      "httpUrl": "https://mcp.example.com/mcp"
    }
  }
}
```
Config files: `~/.gemini/settings.json` (user), `.gemini/settings.json` (project)

**Qwen Code** ([docs](https://qwenlm.github.io/qwen-code-docs/)):
Forked from Gemini CLI - same configuration pattern:
```bash
qwen mcp add --transport http <name> <url>
```
Config files: `~/.qwen/settings.json` (user), `.qwen/settings.json` (project)

**Kilo**:
Edit `~/.kilocode/cli/global/settings/mcp_settings.json`:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-server"],
      "env": {},
      "disabled": false
    }
  }
}
```

**Amp** ([docs](https://ampcode.com/manual)):
Amp reads MCP config from multiple locations. Check `~/.config/amp/` or harness documentation for current format.

## OpenCode Plugins

Config: `~/ai/opencode/opencode.json`

### Auth Plugins
| Plugin | Purpose | Link |
|--------|---------|------|
| `opencode-antigravity-auth@latest` | Antigravity provider auth (Gemini, Claude via Google) | https://github.com/NoeFabris/opencode-antigravity-auth |
| `opencode-qwencode-auth` | Qwen OAuth authentication | https://github.com/anomalyco/opencode/issues/11557 |
| `opencode-openai-codex-auth` | OpenAI Codex auth (GPT-5.x Codex models) | https://github.com/numman-ali/opencode-openai-codex-auth |

### Utility Plugins
| Plugin | Purpose | Link |
|--------|---------|------|
| `cc-safety-net` | Safety net for destructive git/fs commands | https://github.com/kenryu42/claude-code-safety-net |
| `@azumag/opencode-rate-limit-fallback` | Auto fallback on rate limit (429) | https://npmjs.com/package/@azumag/opencode-rate-limit-fallback |
| `@ramtinj95/opencode-tokenscope` | Token usage stats and cost tracking | https://github.com/ramtinJ95/opencode-tokenscope |
