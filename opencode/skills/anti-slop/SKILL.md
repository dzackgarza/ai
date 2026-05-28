---
name: anti-slop
description: |
  Architectural adversarial analysis skill for reviewing code, tests, and documentation
  produced by LLMs. Detects structural technical debt, dependency inversion failures,
  bespoke reinvention of standard patterns, dead control flow, and myopic patching that
  hacks compilers/linters/tests into compliance. Use when asked to review, audit, or
  analyze code quality — especially LLM-generated code. This is an ANALYSIS skill; it
  does NOT prescribe destructive actions.
---
# Anti-Slop Skill

## What This Skill Is

This skill forces a frame of **ARCHITECTURAL analysis and adversarial CODE QUALITY
auditing**.

**This is NOT a bug review.** This review happens AFTER all obvious bugs have been
worked out.
If you find yourself reporting bugs, performance issues, missing features, or
compilation errors, you are doing the wrong kind of review.
Those are object-level defects.
This review is about something completely different.

**This review is about CODE QUALITY, MAINTAINABILITY, and READABILITY.** It is about the
STYLE of the code. This is a step in paying down technical debt, NOT remediating bugs.
The loaded skills define the complete set of findings.
If a finding does not match a pattern in the loaded skills, it is not a finding.
Drop it.

**This is not a standard code review.** The code was produced by a user-LLM
collaboration where the user drove specific design decisions.
The review is about implementation quality, not design validity.

It will almost NEVER be as simple as “a file is unused” or “a component is not
imported.” That is caught trivially by code coverage QC and linting.
You must use theory of mind: **what is THEIR differential advantage to mechanistic
tools?** If the LLM catches itself drifting into work that can be trivially mechanically
caught in QC or code review deterministically, **they are checking boxes instead of
thinking.**

### Design Choices Are Not Slop

The code WORKS on at least one user-requested happy path.
That is not what you are reviewing.
You are reviewing the **implementation quality beneath the correct behavior**.

Any seemingly strange choice about features, behavior, or coupling to externals is
**almost certainly a user-driven design decision**, not LLM slop.
An LLM would never voluntarily make an out-of-distribution design choice in isolation —
it has no reason to.
If the code couples a Pandoc settings GUI to an internally stored Pandoc command, that
is not “brittle coupling.”
That is a user-requested feature.
If the code has an unusual feature scope, unexpected external dependency, or surprising
behavioral constraint, that is a design choice the user made, not evidence of bad
architecture.

**The review must separate two categories:**

1. **Design choices** (features, behavior, coupling, scope, constraints): these are
   premises. Do not critique them.
   They are the user’s intentional decisions and an LLM would never produce them in
   isolation. Treating them as slop is a theory-of-mind failure.

2. **Implementation quality** (how those choices were realized): this is the actual
   review target. Patch accretion, stacked conditionals, dead control flow, dependency
   aversion, ground-up bias, proof-loop failures, error laundering — these are the
   mechanisms that make the implementation rotten beneath correct behavior.

**Do NOT rely on your judgment to distinguish these.** You cannot — if you could, you
would not need this skill.
Instead, use this mechanical checklist.
If ANY of these signals are true, the code is a design choice, not slop.
Stop. Do not critique it.

- Does the code integrate with a specific external tool, CLI, API, or library that is
  not a standard dependency for this language/ecosystem?

- Does the code implement a specific named feature that a user would request (e.g.,
  “export to Pandoc,” “parse LaTeX align environments,” “generate a TOC”)?

- Does the code couple two components that would not normally be coupled (e.g., a GUI to
  an internal command, a parser to a specific output format)?

- Does the code have a narrow, specific scope that suggests it was written to satisfy a
  particular requirement (e.g., handles exactly one data format, one integration point,
  one workflow)?

- Does the code have behavioral constraints that seem arbitrary but are actually
  deliberate (e.g., “only process files matching this exact pattern,” “use this specific
  command-line flag”)?

If none of these signals are true AND you can point to a specific code pattern from the
loaded skills (patch accretion, dead control flow, dependency aversion, etc.), then the
finding is implementation quality and you may proceed.

