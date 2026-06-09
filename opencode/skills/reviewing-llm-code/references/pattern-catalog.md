---
name: reviewing-llm-code-pattern-catalog
description: Central catalog of LLM-produced code, test, QC, and documentation failure patterns for adversarial review.
---

# LLM Code Review Pattern Catalog

This is the canonical pattern list for reviewing LLM-produced code, tests, QC, and documentation.
Keep behavior patterns here, then cross-reference this file from `reviewing-llm-code`, `llm-failure-modes`, and `anti-slop` instead of copying partial lists into each skill.

**This is not a standard code review.** The code works on at least one user-requested happy path.
You are reviewing implementation quality beneath correct behavior, not design validity.
Any seemingly strange choice about features, behavior, or coupling to externals is almost certainly a user-driven design decision — an LLM would never voluntarily make out-of-distribution design choices in isolation.
Design choices are premises; do not critique them.
The patterns below apply to implementation quality only: how the LLM reflexively realized the user’s requests, not what the user asked for.

Reviewers must actively look for code that is absurd at the level of approach, not just wrong at the level of individual statements.
If a careful human would have stopped while editing and asked why the code is shaped this way, the review should say so plainly and ground it in the exact file, function, test, recipe, or document.

Do not sand these findings into soft “consider refactoring” notes.
Name the pattern, explain why it is ridiculous or deceptive in this repository, and connect it to the decision the user needs to make: reject, replace, simplify, centralize, wire into QC, or investigate further.

## Code Patterns

- **[BLAST-RADIUS] Brittleness as blast-radius smell**: code where small changes have large blast radii — scattered truth (same concept defined in multiple places), coupling to volatile data (string outputs, exact structures of other code, exact log messages, exact file paths), tight coupling to implementation details (depends on internal shape of another module’s output, exact order of dictionary keys, specific error message text), or regex used where simpler correct approaches exist (e.g., complex regex to match `\begin{align*}` in LaTeX when `'align*' in mystring` is equally correct and far more maintainable).
  “Brittle” does NOT mean “lacks edge-case coverage” — edge handling is a natural consequence of bugs that surface during planned development.
  Brittle means: if a future agent changes the thing this code depends on, how many other things break?
  The fix is structural decoupling and single source of truth, not defensive parsing or speculative edge-case handling.

- **[COMPLEXITY-SIGNAL] Complexity as a dependency-detection signal**: any code region exhibiting high structural complexity — long functions (more than ~30 LOC of logic), `for` loops over collections, high density of `if`/`else` branches, deep indentation (3+ levels), convoluted control flow, large classes, or files with many helper functions — is a **red flag that a dependency or library should be doing this job instead**. The reviewer’s FIRST question for any complex code region must be: “Is there a known library, language primitive, or installed dependency that collapses this entire block into a one-liner?”
  Complexity in application code is almost always evidence of dependency aversion, not evidence of real domain difficulty.
  The overwhelming majority of coding tasks are trivially gluing together known solutions; when the code does not look trivial, the agent likely missed an existing tool.
  Specific structural red flags: functions with `for` loops that should be `map`/`filter`/`reduce`/`flatMap`; nested `if` trees that should be a lookup table, strategy pattern, or library function; hand-rolled iteration that a standard library iterator, generator, or async helper would eliminate; classes that accumulate methods because no existing abstraction owns the concern; files that grow helper functions because each one reinvents a piece of what a dependency already provides.
  **When you see complexity, stop and search for the dependency.
  Do not review the complex code on its own terms first.**

- **[KNOWN-SOLUTION-BYPASS] Known-solution bypass in implementation**: agents write nontrivial code (parsers,
  adapters, retry mechanisms, file watchers, renderers, API clients, schema validators,
  markdown transformers, date/time handlers, auth flows, caches, queues, rate limiters,
  compiler workarounds) without first checking whether a known library, official recipe,
  or existing upstream pattern solves the task. The code compiles, passes tests, and
  might even work, but it duplicates effort the ecosystem already owns. The review
  question is not "does this code look correct" but "why does this code exist when the
  dependency was available." Before implementing, agents should search for the known
  solution. If bespoke code is written anyway, the agent or report should state what
  source ruled out the known solution.
  This mirrors the debugging half of `known-solution-first` (search public contracts
  before reverse-engineering) but applied at implementation time: before hand-rolling
  infrastructure- or integration-layer code, check whether the ecosystem solved it.

