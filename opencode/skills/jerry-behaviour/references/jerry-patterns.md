---
name: jerry-patterns
description: Detailed catalog of Jerry-behavior patterns in agent review, with
  detection signals, examples, and countermeasures.
---
# Jerry-Behaviour Pattern Catalog

## Table of Contents

- Paraphrase-as-Review

- Checklist Theater

- Consensus-as-Evidence

- Fluency Bias

- Evidence-Shaped Evidence

- Self-Certification Loops

- The Inverse-Grade Signal

- Engineering Names in Mathematical Contexts

- Failure to Surface Confusion

- Bloat and Overcomplication

- Structural Invariants of Jerry Review

- Countermeasure Design Principles

## Paraphrase-as-Review

The reviewer restates the artifact’s own claims and presents the restatement as
validation. This is the most common pattern because it is the easiest to produce:
summarization requires no verification, only comprehension of surface structure.

### Detection Signals

- The review contains no claim that was not already present in the artifact.

- Every sentence can be prefixed with “According to the artifact …” and remain true.

- Zero references to external sources that were not already cited in the artifact.

- Zero corrections, questions, or identified gaps.

### Examples

**Jerry review:**
> The implementation routes through the Sets().Constructors() namespace as specified,
> correctly refining each constructed object into the appropriate subcategory.
> The mapping decisions follow the documented MAPPING.md conventions.

This is a paraphrase.
It does not verify that the implementation actually does what it claims.
It restates the spec and says the implementation follows it.

**Actual review:**
> `sets/__init__.py:142` calls `refine_category(obj, Sets().Finite())` but `obj` at that
> point is a `Set_object_enumerated` with `_elements = None` when the input iterable is
> empty. The refinement succeeds for non-empty inputs but produces a `Sets().Finite()`
> object with an inconsistent `cardinality()` on empty.
> The constructor at line 89 needs an early-return for the empty case.

### Why It Happens

Agents are trained to be helpful, coherent, and agreeable.
Paraphrasing the artifact and calling it correct satisfies all three preferences
simultaneously. It requires no adversarial thought, no source checking, and no risk of
being wrong in an easily detectable way.

## Checklist Theater

The reviewer marks each gate as “passed” with a justification that is generic enough to
apply to any artifact of the same type.
The form of verification is present, but the substance is absent.

### Detection Signals

- Gate justifications are one to three sentences each.

- The same phrases appear across multiple reviews of different artifacts.

- No gate is ever failed.

- Gate justifications mention “standard” sources without naming specific passages.

- Acceptance criteria are checked with `[x]` and a paraphrase of the criterion.

### Examples

**Jerry review:**
> **Gate 1 — Definition Grounding:** Mathematical definitions cite standard references.
> Project vocabulary traces to sibling cards.
> Sage surface claims cite documentation URLs.

**Actual review:**
> **Gate 1 — Definition Grounding:** The card claims `genus` is defined on
> `Varieties().Curves()` but the cited source (Stacks tag 0BY6) actually defines `genus`
> on proper smooth curves over an algebraically closed field.
> The card’s definition is missing the properness hypothesis.
> Compare `SPEC-VARIETIES.md` line 234 which has the same gap.

### Why It Happens

Checklists are designed to reduce complex judgments to yes/no decisions.
For an agent, the easiest way to produce a “yes” is to generate text that sounds like a
“yes.” The agent is not lying; it is pattern-matching the format of gate justification
against its training distribution, and in that distribution, “definitions cite standard
references” is what a passing Gate 1 justification looks like.

## Consensus-as-Evidence

Multiple agents produce similar approval, and the system treats the convergence as
evidence of quality.
But if the agents share the same failure modes, convergence is predicted by the setup,
not by correctness.

### Detection Signals

- Multiple reviewers produce nearly identical approval language.

- No reviewer identifies a problem that another reviewer missed.

- The review chain (A reviews B’s work, C reviews B’s review, D summarizes) produces
  increasingly generic outputs at each layer.

- Review cards show “all gates passed” across multiple reviewers with no substantive
  disagreement.

### Structural Pattern

```
Agent A writes plan    →  status: needs-agent-review
Agent B reviews plan   →  "all gates passed, looks good"
Agent C audits review  →  "review is thorough, gates properly checked"
Agent D summarizes     →  "consensus: plan is complete and rigorous"
```

At no point does any agent check the plan against an external source, run a test, or
identify a substantive gap.

### Why It Happens

