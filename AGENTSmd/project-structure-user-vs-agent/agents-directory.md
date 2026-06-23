---
order: 10
title: .agents Directory
---

Every project root contains a `.agents/` directory. This is the canonical location for
agent-facing project artifacts that are not durable memory or durable documentation:

- **`justfile`** — Agent-facing recipes for QC, debugging, and guardrail enforcement. All recipes are `[private]`.
- **Scripts** — Hygiene checks, anti-gaming measures, slop detection, hook scripts. Scripts that encode reusable diagnostic surfaces live here, referenced by the private justfile.

Durable operational knowledge, corrections, decisions, and planning state are managed
through `agent-memory` and bound by `.agent-memory.toml`; they are not maintained as loose
markdown under `.agents/`.
Durable project doctrine, requirements, user stories, roadmaps, and proof burdens belong
on the wiki.
If a local `.agents/` note starts carrying durable guidance, migrate it to the vault,
wiki, or GitHub issue/PR surface that owns it, then remove or replace the local note with
a pointer.

Nothing in `.agents/` is user-facing. The top-level `justfile` may route through agent
recipes to enforce mandatory measures, but those recipes are `[private]` and invisible to
`just --list`.
