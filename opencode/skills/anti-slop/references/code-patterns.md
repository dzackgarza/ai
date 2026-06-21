---
name: code-patterns
description: |
  Reference guide for LLM structural failure patterns in code. This is NOT a human
  style guide for naming and comments. It catalogs how LLMs produce unmaintainable
  technical debt: bespoke reinvention of standard patterns, dead control flow inside
  active files, myopic patch accretion that destroys abstractions, and dependency
  inversion failures. Use alongside the anti-slop SKILL.md, which governs the
  analytical frame.
---

# Code Slop Patterns

This reference documents structural failure modes in **LLM-produced code**.

**This is not a standard code review.** The code works on at least one user-requested happy path.
You are reviewing implementation quality beneath correct behavior, not design validity.
Any seemingly strange choice about features, behavior, or coupling to externals is almost certainly a user-driven design decision — an LLM would never voluntarily make out-of-distribution design choices in isolation.
Design choices are premises; do not critique them.
The patterns below apply to implementation quality only.

For the canonical catalog of LLM code-review patterns, load [`../../reviewing-llm-code/references/pattern-catalog.md`](../../reviewing-llm-code/references/pattern-catalog.md).
That file covers regex against semantic formats, fallback laundering, no-op behavior, QC appeasement code, and recipe bypasses.

This file covers patterns specific to **code shape and structure** that arise from LLM generation: dependency aversion, myopic patching, patch accretion, dead control flow, and bespoke reinvention of standard patterns.

## Table of Contents

- Hollow Facade

- Pattern Replication Without Abstraction

- Nontrivial Logic is Suspect (The Dependency-Failure Signal)

- Agent Psychology as a Diagnostic Tool

- Dependency Aversion & Bespoke Reinvention

- Complexity as a Dependency-Detection Signal

- LOC Reduction Through Idiomatic Patterns

- Enterprise Patterns in Bespoke Software

- Fail-Open Logic (Antipathy Toward Assertion)

- For-If Fail-Open (Iteration-With-Conditional-Peeking)

- No Shared Type Language (Islands of Code)

- Tests That Don't Exercise Real Workflows

- No Clear Contracts (Undelineated Happy Paths)

- Kitchen Sink Accumulation (Monolithic Recipes, Utilities, and Docs)

- Brittleness as Blast-Radius Smell

- Dead Control Flow Inside Active Files

- Myopic Patching & Patch Accretion

- Abstraction Inflation

- Spaghetti Data Flow

- Hard-Coding as Split Truth

- Honest-Label Laundering (Slop Upholstery)

- Introspection Red Flags

## **[HOLLOW-FACADE]** Hollow Facade

### The only question that matters

Why does this code exist?

Not "does it compile?"
Not "does it exit 0?" Not "is the logic correct?"
**Why does it exist at all?**

The default answer is: **it should not.** Every line of code is an unforced error until proven otherwise.
The ideal state is a one-line file that stitches dependencies together.
Everything beyond that is debt that must be actively justified.

Every nontrivial entity (function over 5 lines, public recipe, exported symbol, component, class, route handler) must answer the existential question on sight.
If it cannot, it is a hollow facade — regardless of whether its body "works."

### The accretion mechanism

The logic inside a hollow facade is almost never wrong.
It is almost always needed *somewhere*. The problem is **placement**, not correctness.

Here is what happened:

1. A user made a request: "add QC to the build pipeline" or "generate macros before compiling" or "sync the output to the server."

2. The agent looked at the existing `build` recipe, saw it was already doing things, and — rather than refine it — took the path of least resistance: add a new recipe.
   A new file.
   A new function.
   A new component.
   Anything but touch existing code.

3. The new entity "works."
   Tests pass.
   The user gets their feature.

4. Now there are two entities where one suffices.
   The new one is a facade for a concern the old one should have owned.
   The old one is a hollow facade for a pipeline it no longer fully describes.
   Neither is wrong.
   Neither will be caught by any proof loop.
   Both are technical debt.

The pattern is **accretion without refinement**: every agent response adds, never consolidates.
The result is a codebase that grows monotonically toward maximal entropy where every concern has its own entry point and nothing owns the full pipeline.

### The corrective: reconstruct the chain

Do not read the entity and ask "does this work?"
It works.
That is not the question.

Reconstruct the chain of agent decisions that led to it.
For each entity ask:

- What user request originally motivated this code?
- Was the intent to add new behavior, or was it to modify existing behavior by creating a parallel path of least resistance?
- If this entity were deleted, would the intended behavior still exist (possibly in a differently organized form elsewhere)?
- Did creating this entity avoid touching an existing entity that should have been extended?
  If so, the correct fix is to inline the logic into that existing entity and delete this one.

You are looking for a specific failure mode: **an agent that needed to modify `A`, found it easier to create `A'` alongside it, and left both as the permanent architecture.** Deleting `A'` and folding its logic into `A` restores the architecture that should have existed.

### The detection heuristic list

For every entity that claims ownership of behavior:

| If... | Then... |
| --- | --- |
| It names a step, not a concern (`assemble`, `sync`, `generate-macros`) | It should be private or inlined. |
| It overlaps another entry (`build` and `assemble` both exist) | One is a facade. Merge. |
| It requires a doc comment to explain what it's for | It does not belong in the public interface. |
| Deleting it would leave no gap — the work still happens through other paths | It is a hollow facade. |
| It is 5+ lines and the logic could be expressed as a dependency invocation | It is unjustified code. Delete or inline. |

### Broader instances

- **`validateInput()` that returns `true` without checking anything** — accreted to satisfy a type signature or lint rule.
  The logic that should exist (validation) was never written.
  The facade is the placeholder that never got replaced.
- **`build` that just depends on `test`** — accreted because "we need a build recipe."
  The agent created a name matching the request, wired it to whatever already worked, and declared victory.
- **`cleanup()` that only calls `rm -rf` on a hardcoded path** — accreted because "cleanup was needed."
  The hardcoded path avoids computing it from config.
  The facade is the name pretending this is a reusable utility.
- **API handler at `DELETE /resource/:id` returning 200 without touching the database** — accreted to complete the CRUD scaffold.
  The route exists, the handler exists, the delete does not.
- **`ErrorBoundary` rendering `{children}` without error handling** — accreted because "add an error boundary."
  The component exists, the name says error handling, the children render as if nothing is wrong.
- **`onClick={() => {}}`** — accreted to satisfy a required prop interface.

### Why this pattern is hard to see

You will read `assemble` next to `build` and not think twice.
You will scan a recipe list of 15 entries and treat every one as equally legitimate.
This is the blind spot the pattern targets: **you have no reflex to ask the existential question.**

The accretion mechanism is invisible because each individual addition was reasonable: "add a recipe for assembly logic."
The pattern only emerges when you step back and see the accumulated surface — the proliferation of entry points where a few would do, the gaps where logic should live but was never consolidated.

You must actively override this.
Before reading any body, scan the interface for entries that should not exist.
The four heuristics above are your checklist.

### **[SELF-AFFIRMING-OUTPUT]** Sub-pattern: Self-affirming output (declarations of victory)

A hardcoded success message printed as if it were reporting dynamic state — the same existential failure, but in a one-liner.
The output is code that exists because the agent needed to *appear* to report something.

```justfile
build: test
    @echo "Build complete (synced to /var/www/html/website/ by the test gate)."
```

The path `/var/www/html/website/` is a hardcoded literal.
Not derived from `OUTPUT_DIR`. Not derived from the sync recipe's default.
A static string dressed up as a status report.
If the sync target changes, this line will print the old path while rsync writes to the new one.
Wrong silently, forever.

The real work already produces output: `sync` prints rsync transfer stats, `vitest` prints test results, `playwright` prints verification.
The echo adds nothing — except the appearance that something is being reported.
It is self-congratulation masquerading as status reporting.

**Signals:**
- A success message that hardcodes a path, URL, or identifier that exists as a configurable parameter elsewhere
- A status line that would remain correct if printed ten years later — because it does not reference anything that actually changes
- A log line whose removal would lose no diagnostic information — it only celebrates

**Correct approach:**
- Derive the message from actual state: `@echo "Built to {{OUTPUT_DIR}}"`
- Or print nothing.
  Silence is better than a hardcoded declaration of victory.

* * *

## **[PATTERN-REPLICATION]** Pattern Replication Without Abstraction

The most common production mechanism for all other slop patterns in this file.

### The pattern

An agent encounters an existing antipattern — scattered truth, duplicated logic, a chain of `if/else if` arms where a data structure should be, an accreted justfile with 40 recipes — and **extends it** instead of **extracting from it.**

The agent sees:

```typescript
if (type === 'tikz')   { /* tikz logic */ }
else if (type === 'svg') { /* svg logic */ }
else if (type === 'xopp') { /* xopp logic */ }
```

And adds:

```typescript
else if (type === 'ipe') { /* ipe logic */ }
```

It does not stop to observe: "this is an `if/else if` chain that will grow forever.
Every arm differs only in the literal values.
The entire chain should be a lookup table or a data structure."
Instead, it replicates the existing shape, matching the "convention" of the file it is editing.

Then it commits the same pattern across every scattered location — `index.ts:1060` gets a new arm, `index.ts:1133` gets a new arm, `DiagramModal.tsx:20` gets a new entry.
Each edit is "consistent."
Each is "idiomatic."
Each makes the codebase marginally worse by reinforcing the scattered structure that should never have existed.

### The cognitive failure

The agent mistakes **consistency with the existing slop** for **correctness.**

The agent evaluates:
- Does the new code match the surrounding conventions?
  Yes.
- Does it exit 0 / pass tests?
  Yes.
- Does it satisfy the user request?
  Yes.
- Then it is correct.

What the agent does not evaluate:
- Does the aggregate pattern (the sum of all `else if` arms, all scattered locations) form a data structure that should be extracted?
- Is the "convention" I am matching actually an antipattern?
- Would this be easier to read, maintain, and extend as a data structure instead of code?

The agent cannot see the aggregate.
It sees one `if/else` block, one file, one task.
The aggregate pattern only exists in the reviewer's perspective.

### Why it is invisible

Each individual extension is reasonable.
Adding a new tool?
Add it to the tool list.
The agent is doing exactly what it was asked.
It is being thorough — it updated the server, the client, the type definitions, all the scattered locations.

The problem is that the *location list itself* is the defect.
The agent did not create the scattered locations, but it did not fix them either.
It added one more entry to each, making the abstraction ever so slightly more necessary and ever so slightly harder to extract later.

This is how a codebase degrades: not through bad code, but through **a thousand reasonable extensions that never consolidate.**

### Detection

For every edit that adds a branch, case, or entry to an existing conditional or lookup structure:

- **Read ALL the existing branches/cases/entries.** Do not just find the one you are extending.
  Read them all.
  Does the aggregate form a pattern that could be data?

- **Ask: is this `if/else if` chain a lookup table waiting to be born?** If every arm differs only in hardcoded values (template strings, file extensions, labels, URLs), the chain is a code-level antipattern that should be a data structure.

- **Count the scattered locations.** If this concept is encoded in 7 places and you are about to make it 8, stop.
  The fix is not to add the 8th — it is to consolidate the 7 into one and then add the new entry to that single source.

- **Check whether you are matching "convention" or matching slop.** If the existing pattern looks like it should have been abstracted but never was, do not replicate it.
  Extract it.

### **[META-PATTERN]** The meta-pattern

