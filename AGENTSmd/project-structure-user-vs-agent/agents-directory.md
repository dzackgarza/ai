---
order: 10
title: .agents Directory
---

Every project root contains a `.agents/` directory. This is the canonical location for all agent-facing artifacts:

- **`memories/`** — Durable operational knowledge managed by `agent-memory` (project scope, bound via `.agent-memory.toml`). All process docs, AGENTS.md supplements, workflow instructions, diagnostic playbooks, and other agent-facing documentation are stored as typed memories, not as loose markdown files.
- **`justfile`** — Agent-facing recipes for QC, debugging, and guardrail enforcement. All recipes are `[private]`.
- **Scripts** — Hygiene checks, anti-gaming measures, slop detection, hook scripts. Scripts that encode reusable diagnostic surfaces live here, referenced by the private justfile.

Nothing in `.agents/` is user-facing. The top-level `justfile` may route through agent recipes to enforce mandatory measures, but those recipes are `[private]` and invisible to `just --list`.