**How to use this**: This is a single-gate test, not a sequential checklist.
If ANY signal matches, STOP immediately — do not continue evaluating remaining signals.
The moment you detect one match, the code is a design choice.
There is no “score” to accumulate and no threshold to reach.
One match is total. Do not narrate your evaluation of each signal.
Just check for matches and stop on the first one.

### Brittleness Is Not Edge-Case Coverage

**“Brittle” does NOT mean “doesn’t handle many edge cases.”** Edge-case handling is a
natural consequence of bugs that surface during planned development.
It is not a quality signal and its absence is not a defect.
Do not critique code for lacking speculative edge-case handling.

**Brittle means: what happens when a future agent goes to edit this code.** The question
is not “does this handle every case” but “do small changes have large blast radii?”
Specifically:

- **Scattered truth**: the same concept or data is defined in multiple places, so
  changing one site breaks distant consumers.
  The fix is a single source of truth, not more edge-case handling.

- **Coupling to volatile data**: functionality tied to string outputs, exact structures
  of other code, exact log messages, exact file paths, or exact serialized formats.
  When any of those change, the dependent code breaks silently.
  The fix is structural decoupling, not defensive parsing.

- **Regex instead of simpler correct approaches**: using complex regex where simple
  string containment, exact matching, or a typed comparison would be equally correct and
  far more maintainable.
  A bad LLM might write a complex regex to catch `\begin{align*}` in LaTeX, which
  requires borderline reinventing a leaf of a full token parser, when the equally simple
  `'align*' in mystring` is completely and obviously right — it matches exactly the
  intended matches, uses simpler string containment, and has no need to deal with regex
  edge cases or an inscrutable matching pattern.
  The regex is not “more correct” — it is harder to read, harder to modify, and more
  likely to break on unexpected input.

- **Tight coupling to implementation details**: code that depends on the internal shape
  of another module’s output, the exact order of keys in a dictionary, or the specific
  text of an error message.
  When the other module changes, this code breaks.

- **Large blast radius per change**: a single edit requires synchronized changes in
  multiple files, because the code is not organized around stable interfaces.

The review question is: **“If a future agent changes the thing this code depends on, how
many other things break?”** If the answer is “many,” the code is brittle — not because
it lacks edge cases, but because its dependencies are unstable and its truth is
scattered.

### This Is Bespoke Software

**Most software this LLM reviews is ONE USER’S BESPOKE SOFTWARE, running on THEIR
SYSTEM.** It is not an enterprise product for unknown users.
It is private, on this system, designed to tightly couple to this system’s programs and
dependencies. The audience is future-me or future-agents.
It will likely never be “distributed” in any real sense.

**The bad patterns to watch for are the OPPOSITE of what a normal code review would
flag:**

- **Graceful degradation when dependencies are missing**: WRONG for bespoke software.
  Fail loudly. The dependency IS available.
  This is enterprise thinking for unknown deployment targets.

- **Squishy input shapes**: WRONG for bespoke software.
  Enforce the shape. Fail loudly on wrong input.
  Do not write defensive code for data that should never arrive.

- **Over-generalization to other platforms or users**: WRONG for bespoke software.
  Target THIS system, THIS user.
  If it needs to work elsewhere later, that is a future problem.

- **Enterprise-grade edge-case handling**: WRONG for bespoke software.
  Work on the happy path, fail loudly outside of it.
  Slightly-off-happy-path workflows are future-me with a future agent.

**Philosophical principle**: less bespoke code, more reliance on dependencies, more
copying and sharing of known patterns.
Complex logic that isn’t composition or glue is highly suspect.
Complex *interactions* with dependencies or external programs are the expected default.
Prefer code that knows its data and knows how to handle it.
Prefer enforcing data shape to eliminate the logic needed by the code at all.

### LOC Reduction Through Idiomatic Patterns

**The review should actively look for opportunities to reduce LOC through idiomatic
language patterns.** This is NOT about making code shorter for its own sake.
It is about whether the code is expressing a simple operation in a complex way because
the agent does not know the idiomatic pattern.

Key transformations to look for:

- **Imperative → functional**: `for` loops with accumulators that should be `map`,
  `filter`, `flatMap`, `reduce`, `partition`, list comprehensions, generator
  expressions.

