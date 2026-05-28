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
  This can be recognized without data or execution; see `addressing-shallow-work` →
  “Recognizing Structurally Wrong Code”.

If the output shows these patterns → LOAD `addressing-shallow-work` skill before
proposing any fixes.
Do not respond to shallow work by adding more structure — that makes it worse.

## Cross-References

- **jerry-behaviour** → LOAD alongside when reviewing agent output and you suspect the
  evaluation itself is shallow.
  Catalogs Checklist Theater, Paraphrase-as-Review, Consensus-as-Evidence, and other
  patterns where evaluators produce the appearance of oversight without epistemic
  independence.

- **addressing-shallow-work** → LOAD alongside when you need to fix a process that
  produced shallow output.
  Provides structural-scrutiny patterns for detecting and correcting work that satisfies
  format without satisfying intent.

- **reviewing-llm-code** → LOAD alongside when the subagent produced code, tests, QC, or
  documentation. Provides the canonical pattern catalog for LLM code artifacts and the
  review procedure. Do not review code without loading this skill first.

- **anti-slop** → LOAD alongside when the subagent output shows generated-code residue:
  generic wrappers, no-op UI, debug debris, boilerplate, or local patches with no real
  abstraction. Provides the Dependency Inversion Rule and structural analysis frame.

- **llm-failure-modes** → LOAD alongside when you need to name the specific cognitive
  failure mode that produced the shallow work (goal substitution, overconfidence,
  confabulation, replacement instinct, dependency aversion bias, meta-artifact
  delegation, scale-complexity confusion).

- **test-guidelines** → LOAD alongside when reviewing subagent-produced tests, QC, smoke
  checks, CI, or proof surfaces.

- **thermo-nuclear-code-quality-review** → LOAD alongside when the subagent output shows
  maintainability, architecture, or abstraction problems (giant files, spaghetti
  condition growth, premature abstraction).
