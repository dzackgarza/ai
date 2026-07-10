---
order: 10
tags:
- source-owner-preference
- source-system-contract
- source-observed-model-failure
- function-constrain
- function-procedure
- function-route
- function-evaluate
- failure-reporting-distortion
- failure-completion-laundering
- failure-proxy-evidence
- retest-model-self-evaluation
- retest-model-alignment
- retest-policy-change
- retest-toolchain-change
title: Chat Responses After Completing Work
---

Never summarize what was done.
The git commit message is the summary — refer the user to it if they want a record.
Before any completion report, progress update, or status response, load
`response-preparation`.

Use that skill to decide what the user needs to know that the commit, diff, terminal,
or artifact cannot already show.
Only report gaps, skipped surprises, undocumented decisions, incomplete required work,
and next actions.

For PR-scoped work, draft PR status, unpushed commits, an unstarted automated review loop,
or untriaged returned review feedback are incomplete required work. Report those gaps
instead of a completion claim.

Before responding after file edits, load `git-guidelines` if not already active and
verify the intended diff.