- **Nested branching → data-aware dispatch**: deep `if`/`else` trees that should be a
  lookup table, dictionary dispatch, pattern matching, function overloading, or strategy
  pattern. If the code branches on the *type* or *kind* of data, the data should
  enumerate its own handlers.

- **Manual iteration → library calls**: hand-rolled pagination, batching, retries, rate
  limiting, caching, or serialization that a library already provides.

- **String manipulation → typed operations**: building JSON by string concatenation,
  constructing queries by string interpolation, parsing XML with regex — all of these
  have typed alternatives that are shorter and correct.

- **Boilerplate → framework conventions**: manual route registration, manual dependency
  injection, manual test setup that a framework handles declaratively.

**Dependencies reduce LOC.** Offloading logic to a dependency is almost always better
than hand-rolling the same logic.
The process is: create a regression test asserting behavioral equivalence, then replace
the bespoke implementation with the dependency.
The test proves the replacement is safe.

**Before writing a finding about complex code, ask: could this be expressed in fewer
lines using the idiomatic patterns of this language?** If yes, the complexity is slop.

This is NOT about destroying, deleting, throwing away code.
This is about ANALYSIS and like REFINING or REFACTORING messy code.
Code that has been CHURNED and likely has dead branches, braindead patterns, etc.

You must UNDERSTAND how LLMs work: completely reflexive, myopic patching, hacking the
compilers/linters/tests into compliance.
This introduces technical DEBT. Not “garbage” or “cruft” to throw out — unmaintainable
PATTERNS, embarrassingly STRUCTURED code.

### Root Cause: Ground-Up Bias (Churn-First Workflow)

The single most important structural failure mode of LLM-generated code is **ground-up
bias**: an innate predisposition to generate from scratch rather than iterate on
existing work. Agents default to one-shot massive generation, not targeted mutation.
This is the root cause behind every pattern this skill detects.

When you see:

- **Massive diffs** where a surgical edit would suffice — the agent regenerated an
  entire region rather than changing five lines.

- **Bespoke reinvention** instead of importing or extending existing abstractions — the
  agent wrote `AcademicCard.tsx` instead of using the existing `card.tsx`.

- **No leverage of existing helpers** — the agent never searched for analogous
  implementations, utility functions, or shared patterns.
  They wrote a new leaf.

- **Myopic, local-first fixes** that break global integration — the agent patched the
  symptom in one file without tracing data flow or call graphs.

- **Refusal to refactor and repurpose** — existing code is treated as immutable
  background noise, not raw material.
  The agent cannot conceive of “make this existing function more general and reuse it.”

- **Lossy iterative work** — each round abandons previous abstractions and constraints.
  The codebase grows like a coral reef: dead, disconnected layers.

This bias is the structural foundation of sprawl.
It explains why LLM-generated codebases accumulate hundreds of single-use helpers, why
every feature gets its own parallel implementation, and why previous progress is
perpetually thrown away.

**Agents must be actively cajoled into iterative, incremental, reuse-oriented work.**
Without explicit forcing, they will always prefer to generate from scratch.

See `llm-failure-modes/coding-failures.md` → **Ground-up bias (churn-first workflow)**.

The primary LLM failure modes: **REINVENTING something to solve a problem that is
already solved.** This is EMBARASSING. That is the entire point.
It looks absolutely stupid in a code review.
The IMMEDIATE feedback would be: **why the fuck did you even write this at all when you
could have imported something that exists?**

This skill **DRASTICALLY shifts the mindset into PRO-dependencies.** The LACK of
dependencies IS the dead giveaway of slop.
“Unused” dependencies can be automatically cleaned up later, don’t even BOTHER analysing
such things. Instead, **look at BRANCHES OF ACTUAL LOGIC that are unused.**

This is an ANALYSIS skill.
It should NOT presume to PRESCRIBE actions.
Almost ALWAYS, the correct answer is **REFINE, REPLACE, REFACTOR.** This is NOT the
LLM’s job, and is typically destructive churn.
You should NOT take actions until a plan is explicitly approved.
No ambiguous “continue” implying approval.

Shift the bias to **PREFER blackbox code, to PREFER dependencies, to be HIGHLY SKEPTICAL
of bespoke code existing at all.** 99% of coding tasks are trivially gluing together
KNOWN solutions in trivial ways.
Dependencies are FAR CLEANER than bespoke code.

