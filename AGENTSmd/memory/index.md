---
order: 90
title: Memory
---

Memories are managed through `iwe`, a file-based knowledge graph for Markdown notes, stored under `.agents/memories/`.
Each project’s `.agents/memories/` directory contains a `config.toml` and all memories stored as plain `.md` files.
Memories are persistent, searchable, and cross-session.

**Store:** Stable operational guidance, environment quirks, cross-session execution context, technical findings, decisions that outlive a single task.

**Do not store:** Audit trails, changelogs, work summaries.
Those belong in git.

**Organization:** Memories form a directed graph via markdown links.
Hierarchy is declared with inclusion links (a link on its own line).
A memory can appear in multiple contexts without duplication.
