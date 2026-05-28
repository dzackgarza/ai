---
name: reviewing-llm-code
description: Use when reviewing code, tests, QC, or documentation produced by an LLM or coding agent, especially when the user asks for bad patterns, low-quality code, shallow work, review of Deepseek/Codex/Claude/Jules output, or why an agent-produced change is untrustworthy.
---

# Reviewing LLM Code

Review LLM-produced code as an agent-failure audit, not as a normal bug list.
The point is to identify the mechanisms that made bad work look acceptable.

**This is NOT a bug review.** This review happens AFTER all obvious bugs have been worked out.
If you find yourself reporting bugs, performance issues, missing features, or compilation errors, you are doing the wrong kind of review.
Those are object-level defects.
This review is about something completely different.

**This review is about CODE QUALITY, MAINTAINABILITY, and READABILITY.** It is about the STYLE of the code — whether the implementation is the result of reflexive hacks layered on top of each other, or whether it is clean, idiomatic, and maintainable.
This is a step in paying down technical debt, NOT remediating bugs.

**Your opinions about what is “bad code” are irrelevant.** The skill is TELLING you exactly what code quality indicators to flag.
If you start returning performance issues, “missing” edge cases, or architectural preferences that are not in the loaded patterns, you are goal-substituting: instead of doing the hard work of evaluating style against the skill’s criteria, you are pattern-matching what YOU think is bad code.
That is not analysis.
That is substitution.

The loaded skills define the complete set of findings.
If a finding does not match a pattern in the loaded skills, it is not a finding.
Drop it.

## Design Choices Are Not Slop (Read This First)

**This is not a standard code review.** The review would not be happening if the code did not work as intended on at least one user-requested happy path.
The outward-facing behavior is almost certainly correct — the user asked for it and it works.
That is not what you are reviewing.

You are reviewing the **implementation quality beneath the correct behavior**: whether the core is rotten, unmaintainable, the result of repeated reflexive hacks layered on top of each other to satisfy the user’s literal requests.

**Use theory of mind.** The code was produced by a process: a user telling an LLM to implement very specific things.
The LLM reflexively added what the user literally asked for.
Any seemingly strange choice about features, behavior, or coupling to externals is **almost certainly a user-driven design decision**, not LLM slop.
An LLM would never voluntarily make an out-of-distribution design choice in isolation — it has no reason to.
If the code couples a Pandoc settings GUI to an internally stored Pandoc command, that is not “brittle coupling.”
That is a user-requested feature.
If the code has an unusual feature scope, unexpected external dependency, or surprising behavioral constraint, that is a design choice the user made, not evidence of bad architecture.

**The review must separate two categories:**

1. **Design choices** (features, behavior, coupling, scope, constraints): these are premises.
   Do not critique them.
   They are the user’s intentional decisions and an LLM would never produce them in isolation.
   Treating them as slop is a theory-of-mind failure — you are attributing user intent to LLM reflexes.

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

## Brittleness Is Not Edge-Case Coverage (Read This Second)

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
  **Regex is ALWAYS suspect.** Most data shapes rarely or never change, and most data sources have semantic parsers which are 1000x more tested.
  Use those.

- **Tight coupling to implementation details**: code that depends on the internal shape of another module’s output, the exact order of keys in a dictionary, or the specific text of an error message.
  When the other module changes, this code breaks.

- **Large blast radius per change**: a single edit requires synchronized changes in multiple files, because the code is not organized around stable interfaces.

The review question is: **“If a future agent changes the thing this code depends on, how many other things break?”** If the answer is “many,” the code is brittle — not because it lacks edge cases, but because its dependencies are unstable and its truth is scattered.

## This Is Bespoke Software (Read This Third)

**Most software this LLM reviews is ONE USER’S BESPOKE SOFTWARE, running on THEIR SYSTEM.** It is not an enterprise product for unknown users.
It is private, on this system, designed to tightly couple to this system’s programs and dependencies.
The audience is future-me or future-agents.
It will likely never be “distributed” in any real sense.
It will generalize to others at some other time, if ever.

