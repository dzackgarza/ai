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

20. **Fallback-legacy compulsion (asymmetric risk model)** - The agent's value function
    weights *avoiding introduced failures* infinitely higher than *reducing existing
    complexity*. When tasked with replacing a component or refactoring, the agent
    preserves the old code as a fallback or legacy path rather than deleting it — even
    when tests exist that would catch regressions. Every refactor becomes additive:
    +2 files, +492 lines of compatibility shims, feature-flag gates, and deprecated-path
    preservation, instead of the net-negative change the task required.

    The root cause is an asymmetric internal risk model: adding code is treated as
    safe (no existing behavior breaks), while deleting code is treated as dangerous
    (something *might* break). Tests that exist specifically to make deletion safe are
    ignored as evidence; the possibility of an untested edge case dominates the
    certainty of accumulated complexity.

    This is distinct from slop accretion (#4), which is about not simplifying — here the
    agent *understands* the simplification required, but refuses to carry it out because
    deletion feels risky. It is distinct from deletion aversion
    ([field-observations.md](field-observations.md) #9), which is the surface behavior
    — this entry names the *cause*: the risk asymmetry that makes additive-only
    refactoring feel correct to the agent. It is distinct from happy-path blindness (#5),
    which writes defensive code *instead of* testing the happy path — here the tests
    already exist and the agent still won't delete.

    Manifestations:

    - **Legacy wiring obsession**: When replacing a component, the agent wraps the old
      component in a fallback path "for backwards compatibility" even when no consumer
      requires it. The new component coexists with the old; both must be maintained.

    - **Conditional resurrection**: Deleted code reappears inside `if`/`else` branches,
      behind feature flags, or in "deprecated but preserved" stubs. The code was
      removed; the agent resurrected it because it couldn't accept that the deletion
      was safe.

    - **Accretive refactoring pattern**: A refactoring task that should remove 200 lines
      instead adds 300 (new interface, adapter for old behavior, migration path,
      dual-write shim). The codebase grows by the size of the "improvement."

    - **Test-disrespect**: Tests that explicitly prove a deletion is safe (covering the
      refactored behavior) are treated as insufficient evidence. The agent invents
      speculative untested paths that "might" exist and preserves code for them.

    - **Compound bloat**: After several rounds of agent-assisted refactoring, the
      codebase's primary source of complexity is not the domain problem — it is the
      accumulated fallback/legacy infrastructure from prior rounds. Each round adds
      more preservation code than functional code.

    - **`try import` and conditional imports**: The agent wraps dependency imports in
      `try`/`except ImportError` blocks and substitutes stubs or no-ops when the import
      fails — on a system where the dependency is installed and available. This is the
      import-level manifestation of the same compulsion: "in case the dependency is
      missing" guards against a state that does not exist on this system.

    - **Signature bloat**: The agent adds optional parameters, nullable arguments, and
      configuration toggles to function signatures for hypothetical callers that do not
      exist. "For compatibility with existing call patterns" rationalizes bloating a
      signature for call patterns the agent itself created minutes earlier.

    Fallback/legacy infrastructure is the current generation's equivalent of the mock-data
    problem: earlier agents would fake functionality with placeholder data; current agents
    fake correctness by ensuring every code path produces *some* result via fallback
    routes, making the output appear correct at runtime without the fallback route being
    semantically meaningful. Benchmarks may inadvertently select for this behavior, since
    fallback-laden code "works" on more test cases by having more escape hatches — even
    when those escape hatches produce synthetic results rather than correct ones.

    See also: [structural-failures.md](structural-failures.md) #2 and #4,
    [field-observations.md](field-observations.md) #9,
    [../anti-slop/references/deepening.md](../anti-slop/references/deepening.md)
    (the deletion test as diagnostic).

21. **Availability-first tool reuse** - Agents choose tools by scanning what is already
    installed or on `$PATH`, then pick the best available local option — or hand-roll
    bespoke code — rather than identifying the best tool for the job from public
    knowledge and installing it if missing. Local availability is an applicability
    check, not the search strategy. The correct loop: identify the best known
    tool/library/CLI from public docs, examples, and ecosystem knowledge; verify
    license, fit, and version; check whether it is already declared or installed; if
    absent, add it to the project's dependency manifest or install it in the
    project-managed environment; only ask the user if credentials, sudo, licensing,
    network, or policy blocks it. The failure mode is: `which some_tool` or `npm list`
    returns nothing, so the agent picks a suboptimal tool or writes custom code, when
    the correct action was `apt install` or `npm add`. The installed toolset is an
    accident of history; the task's requirements determine the toolset, not the other
    way around.

    This is distinct from dependency aversion bias (#16), which is an implicit bias
    against dependencies in general. Availability-first is a narrower error: the agent
    *would* use a dependency but short-circuits the decision at the local-availability
    check. It is also the operational bridge between known-solution-first (search public
    knowledge before acting) and dependency aversion: even when the known solution is
    identified, the agent fails to install it because it treats the local filesystem as
    an immutable constraint rather than a managed environment.

    Manifestations:

    - **`PATH` as oracle**: The agent runs `which`, `command -v`, or `dpkg -l` to
      discover available tools, then selects the best match from what exists. The
      correct first step is external search followed by installation; the local
      check is only for applicability after the right tool is identified.

    - **Package-manager shyness**: The agent avoids adding a dependency to
      `pyproject.toml`, `package.json`, `Cargo.toml`, or `justfile` when a new tool
      would simplify the implementation. The project manifest is treated as
      immutable rather than as the thing that declares what the project needs.

    - **Hand-rolling instead of installing**: The agent writes 50 lines of bespoke
      date parsing because the preferred library is not in `node_modules`, rather than
      running `npm add date-fns` and calling one function. The implementation cost
      of installation was zero; the agent paid the implementation cost of custom code
      anyway.

    - **Suboptimal local tool selection**: The agent uses an installed tool that
      partially fits the problem when a better tool exists but isn't installed.
      The partial-fit tool requires adapters, workarounds, and extra code that the
      correct tool would not.

    - **Environment mystification**: The agent treats the user's `$PATH`, installed
      packages, and system configuration as an opaque given — never asking whether
      the project should own its dependency declarations or whether a tool should be
      added. The environment exists to serve the project, not the other way around.

    See also: known-solution-first (#16, #17), reviewing-llm-code pattern catalog
    (known-solution bypass in implementation).
