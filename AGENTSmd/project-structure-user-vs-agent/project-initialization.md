---
order: 5
tags:
- source-owner-preference
- source-system-contract
- source-observed-model-failure
- function-define
- function-constrain
- function-procedure
- function-route
- function-allocate
- function-evaluate
- failure-process-overproduction
- failure-premature-action
- failure-state-misplacement
- failure-scope-drift
- retest-model-reasoning
- retest-model-alignment
- retest-model-tool-use
- retest-policy-change
- retest-toolchain-change
title: Project Initialization
---

Load `project-initialization` before substantive implementation only when repository-wide
state, durable project surfaces, or public coordination can materially affect the work.

Match the initialization weight to the work, not to the fact that you are inside a
repository. A trivial, self-contained action — filing or triaging a GitHub issue,
leaving a comment, answering a question, a one-off doc or config fix, a spike-sized
probe, data labeling, or a narrow script — does **not** trigger the full normal-form
sweep, discovery, or mixed-state normalization. Do the small named thing and stop.
Filing an issue is a lightweight
`git-guidelines`/`github-issues` action, not a signal to begin project discovery.
Reserve the full `project-initialization` workflow for substantive implementation that
depends on shared project state, roadmap/PRD/proof-bearing work, cross-agent handoff, or
any change that will produce or claim public execution state.
When classification is uncertain but the action is bounded and reversible, default to the
lighter route. Ask only when the alternatives would produce materially different or
hard-to-reverse work.

That skill owns the normal-form check: git root/freshness, GitHub public state
(wiki, issue tree, sub-issues, milestones, PRs, and draft PR claim maps), durable state
surface classification, SDL-MCP registration/indexing when available, repo instructions,
`.agents/`, agent-memory binding and memory search, `justfile` shape, and
`~/ai-review-ci` QC/hooks/CI wiring.

If a project's mixed state overlaps or blocks the requested feature work, normalize the
relevant state first unless the user explicitly asked only for diagnosis or audit.
Unrelated mixed state is not a prerequisite; preserve it and keep the requested boundary.
Normalization means identifying the current
GitHub issue-tree root or creating the missing public execution tree from the accepted
plan, assigning GitHub Milestone scope, and replacing local duplicate status with links to
wiki, `agent-memory`, issues, milestones, or PRs as appropriate.

If work explicitly requires public execution tracking but has no known issue-tree parent,
milestone scope, or PR claim set, load `plan`, `agent-memory`, and `git-guidelines` and use
`plan/references/externalization.md` to place it.
Do not manufacture public coordination surfaces for work that can be completed and
verified as a direct commit.
