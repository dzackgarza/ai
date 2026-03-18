# OpenCode Complete Reference

Comprehensive documentation for OpenCode - the open-source AI coding agent built for the terminal.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [CLI Commands & Flags](#cli-commands--flags)
4. [Built-in Tools](#built-in-tools)
5. [Built-in Agents](#built-in-agents)
6. [Configuration](#configuration)
7. [Permissions System](#permissions-system)
8. [MCP Servers](#mcp-servers)
9. [Agent Skills](#agent-skills)
10. [Environment Variables](#environment-variables)
11. [Providers & Models](#providers--models)
12. [Key Features](#key-features)

---

## Overview

OpenCode is an **open-source AI coding agent** built for the terminal. It's a Go-based TUI (Terminal User Interface) application that provides AI-powered coding assistance directly from the command line.

**Key characteristics:**
- Supports 75+ LLM providers via [Models.dev](https://models.dev)
- Multiple interfaces: TUI, desktop app, IDE extension, web interface
- Built on Bubble Tea TUI framework
- SQLite-based persistent storage for conversations
- LSP integration for code intelligence
- MCP (Model Context Protocol) for extensible tool integration

**Project status:** The original opencode-ai/opencode repository was archived on Sep 18, 2025. The project continues at anomalyco/opencode.

---

## Installation

### Install Script (Recommended)
```bash
curl -fsSL https://opencode.ai/install | bash
```

### Package Managers

**Node.js:**
```bash
npm install -g opencode-ai
bun install -g opencode-ai
pnpm install -g opencode-ai
yarn global add opencode-ai
```

**Homebrew (macOS/Linux):**
```bash
brew install anomalyco/tap/opencode  # Recommended (always up to date)
brew install opencode                # Official formula (updated less)
```

**Arch Linux:**
```bash
sudo pacman -S opencode    # Stable
paru -S opencode-bin       # Latest from AUR
```

**Windows:**
```bash
choco install opencode     # Chocolatey
scoop install opencode     # Scoop
```

**Other:**
```bash
mise use -g github:anomalyco/opencode
docker run -it --rm ghcr.io/anomalyco/opencode
```

### Desktop App
Download from [releases page](https://github.com/anomalyco/opencode/releases) or [opencode.ai/download](https://opencode.ai/download).

**Platforms:**
- macOS (Apple Silicon): `opencode-desktop-darwin-aarch64.dmg`
- macOS (Intel): `opencode-desktop-darwin-x64.dmg`
- Windows: `opencode-desktop-windows-x64.exe`
- Linux: `.deb`, `.rpm`, or AppImage

```bash
brew install --cask opencode-desktop        # macOS
scoop bucket add extras; scoop install extras/opencode-desktop  # Windows
```

---

## CLI Commands & Flags

### Global Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--help` | `-h` | Display help |
| `--version` | `-v` | Print version number |
| `--print-logs` | | Print logs to stderr |
| `--log-level` | | Log level (DEBUG, INFO, WARN, ERROR) |

### TUI Command (Default)

```bash
opencode [project] [flags]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--continue` | `-c` | Continue the last session |
| `--session` | `-s` | Session ID to continue |
| `--fork` | | Fork the session when continuing |
| `--prompt` | | Prompt to use |
| `--model` | `-m` | Model to use (provider/model format) |
| `--agent` | | Agent to use |
| `--port` | | Port to listen on |
| `--hostname` | | Hostname to listen on |

### Subcommands

#### `run` - Non-interactive Mode
```bash
opencode run [message..] [flags]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--command` | | The command to run |
| `--continue` | `-c` | Continue the last session |
| `--session` | `-s` | Session ID to continue |
| `--fork` | | Fork session when continuing |
| `--share` | | Share the session |
| `--model` | `-m` | Model (provider/model format) |
| `--agent` | | Agent to use |
| `--file` | `-f` | File(s) to attach |
| `--format` | | `default` or `json` output |
| `--title` | | Title for the session |
| `--attach` | | Attach to running server |
| `--port` | | Port for local server |

#### `serve` - Headless API Server
```bash
opencode serve [flags]
```

| Flag | Description |
|------|-------------|
| `--port` | Port to listen on |
| `--hostname` | Hostname to listen on |
| `--mdns` | Enable mDNS discovery |
| `--cors` | Additional CORS origins |

Set `OPENCODE_SERVER_PASSWORD` to enable HTTP basic auth.

#### `web` - Web Interface
```bash
opencode web [flags]
```

Same flags as `serve`. Opens browser to web interface.

#### `attach` - Attach to Remote Backend
```bash
opencode attach [url] [flags]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--dir` | | Working directory |
| `--session` | `-s` | Session ID to continue |

#### `auth` - Authentication Management
```bash
opencode auth login    # Configure API keys
opencode auth list     # List authenticated providers
opencode auth ls       # Short version
opencode auth logout   # Remove credentials
```

#### `models` - Model Management
```bash
opencode models [provider] [flags]
```

| Flag | Description |
|------|-------------|
| `--refresh` | Refresh models cache |
| `--verbose` | Include metadata (costs, etc.) |

#### `session` - Session Management
```bash
opencode session list [flags]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--max-count` | `-n` | Limit to N most recent |
| `--format` | | `table` or `json` |

#### `stats` - Usage Statistics
```bash
opencode stats [flags]
```

| Flag | Description |
|------|-------------|
| `--days` | Last N days |
| `--tools` | Number of tools to show |
| `--models` | Show model breakdown |
| `--project` | Filter by project |

#### `export` / `import` - Session Data
```bash
opencode export [sessionID]
opencode import <file>
opencode import https://opncd.ai/s/abc123
```

#### `mcp` - MCP Server Management
```bash
opencode mcp add           # Add MCP server (interactive)
opencode mcp list          # List configured servers
opencode mcp ls            # Short version
opencode mcp auth [name]   # OAuth authentication
opencode mcp auth list     # List OAuth-capable servers
opencode mcp logout [name] # Remove OAuth credentials
opencode mcp debug <name>  # Debug connection issues
```

#### `agent` - Agent Management
```bash
opencode agent create      # Create custom agent
opencode agent list        # List available agents
```

#### `github` - GitHub Integration
```bash
opencode github install    # Install GitHub agent
opencode github run [flags]
```

| Flag | Description |
|------|-------------|
| `--event` | GitHub mock event |
| `--token` | GitHub personal access token |

#### `acp` - ACP Server
```bash
opencode acp [flags]
```

| Flag | Description |
|------|-------------|
| `--cwd` | Working directory |
| `--port` | Port to listen on |
| `--hostname` | Hostname to listen on |

#### `upgrade` / `uninstall`
```bash
opencode upgrade [target]        # Update to latest or specific version
opencode upgrade --method npm    # Specify installation method
opencode uninstall [flags]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--keep-config` | `-c` | Keep configuration files |
| `--keep-data` | `-d` | Keep session data |
| `--dry-run` | | Preview what would be removed |
| `--force` | `-f` | Skip confirmation |

---

## Built-in Tools

Tools allow the LLM to perform actions. All tools are **enabled by default** and don't require permission.

### File Operations

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **read** | Read file contents | `file_path`, `offset`, `limit` |
| **edit** | Modify files via exact string replacement | `file_path`, `old_string`, `new_string`, `use_regex`, `replace_all` |
| **write** | Create/overwrite files | `file_path`, `content` |
| **patch** | Apply patch files | Patch format |

### Search & Discovery

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **grep** | Search file contents with regex | `pattern`, `path`, `include`, `case_insensitive`, `context_before`, `context_after` |
| **glob** | Find files by pattern | `pattern`, `path` |
| **list** | List directory contents | `path`, `ignore` |

### Execution

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **bash** | Execute shell commands | `command`, `timeout` |

### Code Intelligence

| Tool | Description | Notes |
|------|-------------|-------|
| **lsp** | LSP queries | Experimental: requires `OPENCODE_EXPERIMENTAL_LSP_TOOL=true` |

**Supported operations:** `goToDefinition`, `findReferences`, `hover`, `documentSymbol`, `workspaceSymbol`, `goToImplementation`, `prepareCallHierarchy`, `incomingCalls`, `outgoingCalls`

### Web & Knowledge

| Tool | Description | Notes |
|------|-------------|-------|
| **webfetch** | Fetch web content | URL retrieval |
| **websearch** | Search the web | Requires OpenCode provider or `OPENCODE_ENABLE_EXA=1` |
| **codesearch** | Search code examples | Exa Code API |

### Task Management

| Tool | Description |
|------|-------------|
| **todowrite** | Create/update todo lists |
| **todoread** | Read current todo list |

### Interaction

| Tool | Description |
|------|-------------|
| **question** | Ask user questions during execution |
| **skill** | Load agent skills |

### Tool Configuration

Configure in `opencode.json`:

```json
{
  "permission": {
    "edit": "deny",
    "bash": "ask",
    "webfetch": "allow"
  }
}
```

Wildcard support:
```json
{
  "permission": {
    "mymcp_*": "ask"
  }
}
```

### Ignore Patterns

Tools like `grep`, `glob`, `list` use ripgrep and respect `.gitignore`. Create a `.ignore` file to include ignored paths:

```
!node_modules/
!dist/
!build/
```

---

## Built-in Agents

Agents are specialized AI assistants with custom prompts, models, and tool access.

### Primary Agents (Tab to switch)

| Agent | Mode | Description |
|-------|------|-------------|
| **build** | primary | Default - all tools enabled for development |
| **plan** | primary | Read-only analysis (edit/bash require approval) |
| **compaction** | primary | Hidden - auto-compacts long context |
| **title** | primary | Hidden - generates session titles |
| **summary** | primary | Hidden - creates summaries |

### Subagents (@mention to invoke)

| Agent | Mode | Description |
|-------|------|-------------|
| **general** | subagent | Multi-step tasks, can run parallel work |
| **explore** | subagent | Fast, read-only codebase exploration |

### Agent Switching

- **Tab key** - Cycle through primary agents
- **@mention** - Invoke subagents (e.g., `@general help me search`)
- **Navigation** - Use `<Leader>+Right/Left` to navigate parent/child sessions

---

## Configuration

### Config Locations (Precedence Order)

1. **Remote config** - `.well-known/opencode` (organizational defaults)
2. **Global config** - `~/.config/opencode/opencode.json`
3. **Custom config** - `OPENCODE_CONFIG` env var
4. **Project config** - `./opencode.json` in project root
5. **`.opencode` directories** - agents, commands, plugins
6. **Inline config** - `OPENCODE_CONFIG_CONTENT` env var

**Note:** Configs are **merged**, not replaced. Later configs override earlier ones only for conflicting keys.

### Config Format

Supports **JSON** and **JSONC** (JSON with Comments):

```json
{
  "$schema": "https://opencode.ai/config.json",
  // Your configuration
  "model": "anthropic/claude-sonnet-4-5"
}
```

### Schema Reference

```json
{
  "$schema": "https://opencode.ai/config.json",
  
  // Model configuration
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "anthropic/claude-haiku-4-5",
  
  // UI settings
  "theme": "opencode",
  "autoupdate": true,
  
  // Session settings
  "share": "manual",
  "default_agent": "build",
  
  // Instructions
  "instructions": ["AGENTS.md", "docs/*.md"],
  
  // Permissions
  "permission": {
    "*": "allow",
    "edit": "ask"
  },
  
  // MCP servers
  "mcp": {
    "server-name": {
      "type": "remote",
      "url": "https://..."
    }
  },
  
  // Custom agents
  "agent": {
    "custom-agent": {
      "description": "...",
      "model": "...",
      "prompt": "..."
    }
  },
  
  // Custom commands
  "command": {
    "test": {
      "template": "Run tests with coverage",
      "description": "Run tests"
    }
  },
  
  // LSP servers
  "lsp": {
    "go": {
      "command": "gopls",
      "disabled": false
    }
  },
  
  // Formatters
  "formatter": {
    "prettier": {
      "disabled": true
    }
  },
  
  // Keybinds
  "keybinds": {},
  
  // TUI settings
  "tui": {
    "scroll_speed": 3,
    "scroll_acceleration": { "enabled": true },
    "diff_style": "auto"
  },
  
  // Server settings
  "server": {
    "port": 4096,
    "hostname": "0.0.0.0",
    "mdns": true,
    "cors": ["http://localhost:5173"]
  },
  
  // Compaction settings
  "compaction": {
    "auto": true,
    "prune": true,
    "reserved": 10000
  },
  
  // File watcher
  "watcher": {
    "ignore": ["node_modules/**", "dist/**"]
  },
  
  // Plugins
  "plugin": ["opencode-plugin-name"],
  
  // Provider settings
  "provider": {
    "anthropic": {
      "options": {
        "timeout": 600000,
        "setCacheKey": true
      }
    }
  },
  
  // Provider filtering
  "disabled_providers": ["openai"],
  "enabled_providers": ["anthropic"],
  
  // Experimental
  "experimental": {}
}
```

### Variable Substitution

**Environment variables:**
```json
{
  "model": "{env:OPENCODE_MODEL}",
  "provider": {
    "anthropic": {
      "options": {
        "apiKey": "{env:ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

**File contents:**
```json
{
  "provider": {
    "openai": {
      "options": {
        "apiKey": "{file:~/.secrets/openai-key}"
      }
    }
  }
}
```

### Provider-Specific Options

**Amazon Bedrock:**
```json
{
  "provider": {
    "amazon-bedrock": {
      "options": {
        "region": "us-east-1",
        "profile": "my-aws-profile",
        "endpoint": "https://bedrock-runtime.us-east-1.vpce-xxxxx.amazonaws.com"
      }
    }
  }
}
```

---

## Permissions System

### Actions

| Action | Behavior |
|--------|----------|
| `"allow"` | Run without approval |
| `"ask"` | Prompt for approval |
| `"deny"` | Block the action |

### Available Permissions

| Permission | Description |
|------------|-------------|
| `read` | Reading files (matches file path) |
| `edit` | All file modifications (edit, write, patch, multiedit) |
| `glob` | File globbing (matches pattern) |
| `grep` | Content search (matches regex pattern) |
| `list` | Directory listing (matches path) |
| `bash` | Shell commands (matches parsed commands) |
| `task` | Launching subagents (matches subagent type) |
| `skill` | Loading skills (matches skill name) |
| `lsp` | LSP queries |
| `todoread`, `todowrite` | Todo list operations |
| `webfetch` | URL fetching (matches URL) |
| `websearch`, `codesearch` | Web/code search (matches query) |
| `external_directory` | Paths outside working directory |
| `doom_loop` | Repeated tool calls (3x same input) |

### Default Permissions

- Most permissions default to `"allow"`
- `doom_loop` and `external_directory` default to `"ask"`
- `read` is `"allow"`, but `.env` files are denied by default

### Configuration Examples

**Global:**
```json
{
  "permission": {
    "*": "ask",
    "bash": "allow",
    "edit": "deny"
  }
}
```

**Set all at once:**
```json
{
  "permission": "allow"
}
```

**Granular rules (object syntax):**
```json
{
  "permission": {
    "bash": {
      "*": "ask",
      "git *": "allow",
      "npm *": "allow",
      "rm *": "deny"
    },
    "edit": {
      "*": "deny",
      "docs/*.md": "allow"
    }
  }
}
```

**External directories:**
```json
{
  "permission": {
    "external_directory": {
      "~/projects/personal/**": "allow"
    },
    "edit": {
      "~/projects/personal/**": "deny"
    }
  }
}
```

### Wildcard Patterns

- `*` matches zero or more of any character
- `?` matches exactly one character
- `~` or `$HOME` expands to home directory

**Rule precedence:** Last matching rule wins.

### Per-Agent Override

```json
{
  "permission": {
    "bash": { "*": "ask" }
  },
  "agent": {
    "build": {
      "permission": {
        "bash": {
          "*": "ask",
          "git *": "allow"
        }
      }
    }
  }
}
```

---

## MCP Servers

Model Context Protocol for external tool integration.

### Local MCP Servers

```json
{
  "mcp": {
    "my-local-server": {
      "type": "local",
      "command": ["npx", "-y", "my-mcp-command"],
      "environment": {
        "MY_ENV_VAR": "value"
      },
      "enabled": true,
      "timeout": 5000
    }
  }
}
```

**Options:**

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `type` | String | Yes | Must be `"local"` |
| `command` | Array | Yes | Command and arguments |
| `environment` | Object | No | Environment variables |
| `enabled` | Boolean | No | Enable/disable |
| `timeout` | Number | No | Timeout in ms (default: 5000) |

### Remote MCP Servers

```json
{
  "mcp": {
    "my-remote-server": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp",
      "enabled": true,
      "headers": {
        "Authorization": "Bearer token"
      },
      "timeout": 5000
    }
  }
}
```

**Options:**

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `type` | String | Yes | Must be `"remote"` |
| `url` | String | Yes | Server URL |
| `enabled` | Boolean | No | Enable/disable |
| `headers` | Object | No | HTTP headers |
| `oauth` | Object/false | No | OAuth config |
| `timeout` | Number | No | Timeout in ms |

### OAuth Authentication

**Automatic:**
```json
{
  "mcp": {
    "my-oauth-server": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp"
    }
  }
}
```

**Pre-registered:**
```json
{
  "mcp": {
    "my-oauth-server": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "clientId": "{env:MY_CLIENT_ID}",
        "clientSecret": "{env:MY_CLIENT_SECRET}",
        "scope": "tools:read tools:execute"
      }
    }
  }
}
```

**Disable OAuth:**
```json
{
  "mcp": {
    "api-key-server": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp",
      "oauth": false,
      "headers": {
        "Authorization": "Bearer {env:MY_API_KEY}"
      }
    }
  }
}
```

**CLI commands:**
```bash
opencode mcp auth <server-name>     # Authenticate
opencode mcp auth list             # List OAuth servers
opencode mcp logout <server-name>  # Remove credentials
opencode mcp debug <server-name>   # Debug issues
```

### Per-Agent MCP

```json
{
  "mcp": {
    "my-mcp": { "type": "local", "command": ["..."], "enabled": true }
  },
  "tools": {
    "my-mcp*": false
  },
  "agent": {
    "my-agent": {
      "tools": {
        "my-mcp*": true
      }
    }
  }
}
```

### Example MCP Servers

**Sentry:**
```json
{
  "mcp": {
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp",
      "oauth": {}
    }
  }
}
```

**Context7:**
```json
{
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "{env:CONTEXT7_API_KEY}"
      }
    }
  }
}
```

**Grep.app:**
```json
{
  "mcp": {
    "gh_grep": {
      "type": "remote",
      "url": "https://mcp.grep.app"
    }
  }
}
```

---

## Agent Skills

Skills are reusable behaviors defined in `SKILL.md` files.

### Skill Locations

OpenCode searches these locations:

| Location | Type |
|----------|------|
| `.opencode/skills/<name>/SKILL.md` | Project config |
| `~/.config/opencode/skills/<name>/SKILL.md` | Global config |
| `.claude/skills/<name>/SKILL.md` | Claude-compatible (project) |
| `~/.claude/skills/<name>/SKILL.md` | Claude-compatible (global) |
| `.agents/skills/<name>/SKILL.md` | Agent-compatible (project) |
| `~/.agents/skills/<name>/SKILL.md` | Agent-compatible (global) |

### Skill Format

```markdown
---
name: skill-name
description: What this skill does (1-1024 chars)
license: MIT
compatibility: opencode
metadata:
  key: value
---

## What I do
- Task description

## When to use me
Usage instructions
```

### Name Validation

- 1-64 characters
- Lowercase alphanumeric with single hyphen separators
- Cannot start/end with `-`
- No consecutive `--`
- Must match directory name

Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`

### Skill Permissions

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

### Per-Agent Override

**In agent frontmatter:**
```markdown
---
permission:
  skill:
    "documents-*": "allow"
---
```

**In opencode.json:**
```json
{
  "agent": {
    "plan": {
      "permission": {
        "skill": {
          "internal-*": "allow"
        }
      }
    }
  }
}
```

### Disable Skills

**In agent frontmatter:**
```markdown
---
tools:
  skill: false
---
```

**In opencode.json:**
```json
{
  "agent": {
    "plan": {
      "tools": {
        "skill": false
      }
    }
  }
}
```

---

## Environment Variables

### Core Variables

| Variable | Type | Description |
|----------|------|-------------|
| `OPENCODE_AUTO_SHARE` | boolean | Automatically share sessions |
| `OPENCODE_GIT_BASH_PATH` | string | Git Bash path (Windows) |
| `OPENCODE_CONFIG` | string | Custom config file path |
| `OPENCODE_CONFIG_DIR` | string | Custom config directory |
| `OPENCODE_CONFIG_CONTENT` | string | Inline JSON config |
| `OPENCODE_DISABLE_AUTOUPDATE` | boolean | Disable update checks |
| `OPENCODE_DISABLE_PRUNE` | boolean | Disable data pruning |
| `OPENCODE_DISABLE_TERMINAL_TITLE` | boolean | Disable title updates |
| `OPENCODE_PERMISSION` | string | Inline JSON permissions |
| `OPENCODE_DISABLE_DEFAULT_PLUGINS` | boolean | Disable default plugins |
| `OPENCODE_DISABLE_LSP_DOWNLOAD` | boolean | Disable LSP downloads |
| `OPENCODE_ENABLE_EXPERIMENTAL_MODELS` | boolean | Enable experimental models |
| `OPENCODE_DISABLE_AUTOCOMPACT` | boolean | Disable auto-compaction |
| `OPENCODE_DISABLE_CLAUDE_CODE` | boolean | Disable .claude reading |
| `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT` | boolean | Disable CLAUDE.md |
| `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS` | boolean | Disable .claude/skills |
| `OPENCODE_DISABLE_MODELS_FETCH` | boolean | Disable remote models |
| `OPENCODE_FAKE_VCS` | string | Fake VCS for testing |
| `OPENCODE_DISABLE_FILETIME_CHECK` | boolean | Disable filetime check |
| `OPENCODE_CLIENT` | string | Client identifier |
| `OPENCODE_ENABLE_EXA` | boolean | Enable Exa web search |
| `OPENCODE_SERVER_PASSWORD` | string | HTTP basic auth password |
| `OPENCODE_SERVER_USERNAME` | string | HTTP basic auth username |
| `OPENCODE_MODELS_URL` | string | Custom models URL |

### Experimental Variables

| Variable | Type | Description |
|----------|------|-------------|
| `OPENCODE_EXPERIMENTAL` | boolean | Enable all experimental |
| `OPENCODE_EXPERIMENTAL_ICON_DISCOVERY` | boolean | Icon discovery |
| `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` | boolean | Disable copy on select |
| `OPENCODE_EXPERIMENTAL_BASH_DEFAULT_TIMEOUT_MS` | number | Bash timeout |
| `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX` | number | Max output tokens |
| `OPENCODE_EXPERIMENTAL_FILEWATCHER` | boolean | File watcher |
| `OPENCODE_EXPERIMENTAL_OXFMT` | boolean | oxfmt formatter |
| `OPENCODE_EXPERIMENTAL_LSP_TOOL` | boolean | LSP tool |
| `OPENCODE_EXPERIMENTAL_DISABLE_FILEWATCHER` | boolean | Disable file watcher |
| `OPENCODE_EXPERIMENTAL_EXA` | boolean | Exa features |
| `OPENCODE_EXPERIMENTAL_LSP_TY` | boolean | LSP type checking |
| `OPENCODE_EXPERIMENTAL_MARKDOWN` | boolean | Markdown features |
| `OPENCODE_EXPERIMENTAL_PLAN_MODE` | boolean | Plan mode |

---

## Providers & Models

### Supported Providers

OpenCode supports 75+ LLM providers via [Models.dev](https://models.dev):

- Anthropic Claude
- OpenAI GPT
- Google Gemini
- AWS Bedrock
- Azure OpenAI
- Groq
- OpenRouter
- GitHub Copilot
- Minimax
- GLM
- Qwen
- DeepSeek
- Mistral
- Local models (LMStudio, Ollama)

### Model Format

`provider/model-id` (e.g., `anthropic/claude-sonnet-4-5`)

### Model Selection Priority

1. `--model` or `-m` CLI flag
2. `model` in config
3. Last used model
4. Internal priority

### Model Variants

Built-in variants for popular providers:

**Anthropic:**
- `high` - High thinking budget (default)
- `max` - Maximum thinking budget

**OpenAI:**
- `none`, `minimal`, `low`, `medium`, `high`, `xhigh`

**Google:**
- `low`, `high`

### Custom Variants

```json
{
  "provider": {
    "openai": {
      "models": {
        "gpt-5": {
          "variants": {
            "thinking": {
              "reasoningEffort": "high",
              "textVerbosity": "low"
            }
          }
        }
      }
    }
  }
}
```

### Model Options

```json
{
  "provider": {
    "openai": {
      "models": {
        "gpt-5": {
          "options": {
            "reasoningEffort": "high",
            "textVerbosity": "low",
            "reasoningSummary": "auto"
          }
        }
      }
    },
    "anthropic": {
      "models": {
        "claude-sonnet-4-5": {
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 16000
            }
          }
        }
      }
    }
  }
}
```

### Recommended Models

Models that work well with OpenCode (as of Feb 2026):

- GPT 5.2
- GPT 5.1 Codex
- Claude Opus 4.5
- Claude Sonnet 4.5
- Minimax M2.1
- Gemini 3 Pro

---

## Key Features

### Multi-Modal Support
- Images via drag-and-drop
- File attachments with `-f` flag
- Screenshot analysis

### Session Management
- SQLite persistent storage
- Session continuation (`-c`, `-s`)
- Session forking
- Export/import sessions
- Share links (`/share`)

### Context Management
- Auto-compaction when context is full
- Summarization of long conversations
- Token tracking and cost stats

### Git Integration
- Natural language git commands
- Automatic commit messages
- PR creation and management
- GitHub/GitLab integration

### Code Intelligence
- LSP integration (gopls, typescript-language-server, etc.)
- Diagnostics, definitions, references
- Call hierarchy

### Customization
- Themes
- Keybinds
- Formatters (Prettier, custom)
- Custom commands
- Custom agents

### Development Modes
- **Build mode** - Full tool access
- **Plan mode** - Analysis only (no edits)
- Tab to switch between modes

### Undo/Redo
- `/undo` to revert changes
- `/redo` to reapply
- Multiple undo levels

### Stats & Tracking
- Token usage
- Cost tracking
- Per-session statistics

---

## TUI Commands (In-Session)

| Command | Description |
|---------|-------------|
| `/init` | Initialize project (creates AGENTS.md) |
| `/connect` | Configure API keys |
| `/models` | Select model |
| `/share` | Share session |
| `/undo` | Undo changes |
| `/redo` | Redo changes |
| `@filename` | Fuzzy search files |
| `@agent-name` | Invoke subagent |

---

## File Structure

### Project Files

```
project/
├── opencode.json          # Project config
├── AGENTS.md              # Project instructions
├── .opencode/
│   ├── agents/            # Custom agents
│   ├── commands/          # Custom commands
│   ├── skills/            # Agent skills
│   ├── plugins/           # Local plugins
│   └── themes/            # Custom themes
└── .claude/
    └── skills/            # Claude-compatible skills
```

### Global Files

```
~/.config/opencode/
├── opencode.json          # Global config
├── agents/
├── commands/
├── skills/
├── plugins/
└── themes/

~/.local/share/opencode/
├── auth.json              # API credentials
├── mcp-auth.json          # MCP OAuth tokens
└── opencode.db            # Session database
```

---

*Last updated: 2026-02-23*