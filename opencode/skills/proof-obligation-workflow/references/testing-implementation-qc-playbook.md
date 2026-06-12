# Testing, Implementation, and QC Playbook

Read this reference for implementation-specific obligations, test design, test adequacy,
implementation constraints, scope audits, QC, triage, and remediation.

## Implementation-Specific Obligations

Use `Implementation Obligation Writer` mode after concrete planning and second
minimization.
Write obligations specific enough to guide tests, but do not write tests or production
code in this role.

Use this schema:

```yaml
id: IOB-001
abstract_refs:
implementation_component:
statement:
preconditions:
inputs:
expected_outputs:
state_transitions:
error_behavior:
security_behavior:
delegated_behavior:
local_behavior:
evidence_required:
test_refs: []
```

Gate:

- every MVP abstract obligation maps to one or more implementation obligations,
  dependency-contract obligations, or explicit deferrals;
- every implementation obligation identifies local behavior versus delegated behavior.

## Test Design

Use `Test Designer` mode after implementation obligations are frozen.
Load `test-guidelines` and `policy-index/references/test-proof-rules.md`.

Allowed evidence classes include unit, integration, contract, end-to-end, golden,
property-based, fuzz, migration, accessibility, performance, security regression, and
manual demo evidence.
Do not use mocks, fakes, stubs, smoke checks, snapshot-only assertions, visibility-only
assertions, or existence-only checks as proof.

Use this schema in `testing/test-plan.yaml`:

```yaml
id: TEST-001
obligation_refs:
test_type:
test_file:
fixture:
setup:
action:
assertions:
negative_assertions:
failure_mode_caught:
why_this_test_is_not_tautological:
```

Maintain a coverage matrix:

```yaml
IOB-001:
  tests:
    - TEST-001
  evidence:
    - integration
  uncovered_edges: []
```

For every nontrivial obligation, include a proof route that would fail under a plausible
bad implementation.
Examples: wrong insertion point, lost surrounding text, hard-coded fixture, duplicate
import, unescaped shell argument, schema migration data loss, cancellation mutating
state.

Gate:

- every MVP implementation obligation has meaningful test evidence or an explicit
  non-test evidence route.

## Test Adequacy

Use `Test Adequacy Auditor` mode before implementation begins.
The auditor must not implement production code.

Ask:

- does each test map to a real obligation;
- does each obligation have meaningful evidence;
- could a trivial, hard-coded, mocked, or fixture-specific implementation pass;
- could functionality be deleted while tests stay green;
- are tests asserting behavior instead of implementation trivia;
- are dependency contracts tested at the owned boundary;
- are snapshots paired with semantic assertions;
- are there orphan tests.

Where practical, propose or run small mutations such as changing insertion position,
dropping escaping, ignoring cancellation, returning empty results, skipping persistence,
or hard-coding fixture names.
Meaningful tests should fail under those mutations.

Write `testing/test-adequacy-report.md`.

Gate:

- implementation cannot begin until adequacy passes;
- inadequacy routes to `TEST_DESIGN`.

## Implementation

Use `Implementation Agent` mode only after accepted tests, obligations, plan, and ledger
exist.

The implementer may write production code, small internal helpers, and minimal
supporting docs required by the plan.

The implementer must not:

- edit obligations;
- edit tests or fixtures;
- skip or weaken tests;
- add hidden test-specific branches;
- expand bespoke code beyond the plan;
- add dependencies without routing through minimization review;
- change user-facing behavior without requirements/obligation reroute.

Prefer thin adapters, declarative configuration, dependency-owned behavior, small pure
functions, explicit boundaries, typed schemas, simple state machines, and contract
boundaries around external tools.

Avoid custom parsers, layout engines, auth, crypto, sync, serialization formats, shell
construction, unbounded background behavior, and large manager classes unless explicitly
justified by the surface minimization record.

Gate:

- accepted tests pass without modifying tests, fixtures, or obligations.

## Anti-Gaming and Scope Audit

Use `Implementation Scope Auditor` mode after implementation.
Classify every changed file:

- planned production code;
- planned test code;
- generated artifact;
- documentation;
- unplanned production code;
- unplanned dependency/config;
- suspicious test change.

Check for:

- test edits, skipped tests, weakened fixtures, or hidden test-specific branches;
- sample-data hard-coding;
- unplanned bespoke code;
- unreviewed dependencies;
- owned-surface budget violations;
- silent architecture changes;
- tests passing while canonical scenarios fail.

Write `qc/implementation-diff-audit.md`.

Gate:

- unplanned nontrivial production code routes to concrete planning or second
  minimization;
- suspicious test changes route to test design and adequacy review.

## Local and Global QC

Use `Local QC Runner` mode for deterministic repo checks through the repository's
declared `just` recipes.
Do not invent narrower local QC as proof.

Typical evidence:

- format;
- lint;
- typecheck;
- tests;
- build/package;
- dead code;
- dependency/license/secret checks;
- static analysis;
- migration/performance/accessibility checks when owned by the project.

Write `qc/qc-local-report.json` if the workflow uses persisted QC artifacts.

Use `Global QC Runner` mode for standardized independent AI QC:

- anti-slop review;
- requirements traceability review;
- owned-surface review;
- security-policy review;
- test-quality review;
- dependency-risk review;
- PR-readiness review.

Write `qc/qc-global-report.json`.

Gate:

- findings route to triage; a reviewer finding is not automatically true.

## QC Triage

Use `QC Triage Reviewer` mode with fresh context.
Load policy and threat-model inputs before classifying.

Use this schema in `qc/qc-triage.md`:

```yaml
id:
source:
finding:
classification: true_positive | false_positive | unclear
policy_basis:
evidence:
affected_files:
severity:
recommended_route:
```

A true positive violates requirements, obligations, implementation plan,
owned-surface ledger, security policy, repository policy, test adequacy policy, QC
policy, or PR guidelines.

A false positive is factually wrong, policy-misaligned, threat-model-inapplicable,
already delegated upstream, contradicted by requirements, or asking for unnecessary
bespoke code.

Gate:

- all findings are classified;
- true positives route to remediation;
- unclear findings route to human or policy clarification;
- systemic false positives become upstream QC issues rather than local suppressions.

For systemic global-QC false positives, write `qc/upstream-qc-issue.md` with:

```yaml
title:
summary:
finding_text:
code_or_diff_that_triggered_it:
app_threat_model:
local_policy_context:
global_policy_clause:
why_the_finding_is_wrong:
why_this_is_systemic:
proposed_policy_change:
minimal_reproduction:
```

## Remediation

Use `Remediation Agent` mode only after triage assigns specific true positives.
Load `fixing-slop` and, when assigned by policy code, fixer-side remediation references.

The remediation agent must:

- make the minimal correction that satisfies the original obligation;
- preserve green tests;
- add a regression/proof test if the issue exposed an unproved owned behavior;
- update obligations only through formal reroute;
- rerun local QC and relevant global QC.

The remediation agent must not:

- delete or weaken tests;
- silence warnings without policy basis;
- expand bespoke code beyond plan;
- add dependencies without minimization reroute;
- convert the finding into documentation-only completion.

Write `qc/remediation-report.md` only when the workflow persists remediation artifacts.
Then route back to scope audit or QC.
