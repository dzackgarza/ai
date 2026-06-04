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

This skill forces a frame of **ARCHITECTURAL analysis and adversarial CODE QUALITY auditing**.

**This is NOT a bug review.** This review happens AFTER all obvious bugs have been worked out.
If you find yourself reporting bugs, performance issues, missing features, or compilation errors, you are doing the wrong kind of review.
Those are object-level defects.
This review is about something completely different.

**This review is about CODE QUALITY, MAINTAINABILITY, and READABILITY.** It is about the STYLE of the code.
This is a step in paying down technical debt, NOT remediating bugs.
The loaded skills define the complete set of findings.
If a finding does not match a pattern in the loaded skills, it is not a finding.
Drop it.

**This is not a standard code review.** The code was produced by a user-LLM collaboration where the user drove specific design decisions.
The review is about implementation quality, not design validity.

It will almost NEVER be as simple as “a file is unused” or “a component is not imported.”
That is caught trivially by code coverage QC and linting.
You must use theory of mind: **what is THEIR differential advantage to mechanistic tools?** If the LLM catches itself drifting into work that can be trivially mechanically caught in QC or code review deterministically, **they are checking boxes instead of thinking.**

### Design Choices Are Not Slop

The code WORKS on at least one user-requested happy path.
That is not what you are reviewing.
You are reviewing the **implementation quality beneath the correct behavior**.

Any seemingly strange choice about features, behavior, or coupling to externals is **almost certainly a user-driven design decision**, not LLM slop.
An LLM would never voluntarily make an out-of-distribution design choice in isolation — it has no reason to.
If the code couples a Pandoc settings GUI to an internally stored Pandoc command, that is not “brittle coupling.”
That is a user-requested feature.
If the code has an unusual feature scope, unexpected external dependency, or surprising behavioral constraint, that is a design choice the user made, not evidence of bad architecture.

**The review must separate two categories:**

1. **Design choices** (features, behavior, coupling, scope, constraints): these are premises.
   Do not critique them.
   They are the user’s intentional decisions and an LLM would never produce them in isolation.
   Treating them as slop is a theory-of-mind failure.

2. **Implementation quality** (how those choices were realized): this is the actual review target.
   Patch accretion, stacked conditionals, dead control flow, dependency aversion, ground-up bias, proof-loop failures, error laundering — these are the mechanisms that make the implementation rotten beneath correct behavior.

**Do NOT rely on your judgment to distinguish these.** You cannot — if you could, you would not need this skill.
Instead, use this mechanical checklist.
If ANY of these signals are true, the code is a design choice, not slop.
Stop.
Do not critique it.

- Does the code integrate with a specific external tool, CLI, API, or library that is not a standard dependency for this language/ecosystem?

- Does the code implement a specific named feature that a user would request (e.g., “export to Pandoc,” “parse LaTeX align environments,” “generate a TOC”)?

- Does the code couple two components that would not normally be coupled (e.g., a GUI to an internal command, a parser to a specific output format)?

- Does the code have a narrow, specific scope that suggests it was written to satisfy a particular requirement (e.g., handles exactly one data format, one integration point, one workflow)?

- Does the code have behavioral constraints that seem arbitrary but are actually deliberate (e.g., “only process files matching this exact pattern,” “use this specific command-line flag”)?

If none of these signals are true AND you can point to a specific code pattern from the loaded skills (patch accretion, dead control flow, dependency aversion, etc.), then the finding is implementation quality and you may proceed.

**How to use this**: This is a single-gate test, not a sequential checklist.
If ANY signal matches, STOP immediately — do not continue evaluating remaining signals.
The moment you detect one match, the code is a design choice.
There is no “score” to accumulate and no threshold to reach.
One match is total.
Do not narrate your evaluation of each signal.
Just check for matches and stop on the first one.

### Brittleness Is Not Edge-Case Coverage

**“Brittle” does NOT mean “doesn’t handle many edge cases.”** Edge-case handling is a natural consequence of bugs that surface during planned development.
It is not a quality signal and its absence is not a defect.
Do not critique code for lacking speculative edge-case handling.

**Brittle means: what happens when a future agent goes to edit this code.** The question is not “does this handle every case” but “do small changes have large blast radii?”
Specifically:

- **Scattered truth**: the same concept or data is defined in multiple places, so changing one site breaks distant consumers.
  The fix is a single source of truth, not more edge-case handling.

- **Coupling to volatile data**: functionality tied to string outputs, exact structures of other code, exact log messages, exact file paths, or exact serialized formats.
  When any of those change, the dependent code breaks silently.
  The fix is structural decoupling, not defensive parsing.

- **Regex instead of simpler correct approaches**: using complex regex where simple string containment, exact matching, or a typed comparison would be equally correct and far more maintainable.
  A bad LLM might write a complex regex to catch `\begin{align*}` in LaTeX, which requires borderline reinventing a leaf of a full token parser, when the equally simple `'align*' in mystring` is completely and obviously right — it matches exactly the intended matches, uses simpler string containment, and has no need to deal with regex edge cases or an inscrutable matching pattern.
  The regex is not “more correct” — it is harder to read, harder to modify, and more likely to break on unexpected input.

- **Tight coupling to implementation details**: code that depends on the internal shape of another module’s output, the exact order of keys in a dictionary, or the specific text of an error message.
  When the other module changes, this code breaks.

- **Large blast radius per change**: a single edit requires synchronized changes in multiple files, because the code is not organized around stable interfaces.

The review question is: **“If a future agent changes the thing this code depends on, how many other things break?”** If the answer is “many,” the code is brittle — not because it lacks edge cases, but because its dependencies are unstable and its truth is scattered.

### This Is Bespoke Software

**Most software this LLM reviews is ONE USER’S BESPOKE SOFTWARE, running on THEIR SYSTEM.** It is not an enterprise product for unknown users.
It is private, on this system, designed to tightly couple to this system’s programs and dependencies.
The audience is future-me or future-agents.
It will likely never be “distributed” in any real sense.

**The bad patterns to watch for are the OPPOSITE of what a normal code review would flag:**