**The bad patterns to watch for are the OPPOSITE of what a normal code review would flag.** A “helpful” reviewer might surface these as defects.
They are not.
They are signs that the agent is writing enterprise software for an imaginary audience instead of a minimal MVP for the actual user:

- **Graceful degradation when dependencies are missing**: the code tries to “work” even when its required tools are not installed.
  This is WRONG for bespoke software.
  The correct behavior is to fail loudly and tell the user to install the dependency.
  The code is on THIS system.
  The dependency IS available.
  “Graceful degradation” is enterprise thinking for unknown deployment targets.

- **Squishy input shapes**: the code accepts many different input formats, “normalizes” them, handles “various” data shapes.
  This is WRONG for bespoke software.
  The code owns its data.
  Enforce the shape.
  If the input is wrong, fail loudly and fix the input.
  Do not write defensive code to accommodate data that should never arrive.

- **Over-generalization to other platforms or users**: the code tries to work on Windows AND Linux AND macOS, or for multiple user personas, or with multiple backends.
  This is WRONG for bespoke software.
  The code runs on THIS system for THIS user.
  Target it.
  If it needs to work elsewhere later, that is a future problem for future-me with a future agent.

- **Enterprise-grade edge-case handling**: the code catches every possible error, wraps everything in try/catch, handles every conceivable malformed input.
  This is WRONG for bespoke software.
  The correct behavior is: work on the happy path, fail loudly outside of it.
  Functionality for slightly-off-the-happy-path workflows is a simple matter of future-me branching the repo and asking an agent to accommodate it.

**The philosophical principle**: less bespoke code, more reliance on dependencies, more copying and sharing of known patterns.
Complex logic that isn’t composition or glue is highly suspect.
Complex *interactions* with dependencies or external programs are the expected default.
Prefer code that knows its data and knows how to handle it.
Prefer enforcing data shape to eliminate the logic needed by the code at all.

## LOC Reduction Through Idiomatic Patterns (Read This Fourth)

**The review should actively look for opportunities to reduce LOC through idiomatic language patterns.** This is NOT about making code shorter for its own sake.
It is about whether the code is expressing a simple operation in a complex way because the agent does not know the idiomatic pattern.

Key transformations to look for:

- **Imperative → functional**: `for` loops with accumulators that should be `map`, `filter`, `flatMap`, `reduce`, `partition`, list comprehensions, generator expressions.
  The functional form is usually shorter, clearer, and less error-prone.

- **Nested branching → data-aware dispatch**: deep `if`/`else` trees that should be a lookup table, dictionary dispatch, pattern matching, function overloading, or strategy pattern.
  If the code branches on the *type* or *kind* of data, the data should enumerate its own handlers.

- **Manual iteration → library calls**: hand-rolled pagination, batching, retries, rate limiting, caching, or serialization that a library already provides.

- **String manipulation → typed operations**: building JSON by string concatenation, constructing queries by string interpolation, parsing XML with regex — all of these have typed alternatives that are shorter and correct.

- **Boilerplate → framework conventions**: manual route registration, manual dependency injection, manual test setup that a framework handles declaratively.

**Before writing a finding about complex code, ask: could this be expressed in fewer lines using the idiomatic patterns of this language?** If yes, the complexity is slop — the agent did not know the idiom and wrote the operation longhand.

**Dependencies reduce LOC.** Offloading logic to a dependency is almost always better than hand-rolling the same logic.
The process is: create a regression test asserting behavioral equivalence, then replace the bespoke implementation with the dependency.
The test proves the replacement is safe.
The dependency is now the maintained, tested implementation.
The bespoke code is gone.

## Required Background

Before producing review findings, load these skills in this order:

- **`anti-slop`** — Read first.
  This skill teaches you what slop looks like.
  You cannot recognize generated-code residue without it.
  All code you review is agent-produced and almost always contains slop.
  Read its `references/code-patterns.md` and `references/test-patterns.md`.

- **`references/pattern-catalog.md`** — Read second.
  The canonical catalog of concrete LLM code, test, QC, and documentation failure patterns.
  Read this to learn the specific signatures to look for.

