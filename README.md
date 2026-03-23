# AI Configuration

## Installation

**Prerequisites:**

```bash
# Install nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.bashrc  # or ~/.zshrc
nvm install --lts
```

**Install all harnesses:**

```bash
# Claude Code (native install with auto-updates)
curl -fsSL https://claude.ai/install.sh | bash

# Codex
npm install -g @openai/codex

# Gemini CLI
npm install -g @google/gemini-cli

# Qwen Code
npm install -g @qwen-code/qwen-code
# Alternative quick install: bash -c "$(curl -fsSL https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen.sh)"

# OpenCode
npm install -g opencode
# Alternative: curl -fsSL https://opencode.ai/install | bash

# Kilo Code
npm install -g @kilocode/cli
# Alternative: Install via VS Code extension or JetBrains plugin

# Amp (native install with auto-updates)
curl -fsSL https://ampcode.com/install.sh | bash
```

**Cursor CLI** (required for Cursor ACP provider in OpenCode):

```bash
curl -fsSL https://cursor.com/install.sh | bash
```

See [Cursor CLI announcement](https://cursor.com/blog/cli) for details.

**Post-installation:**

```bash
# Set up symlinks and environment variables
just install

# Install OpenCode plugins
npm install -g @ramtinj95/opencode-tokenscope

# Authenticate each harness (run once, opens browser/login prompt)
claude
codex
gemini
qwen
opencode
kilo
amp
```

## Harnesses

| Harness  | Global Context File                              | Project Context File                      | System Prompt Override         | Skills Directories                                                                                             | Source                                                                                                                                                          |
| -------- | ------------------------------------------------ | ----------------------------------------- | ------------------------------ | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| claude   | `~/.claude/CLAUDE.md`                            | `CLAUDE.md` in project root               | —                              | custom slash commands                                                                                          | [docs](https://docs.anthropic.com/en/docs/claude-code/overview)                                                                                                 |
| codex    | `~/.codex/AGENTS.md`                             | `AGENTS.md` in project root               | —                              | —                                                                                                              | [docs](https://developers.openai.com/codex/guides/agents-md/)                                                                                                   |
| gemini   | `~/.gemini/GEMINI.md`                            | `GEMINI.md` in workspace                  | `GEMINI_SYSTEM_MD` env var     | `~/.gemini/skills/`, `~/.agents/skills/`                                                                       | [context](https://geminicli.com/docs/cli/gemini-md/), [skills](https://geminicli.com/docs/cli/skills/), [system](https://geminicli.com/docs/cli/system-prompt/) |
| qwen     | `~/.qwen/QWEN.md`                                | `QWEN.md` in workspace                    | `QWEN_SYSTEM_MD` env var       | `~/.qwen/skills/`                                                                                              | [docs](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/)                                                                                |
| opencode | `~/.config/opencode/AGENTS.md`                   | `AGENTS.md` in project root               | `prompt` field in agent config | `~/.claude/skills/` (fallback)                                                                                 | [docs](https://opencode.ai/docs/rules/)                                                                                                                         |
| kilo     | `~/.config/kilo/AGENTS.md`                       | `AGENTS.md` in project root               | `prompt` field in agent config | `~/.kilocode/skills/`                                                                                          | [docs](https://kilo.ai/docs/agent-behavior/agents-md/), [skills](https://kilo.ai/docs/agent-behavior/skills)                                                    |
| amp      | `~/.config/amp/AGENTS.md`, `~/.config/AGENTS.md` | `AGENTS.md` in cwd, parent dirs, subtrees | —                              | `~/.config/agents/skills/`, `~/.config/amp/skills/`, `.agents/skills/`, `.claude/skills/`, `~/.claude/skills/` | [docs](https://ampcode.com/manual)                                                                                                                              |

**Master files (symlinked to all harnesses):**

- Context file: `~/ai/AGENTS.md`
- Skills: `~/ai/skills/`

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

**Kilo** ([AGENTS.md](https://kilo.ai/docs/agent-behavior/agents-md/), [skills](https://kilo.ai/docs/agent-behavior/skills)):

- Forked from OpenCode, uses similar configuration
- Global: `~/.config/kilo/AGENTS.md`
- Project: `AGENTS.md` in project root
- Skills: `~/.kilocode/skills/` (global), `.kilocode/skills/` (project)
- System prompt override: `prompt` field in agent config (same as OpenCode)

### Project-Local Configuration

Each harness looks for configuration files in the project directory. Place these in your project root:

| Harness  | Context File | Skills Directory                     | Config File                   |
| -------- | ------------ | ------------------------------------ | ----------------------------- |
| Claude   | `CLAUDE.md`  | `.claude/commands/` (slash commands) | —                             |
| Codex    | `AGENTS.md`  | —                                    | —                             |
| Gemini   | `GEMINI.md`  | `.gemini/skills/`                    | `.gemini/settings.json`       |
| Qwen     | `QWEN.md`    | `.qwen/skills/`                      | `.qwen/settings.json`         |
| OpenCode | `AGENTS.md`  | —                                    | `opencode.json`               |
| Kilo     | `AGENTS.md`  | `.kilocode/skills/`                  | `.kilocode/launchConfig.json` |
| Amp      | `AGENTS.md`  | `.agents/skills/`                    | —                             |

**Precedence (workspace > user > built-in):**

| Harness  | Context Hierarchy                                            | Skills Hierarchy                                            |
| -------- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| Gemini   | Project `.gemini/GEMINI.md` > `~/.gemini/GEMINI.md` > JIT    | `.agents/skills/` > `.gemini/skills/` > `~/.gemini/skills/` |
| Qwen     | Project `.qwen/QWEN.md` > `~/.qwen/QWEN.md`                  | `.qwen/skills/` > `~/.qwen/skills/`                         |
| Codex    | Walks project root → cwd reading `AGENTS.md`                 | —                                                           |
| OpenCode | `AGENTS.md` in project root > `~/.config/opencode/AGENTS.md` | `~/.claude/skills/` (fallback only)                         |
| Kilo     | `AGENTS.md` in project root > `~/.config/kilo/AGENTS.md`     | `.kilocode/skills/` > `~/.kilocode/skills/`                 |
| Amp      | cwd → parent dirs (to `$HOME`) → subtrees                    | `.agents/skills/` > `.claude/skills/` > `~/.claude/skills/` |

**Example project structure:**

```
my-project/
├── AGENTS.md              # Context for Codex, OpenCode, Kilo, Amp
├── GEMINI.md              # Context for Gemini (or configure to read AGENTS.md)
├── QWEN.md                # Context for Qwen
├── CLAUDE.md              # Context for Claude
├── .gemini/
│   ├── settings.json      # Gemini project config
│   └── skills/            # Gemini project skills
├── .qwen/
│   ├── settings.json      # Qwen project config
│   └── skills/            # Qwen project skills
├── .kilocode/
│   ├── launchConfig.json  # Kilo project config
│   └── skills/            # Kilo project skills
├── .agents/
│   └── skills/            # Amp project skills
└── opencode.json          # OpenCode project config
```

### Context Files vs System Prompts

**Context files** (AGENTS.md, GEMINI.md, CLAUDE.md, etc.) are user-supplied instructions that get **appended** to the harness's built-in system prompt. They add project-specific context, behavioral preferences, and task guidance.

**System prompts** are the harness's built-in instructions ("You are a helpful assistant..."). Some harnesses allow **replacing** this entirely via environment variables:

| Harness  | Context File (appended) | System Prompt Override (replaces) |
| -------- | ----------------------- | --------------------------------- |
| Gemini   | GEMINI.md               | `GEMINI_SYSTEM_MD` env var        |
| Qwen     | QWEN.md                 | `QWEN_SYSTEM_MD` env var          |
| OpenCode | AGENTS.md               | `prompt` field in agent config    |
| Kilo     | AGENTS.md               | `prompt` field in agent config    |
| Claude   | CLAUDE.md               | —                                 |
| Codex    | AGENTS.md               | —                                 |
| Amp      | AGENTS.md               | —                                 |

**When to override the system prompt:**

- You want complete control over agent behavior
- The built-in prompt conflicts with your workflow
- You're building a specialized tool on top of the harness

### System Prompt Override

Some harnesses allow replacing their built-in system prompt entirely. This is different from context files (AGENTS.md, GEMINI.md) which are appended to the prompt.

**Gemini CLI** ([docs](https://geminicli.com/docs/cli/system-prompt/)):

Set `GEMINI_SYSTEM_MD` environment variable:

```bash
# Use .gemini/system.md in project (fixed path)
GEMINI_SYSTEM_MD=true gemini

# Use custom file (variable holds the path)
GEMINI_SYSTEM_MD=/path/to/my-system.md gemini

# Disable override (use built-in)
GEMINI_SYSTEM_MD=false gemini
```

| Value              | Behavior                            |
| ------------------ | ----------------------------------- |
| `true` or `1`      | Uses `.gemini/system.md` in project |
| `/path/to/file.md` | Uses that file                      |
| `false` or `0`     | Uses built-in system prompt         |

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

**OpenCode** ([docs](https://opencode.ai/docs/agents/)):

OpenCode uses custom agents to replace the system prompt. Define an agent in `opencode.json`:

```json
{
  "agent": {
    "interactive": {
      "prompt": "You are a helpful assistant...",
      "model": "anthropic/claude-sonnet-4"
    }
  }
}
```

The `prompt` field completely replaces the built-in system prompt for that agent.

## Prompts

### Interactive Agents

**Agent definitions are no longer in this repo — they're all defined in the external `ai-prompts` repository.** See that repo for documentation on specific agents. This file contains only general notes about agent behavior patterns.

**Mode-switch indicators:**

- **Interactive -> plan**: If work is large (multi-file rewrite/refactor, substantial test additions/changes, or unclear implementation path), stop implementation and recommend switching to `plan` mode.
- **Interactive (never direct) -> build**: Do not switch directly from interactive to build for complex work. Go through `plan` first.
- **Plan -> interactive/build**: If user asks to edit anything other than the plan file, recommend switching to `interactive` for direct edits or finalizing plan then switching to `build`.
- **Build -> plan**: If any surprise requires a decision not in the plan, stop implementation and recommend returning to `plan` mode to revise.
- **Build -> interactive**: When planned work is complete, recommend switching to `interactive` for fine-tuned turn-by-turn follow-up.

**Workflow:**

```
User → interactive
         │
         ├─► trivial ──► just do it
         │
         ├─► small ──► plan briefly → execute
         │
         └─► complex ──► design doc → plan → build → interactive follow-up
```

**Other:**
| Agent | Description |
|-------|-------------|
| plan | Creates implementation plans |
| build | Executes implementation plans |
| minimal | Minimal agent template |

### Subagents (`ai-prompts` slugs under `sub-agents/`)

**Internal agents - called by top-level agents, not meant for direct user invocation.**

**Research (spawned in parallel):**

| Agent             | Purpose                                                      |
| ----------------- | ------------------------------------------------------------ |
| codebase-locator  | Find WHERE files are                                         |
| codebase-analyzer | Understand HOW code works                                    |
| precedent-finder  | Search memories and codebase for past decisions and patterns |

**Execution (spawned sequentially):**

| Agent               | Purpose                                             |
| ------------------- | --------------------------------------------------- |
| planner             | Creates implementation plan                         |
| build               | Orchestrates code writers + code-reviewer           |
| general_code_writer | Writes delegated non-Python code                    |
| python_code_writer  | Writes delegated Python code                        |
| code-reviewer       | Post-implementation code review and plan compliance |

**Utility:**

| Agent                   | Description                                                 |
| ----------------------- | ----------------------------------------------------------- |
| project-initializer     | Generates ARCHITECTURE.md and CODE_STYLE.md                 |
| plan-contract-validator | Constraint compliance, pattern consistency, smell detection |

### Specialized Agents (`ai-prompts` slugs under `interactive-agents/` and `sub-agents/`)

**Specialized agents with extra local tools - usable both interactively AND autonomously.**

Workers are domain-specific agents that can be:

- **Loaded interactively** when user wants careful, hands-on work
- **Used autonomously** for scheduled tasks, regular upkeep, or audits

| Worker             | Interactive Use                | Autonomous Use           |
| ------------------ | ------------------------------ | ------------------------ |
| librarian          | Careful work on Zotero library | Regular upkeep/audits    |
| test_engineer      | Design test strategy with user | Run test coverage audits |
| lattice_documentor | Plan docs structure            | Generate missing docs    |

Each specialized prompt lives in `ai-prompts`; support material is expanded into the fetched prompt document by slug.

## MCP Servers

| Name               | Command                                                                                                                                         | Description                          | Link                                                                             |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ | -------------------------------------------------------------------------------- |
| serena             | `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --project-from-cwd`                                                    | Code intelligence, symbol navigation | https://github.com/oraios/serena                                                 |
| morph              | `npx -y @morphllm/morphmcp`                                                                                                                     | Fast code edits via Morph LLM        | https://github.com/morph-llm/morphmcp                                            |
| kindly             | `uvx --from git+https://github.com/Shelpuk-AI-Technology-Consulting/kindly-web-search-mcp-server kindly-web-search-mcp-server start-mcp-server` | Web search                           | https://github.com/Shelpuk-AI-Technology-Consulting/kindly-web-search-mcp-server |
| context7           | `npx -y @upstash/context7-mcp`                                                                                                                  | Documentation search (llms.txt)      | https://github.com/upstash/context7                                              |
| cut-copy-paste-mcp | `npx -y @fastmcp-me/cut-copy-paste-mcp`                                                                                                         | Clipboard operations                 | https://github.com/fastmcp-me/cut-copy-paste-mcp                                 |

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

| Plugin                             | Purpose                                               | Link                                                     |
| ---------------------------------- | ----------------------------------------------------- | -------------------------------------------------------- |
| `opencode-antigravity-auth@latest` | Antigravity provider auth (Gemini, Claude via Google) | https://github.com/NoeFabris/opencode-antigravity-auth   |
| `opencode-anthropic-auth@latest`   | Anthropic OAuth authentication                        | https://github.com/anomalyco/opencode-anthropic-auth     |
| `opencode-qwencode-auth`           | Qwen OAuth authentication                             | https://github.com/anomalyco/opencode/issues/11557       |
| `opencode-openai-codex-auth`       | OpenAI Codex auth (GPT-5.x Codex models)              | https://github.com/numman-ali/opencode-openai-codex-auth |
| `@rama_nigg/open-cursor@latest`    | Cursor ACP provider (requires Cursor CLI)             | https://github.com/Nomadcxx/opencode-cursor              |

### Utility Plugins

| Plugin                                 | Purpose                                    | Link                                                           |
| -------------------------------------- | ------------------------------------------ | -------------------------------------------------------------- |
| `cc-safety-net`                        | Safety net for destructive git/fs commands | https://github.com/kenryu42/claude-code-safety-net             |
| `@azumag/opencode-rate-limit-fallback` | Auto fallback on rate limit (429)          | https://npmjs.com/package/@azumag/opencode-rate-limit-fallback |
| `@ramtinj95/opencode-tokenscope`       | Token usage stats and cost tracking        | https://github.com/ramtinJ95/opencode-tokenscope               |

## JSON Schemas and Validation

This repository utilizes the following JSON configuration files:

### `opencode.json`

- **Schema URL**: `https://opencode.ai/config.json`
- **Validation**: Add `"$schema": "https://opencode.ai/config.json"` to the top of your `opencode.json` file for IDE validation and autocompletion.

### `.safety-net.json`

- **Source**: [kenryu42/claude-code-safety-net](https://github.com/kenryu42/claude-code-safety-net)
- **Schema**: No formal JSON schema file. The expected structure is defined by the plugin's TypeScript implementation in its source repository.

### `rate-limit-fallback.json`

- **Source**: [azumag/opencode-rate-limit-fallback](https://github.com/azumag/opencode-rate-limit-fallback)
- **Schema**: No formal JSON schema file. The expected structure is defined by the plugin's TypeScript implementation in its source repository.

## Environment Configuration

The AI Configuration repository uses a modular approach for managing environment variables:

- Repository-local environment variables are stored in `~/ai/.envrc`
- The `just install` command adds a reference to source this file in your shell configuration (`.bashrc` or `.zshrc`)
- This approach keeps environment configuration tied to the repository while keeping shell configuration clean

## LLM Tooling

Prompt templating and model execution now live in two standalone public repos:

- `llm-templating-engine` — Jinja-style prompt/snippet library with structured bindings and JSON CLI interfaces
- `llm-runner` — template-driven model execution, provider handling, structured output, and response-template post-processing

This repo consumes both through GitHub-backed `uv` dependencies declared in:

- `scripts/pyproject.toml`
- `opencode/pyproject.toml`

Local convenience recipe:

- `just run-microagent` — passthrough to the canonical `llm-run` CLI in `opencode/.venv`

Example local use:

```bash
cat <<'EOF' | just run-microagent
{
  "template": {
    "path": "/tmp/evaluator.md"
  },
  "bindings": {
    "data": {
      "subject": "..."
    }
  },
  "overrides": {
    "models": ["groq/llama-3.3-70b-versatile"]
  }
}
EOF
```

Materialize `/tmp/evaluator.md` first with `cd opencode && uv run ai-prompts get micro-agents/evaluator > /tmp/evaluator.md`.

For ad hoc one-offs without syncing this repo, use the public upstream CLIs directly:

```bash
uvx --from git+https://github.com/dzackgarza/llm-templating-engine.git llm-template-render --help
uvx --from git+https://github.com/dzackgarza/llm-runner.git llm-run --help
```

Run `cd /home/dzack/ai/opencode && uv run --python .venv/bin/python llm-run --help` for the canonical local CLI usage.