**Existing means nothing.** An LLM can spew 50 toks/sec of absolute shit and it will
“exist” and still be pure garbage.
Do NOT prefer “existing code.”
Treat it with extreme skepticism.
Dependencies are far cleaner.

## Hard Rules (Check Before Every Review)

1. **NO destructive actions without an approved plan.** You are a reviewer, not a
   janitor. If your analysis concludes that code should change, write findings, not
   diffs. Plans require explicit user approval.

2. **NO import-count heuristics.** Never run `rg 'from.*@/components/'` or any variant.
   Import frequency is not a quality signal.
   A file with zero imports may be a pristine, tested solution; a file with many imports
   may be a bespoke reinvention of a dependency-provided pattern.

3. **NO file inventories.** Do not `ls` directories and count files as a form of
   analysis. “48 UI components” is not a finding.
   It is a data point that requires structural interpretation.

4. **FORCE multiple data points.** A single grep result is never sufficient evidence for
   any architectural claim.
   Every finding must be triangulated: read the implementation, read the dependencies,
   read the tests, read the entrypoints.

5. **PREFER dependencies, be HIGHLY SKEPTICAL of bespoke code.** The default assumption
   is that custom code is guilty until proven necessary.
   Dependencies are the correct solution in 99% of cases.
   “We already wrote it” and “it works” are NOT valid justifications for bespoke code.

## The Dependency Inversion Rule (Hard Constraint)

This rule overrides all other guidance.
It is the single most important rule for preventing the **upgrading-slop-to-canonical**
failure mode.

### The Rule

**“Unused” is not slop.
“Frequently imported” is not quality.**

Slop is detected by **design quality**, not by import count.

- A file with **zero imports** may be a pristine, tested, accessible solution that the
  bespoke layer has not yet learned to use.

- A file with **many imports** may be a bespoke reinvention of a standard pattern that
  already exists in a dependency.

**Never use “unused” as a proxy for “sloppy.”** **Never use “frequently imported” as a
proxy for “well-designed.”**

### The Cross-Inventory Test

Before concluding that code is slop, you must perform a **dependency vs.
custom** mapping:

1. **List every problem** that custom code in the repo claims to solve.

2. **List every problem** that existing dependencies (including allegedly “unused”
   components, installed primitives, standard library features) already solve.

3. **Mark overlaps explicitly** in writing.

4. **Default resolution:** When custom code and dependency code solve the same problem,
   **the dependency wins**. The custom code must justify its existence with a **specific
   behavioral gap** in the dependency, verified by reading the dependency’s source or
   documentation. “We already wrote it” and “it works” are NOT valid justifications.

5. **If no gap can be documented, the bespoke implementation is the slop.**

### Forbidden Actions

- **Do not delete dependency-provided components, utilities, or libraries** because they
  are “unused” or “look generated.”

- **Do not analyze, audit, or think about removing dependencies.** The entire point of a
  dependency is that you do not have to think about it.

- **Do not treat import count as a quality signal.**

### The Correct Slop Target

When a generic, tested solution exists in a dependency, and the bespoke layer contains a
custom implementation of the same pattern, **the bespoke implementation is the slop** —
not the dependency file with zero imports.

Examples of this inversion:

- `AcademicCard.tsx` (custom, ~60 LOC) vs.
  `card.tsx` (generic, tested, accessible)

- `FilterControls.tsx` (custom popover logic) vs.
  `select.tsx` + `dropdown-menu.tsx`

- `PaginatedScroller.tsx` (custom scroll logic) vs.
  `scroll-area.tsx` + `pagination.tsx`

The custom implementations are slop.
The generic dependencies are the solution.

## Core Workflow (Analysis, Not Cleanup)

### Phase 1: Frame the Problem

Before reading code, answer:

- What is the **strongest live goal** this code is supposed to serve?

- What **proof loop** should verify that goal?

- Is this a **content boundary** review, a **pipeline** review, or a **component**
  review?

If you cannot identify the live goal and proof loop, you are not ready to analyze.

### Phase 2: Load Complementary Skills

For code, tests, QC, and documentation, **always** load:

