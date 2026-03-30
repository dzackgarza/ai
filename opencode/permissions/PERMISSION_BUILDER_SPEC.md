# Managed Agent Build Specification

## Overview

Managed OpenCode agents are no longer compiled by `opencode/permissions/main.py`.
The supported build path is the top-level `just build-agents` recipe in `~/ai`.

That recipe performs a three-stage pipeline for each managed agent:

- fetch the published prompt slug from `ai-prompts` with `uvx`
- pipe the markdown into `opencode-permission-policy-compiler`
- write the resulting OpenCode agent markdown into the managed agents directory

## Inputs And Outputs

### Input

- published prompt slugs from `ai-prompts`
- optional `AGENTS_DIR` environment variable to override the output directory

### Output

- OpenCode-compliant markdown agent files in `~/ai/opencode/agents/` by default
- if `AGENTS_DIR` is set, the top-level recipe writes there instead

## Canonical Recipe

```bash
just build-agents
```

The repo-level `build` recipe calls `build-config` before `build-agents`.

## Managed Agent Manifest

The canonical slug-to-filename mapping lives in the top-level `~/ai/justfile`
inside the `build-agents` recipe.

Current managed entries are:

- `interactive-agents/autonomous` -> `autonomous.md`
- `interactive-agents/build` -> `build.md`
- `interactive-agents/plan` -> `plan.md`
- `micro-agents/compaction` -> `compaction.md`
- `sub-agents/correction-finder-ask` -> `correction-finder-ask.md`
- `sub-agents/general` -> `general.md`
- `sub-agents/explore` -> `explore.md`
- `interactive-agents/interactive` -> `interactive.md`
- `interactive-agents/minimal` -> `minimal.md`
- `sub-agents/prover` -> `prover.md`
- `micro-agents/summary` -> `summary.md`
- `micro-agents/title` -> `title.md`
- `interactive-agents/unrestricted-test` -> `unrestricted-test.md`

## Removed Legacy Path

The old repo-local writer path has been removed:

- `permissions/main.py build`
- `permissions/main.py --apply`
- `just build-permissions`

`permissions/main.py` remains only for local permission diagnostics such as
`validate-tools` and `list-rulesets`.
