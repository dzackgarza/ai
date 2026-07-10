---
order: 70
tags:
- purpose-context
- purpose-preference
- purpose-policy
- purpose-procedure
- purpose-reference
- purpose-remediation
- stability-timeless
- stability-model-contingent
- stability-policy-contingent
- stability-tool-contingent
- stability-environment-contingent
title: Hard Rules
---

This section is a router.

For project-internal unknowns, load `reality-grounded-debugging` and expose the local
shape with `tree` before narrowing.
For external tools, compilers, libraries, APIs, providers, package managers, exact
diagnostics, or dependency choices, load `known-solution-first`.

For code, tests, QC, slop findings, fallbacks, mocks, smoke tests, runtime defaults,
compatibility shims, deletion, or bespoke single-user policy, use the Bridge-Burning
Policy Router below.

Irreducible always-on rule: fail loudly, do not add fallbacks or legacy paths, and treat
this system as pre-launch bespoke software unless a loaded skill gives a narrower rule.

For git checkpoints, destructive-operation bans, and recoverable deletion, load
`git-guidelines`.
For standalone Python dependencies and missing tool provisioning, load
`tool-provisioning-and-environment-hygiene`.
