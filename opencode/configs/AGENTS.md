# OpenCode Config Architecture

## Critical Warnings

### Do Not Edit opencode.json

This file is auto-generated. Any manual edits will be overwritten the next time
`scripts/build_config.py` runs. Treat it as a build artifact, not source code.

### .opencode Subdirectories Are Irrelevant To Global Config

The `.opencode/` directories in project folders are local to those projects. The global
config lives at `~/.config/opencode`, symlinked to `/home/dzack/ai/opencode`.

### Edit OpenCode Agents Directly

Runtime OpenCode agents are manually managed in `../agents/*.md`. Their prompt bodies,
frontmatter, model settings, and `permission` blocks are source code in this repo.
Do not introduce generated prompt-slug paths or external compiler paths for these files.

### Keep Config Sources Separate

The skeleton is for top-level defaults only. Modular pieces belong in their own files:

- Providers: `configs/providers/*.json`

- Runtime agents: `../agents/*.md`

- Plugin-local runtime config: `configs/local-plugins.json`

## TL;DR

`opencode.json` is not the source of truth. Persistent changes live in tracked source
files:

- Edit runtime agents in `opencode/agents/*.md`.

- Edit provider/model policy in `opencode/configs/providers/*.json`.

- Edit top-level defaults in `opencode/configs/config_skeleton.json`.

Then run:

```bash
just build
```

For narrower checks:

```bash
just build-agents
just build-config
```

Commit the source files plus any regenerated `opencode.json` diff from
`scripts/build_config.py`.

## Directory Structure

```text
configs/
├── config_skeleton.json   # Base top-level defaults
├── local-plugins.json     # Plugin-local runtime config
├── providers/             # Provider configs merged into opencode.json
│   ├── github-copilot.json
│   ├── opencode.json
│   └── ...
../agents/                 # Manual OpenCode markdown agents
```

## How scripts/build_config.py Works

1. Loads `config_skeleton.json` as the base.

2. Removes any top-level `permission` key from the generated `opencode.json` payload.

3. Merges all `providers/*.json` into `config["provider"]`.

4. Validates the combined config against the OpenCode schema.

5. Writes the combined result to `opencode.json`.

## Manual Agent Permissions

Every file in `opencode/agents/*.md` must carry its own YAML frontmatter and explicit
`permission` block. That frontmatter is the durable source for OpenCode runtime agent
permissions.

`just build-agents` validates the manual files; it does not synthesize permissions,
fetch prompt text, or rewrite agent markdown.

## Common Mistakes

| Mistake | Why It’s Wrong |
| --- | --- |
| Editing `opencode.json` directly | Gets overwritten next time `scripts/build_config.py` runs |
| Adding generated agent fragments | Creates a second source of truth beside `agents/*.md` |
| Removing an agent `permission` block | Breaks the manual permission ownership contract |
| Forgetting to run `just build-config` | Provider/default config changes do not appear in `opencode.json` |
| Committing only `opencode.json` | The tracked config source that produced it is missing |

## Model Provider IDs

When setting a model, use the format `provider/model-id`:

- `github-copilot/gpt-5-mini` — GitHub Copilot’s best GPT model (0x/free)

- `nvidia/moonshotai/kimi-k2.5` — NVIDIA hosted Kimi K2.5

- `opencode/minimax-m2.5-free` — OpenCode’s minimax M2.5 free

- `cursor-acp/auto` — Local Cursor ACP proxy

## Checking Current Settings

```bash
# Top-level default model
grep '^  "model":' opencode.json | head -1

# Provider model count
grep -c 'github-copilot/gpt-5-mini' opencode.json
```
