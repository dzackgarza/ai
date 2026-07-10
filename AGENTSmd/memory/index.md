---
order: 90
tags:
- purpose-context
- purpose-preference
- purpose-policy
- purpose-procedure
- purpose-reference
- stability-model-independent
- stability-policy-contingent
- stability-tool-contingent
- stability-environment-contingent
title: Memory
---

Durable memory and project planning state are managed by `agent-memory`, invoked by default through `uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory`.
Memories are typed plain-Markdown files in a vault, addressed by key (e.g. `projects/<project-id>/decisions/parser-choice`), and split across two scopes:

- **global** — durable, cross-repo operational knowledge ("what this system is": environment conventions, machine stewardship, recurring workflows).
- **project** — knowledge bound to a single repository via `.agent-memory.toml`.

Memory **types** are `decision`, `trap`, `advice`, `context`, `reference`, and `plan`.
Use `plan` records for every plan, contract, phase state, queue, residue ledger, and
other planning state that must survive context windows.
Plans belong in the central vault through `agent-memory`, not as loose repo-local
Markdown.

**Store:** Stable operational guidance, environment quirks, cross-session execution
context, technical findings, corrections that should change future behavior, and
decisions that outlive a single task.

**Promote:** If a decision changes public project direction, user stories, proof burdens,
roadmaps, or cross-agent handoff state, update the owning GitHub issue, milestone, PR, or
wiki page as well as any needed memory.

**Do not store:** Audit trails, changelogs, work summaries, or live TODO lists.
Those belong in git or GitHub issues.

**Setup:** use the `uvx` runner for normal invocation and project binding:
`uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory init project --vault <vault>`.
Use the checkout's `just setup` only when provisioning the global vault and persistent runtime dependencies.
Validate a repository's wiring with `uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory doctor`.