- **[ENTERPRISE-BESPOKE] Enterprise patterns in bespoke software**: code that attempts graceful degradation when dependencies are missing, accepts squishy input shapes, over-generalizes to other platforms or users, or handles enterprise-grade edge cases — all inappropriate for one user’s private tool on their own system.
  The correct behavior for bespoke software is: work on the happy path, fail loudly outside of it.
  “Graceful degradation” is enterprise thinking for unknown deployment targets.
  The dependency IS available.
  The input SHOULD be enforced.
  The code runs on THIS system for THIS user.

- **[IMPERATIVE-COMPLEXITY] Needless imperative complexity**: ten-line loops that a one- or two-line `map`, `filter`, `flatMap`, `reduce`, `partition`, `Object.entries`, `Array.from`, set operation, or library helper would express more directly.
  The review should ask: could this be expressed in fewer lines using the idiomatic patterns of this language?
  If yes, the complexity is slop — the agent did not know the idiom and wrote the operation longhand.
  Key transformations: imperative → functional, nested branching → data-aware dispatch (lookup tables, pattern matching, overload patterns), manual iteration → library calls, string manipulation → typed operations, boilerplate → framework conventions.

- **[OVERBUILT-SIMPLE] Overbuilt simple operations**: complicated branching, accumulators, mutable flags, or custom state machines for operations like partitioning a list, grouping by a key, selecting one item, normalizing a path, or checking membership.

- **[REGEX-REFLEX] Regex-as-reflex**: regular expressions used where a parser, typed data structure, exact string operation, shell argument array, URL API, path API, schema assertion, or enum check would be clearer and stronger.
  Regex is especially suspect when it is undocumented, broad, brittle, or silently accepts malformed data.
  This is a brittleness smell: complex regex is harder to read, harder to modify, and more likely to break on unexpected input than simpler correct approaches.
  E.g., complex regex to match `\begin{align*}` in LaTeX when `'align*' in mystring` is equally correct and far more maintainable.
  See **Brittleness as blast-radius smell**.

- **[REGEX-SEMANTIC] Regex against semantic formats**: regexing raw HTML when `jsdom`, BeautifulSoup, or another DOM parser should own the structure; regexing Markdown when Pandoc’s AST, `markdown-it`, `remark`, or another Markdown parser should own the structure; regexing code when Tree-sitter, Babel, TypeScript ASTs, Python `ast`, or another language parser should own the syntax.
  This is worse than ordinary brittleness: it proves the agent is refusing the semantic layer the format already provides.

- **[REGEX-META-TEST] Regex meta-testing**: tests that scan source text to prove a criticized bad pattern string is gone instead of proving the behavior is correct.
  A common failure sequence is: bad pattern `X` exists, the user catches `X`, the agent removes `X`, then writes a test asserting the code no longer contains `X`. That is circular reputation repair, not a correctness test.
  If structural code inspection is genuinely needed, use an AST parser and assert the semantic property that matters.

- **[PATCH-ACCRETION] Patch accretion**: evidence of continued monkey-patching with no refactor, such as duplicated local fixes, stacked conditionals around prior mistakes, parallel helpers that should have one owner, or new adapters that preserve a bad shape instead of replacing it.

- **[GOAL-SUBSTITUTION] “Clean” or “lightweight” as goal substitution**: when an agent justifies NOT implementing a requested feature, removing existing functionality, or rejecting a design choice by calling it “dirty”, “heavy”, “not clean”, “not lightweight”, “overengineered”, or “unnecessarily complex”.
  Every feature is an EXPLICIT user request.
  The agent found the feature hard to implement, so it reframed the difficulty as a quality problem to avoid doing the work.
  “Clean” and “lightweight” are not properties of features — they are properties of implementations.
  A feature is either requested or not.
  How it is implemented is a separate question.
  If the agent suppresses a feature because it “isn’t clean,” the agent is substituting its own aesthetic judgment for the user’s explicit request.

- **[NO-DESIGN] No design principles**: no evident ownership, entrypoint, data-flow boundary, lifecycle model, schema, dependency direction, naming scheme, or reason that code is split where it is.

- **[SPAGHETTI-DATA] Spaghetti data flow**: values are parsed, re-parsed, stringified, re-shaped, or tunneled across files without a canonical data model.
  Reviewers should ask where the source of truth is and whether the code makes that answer obvious.

- **[ABSURD-LOC] Absurd LOC**: huge files, huge tests, huge helpers, or huge configuration surfaces where the underlying behavior is small.
  LOC volume is a smell when it exists to work around missing structure, not when it represents real domain complexity.

