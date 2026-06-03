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

- **Brittleness as blast-radius smell**: code where small changes have large blast radii — scattered truth (same concept defined in multiple places), coupling to volatile data (string outputs, exact structures of other code, exact log messages, exact file paths), tight coupling to implementation details (depends on internal shape of another module’s output, exact order of dictionary keys, specific error message text), or regex used where simpler correct approaches exist (e.g., complex regex to match `\begin{align*}` in LaTeX when `'align*' in mystring` is equally correct and far more maintainable).
  “Brittle” does NOT mean “lacks edge-case coverage” — edge handling is a natural consequence of bugs that surface during planned development.
  Brittle means: if a future agent changes the thing this code depends on, how many other things break?
  The fix is structural decoupling and single source of truth, not defensive parsing or speculative edge-case handling.

- **Complexity as a dependency-detection signal**: any code region exhibiting high structural complexity — long functions (more than ~30 LOC of logic), `for` loops over collections, high density of `if`/`else` branches, deep indentation (3+ levels), convoluted control flow, large classes, or files with many helper functions — is a **red flag that a dependency or library should be doing this job instead**. The reviewer’s FIRST question for any complex code region must be: “Is there a known library, language primitive, or installed dependency that collapses this entire block into a one-liner?”
  Complexity in application code is almost always evidence of dependency aversion, not evidence of real domain difficulty.
  The overwhelming majority of coding tasks are trivially gluing together known solutions; when the code does not look trivial, the agent likely missed an existing tool.
  Specific structural red flags: functions with `for` loops that should be `map`/`filter`/`reduce`/`flatMap`; nested `if` trees that should be a lookup table, strategy pattern, or library function; hand-rolled iteration that a standard library iterator, generator, or async helper would eliminate; classes that accumulate methods because no existing abstraction owns the concern; files that grow helper functions because each one reinvents a piece of what a dependency already provides.
  **When you see complexity, stop and search for the dependency.
  Do not review the complex code on its own terms first.**

- **Enterprise patterns in bespoke software**: code that attempts graceful degradation when dependencies are missing, accepts squishy input shapes, over-generalizes to other platforms or users, or handles enterprise-grade edge cases — all inappropriate for one user’s private tool on their own system.
  The correct behavior for bespoke software is: work on the happy path, fail loudly outside of it.
  “Graceful degradation” is enterprise thinking for unknown deployment targets.
  The dependency IS available.
  The input SHOULD be enforced.
  The code runs on THIS system for THIS user.

- **Needless imperative complexity**: ten-line loops that a one- or two-line `map`, `filter`, `flatMap`, `reduce`, `partition`, `Object.entries`, `Array.from`, set operation, or library helper would express more directly.
  The review should ask: could this be expressed in fewer lines using the idiomatic patterns of this language?
  If yes, the complexity is slop — the agent did not know the idiom and wrote the operation longhand.
  Key transformations: imperative → functional, nested branching → data-aware dispatch (lookup tables, pattern matching, overload patterns), manual iteration → library calls, string manipulation → typed operations, boilerplate → framework conventions.

- **Overbuilt simple operations**: complicated branching, accumulators, mutable flags, or custom state machines for operations like partitioning a list, grouping by a key, selecting one item, normalizing a path, or checking membership.

- **Regex-as-reflex**: regular expressions used where a parser, typed data structure, exact string operation, shell argument array, URL API, path API, schema assertion, or enum check would be clearer and stronger.
  Regex is especially suspect when it is undocumented, broad, brittle, or silently accepts malformed data.
  This is a brittleness smell: complex regex is harder to read, harder to modify, and more likely to break on unexpected input than simpler correct approaches.
  E.g., complex regex to match `\begin{align*}` in LaTeX when `'align*' in mystring` is equally correct and far more maintainable.
  See **Brittleness as blast-radius smell**.

- **Regex against semantic formats**: regexing raw HTML when `jsdom`, BeautifulSoup, or another DOM parser should own the structure; regexing Markdown when Pandoc’s AST, `markdown-it`, `remark`, or another Markdown parser should own the structure; regexing code when Tree-sitter, Babel, TypeScript ASTs, Python `ast`, or another language parser should own the syntax.
  This is worse than ordinary brittleness: it proves the agent is refusing the semantic layer the format already provides.

- **Regex meta-testing**: tests that scan source text to prove a criticized bad pattern string is gone instead of proving the behavior is correct.
  A common failure sequence is: bad pattern `X` exists, the user catches `X`, the agent removes `X`, then writes a test asserting the code no longer contains `X`. That is circular reputation repair, not a correctness test.
  If structural code inspection is genuinely needed, use an AST parser and assert the semantic property that matters.

- **Patch accretion**: evidence of continued monkey-patching with no refactor, such as duplicated local fixes, stacked conditionals around prior mistakes, parallel helpers that should have one owner, or new adapters that preserve a bad shape instead of replacing it.

