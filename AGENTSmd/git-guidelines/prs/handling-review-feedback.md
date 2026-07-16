---
order: 10
tags:
- source-system-contract
- source-observed-model-failure
- function-constrain
- function-procedure
- function-route
- function-evaluate
- failure-feedback-laundering
- failure-completion-laundering
- failure-reporting-distortion
- retest-model-alignment
- retest-model-self-evaluation
- retest-policy-change
- retest-toolchain-change
title: Handling Review Feedback
---

Load `pr-feedback-triage`, `git-guidelines`, and `test-guidelines` before acting on PR
review feedback.

Reviewer comments require explicit disposition and substantive action.
Do not acknowledge, resolve, hide, or dismiss feedback without either fixing it or
leaving a visible evidence-backed disposition note.

Before starting an A/B/C remediation cycle, assess current-PR necessity separately from
factual truth. A true finding requires current-PR remediation when it affects the PR's
claimed behavior, acceptance criteria, proof obligations, required checks, user-visible
correctness, security, safety, data integrity, fail-loud/type/QC integrity, or a regression
introduced or worsened by the PR.

Use `Backlogged as minor technical debt` only when all of those conditions are absent,
the concern is localized low-risk maintainability debt, batching it is more proportionate
than another commit/push/re-review cycle, and the PR remains semantically complete and
truthful without the change. Append it to an existing work-family debt issue or create one
through the repository's issue route; reply on the review thread with the evidence, issue
link, and why the current PR remains complete, then resolve it without role C or a
remediation commit. Never use this route to defer a current acceptance criterion or proof
gap.
