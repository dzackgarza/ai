# CLI Structure

This repository is a superproject that contains many package repos as submodules.

## Python CLIs

- `clis/ai-prompts`
- `clis/improved-jules-cli`
- `clis/llm-runner`
- `clis/llm-templating-engine`
- `clis/memory-manager`
- `clis/opencode-manager`
- `clis/opencode-permission-manager`
- `clis/otlp-collector`
- `clis/prompt-transformer`
- `clis/task-sched`
- `clis/usage-limits`
- `clis/zotero-librarian`

These packages declare their executable entrypoints in `pyproject.toml` under `[project.scripts]`.

## Mixed Python And TypeScript CLIs

- `clis/skill-suggester`
- `clis/todowrite`
- `clis/webtools`

These packages contain both Python and TypeScript code. Their packaged CLI entrypoints are Python, declared in `pyproject.toml`, while the TypeScript files are sidecars or companion tooling.

## TypeScript Plugins

- `plugins/opencode-plugin-improved-task`
- `plugins/opencode-plugin-improved-todowrite`
- `plugins/opencode-plugin-improved-webtools`
- `plugins/opencode-plugin-prompt-transformer`
- `plugins/opencode-plugin-reminder-injection`
- `plugins/opencode-zotero-plugin`

These packages are plugin packages with TypeScript entrypoints declared in `package.json`.

## Mixed Plugin Package

- `plugins/opencode-memory-plugin`

This package is primarily a TypeScript plugin package, but it also includes a Python MCP server under `src/opencode_memory`.

## Duplicate Package Paths

- `ai-prompts` mirrors `clis/ai-prompts`
- `improved-jules-cli` mirrors `clis/improved-jules-cli`

These top-level paths are separate package directories in this workspace. Keep their `justfile` behavior aligned with the corresponding package repo under `clis/`.
