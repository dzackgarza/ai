---
order: 20
title: What Qualifies as a PR
---

Load `git-guidelines` before opening, updating, reviewing, or merging PRs.

PRs are for significant work: whole features, broad changes, sensitive regressions, or
work that needs review.

For significant work, the PR is a claim against a selected GitHub issue set or subtree,
not a free-standing implementation plan. Before opening or updating the PR, use
`git-guidelines/creating-prs.md` to confirm the issue-tree parent, GitHub Milestone scope,
close/reference split, and proof obligations claimed or not claimed.

Simple doc changes, trivial fixes, and one-off edits usually should stay as direct
commits unless the user asks for PR workflow or the work needs public issue-tree tracking.