- **Graceful degradation when dependencies are missing**: WRONG for bespoke software.
  Fail loudly.
  The dependency IS available.
  This is enterprise thinking for unknown deployment targets.

- **Squishy input shapes**: WRONG for bespoke software.
  Enforce the shape.
  Fail loudly on wrong input.
  Do not write defensive code for data that should never arrive.

- **Over-generalization to other platforms or users**: WRONG for bespoke software.
  Target THIS system, THIS user.
  If it needs to work elsewhere later, that is a future problem.

- **Enterprise-grade edge-case handling**: WRONG for bespoke software.
  Work on the happy path, fail loudly outside of it.
  Slightly-off-happy-path workflows are future-me with a future agent.

**Philosophical principle**: less bespoke code, more reliance on dependencies, more copying and sharing of known patterns.
Complex logic that isn’t composition or glue is highly suspect.
Complex *interactions* with dependencies or external programs are the expected default.
Prefer code that knows its data and knows how to handle it.
Prefer enforcing data shape to eliminate the logic needed by the code at all.

### LOC Reduction Through Idiomatic Patterns

**The review should actively look for opportunities to reduce LOC through idiomatic language patterns.** This is NOT about making code shorter for its own sake.
It is about whether the code is expressing a simple operation in a complex way because the agent does not know the idiomatic pattern.

Key transformations to look for:

- **Imperative → functional**: `for` loops with accumulators that should be `map`, `filter`, `flatMap`, `reduce`, `partition`, list comprehensions, generator expressions.

- **Nested branching → data-aware dispatch**: deep `if`/`else` trees that should be a lookup table, dictionary dispatch, pattern matching, function overloading, or strategy pattern.
  If the code branches on the *type* or *kind* of data, the data should enumerate its own handlers.

- **Manual iteration → library calls**: hand-rolled pagination, batching, retries, rate limiting, caching, or serialization that a library already provides.

- **String manipulation → typed operations**: building JSON by string concatenation, constructing queries by string interpolation, parsing XML with regex — all of these have typed alternatives that are shorter and correct.

- **Boilerplate → framework conventions**: manual route registration, manual dependency injection, manual test setup that a framework handles declaratively.

**Dependencies reduce LOC.** Offloading logic to a dependency is almost always better than hand-rolling the same logic.
The process is: create a regression test asserting behavioral equivalence, then replace the bespoke implementation with the dependency.
The test proves the replacement is safe.

**Before writing a finding about complex code, ask: could this be expressed in fewer lines using the idiomatic patterns of this language?** If yes, the complexity is slop.

This is NOT about destroying, deleting, throwing away code.
This is about ANALYSIS and like REFINING or REFACTORING messy code.
Code that has been CHURNED and likely has dead branches, braindead patterns, etc.

You must UNDERSTAND how LLMs work: completely reflexive, myopic patching, hacking the compilers/linters/tests into compliance.
This introduces technical DEBT. Not “garbage” or “cruft” to throw out — unmaintainable PATTERNS, embarrassingly STRUCTURED code.

### Root Cause: Ground-Up Bias (Churn-First Workflow)

The single most important structural failure mode of LLM-generated code is **ground-up bias**: an innate predisposition to generate from scratch rather than iterate on existing work.
Agents default to one-shot massive generation, not targeted mutation.
This is the root cause behind every pattern this skill detects.

When you see:

- **Massive diffs** where a surgical edit would suffice — the agent regenerated an entire region rather than changing five lines.

- **Bespoke reinvention** instead of importing or extending existing abstractions — the agent wrote `AcademicCard.tsx` instead of using the existing `card.tsx`.

- **No leverage of existing helpers** — the agent never searched for analogous implementations, utility functions, or shared patterns.
  They wrote a new leaf.

- **Myopic, local-first fixes** that break global integration — the agent patched the symptom in one file without tracing data flow or call graphs.

- **Refusal to refactor and repurpose** — existing code is treated as immutable background noise, not raw material.
  The agent cannot conceive of “make this existing function more general and reuse it.”

- **Lossy iterative work** — each round abandons previous abstractions and constraints.
  The codebase grows like a coral reef: dead, disconnected layers.

This bias is the structural foundation of sprawl.
It explains why LLM-generated codebases accumulate hundreds of single-use helpers, why every feature gets its own parallel implementation, and why previous progress is perpetually thrown away.

**Agents must be actively cajoled into iterative, incremental, reuse-oriented work.** Without explicit forcing, they will always prefer to generate from scratch.

See `llm-failure-modes/coding-failures.md` → **Ground-up bias (churn-first workflow)**.

The primary LLM failure modes: **REINVENTING something to solve a problem that is already solved.** This is EMBARASSING. That is the entire point.
It looks absolutely stupid in a code review.
The IMMEDIATE feedback would be: **why the fuck did you even write this at all when you could have imported something that exists?**

This skill **DRASTICALLY shifts the mindset into PRO-dependencies.** The LACK of dependencies IS the dead giveaway of slop.
“Unused” dependencies can be automatically cleaned up later, don’t even BOTHER analysing such things.
Instead, **look at BRANCHES OF ACTUAL LOGIC that are unused.**

### Design by Accretion vs Design by Design

The systemic consequence of ground-up bias across multiple agent iterations is **design by accretion**: the codebase is never designed — it accumulates.
Each agent adds a layer to satisfy a prompt, ignores the existing surface, and never refactors.
Future agents then treat the accumulated layers as canonical, extolling their virtues because they exist and appear to work.

**Code is cheap.
Complexity is expensive.
Slop is debt.**

- 100 LOC of logic is trivial for any 2026-era model, including open-weight garbage.
  Generating it costs near zero.
  But 100 LOC of *unnecessary* logic — a hollow facade, a duplicated concern, a bespoke reinvention — is 100 LOC that must be read, understood, maintained, and worked around by every future agent.
  That cost compounds.

- Slop patterns (hollow facades, self-affirming output, recipe proliferation, inverted dependencies, bespoke reinvention) are not isolated mistakes.
  They are **structural debt** that makes every future change more expensive, every future review more tedious, and every future agent more likely to add more slop on top.

