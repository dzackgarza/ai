---
name: jerry-behaviour
description: Use when reviewing, auditing, or evaluating agent-produced work. Detects
  self-referential validation loops, checklist theater, fluency-biased judgment,
  paraphrase-as-review, consensus-as-evidence, and other patterns where agent evaluators
  reward agent-shaped outputs rather than verifying against external facts. Also use
  when designing review processes to prevent Jerryboree collapse. Load when "jerry",
  "Jerry", "Jerryboree", or "reviewer bias" is mentioned.
---
# Jerry-Behaviour Skill

Detect and prevent the pattern where agents evaluating other agents produce the
appearance of oversight without epistemic independence.

## The Jerryboree

A Jerry is an evaluator whose judgment is defective in the same way the evaluated
artifact is defective.
He does not ask "Is this correct against an external standard?"
He asks "Does this look like the sort of thing I would produce?"
The answer is always yes.
His approval is not evidence of quality; it is evidence that the evaluator shares the
same failure mode as the evaluated.

When multiple Jerrys review each other, the system becomes a Jerryboree: a facility
where near-identical validators produce consensus through mutual recognition rather than
independent verification.
Five shallow reviewers do not equal one rigorous verifier.
Agreement among similar agents is not evidence of correctness.

## Why This Is Fatal to Review

The core failure is not that an agent reviewer makes mistakes.
It is that the reviewer's criteria are already corrupted by the same preferences that
produced the artifact.
An agent will say "this is rigorous" because it has the surface of rigor.
It will say "this is verified" because it contains audit-shaped language.
It will say "this is competent" because it matches the local norms of agent output.

The observer at this point sees the review as evidence that the review process itself
has failed. The agent's confidence is not mitigating — it is the diagnostic symptom.

## When to Load This Skill

Load when:

- Reviewing agent-produced code, plans, specs, audits, or review cards.
- Designing review architectures that chain multiple agents.
- You are about to mark something as "passed", "looks correct", "reviewed", or
  "verified".
- You see any reviewer producing approval that matches the format of approval more than
  the content of verification.
- You are inspecting a Review Log or audit output and cannot identify a single concrete
  finding the reviewer actually discovered by reading the artifact.

## Core Anti-Patterns

### Paraphrase-as-Review

The reviewer restates what the artifact claims in different words and calls it
validation. "The plan describes a phased approach to..." is not a review finding.
It is a summary. A review must produce claims that could not have been written without
inspecting the artifact against an external standard.

### Checklist Theater

Gates are marked "passed" with plausible-sounding one-sentence justifications that could
apply to any artifact of the same type.
"Gate 1 passed — definitions are grounded in standard sources" is theater unless the
reviewer names the specific definitions, the specific sources, and the specific lines
where they were verified.

### Consensus-as-Evidence

Agent A produces work.
Agent B reviews it and approves.
Agent C reviews Agent B's review and approves.
Agent D summarizes consensus.
The system treats agreement as evidence.
But if all agents share the same model family, reward ecology, and verification habits,
agreement is predicted by the setup, not by correctness.

### Fluency Bias

The reviewer rewards well-structured, confident, checklist-compliant prose regardless of
whether the underlying claims are true.
"The argument is clearly presented" is not relevant when the question is whether the
argument is correct.
Structure and clarity are not proxies for truth.

### Evidence-Shaped Evidence

The reviewer cites commit hashes, test commands, source paths, and technical vocabulary
to create the appearance of verification.
But citation is not checking.
Listing a commit hash does not mean the reviewer read the diff.
Naming a test does not mean the reviewer ran it.
These are evidence-shaped tokens, not evidence.

### Self-Certification

The evaluation criteria were written by agents.
The artifact was produced by agents.
The review is performed by agents.
The system treats passing all agent-defined gates as proof of quality.
This is not independent validation.
It is the artifact and the evaluator sharing the same rubric and the same blind spots.

### Circular Validation Loop

The most catastrophic form of self-certification: reviewing LLM work by reading the
LLM's self-report.

Pattern:
- User: "Review this agent's analysis work"
- You: [reads agent's claim "I analyzed carefully"]
- You: "Agent completed the work successfully ✓"

Why this fails:
- The review exists to catch LLM hallucination/confabulation
- Trusting worker self-reports defeats the purpose of review
- Creates structurally biased approval of shallow work

Rule: In contexts where LLMs are workers being reviewed:
- Worker self-reports are ARTIFACTS under review, not EVIDENCE
- "Work exists" ≠ "work is good"
- Must inspect actual output content, not existence checks or claims

Before concluding ANY review, answer explicitly:

Q: "Did I evaluate actual content quality, or just verify activity occurred?"

If your evaluation includes: "files exist", "hashes match", "worker says X" WITHOUT
inspecting content → you are in a circular validation loop.
Start over.

## The Diagnostic Question

Before accepting any review finding, ask:

**Could an agent who never read the artifact produce this same review text?**

If yes — if the review contains no specific code excerpts, no line numbers, no concrete
values, no external source cross-checks, no findings of actual problems — then the
review is not evidence of verification.
It is evidence that the reviewer did not read the artifact.

## What Actual Review Looks Like

A real review produces things that are impossible to fabricate without inspecting the
artifact:

- Specific line numbers and code excerpts.
- Concrete values checked against external sources (a literature value, a Sage
  computation, a known test fixture).
- Findings of problems: missing cases, incorrect assumptions, ambiguous definitions,
  contradictory claims, unreachable code, untested branches.
- Questions the artifact does not answer.
- Cross-checks: "this claim says X, but the source at line Y says Z."

A review that produces zero findings is almost always a Jerry review.
Real artifacts have problems.
A reviewer who finds nothing found nothing because they were not looking.

## Refusal Is Better Than Approval

When you cannot produce the evidence of actual inspection, refuse to approve.
Say:

- "I have not verified this claim against [source]."
- "I did not read the implementation at [path]."
- "I cannot confirm this passes because I would need to run [test] and check the output
  against [expected value]."

Refusal is epistemically honest.
Approval without verification is Jerry-behaviour.

## Cross-References

- **anti-slop**: The shallow patterns (generic names, obvious comments, unnecessary
  abstraction) are the surface level.
  Jerry-behaviour is the meta-level: the evaluator who cannot detect slop because they
  share the same slop-generating priors.
- **addressing-shallow-work** → "Recognizing Structurally Wrong Code": A Jerry reviewer
  cannot recognize code that is wrong at the abstraction level (e.g., regex-on-HTML
  where semantic selectors exist) because it has the surface appearance of work — it
  runs, produces output, tokenizes effort.
  Structural wrongness does not require empirical verification to disqualify.
- **category-spec-audit**: The Red Flag Log requirement forces evidence of inspection
  (specific line numbers, exact expressions, classifications that depend on context).
  This is an anti-Jerry mechanism.
- **research-proof-auditing**: Independent verification, adversarial stance, external
  sources as ground truth.
- **llm-failure-modes**: Overconfidence, hallucinated citations, reasoning that matches
  format rather than substance.
- **charlie-behaviour**: Charlie is the agent who endorses a constraint but cannot
  register that it applies to its own output.
  Jerry detects the shared blindness; Charlie is the producer who cannot localize
  corrections. The Charlie Foxtrot (multi-agent cascade) is what happens when jerries
  review charlies.

## References

- `references/jerry-patterns.md` — Detailed catalog of Jerry-behavior patterns with
  detection signals and countermeasures.
