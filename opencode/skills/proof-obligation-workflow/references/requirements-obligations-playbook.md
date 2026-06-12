# Requirements and Obligations Playbook

Read this reference for requirement discovery, normalization, abstract proof obligations,
MVP viability, and drift/gaming review.

## Requirement Discovery

Use `Requirements Interviewer` mode when user intent is still raw.
Extract user-facing outcomes, not implementation choices.

Distinguish:

- essential user outcome;
- current workaround;
- incidental UI detail;
- technical guess;
- hard external constraint;
- personal preference.

Elicit:

- job-to-be-done;
- current workflow as evidence, not specification;
- one happy path, one messy common path, and one failure path;
- domain objects, source of truth, lifecycle, sensitive fields, and validation rules;
- invariants that must always hold;
- failure costs: annoying, recoverable, expensive, dangerous, compliance-relevant, or
  trust-destroying;
- permissions, trust, data boundaries, internet/API/cloud constraints;
- interaction expectations: CLI, GUI, plugin, editor, daemon, batch, review step;
- non-goals;
- MVP cut line: what must be real from day one and what can be manual.
- acceptance statements in the user's terms.

For each domain object, capture:

```yaml
name:
user_definition:
aliases:
source_of_truth:
who_can_create:
who_can_edit:
who_can_delete:
lifetime:
sensitive_fields:
validation_rules:
```

Write:

- `requirements/requirements-dossier.md`
- `requirements/domain-glossary.md`
- `requirements/canonical-scenarios.yaml`

Gate:

- every requirement is accepted for MVP, accepted but deferred, rejected/non-goal, open
  question, or assumption needing validation;
- unresolved ambiguity affecting MVP routes back to the user;
- future-only ambiguity is recorded as deferred.

## Requirement Normalization

Use `Requirements Normalizer` mode after raw interviews exist.
Convert source material into observable, nontechnical requirements.

Reject implementation-shaped requirements unless they are real constraints:

```text
Bad: Use SQLite.
Good: Preserve notes across restarts without requiring network access.
```

Use this schema:

```yaml
id: REQ-USER-001
title:
user_story:
source_quote_or_scenario:
priority: must | should | could | deferred
mvp_status: in | out | partial
domain_objects:
preconditions:
expected_behavior:
unacceptable_behavior:
observability:
risk_if_wrong:
open_questions:
```

Normalize by:

- splitting compound statements;
- removing technical guesses unless they are genuine constraints;
- classifying requirements as functional, data integrity, UX/interaction,
  interoperability, performance, availability/reliability, privacy/security,
  auditability, migration/portability, installation/packaging, or maintainability;
- identifying conflicts;
- adding hidden standard requirements when normal app behavior implies them.

Gate:

- every MVP requirement has observable behavior, priority, risk if wrong, and at least
  one scenario or rationale.

## Abstract Proof Obligations

Use `Abstract Obligation Writer` mode after normalized requirements are accepted.
Write implementation-independent propositions that can be evidenced by tests, analysis,
review, upstream contracts, manual validation, static analysis, or benchmarks.

Use this schema:

```yaml
id: AOB-001
title:
statement:
requirement_refs:
kind: functional | invariant | safety | liveness | UX | data | security | privacy | performance | interoperability | recovery | standard-app-surface
scope: MVP | post-MVP | always
preconditions:
allowed_behaviors:
forbidden_behaviors:
evidence_required:
  - test
  - review
  - dependency-contract
  - manual-demo
  - static-analysis
  - benchmark
oracle:
edge_cases:
risk_if_unmet:
```

Obligation classes:

- functional behavior the user can perform;
- data integrity and transformation invariants;
- idempotence and reversibility;
- failure and recovery;
- UX cancellation, undo, settings, accessibility, and expected app behavior;
- privacy and threat-model-gated security;
- performance on representative data;
- declared interoperability;
- standard app surface;
- negative obligations that forbid harmful behavior;
- anti-overfit obligations that prevent fixture hard-coding or toy MVP success.

Gate:

- every accepted MVP requirement has at least one abstract obligation;
- every abstract obligation has a requirement, standard-app-surface rule, dependency-risk
  rule, or explicit architectural rationale;
- no orphan obligation exists unless marked as baseline product/security behavior.

## MVP Viability

Use `MVP Planner` mode to select the thinnest vertical slice that proves viability.
An MVP may be ugly or partially manual, but it must exercise the real risk-bearing path.

Include:

- one core happy path;
- one realistic messy path;
- one important failure path;
- one persistence or recovery path when the app owns state;
- one integration path when external tools are central.

Mocking is allowed only when it does not invalidate the viability claim.
Do not mock the boundary that carries the core product risk.

Use this schema:

```yaml
mvp_goal:
included_requirements:
excluded_requirements:
canonical_scenarios:
must_be_real:
may_be_fake_or_manual:
known_shortcuts:
drift_risks:
validation_demo:
success_criteria:
failure_criteria:
```

Also create `standard-app-surface-checklist.yaml` covering install/run instructions,
configuration path, save/recovery, cancellation/undo, clear errors, logging, empty and
loading states, accessibility where relevant, import/export, migration, and dependency
availability.

Gate:

- the MVP would fail if the core product claim were false.

## Drift and Gaming Review

Use `Drift/Gaming Reviewer` mode before architecture work.
Adversarially ask whether an implementation could satisfy the obligations while failing
the user's goal.

Check for:

- hard-coded fixtures;
- test-passing but product-failing behavior;
- critical behavior hidden in manual steps;
- avoided integration risk;
- impressive framework use without workflow proof;
- narrowed input space below user expectation;
- omitted standard app behavior.

Write `planning/drift-risk-register.md` entries:

```yaml
id:
description:
affected_requirements:
how_it_could_game_the_process:
additional_obligation_or_test_needed:
severity:
```

Gate:

- every high-severity drift risk is handled by a new abstract obligation, MVP
  adjustment, explicit deferral, user-visible assumption, or architecture constraint.
