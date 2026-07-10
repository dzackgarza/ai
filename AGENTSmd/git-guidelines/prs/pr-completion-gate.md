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
- retest-model-alignment
- retest-model-self-evaluation
- retest-policy-change
- retest-toolchain-change
title: PR Completion Gate
---

For PR-scoped work, the PR state is part of the work.
Do not report a PR task complete while the PR is still draft, while required claim-map
items remain open, or before the automated review loop has been explicitly started.

Once every claimed issue and proof obligation is complete and evidenced:

- push the branch;
- republish the current PR body or claim map;
- run `gh pr ready <PR_NUMBER>`;
- trigger the automated review loop with `@codex review` or the repo's documented
  equivalent;
- route returned review and check feedback through `pr-feedback-triage`.

If any step is blocked, report that blocker as incomplete required work.