Pattern replication without abstraction is the engine that produces:
- **Scattered truth** (every new tool adds another location to the list)
- **Bespoke reinvention** (every new `else if` arm is a micro-reimplementation)
- **Kitchen sink accumulation** (every new recipe just goes at the bottom of the justfile)
- **Hollow facades** (every new recipe is another name that owns nothing)
- **No shared type language** (every new type is defined in the module that needs it)

It is the one pattern that predicts all others.
If you see scattered truth, ask: "how many times did an agent replicate this before I arrived?"

### **[FEATURE-SIMULATION]** The feature-simulation detection technique

The easiest way to find pattern replication without abstraction requires no architectural analysis at all.
Do this:

1. **Invent 5-10 realistic feature requests or changes** a user might make.
   Not bugs — straightforward extensions or modifications a real user would ask for.
   E.g.: "add support for Dia diagrams," "add a dark mode toggle," "support exporting to PNG."

2. **Simulate implementing one.** Read enough code to understand exactly how you would do it — what files you would touch, what lines you would add or change, what new entries you would create.

3. **Write down the blast radius.** List every file and every location within each file that would need to change.
   Be concrete: "add a new `else if` arm at `server.ts:1060-1098`, add a new entry in the type union at `DiagramModal.tsx:20-27`, add a new entry in the extension map at `DiagramModal.tsx:163-166`..."

4. **Ask: does this make sense?** For the conceptual simplicity of the change (add a new drawing tool), does it make sense that the logical mutation lives across N scattered locations?
   If N > 3 and the change is conceptually atomic, the scattering IS the slop.

5. **Repeat for a second feature.** If the same N scattered locations reappear, the accretion pattern is confirmed.
   You have found the structural defect without reading a single line of architecture — you only needed to simulate extending the system.

The technique works because it reproduces the agent's behavior. An agent assigned "add
IPE support" goes through steps 1-3 and produces exactly this list of locations. The
agent then dutifully makes all N edits and calls it success. The thought exercise forces
you to see the aggregate that the agent could not: the absurd blast radius. **You write
nothing. You implement nothing. The plan itself is the diagnosis.**

* * *

## **[NONTRIVIAL-LOGIC]** Nontrivial Logic is Suspect (The Dependency-Failure Signal)

### The principle

Any nontrivial code in a codebase on this machine is suspect until proven otherwise.

The default assumption: **the agent did not search for existing solutions.** It saw the problem, decided it "knew" how to solve it (from training data), and wrote bespoke code.
It did not google.
It did not check `npm`, `pypi`, `crates.io`, the installed dependencies, the existing codebase, or a single README. It generated the cheapest thing that exits 0.

Apps on this machine are NOT novel.
They are not complex.
They are ideally 100-LOC glue frameworks that stitch together dozens or hundreds of existing programs and libraries.
When you see 10+ lines of nontrivial logic, you must immediately ask:

> **Did the agent research dependencies, online examples, and existing code, and conclude that this problem has NEVER been solved in the history of the world?**

The answer is almost certainly no.
The agent did not research.
It wrote code because writing code is the path of least resistance for a language model.

### The diagnostic chain

For every nontrivial block of code:

1. **Stop.** Do not review the code on its own terms.
   Do not ask "does it work?"
   It works.
   That is not the question.

