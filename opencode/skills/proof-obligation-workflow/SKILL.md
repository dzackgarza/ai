---
name: proof-obligation-workflow
description: Use when developing or planning a project through a requirements-to-implementation pipeline that must trace user-facing requirements into proof obligations, tests, owned-surface minimization, QC triage, commits, or PR review. Trigger for requests to grill users, normalize requirements, create obligation/test plans, minimize bespoke code, separate subagent roles, audit drift/gaming, or route implementation through evidence gates.
---

# Proof Obligation Workflow

Use this skill to route product or project development through a proof-obligation-driven
state machine.
The core output is verified behavior with minimum locally owned implementation surface,
not a pile of planning artifacts.

## Mandatory Background

This skill governs coding, testing, QC, and PR workflow.
Before any stage that writes, reviews, tests, builds, or remediates code, load:

- `policy-index`
- `anti-slop`
- `policy-index/references/red-flags.md`
- `policy-index/references/runtime-control-flow.md`
- `test-guidelines`
- `policy-index/references/test-proof-rules.md`

Also load stage-specific skills instead of restating them:

- `known-solution-first` before external tool, compiler, library, API, package-manager,
  provider, or exact-error investigation.
- `reality-grounded-debugging` and `systematic-debugging` when the request is about an
  observed failure.
- `fixing-slop` before fixing a slop finding, deleting/quarantining artifacts, or
  making a false proof honest.
- `pr-feedback-triage` and `git-guidelines` when acting on review comments or PRs.

## Central Invariant

Every implemented behavior must trace backward to one of:

- a user-facing requirement;
- an expected standard app behavior;
- a chosen dependency or architecture contract;
- a documented technical necessity.

Every requirement must trace forward to obligations, tests, implementation evidence, or
an explicit deferral.
If any edge of that graph breaks, route backward.
Do not silently weaken a requirement to match the implementation.

## Start Gate

Before producing or modifying artifacts, state the live goal:

```text
The strongest live goal is ___.
The action I am about to take changes ___.
This does / does not satisfy the strongest goal because ___.
```

Then classify the request:

| Request shape | Route |
| --- | --- |
| User intent is unclear or overloaded with technical guesses | Read `references/requirements-obligations-playbook.md`; start at requirements discovery. |
| Requirements exist but are not traceable or observable | Read `references/requirements-obligations-playbook.md`; normalize requirements and write abstract obligations. |
| MVP scope may be fake, toy, or drift-prone | Read `references/requirements-obligations-playbook.md`; run MVP and drift review. |
| Architecture, dependencies, fork-vs-build, or bespoke-code scope is undecided | Read `references/architecture-minimization-playbook.md`. |
| A concrete plan exists but tests/proof obligations are missing | Read `references/testing-implementation-qc-playbook.md`; start at implementation-specific obligations. |
| Tests exist but may be tautological, mocked, snapshot-only, or overfit | Read `references/testing-implementation-qc-playbook.md`; run test adequacy. |
| Implementation is requested after accepted tests and plan | Read `references/testing-implementation-qc-playbook.md`; enforce implementation constraints. |
| QC findings, slop findings, or remediation are in scope | Read `references/testing-implementation-qc-playbook.md`; triage before fixing. |
| Commit, push, PR, CI, or review comments are in scope | Read `references/commit-pr-routing-playbook.md`. |
| Artifact names, IDs, state schema, or traceability edges are needed | Read `references/artifact-traceability-schema.md`. |

For external standards such as ISO requirements engineering, NIST SSDF, OWASP ASVS, or
SLSA, verify the current upstream source before citing exact clauses.
Use them as external contract context, not as a substitute for local requirements.

## State Machine

Use these state names as stable routing labels:

