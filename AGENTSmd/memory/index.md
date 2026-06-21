---
order: 90
title: Memory
---

Durable memory is managed by `agent-memory`, an IWE-backed Markdown memory database installed from `github.com/dzackgarza/agent-memory`.
Memories are typed plain-Markdown files in a vault, addressed by key (e.g. `projects/<project-id>/decisions/parser-choice`), and split across two scopes:

- **global** — durable, cross-repo operational knowledge ("what this system is": environment conventions, machine stewardship, recurring workflows).
- **project** — knowledge bound to a single repository via `.agent-memory.toml`.

Memory **types** are `decision`, `trap`, `advice`, `context`, `reference`, and `plan`.

**Store:** Stable operational guidance, environment quirks, cross-session execution context, technical findings, decisions that outlive a single task.

**Do not store:** Audit trails, changelogs, work summaries.
Those belong in git.

**Setup:** install and provision once from the repo (`just setup` for the global vault; `agent-memory init project --vault <vault>` to bind a repository).
Validate a repository's wiring with `agent-memory doctor`.