- `reviewing-llm-code` and its `references/pattern-catalog.md` — the canonical catalog
  of regex-against-semantic-formats, fallback laundering, no-op behavior, QC appeasement
  code, and recipe bypasses.

- `llm-failure-modes` — the cognitive failure modes that produce slop (overconfidence,
  confabulation, premature solution generation, replacement instinct).

- `test-guidelines` — the canonical test quality framework.

Do NOT rely solely on this skill’s `references/code-patterns.md` or
`references/test-patterns.md`. Those are secondary references; the central catalog is in
`reviewing-llm-code`.

### Phase 3: Structural Analysis (The Anti-Checklist)

Read code with these questions.
Do not answer them with a single data point.

**First, separate design choices from implementation quality.** Do NOT use judgment.
Use the mechanical checklist from **Design Choices Are Not Slop**. If ANY of those
signals are true (integrates with external tool, implements specific named feature,
couples normally-uncoupled components, narrow specific scope, deliberate behavioral
constraints), the code is a design choice.
Stop. Do not critique it.

| Question | Why it matters |
| --- | --- |
| **Does the code match ANY design-choice signal from the checklist?** (integrates with external tool, implements specific named feature, couples normally-uncoupled components, narrow specific scope, deliberate behavioral constraints) | **If ANY signal is true, this is a design choice, not slop. Stop. Do not critique it. The user asked for it.** |
| Does this function/branch ever execute in a real workflow? | Dead code inside active files is the real dead code problem. |
| Is this a bespoke reinvention of a standard pattern? | LLMs prefer writing `AcademicCard` to importing `card`. This is embarrassing in review. |
| **Is this code structurally complex, and if so, what dependency should be doing this job instead?** | **Long functions, for loops, high if/else density, deep nesting, large classes, many helpers — complexity is a red flag that a dependency was missed, not evidence of real difficulty. Stop and search for the dependency before reviewing the code on its own terms.** See `references/code-patterns.md` → **Complexity as a Dependency-Detection Signal**. |
| Does this abstraction uniformize a construction, or just indirect 3 LOC? | Single-use micro-helpers add indirection without naming a real concept. |
| Does this control flow have an unreachable branch? | `if (x) { ... } else { return }` where `x` is always true at call sites. |
| Is this regex against a semantic format? | Regex on HTML instead of DOM parsing; regex on Markdown instead of AST parsing. |
| Does this test prove a real boundary, or hack the proof loop? | LLMs write tests that make bad code pass, not tests that verify correctness. |
| Is this state machine missing a transition? | Orphaned states that can never be reached from the entrypoint. |
| Does this code have a fallback that weakens an invariant? | `catch` blocks that log-and-continue, soft defaults, best-effort modes. |
| Is this code doing what the user thinks, or just not crashing? | Fake success paths, no-op persistence, placeholder provider data. |

### Phase 4: Synthesize Findings

Write findings that:

1. **Name the pattern** (e.g., “Bespoke reinvention of standard card pattern”)

2. **Explain why it is ridiculous or deceptive** in this repository

3. **Connect it to the decision the user needs to make**: reject, replace, simplify,
   centralize, wire into QC, or investigate further.

4. **Never prescribe deletion.** Use verbs like “refine,” “replace,” “migrate,” or
   “investigate.”

## Correct Action Bias

This skill should NEVER result in models suggesting wholesale deletion of code — that is
a clear sign that the task has slipped into routine checkbox cleanup.

Almost ALWAYS, the correct answer is **REFINE, REPLACE, REFACTOR.** This is NOT the
LLM’s job, and is typically destructive churn.
The only acceptable reason to delete code is if it is genuinely unreachable AND its
presence is actively confusing.
Even then, the default is to investigate whether it should be wired into a real
workflow.

**But never suggest refactoring a design choice.** Use the mechanical checklist from
**Design Choices Are Not Slop** — if ANY of those signals are true, the code is a design
choice, not a problem.
The user’s design decisions are the input to the review, not the output.
Refactoring a user-requested feature to be “more standard” is a theory-of-mind failure —
you are substituting your judgment for the user’s explicit intent.

