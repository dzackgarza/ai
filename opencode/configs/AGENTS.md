# OpenCode Config Architecture

## Critical Warnings

- Do not edit `opencode.json` directly. It is rebuilt from source files.
- Do not edit generated files in `../agents/` directly. `just build-agents` overwrites them.
- Do not treat project-local `.opencode/` directories as the global config. The global config lives in `~/.config/opencode`, which is symlinked to this repository.

## Source Of Truth

- Top-level agent build workflow: `~/ai/justfile` `build-agents`
- Published prompt sources: `ai-prompts`
- Policy compiler: `~/opencode-plugins/opencode-permission-policy-compiler`
- Config skeleton: `config_skeleton.json`
- Provider fragments: `providers/*.json`
- Config assembly: `../scripts/build_config.py`

## Current Build Flow

### Managed agents

`just build-agents` is the only supported way to populate `../agents/*.md`.

For each managed agent, it:

- fetches the published prompt slug from `ai-prompts` with `uvx`
- pipes that markdown through `opencode-permission-policy-compiler`
- writes the resulting OpenCode agent markdown into the managed agents directory

By default the managed agents directory is `../agents/`. If `AGENTS_DIR` is exported,
the top-level recipe writes there instead.

### OpenCode config

`just build-config` rebuilds `opencode.json` from:

- `config_skeleton.json`
- `providers/*.json`

`scripts/build_config.py` ignores any skeleton-level `permission` block, then
`opencode-permission-policy-compiler set-global-policy global` applies the
global permission baseline to the compiled `opencode.json`.

### Full repo build

`just build` runs the repo-level OpenCode build flow:

- `just check-plugins`
- `just build-config`
- `just build-agents`
- `just build-agents-md`

## Update Workflow

### To change a managed agent

- edit or publish the prompt slug in `ai-prompts`
- update the policy compiler if permission behavior must change
- run `just build-agents`

### To change provider or top-level config

- edit `config_skeleton.json` and/or `providers/*.json`
- run `just build-config`

### To refresh everything

- run `just build`

## Common Mistakes

| Mistake | Why it is wrong |
| --- | --- |
| Editing `opencode.json` directly | The next `just build-config` overwrites it |
| Editing `../agents/*.md` directly | The next `just build-agents` overwrites them |
| Running any removed repo-local permission writer path | Permission application is owned by the external policy compiler |
| Updating prompt text locally without publishing `ai-prompts` | `just build-agents` fetches published slugs via `uvx` |