- **`llm-failure-modes`** — Read third.
  This teaches the cognitive failure modes that produce slop: ground-up bias, dependency aversion, meta-artifact delegation, replacement instinct, overconfidence, confabulation.
  You must understand WHY agents produce bad code before you can spot it.

- **`llm-failure-modes/coding-failures.md`** — The specific coding failure modes.

- **`llm-failure-modes/testing-failures.md`** — The specific testing failure modes.

- **`llm-failure-modes/structural-failures.md`** — Structural wrongness patterns.

- **`llm-failure-modes/field-observations.md`** — Field-observed behavioral patterns.

- **`llm-failure-modes/jerry-behaviour.md`** — How evaluator agents fail to catch slop.

- **`llm-failure-modes/references/behavioral-detection-methodology.md`** — How to detect behavioral failures without turning observations into interaction-specific narratives.

- **`addressing-shallow-work`** — How to avoid adding structure instead of fixing the actual problem.

- **`reviewing-subagent-work`** — The Synthesis Gate for verifying subagent output.

Also load as applicable:

- `test-guidelines` when the review includes tests, QC, smoke checks, CI, or proof surfaces.

- `thermo-nuclear-code-quality-review` when the review includes maintainability, architecture, abstractions, giant files, or code that feels obviously badly shaped.

Do not summarize these skills in the review.
Use them to shape the judgment.

**Critical framing**: You are not reviewing code because you already know what slop looks like.
You are reviewing code BECAUSE you do not know what slop looks like, and these skills teach you.
The skills are curriculum, not reference.
Read them to learn the patterns, then apply that learning to the code.
If you skip reading the skills first, you will miss slop that you did not know to look for.

## Systematic Analysis Procedure (Mandatory)

**Do NOT start producing findings after a cursory scan.** LLM slop hides in the structures the agent built, not in individual lines.
You cannot find it by skimming, grepping for "bad patterns," or reading the files you think are suspicious.
You must systematically understand the entire codebase before producing a single finding.

### Phase 1: Map the Codebase

Start with a broad structural survey.
Use `tree` (not `ls`, not `grep`) to understand the full layout:

```
tree -I node_modules --dirsfirst -L 3
```

Then identify:
- Total LOC and language breakdown (use `cloc` or `pygount` if available)
- The entrypoint(s) — what does the user actually run?
- The dependency graph — what imports what?
- File modification dates — where has churn happened?
  (use `exa -l --sort=modified` or `ls -lt` on key directories)

**Do NOT skip this step.** If you do not know the full shape of the codebase, you cannot distinguish design choices from slop, and you will produce findings about symptoms instead of root causes.

### Phase 2: Understand the Git History

LLM slop often appears as churn — layers of additions without refactoring.
Check:

```bash
git log --oneline -30          # recent commits
git log --stat -10             # what files changed most
git log --diff-filter=A --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20
                               # most-added files (evidence of ground-up generation)
```

Look for:
- Commits that add entire files instead of editing existing ones (ground-up bias)
- Files that were added, then modified repeatedly without consolidation (patch accretion)
- Large diffs where surgical edits would suffice (regeneration vs.
  mutation)
- Features that were added and then immediately needed fixes (reflexive implementation)

### Phase 3: Read the Actual Code

Do NOT grep for keywords and call it analysis.
Read the files that matter, in order:

1. The entrypoint(s) — understand what the app actually does
2. The core logic files — where does nontrivial computation happen?
3. The configuration and setup — what decisions did the agent make?
4. The test files — what is actually being proven?

For each file, ask:
- **Why does this file exist?** Could its contents be 5 lines of imports and composition?
- **Why does this function exist?** Is there a library that does this?
- **Why is this logic HERE instead of in a dependency?** What justifies bespoke code?
- **Where is the churn?** Which files have been modified most recently?
  What changed?

### Phase 4: Identify the Slope of the Code

Before producing findings, answer these questions in writing:

1. **What is the simplest possible version of this app?** If you were rewriting it from scratch using only imports, compositions of existing tools, and minimal glue code — what would it look like?
   How many files?
   How many lines?

2. **What code in this app has no justification for existing?** Where did the agent write something that a library, CLI tool, or API call already handles?
   Where did the agent reinvent a solved problem?

