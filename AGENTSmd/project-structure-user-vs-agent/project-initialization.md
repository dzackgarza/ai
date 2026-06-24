---
order: 5
title: Project Initialization
---

At the start of a session in a repository, load `project-initialization` before
substantive implementation.

That skill owns the normal-form check: git root/freshness, GitHub public state
(wiki, issue tree, sub-issues, milestones, PRs, and draft PR claim maps), durable state
surface classification, SDL-MCP registration/indexing when available, repo instructions,
`.agents/`, agent-memory binding and memory search, `justfile` shape, and
`~/ai-review-ci` QC/hooks/CI wiring.

If a project is in a mixed state, normalize that state before feature work unless the user
explicitly asked only for diagnosis or audit. Normalization means identifying the current
GitHub issue-tree root or creating the missing public execution tree from the accepted
plan, assigning GitHub Milestone scope, and replacing local duplicate status with links to
wiki, `agent-memory`, issues, milestones, or PRs as appropriate.

If nontrivial work has no known issue-tree parent, milestone scope, or PR claim set, do
not begin implementation. Load `plan`, `agent-memory`, and `git-guidelines`; use
`plan/references/externalization.md` to decide where the work fits or to report the public
state blocker.
