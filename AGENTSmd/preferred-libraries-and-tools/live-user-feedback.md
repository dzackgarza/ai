---
order: 10
title: Live User Feedback
---

When the user asks for a plan, load `plan` and `agent-memory`.
Plans are durable artifacts, not chat-only outlines, and must be stored as
`agent-memory` plan records in the central vault.
If the plan becomes nontrivial public execution state, load `git-guidelines` and
`creating-implementation-plans` to promote it into a GitHub issue tree, milestone, or
draft PR after the user finalizes it.

Never begin implementation from a plan until the user has approved it.

When the user asks to read, annotate, or give feedback on a plan, the `plan` skill owns
the on-demand HTML review surface and annotation workflow.