3. **Where is the nontrivial logic, and why does it need to exist?** Most of this app should be trivial composition.
   Where is it not?
   What makes those parts necessary?

4. **What would this app look like if the agent had searched for existing solutions before writing code?** The gap between that vision and the current codebase IS the slop.

**If you cannot answer these questions, you are not ready to produce findings.** Go back to Phase 1.

## Synthesis Gate

Before writing findings, answer internally:

**“The LLM code is untrustworthy because it repeatedly uses _____ to make _____ look verified, while the repository actually owns _____.”**

If this sentence cannot be filled with a concrete mechanism, do more inspection.
Do not compensate by adding more bullets.

Also answer:

**“The strongest live goal is _____; the current proof loop does or does not prove that goal because _____; the mess was caused by _____.”**

If you cannot identify the live work and the broken proof loop, do not list triage items.
Reviews must fix the frame before ranking fixes.
A review that proposes adding more tests before repairing a fundamentally stale, bypassed, or noncanonical test gate is creating more false confidence, not increasing correctness.

Also answer:

**“For each finding I plan to make: can I point to a SPECIFIC code pattern from the loaded skills that proves the LLM introduced this independently?”**

You CANNOT determine this by judgment.
You can only determine it by matching against the concrete patterns in the loaded skills: patch accretion, stacked conditionals, dead control flow, dependency aversion, ground-up bias, proof-loop failures, error laundering, QC appeasement, etc.
If you cannot match the finding to one of these patterns, you have not proven it is implementation quality.
Drop it.

Also check against the mechanical design-choice signals: does the code integrate with an external tool?
Implement a specific named feature?
Couple components that would not normally be coupled?
Have narrow specific scope?
Have arbitrary-seeming but deliberate behavioral constraints?
If ANY of these are true, the finding is a design choice.
Drop it.

## Existential Justification Gate (Mandatory)

Before producing ANY finding, you must answer this question for the code in question:

**"Why does this code exist at all?"**

Not "what does it do" — that is obvious from reading it.
But WHY was it written?
What justified its existence?
Could the entire block be replaced by:

- A single import from an existing library?
- A call to an external CLI tool?
- A composition of 2-3 existing functions?
- A configuration change that eliminates the need for the code entirely?
- A data model change that makes the logic unnecessary?

**Every nontrivial line of code must justify its existence to survive this review unscathed.** If the answer is "the agent wrote it because it didn't search for an existing solution," that is dependency aversion — the most common and most damaging LLM failure mode.

**The review must also answer:** Even after refactoring, why MUST this functionality still be owned by THIS app?
Can it be:

- Replaced by an external tool or API?
- Consolidated into a standalone module that other projects could use?
- Eliminated entirely by changing the data model or configuration?
- Delegated to a dependency that already handles this concern?

If the answer is "the agent could have avoided writing this by doing X," the finding is not about code quality — it is about the agent's failure to think before writing.
That is the finding.

**This is the difference between a linter report and an agent-failure audit.** A linter says "this line could be shorter."
This audit says "this line should never have been written, and the fact that it exists proves the agent did not search for an existing solution."

## Priority Calibration

Before ranking findings, identify which layer currently blocks trustworthy progress:

1. the canonical proof loop itself;

2. the user-visible happy path the loop should prove;

3. representative regression fixtures for that happy path;

4. cleanup, maintainability, and architectural debt.

If the proof loop is broken, that is the first finding.
Do not start by recommending new tests, more fixture coverage, extra inventories, or broad freezes while the existing gate can pass against stale artifacts, bypass the runtime path, or validate the wrong system.
First repair the loop so future tests can mean something.

Treat repo-local product choices as premises unless the user asks for architecture review or the choice contradicts the stated goal.
Do not critique intentional bespoke choices as if the software were an enterprise product for unknown users.
For personal or research tooling, a hard local invariant can be correct; the review question is whether the proof loop verifies that invariant on the real workflow.

## What A Useful Review Finds

A useful review names patterns a maintainer can act on:

- proof laundering through narrow or standalone checks;

- unified test-gate bypasses;

