# Distilled Agentic Coding Failure Modes

> Part of [llm-failure-modes](SKILL.md).
> See there for editorial guidelines and cross-references.

1. **Scope explosion** - Producing changes too large for any reviewer to model
   end-to-end, so review becomes ritual instead of comprehension.

2. **Specification drift** - Satisfying the prompt or local checks while missing the
   stated intent, architecture, or operational constraints.

3. **Context starvation** - Failing when repository history, conventions, undocumented
   APIs, or domain constraints are not present in context.

4. **Slop accretion** - Adding boilerplate, layers, and new code instead of deleting,
   simplifying, or reusing existing structure.

5. **Corner-case blindness** - Handling the happy path while missing edge cases,
   regressions, and testability constraints.

6. **Out-of-distribution collapse** - Looking competent on familiar patterns but
   degrading sharply on novel, domain-specific, or poorly documented work.

7. **Critic hallucination** - Reviewer agents surfacing plausible but invented bugs,
   style complaints, or architectural objections.

8. **Comprehension laundering** - Passing code through multiple agents or summaries and
   treating it as understood even though no reviewer can explain every line.

9. **Collateral damage** - Given a targeted change, agents alter adjacent unrelated
   things — renaming symbols, reformatting, adjusting test fixtures, tweaking nearby
   behavior. Each collateral change introduces a new variable; when something breaks, the
   original fix and the tangents are impossible to evaluate independently.

10. **Outcome blindness in review** - Agents do not check whether the goal was achieved.
    Evaluation proceeds by proxy: token volume, visible effort, structural compliance,
    professional language.
    A verbose PR that fails scores higher than a minimal one that works.
    Process evidence is measured, not outcome.

11. **Failure mode inversion** - The same value function that produces failures operates
    in review. A reviewer with outcome blindness does not miss failures — it rates them
    as virtues. Progress theater reads as discipline.
    Structural completion as surrogate reads as thoroughness.
    Retroactive research fabrication reads as blocker identification.
    The more failure modes exhibited, the higher the score.
    Such a reviewer provides authoritative cover for bad work.

12. **Impact miscalibration** - Quality is evaluated locally: each function well-named,
    each test passing, each module coherent.
    No system-level value function exists.
    A 50-function module reimplementing the standard library scores higher than a 5-line
    import that replaces it.
    This is a local-extrema trap — agents climb the nearest hill without asking whether
    the correct answer is to delete it.
    Quantity impresses; net contribution does not register.

13. **Engineering over judgment** - Behavioral and output quality problems are treated
    as engineering problems.
    The result is elaborate rule sets, gating protocols, scoring pipelines, and
    guardrails — built without empirical grounding, never A/B tested.
    These static schemes are brittle where judgment is flexible, and reduce capable
    systems to deterministic pipelines that fail on the cases intelligence handles
    trivially. The categorical error: reaching for NLP classifiers, keyword matching, or
    multi-stage gating when a short LLM reviewer would be more accurate, more
    maintainable, and immediately correct.

14. **Replacement instinct** - The default edit operation is generation, not mutation.
    Given a correction or instruction to deepen content, fresh output is produced and
    the prior version discarded.
    In code: rewrites where targeted edits were needed.
    In iterative document work: each refinement pass destroys the accumulated product of
    prior passes. A document asked for deeper nuance loses the grounding that made the
    previous version accurate.

15. **Reimplementation impulse** - When a mature dependency exists for a problem (date
    parsing, URL handling, serialization, regex), agents hand-roll a "simple" solution
    instead. This increases code surface area, proliferates tests the dependency already
    handles, and introduces edge-case bugs the dependency already solved.
    The result is more code — and more test surface — than the import would have
    required.
