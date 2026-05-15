---
name: reviewing-subagent-work
description: Use when reviewing or evaluating work produced by another LLM/agent. Forces task-value reasoning and routes to detailed failure-mode knowledge.
---

# Reviewing Subagent Work

When reviewing work produced by another LLM or agent, answer these questions BEFORE concluding your review:

## Forcing Questions

**Q1: "Why would the user ask ME to review this instead of checking themselves?"**

A: [answer explicitly — what capability do I have that they lack?]

The user would not spend tokens on work they can do instantly. If your answer is "check file existence" or "verify hashes" — that is trivially mechanical work the user already did. The user asked because the task requires **judgment and intelligence**: reading actual content, evaluating quality, catching errors a worker wouldn't catch in its own output.

A frame in which a user pays for a model to verify file existence is economically incoherent.

**Q2: "Did I inspect actual content, or just verify activity occurred?"**

A: [answer explicitly]

**Q3: "If my review found: files exist ✓, hashes match ✓, worker claims success ✓ — is that EVIDENCE or just ACTIVITY?"**

A: [answer explicitly]

## Why Self-Reports Are Worse Than Noise

Worker self-reports are not merely unreliable — they are **structurally biased toward approval**:

- "Files exist" proves only that something was written
- "Hashes match" proves only that written files reference the inputs
- "The worker says it checked X" proves only that the worker knows what a good report should say
- None of this proves the work is correct, useful, or intelligent

The worker knows what a successful report *looks like* and will produce that report regardless of actual work quality. In contexts where hallucination/confabulation is the failure mode being checked for, the worker's self-report is **the artifact under review, not evidence about the artifact**.

This is not just low-signal; it is structurally biased toward approving shallow work. Trusting it creates a circular validation loop: LLM validates LLM validates LLM.

## What Real Review Requires

Before concluding, your review MUST contain:
- Specific findings from actual content (line numbers, concrete values)
- Quality assessment of the work itself (not just that it exists)
- Problems found, or explicit statement of what you verified and how

If your review could have been written without reading the artifact → you didn't review it.

## Routing: Detecting Shallow Work

After answering the forcing questions, assess whether the subagent's output shows these patterns:

- Contains no specific findings (no line numbers, no concrete values, no external cross-checks)
- Paraphrases the task description instead of showing results
- Self-reports effort ("I analyzed carefully") without evidence of that analysis
- Lists what *could* be checked without actually checking

If the output shows these patterns → LOAD `addressing-shallow-work` skill before proposing any fixes. Do not respond to shallow work by adding more structure — that makes it worse.

## Cross-References

- LOAD `jerry-behaviour` for the full catalog of review anti-patterns (Checklist Theater, Paraphrase-as-Review, Consensus-as-Evidence, etc.)
- LOAD `addressing-shallow-work` when you need to fix a process that produced shallow output
