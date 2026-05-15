---
name: reviewing-subagent-work
description: Use when reviewing or evaluating work produced by another LLM/agent. Forces task-value reasoning and routes to detailed failure-mode knowledge.
---

# Reviewing Subagent Work

When reviewing work produced by another LLM or agent, answer these questions BEFORE concluding your review:

## Forcing Questions

**Q1: "Did I inspect actual content, or just verify activity occurred?"**

A: [answer explicitly]

**Q2: "Why would user ask ME to review this instead of checking themselves?"**

A: [answer explicitly - what capability do I have that they lack?]

**Q3: "If my review found: files exist ✓, hashes match ✓, worker claims success ✓ — is that EVIDENCE or just ACTIVITY?"**

A: [answer explicitly]

## The Failure Mode

If you:
- Checked file existence without reading content
- Verified hashes/metadata without evaluating quality
- Read the worker's self-report and trusted it
- Confirmed "work was done" without assessing "work is good"

Then you did **circular validation** - you reviewed an LLM by trusting the LLM's self-report. This defeats the purpose of review.

## What Real Review Requires

Before concluding, your review MUST contain:
- Specific findings from actual content (line numbers, concrete values)
- Quality assessment of the work itself (not just that it exists)
- Problems found, or explicit statement of what you verified and how

If your review could have been written without reading the artifact → you didn't review it.

## Next Steps

If you found yourself doing circular validation:
- LOAD `jerry-behaviour` skill for detailed failure patterns
- Start over: actually read the content and evaluate quality

If user reports the subagent work was shallow:
- LOAD `addressing-shallow-work` skill before proposing fixes
