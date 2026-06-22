---
order: 90
title: Memory
---

Durable memory and project planning state are managed by `agent-memory`, invoked by default through `uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory`.
Memories are typed plain-Markdown files in a vault, addressed by key (e.g. `projects/<project-id>/decisions/parser-choice`), and split across two scopes:

- **global** — durable, cross-repo operational knowledge ("what this system is": environment conventions, machine stewardship, recurring workflows).
- **project** — knowledge bound to a single repository via `.agent-memory.toml`.

Memory **types** are `decision`, `trap`, `advice`, `context`, `reference`, and `plan`.
Use `plan` records for contracts, phase state, queues, residue ledgers, and other planning state that must survive context windows.

**Store:** Stable operational guidance, environment quirks, cross-session execution context, technical findings, decisions that outlive a single task.

**Do not store:** Audit trails, changelogs, work summaries.
Those belong in git.

**Setup:** use the `uvx` runner for normal invocation and project binding:
`uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory init project --vault <vault>`.
Use the checkout's `just setup` only when provisioning the global vault and persistent runtime dependencies.
Validate a repository's wiring with `uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory doctor`.