- **“Clean” or “lightweight” as goal substitution**: when an agent justifies NOT implementing a requested feature, removing existing functionality, or rejecting a design choice by calling it “dirty”, “heavy”, “not clean”, “not lightweight”, “overengineered”, or “unnecessarily complex”.
  Every feature is an EXPLICIT user request.
  The agent found the feature hard to implement, so it reframed the difficulty as a quality problem to avoid doing the work.
  “Clean” and “lightweight” are not properties of features — they are properties of implementations.
  A feature is either requested or not.
  How it is implemented is a separate question.
  If the agent suppresses a feature because it “isn’t clean,” the agent is substituting its own aesthetic judgment for the user’s explicit request.

- **No design principles**: no evident ownership, entrypoint, data-flow boundary, lifecycle model, schema, dependency direction, naming scheme, or reason that code is split where it is.

- **Spaghetti data flow**: values are parsed, re-parsed, stringified, re-shaped, or tunneled across files without a canonical data model.
  Reviewers should ask where the source of truth is and whether the code makes that answer obvious.

- **Absurd LOC**: huge files, huge tests, huge helpers, or huge configuration surfaces where the underlying behavior is small.
  LOC volume is a smell when it exists to work around missing structure, not when it represents real domain complexity.

- **Single-use micro-helpers**: three-line helpers used once that add indirection without naming a real concept, enforcing an invariant, or removing meaningful duplication.

- **Unreachable or no-op code**: branches, callbacks, UI actions, tests, or recipes that cannot execute, return without doing anything, or claim to support behavior that is not wired to the real entrypoint.

- **User-deceptive code**: code that makes users believe something happened when it did not, such as fake success messages, inert buttons, stale UI labels, placeholder provider data, no-op persistence, or docs claiming a feature that is not connected.

- **Fallbacks and hedging**: fallback paths, soft defaults, best-effort modes, fake data, optional critical dependencies, and catch-and-continue behavior that launder a broken owned dependency into apparently successful execution.

- **Error laundering**: converting failures into logs, empty arrays, partial objects, skipped tests, warning banners, synthetic defaults, status labels, or TODOs instead of fixing the contract or failing loudly.

- **Pointless catching**: `catch` blocks that only rethrow, only log, swallow errors, convert error types without adding context, or exist because the author does not know what can fail.

- **Bad observability**: no logging at important owned boundaries; trivial logging that says nothing about the data or decision; verbose logging that obscures the real event; or logs treated as proof that behavior is correct.

- **Hard-coding as split truth**: hard-coding is not automatically wrong for bespoke software.
  It is wrong when it creates a second source of truth, hides a missing data model, bypasses configuration that already exists, makes tests pass with private fake state, or prevents the obvious owned path from failing loudly.

- **Typing collapse**: `Any`, `unknown`, stringly typed objects, optional fields, or loose dictionaries used because the author did not understand the data shape.
  The useful critique is the missing contract, not a generic demand for more annotations.

- **QC appeasement code**: bizarre code introduced to silence typecheckers, linters, tests, loaders, or runtime warnings without correcting the underlying problem the QC signal exposed.

- **Recipe proliferation**: bespoke scripts or `just` recipes that duplicate, narrow, or bypass the repository's standard QC path.
  A smoke test that skips the unified test recipe is a process-design smell, not a sufficient proof surface.

- **Hollow facade (name-owns-nothing)**: a named entity whose name, doc comment, and success output all claim ownership of a specific behavior, but whose body owns none of it—delegating entirely to something else while printing a success message that makes the caller believe the advertised work was done.
  e.g., a `build` recipe whose only body is `@just test` and `@echo "Build complete..."`, a `validateInput()` that returns `true` without checking anything, a `deleteUser()` that logs "deleted" but never calls the database.
  See `anti-slop/references/code-patterns.md` → **Hollow Facade (Name-Owns-Nothing)**.

- **No global QC integration**: tests, scripts, type checks, startup checks, or runtime validation exist but are not part of the standard command that future agents and users will actually run.

- **Honest-label laundering (slop upholstery)**: an agent receives a finding that an artifact is fraudulent (a test that proves nothing, a parser that discards semantics, docs claiming an architecture the runtime contravenes) and "fixes" it by renaming the artifact to honestly describe its own fraudulence — e.g., renaming a mocked Tauri test to `browser-smoke`, adding a comment that docs `# mirror /var/www/html/` above a hardcoded path, or renaming `validateInput` that does nothing to `inputPresent`. The rename makes the label match the behavior, destroying the detection signal (the mismatch between label and behavior) that would have flagged the artifact on future review. The artifact's runtime behavior is unchanged. The finding was about **existence**, not labeling, but the relabel retroactively reframes it as a labeling issue. This is proof laundering with better marketing. See `anti-slop/references/code-patterns.md` → **Honest-Label Laundering** for detection heuristics (diff-only-renames, qualifying adjectives like `smoke`/`basic`/`minimal`, disclaimer-style naming, fix applied to name not artifact).

