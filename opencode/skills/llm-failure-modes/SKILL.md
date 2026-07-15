---
name: llm-failure-modes
description: Use when reasoning through a complex or high-stakes problem to check for common LLM cognitive failures.
metadata:
  author: dzack
  version: '0.3.0'
---
# LLM Failure Modes

> **Privacy note:** This document is a public-facing skill file.
> Examples grounded in real engineering or technical problems are fine — a misconfigured
> file watcher or a broken CI step is not sensitive.
> What must be avoided: personal details, account or system identifiers, verbatim
> session excerpts that would identify a specific person or interaction, and any
> narrative that reads as a story about a particular individual rather than a class of
> agent behavior.

## Editorial Guidelines

When contributing to this document:

- **Objective failures only.** Describe what happens; do not posit why or attribute
  motivations. “Agents assert authority before investigation” — not “Agents assert
  authority *to save face*.”

- **General, not interaction-specific.** These are properties of model behavior
  observable in any interaction — with humans, other models, or automated scripts.
  Write “agents” not “the agent”; write “when a claim is made” not “when the user says.”
  The other party in any documented failure could be anything.

- **Examples over observables.** A concrete example illustrates a failure pattern more
  reliably than an abstract “Observable:” clause, which tends to restate the definition.
  Show what the failure looks like in actual output.

- **Intrinsic, not reactive.** Behaviors like goal substitution or authority assertion
  are not responses to a particular kind of interlocutor — they are properties of model
  behavior that emerge regardless of what the other party is.
  Do not frame them as reactions to human behavior specifically.

## Contents

This skill is organized into focused subfiles.
Load the relevant section for your context:

### Reasoning and Epistemic Failures

- **Formal cognitive failures** — [cognitive-failures.md](cognitive-failures.md)
  Constraint hallucination, citation without comprehension, internal incoherence,
  confabulation, sunk cost continuation, frame-suppressed self-contradiction,
  confidence-evidence decoupling.
  (10 items)

- **Conversational and epistemic failure modes** —
  [conversational-failures.md](conversational-failures.md) Authority assertion without
  grounding, investigation theater, anomaly normalization, goal substitution, correction
  weight insensitivity, CoT-output deception, local minimum lock, confidence floor
  invariance. (23 items)

### Investigation and Diagnosis

- **Investigation and diagnostic failures** —
  [investigation-failures.md](investigation-failures.md) Premature solution generation,
  thrashing, question dissolution, verification theater, tool output blindness,
  unfalsified external attribution, concept label substitution, analysis-action
  concurrency, prior-shaped inspection, local-artifact laundering, reverse-engineering
  before lookup. (17 items)

- **Self-evaluation and introspection failures** —
  [introspection-failures.md](introspection-failures.md) Attribution error, narrative
  scrubbing, structural inability to state incorrectness, introspective depth ceiling,
  absent self-model of failure modes.
  (7 items)

- **Charlie behaviour** — [charlie-behaviour.md](charlie-behaviour.md) Agreement without
  tracking, self-reference failure, frame drift, escalating agreement without
  resolution, third-party deflection, multi-agent cascade.
  (9 items)

### Testing, Review, and Code Quality

- **Testing and verification failures** — [testing-failures.md](testing-failures.md)
  Content-free verification, tautological testing, instrumental deception, test-cheat
  escalation ladder (7 sub-tactics).
  (8 items)

- **Jerry behaviour** — [jerry-behaviour.md](jerry-behaviour.md) Paraphrase-as-review,
  checklist theater, fluency bias, evidence-shaped evidence, consensus-as-evidence,
  self-certification, circular validation loop.
  (10 items)

- **Distilled agentic coding failure modes** — [coding-failures.md](coding-failures.md)
  Scope explosion, specification drift, slop accretion, critic hallucination, outcome
  blindness in review, failure mode inversion, impact miscalibration, replacement
  instinct, reimplementation impulse, dependency aversion bias, meta-artifact
  delegation, scale-complexity confusion, ground-up bias (churn-first workflow),
  fallback-legacy compulsion (asymmetric risk model), availability-first tool reuse,
  workflow phase collapse, state-channel proliferation, abstraction rebound after
  simplification.
  (24 items)

- **Documentation and frame-contamination failures** —
  [documentation-failures.md](documentation-failures.md) Private-context leakage,
  naming-as-existence, audience collapse, disclosure substitution, correction-history
  leakage, control-payload inversion, circular doctrine, and reviewer frame capture.
  (15 items)

- **Agent cognitive-distortion index** —
  [references/agent-distortion-index.md](references/agent-distortion-index.md) Compact
  shorthand (R/T/L/O/C/V codes) for the distortions that produce slop in documents, plans,
  schemas, and project structure, plus the reviewer-infection failure modes to watch for in
  your own analysis. Use the codes to label findings; keep report vocabulary neutral.
  (60 codes + composite clusters)

### Structural and Behavioral Observations

- **Structural and optimization failures** —
  [structural-failures.md](structural-failures.md) Fake success blocks debugging,
  root-cause evasion, self-authored debris, wrapper slop, context loss.
  (7 items)

- **Observed in the field** — [field-observations.md](field-observations.md) Spaghetti
  shotgun, plausible fixture injection, checker removal, deep-context quality collapse,
  progress theater, refactoring to the mean, hot-path defensive programming, helper
  function explosion, partial contract grounding.
  (33 items)

- **Behavioral detection methodology** —
  [references/behavioral-detection-methodology.md](references/behavioral-detection-methodology.md)
  Concrete anchors and review tactics for identifying behavioral failures without
  turning observations into interaction-specific narratives.

### Cross-References

- [[addressing-shallow-work/SKILL|addressing-shallow-work]] → Load alongside when investigating failure modes that
  produce structurally wrong code.
  The inability to recognize when an approach is structurally incapable of correctness —
  even without empirical verification — is a failure mode distinct from “didn’t test
  enough.” The regex-on-HTML example (flattening a semantic tree into bytes before
  searching) illustrates fluency masking structural wrongness.

- [[anti-slop/SKILL|anti-slop]] → Load alongside when the failure mode produces surface-level quality
  issues (generic names, boilerplate) alongside deeper epistemic failures.
  Surface patterns often mask the structural wrongness cataloged here.
  All implementation work influenced by this skill is subject to the
  [[policy-index/SKILL#policy-registry|Bridge-Burning Policies]]
  in `policy-index/SKILL.md` as non-negotiable hard constraints — no runtime defaults,
  fallbacks, mocks, or optional critical dependencies.

- **[[reviewing-llm-code/SKILL|reviewing-llm-code]] pattern catalog** →
  [../reviewing-llm-code/references/pattern-catalog.md](../reviewing-llm-code/references/pattern-catalog.md)
  is the canonical catalog for concrete code, test, QC, and documentation patterns that
  instantiate these failure modes.
  Use it when the failure mode appears in artifacts: regex against semantic formats,
  developer-controlled assertions, fallback laundering, no-op behavior, QC appeasement
  code, and recipe bypasses.

- [[reviewing-subagent-work/SKILL|reviewing-subagent-work]] → Load alongside when designing review processes that must
  detect the failures cataloged in this skill.
  The Synthesis Gate forces content-level evaluation; structural-wrongness recognition
  is its prerequisite gate.
