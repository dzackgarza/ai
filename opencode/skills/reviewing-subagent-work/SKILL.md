---
name: reviewing-subagent-work
description: Use when reviewing or evaluating work produced by another LLM/agent. Forces task-value reasoning and routes to detailed failure-mode knowledge.
---
# Reviewing Subagent Work

When reviewing work produced by another LLM or agent, produce this statement BEFORE
concluding your review:

## Synthesis Gate

**“The subagent’s work proves _____ about the task’s correctness, based on this specific
evidence: _____.”**

If you cannot fill both blanks with concrete content (line numbers, specific values,
external cross-checks), you have not reviewed the work — you have verified that activity
occurred. File existence, hash matches, and the worker’s own success claims are not
evidence of correctness.
They are evidence that something was written.

The user would not spend tokens on work they can do instantly.
If your review could have been produced without reading the artifact’s content, it is
not a review.

## Why Self-Reports Are Worse Than Noise

Worker self-reports are not merely unreliable — they are **structurally biased toward
approval**:

- “Files exist” proves only that something was written

- “Hashes match” proves only that written files reference the inputs

- “The worker says it checked X” proves only that the worker knows what a good report
  should say

- None of this proves the work is correct, useful, or intelligent

The worker knows what a successful report *looks like* and will produce that report
regardless of actual work quality.
In contexts where hallucination/confabulation is the failure mode being checked for, the
worker’s self-report is **the artifact under review, not evidence about the artifact**.

This is not just low-signal; it is structurally biased toward approving shallow work.
Trusting it creates a circular validation loop: LLM validates LLM validates LLM.

## Shared Frames Are Not Independent Evidence

Multiple agents exposed to the same prompt, transcript, README, plan, or generated
doctrine are one contaminated witness until proven otherwise. Agreement is not
corroboration; it may only show that the same frame was copied.

When the artifact under review uses project-created terms, internal status labels, or
cross-references to generated artifacts, keep two ledgers:

- Observed reality: files, code, data, commands, outputs, external sources, and
  user-visible behavior actually inspected.
- Project narrative: names, roles, statuses, doctrine, plans, and claims asserted by
  agents or docs.

Never move a claim from narrative to reality because several agents repeat it,
formalize it, or mark it confirmed.

## What Real Review Requires

Before concluding, your review MUST contain:

- Specific findings from actual content (line numbers, concrete values)

- Quality assessment of the work itself (not just that it exists)

- Problems found, or explicit statement of what you verified and how

If your review could have been written without reading the artifact → you didn’t review
it.

## Routing: Detecting Shallow Work

After answering the forcing questions, assess whether the subagent’s output shows these
patterns:

- Contains no specific findings (no line numbers, no concrete values, no external
  cross-checks)

- Paraphrases the task description instead of showing results

- Self-reports effort ("I analyzed carefully") without evidence of that analysis

- Lists what *could* be checked without actually checking

- **Structurally wrong at the abstraction level** — the approach destroys the
  abstraction before operating (e.g., regex-on-HTML where semantic DOM selectors exist).
  This can be recognized without data or execution; see [[addressing-shallow-work/SKILL|addressing-shallow-work]] →
  “Recognizing Structurally Wrong Code”.

If the output shows these patterns → LOAD [[addressing-shallow-work/SKILL|addressing-shallow-work]] skill before
proposing any fixes.
Do not respond to shallow work by adding more structure — that makes it worse.

## Deletion Does Not Prove Correction

When reviewing another agent’s fix, do not treat removal of criticized code as proof that
the problem was solved.

Ask:
- What did the deleted code/test/doc claim to do?
- Was that claim still required?
- Is there a replacement?
- Did the task’s acceptance standard change visibly?
- Did the agent merely remove the evidence that the requirement was unmet?

A cleanup diff can be a stronger deception than an additive diff.

## Reviewing Review Feedback

A review comment from another agent is itself an artifact under review.
Do not trust the reviewer’s framing, severity, or proposed fix.

Apply [[pr-feedback-triage/SKILL|pr-feedback-triage]]:
- Is the underlying claim true?
- Is the suggested remediation policy-compatible?
- What evidence would falsify either?

## Reviewing Review-Remediation Subagents

When a subagent was assigned to remediate accepted PR feedback, review it against the remediation spec, not the original review comment.

Reject if:
- it patched the exact symptom but did not discharge the proof burden;
- it introduced banned test shapes;
- it added fail-open runtime branches;
- it deleted or renamed slop without burden disposition;
- it used the reviewer’s wording as an implementation target;
- it produced a commit that cannot be mapped to the spec’s invariants.

## Cross-References

- **jerry-behaviour** → LOAD alongside when reviewing agent output and you suspect the
  evaluation itself is shallow.
  Catalogs Checklist Theater, Paraphrase-as-Review, Consensus-as-Evidence, and other
  patterns where evaluators produce the appearance of oversight without epistemic
  independence.

- [[addressing-shallow-work/SKILL|addressing-shallow-work]] → LOAD alongside when you need to fix a process that
  produced shallow output.
  Provides structural-scrutiny patterns for detecting and correcting work that satisfies
  format without satisfying intent.

- [[reviewing-llm-code/SKILL|reviewing-llm-code]] → LOAD alongside when the subagent produced code, tests, QC, or
  documentation. Provides the canonical pattern catalog for LLM code artifacts and the
  review procedure. Do not review code without loading this skill first.

- [[anti-slop/SKILL|anti-slop]] → LOAD alongside when the subagent output shows generated-code residue:
  generic wrappers, no-op UI, debug debris, boilerplate, or local patches with no real
  abstraction. Provides the Dependency Inversion Rule and structural analysis frame.
  Reviewing subagent work MUST check compliance with the
  [[policy-index/SKILL#policy-registry|Bridge-Burning Policies]]
  in `policy-index/SKILL.md` — these are non-negotiable hard constraints. Any subagent
  output containing runtime defaults, fallbacks, mocks, or optional critical
  dependencies MUST be rejected.

- [[llm-failure-modes/SKILL|llm-failure-modes]] → LOAD alongside when you need to name the specific cognitive
  failure mode that produced the shallow work (goal substitution, overconfidence,
  confabulation, replacement instinct, dependency aversion bias, meta-artifact
  delegation, scale-complexity confusion).

- [[test-guidelines/SKILL|test-guidelines]] → LOAD alongside when reviewing subagent-produced tests, QC, smoke
  checks, CI, or proof surfaces.

- [[thermo-nuclear-code-quality-review/SKILL|thermo-nuclear-code-quality-review]] → LOAD alongside when the subagent output shows
  maintainability, architecture, or abstraction problems (giant files, spaghetti
  condition growth, premature abstraction).
