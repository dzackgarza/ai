# OpenCode Config Architecture

## TL;DR

**`opencode.json` is NOT the source of truth.** It's generated from files in `configs/` via `build_config.py`.

To make config changes persist:
1. Edit files in `configs/` (providers, agents, subagents, or config_skeleton.json)
2. Run `python3 build_config.py` to regenerate `opencode.json`
3. Commit the regenerated `opencode.json` along with the config changes

## Directory Structure

```
configs/
├── config_skeleton.json   # Base template (top-level defaults, MCP, permissions)
├── providers/             # Provider configs (merged into opencode.json provider key)
│   ├── github-copilot.json
│   ├── opencode.json
│   └── ...
├── agents/               # Primary agent definitions (mode: "primary")
│   ├── Interactive.json
│   ├── Build (Custom).json
│   └── ...
└── subagents/            # Subagent definitions (mode: "subagent")
    ├── general.json
    ├── explore.json
    └── ...
```

## How build_config.py Works

1. Loads `config_skeleton.json` as the base
2. Merges all `providers/*.json` into `config["provider"]`
3. Merges all `agents/*.json` into `config["agent"]`
4. Merges all `subagents/*.json` into `config["agent"]` (appended after primary agents)
5. Writes the combined result to `opencode.json`

## Permissions

Permissions are **NOT generated or inherited**. Each agent/subagent file explicitly defines its own `permission` block.

- `config_skeleton.json` — top-level permission defaults (used for top-level permissions)
- `configs/agents/*.json` — each agent has its own `permission` block (completely defines what that agent can do)
- `configs/subagents/*.json` — each subagent has its own `permission` block

**There is no inheritance.** If you want an agent to have the same permissions as another, you must explicitly copy the permission block.

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|----------------|
| Editing opencode.json directly | Gets overwritten next time build_config.py runs |
| Forgetting to run build_config.py | Changes to configs/ don't appear in opencode.json |
| Committing only opencode.json | Source configs aren't updated |

## Model Provider IDs

When setting a model, use the format `provider/model-id`:

- `github-copilot/gpt-5-mini` — GitHub Copilot's best GPT model (0x/free)
- `nvidia/moonshotai/kimi-k2.5` — NVIDIA hosted Kimi K2.5
- `opencode/minimax-m2.5-free` — OpenCode's minimax M2.5 free
- `cursor-acp/auto` — Local Cursor ACP proxy

## Checking Current Settings

```bash
# Top-level default model
grep '^  "model":' opencode.json | head -1

# Subagent model count
grep -c "github-copilot/gpt-5-mini" opencode.json
```
