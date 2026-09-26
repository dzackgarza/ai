# AGENTS.md

This repository holds the harness configuration for this machine. The operating policy
every harness loads is [AGENTS.global.md](./AGENTS.global.md); `just install` links it
into each harness home (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md`,
`~/.config/AGENTS.md`). This file covers only what is specific to working in this repo.

## Layout

| Path | Owns |
| --- | --- |
| `AGENTS.global.md` | the policy and skill routing table, hand-authored |
| `opencode/skills/` | the skills vault; some subtrees are symlinks into `~/ai-review-ci`, `~/gitclones/automated-reviews`, and `~/gitclones/agent-memory` |
| `opencode/agents/` | hand-written OpenCode agent definitions |
| `opencode/configs/` | source fragments compiled into `~/.config/opencode/opencode.json` |
| `justfile` | the recipe surface: `just install`, `just build`, `just test` |

## Rules for this repo

- A skill owned by another repository is edited and committed there, not here.
- A skill description is one sentence of at most 160 characters in the form
  "Use when <object or operation>". The routing table in `AGENTS.global.md` keys on
  concrete objects and operations, never on a situation the agent must classify.
- `just test` validates Markdown entrypoints and every WikiLink in the vault. Run it
  after adding, moving, or deleting a skill.
- `opencode/skills/synced/` is written by Claude Code's skill sync and is ignored.
- The commit hook compiles the OpenCode config and validates providers; it needs the
  network and takes about half a minute.