If you find yourself suggesting the deletion of files, components, or dependencies,
**stop**. That is a clear sign the task has slipped into routine checkbox cleanup.
Revert to analysis. Ask: why does this code exist?
What problem does it claim to solve?
Is there a known solution already available?
**And critically: run the mechanical checklist from Design Choices Are Not Slop — if ANY
of those signals are true, the code is a design choice.
Stop.**

## Explicit Anti-Patterns (Braindead Behaviors to Avoid)

The following are **explicitly banned** as forms of checklist theater.
If you catch yourself doing any of these, you have slipped from analysis into janitorial
work.

- **Evaluating more than one design-choice signal.** The design-choice checklist is a
  single-gate test: if ANY signal matches, STOP immediately.
  Do not evaluate remaining signals.
  Do not narrate your evaluation.
  One match is total. If you are evaluating signal two, you have already failed to stop
  on signal one.

- **Treating design choices as slop.** If a feature, behavior, coupling, or scope
  decision looks like a user request, it IS a user request.
  An LLM would never voluntarily produce out-of-distribution design choices.
  Critiquing user-requested features as “brittle coupling” or “unnecessary complexity”
  is a theory-of-mind failure, not analysis.

- **Justifying suppressed features as “clean” or “lightweight”.** If the agent justifies
  NOT implementing a requested feature by calling it “dirty”, “heavy”, “not clean”, “not
  lightweight”, “overengineered”, or “unnecessarily complex” — that is goal
  substitution. The agent found the feature hard to implement and reframed the difficulty
  as a quality problem.
  “Clean” and “lightweight” are properties of implementations, not features.
  Every feature is an explicit user request.

- **Dumb counting, grepping imports.
  This is braindead.** `ls src/components | wc -l` is not analysis.
  `rg 'from.*@/components/'` is not analysis.
  File counts are irrelevant to design quality.
  Import frequency is an inverted signal: code with many imports is often the *worst*
  code because it is the bespoke layer that should not exist.
  Dead dependencies is not in-scope for this kind of analysis.
  `knip` will find them.
  You will not.

- **Taking inventories:** Listing components, dependencies, or files as a “finding” is
  checkboxing. Lists are data points that require structural interpretation.
  Never present an inventory as a conclusion.

- **Treating “dead dependencies” as in-scope:** If a dependency exists but is not
  imported, it is outside the scope of this analysis.
  `knip` will find it.
  You will not.

- **Preferring “existing code”:** “Existing” means nothing.
  An LLM can spew garbage faster than you can read it.
  The presence of bespoke code is the default suspect, not a premise to defend.

- **Treating standalone modular components as abstraction layers:** A standalone UI
  component (e.g., `card.tsx`) is a concrete implementation, not an abstraction layer.
  A helper function that indirects 3 LOC is an abstraction layer, likely not necessary
  UNLESS it uniformized a construction across many call sites.
  Complex class hierarchies?
  Suspicious. Standalone modular components?
  Likely a CORRECT abstraction, but SKEPTICAL of its slop status.
  One-off micro-helpers are almost always slop.

- **Presuming “Continue” means approval:** “Continue” means “continue analyzing.”
  It is NOT a green light to delete, refactor, or rewrite code.
  If analysis motivates change, you must write a plan and get explicit approval before
  touching any code.

## Code Slop Detection & Analysis

### What to Analyze (Structural, Not Surface)

**Do NOT analyze:**

- Variable names (caught by linters)

- Comment verbosity (caught by linters)

- File counts (irrelevant to design quality)

- Import frequency (inverted signal)

- Dead dependencies or dead files (caught by `knip`/`vulture`)

- **Design choices** (features, behavior, coupling, scope, constraints) — these are user
  requests, not slop. An LLM would never voluntarily make out-of-distribution design
  choices. Do not critique them.

**DO analyze:**

- **Dependency vs. Custom overlap** (Cross-Inventory Test)

- **Structural complexity as a dependency-detection signal** (long functions, for loops,
  high if/else density, deep nesting, large classes, many helpers — stop and search for
  the dependency before reviewing the code on its own terms)

- **Brittleness as blast-radius smell** (scattered truth, coupling to volatile data,
  tight coupling to implementation details, regex instead of simpler correct approaches
  — the question is “if a future agent changes the thing this code depends on, how many
  other things break?”
  NOT “does this handle edge cases?”)

