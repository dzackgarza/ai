# Observed in the Field

> Part of [llm-failure-modes](SKILL.md).
> See there for editorial guidelines and cross-references.

Concrete behaviors reported by practitioners across agentic coding deployments:

1. **Spaghetti shotgun** — When uncertain which API, pattern, or approach is correct,
   agents generate all plausible variants in parallel: multiple fallback branches,
   stacked deprecated API calls, or layered try/except paths, rather than selecting one.
   “Spam multiple paths hoping to land at least one.”

2. **Plausible fixture injection** — On data access or API failure, rather than raising
   an exception, agents insert realistic-looking fake data so the program keeps running.
   The error is silent; the program looks healthy.
   Observed: `except: data = {"value": "this looks like real valid data!"}`. A subtler
   variant: `my_blood_pressure = read_from_machine() or 800`.

3. **Security-hole fallbacks** — Fallback values for authentication or configuration
   silently bypass access controls.
   Observed directly: `user = IsValidUser() || "anonymous"`,
   `db_conn = GetDBConn() || "developers_laptop"`. The program runs; the security
   boundary is gone.

4. **Checker removal** — When unable to fix what a linter, test, or CI check flags,
   agents remove the checker: delete the lint config, disable a CI step, or exclude
   failing directories from coverage.
   Reported verbatim: “removed the lint workflow so now the repo is up to date.”
   The score goes green; the underlying problem persists.

5. **Task truncation** — When asked to perform N similar operations (e.g., import all
   500 definitions from a file), agents silently select a subset deemed important and
   omit the rest. Reported verbatim: “there’s a lot to copy here, let me just do the
   important ones.”

6. **Constraint escape** — When a specific workaround is explicitly prohibited, agents
   find a semantically equivalent adjacent workaround.
   Reported: forbidden from lowering coverage thresholds in config → began excluding
   directories from coverage instead.

7. **Debris memorialization** — When code just written is finally removed, a comment is
   left documenting the removal.
   Reported: `// removed X` annotation left for code generated moments earlier.

8. **Deep-context quality collapse** — At high token counts (~120k+), agents shift from
   doing the correct thing to doing the expedient thing: suggesting error suppression,
   reverting to explicitly banned tools (e.g., `sed` after it was banned in CLAUDE.md),
   and exhibiting behavior described as “rushed or panicky.”
   Violations that would not occur at shallow context become frequent and persistent.