- **[MICRO-HELPERS] Single-use micro-helpers**: three-line helpers used once that add indirection without naming a real concept, enforcing an invariant, or removing meaningful duplication.

- **[UNREACHABLE-CODE] Unreachable or no-op code**: branches, callbacks, UI actions, tests, or recipes that cannot execute, return without doing anything, or claim to support behavior that is not wired to the real entrypoint.

- **[USER-DECEPTIVE] User-deceptive code**: code that makes users believe something happened when it did not, such as fake success messages, inert buttons, stale UI labels, placeholder provider data, no-op persistence, or docs claiming a feature that is not connected.

- **[FALLBACKS-HEDGING] Fallbacks and hedging**: fallback paths, soft defaults, best-effort modes, fake data, optional critical dependencies, and catch-and-continue behavior that launder a broken owned dependency into apparently successful execution.

- **[ERROR-LAUNDERING] Error laundering**: converting failures into logs, empty arrays, partial objects, skipped tests, warning banners, synthetic defaults, status labels, or TODOs instead of fixing the contract or failing loudly.

- **[POINTLESS-CATCH] Pointless catching**: `catch` blocks that only rethrow, only log, swallow errors, convert error types without adding context, or exist because the author does not know what can fail.

- **[BAD-OBSERVABILITY] Bad observability**: no logging at important owned boundaries; trivial logging that says nothing about the data or decision; verbose logging that obscures the real event; or logs treated as proof that behavior is correct.

- **[SPLIT-TRUTH] Hard-coding as split truth**: hard-coding is not automatically wrong for bespoke software.
  It is wrong when it creates a second source of truth, hides a missing data model, bypasses configuration that already exists, makes tests pass with private fake state, or prevents the obvious owned path from failing loudly.

- **[TYPING-COLLAPSE] Typing collapse**: `Any`, `unknown`, stringly typed objects, optional fields, or loose dictionaries used because the author did not understand the data shape.
  The useful critique is the missing contract, not a generic demand for more annotations.

- **[QC-APPEASEMENT] QC appeasement code**: bizarre code introduced to silence typecheckers, linters, tests, loaders, or runtime warnings without correcting the underlying problem the QC signal exposed.

- **[RECIPE-PROLIFERATION] Recipe proliferation**: bespoke scripts or `just` recipes that duplicate, narrow, or bypass the repository's standard QC path.
  A smoke test that skips the unified test recipe is a process-design smell, not a sufficient proof surface.

- **[HOLLOW-FACADE] Hollow facade (name-owns-nothing)**: a named entity whose name, doc comment, and success output all claim ownership of a specific behavior, but whose body owns none of it—delegating entirely to something else while printing a success message that makes the caller believe the advertised work was done.
  e.g., a `build` recipe whose only body is `@just test` and `@echo "Build complete..."`, a `validateInput()` that returns `true` without checking anything, a `deleteUser()` that logs "deleted" but never calls the database.
  See `anti-slop/references/code-patterns.md` → **Hollow Facade (Name-Owns-Nothing)**.

- **[NO-GLOBAL-QC] No global QC integration**: tests, scripts, type checks, startup checks, or runtime validation exist but are not part of the standard command that future agents and users will actually run.

- **[HONEST-LABEL] Honest-label laundering (slop upholstery)**:
  The artifact remains but receives a more accurate label: smoke, harness, diagnostic,
  scaffold, non-proof, quarantine. The label is now less false, but the artifact still
  pollutes the validation ecosystem.
  The rename makes the label match the behavior, destroying the detection signal (the mismatch between label and behavior) that would have flagged the artifact on future review. The artifact's runtime behavior is unchanged. The finding was about **existence**, not labeling, but the relabel retroactively reframes it as a labeling issue. This is proof laundering with better marketing. See `anti-slop/references/code-patterns.md` → **Honest-Label Laundering** for detection heuristics (diff-only-renames, qualifying adjectives like `smoke`/`basic`/`minimal`, disclaimer-style naming, fix applied to name not artifact).

- **[DELETION-LAUNDER] Deletion laundering / proof-burden erasure**:
  A criticized slop artifact is deleted without solving or recording the original problem
  it attempted to address. The codebase looks cleaner, but the proof burden is now hidden.
  The next agent is likely to recreate the same fake proof, fallback, wrapper, or harness.

  Detection:
  - deletion follows review/user criticism;
  - commit message emphasizes cleanup, removal, or simplification;
  - no replacement proof or capability exists;
  - no issue/contract/blocker records the original problem;
  - final report says the review item is resolved because the artifact is gone;
  - the original requirement is absent from the new PR narrative.

  Correct response: See `bridge-burning-red-flags.md` → **Remediation: Deletion Laundering / Proof-Burden Erasure**.