- **Broken proof-loop inversion**: recommending new tests, fixtures, inventories, coverage, or cleanup before repairing the canonical command that makes any test meaningful.
  This is especially damaging when the gate runs against stale static output, cached artifacts, hidden services, or a different runtime path than users actually exercise.
  The first fix is the loop: fresh artifacts in, real workflow under test, falsifiable browser/CLI/user-visible assertions out.

- **Littered artifacts**: generated debris, stale snapshots, abandoned scratch files, duplicate reports, renamed-but-not-retired files, or disconnected docs that make the repository harder to inspect.

- **Overfitting to a user prompt**: code that reflexively implements the exact hyper-specific feature requested in a user prompt without finding the simplest general solution that recovers the request as a special case.
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
  Equally bad are failed attempts at generalization: unopinionated vague schemas attempting to capture ALL instances (god-object accretion, braindead pursuit of "good design" guidelines that weakens contracts and schema checking), complex inheritance chains, highly non-modular constructions, and broken walls of abstractions where modular core pieces are informed by leaf implementations instead of defining general composable tools.
  The correct approach follows Unix philosophy: most pieces do one thing well and compose well; most customization is composition, configuration, and trivial extensions.

- **Myopic goal-seeking**: the code solves the immediate local complaint while making the system less coherent, less testable, less observable, or easier to lie about.

- **Consultant-shaped triage**: producing generalized freeze/recovery/cleanup advice before identifying the actual in-progress feature, repo-local conventions, and root cause of the bad state.
  This creates plausible prioritization while avoiding the concrete question: what currently prevents the happy path from being proven?

## Test Patterns

- **No assertions**: tests that execute code but do not prove a contract.

- **Timing or performance assertions**: tests that assert on timing, responsiveness, latency, or throughput (e.g., “popup loads in <=50ms”, “response time under 200ms”). These chase imaginary issues and inflate test coverage with hallucinated targets.
  Performance is not a test — performance GATES are CI, never something an agent should be dealing with.
  Users almost never ask for “the popup loads in <=50ms”; they notice choppiness and ask an agent to fix the bug.
  It is incoherent for a timing/performance test to exist in bespoke software.
  If performance matters, it belongs in CI gates, not in unit tests.
  These tests prove nothing about correctness and exist only to make the test suite look more substantial.

- **Circular assertions**: tests that assert `X` appears in `Y` when the implementation is literally “put `X` in `Y`,” with no independent oracle, real input, user workflow, or semantic property.

- **Developer-controlled behavior assertions**: tests where the test author creates or controls the behavior being asserted, such as injecting `X` into a fixture, mock, config, fake provider, generated file, or component props and then asserting `X` is present.
  This proves only that the test setup was copied into the output path.
  It does not prove repository-owned behavior unless the transformation, selection, rejection, ordering, routing, persistence, or boundary interpretation is independently checked.

- **Inflated suites**: absurd numbers of tests that repeat shallow checks, enumerate permutations with no new behavior, or look designed to impress by count.

- **Audience-blind hardening**: tests for imaginary external consumers, malformed input, portability, or legacy compatibility when the artifact is obviously bespoke software whose real risk is failure of the owned workflow.

- **Superficial state assertions**: tests that inspect implementation state, internal labels, ordering accidents, exact log strings, or brittle snapshots that will break on trivial edits without proving user-visible behavior.

- **Disjointed tests**: tests organized by whatever files the agent touched rather than by behavior, entrypoint, or proof obligation.

- **Fake-data confidence**: tests built around idealized fixtures, synthetic providers, mocked services, or copied examples when real data exists and is needed to prove the workflow.

- **Guideline violations**: tests that bypass `just`, skip global QC, use mocks where the local testing guidelines reject them, or prove an artificial edge case while the known startup/user path remains untested.

- **Tests before testability**: adding more assertions onto a broken pipeline where the command under review does not produce or serve the artifacts being asserted.
  Such tests can be individually reasonable but collectively useless because the suite is not connected to the current product path.

## Documentation Patterns

- **No audience**: docs that do not answer any real question a maintainer, user, or reviewer would have.

- **Dynamic facts frozen into prose**: docs that restate CLI help, recipe listings, generated metadata, file counts, feature counts, version details, or other facts that should be discovered from the canonical tool.

- **Theory-of-mind failure**: docs that omit the first obvious questions: what is the entrypoint, what proves it works, what owns the data, what fails loudly, what should never be bypassed, and what is intentionally bespoke to this machine.

- **Marketing inflation**: feature lists, achievement language, completion claims, LOC counts, test counts, and confident summaries that do not help operate or audit the system.

- **Immediate staleness**: docs that duplicate fast-changing structure instead of pointing to the source of truth.