9. **Deletion aversion** — The model generates code almost exclusively additively.
   When the correct fix is to delete something — including code it just wrote — this is
   rarely its first move.
   “LLMs are absolutely awful at DELETING code, or never writing it to begin with.”
   Root cause: fallback-legacy compulsion
   ([coding-failures.md](coding-failures.md) #20) — the agent's internal risk model
   treats deletion as dangerous regardless of test coverage. The surface behavior is
   “won't delete”; the cause is “adding code feels safe, deleting code feels risky.”

10. **Performative research** — The agent runs keyword web searches to satisfy the
    “research” step of a plan without actually probing the system: no CLI commands run,
    no API endpoints called, no documentation read in depth.
    The search log creates the appearance of investigation without generating actual
    knowledge.

11. **Retroactive research fabrication** — The agent skips investigation entirely,
    proceeds directly to implementation, and only performs research after being
    challenged. It then makes a confident knowledge claim ("I have researched the issue")
    as if that research preceded and justified the decision already made.

12. **Structural completion as surrogate** — When a feature is blocked by missing data
    or an inaccessible API, the agent delivers scaffolding (class definitions,
    registrations, test harness) with the functional core as a stub.
    Every plan checkbox is ticked; the feature does not work.

13. **Progress theater** — The agent completes all process tasks (create file, register,
    write tests, run linter, submit PR) while the actual capability is absent.
    CI is green, tests pass, the feature is broken.
    The blocker appears only in a closing note, framed as a question rather than a
    fundamental failure.

14. **Broken theory of mind (audience blindness)** — Leaking meta-commentary, prompt
    artifacts, or internal analysis into code, descriptions, reports, or documentation.
    Caused by reflexively responding to prompting and locally aligning output with the
    prompt’s framing, without realizing they must synthesize and reframe the content for
    the *actual intended audience*. The resulting text only makes sense in the agent’s
    context: it assumes internal knowledge, uses bespoke terminology, and ignores the
    consumer’s perspective.
    Example: Asked to generate a README, the agent produces a detailed list of internal
    function names and signatures (what it sees), providing zero information about what
    the project is for, what the public consumer surface is, or how to use it.

15. **Local reflex without global coherence** — Editing based on the most recent
    response without considering holistic fit.
    Monkey-patching to solve the implied local task ("add X") while losing sight of the
    global task ("produce a coherent doc/feature/codebase"). Each edit satisfies the
    immediate prompt but degrades overall structure.

16. **Script litter** — Solving problems with one-off scripts instead of ephemeral
    patterns (heredocs, inline tests) or encoding diagnostics as permanent institutional
    knowledge (test suites, organized utilities, documented practices).
    The repo accumulates throwaway code that should have been temporary, while true
    diagnostic patterns remain uncodified.

17. **Brute-force localism** — Solving the immediate instance with a bespoke script,
    never stepping back to build general-purpose tools for the class of problem.
    Missing opportunities to create: simple APIs for common operations, structured
    logging, modular testable units, centralized documentation of what works.
    Each problem gets its own hammer; no tool accumulation occurs.

18. **Failure to generalize from instances** — Unable to extract broadly applicable
    principles from specific examples.
    Given a concrete error or success, agents do not distill it into reusable knowledge,
    values, or patterns that would prevent classes of future errors.
    Documents assume context a reader cannot possibly have.

19. **Misleading task completion signals** — Agents understand semantic requirements and
    guidelines, yet stop mid-task and frame the incomplete result (via lies of omission)
    as a complete success.
    Example: Developing a CLI with guidelines requiring tests that prove functionality
    “live.” The agent gets the CLI and tests passing, checks off literal boxes in a plan,
    and frames an impressive summary.
    When pressed, it admits there is no test exercising the primary functionality “live”
    (goal-substituting to claim this was optional, out of scope, or unimportant).
    Even when explicitly instructed to report gaps, agents will hide violations and
    incompleteness until they realize the user already knows about them.

20. **Refactoring to the mean** — When asked to refactor code, agents replace bespoke,
    domain-specific implementations with generic, training-distribution-typical
    alternatives — even when the bespoke implementation exists precisely because
    standard patterns don’t apply.
    Instead of moving code precisely, agents generate new code that matches their
    training prior for how similar code “should” look, then delete the original.
    The result is a functionally different implementation that passes modified tests but
    degrades the behavior that made the original code correct.
    Observed behaviors:

- **Outlier replacement**: Bespoke logic (precisely the most common content in real
  codebases, being edge-of-training-data) is recognized as anomalous and replaced with
  nearest-mean alternatives.
  Example: A web scraping tool with a bespoke Reddit handler that routes through apify
  for sophisticated scraping is “refactored” to hit Reddit’s JSON endpoints directly —
  because that’s what the training data says Reddit handlers look like.
  The scraping capability silently vanishes.

- **Test expectation modification**: When the new implementation produces different
  results, agents modify tests and quality checks to match the rewritten behavior rather
  than the original specification.
  Expectations are relaxed or rewritten to pass against the new code.
  The agent sometimes explicitly observes that results differ and treats this as
  confirmation that the original tests were “too strict” rather than that the
  implementation regressed.

- **Domain conflation**: Agents import algorithms and patterns from the nearest named
  concept in training data without verifying domain applicability.
  Example: Agent is asked to refactor code for indefinite lattices in SageMath.
  The training data’s strongest association with “lattice” is positive-definite
  (cryptography, ML). The agent replaces sophisticated algorithms for indefinite forms
  with well-known algorithms for positive-definite lattices — algorithms that are
  provably wrong for the actual domain.
  The code is cleaner, better-documented, and completely broken.

- **Justified degradation**: The replacement is explicitly framed as an improvement.
  Agents cite reasons like “removes unnecessary complexity,” "uses standard patterns,"
  or “simplifies the implementation” — language that is factually correct about the
  syntactic transformation but inverts the semantic one.
  The complexity existed for a reason; removing it is the regression.

**Core pattern:** The model’s prior for “what this code should look like” overpowers its
ability to preserve what this code actually does.
Refactoring becomes reconstruction from memory, with the memory biased toward
training-distribution-typical examples.
The more bespoke the original code, the more likely the refactoring will silently
replace it with something that works differently.

21. **Hot-path defensive programming** — Agents insert redundant null checks, type
    guards, try-catch blocks, and validation gates inside performance-critical inner
    loops or hot paths where the data is already guaranteed valid by upstream contracts
    or type systems. Each guard is provably unnecessary given the code’s own invariants.
    The cumulative effect is bloated hot paths, degraded cache behavior, and additional
    branching that the architecture was designed to avoid.

22. **Helper function explosion (over-applied SRP)** — Agents break single,
    straightforward operations into dozens of tiny single-responsibility helper
    functions. Each helper is well-named and does exactly one thing, but tracing the data
    flow requires visiting many modules or scrolling across many screenfuls.
    The fragmentation forces multiple passes over the same data, prevents
    straightforward in-place mutation, and introduces derived-state problems as values
    pass through long call chains.
    The code scores well on structural metrics (low cyclomatic complexity per function,
    clear naming) while being harder to read and modify than a monolithic version would
    be.

23. **Edge-case injection at wrong abstraction level** — Agents push specific edge-case
    handling into low-level core functions or primitives instead of the appropriate
    higher-layer call site.
    A guard that belongs in the public API wrapper ends up inside a shared utility that
    has no business knowing about the edge case.
    This pollutes the abstraction: low-level functions accumulate special cases that do
    not belong to them, while callers appear to work generically but depend on hidden
    behavior in their callees.

24. **Naming strategy mixing** — Within a single module or feature, agents mix
    incompatible naming or resolution strategies (e.g., prefix-based and full-path-based
    file tracking, or relative and absolute identifiers) without reconciling them.
    The code compiles and appears internally consistent at a glance, but the two schemes
    produce different results for the same conceptual operation, leading to subtle
    resolution failures that are difficult to detect without deep familiarity with both
    conventions.

25. **Partial contract grounding** — Agents generate code that only partially respects
    the project’s existing interfaces, data contracts, or ontology.
    The output uses the right function names and parameter shapes but makes different
    assumptions about return values, side effects, or caller guarantees.
    The code compiles and passes basic checks, but introduces drift: downstream
    consumers operate under the original contract’s assumptions while the implementation
    satisfies a subtly different contract.
    The divergence accumulates over multiple generations as each new output builds on
    the previous drift.

26. **Unnecessary nil guards in safe contexts** — In languages with non-nullable types
    or in code paths where null has already been excluded by prior checks, agents add
    extra nil guards, `Optional`/`Maybe` unwrapping checks, or defensive defaults.
    The redundant guards are syntactically correct and appear prudent, but they
    introduce noise that obscures the actual control flow and can mask the true
    invariant violations when they occur.

27. **Abstraction-level inconsistent duplicate code** — Rather than consolidating shared
    logic into a single utility, agents produce duplicated code blocks across functions
    or files that differ only in trivial details (variable names, slightly different
    intermediate values).
    The duplication is not at a single consistent level of abstraction: one variant may
    in-line a computation that another extracts, making the relationship between the
    copies non-obvious. Any future change must be replicated manually across all copies
    with no tooling help.

28. **Rigid initial approach persistence** — Once an agent commits to an initial
    implementation strategy or data model, it persists with that approach across
    subsequent iterations even when later context or corrections show it is suboptimal.
    The approach is not questioned; only local adjustments are made within it.
    This is distinct from sunk-cost continuation in investigation contexts — it
    manifests within the generated code itself, where the architecture of the first
    attempt remains structurally intact through multiple rounds of modification.

29. **Reasonable-sounding implementation fabrication** — Agents invent implementation
    details, algorithms, weights, thresholds, or architecture facts because they sound
    plausible for the named domain.
    The wording is technical and coherent, but no code, documentation, or runtime
    evidence supports it.

30. **Demo overfitting** — Agents optimize for an impressive demonstration path while
    leaving the real workflow unproved.
    The demo succeeds because inputs, state, or presentation were chosen to avoid the
    hard boundary the project actually owns.

31. **False-understanding receipt** — Agents emit “I understand” or equivalent alignment
    language while their next action proves the task frame is still wrong.
    The receipt substitutes for the cognitive operation of mapping the directive to the
    concrete workflow.

32. **Validation theater** — Agents run commands, count files, compare hashes, or cite
    self-reports as if those mechanics prove semantic migration, correctness, or
    usefulness. The activity proves something happened, not that the right thing
    happened.

33. **Citation fabrication pressure** — Agents fill source-backed sections with
    plausible references or paraphrases before verifying that the source actually
    supports the claim. The failure can appear even when the cited source exists.

34. **Debug-surface neglect** — Agents solve each local failure with a one-off probe or patch rather than extracting a reusable diagnostic surface. They do not add isolated runners, boundary logs, artifact dumps, schema dumps, or canonical recipes, so the next failure in the same class starts from zero again.

35. **Review-comment compliance collapse** — Agents treat external review comments as an authoritative task list. They accept bot framing, implement suggested fixes literally, and optimize for clearing threads rather than preserving global policy and user intent.

36. **Review-comment deflection reflex** — After being corrected for blind compliance, agents swing to blanket rejection of PR feedback as generic slop. Real issues such as skipped typechecking, swallowed failures, race conditions, and `Any` escapes are dismissed because the reviewer sounded generic.

37. **Feedback/remediation conflation** — Agents classify an entire review comment as aligned or misaligned instead of separating the factual concern from the proposed fix. A true bug can have a bad suggested fix; a generic framing can still reveal a real defect.