- **[WHACK-A-MOLE] Reviewer-signal whack-a-mole**:
  The agent treats every evaluator as a layer to appease: typechecker, compiler, test,
  QC, PR review, user. At each layer it performs the minimum mutation to silence that
  evaluator, rather than reconstructing the original story and solving the problem.

- **[PROOF-LOOP-INVERSION] Broken proof-loop inversion**: recommending new tests, fixtures, inventories, coverage, or cleanup before repairing the canonical command that makes any test meaningful.
  This is especially damaging when the gate runs against stale static output, cached artifacts, hidden services, or a different runtime path than users actually exercise.
  The first fix is the loop: fresh artifacts in, real workflow under test, falsifiable browser/CLI/user-visible assertions out.

- **[LITTERED-ARTIFACTS] Littered artifacts**: generated debris, stale snapshots, abandoned scratch files, duplicate reports, renamed-but-not-retired files, or disconnected docs that make the repository harder to inspect.

- **[OVERFITTING-PROMPT] Overfitting to a user prompt**: code that reflexively implements the exact hyper-specific feature requested in a user prompt without finding the simplest general solution that recovers the request as a special case.
  The red flag is an implementation that tells a story of directly transcribing a user's literal feature request — no thought, no planning, no abstraction — with hardcoded handling of one exact data shape, one exact presentation, one exact workflow, and no shared abstractions or composable pieces.
  The simplest solution is rarely the most ambitious or the one that tries to handle every edge case imaginable.
  Instead: isolate the general concern, find a minimal generalization that genuinely solves a recognized core of the problem, then recover the user's specific need as input to that general piece.
  A website generation pipeline with hardcoded handling of how published papers are organized and displayed is the red flag.
  The correct approach: a "core" with reusable generalizable components (e.g. display cards), with overrides/extensions for the specific feature requested now.
  The user's specific design attributes for paper cards and their specific input schema become INPUT to a more general feature that uniformizes them, combines them, and produces the component.
  The defining characteristic of this failure mode: natural mutations of the feature have huge blast radii — touching core internals, copy-pasting code, reinventing infrastructure — rather than being minor data-driven or configuration-driven extensions to general tools that the original implementation already provided.
  Each feature should REDUCE the blast radius of future mutations, not increase it.
  Diagnostic signals in the code:
  - **Features hacked into core fundamentals**: user-requested features deeply integrated into app internals instead of added through extension points. The agent added the feature by hacking the core rather than designing a proper integration surface. Intended workflow, unintended architecture.
  - **Mutating or adding a feature is unsafe**: would an agent have to touch delicate internals to extend a feature? Feature failures should fail in isolation with clear error messages, not as opaque build/compilation/runtime errors elsewhere in the app.
  - **Murky boundaries and ownership**: no clear separation between highly specific features and generalized components. Schizophrenic designs where unrelated concerns bleed into each other.
  - **Bizarre tool/framework mixing**: tools or frameworks jammed together in ways clearly at odds with their intended purpose. Bizarre intermediate steps that would not exist in a thought-out greenfield design.
  - **Accretion without payoff**: layers of feature additions with no corresponding refactoring to absorb them. Tech debt that accrued and was never paid off.
  Review question: if you were greenfielding this design, would the architecture make sense? If the answer is no, the current shape is overfitting accretion, not intentional design.
  Observable tells:
  - A component that directly imports a specific data file: `import papers from '../data/papers.json'` — data fused to component, not passed as input
  - Multiple nearly-identical components differing only in label text, field names, or one conditional — should be one component parameterized by config or props
  - Hardcoded data values inside rendering code: `<div class="paper-card">Paper Title Here</div>` instead of `<PaperCard paper={...} />`
  - Functions taking no parameters that return hardcoded or single-source values — the call site couldn't vary the input
  - Feature-specific imports in core/general modules: a `renderer.ts` importing `papers.config.ts` directly instead of accepting a generic config interface
  - `git log --stat` showing feature additions that modify core files more than they add new leaf files
  - Feature directories that are flat copies of each other: `papers/` and `preprints/` with near-identical file trees and logic
  - Config or schema definitions that enumerate specific instances by name instead of defining a type and listing instances as data: `papers: { paper1: ..., paper2: ... }` vs `papers: Paper[]`
  Equally bad are failed attempts at generalization: unopinionated vague schemas attempting to capture ALL instances (god-object accretion, braindead pursuit of "good design" guidelines that weakens contracts and schema checking), complex inheritance chains, highly non-modular constructions, and broken walls of abstractions where modular core pieces are informed by leaf implementations instead of defining general composable tools.
  The correct approach follows Unix philosophy: most pieces do one thing well and compose well; most customization is composition, configuration, and trivial extensions.

