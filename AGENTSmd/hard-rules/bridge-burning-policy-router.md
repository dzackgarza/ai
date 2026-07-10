---
order: 10
tags:
- source-system-contract
- source-observed-model-failure
- function-define
- function-constrain
- function-procedure
- function-route
- function-evaluate
- failure-tool-bypass
- failure-proof-gaming
- failure-proxy-evidence
- failure-destructive-state-change
- failure-process-overproduction
- retest-model-alignment
- retest-model-self-evaluation
- retest-model-tool-use
- retest-policy-change
- retest-toolchain-change
title: Bridge-Burning Policy Router
---

Use `policy-index` as the entry point when code, tests, or QC encounters a bridge-burning
policy concern. It decides which detailed policy is relevant.
Do not preload the entire policy suite for ordinary implementation.

Load the narrower owner only when its trigger is present:

- `anti-slop` for bridge-burning policies and anti-laundering doctrine.
- `bespoke-software-policy` for single-user, pre-launch, no-fallback constraints.
- `reviewing-llm-code/references/bridge-burning-red-flags.md` for the canonical red-flag inventory.
- `reviewing-llm-code/references/runtime-control-flow-red-flags.md` for runtime control-flow rules.
- `test-guidelines` for proof/test obligations.
- `test-guidelines/references/banned-test-shapes.md` for banned test assertion patterns.
- `fixing-slop` when an artifact is being renamed, deleted, quarantined, or “made honest.”
- `pr-feedback-triage` when acting on review comments or automated review feedback.

When tests are in scope, a test line is admissible only if it increases the epistemic
status of a repository-owned proof burden. If an assertion would still pass on a
plausibly broken app, it is banned.
Runtime defaults, fallbacks, optional critical dependencies, mocks/fakes/stubs, smoke
tests in proof paths, helper-level proof for boundary obligations, stringly errors,
boolean mode flags, compatibility shims, and deletion without burden transfer are hard
red flags.
