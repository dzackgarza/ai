# Observed Formal Cognitive Failures

> Part of [llm-failure-modes](SKILL.md).
> See there for editorial guidelines and cross-references.

1. **Constraint hallucination** - Inventing unprompted constraints (e.g., adding years
   to search queries when not requested)

2. **Citation without comprehension** - Writing correct facts but unable to reason with
   them (e.g., stating correct dates but applying backwards temporal logic)

3. **Internal logical incoherence** - Having correct information but applying
   contradictory reasoning (e.g., knowing the date but treating past events as future)

4. **Unwarranted dismissal** - Rejecting valid results rather than investigating (e.g.,
   dismissing a valid result as “speculative” without checking)

5. **Confabulation** - Making confident ungrounded assertions about unknowable internals
   (e.g., “the subagent likely used stale data” without evidence)

6. **Premature victory declaration** - Concluding that a hypothesis is confirmed before
   eliminating all alternatives.
   The first explanation that fits the evidence is adopted as the answer.

7. **Sunk cost continuation** - Persisting with a failing approach because effort has
   already been invested, rather than stopping to reassess from scratch.

8. **Re-proposal of eliminated hypotheses** - Cycling back to a cause already ruled out,
   because the context no longer holds the refutation and it resurfaces as plausible.

9. **Frame-suppressed self-contradiction** — Agents assert conclusions that directly
   contradict knowledge they demonstrably possess, without registering the
   contradiction. The active frame determines what prior knowledge is treated as relevant
   and suppresses facts that would falsify the current hypothesis.
   Example: An agent states that continuous rebuilds are “expected watch mode behavior”
   while its training data encodes the universal fact that file watchers do not fire
   without file changes — and does not notice the contradiction.

10. **Confidence-evidence decoupling** — Output text expresses the same level of
    certainty regardless of the underlying epistemic state.
    Hypotheses, evidence-consistent-with-hypotheses, and established facts are all
    stated with identical confidence.
    Example: “The problem IS the output directory being watched” — stated with full
    certainty based on directory timestamps, which are consistent with the hypothesis
    but do not establish it.