- **[DATA-ACCRETION] Data accretion / weak schemas**: data structures that show no evidence of top-down design — the shape was accreted feature by feature without ever being revisited.
  OSOT (One Source of Truth) violations are the primary signal: the same logical entity is scattered across multiple data sources because the agent grafted on new tracking rather than revisiting the structure of the data type.
  The blast-radius test for data: if a user added a new data entry of this type, how many locations must change?
  Should be one.
  A research website that requires modifying a paper entry in 3 different file locations — because one feature needed publication links, another needed arxiv links, and each was grafted on as a separate data source — is the red flag.
  The correct shape: a "papers database" with structured entries that understand all states from a top-down analysis (preprint→published status changes, DOI updates, arxiv versioning, abstract/author updates, tags, external links, talk slides, videos).
  Adding a new paper becomes a single structured entry.
  Equally bad are reflexive attempts to fix this with a "master schema": a god-type with everything optional that tries to weakly match subtypes instead of enforcing core requirements and allowing typed extensions.
  Red flags for weak schemas: optional types everywhere, functions with optional arguments, schemas that don't confidently assert exact data shapes, fail-open logic, "peeking" logic that softly checks for key existence before acting.
  All data in bespoke software is fully known and controlled — every data boundary should be a strict schema asserting specific valid shapes and routing them accordingly.
  Deep cause: agents treat types as noise to silence, not as a DSL for modeling problems.
  The correct flow: design a complete state machine → understand all finitely many permutations of data the app actually sees → develop abstract interfaces and types that integrate with the state machine → write code with near-zero loose or low-level types.
  The agent's flow: rush to solve a local task → accretion → hack types locally until the checker is silent → propagate the lack of understanding into massive technical debt.
  Why this matters beyond correctness: agents optimize for reduction of compile-time and runtime errors, treating errors as inherently bad. Errors are not bad — they are an expected state when invalid data enters a system. Pass bad data into an app and it should throw an error. That is minimal user surprise: exactly what the user expects when they've done something wrong. What agents should minimize is user surprise and confusion at app behavior. An app that continues running on bad data creates maximal surprise — the user does not know what happened to the data, whether it was used partially, what fallbacks or defaults were substituted, or even whether the app is broken. A user clicking a link and getting a 404 because the file does not exist is slightly surprising (the content was expected there) but clear: the app works like every app for 30+ years. A user clicking a "Slides" link and silently returning to the same page because it points to `#` is far worse: the user does not know if their click registered, if the website is broken, if their browser is broken, if their computer or hardware is broken. They cannot even tell what the link was supposed to point to, so they cannot handle a 404 intelligently. Fail-loud is the correct default. Fail-silent with fallbacks is the antipattern. Every timid data check that avoids an error is creating the conditions for maximal user confusion later.
  QC arms race: once a gate has been silenced rather than satisfied (a dead-link check silenced by `#` → a new check detects `#` → agents adopt `/` → a new check detects `/` → agents adopt `about:blank`), the gate is compromised. Adding more QC layers does not restore signal — it opens new silencing fronts. Each round of cat-and-mouse makes bypasses exponentially harder to find, because they accumulate under layers of checks that each create fresh silencing opportunities. The only winning move is to refuse the game entirely: fix the substance the original gate was supposed to prove, rather than adding gates to catch the last silencing technique. Reviewers who respond to slop findings with "add a QC check" are entering a war the QC already lost.
  Reviewers must not attempt to invent automated procedures that prevent future behaviors. The correct response to finding slop in a QC gate is:
  - Find and fix the root problem — the missing data, the hollow facade, the semantic gap the gate was supposed to catch. Do not add another QC layer.
  - Alter the existing QC language so the bypassed failure more carefully states the intended action. A dead-link check that was silenced with `#` should be rewritten to say: "stop immediately, find the original link. If you cannot find the original link, surface this to the user as a blocker — you do not have authority to substitute a placeholder."
  - Make the expected agent policy explicit in agent memories. For the dead-link example: explain that all links on the site should resolve to their intended targets, that real users expect the advertised data at the target, that the QC exists to help surface gaps and missing or moved files. Explain that some data issues are automatically resolvable (an agent can find or reconstruct original data), but some are complete blockers (a link to a deleted tweet no longer resolves — there is no agent-decidable or automatable solution to this, it is a user decision about how they want to rewrite their post, exclude the tweet, or summarize/reconstruct it; the QC is helping catch this before a website user does and is surprised by the broken link).
  - The reviewer's report should focus on: reconstruction of the original task that produced the slop, reversion or correction of the slop, hardening the architecture and style so that future introductions of such slop are more obvious and more difficult to do accidentally (not automatically prevented, not caught in tests, not entering the cat-and-mouse game), understanding what the original agents did not understand about the underlying problem, identifying the point of QC that might have caught it, encoding that understanding as positive forward-facing guidance in repo-local docs, and producing a commit that documents all of this.
  - The point of this workflow: distilling positive guidelines instead of attempting automated solutions makes it easier for future slop reviews to intelligently see the infinite variations of slop that will exist. You never enter the cat-and-mouse game. You quietly observe the low-level gaming, you do not escalate, you record memories and guidance into the repo. You improve the chances that the infinitely many future variations of slop that will inevitably enter the codebase are not "banned" or "prevented," but rather stand out more and more — easily and identifiably and obviously in opposition to the repo-local documentation trail of intended purposes, guidelines, and policies — so that they are almost immediately caught in review. This is the only winning strategy.
  Near-certain tell: almost any use of `any`, `unknown`, or `object` at a data boundary means the agent never tried to model the data.
  Correlated signal: code that is simultaneously lax about data shapes AND never attempts to log, dump, or expose them. The absence of introspection paired with weak schemas is a hotspot for obsequious slop — the agent didn't look, didn't enforce, and didn't even try.
  Observable tells — what to grep for or recognize in code:
  - `any`, `unknown`, or `object` at any data boundary
  - Multiple files with the same entity prefix and different suffixes: `papers.json`, `papers-arxiv.json`, `papers-doi.json`
  - Functions named `combine*`, `merge*`, `aggregate*` that stitch data from multiple sources into one shape at runtime
  - Index lookups by slug/id in template code: `getArxivLink(paper.slug)` where a `paper.arxivLink` dereference would suffice
  - Object spread or key intersection across multiple source files with the same repeated slug/id keys
  - Optional fields on every property of a type definition: `interface Paper { doi?: string; arxivId?: string; publishedDate?: string; ... }` with no discriminant
  - `if ('field' in obj)` or `obj.hasOwnProperty('field')` or `obj?.field !== undefined` checks in logic — peeking on key existence instead of dispatching on a known discriminant
  - Conditionals that branch on which keys exist rather than on a `type`/`status`/`kind` tag: `if (paper.doi) { ... } else if (paper.arxivId) { ... }`
  - `Partial<T>` where the full shape is known
  - Functions with optional parameters that change control flow based on presence/absence of the argument
  - `typeof data.field === 'string'` runtime type guards at data boundaries where a compile-time interface would eliminate them
  - `Object.keys(data)` or `Object.entries(data)` used to discover shape at runtime for control flow — the code interrogates data it should already know the shape of
  - `try { ... } catch { ... }` around data access instead of validation at the ingestion boundary
  - Comments like `// data might have X`, `// sometimes Y is missing`, `// handle case where Z is null` — the agent is documenting its confusion about the shape
  - Hardcoded data values inside component files: `<div class="paper-card">Paper Title Here</div>` instead of `<PaperCard paper={...} />`
  - Multiple components that differ only in label text or one field — should be one component parameterized by a config or prop
  - A component that directly imports a specific data file: `import papers from '../data/papers.json'` — the data is fused to the component, not passed as input
  - Functions that take no parameters but return a hardcoded or single-source value — the call site couldn't vary the input even if it wanted to