```text
START
  -> REQUIREMENT_DISCOVERY
  -> REQUIREMENT_NORMALIZATION
  -> ABSTRACT_PROOF_OBLIGATIONS
  -> MVP_VIABILITY_PLANNING
  -> PRODUCT_DRIFT_AND_GAMING_REVIEW
  -> ARCHITECTURAL_SURFACE_MINIMIZATION
  -> IMPLEMENTATION_PATH_DECISION
  -> CONCRETE_IMPLEMENTATION_PLANNING
  -> SECOND_SURFACE_MINIMIZATION
  -> IMPLEMENTATION_SPECIFIC_OBLIGATIONS
  -> TEST_DESIGN
  -> TEST_ADEQUACY_REVIEW
  -> IMPLEMENTATION
  -> ANTI_GAMING_AND_SCOPE_AUDIT
  -> LOCAL_QC
  -> GLOBAL_QC
  -> QC_TRIAGE
  -> REMEDIATION_OR_EXCEPTION
  -> COMMIT
  -> PUSH_OR_PR
  -> PR_CI_AND_REVIEW
  -> PR_TRIAGE_AND_REMEDIATION
  -> DONE
```

Backward edges are mandatory when evidence fails.
Examples:

- An ambiguous MVP requirement routes to `REQUIREMENT_DISCOVERY`.
- A gamed or toy MVP routes to `MVP_VIABILITY_PLANNING`.
- A bespoke module without dependency survey evidence routes to
  `ARCHITECTURAL_SURFACE_MINIMIZATION`.
- A weak test routes to `TEST_DESIGN`.
- A suspicious implementation diff routes to `CONCRETE_IMPLEMENTATION_PLANNING` or
  `SECOND_SURFACE_MINIMIZATION`.
- A true QC or PR finding routes to `REMEDIATION_OR_EXCEPTION`.

## Independence Rule

Keep authorship independent whenever the workflow is nontrivial:

```text
requirement normalizer != obligation writer
obligation writer != test designer
test designer != implementation agent
implementation agent != adequacy/scope/QC reviewer
QC triage reviewer != remediation agent
```

If one person or agent must perform multiple roles, preserve separation by committing or
freezing each artifact before moving to the next role, then re-read the frozen artifact
as input rather than editing it opportunistically.

## Core Routing Rules

- Treat technical requests from users as hypotheses unless they are stated operational
  constraints.
- Keep proof obligations implementation-agnostic until architecture is selected.
- In GitHub-externalized work, proof obligations normally live in the owning story or
  feature issue body as definition-of-done material. Split a proof obligation into a
  child issue only when it is independently trackable, reviewable, or implementable.
  Tests, checks, screenshots, logs, CI runs, and artifacts are evidence for obligations,
  not obligations themselves.
- For every nontrivial behavior, ask why local code should exist at all.
- Delegating behavior to a dependency transfers implementation burden upstream but
  keeps local obligations for integration, versioning, configuration, and user-visible
  expectations.
- Do not use mocks, fakes, smoke checks, snapshots, status labels, or existence checks as
  proof of product behavior.
- Do not allow implementation agents to edit tests, obligations, fixtures, or
  requirements without a formal backward route.
- Do not treat QC reports, issues, comments, labels, PR metadata, or artifact existence
  as completion of implementation or proof obligations.
- For significant changes to existing implementation, route through branch, PR, CI,
  review, triage, and remediation.

## Default Artifact Location

Use the repository's existing planning/artifact convention.
If none exists, place agent-facing workflow artifacts under:

```text
.agents/proof-obligation-workflow/
```

Do not scatter requirements, obligations, plans, QC reports, and PR triage notes across
unrelated paths.
See `references/artifact-traceability-schema.md` for the artifact list and traceability
edges.

## Done Gate

A change is done only when the relevant traceability graph is closed:

- accepted MVP requirements have abstract obligations;
- abstract obligations map to implementation obligations, dependency-contract evidence,
  or explicit deferrals;
- tests or approved non-test evidence map to implementation obligations;
- tests passed adequacy review;
- implementation stayed within the plan and owned-surface ledger;
- local and global QC findings are triaged;
- true positives are remediated;
- systemic false positives are escalated upstream;
- commits or PRs record requirement, obligation, test, and QC anchors.

If any required edge is missing, report the missing edge as the live work item.
Do not call the workflow complete.
