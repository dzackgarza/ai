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
- failure-process-overproduction
- retest-model-self-evaluation
- retest-model-alignment
- retest-policy-change
- retest-toolchain-change
title: Chat Responses After Completing Work
---

Never summarize what was done.
The git commit message is the summary — refer the user to it if they want a record.
Before a substantive or multi-step completion report, progress update, or status
response, load `response-preparation` when the user needs synthesized status.
Do not invoke a reporting workflow for a direct answer, an obvious correction, or a
single trivial edit whose result can be stated plainly.

Use that skill to decide what the user needs to know that the commit, diff, terminal,
or artifact cannot already show.
Only report gaps, skipped surprises, undocumented decisions, incomplete required work,
and next actions.

For work already scoped to an active PR, required PR state and returned feedback remain
part of the task.
Do not create a PR or start a review loop merely to make a direct-commit task satisfy this
reporting rule.

Before responding after file edits, load `git-guidelines` if not already active and
verify the intended diff.