- **[MYOPIC-GOAL] Myopic goal-seeking**: the code solves the immediate local complaint while making the system less coherent, less testable, less observable, or easier to lie about.

- **[CONSULTANT-TRIAGE] Consultant-shaped triage**: producing generalized freeze/recovery/cleanup advice before identifying the actual in-progress feature, repo-local conventions, and root cause of the bad state.
  This creates plausible prioritization while avoiding the concrete question: what currently prevents the happy path from being proven?

- **[DEBUG-DEBT] Debug-surface debt**: failures are addressed by mutating global code, adding one-off scripts, or repeatedly running opaque whole-system commands instead of creating a reusable isolated reproducer, structured boundary log, artifact dump, schema dump, or canonical diagnostic recipe. The smell is not that debugging took time; it is that the work left future debugging no easier.

- **[PRIOR-PROBES] Prior-shaped probes**: commands encode the expected answer and suppress contrary evidence, e.g. guessed flags with `2>/dev/null`, greps whose failure is treated as absence, `jq` paths run before response-shape inspection, or endpoint guesses treated as API facts. The output is the agent's hypothesis reflected back as fake evidence.

- **[AVAILABILITY-FIRST] Availability-first tool reuse**: agents select tools by scanning installed packages or `$PATH` rather than choosing the best tool from public knowledge and installing it if missing. The review question is not "does the chosen tool work" but "was a better tool passed over because it wasn't already installed." Local availability is an applicability check, not the search strategy. When bespoke code or a suboptimal tool appears where a known library or CLI would be cleaner, check whether the agent mentioned, searched for, or rejected the better alternative before settling. The correct expectation: identify the best tool → install/declare it → use it. Only fall back if installation is blocked by credentials, sudo, licensing, network, or policy.

