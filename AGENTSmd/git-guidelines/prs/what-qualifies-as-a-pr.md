---
order: 20
tags:
- source-owner-preference
- source-system-contract
- source-observed-model-failure
- function-define
- function-constrain
- function-procedure
- function-route
- function-evaluate
- failure-process-overproduction
- failure-scope-drift
- retest-model-reasoning
- retest-model-alignment
- retest-policy-change
- retest-toolchain-change
title: What Qualifies as a PR
---

Load `git-guidelines` before opening, updating, reviewing, or merging PRs.

PRs are for significant work: whole features, broad changes, sensitive regressions, or
work that needs review.

For significant work, the PR is a claim against a selected GitHub issue set or subtree,
not a free-standing implementation plan. Before opening or updating the PR, use
`git-guidelines/creating-prs.md` to confirm the issue-tree parent, GitHub Milestone scope,
close/reference split, and proof obligations claimed or not claimed.

Planning a nontrivial issue tree should also produce small draft PRs that each scope a
coherent unit of work — a group of related issues or a subtree node — so downstream agents
pick up pre-scoped units instead of opening a separate PR per narrow issue. One-issue-per-PR
fragments work into many tiny review-heavy PRs and forces agents to reinvent the unit of
work; scoping those units is a planning step, not a triage step. See
`plan/references/externalization.md`.

Simple doc changes, trivial fixes, and one-off edits usually should stay as direct
commits unless the user asks for PR workflow or the work needs public issue-tree tracking.
Complexity alone does not require a PR: substantive but bounded maintenance can remain a
direct commit when ownership, verification, and rollback are local and no review handoff
is needed.
