---
order: 40
tags:
- source-system-contract
- source-observed-model-failure
- function-constrain
- function-procedure
- function-route
- function-evaluate
- failure-premature-action
- failure-proxy-evidence
- failure-tool-bypass
- failure-proof-gaming
- failure-process-overproduction
- retest-model-reasoning
- retest-model-self-evaluation
- retest-model-alignment
- retest-model-tool-use
- retest-policy-change
- retest-toolchain-change
title: Dealing With Bugs / Handling Bugs
---

Route failures by the requested object and proof burden:

- **Diagnosis only:** inspect the real failure and report the supported cause. Do not
  implement a fix merely because one becomes apparent.
- **Trivial non-behavioral correction:** typos, documentation, metadata, and simple
  configuration mistakes need the smallest direct verification, not a synthetic red-test
  lifecycle.
- **Behavioral regression or uncertain implementation failure:** reproduce the observed
  failure faithfully before changing implementation, then prove the fix against that
  boundary.

For behavioral regressions and uncertain implementation failures, load as applicable:

- `reality-grounded-debugging` for the observed-failure protocol, synthesis gate, and
  faithful red proof
- `systematic-debugging` for hypothesis discipline
- `test-driven-development` and `test-guidelines` for red/green proof obligations
- `git-guidelines` for the red-test commit and green-fix commit boundary
- `known-solution-first` as well when the symptom is owned by an external tool,
  compiler, API, package, provider, or library

The required first substantive artifact for a reproducible product regression is a red
test or reproducer that fails because of the real observed bug.
Commit a durable red proof separately. When the repository's ordinary hook rejects an
intentionally failing red proof, use its sanctioned route rather than bypassing the hook:

```bash
ai-review-ci red-commit --issue <owning-issue> -m "<message>"
```

This exception is only for the separately committed, faithful red proof of an actual
behavioral regression. It does not apply to documentation, prompts, metadata,
data-labeling, external-environment failures, or corrections whose proof is direct
inspection. Do not manufacture tests, commits, or bypasses for those changes.
Mocks, simulations, stubs, and tests that merely assert the absence of a proposed fix
do not prove the bug.

Only after the required proof exists should behavioral implementation change begin.

Debug by the scientific method, not by guess-and-check:

- **Form a falsifiable hypothesis and try to falsify it.** State the cause specifically
  enough that it could be proven wrong, then actively attempt to disprove it — do not
  gather only confirming evidence, and do not chase a vague, hard-to-falsify hunch. A
  hypothesis you cannot imagine disproving is not a hypothesis.
- **Bisect from the known-good state.** When a change introduces a regression from a state
  that was working, walk back to that known-good state and re-apply the changes in
  individually verified pieces until the exact breaking step is isolated. When you just
  changed something and it broke, the change is the suspect: do not blame the environment,
  invent external causes, or pursue speculative fixes with no evidence.
- **Prove the fix against the real failure, not a proxy.** Confirm the fix against the
  actual observed failure (the committed red reproducer), never against a stand-in signal
  that would still pass if the bug were unfixed.

Load `systematic-debugging` for the hypothesis ledger and falsification discipline and
`reality-grounded-debugging` for the observed-failure protocol.