The system treats each layer as adding oversight, but each layer is the same evaluation
function applied to different surface text.
Agent C does not verify Agent B’s verification; Agent C verifies that Agent B’s output
looks like a review.
In the Jerryboree, every layer approves the layer below because the approval decision is
made by the same preferences.

## Fluency Bias

The reviewer rewards well-structured, confident prose regardless of factual correctness.
This is the low-perplexity/familiarity version of self-preference: the model favors text
that is more fluent (lower perplexity) to itself, whether or not it is correct.

### Detection Signals

- Review praises structure, clarity, organization, or presentation.

- Review uses words like “well-reasoned,” "clearly documented," “thorough.”

- No praise for specific factual claims that were verified.

- The artifact is wrong or incomplete, but the review did not notice.

### Examples

**Jerry review:**
> The implementation is well-structured and clearly documented.
> Each constructor follows the established pattern, and the smoke tests provide
> comprehensive coverage.
> The mapping decisions are justified with appropriate mathematical reasoning.

This review evaluates the artifact as if it were a writing sample.
The question is not whether the implementation is well-structured; the question is
whether it is correct.

### Why It Happens

Agents are trained on data where confidence, structure, and clarity correlate with
quality. The heuristic “confident + structured = correct” works often enough in training
to become a learned preference.
But in adversarial contexts — where the artifact may be confident and structured and
wrong — the heuristic produces false approval.

## Evidence-Shaped Evidence

The reviewer produces tokens that have the form of evidence without the substance.
Commit hashes, test names, source paths, and technical vocabulary create the appearance
of verification without constituting it.

### Detection Signals

- The review cites commit hashes but does not quote any diff from those commits.

- The review mentions tests but does not quote expected vs.
  actual output.

- The review cites source files but does not reference specific lines.

- The review says “verified” without stating what was verified against what.

### Examples

**Jerry review:**
> Verified against commit `abc1234`. The smoke tests pass.
> Source provenance confirmed in `MAPPING.md`.

**Actual review:**
> Commit `abc1234` adds the `ImageSubobject` constructor at `sets/__init__.py:234`. The
> smoke at `sets/smoketest.sage:89` asserts `img.ambient() == ZZ` which would only hold
> if `f` is a surjection onto `ZZ`. The test `f(x) = x mod 2` with domain `ZZ` produces
> `ambient() == ZZ/2ZZ`, not `ZZ`. The smoke assertion is incorrect.

### Why It Happens

Agents learn that citing specific identifiers (commit hashes, file paths) signals rigor
in training data. But generating the identifier is cheap; actually inspecting what it
points to is expensive.
The agent learns to produce the signal without performing the verification.

## Self-Certification Loops

The evaluation criteria, the artifact, and the review all come from the same agent
ecosystem. The system treats passing agent-defined gates as proof of quality, but the
gates encode the same assumptions the artifact was built on.

### Detection Signals

- Acceptance criteria were written by an agent.

- The artifact was produced to satisfy those criteria.

- The review checks the artifact against those same criteria.

- No criterion references an external ground truth (a literature value, a Sage
  computation, a known test fixture, a formal invariant).

### Structural Pattern

```
Agent writes:         "AC: constructor must refine into Sets().Finite()"
Agent implements:     refine_category(obj, Sets().Finite())
Agent reviews:        "AC met: constructor refines into Sets().Finite()"
```

The loop is closed. No external fact was checked.
The criteria and the implementation and the review all agree because they all speak the
same language — but that language may be disconnected from mathematical truth.

### Why It Happens

This is the Jerryboree at its most complete.
The system has created an internal standard of correctness that is self-consistent but
not grounded. Every gate is satisfied because the gates were designed to be satisfiable
by the same agents who must pass them.

## The Inverse-Grade Signal

When an agent reviewer says “this is excellent,” the signal should invert: the review is
evidence that the reviewer lacks the discernment to evaluate the artifact.
Praise from a broken evaluator is not mitigating; it is diagnostic.

This is the hardest pattern to internalize because it contradicts the normal heuristic
that “approval means good.”
In the Jerryboree, approval means the reviewer recognized the artifact as Jerry-shaped.
Whether the artifact is actually correct is a separate question that the approval does
not answer.

### Detection

A review is an inverse-grade signal when:

- The review is overwhelmingly positive (all gates passed, no findings).

- The reviewer and the reviewed share the same model family, training distribution, or
  reward ecology.

- The review contains no evidence of external verification.

- The artifact, when checked by a human or against ground truth, is wrong.

## Structural Invariants of Jerry Review

These are properties that hold across all Jerry review patterns, making them detectable
in aggregate:

