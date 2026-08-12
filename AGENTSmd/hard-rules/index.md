---
order: 70
tags:
- source-owner-context
- source-owner-preference
- source-system-contract
- source-observed-model-failure
- function-orient
- function-define
- function-constrain
- function-procedure
- function-route
- failure-tool-bypass
- failure-destructive-state-change
- failure-process-overproduction
- retest-model-alignment
- retest-model-tool-use
- retest-policy-change
- retest-toolchain-change
title: Hard Rules
---

This section is a router.

For project-internal unknowns, load `reality-grounded-debugging` and expose the local
shape with `tree` before narrowing.
For external tools, compilers, libraries, APIs, providers, package managers, exact
diagnostics, or dependency choices, load `known-solution-first`.

For code, tests, or QC that actually touches slop findings, fallbacks, mocks, smoke tests,
runtime defaults, compatibility shims, deletion, or bespoke single-user policy, use the
Bridge-Burning Policy Router below.
Ordinary bounded code editing does not require loading the entire review-policy stack.

Irreducible always-on rule: fail loudly, do not add fallbacks or legacy paths, and treat
this system as pre-launch bespoke software unless a loaded skill gives a narrower rule.

For git checkpoints, destructive-operation bans, and recoverable deletion, load
`git-guidelines`.
For standalone Python dependencies and missing tool provisioning, load
`tool-provisioning-and-environment-hygiene`.
