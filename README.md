# AI Configuration

## Harnesses

| Harness | Global System Prompt | Project System Prompt | Skills Directories | Source |
|---------|---------------------|----------------------|-------------------|--------|
| claude | `~/.claude/CLAUDE.md` | `CLAUDE.md` in project root | custom slash commands | [docs](https://docs.anthropic.com/en/docs/claude-code/overview) |
| codex | `~/.codex/AGENTS.md` | `AGENTS.md` in project root | — | [docs](https://developers.openai.com/codex/guides/agents-md/) |
| gemini | `~/.gemini/GEMINI.md` | `GEMINI.md` in workspace | `~/.gemini/skills/`, `~/.agents/skills/` | [context](https://geminicli.com/docs/cli/gemini-md/), [skills](https://geminicli.com/docs/cli/skills/) |
| qwen | `~/.qwen/QWEN.md` | `QWEN.md` in workspace | `~/.qwen/skills/` | [docs](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/) |
| opencode | `~/.config/opencode/AGENTS.md` | `AGENTS.md` in project root | `~/.claude/skills/` (fallback) | [docs](https://opencode.ai/docs/rules/) |
| amp | `~/.config/amp/AGENTS.md`, `~/.config/AGENTS.md` | `AGENTS.md` in cwd, parent dirs, subtrees | `~/.config/agents/skills/`, `~/.config/amp/skills/`, `.agents/skills/`, `.claude/skills/`, `~/.claude/skills/` | [docs](https://ampcode.com/manual) |
| kilo | `~/.kilocode/` | — | `~/.kilocode/skills/` | local (docs TBD) |

**Master files (symlinked to all harnesses):**
- System prompt: `~/ai/AGENTS.md`
- Skills: `~/ai/skills/` (29 skills)

### Verified Details

**Codex CLI** ([source](https://developers.openai.com/codex/guides/agents-md/)):
- Global scope: `~/.codex/AGENTS.md` or `~/.codex/AGENTS.override.md`
- Project scope: Walks from project root to cwd, reading `AGENTS.md` or `AGENTS.override.md`
- Fallback filenames configurable via `project_doc_fallback_filenames`

**Gemini CLI** ([context](https://geminicli.com/docs/cli/gemini-md/), [skills](https://geminicli.com/docs/cli/skills/)):
- Context hierarchy: Global (`~/.gemini/GEMINI.md`) → Workspace → JIT (auto-scans when accessing dirs)
- Custom filename via `context.fileName` setting: `{"context": {"fileName": ["AGENTS.md", "GEMINI.md"]}}`
- Skills precedence: Workspace > User > Extension; `.agents/skills/` takes precedence over `.gemini/skills/`

**Qwen Code** ([source](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/)):
- Forked from Gemini CLI, uses similar context system
- Default context file: `QWEN.md` (configurable via `context.fileName`)
- Skills from `.qwen/skills/` (workspace) and `~/.qwen/skills/` (user)

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

### System Prompts (`~/ai/prompts/system_prompts/`)

| File | Description |
|------|-------------|
| system.md | General system prompt template |

## MCP Servers

| Name | Command | Description | Link |
|------|---------|-------------|------|
| serena | `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --project-from-cwd` | Code intelligence, symbol navigation | https://github.com/oraios/serena |
| morph | `npx -y @morphllm/morphmcp` | Fast code edits via Morph LLM | https://github.com/morph-llm/morphmcp |
| kindly | `uvx --from git+https://github.com/Shelpuk-AI-Technology-Consulting/kindly-web-search-mcp-server kindly-web-search-mcp-server start-mcp-server` | Web search | https://github.com/Shelpuk-AI-Technology-Consulting/kindly-web-search-mcp-server |
| context7 | `npx -y @upstash/context7-mcp` | Documentation search (llms.txt) | https://github.com/upstash/context7 |
| cut-copy-paste-mcp | `npx -y @fastmcp-me/cut-copy-paste-mcp` | Clipboard operations | https://github.com/fastmcp-me/cut-copy-paste-mcp |

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
