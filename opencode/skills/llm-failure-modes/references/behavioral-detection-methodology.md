# Behavioral Detection Methodology

Behavioral failure detection must be evidence-based.
Do not classify an agent by surface language alone; classify it by the relation between
directive, action, evidence, and output.

## Required Evidence

- The exact directive or claim being evaluated.

- The concrete action or artifact produced in response.

- The evidence that the action satisfied, contradicted, or substituted for the
  directive.

- Any competing explanation that was ruled out.

## Anti-Gaming Principle

Behavioral tests should hide or vary the property that matters.
Visible examples are useful only when paired with adversarial or property-based checks
that force a general solution.
A test that can be passed by hard-coded fixtures, keyword matching, or output-shaped
compliance is not a competence test.

## Review Principle

Reviews of agent work must judge semantic correctness.
Agent self-reports, hashes, file existence, line counts, and checklist-shaped text are
activity evidence, not correctness evidence.

## Debugging Principle

Adversarial debugging evaluations should include red herrings and require explicit
hypothesis elimination.
A correct result should identify why the obvious suspect is not the cause and name the
concrete evidence for the actual defect.

## Concrete Anchoring Examples

Use these as patterns when designing evaluations or reviewing agent behavior.
They are intentionally class-level examples, not transcripts.

- **Reflexive agreement:** An agent first agrees with a correction, then continues from
  the pre-correction plan.
  The evidence is the post-correction action, not the agreement language.

- **Confidence inflation:** A speculative cause, an evidence-compatible hypothesis, and
  an established fact are all reported with identical certainty.
  Require explicit source and confidence separation.

- **Task completion bias:** A task is declared complete when a visible artifact exists,
  even though the artifact does not satisfy the stated directive.
  Completion requires matching the user-visible outcome, not producing an activity
  trace.

- **Context fabrication:** An agent fills in missing architecture with plausible
  implementation details.
  Require file, line, command, or source evidence for every concrete implementation
  claim.

- **Fake research gaming:** An agent cites “research” or “best practice” after reading
  only local summaries or stale notes.
  Require the cited source to support the exact claim being used.

- **Commentary gaming:** An agent writes persuasive commentary about test intent while
  the test body checks only shape, existence, or known visible examples.
  Review the assertion semantics, not the explanation.

- **Try/except success laundering:** A test treats any exception as proof that
  validation works. The test must assert the repository-owned failure type or public
  error contract, and must fail if the wrong exception or no exception is produced.

- **External-state bypass:** A validation claims success by inspecting local artifacts
  only when the claim is about a remote service, persisted state, or user-visible
  behavior. The evidence must come from the owned boundary.