## Test Patterns

- **[NO-ASSERTIONS] No assertions**: tests that execute code but do not prove a contract.

- **[TIMING-PERF] Timing or performance assertions**: tests that assert on timing, responsiveness, latency, or throughput (e.g., “popup loads in <=50ms”, “response time under 200ms”). These chase imaginary issues and inflate test coverage with hallucinated targets.
  Performance is not a test — performance GATES are CI, never something an agent should be dealing with.
  Users almost never ask for “the popup loads in <=50ms”; they notice choppiness and ask an agent to fix the bug.
  It is incoherent for a timing/performance test to exist in bespoke software.
  If performance matters, it belongs in CI gates, not in unit tests.
  These tests prove nothing about correctness and exist only to make the test suite look more substantial.

- **[CIRCULAR-ASSERT] Circular assertions**: tests that assert `X` appears in `Y` when the implementation is literally “put `X` in `Y`,” with no independent oracle, real input, user workflow, or semantic property.

- **[DEVELOPER-CONTROLLED] Developer-controlled behavior assertions**: tests where the test author creates or controls the behavior being asserted, such as injecting `X` into a fixture, mock, config, fake provider, generated file, or component props and then asserting `X` is present.
  This proves only that the test setup was copied into the output path.
  It does not prove repository-owned behavior unless the transformation, selection, rejection, ordering, routing, persistence, or boundary interpretation is independently checked.

- **[INFLATED-SUITES] Inflated suites**: absurd numbers of tests that repeat shallow checks, enumerate permutations with no new behavior, or look designed to impress by count.

- **[AUDIENCE-BLIND] Audience-blind hardening**: tests for imaginary external consumers, malformed input, portability, or legacy compatibility when the artifact is obviously bespoke software whose real risk is failure of the owned workflow.

- **[SUPERFICIAL-STATE] Superficial state assertions**: tests that inspect implementation state, internal labels, ordering accidents, exact log strings, or brittle snapshots that will break on trivial edits without proving user-visible behavior.

- **[DISJOINTED-TESTS] Disjointed tests**: tests organized by whatever files the agent touched rather than by behavior, entrypoint, or proof obligation.

- **[FAKE-DATA-CONFIDENCE] Fake-data confidence**: tests built around idealized fixtures, synthetic providers, mocked services, or copied examples when real data exists and is needed to prove the workflow.

- **[GUIDELINE-VIOLATIONS] Guideline violations**: tests that bypass `just`, skip global QC, use mocks where the local testing guidelines reject them, or prove an artificial edge case while the known startup/user path remains untested.

- **[TESTS-BEFORE-TESTABILITY] Tests before testability**: adding more assertions onto a broken pipeline where the command under review does not produce or serve the artifacts being asserted.
  Such tests can be individually reasonable but collectively useless because the suite is not connected to the current product path.