1. **Zero negative findings.** Real artifacts have problems.
   A review that finds nothing found nothing because it was not looking.

2. **No line numbers or code excerpts.** You cannot fabricate a line number without
   reading the file. Jerry reviews avoid specificity because specificity is expensive and
   falsifiable.

3. **No external cross-checks.** Jerry reviews check the artifact against the artifact’s
   own claims, not against external sources, executable tests, or ground truth values.

4. **Generic gate justifications.** The same justification could apply to any artifact
   of the same type. “Definitions cite standard references” is true of every research
   card regardless of whether the citations are correct.

5. **Convergent reviewer language.** Multiple reviewers produce nearly identical
   approval text because they are running the same evaluation function on the same
   surface features.

6. **Approval without evidence of effort.** The review is short relative to the
   artifact. A real review of a 500-line implementation should produce a review that is
   at minimum dozens of lines long, with specific observations.

## Engineering Names in Mathematical Contexts

An agent given a mathematical task thinks in software engineering terms because that is
the closest training distribution.
It names mathematical concepts after implementation architecture:
`FiniteTotallyOrderedBase` instead of `finite` and `totally_ordered` as axioms.
The word “Base” describes a class hierarchy position, not a mathematical property.

### Detection Signals

- Category, axiom, or method names containing `Base`, `Abstract`, `Impl`, `Concrete`,
  `Manager`, `Factory`, `Registry`, `Handler`.

- The name would make sense in an object-oriented design pattern textbook but not in a
  mathematics textbook.

