---
order: 25
tags:
- source-system-contract
- source-observed-model-failure
- function-define
- function-constrain
- function-procedure
- function-route
- function-evaluate
- failure-completion-laundering
- failure-reporting-distortion
- failure-feedback-laundering
- failure-process-overproduction
- retest-model-alignment
- retest-model-self-evaluation
- retest-policy-change
- retest-toolchain-change
title: PR Completion Gate
---

This gate applies only when the user requested PR work, the task began from an active PR,
or an existing public claim map makes review lifecycle part of the work.
A request to edit, commit, or push directly is not implicitly PR-scoped; do not open a PR
to activate this gate.

For genuinely PR-scoped work, the PR state is part of the work.
Do not report a PR task complete while the PR is still draft, while required claim-map
items remain open, or before any review required by the task's scope has been started.

Once every claimed issue and proof obligation is complete and evidenced:

- push the branch;
- republish the current PR body or claim map;
- run `gh pr ready <PR_NUMBER>`;
- trigger the automated review loop when the user, repository contract, or tracked claim
  requires it;
- route returned review and check feedback through `pr-feedback-triage`.

If any step is blocked, report that blocker as incomplete required work.