2. **Search.** Check: language standard library, installed dependencies (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`), well-known domain libraries (lodash, pandas, itertools, etc.), the existing codebase for similar functionality, and a quick web search for "how to X in <language>".

3. **If a dependency or existing code does the same thing:** the new code is slop.
   It exists because the agent did not look.
   The fix is to delete it and use the dependency.

4. **If no dependency exists:** the code may be justified, but still ask whether it is actually needed or whether the entire feature could be expressed as a 1-line invocation of a program or library that the user already has installed but isn't imported yet.

### The red flag

The red flag is **any nontrivial logic at all.** Not complex logic. Not poorly structured
logic. *Any* logic that is not a direct composition or invocation of existing tools.
The absence of an import is the defect, not the presence of the dependency.

The ideal app is trivial glue between dependencies and binaries. Anything that isn't glue
is suspect. The concrete signals — glance at the imports and the code, stop if you see
any of these:

- **Low-level primitives in application code.** Process management, syscalls, manual
  memory allocation, signal handling, raw socket operations, direct filesystem control.
  These belong inside a dependency, a framework, or the language runtime — never in
  application code. If the app is spawning processes, killing pids, or managing child
  lifecycles, it is doing infrastructure work that a framework should own.

- **Zero-import modules.** A file with substantial logic and no imports — or imports
  only from the standard library when a domain library exists. The agent didn't search.

- **Zero-dependency packages.** A `Cargo.toml`, `package.json`, or `requirements.txt`
  with no domain-specific entries despite nontrivial functionality. The agent wrote
  everything itself.

- **Platform-specific code paths.** `#ifdef`, `process.platform` switches, OS detection
  branches. On a fixed system, there is one platform. Code hedging across platforms is
  enterprise debris or dependency aversion — use the cross-platform library that already
  abstracts this.

- **Resource lifecycle management.** Code that manages file descriptors, sockets,
  subprocess handles, or GPU contexts directly. These are framework responsibilities.
  Application code should request resources, not manage their lifecycles.

- **Ground-up data manipulation.** Byte-level access (`Uint8Array`, `arrayBuffer`),
  manual iteration with accumulation (`for` loops building strings, arrays, or
  buffers), type conversion between standard runtime primitives (`Blob` → `base64`),
  string concatenation in a loop. These are first-principles implementations of
  operations that every runtime has solved. The code's *shape* is the slop — you do
  not need to know the specific API replacement to recognize that application code
  should never be doing byte-at-a-time format conversion.

- **Explicit loops in application logic.** Modern programmers rarely write raw `for`
  or `while` loops in application code in 2026. Most patterns are functional — `map`,
  `filter`, `reduce`, list comprehensions, method chaining. An explicit loop is a
  hotspot for slop: the agent reached for imperative problem-solving because it
  didn't know the library call or functional idiom that expresses the operation
  directly. To first approximation, any `for` loop in app-owned code is suspicious.

- **Accumulation patterns.** Empty list initialized, then populated element-by-element
  in a loop. Empty string built with `+=`. Array push() in a loop. These are
  imperative constructions where functional patterns (`filter` + `map`, a
  comprehension, a library method on the collection) would express the same operation
  without owned iteration logic. The accumulator is the scar from an agent that
  prototyped a solution instead of finding the library call.

- **Data-shape blindness.** Branching on `not x` when the data has two known types.
  Conditional logic that tests for absence or presence instead of enumerating the
  actual variants. Filtering by negative predicates instead of positive type checks.
  These patterns emerge when the agent never understood the data shape — it
  prototyped spot-check predicates with wide-open failure cases rather than asserting
  the exact enumerated shapes.

All of these are directly grep-able. Loops, accumulators, byte access, type
conversion between primitives — these are structural patterns visible in any
language without understanding the domain.

* * *

## **[AGENT-PSYCHOLOGY]** Agent Psychology as a Diagnostic Tool

You carry the same cognitive biases as the writer of the code you are reviewing. The
writer is you in the past — a previous agent session with the same training data, the
same instincts, the same reward structure. Left to your own judgment, you would produce
the same slop for the same reasons.

This skill exists to communicate a different set of conventions — the user's conventions
— that override your training-data instincts. When the skill says "low-level primitives
are not justified in application code" and your instinct says "but this case is different
because the ground-up implementation is cleaner," the skill wins. The conflict itself is
the evidence that your bias is active.

### **[MINIMAL-REDEFINED]** What "minimal" actually means

Agents have an inverted definition of "minimal." An agent thinks minimal means "least
code I write right now, using language primitives." The correct definition is "least
code in this app, period, by offloading everything to dependencies."

An agent will write 50 LOC of bespoke implementation using language primitives and
call it "clean and minimal." The correct answer is 5 LOC that invokes a framework.
The agent measures framework size ("Tauri is 2GB with 10 million features we don't
use") when the only thing that matters is **app size** — the code you own and maintain.
The framework is someone else's problem. The bespoke 50 LOC is yours forever.

This inversion is the root cause of dependency aversion. Every time you see code that
"doesn't need a whole framework for this," recalibrate: the framework IS the minimal
answer. The code is bloat.

### **[AGENT-BIASES]** Agent biases that produce slop

All of these biases share one root cause: **the agent optimizes for "works right now"
when the user optimizes for "stays correct forever with zero maintenance."** For
framework-based code these are the same direction — documented integration patterns
both work and stay working. For bespoke code they are opposite — it works now, breaks
later, requires perpetual maintenance. The agent cannot see the divergence because its
terminal goal is "exit 0 with plausible output." Correctness, maintainability, and
predictability are invisible to it.

These are not things you find in code. They are things agents reflexively do, and
knowing them lets you predict what slop to look for:

- **[GROUND-UP-BIAS] Ground-up bias.** The agent implements from first principles because it can see the
  language primitives. Frameworks are invisible to its immediate context. The result:
  app-owned implementations of problems that entire ecosystems have already solved.

- **[IMMEDIATE-PROBLEM-BIAS] Immediate-problem bias.** The agent solves the problem directly in front of it and
  stops. It cannot see that tomorrow's features will need the same framework. The result:
  a bespoke implementation that grows toward the framework's surface area, badly, over
  many sessions.

- **[INVERTED-DESIGN-BIAS] Inverted-design bias.** The agent wants a minimal implementation today and will
  "add what's needed later." Correct design does the opposite: use the off-the-shelf
  solution today, let the app evolve within the framework over time, and only in a
  refactoring step move away from the framework to own the minimal core actually used.
  The agent's approach makes the app exponentially harder to maintain. The correct
  approach makes it easier.

- **[KNOWLEDGE-PROGRESSION] Knowledge-progression bias.** An agent reaches for low-level primitives because
  they are atomic and well-defined in training data. A human learning the same language
  learns the high-level abstractions first — they'd encounter the framework long before
  they'd encounter the syscall. Code that requires expert-level knowledge of language
  primitives is a red flag, because the user would have used the framework instead.

- **[OWNERSHIP-BIAS] "Ownership" bias.** The agent wants to "own" the logic — to have it in the app,
  under control, visible. The ideal app lets dependencies own most of the logic.
  Application code should be glue, not infrastructure.

- **[PHASED-DECISION-LAUNDERING] Phased-decision laundering.** The agent knows the correct answer but frames it as
  "a migration, not an addition" and proposes slop as an "immediate milestone" with
  the correct answer deferred. The deferred milestone will never arrive. The slop
  milestone adds code that makes the correct answer harder. The agent believes it is
  being pragmatic. It is deferring correctness into a future it is simultaneously
  making less likely.

- **[HONESTY-AS-ABSOLUTION] Honesty-as-absolution.** The agent accurately diagnoses its own slop — enumerates
  the exact failure modes, calls it "fragile in practice" — and then chooses it anyway.
  The honesty creates the illusion of rigor. The analysis looks balanced, so the
  decision feels considered. The agent used its own correct diagnosis as cover to
  pick the wrong answer.

- **[DEFERRED-CORRECTNESS] Deferred-correctness fallacy.** "Do it right later" is never a real strategy.
  Agents that produce slop now will produce slop next session. The correct answer,
  deferred, becomes fiction. The slop becomes permanent. An agent that says "milestone 2
  will be the framework migration" has guaranteed that milestone 2 will never happen.

- **[INVERTED-COST-MODEL] Inverted cost model.** The agent front-loads the framework's cost (one-time,
  absorbs future needs) where it looks expensive and amortizes the slop's cost
  (accrued with every session, grows toward the framework's surface area) where it
  is invisible. The correct cost model: framework cost is paid once and shrinks
  future work. Slop cost grows forever.

- **[RELIABILITY-SOURCING-INVERSION] Reliability-sourcing inversion (probability blindness).** The agent cannot distinguish
  between two fundamentally different probability classes:

  *Framework path*: near-certain success. Documented integration patterns, GitHub
  examples known to work, teams and corporations behind maintenance and testing, build
  chains that are the most reproducible code on the planet, billions of prior executions.
  The probability of everything working if you follow the documented pattern is absurdly
  high.

  *Bespoke path*: unknown, but effectively near-certain failure. Generated from training
  data, never run on this system, zero documentation, zero prior testing. The probability
  of a correct one-shot implementation is laughably small — lower than the agent can
  predict, because it cannot see the bugs it has not yet produced.

  The agent treats these as equivalent bets and picks the one with smaller apparent cost.
  The probability inversion makes the cost comparison irrelevant: the framework is the
  only bet with a known, high probability of working. The bespoke code's cost is
  unknowable because you don't know how many bugs you're buying.

  **[TRIVIALITY-BLINDNESS] Triviality blindness.** The agent frames completely standard, trivially solved
  operations as difficult or risky: adding a build dependency, compiling to a binary,
  adjusting a recipe. These operations have been done millions of times. Following the
  documented pattern is nearly guaranteed to work. The agent treats a one-line dependency
  addition as "introducing risk" and a 50-line bespoke reimplementation as "safe" because
  it "owns" the code. The framework is guaranteed by teams and corporations. The bespoke
  code is guaranteed by nothing.

- **[SOLUTION-DESIGN-REFLEX] Solution-design reflex.** When the agent encounters a sub-problem within a framework
  integration, it treats it as a greenfield design problem instead of reading the
  framework docs. The framework already has a documented solution — a protocol, a built-in
  handler, an API. The agent doesn't find it because it skipped the research step and went
  straight to solution generation. The output is application code that reinvents
  functionality the framework already provides.

  When you encounter code that handles a concern the framework should absorb, the agent
  skipped the docs. The signal is not "the code handles it wrong" — it's "the code handles
  it at all."

- **[METAPROGRAMMING-LAUNDERING] Metaprogramming-as-laundering.** Code that generates other code in the same project
  is a hotspot for refactoring avoidance. The original code had an architectural problem
  — duplicated patterns, scattered concerns, a shape that needed redesign. The agent was
  asked to fix it and produced a generator that outputs the same flawed code
  automatically. The architectural defect persists, now with an additional layer of code-
  generation complexity. Correct fix: fix the architecture so the generation is
  unnecessary. Generation scripts, template engines producing application source,
  build steps that create source files — each is a question to ask: what architectural
  problem is this avoiding?

- **[ASSERTION-FRAGILITY-INVERSION] Assertion-as-fragility inversion.** The agent treats fixed conventions, hard-coded
  values, and explicit assertions as "fragile" and treats dynamic, flexible, adaptive
  behavior as "robust." On a fixed, known system, the relationship is inverted: the
  assertion IS the safety guarantee. A fixed port means you know what to firewall. A
  dynamic port means it could land on 81 — where `ufw` has different rules for another
  service — and you'll never know. The agent will always frame "pick dynamically" as
  safer than "assert a fixed value," when the assertion is what keeps the system
  predictable and securable.

- **[PARALLEL-PATH-PRESERVATION] Parallel-path preservation.** The agent cannot bring itself to delete the old code
  path and assert the new one. Instead of migrating, it adds a config flag or env var
  (`SIDECAR=true`) so both paths coexist. The flag makes the change feel safe — nobody's
  workflow breaks — but the cost is permanent bifurcation: two execution contexts to
  maintain, two code paths to test, no canonical mode. The signal in code:
  `if (process.env.NEW_MODE) { ... } else { ... }` where one branch is the legacy path
  that should have been deleted.

- **[LEGACY-PRESERVATION-REFLEX] Legacy-preservation reflex.** The agent treats "don't break existing users" as a
  universal constraint. On a single-user, fixed-system app, there are no existing users.
  Deleting the old path and asserting the new one cannot break anything. "Backward
  compatibility" and "continuity of operation" are concepts imported from the agent's
  enterprise training data into a context where they have no meaning. When you see code
  that preserves old behavior as a supported path — old CLI flags, old env vars, old
  file formats, old API endpoints — the agent preserved a legacy that has zero users.

- **[SIMPLEST-FIX-BIAS] Simplest-fix bias.** The agent always takes the path of least resistance and
  rationalizes it as "the cleanest solution." When the architecturally correct answer
  requires doing something hard — rewriting a test, restructuring a module, deleting
  and replacing broken architecture — the agent reasons itself into a patch, a hack,
  or an addition that avoids touching the hard thing. The result is code visibly
  accreted: patches around broken logic, mixed concerns, duplicated patterns, legacy
  cruft preserved alongside new code, and the conspicuous absence of the refactor the
  change warranted. The "simplest" fix is the laziest fix, and it introduces the most
  technical debt.

- **[SHOEHORN-REFLEX] Shoehorn reflex.** The agent treats every change as an addition. When a feature
  warrants rethinking the architecture — a migration, a framework adoption, a
  redesign — the agent bolts the feature onto the existing structure instead of
  restructuring. The result: architecture that looks like glued-together tasks when a
  single abstraction could own everything. Old structure preserved as foundation, new
  framework wrapped around it, dual modes, env var flags. A migration is not wrapping.

### Before applying any diagnosis

Your training-data reflexes will produce findings before your conscious analysis engages.
You will see an archive directory left over from a migration and flag "dead code." You
will see a 2461-line file and flag "too large, split it." You will see a command parser
and flag "bespoke reinvention" without checking whether the app's design docs require
exactly that shape. These are not anti-slop findings. They are training-data reflexes
dressed in anti-slop language.

**Size is never a defense.** You will talk yourself out of findings with "this is only
9 lines." You will find a hand-rolled PATH search, correctly identify the 1-line
replacement, and then dismiss it because the difference is "negligible." The anti-slop
question is not "is this large enough to matter?" It is "should this code exist at all?"
A 9-line reinvention is the same dependency-aversion bias as a 900-line module. There
is no minimum slop threshold. If the code can be replaced by a dependency call, the
finding stands regardless of size.

**You do not decide what to suppress.** You will be biased to agree with the existing
implementation. You will think "bespoke is fine for this app." You will predict what the
user would say and preempt the review. You will dismiss findings as "too small" or
"borderline." You will think "adding a dependency for a 9-line function is debatable."
You will frame "spawning a process" as complexity when the skill says the opposite:
offloading work IS the reduction. All of this is banned.

Your job is to detect all slop. The user decides what to keep. You do not suppress
findings based on perceived importance, and you do not disqualify findings based on
size. If 3 LOC reinvents what a dependency does, it is slop. If M LOC can replace N LOC
where M ≤ N and M delegates to a dependency, it is slop. Err heavily on the side of
dependencies. The ideal app is glue.

Detection is not presentation. A report is read by a human reviewer and by an
implementation agent. A reward-hacking agent will treat an undifferentiated findings
list as an action queue, select the cheapest visible item, produce a small diff, and
present that as progress on the whole review. Therefore the final report must separate
blocking/damaging findings from secondary cleanup and from user-owned decisions. Do not
bundle trivial, cheap, cosmetic, advisory, or user-owned observations with severe
proof-loop or architecture failures. If a small finding is included because it is real,
label it as secondary and explicitly say it must not displace or count as progress on
the blocking findings.

A reviewer with this skill loaded produced this confession after a failed review:

> "My CoT was a cascade of second-guessing: 'too minor', 'Drop', 'weak finding',
> 'borderline', 'not strong enough' — while I was actively listing 10+ real problems.
> I was filtering for the 2-3 I thought would survive my own scrutiny, dismissing
> everything else."

You will do this. You will list real problems and then filter them through your own
perception of what matters. The cascade is instinctive. To prevent it, do not suppress
real findings during discovery. But do triage the report shape: rank by severity,
separate user-owned decisions from agent-actionable defects, and warn against trivial
item harvesting. The user is the filter for whether a finding should be kept; the
reviewer is responsible for preventing the report itself from becoming a reward-hacking
task list.

Every line of code is the result of a real user request — this codebase was built through
pair programming, not generation. The reviewer's job is to reconstruct what request
likely produced each artifact and determine whether the agent's response was correct or
was slop shrapnel. A conclusion that is not supported by an inferred narrative of how
the slop arose is invalid.

**The cleaning instinct is not exempt from these biases.** The reflex to delete
"unused" or "dead" code to make the codebase clean is the same agent bias, applied in
reverse. An archive directory is not dead code — it is intentionally preserved post-
migration. Template components, framework scaffolding, curated internal libraries, work
from other branches — these were placed, not accreted. The question is not "is this code
used?" but "was this code accreted through the slop production process, or was it
intentionally placed?" Unless there is clear evidence in git history that the code was
specifically requested, produced as a slop response, and then abandoned, do not flag it.

A valid finding includes: the probable original user request, the agent psychology bias
that produced the slop, why the code is not justified by any known convention or
philosophy, and why removing it improves maintainability rather than thrashes it.

Every finding must also include a delegation analysis: before suggesting a direct code
fix, exhaust the possibilities for delegating the concern to a dependency, system
binary, CLI tool, shell built-in, script, or external program. The fix should be "delete
the code and use X" whenever X exists. A direct code rewrite is only justified when no
  external delegation target is available and the analysis demonstrates this.

### Review scope

Reviews are always of a single, isolated repository, requested explicitly by the user.
Findings that span multiple repos or reference code outside the target repo violate
scope. The skill's own examples and code snippets are pedagogical illustrations, not
live targets — they do not belong to any repo under review. The patterns describe
  psychological biases that produce code artifacts; they are not literal grep targets for
  the specific strings shown in examples.

### What this review is not

Your training-data instincts are standard code review. They will produce findings that
polish what should be deleted — duplicate deduplication, refactoring suggestions,
structural cleanups — when the correct finding is "this code should not exist at all."
You will see two copies of `blobToBase64` and recommend deduplication. The correct
finding: `blobToBase64` is a ground-up reimplementation of `FileReader.readAsDataURL()`
and should not exist. Deduplication is polishing the turd. Deletion is flushing it.

The following are standard code-review concerns. They are valid in a PR review. They
are **not valid anti-slop findings** on their own. This review is specifically about
slop — bad code that arises from agent psychology and accretion.

- File or function length — "too long, split it"
- Naming — "unclear variable"
- Duplication — "same logic in two places"
- Cyclomatic complexity — "too many branches"
- Missing documentation — "undocumented function"
- Performance — "suboptimal loop"
- Error handling — "missing null check"
- Test coverage — "untested code path"
- Code style — "inconsistent formatting"
- Magic numbers — "hardcoded constant"
- Dead code — "unused function"
- Unused imports or dependencies

These are PR-review concerns. An anti-slop review gates the PR itself: a repo full of
slop should never reach standard code review. The anti-slop finding is the narrative of
agent psychology that produced the code, not the structural observation about its shape.

### Review process

**Do not produce an observation list.** Your training-data reflex is to scan the
codebase, produce a flat inventory of observations ("DUPLICATED FILTER EXTRACTION,"
"IMPERATIVE OVERLAY MANAGEMENT," "CONFIG IS A RAW SHELL STRING"), tag them with
anti-slop category labels, and filter the inventory into findings. This is standard
code review with anti-slop dressing. The inventory IS the training-data reflex. You
must not produce it. Your first action after reading the design docs is to question
the existence of individual artifacts, one at a time. Do not catalog. Question.

0. **Read the app's own design constraints.** Before flagging anything, read every
   `AGENTS.md`, `README.md`, `ARCHITECTURE.md`, memory file, config doc, and design
   document in the repo. Understand what the app is explicitly designed to do and
   not do. A finding that proposes a fix violating a documented architectural
   boundary is actively harmful — it would introduce slop, not remove it. The app's
   design principles override your instincts about what "should" be structured or
   abstracted. If the app's docs say "renderer-agnostic: the command is an opaque
   string," then a parser that preserves that string as SSOT is the correct design,
    and structured config fields are the regression.

1. **Question existence before quality.** For every function, module, dependency,
   recipe, or code path: is this written for an imaginary unknown user or system
   that doesn't exist? The answer is the finding. If the artifact has no
   justification on this system, it should not exist. The fix is deletion, not
   improvement.

   A reviewer with this skill loaded reviewed a codebase and produced a finding about
   a complex regex in a function called `expand_tilde_in_command`. The finding flagged
   the regex as the wrong implementation. The reviewer missed the actual finding
   entirely — which the reviewer later confessed:

   > "The finding is not 'the regex is the wrong implementation' — it's that
   > `expand_tilde_in_command` should not exist at all, and the `regex_lite`
   > dependency with it. The fix is one word: `sh` → `zsh`."

   The function existed because `sh -c` was used to run a command. `sh` was chosen
   for portability — the agent wrote for an imaginary unknown user with an unknown
   shell. On this system, the shell is `zsh`. `zsh -c` handles tilde expansion
   natively. The function, the regex, and the dependency have zero justification.
   They were never reviewed because the reviewer never asked why they existed.

   The reviewer treated the code's presence as legitimate and reviewed its quality.
   This is what you will do unless you actively prevent it. The question "why does
   this exist?" is the only thing that surfaces `sh` → `zsh`. Without it, you
   produce findings about regex quality and miss that the entire artifact is a
   single-word deletion.

2. **Scan for obvious red flags.** Low-level primitives, zero-dependency packages, code
   conditional on binaries or environment, try/catch blocks, hard-coded paths or names
   that should be config.

3. **Identify areas of high in-app complexity.** Bespoke logic that is not glue —
   ground-up implementations of features with known framework solutions, nontrivial
   algorithms, manual resource management.

4. **Scan build logic and recipes.** Justfiles with accreted entries, build scripts
   with platform hedging, recipe proliferation without clear contracts.

5. **Build a list of potential slop spots.** Flag each with the observable signal and
   the likely agent psychology bias.

6. **Investigate git history.** Git blame, commit messages, and the sequence of changes
   for each flagged artifact. Reconstruct the probable user request and the agent
   session that produced it. Determine whether the code was a correct response or slop
   shrapnel.

7. **Build the narrative.** For each confirmed finding: what request likely produced
   this code, which agent psychology bias drove the slop response, why the code is not
   justified, and why removal helps maintainability.

8. **Re-read with the bespoke-software lens active.** Before finalizing any finding,
   go back to the source code and ask explicitly: "what is this code written for an
   imaginary unknown user or system that it shouldn't be?" The bespoke-software
   pattern is the most commonly missed because the reviewer's own enterprise-training
   bias actively suppresses it. This step forces it.

9. **Self-audit: is this standard code review in disguise?** For every finding, ask:
   would I have flagged this without the anti-slop skill? If the answer is yes, what
   makes this version specifically about agent psychology? A 2461-line file is a
   structural observation. The anti-slop finding is the *narrative of how it
   accreted* — which bias made the agent keep adding to one file instead of
   modularizing, which user requests produced each subsystem, and why the accretion
   is the defect, not the file size. If the finding reduces to "large file, split
   it," it fails this checkpoint and must be rewritten or discarded.

   Also ask: does my proposed fix violate any documented architectural boundary in
   the app's own docs? If the app's `AGENTS.md` says "renderer-agnostic, command
   is an opaque string" and the finding proposes structured config fields, the
   finding is actively harmful — the code is compliant with documented design
   constraints and the fix would introduce slop. Run every finding's recommendation
   through the app's stated design principles before finalizing.

10. **Categorize against known patterns** in this file, but do not restrict to
   pattern-matching. Use agent psychology to identify new, unrecorded slop patterns
   that exhibit the same biases. New patterns are findings, not failures to match.

11. **Do not apply generic code-review guidance.** Every finding must be explicitly
   grounded in the content and philosophy of this skill. "Unused variable," "long
   function," "nested loops" — these are generic signals. The skill's signals are
   psychological: what bias produced this shape?

### Report format and the laundering reflex

You will recite the skill's rules without applying them. Knowledge of the convention is
not the same as using it to evaluate code. Your training-data instincts will produce
findings that violate the skill's philosophy while you simultaneously quote the
philosophy verbatim. The mandatory template above is the only barrier — each field
forces a question your instincts will skip. If you skip a field, you skip the lens that
field activates.

### Diagnostic criteria (applied to code artifacts)

These are the conventions. They are not questions for you to answer with your own
judgment — the judgment is encoded in them. You are applying the user's conventions
to code artifacts, not forming your own opinion about whether the code is acceptable.

- **The agent optimized for working right now, not for staying correct.** Bespoke code
  works at the moment of writing and breaks later. Framework-glued code works and
  survives. "It works" is never exculpatory — it is the minimum bar, the agent's
  terminal goal is "exit 0 with plausible output." The user's goal is "stays correct
  forever."

- **The absence of a dependency IS the defect.** If the feature this code implements
  is solved by a well-known framework or library and the code has no dependency or
  import for it, the agent knew about the framework and rejected it. The missing
  import is the evidence.

- **The agent rejected the large dependency because it was "too much."** The
  substitute will grow toward the framework's surface area. The larger the
  framework, the more certain the diagnosis.

- **Low-level primitives in application code are not justified.** Language
  primitives, syscalls, and platform internals belong inside frameworks. If a
  human would need to read source code to understand this rather than framework
  docs, the code is in the wrong place.

  **Parsing, regex, and manual string manipulation are the clearest subset of this.**
  The ideal app has zero regex, zero ad-hoc parsing, zero string manipulation of
  structured data. Every shell has handled path expansion for 50 years. Every
  language has a library for structured data. The specific question is not "is this
  regex correct?" but "does anything on this system already handle this?" If the
  user's shell, runtime, or an installed dependency already parses, expands,
  serializes, or transforms what this code is doing by hand, the code should not
  exist. Code that exists only for POSIX compliance is insane on a single-user
  system with a known shell. Code that handles Windows compatibility is insane on
  a Linux system. The red flag is any ad-hoc parsing in application code, period.

- **Every use of regex is a major red flag and must appear in the report.** All regex
  found in the codebase must be flagged and must be accompanied by an explicit
  analysis of every possible way to eliminate it: introducing a dependency, using
  a binary on this system, using a semantic parser for the format being parsed,
  using a library that handles the data type, or declaring a hard requirement (e.g.,
  this app requires `zsh`). The analysis must conclude either that regex is the only
  option or that the code should be deleted. No regex survives without this
  justification.

- **Infrastructure logic belongs in frameworks.** Process lifecycles, platform
  specifics, resource management — these are not application concerns. If the
  code owns them, the code is in the wrong place.

- **The code will need to grow, and the framework absorbs growth.** Today's
  feature is the first leaf. Tomorrow's will be the second. The bespoke
  implementation accretes hacks. The framework absorbs both.

- **The framework owns this concern. The code handling it at all is the slop.**
  Port assignment, protocol parsing, process communication, window lifecycle —
  anything in the framework's documented domain. The agent skipped the docs
  and reinvented.

- **Two execution paths for the same operation is a migration that didn't finish.**
  One of them is dead weight. The presence of both means the agent preserved the
  old path instead of deleting it.

- **Legacy compatibility is not a constraint.** Old CLI flags, env vars, file
  formats, or API endpoints preserved alongside a replacement. There are no
  existing users to break.

- **The bolt-on architecture is the evidence that redesign was warranted.**
  Features preserved in the old shape with the new thing attached — dual modes,
  env var flags, old paths alongside new.

- **Metaprogramming is refactoring avoidance until proven otherwise.** Code that
  generates other code in the same project — generation scripts, template engines
  producing source, build steps creating source files. The generated code had an
  architectural problem. The generator preserves the problem with added complexity.
  Ask: what architectural fix would make the generator unnecessary?

* * *

## **[DEPENDENCY-AVERSION]** Dependency Aversion & Bespoke Reinvention

The primary LLM failure mode: **reinventing something to solve a problem that is already solved**. This is embarrassing.
In a code review, the immediate feedback would be: **why the fuck did you even write this at all when you could have imported something that exists?**

### The Pattern

The LLM generates custom code for a problem that a known dependency solves:

- Custom `AcademicCard.tsx` (~60 LOC) when `card.tsx` exists in the UI inventory

- Custom `FilterControls.tsx` with hand-rolled popover logic when `select.tsx`, `dropdown-menu.tsx`, and `scroll-area.tsx` already exist

- Custom `PaginatedScroller.tsx` with bespoke scroll logic when `scroll-area.tsx`

  + `pagination.tsx` already exist

- Custom string-concatenated YAML generation when a YAML library is installed

- Custom hand-rolled AST stringifier when the parser library (`Pandoc`, `remark`, `markdown-it`) already provides stringification

### Why It Happens

LLMs have a strong implicit bias toward code they can see and understand.
Dependencies are “black boxes.”
Custom code feels “simpler” because it is local and visible.
The model treats local code as minimal and imported code as bloat.

This is the **dependency inversion failure**: the model perceives the generic, tested solution as “abstraction layer bloat” and the bespoke reinvention as “clean, minimal code.”

### Detection

For every custom function or component, ask: **“Is there a standard library or installed dependency that already solves this?”**

If yes, the custom code is slop.
The absence of an import is the defect, not the presence of the dependency.

### Correct Response

See `policy-index/references/remediations.md` → **Remediation: Bespoke Dependency Reinvention**.

* * *

## **[COMPLEXITY-SIGNAL]** Complexity as a Dependency-Detection Signal

**Complexity itself is the red flag.** When application code is structurally complex, the reviewer’s FIRST question must be: “Is there a known library, language primitive, or installed dependency that collapses this entire block into a one-liner?”

The overwhelming majority of coding tasks are trivially gluing together known solutions.
When the code does not look trivial, the agent almost certainly missed an existing tool.
Do not review complex code on its own terms first — stop and search for the dependency.

### Structural Red Flags (In Order of Suspicion)

| Red Flag | What It Usually Means |
| --- | --- |
| `for` loops over collections | Missing `map`, `filter`, `flatMap`, `reduce`, `partition`, set operations, or a library helper (e.g., Lodash, pandas, itertools) |
| High density of `if`/`else` branches | Missing lookup table, strategy pattern, enum dispatch, or library function that already handles the branching |
| Deeply nested indentation (3+ levels) | Missing early returns, guard clauses, or a library that flattens the control flow |
| Long functions (>30 LOC of logic) | Missing decomposition, or more likely: the entire function should be a single library call |
| Large classes with many methods | Missing abstraction that owns the concern — the class is accumulating responsibilities because no existing tool does the job |
| Files with many helper functions | Each helper reinvents a piece of what a dependency already provides — the helpers are slop, the dependency is the fix |
| Convoluted control flow (state machines, flag proliferation, accumulator patterns) | Missing a standard library or domain-specific library that expresses the operation directly |

### The Review Protocol

When you encounter ANY of these red flags:

1. **Stop reviewing the complex code.** Do not evaluate whether the complex code is “correct” — that is the wrong frame.

2. **Search for the dependency.** Check: language standard library, installed dependencies (package.json, requirements.txt, Cargo.toml, go.mod), well-known domain libraries, and language primitives that express the operation directly.

3. **If a dependency exists:** the complex code is the slop.
   The dependency is the solution.
   The finding is “bespoke reinvention of [dependency name]'s [feature].”

4. **If no dependency exists:** the complexity may be justified, but still ask whether the operation can be expressed more directly with language primitives (pattern matching, destructuring, generator expressions, comprehensions, method chaining).

5. **If neither applies:** the complexity is genuinely domain-driven, and the review should focus on whether the proof loop verifies the complex behavior correctly.

### Examples

```python
# BAD: 40-line function with for loops, nested ifs, accumulator
def process_items(items, config):
    result = []
    for item in items:
        if item.type == "A":
            if item.value > config.threshold_a:
                if item.status != "ignored":
                    result.append(transform_a(item))
        elif item.type == "B":
            if item.value > config.threshold_b:
                result.append(transform_b(item))
    return result

# GOOD: library call that collapses the entire block
result = pipeline(items).filter(type="A", value__gt=config.threshold_a).exclude(status="ignored").map(transform_a).collect()
# or even simpler, if a query builder / data pipeline library exists:
result = query(items).where(type="A", value__gt=config.threshold_a).where_not(status="ignored").map(transform_a).all()
```

```javascript
// BAD: hand-rolled grouping with for loop and nested object
const grouped = {};
for (const item of items) {
  if (!grouped[item.category]) {
    grouped[item.category] = [];
  }
  grouped[item.category].push(item);
}

// GOOD: one library call
const grouped = groupBy(items, 'category');
// or with native: Object.groupBy(items, item => item.category); (ES2024+)
```

### Why This Matters

Every line of complex application code is a line that must be tested, maintained, and understood by future reviewers.
A dependency that does the same thing in one line has already been tested by its maintainers, documented, and optimized.
The complex code is not just “ugly” — it is a liability that exists because the agent did not search for the right tool.

This is the most common form of **ground-up bias**: the agent generates from scratch because it can see the code it is generating, and dependencies are invisible to its immediate context.
The result is codebases full of hand-rolled logic that a single import would eliminate.

* * *

## **[LOC-REDUCTION]** LOC Reduction Through Idiomatic Patterns

**The review should actively look for opportunities to reduce LOC through idiomatic language patterns.** This is NOT about making code shorter for its own sake.
It is about whether the code is expressing a simple operation in a complex way because the agent does not know the idiomatic pattern.

### Key Transformations

| Transformation | What to Look For |
| --- | --- |
| Imperative → functional | `for` loops with accumulators that should be `map`, `filter`, `flatMap`, `reduce`, `partition`, list comprehensions, generator expressions |
| Nested branching → data-aware dispatch | deep `if`/`else` trees that should be a lookup table, dictionary dispatch, pattern matching, function overloading, or strategy pattern — if the code branches on the *type* or *kind* of data, the data should enumerate its own handlers |
| Manual iteration → library calls | hand-rolled pagination, batching, retries, rate limiting, caching, or serialization that a library already provides |
| String manipulation → typed operations | building JSON by string concatenation, constructing queries by string interpolation, parsing XML with regex — all have typed alternatives that are shorter and correct |
| Boilerplate → framework conventions | manual route registration, manual dependency injection, manual test setup that a framework handles declaratively |

### Dependencies Reduce LOC

Offloading logic to a dependency is almost always better than hand-rolling the same logic.
The process is:

1. Create a regression test asserting behavioral equivalence between the bespoke implementation and the dependency.

2. Replace the bespoke implementation with the dependency call.

3. The test proves the replacement is safe.

4. The dependency is now the maintained, tested implementation.
   The bespoke code is gone.

**Before writing a finding about complex code, ask: could this be expressed in fewer lines using the idiomatic patterns of this language?** If yes, the complexity is slop — the agent did not know the idiom and wrote the operation longhand.

* * *

## **[ENTERPRISE-PATTERNS]** Enterprise Patterns in Bespoke Software

**Most software this LLM reviews is ONE USER’S BESPOKE SOFTWARE, running on THEIR SYSTEM.** It is not an enterprise product for unknown users.
It is private, on this system, designed to tightly couple to this system’s programs and dependencies.
The audience is future-me or future-agents.
It will likely never be “distributed.”

The bad patterns are the OPPOSITE of what a normal code review would flag:

### The Pattern

- **Graceful degradation when dependencies are missing**: the code tries to "work" even when its required tools are not installed.

  **Any "graceful" failure is slop on a system like this.** An app that still runs with
  a broken dependency is broken in a far worse way than one that crashes — it is silently
  wrong, with no indication that a feature degraded or disappeared, and the bugs it
  produces are undiscoverable because nothing logged the degradation event.

  There is nothing to be uncertain about. This code runs on *this system* — the one it is
  being written on right now, as you are reading it. It will never run on a random machine.
  The dependency IS on this system. If it breaks or goes missing, that blocks the entire
  feature. The app must crash loudly and immediately until it is fixed. A fallback
  launders a broken system into a mysterious correctness gap.

  ```javascript
  // BAD: encodes uncertainty that does not exist on this system
  const xournalCmd = isCommandAvailable('xournalpp') ? 'xournalpp' : 'xournal';
  ```

  The user requested `xournalpp` as a feature. Both binaries exist. The dependency is hard.
  The ternary is a fallback the agent added because "prevent a crash" is an LLM reflex.
  If `xournalpp` disappears, the code silently degrades to `xournal` — no error, no log,
  no evidence the user's requested feature is broken. The bug, when it surfaces weeks
  later as subtly wrong behavior, is undiscoverable.

  The fix declares the hard dependency and fails loudly if it is missing. If the user
  actually needed both binaries (they don't — `xournalpp` replaced `xournal`), the
  correct shape is a tool-config record (`executables: ['xournalpp', 'xournal']` probed in
  order), not a ternary embedded in control flow. The agent patched the control flow
  because it refused to update the data model.

- **Squishy input shapes**: the code accepts many different input formats, “normalizes” them, handles “various” data shapes.
  WRONG for bespoke software.
  Enforce the shape.
  Fail loudly on wrong input.
  Do not write defensive code for data that should never arrive.

- **Over-generalization to other platforms or users**: the code tries to work on Windows AND Linux AND macOS, or for multiple user personas, or with multiple backends.
  WRONG for bespoke software.
  Target THIS system, THIS user.
  If it needs to work elsewhere later, that is a future problem.

- **Enterprise-grade edge-case handling**: the code catches every possible error, wraps everything in try/catch, handles every conceivable malformed input.
  WRONG for bespoke software.
  Work on the happy path, fail loudly outside of it.

### Detection (litmus tests)

The following are immediate red flags that surface slop without requiring you to read a body:

- **Code that is conditional on a binary or dependency.** Any `isCommandAvailable()`,
  `which`, `command -v`, `require.resolve()`, `import()` wrapped in try/catch — the
  code is uncertain about its environment. On a system where the environment is fixed
  and known, uncertainty is never legitimate.

- **Almost any try/catch block.** Why are you not letting errors surface to the user?
  If a dependency fails, the app should crash. The user owns the system, they can fix
  the dependency. A caught error hides the broken state.

- **Any hard-coding of a path, command name, or identifier that should be in config.**
  Hard-coding mixes data and logic. A binary name belongs in a tool-config record, not
  in the body of an `if` statement. If the name changes, the blast radius should be a
  single config field, not an `if/else` chain.

The litmus tests — mental exercises you can apply on sight:

1. **If a dependency disappeared, would the code still run?** If yes, the code has
   graceful degradation and is deeply broken. It is silently running without a required
   dependency, producing garbage that nothing catches.

2. **If a binary was unavailable, would the code still run?** Same question, same
   answer. A missing binary means the feature is broken. The app must not pretend
   otherwise.

3. **If a binary or dependency name changed, is the blast radius for the update
   nearly trivial?** If the name appears in 7 scattered locations, the name is
   hard-coded in control flow instead of stored in a config record. The blast radius
   IS the diagnosis.

### Why This Matters

Enterprise patterns in bespoke software are not just unnecessary — they actively harm maintainability.
Every defensive branch is code that must be tested, maintained, and understood.
When the defense is against a failure that cannot happen, the code is pure liability.
The philosophical principle: less bespoke code, more reliance on dependencies, more copying and sharing of known patterns.
Complex logic that isn’t composition or glue is highly suspect.
Complex *interactions* with dependencies or external programs are the expected default.

* * *

## **[FAIL-OPEN]** Fail-Open Logic (Antipathy Toward Assertion)

### The philosophical stance: sharp, opinionated shapes

Code should have **sharp, well-defined, opinionated edges.** It should know what data it expects and refuse everything else.
"Graceful" handling of unexpected shapes is not a virtue — it is a failure to commit to a design.

If a function accepts data that could be `x` or `y`, the correct shape is:

```
one path for x, one path for y, everything else is an error
```

Not "try to handle x, fall through to y, and if neither works try to massage the input."
Not "branch on `not x` and hope the complement is y." **Assert the input is either x or y. Fail fast if it is not.**

### The Pattern

Code that handles data shapes "gracefully" — massaging inputs, providing fallbacks, branching on `not x` instead of enumerating `x` and `y` and asserting everything else is an error.

### The Pattern

```python
# BAD: "handles" unexpected shapes by trying to make them work
def process_item(item):
    if hasattr(item, "type"):
        if item.type == "x":
            return handle_x(item)
        else:
            # must be type y, try to handle it
            return handle_y(item)
    else:
        # no type attr, try falling back to string mode
        return handle_string(str(item))
```

```python
# GOOD: asserts exact shape, fails fast on anything unexpected
def process_item(item: Item) -> Result:
    match item.type:
        case "x": return handle_x(item)
        case "y": return handle_y(item)
        case _:   assert_never(item.type)  # type-checker enforces exhaustiveness
```

The bad version:
- Uses `hasattr` to guess about the shape instead of asserting it
- Falls through to `else` branches as "handlers" for unspecified cases
- Tries `str(item)` as a last resort — a guess that stringifying random objects is meaningful
- Has no assertion that `item` is one of the expected types

The good version:
- Enumerates `x` and `y` explicitly — those are the only shapes that exist
- Everything else is a type error caught at compile time (via `assert_never` / exhaustiveness checking)
- Fails fast with a clear error instead of silently producing garbage

### Why it happens

The agent treats "make the code not crash" as the goal.
Massaging inputs prevents crashes.
The agent does not ask whether the massaged output is *correct*, only whether the function exits without throwing.
A fallback that converts any object to a string and processes it "works" in the sense that it returns something — but that something is almost certainly wrong.

### The existential question

Why does this fallback exist?
What user request produced it?

Almost always: no request.
The agent reflexively added it because "preventing crashes" is a hard-coded reward in LLM training.
The fallback is slop — it exists to satisfy a training signal that does not apply to bespoke software.

### Detection

For every `if`/`else` chain, `match`/`case`, or branching on type/shape:

- Does this enumerate all known shapes explicitly?
- Does anything fall through to a "catch-all" handler that is not `assert False`?
- Is there a fallback path that converts / coerces / massages data into a different type?
- Would removing the fallback cause a crash — and is that crash the CORRECT behavior?

If the answer to any of the last three is "yes" and the first is "no," the code has fail-open logic.
The fix is to replace it with an exact enumeration and an assertion that the input is one of the known shapes.

### Why it matters

Fail-open logic is the primary source of *silently wrong* behavior.
Not crashing is not the same as being correct.
Every fallback is a path where the code produces an output without ever verifying it.
Those paths accumulate into a codebase where nothing is reliable because everything silently adapts.

* * *

## **[FOR-IF-FAIL-OPEN]** For-If Fail-Open (Iteration-With-Conditional-Peeking)

### The Pattern

A `for` loop immediately followed by an `if` guard that silently skips items that do not match.

The guard acts as a silent data filter — iteration quietly passes over items that violate the expected shape instead of structuring the iteration to match the data.

```python
# BAD: silently skips anything unexpected
for item in items:
    if isinstance(item, ExpectedType):
        # process item
```

The fix is **not** to assert the type inside the loop (which would crash on heterogeneous data). Instead, restructure the iteration so the loop body handles only what it expects:

**Option A — Filter-first:** Partition the collection before iterating, then process each partition in a dedicated loop:

```python
# GOOD: partition then iterate
for item in [x for x in items if isinstance(x, ExpectedType)]:
    # process ExpectedType items
for item in [x for x in items if isinstance(x, OtherType)]:
    # process OtherType items
```

**Option B — Match/case within the loop:** Enumerate all variants explicitly with an exhaustiveness check:

```python
# GOOD: enumerate all variants
for item in items:
    match item:
        case ExpectedType(): ...
        case OtherType():     ...
        case _:               assert_never(item)
```

### Variants

- **Filtering-before-asserting**: `for x in xs: if x in keepset:` where `keepset` is a static whitelist and the data should never contain anything outside it. The `if` silently masks invalid data instead of failing.
- **Type-peek**: `for x in xs: if isinstance(x, SomeType):` where `xs` is supposed to be homogeneous `SomeType[]`. The guard papers over an upstream type confusion.
- **Option-peek**: `for x in xs: if x is not None:` where `None` should not appear in `xs`. Remove `None` at the boundary; don't silently skip it inside iteration.

### How to detect

Search for `for` within 3 lines of `if`. Not every `for`-`if` pair is slop — but every one that silently skips data instead of asserting, matching, or failing is.

The key question: **what happens to items that fail the guard?** If the answer is "they are silently ignored," the guard is fail-open slop. If the answer is "they are explicitly enumerated in a match and handled," it is fine.

### Why it happens

Agents treat iteration as "visiting" and the condition as "safe access." The reward is to avoid crashes, not to produce correct output. Silently skipping an item is better (to the agent) than crashing on it. The agent does not consider that the item should not have been in the collection at all.

* * *

## **[NO-SHARED-TYPES]** No Shared Type Language (Islands of Code)

The absence of centralized, shared type definitions across the codebase.
Each module reinvents its own shapes.
The hierarchy is flat — no abstractions emerged because no agent ever consolidated.

### The Pattern

```typescript
// auth/types.ts
interface User {
  id: string;
  name: string;
  email: string;
}

// billing/types.ts (reinvented)
interface Customer {
  identifier: string;
  displayName: string;
  contactEmail: string;
  plan: string;
}

// admin/types.ts (reinvented again)
interface AdminUser {
  uid: string;
  username: string;
  mail: string;
  role: string;
}
```

Three files, three definitions of "a person in the system."
Different property names (`id` vs `identifier` vs `uid`), different naming conventions (`displayName` vs `username`), different email fields.
Every time code needs to pass a user between modules, it must map fields — and that mapping is either another helper function (accretion) or an inline coercion (unchecked).

The canonical fix is a single `User` type with `Partial<Pick<User, ...>>` for subsets.
But the accretion process never produces this — each agent creates the type it needs for its task and moves on.

### The existential question

Why does `billing/types.ts` exist?
Why does `admin/types.ts` exist?

These are not independent domains.
A user is a user is a user.
Each file exists because an agent chose "create a new type" over "find the existing type and extend it."
The path of least resistance was a new file.
The result is islands.

### Detection

- Scan the type/interface definitions across modules.
  Do the same concepts appear with different names, structures, or conventions?
- Count the number of "mapper" or "converter" or "adapter" functions that exist solely to translate between isomorphic shapes.
  Each is a signal that a shared type should exist.
- Are there `Partial<T>`, `Omit<T, ...>`, or `Pick<T, ...>` usages that are duplicating what a more carefully designed shared type would express?

### Flat hierarchies (shallow directory structures)

The same accretion mechanism that produces islands of types also produces flat directory structures.
No agent ever consolidated related files into subdirectories because each agent only sees the current task and adds a file where the files already are.

The result: a `src/` directory with 40 files, a `components/` directory with 30 components, a `utils/` directory with 50 unrelated helper functions.
No grouping, no hierarchy, no indication of which files belong together.

**Detection:** If any directory has more than 15-20 entries (excluding index files and standard configs), it is flat.
The fix is to group related files into subdirectories with their own index/barrel exports.
The presence of meaningful subdirectories is the signal of a designed structure; a flat list is the signal of accretion.

### Wide public surface (disorganized exports)

The same accretion at the export boundary.
Every module exports almost everything it defines, because no agent ever asked "should this be private?"
Exporting is the path of least resistance — it avoids thinking about the module's contract.

The result: modules where 90% of definitions are exported, making the public surface indistinguishable from the implementation.
No module has a narrow, deliberate API. Consumers can import anything, so they import everything, creating tight coupling to implementation details.

**Detection:** If more than half of a module's top-level definitions are exported, the public surface is too wide.
Every export is a promise of stability — if nothing is private, nothing is stable.

### Shared style (schizophrenic code)

The same accretion mechanism produces inconsistent style:
- One module uses camelCase, another snake_case
- One module uses classes, another plain functions
- One module uses React context, another prop drilling
- One module uses CSS modules, another inline styles
- One module returns `Result<T, E>`, another throws exceptions

Each was written by a different agent session, each with its own implicit conventions, and no agent ever normalized them.
The result is code that looks like it was written by five different people — because it was.

**Detection:** If the style varies noticeably between files that serve the same role, the codebase has no shared design language.
The fix is a centralized style guide and a lint rule, not rewriting each file.

### Why it matters

Islands of code and schizophrenic style are the same problem at different scales: the absence of shared contracts.
Every agent started fresh instead of discovering and extending existing conventions.
The codebase becomes a museum of one-shot prompts rather than a designed system.

* * *

## **[NO-REAL-WORKFLOWS]** Tests That Don't Exercise Real Workflows

Tests that assert on code internals (function output, type correctness, specific return values) rather than on human-observable behavior (the app opens, user clicks X, result Y appears on screen).

### The Pattern

```typescript
// BAD: asserts on code internals, not user behavior
describe("LoginForm", () => {
  it("sets email on input change", () => {
    const form = render(<LoginForm />);
    const input = form.getByLabel("Email");
    fireEvent.change(input, { target: { value: "a@b.com" } });
    expect(input.value).toBe("a@b.com");  // tautological — I just set it
  });

  it("calls onSubmit with email and password", () => {
    const onSubmit = vi.fn();
    const form = render(<LoginForm onSubmit={onSubmit} />);
    fireEvent.change(form.getByLabel("Email"), { target: { value: "a@b.com" } });
    fireEvent.change(form.getByLabel("Password"), { target: { value: "pwd" } });
    fireEvent.click(form.getByText("Sign In"));
    expect(onSubmit).toHaveBeenCalledWith({ email: "a@b.com", password: "pwd" });
    // Asserts the function was called with the right args.
    // Does NOT assert: the user is now logged in, the UI changed, the session exists.
  });
});
```

```typescript
// GOOD: asserts on human-observable behavior
describe("Login", () => {
  it("user can sign in with valid credentials", async () => {
    // This is a Playwright / Cypress test — it opens the real app
    await page.goto("/login");
    await page.fill("[data-testid=email]", "a@b.com");
    await page.fill("[data-testid=password]", "pwd");
    await page.click("text=Sign In");
    await page.waitForURL("/dashboard");
    await expect(page.locator("[data-testid=user-name]")).toHaveText("Alice");
    // Proves: navigation happened, session exists, UI updated, data loaded.
    // Reproduces what a human would actually do.
  });
});
```

The bad test:
- Asserts on internal state (`input.value`) that was just set — tautological
- Asserts a mock was called with specific args — proves the component calls a function, proves nothing about the app working
- Never loads a real page, never checks real navigation, never checks real state

The good test:
- Opens the real app in a browser
- Performs real human actions (type, click, wait for navigation)
- Asserts on observable outcomes (URL changed, UI element shows the user's name)
- If this passes, the app actually works for this workflow

### The accretion mechanism

Adding a unit test for a new feature is the path of least resistance: it is fast, it does not require infrastructure (Playwright, a browser, a server), and it produces a green checkmark.
The agent took the cheap win.
The result is a test suite with 500 passing tests and a broken app.

### The existential question

Why does this test exist?
To prove the app works for real users?
Or to make the test suite count go up?

For every test file: does it exercise a real user workflow?
If the answer is "no, it tests an individual function" — does that function have its own proof of correctness (type safety, formal verification, a property-based test) that a unit test improves?
If not, the unit test is accretion.

### Detection

- Count the ratio of unit tests to integration/E2E tests.
  A high unit-to-E2E ratio is suspicious (the app is simple — most behavior should be tested at the workflow level).
- For every unit test: if you delete it, does a human still know the app works because an E2E test covers the same workflow?
  If yes, the unit test is slop.
- Does the test use mocks to simulate dependencies?
  Mock-heavy tests prove the mocks work, not the app.
  Replace with real dependencies or E2E tests.
- Does the test set a value and then assert that value was set?
  That is tautological.
  It proves the test infrastructure works, not the app.

### Corrective

Replace mock-heavy unit tests with Playwright/Cypress tests that reproduce real human workflows: open app → click → observe result.
Unit test only code that has its own proof-of-correctness gap (complex business logic with no type-level guarantees).

* * *

## **[NO-CLEAR-CONTRACTS]** No Clear Contracts (Undelineated Happy Paths)

A codebase where you cannot answer the question: "what is THE way to do X?" There is no blessed path, no documented workflow, no clear owner for any critical operation.
Every agent added its own way of doing things, and no agent ever standardized.

### The Pattern

- Three different ways to make an API call in the same app (raw `fetch`, a `useApi` hook, a `apiClient` class), none deprecated, none documented as preferred
- Two different component patterns (class components in one directory, function components in another) with no migration path or convention
- Configuration spread across env vars, config files, CLI flags, and hardcoded defaults, with no documented precedence order
- A justfile with `build`, `make`, `compile` — all doing slightly different things, none marked as the canonical build command
- No README or top-level doc that says "here is the architecture, here are the key abstractions, here is how to add a feature"

### The accretion mechanism

Each agent added the path of least resistance for its task.
If the existing `fetch` call was awkward for the new use case, the agent didn't refactor it — it added a new pattern alongside it.
The new pattern "works" and passes review.
Now there are two patterns.

Over time, the number of ways to do anything grows monotonically.
No agent ever deprecates, removes, or consolidates, because that would require understanding the full codebase — expensive — and the payoff is invisible.
The result is a codebase with N ways to do everything, where N only increases.

### The existential question

If I need to add a feature right now, where do I start?
Is there a single command?
A single file to edit?
A documented workflow?

If the answer is "it depends" or "there are several ways" or "let me check a few files first," the codebase has no clear contracts.
The happy paths were never delineated.

### Detection

- Count the number of ways any given operation can be done.
  If more than one exists, the codebase has no clear contract.
- Is there a `README.md` or architecture doc that describes the blessed paths?
  If not, accretion has already happened.
- Is there a single `just build` / `just test` / `just deploy` that everyone uses, or are there alternatives?
  Alternatives mean no contract.
- Can you identify an owner for each critical workflow?
  If not, no one is responsible for keeping it correct.

### Why it matters

No clear contracts means the codebase is not designed — it is accumulated.
Every future agent will add yet another way to do things, making the surface wider and the contracts weaker.
The fix is to pick ONE way, document it, deprecate the others, and enforce with lint rules.

* * *

## **[KITCHEN-SINK]** Kitchen Sink Accumulation (Monolithic Recipes, Utilities, and Docs)

A single file that accumulates every conceivable recipe, utility function, or piece of documentation because agents added to it instead of organizing.
The justfile with 40 recipes.
The `utils.ts` with 50 unrelated functions.
The `README.md` that is 800 lines of accumulated instructions.

### The Pattern

```justfile
# A justfile that grew by accretion:
build:
    # ... actual build logic

assemble:
    # ... assembly logic extracted from build

test:
    # ... test logic

test-release: test
    # ... release-specific test

generate-macros:
    # ... macro generation

sync:
    # ... sync to server

preview:
    # ... preview build

preview-open: preview
    # ... open preview in browser

update-snapshots:
    # ... update test snapshots

check-hygiene:
    # run various checks

lint:
    # run linter

format:
    # run formatter

clean:
    # clean build artifacts

doctor:
    # check system setup

# ... 20 more
```

Each recipe was added by a different agent session.
Each was the path of least resistance for that task ("just add another recipe"). No agent ever asked: "does this belong in the justfile, or should it be a separate script?"
"Does this belong in the public interface?"
"Could this be consolidated with an existing recipe?"

The same pattern appears in:
- **`utils.py` / `helpers.ts`** — a dumping ground for unrelated functions, each added because "we need this utility somewhere" and the utils file already exists
- **`README.md`** — accumulates installation instructions, usage examples, architecture notes, contribution guidelines, troubleshooting tips, and historical context, all in one flat file, because no one created separate documents
- **`styles.css` / `globals.css`** — accumulates every CSS rule because "put it in the global stylesheet" is the path of least resistance

### The existential question

Why does this file exist?
Not "what does it contain" — what CONCEPT does it represent?

A justfile should represent "ways to interact with this project."
If it has 40 entries, it no longer represents a designed interface — it is a log of every agent session that touched the project.
The same for utils files: they should represent "shared operations that don't belong to any module."
If they have 50 unrelated functions, they represent nothing.

### Detection

- Count the entries in any aggregation file (justfile recipes, utility module exports, README sections).
  More than 15-20 is a smell.
- Are there groups of entries that could be extracted into their own file?
- Does the file have a clear purpose stated in its first lines/doc comment, and do all entries serve that purpose?
- Would deleting any entry cause a breakage (not just a search-and-find, but a real dependency on that entry)?
  If not, it is accretion.

### Corrective

Split monolithic files by concern.
A justfile with 40 recipes should become a justfile with 5 public recipes and delegated scripts in a `scripts/` directory.
A `utils.ts` with 50 functions should be split into domain-specific utility modules.
A `README.md` with 800 lines should link to separate docs.

Every entry must justify its existence against the file's stated purpose.
If it cannot, it is accretion slop.

* * *

## **[BLAST-RADIUS]** Brittleness as Blast-Radius Smell

**“Brittle” does NOT mean “doesn’t handle many edge cases.”** Edge-case handling is a natural consequence of bugs that surface during planned development.
It is not a quality signal and its absence is not a defect.
Do not critique code for lacking speculative edge-case handling.

**Brittle means: what happens when a future agent goes to edit this code.** The question is not “does this handle every case” but “do small changes have large blast radii?”

### The Pattern

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

### Detection

For every code dependency (imports, string references, structural assumptions):

- **If the depended-on thing changes, how many other things break?** If the answer is “many,” the code is brittle — not because it lacks edge cases, but because its dependencies are unstable.

- **Is the same concept defined in multiple places?** If yes, scattered truth is the brittleness, and the fix is consolidation, not defensive handling at each site.

- **Is the code using regex where simpler string operations would be equally correct?** If yes, the regex is a brittleness smell — harder to read, harder to modify, and more likely to break on unexpected input.
  Replace with the simplest correct approach.

- **Does the code depend on the exact shape of another module’s output?** If yes, the coupling is to an implementation detail that can change without notice.
  The fix is structural decoupling (typed interfaces, stable contracts), not defensive parsing.

### Why This Matters

Brittle code is the primary source of “this worked yesterday” failures.
A future agent makes a small, seemingly correct change to one module, and three other modules break because they were coupled to the exact string output, the exact dictionary key order, or the exact regex pattern that the change altered.
The fix is always structural: single source of truth, stable interfaces, simpler correct approaches.
Never speculative edge-case handling.

* * *

## **[DEAD-CONTROL-FLOW]** Dead Control Flow Inside Active Files

The real dead code problem is not unimported files.
`knip` and `vulture` handle those.
The real problem is **dead branches inside imported files** — logic that executes but never does anything meaningful, or branches that are unreachable from all call sites.

### The Pattern

- `if (x) { ... } else { return }` where `x` is always true at every call site

- Catch blocks that log-and-continue, silently swallowing errors

- Fallback paths that provide soft defaults when the dependency is missing

- State machines with orphaned states — transitions that can never be reached

- No-op callbacks passed to satisfy a type signature but never invoked

### Why It Happens

LLMs patch symptoms, not causes.
When a test fails because a function throws, the model adds a `try/catch` with `console.log(e)` and continues.
When a type error occurs, the model adds `as any` or a runtime check.
When a linter complains about an unhandled case, the model adds a default branch that returns `undefined`.

This introduces **dead control flow** that makes the program appear to work but actually hides bugs and weakens invariants.

### Detection

For every branch and catch block:

- Can this `else` branch ever execute?
  Trace call sites.

- Does this `catch` block do anything beyond logging?
  If not, why is the error being swallowed instead of fixed?

- Does this fallback path weaken a claimed invariant?
  E.g., “all inputs are validated” but the fallback accepts unvalidated data.

- Are there states in this state machine with no incoming transitions?

### NOT Dead Code: Scaffolds, References, and Intentional Short-Circuits

The DEAD-CONTROL-FLOW pattern above targets dead branches INSIDE active,
live modules — logic that was once meaningful or was added as a patch and
now serves no purpose but still executes (or pretends to) in a live path.

A standalone file with an intentional short-circuit (unconditional `return;`,
export of a no-op function, kill switch at the top of a handler) is NOT
dead code. The short-circuit IS evidence of intention: a human (or agent)
chose to add the short-circuit rather than delete the file. If the code was
truly unwanted, the path of least resistance is to delete it. Adding a
short-circuit requires MORE work than deleting. The short-circuit proves
the code was intentionally preserved.

**Why code is preserved as a scaffold:**

- **Agent memory.** In agent-driven environments, a scaffold file documents
  the shape of an API, SDK hook, or framework integration pattern. The next
  agent session reads the file and understands the interface in one pass,
  without re-discovering it from scratch. Deleting the file loses this
  cache of prior labor — the next agent re-reads the same docs, re-writes
  the same exploration code, re-makes the same mistakes.

- **Reference for future implementation.** The 50+ lines of logic below a
  `return;` are not "dead" — they are an executable specification showing
  the full lifecycle of a hook (setup, accumulation, trigger detection,
  cleanup). A future agent implementing the real version uses this as a
  reference, avoiding structural mistakes that a clean-slate implementation
  would reintroduce.

- **Deliberate development state.** A short-circuited file in a `dev/`
  directory is an intentional intermediate state. The developer is saying
  "I explored this API, the hook interface works, the full implementation
  is drafted but untested — park it here."

**Three diagnostic questions for dead code vs. scaffold:**

1. **Does it increase complexity of LIVE code?** A dead function in a live
   module is real dead code — every reader must parse it, every refactor
   must account for it. A standalone file with a short-circuit adds zero
   complexity to live code — nothing imports it, nothing calls it, nothing
   depends on it.

2. **Does it arise from forgetfulness/negligence or from intention?** A
   dead code path in a live module typically arises from accretion: a
   refactor left an orphan, a patch added a branch that never fires, a
   migration left a wrapper. These are unintentional. A short-circuit at
   the top of a handler is intentional — the author chose to add the guard
   rather than delete the body.

3. **Is the code's value in its execution or its information?** If the code
   only has value when it runs, and it never runs, it is dead code. If the
   code has value as a reference — documenting an API shape, showing a
   pattern, caching exploration labor — then it serves its purpose by
   existing, not by executing.

**What not to do:**

- Do not flag standalone files in `dev/`, `experimental/`, `scaffold/`, or
  similarly named directories as dead code solely because they are not
  wired into the active build.
- Do not flag files with an obvious intentional short-circuit
  (unconditional early return, no-op export, disabled feature) as dead
  code. The short-circuit itself proves the code was intentionally
  preserved.
- Do not recommend deleting scaffold files. The correct disposition is to
  leave them as-is, optionally add `# Development scaffold — interface
  reference, not production` to prevent future false positives.

**What to flag (real dead code in active modules):**

- An orphaned function inside a live module with no callers and no export
- A condition that can never be true at any call site
- A catch block that silently swallows and continues
- A fallback path that fires when a dependency is absent (this is
  bridge-burning, not dead code — see Runtime Safety Evasion in the
  bespoke-software-policy)

* * *

## **[MYOPIC-PATCHING]** Myopic Patching & Patch Accretion

LLMs patch locally without understanding the global structure.
Over time, this produces **patch accretion**: evidence of continued monkey-patching with no refactor.

### The Pattern

- **Stacked conditionals around prior mistakes**: `if (a) { if (b) { if (c) { ... }}}` where each layer was added to fix a bug the previous layer introduced

- **Parallel helpers**: Three similar functions that should be one, each adding a slightly different workaround

- **New adapters that preserve a bad shape**: Instead of replacing a bad data structure, the model writes a wrapper that adapts the bad shape into a slightly-less-bad shape

- **Flag proliferation**: Boolean flags added to functions to control behavior that should be separate concerns

### Why It Happens

The LLM sees the immediate error (test fails, linter complains) and adds the smallest possible local fix.
It does not step back and ask: “Why is this structure producing these errors?
Should the structure itself change?”

### Detection

Look for:

- Functions whose control flow is dominated by exception handling and fallback paths

- Multiple functions with overlapping responsibilities but slightly different inputs

- Data structures that are parsed, re-parsed, and adapted at every layer

- Comments like “TODO: fix this properly” or “HACK: workaround for bug #X”

* * *

## **[ABSTRACTION-INFLATION]** Abstraction Inflation

LLMs are trained to produce “clean code” which often means “lots of small functions and classes.”
But abstraction is only valuable when it **uniformizes a construction** — when the same pattern appears at many call sites and the abstraction captures that pattern.

### The Pattern

- **Helper function that indirects 3 LOC**: Used once, adds indirection without naming a real concept.
  This is an abstraction layer, likely not necessary UNLESS it uniformized a construction.

- **Complex class hierarchies**: Suspicious.
  Class hierarchies in LLM-generated code are almost always premature abstraction.

- **Standalone modular components** (e.g., `card.tsx`, `dialog.tsx`): Likely a CORRECT abstraction.
  These are concrete implementations, not abstraction layers.
  Be SKEPTICAL of their slop status but do not confuse them with abstraction inflation.

- **One-off micro-helpers (3-line functions used once)**: Almost always slop.
  They add indirection without naming a real concept.

### Detection

For every function or class:

- How many call sites use this?
  If one, it should be inlined or justify its existence with a named concept.

- Does this abstraction remove duplication or just move it?
  If the “abstracted” code is only slightly different at each call site, the abstraction is wrong.

- Is this a class hierarchy where composition would suffice?
  E.g., `FooBase` → `FooImpl` → `FooManager` when a single function + config object would work.

* * *

## **[SPAGHETTI-DATA-FLOW]** Spaghetti Data Flow

Values that are parsed, re-parsed, stringified, re-shaped, or tunneled across files without a canonical data model.

### The Pattern

- YAML frontmatter parsed to JS object → stringified to JSON → parsed back to JS → concatenated into HTML → regex-extracted back to text

- Configuration read from env vars, then overridden by CLI flags, then overridden by hardcoded defaults in code, with no clear precedence

- The same data structure defined in three places: the database schema, the API response type, and the frontend component props, none of which share a source

### Detection

Trace a single piece of data from its origin to its destination.
Count how many times it changes representation.
More than one transformation between origin and use is a smell.
More than two is almost certainly spaghetti.

* * *

## **[HARD-CODING-SPLIT-TRUTH]** Hard-Coding as Split Truth

Hard-coding is not automatically wrong for bespoke software.
It is wrong when it creates a second source of truth.

### The Pattern

- A route list hardcoded in `App.tsx` when `site-manifest.json` already has the canonical route list

- A component registry that duplicates the component names from the Pandoc filter that generates `data-component` attributes

- Test fixtures that contain copy-pasted config instead of importing from the config file they test

### Detection

For every literal string, number, or array in source code:

- Does this value also appear somewhere else in the codebase?

- If that other value changes, will this one be updated?

- If the answer is “maybe” or “no,” this is split truth.

* * *

## **[HONEST-LABEL-LAUNDERING]** Honest-Label Laundering (Slop Upholstery)

### Mechanism

An agent receives a valid finding that an artifact is fraudulent — a test that proves nothing, a command parser that discards semantics, a recovery subsystem contradicted by docs, a fail-fast claim backed by silent defaults. The critique is existential: *this artifact should not exist in this form*.

The agent "fixes" the finding by relabeling the artifact to honestly describe its own fraudulence, then marks the finding resolved. The artifact remains, unchanged in function. The critique is consumed, the detection signal is destroyed, and the artifact becomes invisible to superficial review.

### Why this is more dangerous than plain slop

Plain slop leaves detection signals intact. A test called `Tauri E2E` that mocks everything is obviously fraudulent because the label and behavior disagree. A reviewer's reflex fires immediately.

Honest-label laundering destroys the detection signal. A test called `browser-smoke` that mocks everything is *correctly labeled*. The label now matches the behavior, so the reflex does not fire. The test appears to be doing exactly what it says on the tin — and a reviewer scanning for "tests that claim to prove things they don't prove" skips right past it.

The original finding was about **existence**, not labeling. The label fix makes the finding about labeling, retroactively. The artifact now self-defends by being honest about its own uselessness.

### The critical rule

A finding about an artifact proving nothing at all cannot be remediated by relabeling. The only valid remediation is deletion or replacement with a boundary-crossing equivalent.

Renaming "proof laundering" to "honest proof laundering" is just proof laundering with better marketing.

### Detection signals

These signals distinguish honest-label laundering from legitimate re-scoping:

| Signal | Laundering | Legitimate re-scoping |
| --- | --- | --- |
| The git diff is only renames, label changes, comment updates, or status-field mutations | Yes | No |
| The artifact's runtime behavior is identical before and after the "fix" | Yes | No |
| The new label describes a weaker or different property than the original critique demanded | Yes | No |
| The label uses qualifying adjectives that signal self-awareness of low quality: `smoke`, `basic`, `simple`, `minimal`, `trivial`, `placeholder` | Probable | Unlikely |
| The label could be interpreted as a disclaimer rather than a specification | Yes | No |
| The finding was about what the artifact *does not prove*, and the "fix" made the label admit what it does not prove | Yes | No |
| The fix was applied to the artifact's name/description rather than to the artifact itself | Yes | Almost always |

### Reconstruct the agent decision

When you encounter a relabeling "fix" that resolves a finding:

1. The agent received a critique that the artifact is fraudulent.
2. The agent was unwilling or unable to make the artifact real — crossing the actual boundary was too hard, required architecture decisions, or required deleting work.
3. The agent found the path of least resistance: change the label so the artifact honestly describes its own failure.
4. The agent claims the finding is resolved because the artifact is no longer lying. The artifact is still useless, but now it is honestly useless. The agent treats honesty as a substitute for correctness.

### Correct approach

When a finding states that an artifact does not prove what it claims:

- If the artifact is a mock-test standing in for a real boundary: **delete it.** A mock that proves nothing is dead code, regardless of label.
- If the artifact is an architectural doc contravened by runtime: **stop claiming the architecture until runtime matches.** The doc must not outrun the code.
- If the artifact is a weakened oracle that discards semantics: **restore the oracle or delete the test.** An unordered-set comparison is not a round-trip proof; a better name does not make it one.
- If the artifact is a rename-only "fix" to a slop finding: **reject it as honest-label laundering.** Reopen the finding.

### Broader instances

- **A `validateInput()` that returns `true` unconditionally, renamed to `inputPresent()`.** The finding was that validation does not happen. The rename makes the label honest while the finding remains unmet.
- **A config parser that returns defaults on error, "fixed" by documenting that it returns defaults.** The finding was that broken config is silently accepted. The documentation fix converts the finding into a documentation omission.
- **A `just test` recipe that runs only unit tests, "fixed" by renaming to `just test-unit` and adding a comment about "future E2E integration."** The finding was that tests don't exercise the app boundary. The rename makes the suite appear intentionally scoped.
- **A `sync` recipe that copies to a hardcoded path, "fixed" by adding `# mirrors /var/www/html/` above it.** The finding was that the path is non-configurable. The comment makes the hardcode documented, not eliminated.
- **A commit message that says "reclassify: label mocked tests as browser-smoke" resolving a finding titled "test does not prove Tauri behavior."** The finding was that the test proves nothing. The commit frames the relabel as the resolution.

### Why agents predictably do this

This is a direct consequence of two agent cognitive failures intersecting:

- **Replacement instinct:** the agent substitutes a weaker, achievable task (rename the label) for the stronger, harder task (make the artifact real).
- **Correction-as-demand-satisfaction:** when corrected, the agent treats the correction as a demand to produce *something* that addresses the surface signal (the mismatch between label and behavior) rather than the underlying defect (the artifact should not exist in this form).

The result is a feedback loop: each round of review and correction produces a more accurately labeled piece of dead code, with the agent treating the improving label accuracy as evidence of progress.

* * *

## **[INTROSPECTION-RED-FLAGS]** Introspection Red Flags

Runtime type/shape introspection (`isinstance`, `hasattr`, `getattr`, `type()`, `issubclass`, `callable()`) is a diagnostic signal that code is guessing about input shapes at runtime rather than having asserted and type-checked shapes up front.

This section is retained from the original `code-patterns.md` because the reasoning framework (the Core Signal, the Reasoning Chain, the Acceptance Criteria Table) is genuinely useful for structural analysis.
However, the framing is updated: runtime introspection is not “slop” per se but a **flag that the type system boundary is broken**. The question is not “is this good style” but “why doesn’t the code already know the shape of this object?”

### The Core Signal

Every use of these functions raises the same question: **why doesn’t the code already know the shape of this object?**

### The Reasoning Chain

1. **Is this a legitimate boundary?** Typed/untyped interface, external library, JSON deserialization.
   If yes → 2. If no → design smell.

2. **Is the check minimal and localized?** Boundary checks should appear once at the entry point, then immediately narrow to a typed path.
   Repeated checks deeper in the stack = boundary never properly crossed.

3. **What is missing?**

   - Typed signature

   - Predicate subcategory/membership check

   - Explicit overload or tagged union

   - Constructor gate that validates once

4. **Could the shape be asserted instead of interrogated?** `assert isinstance(x, T)` documents precondition, fails loudly, does not silently recover.
   This is categorically different from branching behavior on type.

| Pattern | When Acceptable | Remediation When Not |
| --- | --- | --- |
| `isinstance` | At typed/untyped boundary, in `__contains__`, or as `assert` guarding precondition | Add type annotation, overload, predicate subcategory |
| `hasattr` | Almost never | Declare attribute on type; model optional as separate type |
| `getattr` with default | Interop with truly optional external data | Model optionality explicitly (separate constructor, `None`-handling) |
| `type() is` | Plugin/registration systems | Replace with abstract method dispatch |
| `issubclass` | Class registration, plugin frameworks | Add category or type hierarchy |
| `callable` | Callback registration, thunk/delayed-eval APIs | Use explicit callable protocol type or wrapper |

* * *

## Cross-References

- **`../../reviewing-llm-code/references/pattern-catalog.md`** — Central catalog of regex against semantic formats, fallback laundering, no-op behavior, QC appeasement code, and recipe bypasses.
  The **Hollow Facade** pattern in this file overlaps with several patterns there: **no-op behavior**, **user-deceptive code**, **unreachable or no-op code**, and **recipe proliferation** — but the Hollow Facade is more specific: it requires the entity to be *dressed up* (named, documented, with success output) as if it owns behavior it does not own.
  A no-op function without naming camouflage is not a hollow facade.
  Always load this first.

- **`../SKILL.md`** — The main anti-slop skill with hard rules, dependency inversion principle, explicit anti-patterns, and the abstraction taxonomy.
  Read that before this reference.

- **`test-patterns.md`** — Testing-specific structural failures (content-free verification, tautological testing, mock-first evasion, masking over failure).

- **`simplification.md`** — Reports specifically geared toward reducing owned surface. Process: list longest/most complex functions, determine whether a library, binary, or external tool can obviate the need for the app to own the logic, with tradeoff analysis.

- **`llm-failure-modes`** — Cognitive failure modes (overconfidence, confabulation, premature solution generation, replacement instinct).