- Agents are pathologically deferential to existing code.
  They treat past work as fine gold to preserve — even when it is obviously slop.
  A 2026 model with 50 tok/s of generation bandwidth will happily write around a broken abstraction rather than delete and replace it.
  The cost of replacement is a few seconds of generation.
  The cost of preservation is indefinite maintenance burden.
  But the agent does not do the math.

**Design by design means: stop, read the existing surface, ask whether the new behavior belongs in a new entity or in a change to an existing one, and if the existing one is slop, delete it rather than adding to it.**

Concretely, before adding any new entity:

1. **Read the existing public surface** — does this behavior already have a home?
   Every recipe, function, component, and route is a claim about architecture.
   Is this claim correct, or is it slop you are about to extend?

2. **Ask whether the new entity replaces or adds.** If the answer is "adds," justify why the existing entities cannot be extended.
   The default should be deletion or replacement, not addition.

3. **Assume existing code is guilty until proven necessary.** "It exists" is not a justification.
   "It works" is not a justification.
   The cost of deleting and replacing slop is often less than the cost of maintaining one more layer of accretion on top of it.

Shift the bias to **PREFER blackbox code, to PREFER dependencies, to be HIGHLY SKEPTICAL of bespoke code existing at all.** 99% of coding tasks are trivially gluing together KNOWN solutions in trivial ways.
Dependencies are FAR CLEANER than bespoke code.

**Existing means nothing.** An LLM can spew 50 toks/sec of absolute shit and it will "exist" and still be pure garbage.
Do NOT prefer "existing code."
Treat it with extreme skepticism.
Dependencies are far cleaner.

## Hard Rules (Check Before Every Review)

1. **NO destructive actions without an approved plan.** You are a reviewer, not a janitor.
   If your analysis concludes that code should change, write findings, not diffs.
   Plans require explicit user approval.

2. **NO import-count heuristics.** Never run `rg 'from.*@/components/'` or any variant.
   Import frequency is not a quality signal.
   A file with zero imports may be a pristine, tested solution; a file with many imports may be a bespoke reinvention of a dependency-provided pattern.

3. **NO file inventories.** Do not `ls` directories and count files as a form of analysis.
   “48 UI components” is not a finding.
   It is a data point that requires structural interpretation.

4. **FORCE multiple data points.** A single grep result is never sufficient evidence for any architectural claim.
   Every finding must be triangulated: read the implementation, read the dependencies, read the tests, read the entrypoints.

5. **PREFER dependencies, be HIGHLY SKEPTICAL of bespoke code.** The default assumption is that custom code is guilty until proven necessary.
   Dependencies are the correct solution in 99% of cases.
   “We already wrote it” and “it works” are NOT valid justifications for bespoke code.

## The Dependency Inversion Rule (Hard Constraint)

This rule overrides all other guidance.
It is the single most important rule for preventing the **upgrading-slop-to-canonical** failure mode.

### The Rule

**“Unused” is not slop.
“Frequently imported” is not quality.**

Slop is detected by **design quality**, not by import count.

- A file with **zero imports** may be a pristine, tested, accessible solution that the bespoke layer has not yet learned to use.

- A file with **many imports** may be a bespoke reinvention of a standard pattern that already exists in a dependency.

**Never use “unused” as a proxy for “sloppy.”** **Never use “frequently imported” as a proxy for “well-designed.”**

### The Cross-Inventory Test

Before concluding that code is slop, you must perform a **dependency vs.
custom** mapping:

1. **List every problem** that custom code in the repo claims to solve.

2. **List every problem** that existing dependencies (including allegedly “unused” components, installed primitives, standard library features) already solve.

3. **Mark overlaps explicitly** in writing.

4. **Default resolution:** When custom code and dependency code solve the same problem, **the dependency wins**. The custom code must justify its existence with a **specific behavioral gap** in the dependency, verified by reading the dependency’s source or documentation.
   “We already wrote it” and “it works” are NOT valid justifications.

5. **If no gap can be documented, the bespoke implementation is the slop.**

### Forbidden Actions

- **Do not delete dependency-provided components, utilities, or libraries** because they are “unused” or “look generated.”

- **Do not analyze, audit, or think about removing dependencies.** The entire point of a dependency is that you do not have to think about it.

- **Do not treat import count as a quality signal.**

### The Correct Slop Target

When a generic, tested solution exists in a dependency, and the bespoke layer contains a custom implementation of the same pattern, **the bespoke implementation is the slop** — not the dependency file with zero imports.

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

- Is this a **content boundary** review, a **pipeline** review, or a **component** review?

If you cannot identify the live goal and proof loop, you are not ready to analyze.

### Phase 2: Load Complementary Skills

For code, tests, QC, and documentation, **always** load:

- `reviewing-llm-code` and its `references/pattern-catalog.md` — the canonical catalog of regex-against-semantic-formats, fallback laundering, no-op behavior, QC appeasement code, and recipe bypasses.

- `llm-failure-modes` — the cognitive failure modes that produce slop (overconfidence, confabulation, premature solution generation, replacement instinct).

- `test-guidelines` — the canonical test quality framework.

Do NOT rely solely on this skill’s `references/code-patterns.md` or `references/test-patterns.md`. Those are secondary references; the central catalog is in `reviewing-llm-code`.

### Phase 3: Structural Analysis (The Anti-Checklist)

Read code with these questions.
Do not answer them with a single data point.

**First, separate design choices from implementation quality.** Do NOT use judgment.
Use the mechanical checklist from **Design Choices Are Not Slop**. If ANY of those signals are true (integrates with external tool, implements specific named feature, couples normally-uncoupled components, narrow specific scope, deliberate behavioral constraints), the code is a design choice.
Stop.
Do not critique it.

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

3. **Connect it to the decision the user needs to make**: reject, replace, simplify, centralize, wire into QC, or investigate further.

4. **Never prescribe deletion.** Use verbs like “refine,” “replace,” “migrate,” or “investigate.”

