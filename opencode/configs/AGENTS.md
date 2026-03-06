# OpenCode Config Architecture

## TL;DR

**`opencode.json` is NOT the source of truth.** It's generated via two scripts:

1. `manage_permissions.py` — compiles permission logic → `configs/agents/` and `configs/subagents/`
2. `build_config.py` — merges configs → `opencode.json`

To make config changes persist:

### For permissions changes:
1. Edit `opencode/manage_permissions.py` (AGENTS dict, TAG_RULES, capabilities)
2. Run `python3 manage_permissions.py --apply`
3. Run `python3 build_config.py`

### For model/provider/other changes:
1. Edit files in `configs/` (providers, agents, subagents, config_skeleton.json)
2. Run `python3 build_config.py`
3. Commit both the source configs AND the regenerated opencode.json

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

## Permissions: Two-Layer System

Permissions are managed in TWO steps:

### Step 1: manage_permissions.py (Source of Truth)

Located at `opencode/manage_permissions.py` — defines permission logic via:

- **TAG_RULES**: Base permissions by agent type (primary, subagent)
- **Capabilities**: Composable permission functions (`read_all()`, `write_in()`, etc.)
- **AGENTS dict**: Maps agent name → tags + capabilities + overrides

This is the SINGLE SOURCE OF TRUTH for permission logic.

### Step 2: Apply and Build

```bash
# 1. Compile permissions from manage_permissions.py -> configs/
python3 manage_permissions.py --apply

# 2. Merge configs/ -> opencode.json
python3 build_config.py
```

### What gets generated

- `configs/config_skeleton.json` — gets GLOBAL_PERMISSION (baseline)
- `configs/agents/*.json` — gets compiled permission block
- `configs/subagents/*.json` — gets compiled permission block

**Never edit permission blocks manually** — they're regenerated every time `manage_permissions.py --apply` runs. Edit the source in `manage_permissions.py` instead.

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|----------------|
| Editing opencode.json directly | Gets overwritten next time build_config.py runs |
| Editing permissions in configs/*.json manually | Gets overwritten next time manage_permissions.py --apply runs |
| Forgetting to run manage_permissions.py --apply | Permission changes don't appear in configs/ |
| Forgetting to run build_config.py | Changes to configs/ don't appear in opencode.json |
| Committing only opencode.json | Source configs aren't updated |
| Running build_config.py but not manage_permissions.py | Permissions revert to old values |

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
