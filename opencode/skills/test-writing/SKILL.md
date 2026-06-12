---
name: test-writing
description: >-
  Use when a project has no tests, QC reports missing tests, proof obligations need to
  be designed before implementation, or an agent believes an existing test may be wrong.
  This skill defines the mandatory subagent workflow for creating real proof-bearing
  tests before application fixes.
---
# Test Writing

Use this skill when the problem is not a single failing test, but the absence or
trustworthiness of proof-bearing tests.

Missing tests are a design failure, not a routine QC failure. Do not patch application
code, add placeholder tests, weaken QC, or route the issue through generic slop triage
until the proof obligations have been defined and locked in.

## Required Companion Skills

Load these before acting:

- `test-guidelines` for testing epistemology, banned test shapes, no mocks, and proof
  standards.
- `test-driven-development` for the red-green audit trail.
- `subagent-delegation` for constructing and reviewing subagent work.
- Domain skills for the repository language or framework.

## Missing-Test Workflow

When QC reports that a project has source code but no tests:

- Spawn a proof-obligation subagent.
  The subagent identifies the behaviors the repository owns, the real user-visible or
  system boundaries to exercise, the fixtures or real data required, and the assertions
  that would prove those behaviors.
  It must not write tests.

- Review the proof obligations.
  Reject obligations that prove implementation details, source text, tool policy,
  constructor existence, mocks, tautologies, or generic coverage.
  Keep only obligations tied to real behavior the repository owns.

- Spawn a separate test-writing subagent.
  The subagent writes tests from the approved proof obligations, runs them, confirms
  they fail for the expected reason, and commits the red tests.
  Red tests are the audit trail proving the missing behavior is observable.

- The main agent fixes the application.
  After red tests are committed, the main agent may change application code until the
  tests pass, using the repository's normal `just test` route for final QC.

- Preserve the test/app authority boundary.
  The main agent may not edit those tests merely because they fail.

## If a Test Looks Wrong

If the main agent believes a locked-in test is incorrect, it is not authorized to edit
the test or direct a fixer subagent to edit it.

Required procedure:

- Ask the same test-writing subagent for a verdict when that session is available.
- If it is not available, spawn a fresh neutral subagent primed on all project policies,
  `test-writing`, and `test-guidelines`.
- Give the neutral subagent the test, observed behavior, relevant product/domain facts,
  and command output. Do not frame the prompt as "the test is wrong" or "please fix the
  test."
- Require a verdict: app should change, test should change, or more evidence is needed.
- If the verdict says the test should change, the validating subagent may update the
  test and must explain why the original proof obligation was invalid.
- If the verdict says the app should change, the main agent changes the app.

## Test Quality Standard

Tests must prove behavior through real execution:

- Exercise real code paths and owned boundaries.
- Use real fixtures, captured data, or deterministic local resources.
- Assert semantic outcomes and side effects.
- Fail before the application change for the expected reason.
- Avoid mocks, fake services, synthetic success signals, string-only source inspection,
  tautological assertions, and coverage theater.

If the proof cannot be made real yet, report the missing boundary or fixture as the
blocker. Do not substitute a mock or meta-test.
