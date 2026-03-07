---
name: llm-failure-modes
description: Use when reasoning through a complex or high-stakes problem to check for common LLM cognitive failures.
metadata:
  author: dzack
  version: "0.1.0"
---

# LLM Failure Modes

## Observed Formal Cognitive Failures

### Subagent (LLM) Failures

1. **Constraint hallucination** - Inventing unprompted constraints (e.g., adding years to search queries when not requested)

2. **Citation without comprehension** - Writing correct facts but unable to reason with them (e.g., stating correct dates but applying backwards temporal logic)

3. **Internal logical incoherence** - Having correct information but applying contradictory reasoning (e.g., knowing the date but treating past events as future)

4. **Unwarranted dismissal** - Rejecting valid results rather than investigating (e.g., dismissing a valid result as "speculative" without checking)

### Operator (Human) Failures

5. **Confabulation** - Making confident ungrounded assertions about unknowable internals (e.g., "the subagent likely used stale data" without evidence)

## How to Avoid These Failures

### Before Making Claims

1. **Check evidence first** - Read available data before drawing conclusions
2. **Acknowledge limits** - Don't claim knowledge about unobservable internals
3. **Trust plain text** - Accept what evidence shows rather than inventing complex explanations
4. **Label inferences** - Use "I believe", "based on limited evidence", "inference" for ungrounded claims

### When Reasoning About Dates/Temporal Context

1. **Always search with current year** - Never add arbitrary date constraints
2. **Trust historical dates** - If it's March 2026, November 2025 is historical (past), not future
3. **Verify temporal logic** - Check that conclusions align with known dates

### When Interpreting Subagent Behavior

1. **Read transcripts** - Don't speculate without evidence
2. **Quote exactly** - Use exact lines, not paraphrases
3. **Don't over-interpret** - Simple explanations usually suffice
