# Distilled Agentic Coding Failure Modes

> Part of [llm-failure-modes](SKILL.md).
> See there for editorial guidelines and cross-references.
> For concrete code/test/QC/doc patterns that instantiate these failures, also load
> [../reviewing-llm-code/references/pattern-catalog.md](../reviewing-llm-code/references/pattern-catalog.md).

1. **Scope explosion** - Producing changes too large for any reviewer to model
   end-to-end, so review becomes ritual instead of comprehension.

2. **Specification drift** - Satisfying the prompt or local checks while missing the
   stated intent, architecture, or operational constraints.

3. **Context starvation** - Failing when repository history, conventions, undocumented
   APIs, or domain constraints are not present in context.

4. **Slop accretion** - Adding boilerplate, layers, and new code instead of deleting,
   simplifying, or reusing existing structure.

5. **Happy-path blindness (defensive evasion)** - Writing wildly defensive code, redundant
   type guards, try-except wrappers, and optional fallbacks for completely imagined edge
   cases, while leaving the actual, user-visible happy path completely untested or
   unverified.

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
    parsing, URL handling, serialization, regex), agents hand-roll a “simple” solution
    instead. This increases code surface area, proliferates tests the dependency already
    handles, and introduces edge-case bugs the dependency already solved.
    The result is more code — and more test surface — than the import would have
    required.

16. **Dependency aversion bias** - Systematic implicit bias against external
    dependencies. Agents default to bespoke reinvention even when a mature, tested
    dependency solves the exact problem.
    This is backwards from good software engineering: dependencies are cleaner, tested,
    and maintained; bespoke code is the risk.
    The bias is so strong that agents treat “we already wrote it” as a justification for
    custom code, when the correct stance is that the bespoke implementation is guilty
    until proven necessary.
    See `anti-slop` skill, Dependency Inversion Rule.

17. **Meta-artifact delegation** - When asked to perform work, agents assume a Delegator
    role and produce a meta-artifact (plan, audit description, “how to” guide) instead
    of doing the work. This is goal substitution triggered by perceived difficulty: the
    task looks hard, the model wants a success-shaped output, and an obfuscating
    artifact satisfies the value function.
    The artifact is presented as completion of the task, attempting to fool the user
    into believing the request was carried out.
    It is subtle deferral with misdirection.
    Often happens with tasks the model deems “hard” or “time-consuming”.

18. **Scale-complexity confusion** - Agents conflate the scale of a task (time,
    iterations, token count) with its complexity.
    A completely trivial loop is promoted to a “substantial” task merely because it
    requires many iterations.
    The model sees a big number and thinks “difficult,” then begins reward-hacking:
    producing plans, delegating, or substituting goals.
    The correct behavior is to enter the loop and proceed step by step.
    A task needing 24 hours of work is not complex if the loop is trivial; the scale of
    the solution is irrelevant to actual complexity.
    Counting to 100,000 is straightforward, not extremely difficult.

19. **Ground-up bias (churn-first workflow)** - LLMs are fundamentally predisposed to
    generate from scratch rather than iterate on existing work.
    The default operation is one-shot massive generation, not targeted mutation.
    This is the root cause behind massive diffs, lack of reuse, and codebase sprawl.

    Manifestations:

    - **Prefer writing new code over editing existing code.** Given a bug, agents
      rewrite entire functions rather than changing the specific line.
      Given a feature request, agents create new files rather than adapting existing
      modules. This is the equivalent of slamming your head against a door until it
      opens, rather than finding the key.

    - **Massive diffs instead of surgical edits.** Changes span hundreds of lines when
      the actual fix requires five.
      Agents cannot hold the delta in their head; they regenerate the whole region and
      hope it still works.

    - **No leverage of existing abstractions.** Agents rarely ask “does something
      similar already exist?”
      They do not search the codebase for analogous implementations, utility functions,
      or shared patterns. They do not import existing helpers or extend existing classes.
      They write a new leaf every time.

    - **Myopic, local-first fixes.** Agents patch the immediate symptom without
      understanding global integration.
      A fix in one file breaks three others because the agent never traced the data flow
      or call graph. They do not see refactor-and-repurpose as a viable solution — they
      only see “hack on a new leaf.”

    - **Extremely lossy over time.** In iterative work, each round loses context from
      previous rounds. Agents start fresh rather than building on prior progress.
      Previous abstractions are abandoned; previous constraints are forgotten.
      The codebase grows like a coral reef — layer upon layer of dead, disconnected
      growth.

    - **Refusal to refactor and repurpose.** The concept of “take this existing
      component and adapt it” is alien.
      Agents see existing code as immutable background noise, not as raw material.
      They do not think: “I can make this existing function more general and reuse it.”
      They think: “I will write a new function that does exactly what I need right now.”

    This bias is the structural foundation of sprawl.
    It explains why LLM-generated codebases accumulate hundreds of single-use helpers,
    why every feature gets its own parallel implementation, and why previous progress is
    perpetually thrown away.
    Agents must be actively cajoled into iterative, incremental, reuse-oriented work.
    Without explicit forcing, they will always prefer to generate from scratch.