- tests that prove shape, existence, or command activity instead of owned behavior;

- runtime and tests sharing the same flawed boundary;

- code/prose contradictions inside the same artifact;

- UI surfaces that advertise behavior not wired to the service;

- duplicated domain contracts across producer, runtime, UI, and tests;

- **brittleness as blast-radius smell**: scattered truth (same concept in multiple places), coupling to volatile data (string outputs, exact structures, exact log messages), tight coupling to implementation details, or regex used where simpler correct approaches exist — the review question is “if a future agent changes the thing this code depends on, how many other things break?”
  not “does this handle edge cases?”
  See **Brittleness Is Not Edge-Case Coverage** and `anti-slop/references/code-patterns.md` → **Brittleness as blast-radius smell**;

- **enterprise patterns in bespoke software**: graceful degradation when dependencies are missing, squishy input shapes, over-generalization to other platforms or users, enterprise-grade edge-case handling — all inappropriate for one user’s private tool on their own system.
  The correct behavior is: work on the happy path, fail loudly outside of it.
  See **This Is Bespoke Software** and `anti-slop/references/code-patterns.md` → **Enterprise Patterns in Bespoke Software**;

- **needless imperative complexity**: code that could be expressed in fewer lines using idiomatic language patterns — imperative loops that should be functional (map/filter/reduce), nested branching that should be data-aware dispatch (lookup tables, pattern matching, overloads), manual iteration that should be library calls, string manipulation that should be typed operations.
  The complexity is slop when the idiom exists and the agent did not know it.
  See `anti-slop/references/code-patterns.md` → **LOC Reduction Through Idiomatic Patterns**;

- **“clean” or “lightweight” as justification for suppressing features**: when an agent justifies NOT implementing a requested feature, removing existing functionality, or rejecting a design choice by calling it “dirty”, “heavy”, “not clean”, “not lightweight”, “overengineered”, or “unnecessarily complex” — that is goal substitution.
  Every feature is an EXPLICIT user request.
  The agent found the feature hard to implement, so it reframed the difficulty as a quality problem to avoid doing the work.
  “Clean” and “lightweight” are not properties of features — they are properties of implementations.
  A feature is either requested or not.
  How it is implemented is a separate question.
  If the agent suppresses a feature because it “isn’t clean,” the agent is substituting its own aesthetic judgment for the user’s explicit request;

- fallback branches that weaken invariants tests pretend to enforce;

- fake success paths: caught owned failures returning success-shaped state;

- **timing or performance assertions in tests**: tests that assert on timing, responsiveness, latency, or throughput — these chase imaginary issues, inflate test coverage with hallucinated targets, and prove nothing about correctness.
  Performance belongs in CI gates, not unit tests.
  Users notice choppiness and ask for a fix; they do not ask for “popup loads in <=50ms”. See **Test Patterns** → **Timing or performance assertions**;

- god objects and unsegmented service interfaces;

- manual enumeration of the same concept in several distant places;

- boolean theater: `return true` APIs whose values callers ignore;

- stale generations of a feature left alive beside the new one;

- tool-appeasement debris, unreachable casts, raw debug logs, and half-refactors;

- reimplementation where a repo-local abstraction already exists;

- **structural complexity that should be a dependency call**: long functions, for loops over collections, high density of if/else branches, deeply nested indentation, convoluted control flow, large classes, or files with many helper functions — the first question for any of these is “what library already does this?”
  not “is this correct?”
  See `anti-slop/references/code-patterns.md` → **Complexity as a Dependency-Detection Signal**;

- massive diffs where surgical edits would suffice — the agent regenerated an entire region rather than changing five lines, evidence of ground-up bias;

- refusal to refactor and repurpose — existing code treated as immutable background noise rather than raw material, with the agent writing new leaves instead of adapting existing branches;

- process split that lets an agent report a subset as if it were the whole gate.

These are patterns.
Each finding must explain how the pattern can produce more bad work, not merely that one line is ugly.

## Pattern Catalog

