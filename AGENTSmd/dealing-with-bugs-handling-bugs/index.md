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
- retest-model-reasoning
- retest-model-self-evaluation
- retest-model-alignment
- retest-model-tool-use
- retest-policy-change
- retest-toolchain-change
title: Dealing With Bugs / Handling Bugs
---

When a bug or failure appears, do not patch first.

Load:

- `reality-grounded-debugging` for the observed-failure protocol, synthesis gate, and
  faithful red proof
- `systematic-debugging` for hypothesis discipline
- `test-driven-development` and `test-guidelines` for red/green proof obligations
- `git-guidelines` for the red-test commit and green-fix commit boundary
- `known-solution-first` as well when the symptom is owned by an external tool,
  compiler, API, package, provider, or library

The required first substantive artifact is a committed red test or reproducer that
fails because of the real observed bug.
Mocks, simulations, stubs, and tests that merely assert the absence of a proposed fix
do not prove the bug.

Only after the red proof exists should implementation change begin.

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