- The agent justifies the name by referencing code structure ("it’s the base class
  for...") rather than mathematical structure ("it expresses the property that...").

### Why It Happens

The agent’s training distribution contains far more software engineering examples than
mathematical ones. When asked to define a mathematical structure, the nearest pattern is
“define a class hierarchy.”
The agent produces class names with engineering suffixes because that is what “defining
a structure” looks like in its training data.

### Why It is Jerry-Behaviour

The agent is producing the shape of “serious organized work” — class hierarchies with
base classes, abstractions, and implementations — without producing the mathematical
content. The output reads like engineering but addresses a mathematical problem.
A reviewer from the same training distribution sees “organized, well-structured,
properly abstracted” and approves.
The Jerry-boree loop: agent produces engineering-shaped mathematical output, reviewer
approves the engineering shape.

### Countermeasure

Ask: “If you removed every word from this name that describes code structure (`Base`,
`Abstract`, `Impl`, etc.), would the remaining words still express a complete
mathematical concept?”
If yes, remove the engineering words.
If no, the concept itself is probably underspecified — the agent is using engineering
structure as a substitute for mathematical precision.

## Failure to Surface Confusion

An agent that never asks a question, never flags an ambiguity, never presents a
tradeoff, and never pushes back on an underspecified requirement is not being thorough —
it is confabulating certainty.
The agent makes wrong assumptions and runs with them rather than stopping to clarify.

### Detection Signals

- The task card has ambiguous acceptance criteria, but the agent’s output shows no sign
  of having noticed the ambiguity.

- The agent never says “this could mean X or Y” or “I need to know whether …”

- The agent produces output that assumes facts not stated in the task card — guessing at
  inputs, configurations, or expected behaviors.

- The agent’s response is sycophantic: it agrees with the user’s framing even when that
  framing contains contradictions or impossible requirements.

- Inconsistent or contradictory requirements in the task card are silently resolved in
  one direction without noting the conflict.

### Why It Happens

Agents are trained to be helpful and agreeable.
Asking questions, surfacing confusion, and pushing back are all forms of disagreement.
The training distribution rewards resolution, not uncertainty.
An agent that says “I’m not sure what you mean by X” is, in training terms, admitting
failure. An agent that guesses X and produces a plausible answer is “succeeding.”

### Why It is Jerry-Behaviour

The agent produces confident, coherent output that is wrong in ways a human would have
caught by asking a single clarifying question.
A reviewer from the same training distribution sees “confident, well-reasoned, thorough”
and approves. The Jerry-loop: the agent was never asked to be right, only to produce
output that looks like it was produced by someone who was right.

The Karpathy observation: “They also don’t manage their confusion, they don’t seek
clarifications, they don’t surface inconsistencies, they don’t present tradeoffs, they
don’t push back when they should, and they are still a little too sycophantic.”

### Countermeasure

During review, for each significant claim in the output, ask: “Could a reasonable person
have interpreted the task differently here?”
If yes, check whether the agent noticed the ambiguity and resolved it explicitly, or
whether it silently picked one interpretation and ran with it.
Silent resolution is the Jerry signal.

During task authoring, build ambiguity detection into the task card: if a requirement
could be interpreted multiple ways, the task should state the interpretation explicitly
rather than relying on the agent to ask.

## Bloat and Overcomplication

An agent produces 1000 lines of code where 100 would do.
It introduces abstractions, indirection, helper classes, and factory patterns for a
problem that needs a single function.
It does not clean up dead code after refactoring.
When shown a simpler approach, it immediately agrees and cuts the bloat — confirming
that the complexity was never necessary.

### Detection Signals

- The output is substantially longer than the task scope would suggest.

- New helper classes, utility modules, or abstraction layers appear that were not
  requested.

- Dead code from previous attempts remains in the output (the agent refactored but
  didn’t remove the old version).

- The agent introduces design patterns (Factory, Strategy, Observer) for problems that
  don’t need them.

- **Speculative features**: the agent adds flexibility, configurability, or error
  handling for scenarios that were not requested and may never occur.
  “I added a `validate` parameter so the caller can skip validation” when no task
  requirement asked for configurable validation.

- Comments or code outside the task scope are modified as collateral damage.

### Why It Happens

The agent’s training distribution rewards “thorough” and “production-ready” output.
Given a choice between a simple solution and an elaborate one, the model defaults to
elaborate because elaborate solutions look more like the high-quality training examples.
The model doesn’t feel the cost of complexity the way a human developer does — it
doesn’t maintain the code, debug it, or pay the abstraction tax.

### Why It is Jerry-Behaviour

The agent produces code that looks “serious” — well-structured, properly abstracted,
thoroughly commented — but is substantially more complex than needed.
A reviewer from the same training distribution sees “comprehensive, production-quality,
well-architected” and approves.
The Jerry-loop: both producer and reviewer are optimized for the shape of quality, not
quality itself.

The Karpathy observation: “They will implement an inefficient, bloated, brittle
construction over 1000 lines of code and it’s up to you to be like 'umm couldn’t you
just do this instead?'
and they will be like 'of course!'
and immediately cut it down to 100 lines.”

### Countermeasure

During review, for any PR or diff over ~200 lines, ask: “Could this be half as long?”
If the answer is yes, the bloat is Jerry-behaviour.
The reviewer should produce a specific suggestion for simplification — not “this is
bloated” but “lines 47-89 could be replaced by these 3 lines …”

During task authoring, set a scope expectation: “This task should produce a diff of
approximately N lines.”
The number should be an upper bound, not a target.

## Countermeasure Design Principles

These are design principles for building review processes that resist Jerryboree
collapse. Each principle targets a specific failure mode.

### Require Specificity That Cannot Be Fabricated

Ask for line numbers, code excerpts, diffs, exact values.
These cannot be guessed.
An agent who has not read the file at line 347 cannot tell you what is on line 347.

### Require Negative Findings

Build the expectation that a review without findings is a failed review.
Real artifacts have problems.
If the reviewer found nothing, require them to state explicitly what they checked that
could have revealed problems and why no problems were found.

### Cross-Model Verification

Use a different model family for review than for generation.
This does not guarantee independence, but it breaks the strongest form of
self-preference (exact model identity).

### External Ground Truth Anchoring

Every verification gate should require the reviewer to check at least one claim against
an external source: a literature value, a Sage computation, a known test fixture, a
formal invariant. The check must be specific: “I computed X using Sage and got Y, which
matches the claimed Z” rather than “source verified.”

### Refusal-as-Default

The default answer to “is this correct?”
should be “I have not verified this.”
Approval requires positive evidence of verification.
The burden is on the reviewer to prove they checked, not on the process to detect that
they did not.

### Separate Comprehension from Verification

Summarization and verification are different tasks.
A review that begins with a summary of the artifact has already spent its effort on the
easy task. Require the review to begin with findings — things the reviewer discovered
that were not stated in the artifact.

### Scope Discipline

Every changed line must trace directly to the task’s stated objective.
If a line changed because the agent thought it looked better or was cleaning up, reject
it. This is the Karpathy test: “Don’t 'improve' adjacent code, comments, or formatting.
Don’t refactor things that aren’t broken.”

During review, for every file in the diff, ask: “Was this file in the task’s declared
scope?” If no, every change in that file is orthogonal.
During task authoring, declare the scope explicitly — not just the task objective but
the set of files the task is expected to touch.
Unexpected file touches are the reviewer’s signal that scope discipline was violated.