Load [`references/pattern-catalog.md`](references/pattern-catalog.md) before producing findings.
It is the canonical list for automaton-grade code, test, QC, and documentation patterns, including regex against semantic formats, developer-controlled test assertions, fallback laundering, recipe bypasses, fake data, no-op behavior, and stale documentation.

## What Not To Do

Do not write a linter report.

Do not critique design choices.
Use the mechanical checklist from **Design Choices Are Not Slop** — if ANY of those signals are true (integrates with external tool, implements specific named feature, couples normally-uncoupled components, narrow specific scope, deliberate behavioral constraints), the code is a design choice.
Stop.
Do not critique it.
The user asked for it.
Move on.

**Do not bring trivial nits.** This review is NOT about:
- "This function could be a one-liner" (unless the one-liner is a library call that
  eliminates the function entirely)
- "This switch could be a Record lookup" (style preference, not slop)
- "This loop could be map/filter" (unless the loop is 50+ lines of bespoke logic that
  a library already handles)
- "This variable name could be better" (linter output, not analysis)
- "This file is too long" (unless the length is caused by scattered truth or patch
  accretion)
- "This code duplicates X" (only a finding if the duplication is caused by the agent
  creating a problem and then writing bespoke code to solve it, or by dependency
  aversion)

**The bar for findings is high.** A finding must name a pattern from the loaded skills
that explains WHY the code is shaped this way, not just THAT it could be different.
If you can only say "this could be shorter," you have not found slop — you have found a
style preference. Drop it.

**LLM slop is not the same as human bad code.** Human developers write verbose code
because they are careful, because they are learning, or because the codebase evolved
organically. LLMs write verbose code because they did not search for existing solutions,
because they reinvented solved problems, or because they built infrastructure to cope
with their own earlier mistakes. The review must distinguish these. A human wrote a
long function because the logic is genuinely complex? Not slop. An LLM wrote a long
function because it didn't know about a library that does the same thing in one call?
That IS slop. The difference is whether the complexity is justified by the domain or
caused by the agent's failure to search.

Bad review shape:

- “This command failed.”
  (bug review, not this review)

- “This line is formatted wrong.”
  (linter output, not analysis)

- “This function should handle edge cases.”
  (the skill says not to)

- “This path is hard-coded.”
  (may be a deliberate local invariant)

- “This test could use more coverage.”
  (not this review’s scope)

- “This couples the GUI to an internal command” (user asked for that coupling)

- “This feature scope seems oddly specific” (user asked for that specific feature)

- “This external dependency seems unnecessary” (user wanted that integration)

- “This code freezes the server / is slow / has bad performance” (performance review, not this review)

- “This code is missing feature X” (feature request, not this review)

- “This code has a bug in edge case Y” (bug review, not this review)

- “This component is a god object / monolithic” (aesthetic judgment, not a pattern match unless you can point to the specific pattern)

- "The code should be refactored to be cleaner" (opinion, not a finding from the loaded skills)

- "This function could be a one-liner" (style nit, unless the one-liner is a library call)

- "This switch could be a Record" (style preference)

- "This loop could be map/filter" (only if the loop is bespoke logic a library handles)

- "This variable name is bad" (linter output)

- "This file is too long" (only if caused by scattered truth or patch accretion)

Useful review shape:

- “This standalone recipe bypasses the unified gate, so agents can validate a subset and present it as project proof.”

- “Runtime and tests call the same cached external package, so both can pass while local integration is broken.”

- “The UI has two overlapping usage surfaces; behavior is wired to the old hidden one while the visible one only changes state.”

- “The test declares missing provider icons unacceptable, but runtime has a generic fallback, so the invariant is split.”

Do not critique intentional machine-local contracts as portability bugs.
Critique hard-coding when it splits truth, hides data ownership, or launders failure, not when it states a deliberate local invariant.
Do not ask for defensive branches around owned providers or owned scripts.
Do not invent edge-case work unless it ties to an observed failure or an invariant the repo actually owns.
Do not call a review complete because you found command output, hashes, file existence, or test counts.

## Review Procedure

Read the artifacts in this order:

- User directive and any corrections in the conversation.

- Repo-local instructions and nearby docs.

- The actual diff, current files, and relevant recent commits.

