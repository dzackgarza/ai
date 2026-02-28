# Plugins — Required Reading

Before working in this directory, read the following in full:

## 1. OpenCode CLI Skill

- **SKILL.md** — CLI usage, interactive mode, `opencode run` limitations, async post-idle behavior
- **PLUGINS.md** — Plugin structure, all events, stop hook patterns, debugging workflow, session scoping

Located at: `~/ai/skills/opencode-cli/` (same repo, `skills/opencode-cli/`)

## 2. Serena Memories

Run `serena_read_memory` at session start. All memories apply here.

## 3. Tool Description Guidelines

When writing `tool({ description: ... })` in any plugin:

- Description = **when to use**, not what it does
- Start with `"Use when..."` — triggering conditions only
- NEVER summarize the tool's workflow or return value (model follows the description as a shortcut and skips the actual behavior)
- NEVER expose internals — file paths, directories, return shapes, implementation details. Tools abstract these away on purpose. Details are provided JIT via return values (e.g. `write_plan` returns the written path when done; the description doesn't need to mention `.serena/plans/`). Leaking internals in the description breaks abstraction, pollutes context (reducing the chance the tool is used in the right circumstances), and encourages the model to manually bypass the tool entirely.
- Use MUST/ALWAYS/NEVER for hard constraints
- Keep it short — one or two sentences