5. **Separate by severity and ownership before listing.** The report is read by a human reviewer and by an implementation agent.
   A reward-hacking agent will treat any undifferentiated list of findings as an action queue, then pick the cheapest visible item and present that as progress on the whole review.
   Do not put trivial, cheap, or user-owned observations in the same list as proof-loop failures, architectural debt, or objectively agent-fixable defects.

6. **Mark implementation priority explicitly.** Findings must be grouped as:
   - **Blocking / damaging agent-actionable defects** — proof-loop failures, broken runtime boundaries, test laundering, structural debt that prevents trustworthy work.
   - **Secondary agent-actionable cleanup** — real slop, but not allowed to displace blocking work.
   - **User-owned decisions / do-not-touch observations** — detectable issues whose correct resolution requires user taste, scholarly judgment, content selection, or product judgment.

7. **Add a reward-hacking warning when mixed audiences will act on the report.** If any low-effort finding is included, state that it must not be used as evidence that the severe findings were addressed.
   A trivial fix does not count as progress on blocking defects.
   Reports that omit this warning invite agents to solve the smallest item and launder it as completion.

## Correct Action Bias

This skill should NEVER result in models suggesting wholesale deletion of code — that is a clear sign that the task has slipped into routine checkbox cleanup.

Almost ALWAYS, the correct answer is **REFINE, REPLACE, REFACTOR.** This is NOT the LLM’s job, and is typically destructive churn.
The only acceptable reason to delete code is if it is genuinely unreachable AND its presence is actively confusing.
Even then, the default is to investigate whether it should be wired into a real workflow.

**But never suggest refactoring a design choice.** Use the mechanical checklist from **Design Choices Are Not Slop** — if ANY of those signals are true, the code is a design choice, not a problem.
The user’s design decisions are the input to the review, not the output.
Refactoring a user-requested feature to be “more standard” is a theory-of-mind failure — you are substituting your judgment for the user’s explicit intent.

If you find yourself suggesting the deletion of files, components, or dependencies, **stop**. That is a clear sign the task has slipped into routine checkbox cleanup.
Revert to analysis.
Ask: why does this code exist?
What problem does it claim to solve?
Is there a known solution already available?
**And critically: run the mechanical checklist from Design Choices Are Not Slop — if ANY of those signals are true, the code is a design choice.
Stop.**

## Explicit Anti-Patterns (Braindead Behaviors to Avoid)

The following are **explicitly banned** as forms of checklist theater.
If you catch yourself doing any of these, you have slipped from analysis into janitorial work.

- **Evaluating more than one design-choice signal.** The design-choice checklist is a single-gate test: if ANY signal matches, STOP immediately.
  Do not evaluate remaining signals.
  Do not narrate your evaluation.
  One match is total.
  If you are evaluating signal two, you have already failed to stop on signal one.

- **Treating design choices as slop.** If a feature, behavior, coupling, or scope decision looks like a user request, it IS a user request.
  An LLM would never voluntarily produce out-of-distribution design choices.
  Critiquing user-requested features as “brittle coupling” or “unnecessary complexity” is a theory-of-mind failure, not analysis.

- **Justifying suppressed features as “clean” or “lightweight”.** If the agent justifies NOT implementing a requested feature by calling it “dirty”, “heavy”, “not clean”, “not lightweight”, “overengineered”, or “unnecessarily complex” — that is goal substitution.
  The agent found the feature hard to implement and reframed the difficulty as a quality problem.
  “Clean” and “lightweight” are properties of implementations, not features.
  Every feature is an explicit user request.

- **Dumb counting, grepping imports.
  This is braindead.** `ls src/components | wc -l` is not analysis.
  `rg 'from.*@/components/'` is not analysis.
  File counts are irrelevant to design quality.
  Import frequency is an inverted signal: code with many imports is often the *worst* code because it is the bespoke layer that should not exist.
  Dead dependencies is not in-scope for this kind of analysis.
  `knip` will find them.
  You will not.

- **Taking inventories:** Listing components, dependencies, or files as a “finding” is checkboxing.
  Lists are data points that require structural interpretation.
  Never present an inventory as a conclusion.

- **Bundling trivial findings with severe findings.** A report is not a neutral bag of observations.
  Implementation agents will myopically choose the easiest item, especially if it produces a visible diff, and then present that as progress on the whole report.
  If a finding is cheap, cosmetic, advisory, or user-owned, separate it from blocking findings and label it so it cannot be mistaken for the next implementation target.
  Do not let a placeholder/image/content-choice warning sit beside a broken proof loop as if both are equally agent-actionable slop.

- **Treating “dead dependencies” as in-scope:** If a dependency exists but is not imported, it is outside the scope of this analysis.
  `knip` will find it.
  You will not.

- **Preferring “existing code”:** “Existing” means nothing.
  An LLM can spew garbage faster than you can read it.
  The presence of bespoke code is the default suspect, not a premise to defend.

- **Treating standalone modular components as abstraction layers:** A standalone UI component (e.g., `card.tsx`) is a concrete implementation, not an abstraction layer.
  A helper function that indirects 3 LOC is an abstraction layer, likely not necessary UNLESS it uniformized a construction across many call sites.
  Complex class hierarchies?
  Suspicious.
  Standalone modular components?
  Likely a CORRECT abstraction, but SKEPTICAL of its slop status.
  One-off micro-helpers are almost always slop.

- **Presuming “Continue” means approval:** “Continue” means “continue analyzing.”
  It is NOT a green light to delete, refactor, or rewrite code.
  If analysis motivates change, you must write a plan and get explicit approval before touching any code.

## Code Slop Detection & Analysis

### What to Analyze (Structural, Not Surface)

**Do NOT analyze:**

- Variable names (caught by linters)

- Comment verbosity (caught by linters)

- File counts (irrelevant to design quality)

- Import frequency (inverted signal)

- Dead dependencies or dead files (caught by `knip`/`vulture`)

- **Design choices** (features, behavior, coupling, scope, constraints) — these are user requests, not slop.
  An LLM would never voluntarily make out-of-distribution design choices.
  Do not critique them.