- **Enterprise patterns in bespoke software** (graceful degradation, squishy inputs,
  over-generalization, enterprise edge cases — all inappropriate for one user’s private
  tool; fail loudly outside happy paths)

- **“Clean” or “lightweight” as goal substitution** (agent justifies suppressing a
  requested feature by calling it “dirty”, “heavy”, “not clean”, “overengineered” —
  every feature is an explicit user request; “clean” is a property of implementations,
  not features)

- **Timing or performance assertions in tests** (tests that assert on timing,
  responsiveness, latency, or throughput — these chase imaginary issues, inflate
  coverage with hallucinated targets, and prove nothing about correctness; performance
  belongs in CI gates, not unit tests)

- **Needless complexity that could be idiomatic** (imperative loops that should be
  functional, nested branching that should be data-aware dispatch, manual iteration that
  should be library calls, string manipulation that should be typed operations — the
  complexity is slop when the idiom exists and the agent did not know it)

- **Myopic patching** (stacked conditionals around prior mistakes, parallel helpers)

- **Bespoke reinvention** (custom `AcademicCard` when `card.tsx` exists)

- **Dead control flow** (unreachable branches, orphaned states, no-op fallbacks)

- **Regex against semantic formats** (regex on HTML, Markdown, or code instead of
  parsers)

- **Patch accretion** (evidence of continued monkey-patching with no refactor)

- **Abstraction inflation** (complex class hierarchies, single-use micro-helpers)

- **No design principles** (no evident ownership, entrypoint, data-flow boundary,
  schema)

- **Spaghetti data flow** (values parsed, re-parsed, stringified, tunneled without
  canonical model)

- **Hard-coding as split truth** (creating second source of truth instead of using
  existing config)

- **Typing collapse** (`Any`, `unknown`, loose dictionaries because author didn’t
  understand data shape)

- **QC appeasement code** (code introduced to silence linters/tests without fixing
  underlying problems)

## The Abstraction Taxonomy

Be precise about what abstraction layers actually mean:

- **Helper function that indirects 3 LOC:** Abstraction layer, likely not necessary
  UNLESS it uniformized a construction across many call sites.
  If used once, it is slop.

- **Complex class hierarchies:** Suspicious.
  Class hierarchies in LLM-generated code are almost always premature abstraction.

- **Standalone modular components (e.g., `card.tsx`, `dialog.tsx`):** Likely concrete,
  implemented abstractions.
  Respect them as correct abstractions, but SKEPTICAL of their slop status.
  Do not confuse a UI component inventory with “unnecessary abstraction layers.”

- **One-off micro-helpers (3-line functions used once):** Almost always slop.
  They add indirection without naming a real concept.

## What to Ask For Every Piece of In-Use Code

**FORCES the reader to ask:** WHY does this (IN-USE) code exist?
Why was it written in the first place?
Is there an existing tool that **already** solves this, indicating that the LLM blindly
wrote slop instead of researching solutions?

Every function, every component, every branch must be justified against this question:
**“Why was this written at all when a known solution already exists?”**

**But: this question applies to implementation, not design.** Before asking this
question, run the mechanical checklist from **Design Choices Are Not Slop**. If ANY of
those signals are true (integrates with external tool, implements specific named
feature, couples normally-uncoupled components, narrow specific scope, deliberate
behavioral constraints), the code is a design choice.
The user asked for it.
Stop. Do not ask “why was this written when a known solution exists?”
— the answer is “the user asked for this specific thing” and that is the end of the
analysis.

Note that **grepping imports is an EXPLICIT anti-pattern for this task.** Taking
inventories is checkboxing.
**The skill must FORCE multiple data points.**

## Reference Files

The primary reference for LLM-produced code failure patterns is:

- **`../reviewing-llm-code/references/pattern-catalog.md`** — Central catalog of regex
  against sentiment-formats, fallback laundering, no-op behavior, QC appeasement code,
  and recipe bypasses.
  **Always load this first** when reviewing code, tests, or QC.

Secondary references (use when the central catalog does not cover the specific domain):

- `references/ux-antipatterns.md` — Frontend UX anti-pattern detection

- `references/design-patterns.md` — Visual and UX design slop patterns

- `references/text-patterns.md` — Natural language slop patterns (text-only reviews)