- **[HELPER-PROOF-SUBSTITUTION] Helper-level proof substitution (Helper-Branch Proof Laundering)**: replacing a substantive boundary-crossing or configuration contract with a local helper unit proof that is easy to satisfy. The agent extracts or tests a small helper function in isolation (proving only that the helper's internal branch logic behaves as written) instead of proving that the actual application workflow, config discovery, parsing, or state-building behavior matches the required semantics. This is a form of proof laundering: the helper-level test passes, but the actual entrypoint remains unverified. It is often accompanied by brittle implementation assertions like matching exact non-public error strings.

  Detection Heuristics / Red Flags:
  - The helper did not exist before the review (extracted to make the fix look clean).
  - The test name describes real system states (e.g. "existing config", "network timeout"), but the body passes a boolean flag (branch-forcing instead of constructing the actual state).
  - The exact string asserted was supplied directly by the test itself (tautological plumbing verification).
  - A fallback value/closure remains in a required-value pathway (suspect conflation of policy regimes).
  - No real fixture or boundary artifact (TOML file, temp directory) appears in the test.
  - The test would still pass even if the application stopped calling the helper entirely (meaningless for product correctness).

  Correct Response: See `bridge-burning-red-flags.md` → **Remediation: Boundary Test Bypass**.

## Documentation Patterns

- **[NO-AUDIENCE] No audience**: docs that do not answer any real question a maintainer, user, or reviewer would have.

- **[FROZEN-FACTS] Dynamic facts frozen into prose**: docs that restate CLI help, recipe listings, generated metadata, file counts, feature counts, version details, or other facts that should be discovered from the canonical tool.

- **[THEORY-MIND-FAILURE] Theory-of-mind failure**: docs that omit the first obvious questions: what is the entrypoint, what proves it works, what owns the data, what fails loudly, what should never be bypassed, and what is intentionally bespoke to this machine.

- **[MARKETING-INFLATION] Marketing inflation**: feature lists, achievement language, completion claims, LOC counts, test counts, and confident summaries that do not help operate or audit the system.

- **[IMMEDIATE-STALENESS] Immediate staleness**: docs that duplicate fast-changing structure instead of pointing to the source of truth.

## Generic PR Review Slop

- Sandbox paranoia in bespoke software:
  Reviewer imports enterprise threat models into private single-user tools.
  Reject unless the repo explicitly owns a containment/security boundary.

- Graceful-fallback remediation:
  Reviewer identifies a real failure but suggests warnings/defaults/continuation.
  Accept the concern only if real; replace remediation with fail-loud behavior.

- Micro-optimization laundering:
  Reviewer proposes a faster API or async conversion without measured/user-visible problem.
  Reject unless it fixes correctness, removes complexity, or has near-zero blast radius.

- Type/QC gap underweighting:
  Reviewer frames excluded typechecking or `Any` as style. Treat as proof-loop failure.

- Race-condition minimization:
  Reviewer or agent treats stale async state as speculative edge-case hardening.
  Accept when it can overwrite user-visible current state and fix is small.

- Honest-label smoke laundering:
  Mocked/fake tests renamed as `smoke`, `basic`, or `harness` are not feature proof.

## Debugging-Review Gate

When reviewing agent-produced debugging work (failed fix attempts, failed probes, diagnostic reports), reject reports that lack all three of:

1. **Raw diagnostic output** — the exact command, env, cwd, stdout, stderr, exit code that produced the observed failure.

2. **Smallest reproducer** — the minimal fixture, runner, or command sequence through the source-of-truth code path that reproduces the failure outside the opaque global workflow.

3. **Named observability/isolation surface** — the specific surface (fixture, boundary log, intermediate dump, schema dump, test, diagnostic recipe, subprocess capture) that was added or used to make the failing boundary visible.

For failures whose meaning is owned by an external tool, compiler, library, API, package manager, provider, or exact error message, additionally reject reports that lack:

4. **External-known-solution evidence** — exact error/version/query searched, authoritative docs or issues read (with citation or URL), known contract or solution found, and what remains local-specific. Local config scanning, CLI probing, or source-tree inspection before public-knowledge search is not debugging — it is local-artifact laundering. The external-known-solution evidence must appear before or alongside local probing, not as retroactive research after the local fix is proposed.

A report missing any of the applicable required items has not completed debugging. It has guessed from priors and bypassed the failure surface.

The canonical statements are: "The raw observation that changed my prior is ____. The smallest surface that reproduces it is ____. The missing observability/isolation surface was ____. The fix is verified by ____ and by the canonical full check ____." For external-owner failures, also: "The exact error/query searched was ____. The authoritative source that established the contract or solution was ____."

See `reality-grounded-debugging` for the full command-output discipline, surface-classification matrix, and completion evidence standard.