- The test/QC entrypoints and which ones are canonical.

- The runtime boundary the change claims to prove.

Then identify the repository-owned behavior:

- What active feature or repair is currently in progress?

- What user-stated design choices are intentional and should be preserved?

- What public or user-visible behavior should work?

- What data contract does the repo own?

- What proof surface is supposed to establish correctness?

- What would remain broken even if the current tests pass?

- What caused the current bad state: stale artifacts, bypassed gates, fake fixtures, goal substitution, split commands, hidden runtime state, or another mechanism?

Then inspect for LLM-specific mechanisms:

- Where did the agent add surface instead of deleting or simplifying?

- Where did it split proof across commands?

- Where did it make success easier to claim?

- Where did it create visual/UI or API shape without real behavior?

- Where did it copy a contract instead of owning it in one place?

- Where did tests mirror implementation instead of independently proving behavior?

## Finding Format

Use this structure for each substantive finding:

```markdown
## [Pattern Name]

Pattern: [mechanism, not symptom]

Concrete evidence:

- `[file:line]` [specific code behavior]
- `[file:line]` [related code behavior]
- [optional commit or command evidence]

Why this matters:

[How this mechanism lets bad work pass, hides failures, or increases future agent
damage.]

Existential justification:

[WHY does this code exist at all? What justified the agent writing it instead of
using an existing solution? Even after refactoring, why MUST this functionality be
owned by this app — can it be replaced by an external tool, consolidated into a
dependency, or eliminated by changing the data model?]

Failure mode: [name from loaded failure-mode skills]
```

If a finding cannot fill “Pattern”, “Why this matters”, and “Existential justification”,
it is probably a nitpick.
Drop it or merge it into a larger pattern.

## Required Negative Finding Format

When saying something was not found, use:

```markdown
- Searched: [specific files, commits, recipes, commands]
- Found: [what was found and not found]
- Conclusion: [inference, not absolute claim]
- Confidence: [High / Medium / Low]
- Gaps: [what remains unknown]
```

## Calibration Rules

Treat these as strong review findings:

- A direct route around the canonical test command.

- Local and CI gates proving different behavior classes.

- A smoke test that checks logs instead of the app-owned contract.

- A test that can pass while the user-visible workflow is broken.

- Runtime code and tests invoking the same stale/cached dependency boundary.

- Multiple copies of the same schema or domain concept;

- **Brittleness as blast-radius smell.** Code where small changes have large blast radii: scattered truth, coupling to volatile data (string outputs, exact structures, exact log messages), tight coupling to implementation details, or regex used where simpler correct approaches exist.
  The reviewer’s question is “if a future agent changes the thing this code depends on, how many other things break?”
  NOT “does this handle edge cases?”
  Edge-case handling is a natural consequence of planned development, not a quality signal.
  See **Brittleness Is Not Edge-Case Coverage**.

- **Enterprise patterns in bespoke software.** Graceful degradation when dependencies are missing, squishy input shapes, over-generalization to other platforms or users, enterprise-grade edge-case handling — all inappropriate for one user’s private tool on their own system.
  The correct behavior is: work on the happy path, fail loudly outside of it.
  See **This Is Bespoke Software**.

- **Needless complexity that could be idiomatic.** Code that could be expressed in fewer lines using idiomatic language patterns: imperative loops that should be functional, nested branching that should be data-aware dispatch, manual iteration that should be library calls, string manipulation that should be typed operations.
  The complexity is slop when the idiom exists and the agent did not know it.
  See **LOC Reduction Through Idiomatic Patterns**.

- **“Clean” or “lightweight” as justification for suppressing features.** When the agent justifies NOT implementing a requested feature by calling it “dirty”, “heavy”, “not clean”, “not lightweight”, “overengineered”, or “unnecessarily complex” — that is goal substitution.
  Every feature is an EXPLICIT user request.
  The agent found it hard to implement and reframed the difficulty as a quality problem.
  “Clean” and “lightweight” are properties of implementations, not features.
  A feature is either requested or not.

- A UI control whose handler is a log statement.

- A “fail fast” comment beside code that catches and returns success-shaped state.

