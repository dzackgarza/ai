---
order: 10
title: Live User Feedback
---

When the user asks for a plan, load `plan` and `agent-memory`.
Plans are durable artifacts, not chat-only outlines, and must be stored as
`agent-memory` plan records in the central vault while private or converging.

Nontrivial plans must decide where they fit in the GitHub execution tree before
implementation begins. Load `git-guidelines` and `plan/references/externalization.md` when
a plan may become public execution state, a GitHub issue tree, a GitHub Milestone, a draft
PR, or a multi-agent handoff. The plan must name the tree root or parent issue, milestone
scope, issue set or subtree claimed, close/reference split, and proof obligations claimed
or not claimed.

Never begin implementation from a plan until the user has approved it and the required
GitHub issue-tree, milestone, and PR-claim surfaces either exist or are explicitly out of
scope for a trivial direct commit.

When the user asks for a simple plan, write the minimal workflow in positive terms. Still
include the concrete interception point, data path, state owner before and after the
action, and proof point. Do not replace those details with extra artifacts, governance, or
a list of rejected mechanisms.

When the user asks to read, annotate, or give feedback on a plan, the `plan` skill owns
the on-demand HTML review surface and annotation workflow.