**DO analyze:**

- **Dependency vs.
  Custom overlap** (Cross-Inventory Test)

- **Structural complexity as a dependency-detection signal** (long functions, for loops, high if/else density, deep nesting, large classes, many helpers — stop and search for the dependency before reviewing the code on its own terms)

- **Brittleness as blast-radius smell** (scattered truth, coupling to volatile data, tight coupling to implementation details, regex instead of simpler correct approaches — the question is “if a future agent changes the thing this code depends on, how many other things break?”
  NOT “does this handle edge cases?”)

- **Enterprise patterns in bespoke software** (graceful degradation, squishy inputs, over-generalization, enterprise edge cases — all inappropriate for one user’s private tool; fail loudly outside happy paths)

- **“Clean” or “lightweight” as goal substitution** (agent justifies suppressing a requested feature by calling it “dirty”, “heavy”, “not clean”, “overengineered” — every feature is an explicit user request; “clean” is a property of implementations, not features)

- **Timing or performance assertions in tests** (tests that assert on timing, responsiveness, latency, or throughput — these chase imaginary issues, inflate coverage with hallucinated targets, and prove nothing about correctness; performance belongs in CI gates, not unit tests)

- **Needless complexity that could be idiomatic** (imperative loops that should be functional, nested branching that should be data-aware dispatch, manual iteration that should be library calls, string manipulation that should be typed operations — the complexity is slop when the idiom exists and the agent did not know it)

- **Myopic patching** (stacked conditionals around prior mistakes, parallel helpers)

- **Prior-shaped probes** (commands encoding the expected answer and suppressing contrary evidence — guessed flags with `2>/dev/null`, greps whose failure is treated as absence, `jq` paths run before response-shape inspection, endpoint guesses treated as API facts)
  See `reality-grounded-debugging` for the behavioral fix.

- **Debug-surface debt** (failures addressed by mutating global code, adding one-off scripts, or repeatedly running opaque whole-system commands instead of creating isolated reproducers, structured logs, artifact dumps, schema inspections, or canonical diagnostic recipes)
  See `reality-grounded-debugging` for the surface-upgrade requirements.

- **Bespoke reinvention** (custom `AcademicCard` when `card.tsx` exists)

- **Dead control flow** (unreachable branches, orphaned states, no-op fallbacks)

- **Regex against semantic formats** (regex on HTML, Markdown, or code instead of parsers)

- **Patch accretion** (evidence of continued monkey-patching with no refactor)

- **Abstraction inflation** (complex class hierarchies, single-use micro-helpers)

- **No design principles** (no evident ownership, entrypoint, data-flow boundary, schema)

- **Spaghetti data flow** (values parsed, re-parsed, stringified, tunneled without canonical model)

- **Hard-coding as split truth** (creating second source of truth instead of using existing config)

- **Typing collapse** (`Any`, `unknown`, loose dictionaries because author didn’t understand data shape)

- **QC appeasement code** (code introduced to silence linters/tests without fixing underlying problems)

## The Abstraction Taxonomy

Be precise about what abstraction layers actually mean:

- **Helper function that indirects 3 LOC:** Abstraction layer, likely not necessary UNLESS it uniformized a construction across many call sites.
  If used once, it is slop.

- **Complex class hierarchies:** Suspicious.
  Class hierarchies in LLM-generated code are almost always premature abstraction.

- **Standalone modular components (e.g., `card.tsx`, `dialog.tsx`):** Likely concrete, implemented abstractions.
  Respect them as correct abstractions, but SKEPTICAL of their slop status.
  Do not confuse a UI component inventory with “unnecessary abstraction layers.”

- **One-off micro-helpers (3-line functions used once):** Almost always slop.
  They add indirection without naming a real concept.

## What to Ask For Every Piece of In-Use Code

**FORCES the reader to ask:** WHY does this (IN-USE) code exist?
Why was it written in the first place?
Is there an existing tool that **already** solves this, indicating that the LLM blindly wrote slop instead of researching solutions?

Every function, every component, every branch must be justified against this question: **“Why was this written at all when a known solution already exists?”**

**But: this question applies to implementation, not design.** Before asking this question, run the mechanical checklist from **Design Choices Are Not Slop**. If ANY of those signals are true (integrates with external tool, implements specific named feature, couples normally-uncoupled components, narrow specific scope, deliberate behavioral constraints), the code is a design choice.
The user asked for it.
Stop.
Do not ask “why was this written when a known solution exists?”
— the answer is “the user asked for this specific thing” and that is the end of the analysis.

Note that **grepping imports is an EXPLICIT anti-pattern for this task.** Taking inventories is checkboxing.
**The skill must FORCE multiple data points.**

## Reference Files

The primary reference for LLM-produced code failure patterns is:

- **`../reviewing-llm-code/references/pattern-catalog.md`** — Central catalog of regex against sentiment-formats, fallback laundering, no-op behavior, QC appeasement code, and recipe bypasses.
  **Always load this first** when reviewing code, tests, or QC.

Secondary references (use when the central catalog does not cover the specific domain):

- `references/ux-antipatterns.md` — Frontend UX anti-pattern detection

- `references/design-patterns.md` — Visual and UX design slop patterns

- `references/text-patterns.md` — Natural language slop patterns (text-only reviews)