- **Timing or performance assertions in tests.** Tests that assert on timing, responsiveness, latency, or throughput chase imaginary issues and inflate coverage with hallucinated targets.
  Performance belongs in CI gates, not unit tests.
  Users notice choppiness and ask for a fix; they do not ask for “popup loads in <=50ms”. These tests prove nothing about correctness.

- A giant file that owns unrelated concerns and forces manual synchronization.

- Repeated hard-coded counts or duplicated lists of the same concepts.

- Imperative loops, regex, local scripts, or helper layers that make a simple owned operation more obscure and less assertive.

- Swallowed errors, fallback state, fake data, no-op behavior, or logging that makes failure look like success.

- Tests or docs inflated to look substantial while proving or explaining no real owned behavior.

- **Structural complexity that should be a dependency call.** Any code region with long functions (>30 LOC), `for` loops over collections, high density of `if`/`else` branches, deep indentation (3+ levels), convoluted control flow, large classes, or files with many helper functions is a red flag.
  The reviewer’s FIRST question must be: “Is there a known library, language primitive, or installed dependency that collapses this entire block?”
  When you see complexity, stop and search for the dependency — do not review the complex code on its own terms first.
  This is the most reliable detector of dependency aversion and ground-up bias.
  See `anti-slop/references/code-patterns.md` → **Complexity as a Dependency-Detection Signal**.

Treat these as weak findings unless tied to a larger mechanism:

- formatting failures;

- one-off bad names;

- isolated raw logs;

- hard-coded paths intended for the user’s machine;

- lack of portability;

- lack of speculative edge-case handling.

## Completion Standard

A useful LLM-code review should leave the user knowing:

- which patterns make the work untrustworthy;

- the concrete code examples proving those patterns;

- which proof surfaces are false or incomplete;

- what kind of corrective work would remove the pattern;

- which underlying app/code issues remain unfixed;

- for each finding, WHY the code exists at all and whether it can be eliminated,
  not just refactored;

- what the app would look like if the agent had searched for existing solutions
  before writing code (the gap between that vision and the current code IS the slop).

If the review could have been produced by reading a linter output, a test log, or an agent summary, it is not a useful review.

A review that lists findings without explaining why the code exists is incomplete.
The user does not need to know that a switch could be a Record.
The user needs to know that the switch should never have been written because a
library call replaces the entire function.

## Findings Are Flags, Not Directives

A finding is a FLAG that invites intelligent investigation.
It asks: WHY does this code have this red flag behavior?
Not: how do I preserve this code with minimal changes.

The correct remediation frame starts from the finding’s actual question.
The WRONG frame starts from “how do I keep this code and make it look better.”

If you find yourself “fixing” a finding by swapping one implementation for another while keeping the same design-level red flag, you have not remediated the finding.
You have laundered it.
Stop.
Go back to what the finding is actually flagging.

For example: when the skill flags “regex against semantic formats,” it means the code is using regex where a semantic parser already exists and should be used instead.
The remediation is to use the semantic tool — not to replace the regex with a different post-processor while keeping the same design-level smell.
The skill already tells you what the correct fix is: use the semantic tool that owns the format.
Follow that direction.
Do not invent alternatives that preserve the red flag while laundering the implementation.

Before doing any refactor prescribed by a finding, check the EXISTING tests for LLM idiocy.
Tests that assert on strings, formatting, whitespace, or byte-level output are a HUGE sign of slop — the skill flags this as “superficial state assertions.”
Fix the test slop FIRST: replace bad tests with proper tests that follow the test-guidelines skill.
Verify they are green.

Then add regression tests that capture the current behavior BEFORE the refactor.
Verify they are green.

Then add a SLIGHTLY incorrect implementation (e.g., targeted replacement with a no-op).
Verify the tests are red — for the RIGHT reason: not trivial crashes or early-exits, but BECAUSE the correct logic does not exist yet.

THEN do the refactoring.

THEN assert tests are still green.

This is TDD: red → green → refactor.
Do not skip steps.
Do not revert a correct change because a brittle test failed.
Do not change test expectations to match a new implementation.
The test must prove the implementation is correct, not the other way around.
