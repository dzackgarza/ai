---
order: 30
tags:
- purpose-context
- purpose-preference
- purpose-policy
- purpose-procedure
- purpose-reference
- purpose-remediation
- stability-model-independent
- stability-model-contingent
- stability-policy-contingent
- stability-tool-contingent
- stability-environment-contingent
title: Issues
---

Most tools in this environment are sourced from repos on the `dzackgarza` Github account.
Small observed errors, app inefficiencies, tool friction, false greens, and recurring
surprises in owned repos should become either an immediate fix or a GitHub issue on the
owning repo.
Do not file “bugs” for errors that have never actually been observed.
If the issue is observed, owned, and not fixed in the current coherent work unit, prefer
filing it over leaving it in chat, a local scratchpad, or memory.
For ambiguous ownership, broad policy changes, or interruptions outside the user's scope,
ask before filing.

For issue creation, triage, labels, assignment, and cross-repo issue work, load
`git-guidelines`.
For roadmap, PRD, feature, proof-bearing, or cross-agent work, do not file a flat issue
unless it is truly atomic. Load `plan/references/externalization.md` through `plan`, then
create or update the story-shaped issue tree, sub-issue edges, blocker dependencies,
GitHub Milestone scope, and linked PR claim map.

To manage the issue tree and discover traversal order programmatically, use the `itree` tool from `dzackgarza/itree` via `uvx`. Run `uvx --from git+https://github.com/dzackgarza/itree itree help model` for the full organization model; a work unit is always a leaf (checklist and proof live in its body, never in child issues).
- `uvx --from git+https://github.com/dzackgarza/itree itree next OWNER/REPO` to find the next open work unit — the single next task, not a task enclosed within one.
- `uvx --from git+https://github.com/dzackgarza/itree itree doctor OWNER/REPO` to verify the tree structure.
- `uvx --from git+https://github.com/dzackgarza/itree itree new OWNER/REPO "Title" --under OWNER/REPO#PARENT` to file a new work unit under a grouping issue (omit `--under` to be shown where it fits).
- `uvx --from git+https://github.com/dzackgarza/itree itree absorb OWNER/REPO#SOURCE --into OWNER/REPO#UNIT` to merge sub-PR content into a work unit verbatim.
- `uvx --from git+https://github.com/dzackgarza/itree itree attach OWNER/REPO#PARENT OWNER/REPO#CHILD` to attach a child issue.
- `uvx --from git+https://github.com/dzackgarza/itree itree move OWNER/REPO#CHILD --under OWNER/REPO#PARENT` to reparent or reorder.

For PR review comment surfaces, load `pr-feedback-triage` and `git-guidelines`.