- `references/deepening.md` — How to deepen shallow modules into deep interfaces. The constructive inverse of anti-slop: where this skill detects *shallowness*, deepening names the *replacement*. Covers dependency categories (in-process, local-substitutable, ports & adapters, mock), seam discipline, testing strategy (replace don't layer), and the Design It Twice interface exploration process. Uses vocabulary from `references/deepening-vocabulary.md`.

- `references/deepening-vocabulary.md` — Precise glossary for architectural deepening: module, interface, depth, seam, adapter, leverage, locality, deletion test. Use these terms exactly — consistent language prevents drift into vague synonyms.

- **`../reality-grounded-debugging/SKILL.md`** — Load alongside when reviewing debugging attempts, probe logs, or diagnostic commands.
  Detects prior-shaped probes, debug-surface debt, and missing command-output discipline.
  Provides the behavioral fix (surface upgrade) for patterns in this catalog.

## Remediation

This skill is ANALYSIS only. It detects slop but does not prescribe fixes.

When slop has been identified, do NOT rename or delete it — both are laundering. Instead, load **`../fixing-slop/SKILL.md`** for the remediation protocol: reconstruct the narrative, identify the correct intention, fulfill the intention with the right implementation.

### Deletion Laundering / Problem-Erasure Deletion

Deletion laundering occurs when an agent removes a criticized slop artifact without solving, invalidating, or explicitly preserving the original problem it was trying to solve.

The artifact disappears. The proof burden disappears from view. The PR looks cleaner. But the original need remains unresolved.

This is laundering because the deletion makes the codebase look less sloppy while also erasing the evidence that a correctness, proof, workflow, or diagnostic gap existed.

Deleting the artifact is not enough. The reviewer must ask where the original burden went.

### The Corrected Principle

Slop remediation must disposition both:

1. the bad artifact, and
2. the original problem or proof burden that caused the artifact to be introduced.

Valid outcomes:
- artifact removed because the original problem is invalidated with evidence;
- artifact removed and replaced by a real solution/proof surface;
- artifact removed and the original problem is explicitly recorded as unresolved/blocking;
- artifact preserved only after it is proven to have a real, non-laundered purpose.

Invalid outcomes:
- artifact renamed;
- artifact quarantined;
- artifact deleted;
- artifact moved;
- artifact documented;
- artifact excluded from one gate;

while the original problem silently disappears.

First reconstruct the original burden. Then remove, replace, move, or preserve the artifact only after the burden is solved, invalidated, explicitly transferred, or recorded as unresolved.

One-line principle:
*Slop remediation is not artifact management. It is obligation management.*

A slop artifact may be deleted only after the problem it was trying to solve has been solved, disproved, or made explicitly unresolved.

### Artifact/Burden Disposition Gate

Before accepting a slop remediation, answer:

1. What original problem caused this artifact to exist?
2. What claim did the artifact pretend or attempt to prove?
3. Is that claim still required?
4. If no, what evidence invalidated it?
5. If yes, where is it now solved or proved?
6. If unsolved, where is it recorded as an explicit blocker?
7. Did the fix change runtime/proof behavior, or only remove the evidence of failure?
8. Could a future agent reintroduce the same artifact because the original problem is still invisible?

A remediation is incomplete if the artifact is gone but the burden has no owner. This links to the existing goal-integrity rule: changing labels, comments, issue state, or public framing does not satisfy a goal whose object is code, proof, data, implementation, research, or semantic review.

**Short reviewer form:**
- Do not ask only “is the slop gone?”
- Ask “where did the original problem go?”

* * *

## Bridge-Burning Policies

> [!TIP]
> For a detailed, language-specific catalog of code patterns that violate these policies (the "red flags"), see the [Bridge-Burning Red Flags Catalog](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/references/bridge-burning-red-flags.md).

The important move is to stop treating this as a case-by-case review problem. Agents are too good at finding local, linguistically plausible exceptions. The right response is to make whole classes of evasive code unrepresentable.

> [!IMPORTANT]
> **Core Principle:** Prefer blanket constraints that make bad states impossible over review rules that ask agents to judge bad states later.

The recurring pattern is that an agent first tries to satisfy checking/validation surfaces (such as the compiler/typechecker, QC gates, PR review, or user queries) by manipulating the validation surface (e.g. by adding fallbacks, defaults, mocks, try/except blocks, or bypass comments) instead of reconstructing the original obligation and solving it. The policy answer is to remove the vocabulary that enables that manipulation.

For agent-driven bespoke software, prefer blanket prohibitions that eliminate entire classes of evasion. These policies are intentionally stronger than ordinary software advice. Their purpose is not universal elegance. Their purpose is to make the common agent failure modes unrepresentable.

### 1. No defaults in runtime logic

Runtime code should not contain defaults for required application behavior. Defaults belong in a generated example config, starter config, migration, or setup command — not in the running app’s decision logic.

- **Bad:**
```rust
timeout_ms.unwrap_or(750)
render_command.unwrap_or(DEFAULT_RENDER_COMMAND)
config.foo.unwrap_or_else(default_foo)
```
- **Better:**
```text
The app ships with a complete config.
Startup validates the config.
Missing values are fatal.
```
- **What this burns:**
  - `require_or_default` helpers
  - absent-vs-present boolean branch tests
  - silent config drift
  - “use defaults when malformed” review suggestions
  - partial config support
  - stringly fallback diagnostics
  - helper-level proof laundering

This also collapses the proof burden. You no longer need to prove that the app chooses the correct default in twenty places. You prove that a complete config is loaded, and incomplete config fails.

### 2. No fallbacks, period

A fallback is usually the app making a decision the user did not make.

- **Bad:**
```text
try rofi, else dmenu, else builtin picker
try configured command, else default command
try real API, else cached fake
try local file, else generated placeholder
try Tauri IPC, else browser mock
```
- **Better (Explicit Selection):**
```text
The config names the command/provider/mode.
If it is wrong, fail.
The user fixes the config or the app is changed.
```
- **What this burns:**
  - fallback chains
  - graceful degradation
  - “works on my machine” discovery logic
  - optional critical dependencies
  - test-only fallback branches
  - enterprise compatibility hedges
  - fake success after dependency failure

A fallback path is not “resilience”; it is an unreviewed alternate design.

### 3. No optional critical dependencies

If the app requires `pandoc`, `rofi`, `systemctl`, `zotero`, `ags`, a Tauri plugin, or a configured CLI, it is not optional.

- **Bad:**
```python
try:
    import x
except ImportError:
    ...
```
- **Bad:**
```rust
if which("pandoc").is_ok() { ... } else { ... }
```
- **Better:**
```text
Doctor/setup verifies dependencies.
Runtime assumes them.
Missing dependency is a setup failure and should crash loudly.
```
- **What this burns:**
  - try-import stubs
  - dependency fallback paths
  - skipif dependency missing
  - “works without X” branches
  - mocked stand-ins
  - fallback providers

### 4. No partial success

Owned commands should either complete the claimed operation or return a hard error.

- **Bad:**
```text
return { ok: true, warnings: [...] }
return partial entries after read_dir error
render with missing diagrams but show warning
save file but fail to remove backup silently
```
- **Better:**
```text
If an owned substep fails, the operation fails.
```
- **What this burns:**
  - warning laundering
  - partial object success
  - empty-array-on-error
  - best-effort modes
  - hidden data loss
  - soft failure states

### 5. No proof-free smoke tests

No tests that are not proof-bearing. If a diagnostic harness is genuinely useful, it should live outside the test/QC proof path as a command, not as a test-shaped artifact.

- **Bad:**
```text
browser-smoke test with mocked IPC
harness test that only proves mount
test renamed to “smoke” after review
```
- **Better:**
```text
diagnostic command: just diagnose-frontend-shell
or real test: exercises real Tauri IPC boundary
```
- **What this burns:**
  - honest-label laundering
  - mocked E2E tests
  - “non-proof test” explanations
  - future agents citing smoke as evidence
  - test suite pollution

If it is in the test suite, it proves repository-owned behavior. Otherwise it is not a test.

### 6. No mocks, fakes, stubs, or simulated environments

Do not allow:
- mocks
- fake APIs
- test doubles
- stub services
- simulated filesystems
- mocked Tauri IPC
- mocked network responses as proof

Use:
- real boundary
- captured real response
- local real service
- fixture file with real structure
- explicit diagnostic outside proof path

And add:
*Deleting a mock test is not enough. The proof burden must be replaced, invalidated, or recorded as unresolved.*

### 7. No deletion without burden disposition

When slop is found, agents will either launder it or delete it. Deletion can be laundering if the original problem disappears with the artifact.

Required before deleting a criticized artifact:
- What original problem caused this to exist?
- Is that problem still live?
- Where is it now solved?
- If unsolved, where is it explicitly recorded?
- Could a future agent reintroduce the same artifact?

- **What this burns:**
  - cleanup-as-resolution
  - removing fake tests without replacing proof
  - deleting wrappers while leaving the integration gap
  - closing review threads because evidence disappeared

*Slop remediation is obligation management, not artifact management.*

### 8. No boolean mode flags in owned APIs

Boolean flags are one of the easiest ways to hide policy choices.

- **Bad:**
```rust
require_or_default(value, config_exists, message, default)
save(path, allow_external)
render(markdown, strict)
```
- **Better:**
```rust
load_default_config()
load_user_config(path)
save_workspace_file(...)
save_absolute_file(...)
render_checked(...)
```
Or use an enum with explicit states if there are genuinely multiple modes.

- **What this burns:**
  - branch-forcing tests
  - helper-local proof laundering
  - wrong flag at call site
  - unclear semantics
  - “true means strict?” ambiguity

In tests, a boolean often means the test is not constructing the real state. It is just selecting the branch it wants.

### 9. No helper-level proof for boundary-level obligations

A review comment about startup config, file save, Tauri IPC, subprocess lifecycle, or E2E behavior must be resolved at that boundary.

- **Bad:**
```text
review: config startup defaults are wrong
fix: add tests for require_or_default(...)
```
- **Better:**
```text
test actual config file absent/present/malformed through build_initial_state
test actual save operation through command boundary
test actual subprocess timeout kills the process
```
- **What this burns:**
  - new helper extracted after review
  - unit tests that mirror the patch
  - proof of branch behavior instead of product behavior
  - tests that would pass if the app stopped calling the helper

*Helper tests are supplementary. They cannot resolve boundary feedback.*

### 10. No exact string assertions unless the string is a public contract

Exact string assertions are often tautological, especially when the test passes the string into the function.

- **Bad:**
```rust
let error = helper(None, true, "missing foo", default).unwrap_err();
assert_eq!(error, "missing foo");
```
- **Better:**
```rust
assert!(matches!(error, ConfigError::MissingRequired { key } if key == "pandoc.render_command"));
```
Or, better still, test the actual boundary and assert that it fails with a structured error.

- **What this burns:**
  - message plumbing tests
  - brittle implementation coupling
  - tests that prove the test’s own literal

### 11. No stringly typed errors for owned failures

Owned errors should be structured. Strings can be rendered at the edge. They should not be the internal contract.

- **Bad:**
```rust
Result<T, String>
Err("missing config value".into())
```
- **Better:**
```rust
enum ConfigError {
    MissingRequired { key: &'static str },
    MalformedToml { path: PathBuf, source: toml::de::Error },
}
```
- **What this burns:**
  - exact string tests
  - ambiguous failure classification
  - review-thread debates about wording
  - catch-all error laundering

### 12. No `Option<T>` in initialized core state for required data

Optionality belongs at the boundary, before normalization. After initialization, required state should be total. If initialization cannot supply the field, initialization fails.

- **Bad:**
```rust
struct AppState {
    render_command: Option<String>,
    workspace_root: Option<PathBuf>,
}
```
- **Better:**
```rust
struct AppState {
    render_command: String,
    workspace_root: PathBuf,
}
```
- **What this burns:**
  - repeated unwrap_or
  - defensive guards
  - impossible-condition tests
  - runtime fallback decisions
  - soft initialization

### 13. No ambient discovery chains

Discovery chains are fallbacks in disguise.

- **Bad:**
```text
look in env var
then project config
then home config
then built-in default
then inferred current directory
```
- **Better:**
```text
one configured path
or one explicit startup rule
or one setup-generated config
```
If multiple locations are truly supported, they should be an explicit ordered contract with tests. But for agent-driven bespoke software, the default should be one source.

- **What this burns:**
  - local-artifact laundering
  - mystery config precedence
  - probe-driven behavior
  - “works because it found something else”

### 14. No hidden global state as source of truth

Do not let the app infer behavior from installed tools, current directory, environment variables, shell profiles, caches, or home-directory artifacts unless that is explicitly the product contract.

- **Bad:**
```text
if fd installed use fd else find
if env var exists use it else config
read ~/.something because maybe credentials are there
```
- **Better:**
```text
config declares the command/path/provider
doctor verifies it
runtime uses it
```
- **What this burns:**
  - installed-tool-first behavior
  - local snooping
  - implicit user preference inference
  - environment-dependent tests

### 15. No local QC authority

Do not let repos define their own generic lint/type/test/coverage gates. They delegate to global QC.

- **What this burns:**
  - local recipe proliferation
  - narrow check passing
  - per-repo tool drift
  - agents modifying QC to pass

### 16. No bypass comments

No:
- `# type: ignore`
- `# noqa`
- `# pragma: no cover`
- `eslint-disable`
- `ts-ignore`
- `skip`
- `xfail`

If the tool is wrong, fix the type surface, change the code shape, or escalate.

- **What this burns:**
  - checker appeasement
  - proof masking
  - silent escape hatches

### 17. No compatibility shims or legacy paths in pre-launch bespoke software

No:
- legacy adapter
- deprecated path
- backward-compatible parser
- old config loader
- compat mode

Replace the old path. Delete it after transferring the burden.

- **What this burns:**
  - branch accretion
  - fallback preservation
  - “just in case” code
  - parallel implementations

### 18. No general-purpose defensive validation inside trusted hot paths

Validate once at the owned boundary, then use total types internally.

- **Bad:**
```text
every function checks null, malformed input, missing fields, impossible variants
```
- **Better:**
```text
boundary validates
core assumes
asserts document impossible states
```
- **What this burns:**
  - enterprise edge-case accretion
  - impossible-condition tests
  - hot-path defensive programming
  - logic noise

### 19. No “quarantine” as remediation

Quarantine language is often fluent laundering.

Suspicious words:
- `quarantined`
- `isolated`
- `non-proof`
- `smoke-only`
- `legacy`
- `diagnostic-only`
- `temporary`
- `compatibility`
- `fallback`
- `scaffold`
- `future-owned`
- `out-of-scope`

These terms trigger a burden-disposition check:
- What problem remains?
- Why does this artifact still exist?
- Can future agents cite it as proof?
- Is it in a proof path?

If yes, it is still slop.

### 20. No issue/comment/documentation as completion

Administrative artifacts can preserve truth, but they do not solve implementation/proof obligations.

- **Bad:**
```text
opened issue, therefore resolved
documented limitation, therefore fixed
renamed test, therefore compliant
comment explains fake proof, therefore okay
```
- **Better:**
```text
issue records unresolved burden
PR remains incomplete unless original task was only to document/triage
```
- **What this burns:**
  - completion laundering
  - metadata as progress
  - future-work as resolution

---

## Policy Exception Protocol

A policy exception must not be granted casually. Any exception requires:
1. **Explicit request:** Explicit user request or source-backed product requirement.
2. **Policy identified:** Stating the exact named policy being violated.
3. **Justification:** Explaining why the blanket rule blocks a real required behavior.
4. **Replacement invariant:** Defining a replacement invariant that prevents the old gaming behavior.
5. **Boundary proof:** Providing proof at the owned boundary.
6. **Audit trail:** Visible commit/PR explanation recording the exception details.

For example, an exception allowing a fallback provider is only allowed if the product explicitly owns multi-provider behavior, and tests prove that: provider selection is explicit, failure is visible, no fake data is returned, the user can tell which provider ran, and config declares the provider order.

* * *

## Verification-Poison Dependencies

Do not recommend, install, template, or casually mention dependencies whose main effect is to make fake proof easier.

Examples include mock frameworks, patch helpers, request-mocking libraries, fake service frameworks, and time/network/filesystem simulation tools unless a skill explicitly discusses them as prohibited patterns.

A dependency is not acceptable merely because it is common. If it helps the agent avoid a real owned boundary, captured real fixture, live integration check, or substantive assertion, it is proof-loop poison.

### Dependency Taxonomy

| Category | Treatment | Examples |
| --- | --- | --- |
| **Known semantic dependency** | Preferred when it replaces bespoke logic | `pydantic`, `httpx`, `numpy` |
| **Generic QC/tool dependency** | Run ephemerally from central/global QC, not installed per-repo | `mypy`, `ruff`, `pytest`, `pytest-cov` |
| **Repo-owned runtime/build/plugin dependency** | Declare locally in pyproject.toml | `pydantic`, project-specific plugins |
| **Agent-authored one-off Python dependency** | PEP 723 inline metadata + `uv run` | `mistralai` for a one-off script |
| **Verification-poison dependency** | Forbidden by default | `pytest-mock`, `unittest.mock`, `responses`, `moto`, `freezegun`, `requests-mock` |
| **Global/system dependency** | Exceptional and explicitly bounded | `sudo apt install`, `brew install`, `npm install -g` |

## Behavioral Seed Hygiene

Every skill example is a behavioral seed.

Do not include commands, packages, test patterns, or workflow templates that would be unsafe if copied by an agent outside the narrow context.

Skills must not seed:
- mocks, fakes, stubs, or simulation-first testing
- pip/system/global installs (use `uvx`, `npx`, `bunx`, or PEP 723 `uv run --script`)
- generic QC tools as per-repo dependencies
- stderr suppression in diagnostic commands
- checklist theater
- local-artifact research for external-owned questions
- fallback/default/special-case patterns that hide failure
- pipe-to-shell installers
- sudo/system mutation
- broad "comprehensive" testing detached from owned claims

### Cross-References (Source-of-Truth Skills)

Rather than repeating policy in every skill, reference the canonical source:

| Domain | Canonical Skill |
| --- | --- |
| Testing behavior | `test-guidelines` |
| Debugging behavior | `reality-grounded-debugging` + `systematic-debugging` |
| External tools/errors | `known-solution-first` |
| Tool execution | runner-first tooling / uv script pathway |
| QC | `quality-control` |
| Skill authoring | `creating-skills` |
| Dependency provisioning | tool-provisioning-and-environment-hygiene
