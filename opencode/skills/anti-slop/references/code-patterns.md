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

**This is not a standard code review.** The code works on at least one user-requested
happy path.
You are reviewing implementation quality beneath correct behavior, not design
validity.
Any seemingly strange choice about features, behavior, or coupling to externals
is almost certainly a user-driven design decision — an LLM would never voluntarily make
out-of-distribution design choices in isolation.
Design choices are premises; do not critique them.
The patterns below apply to implementation quality only.

For the canonical catalog of LLM code-review patterns, load
[`../../reviewing-llm-code/references/pattern-catalog.md`](../../reviewing-llm-code/references/pattern-catalog.md).
That file covers regex against semantic formats, fallback laundering, no-op behavior, QC
appeasement code, and recipe bypasses.

This file covers patterns specific to **code shape and structure** that arise from LLM
generation: dependency aversion, myopic patching, patch accretion, dead control flow,
and bespoke reinvention of standard patterns.

## Table of Contents

- Dependency Aversion & Bespoke Reinvention

- Dead Control Flow Inside Active Files

- Myopic Patching & Patch Accretion

- Abstraction Inflation

- Spaghetti Data Flow

- Hard-Coding as Split Truth

- Introspection Red Flags

## Dependency Aversion & Bespoke Reinvention

The primary LLM failure mode: **reinventing something to solve a problem that is already
solved**. This is embarrassing.
In a code review, the immediate feedback would be: **why the fuck did you even write
this at all when you could have imported something that exists?**

### The Pattern

The LLM generates custom code for a problem that a known dependency solves:

- Custom `AcademicCard.tsx` (~60 LOC) when `card.tsx` exists in the UI inventory

- Custom `FilterControls.tsx` with hand-rolled popover logic when `select.tsx`,
  `dropdown-menu.tsx`, and `scroll-area.tsx` already exist

- Custom `PaginatedScroller.tsx` with bespoke scroll logic when `scroll-area.tsx`

  + `pagination.tsx` already exist

- Custom string-concatenated YAML generation when a YAML library is installed

- Custom hand-rolled AST stringifier when the parser library (`Pandoc`, `remark`,
  `markdown-it`) already provides stringification

### Why It Happens

LLMs have a strong implicit bias toward code they can see and understand.
Dependencies are “black boxes.”
Custom code feels “simpler” because it is local and visible.
The model treats local code as minimal and imported code as bloat.

This is the **dependency inversion failure**: the model perceives the generic, tested
solution as “abstraction layer bloat” and the bespoke reinvention as “clean, minimal
code.”

### Detection

For every custom function or component, ask: **“Is there a standard library or installed
dependency that already solves this?”**

If yes, the custom code is slop.
The absence of an import is the defect, not the presence of the dependency.

### Correct Response

**REFINE, REPLACE, REFACTOR** — migrate the bespoke implementation to use the
dependency. Do not delete the dependency because it is “unused.”

* * *

## Complexity as a Dependency-Detection Signal

**Complexity itself is the red flag.** When application code is structurally complex,
the reviewer’s FIRST question must be: “Is there a known library, language primitive, or
installed dependency that collapses this entire block into a one-liner?”

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

1. **Stop reviewing the complex code.** Do not evaluate whether the complex code is
   “correct” — that is the wrong frame.

2. **Search for the dependency.** Check: language standard library, installed
   dependencies (package.json, requirements.txt, Cargo.toml, go.mod), well-known domain
   libraries, and language primitives that express the operation directly.

3. **If a dependency exists:** the complex code is the slop.
   The dependency is the solution.
   The finding is “bespoke reinvention of [dependency name]'s [feature].”

4. **If no dependency exists:** the complexity may be justified, but still ask whether
   the operation can be expressed more directly with language primitives (pattern
   matching, destructuring, generator expressions, comprehensions, method chaining).

5. **If neither applies:** the complexity is genuinely domain-driven, and the review
   should focus on whether the proof loop verifies the complex behavior correctly.

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

Every line of complex application code is a line that must be tested, maintained, and
understood by future reviewers.
A dependency that does the same thing in one line has already been tested by its
maintainers, documented, and optimized.
The complex code is not just “ugly” — it is a liability that exists because the agent
did not search for the right tool.

This is the most common form of **ground-up bias**: the agent generates from scratch
because it can see the code it is generating, and dependencies are invisible to its
immediate context.
The result is codebases full of hand-rolled logic that a single import
would eliminate.

* * *

## LOC Reduction Through Idiomatic Patterns

**The review should actively look for opportunities to reduce LOC through idiomatic
language patterns.** This is NOT about making code shorter for its own sake.
It is about whether the code is expressing a simple operation in a complex way because
the agent does not know the idiomatic pattern.

### Key Transformations

| Transformation | What to Look For |
| --- | --- |
| Imperative → functional | `for` loops with accumulators that should be `map`, `filter`, `flatMap`, `reduce`, `partition`, list comprehensions, generator expressions |
| Nested branching → data-aware dispatch | deep `if`/`else` trees that should be a lookup table, dictionary dispatch, pattern matching, function overloading, or strategy pattern — if the code branches on the *type* or *kind* of data, the data should enumerate its own handlers |
| Manual iteration → library calls | hand-rolled pagination, batching, retries, rate limiting, caching, or serialization that a library already provides |
| String manipulation → typed operations | building JSON by string concatenation, constructing queries by string interpolation, parsing XML with regex — all have typed alternatives that are shorter and correct |
| Boilerplate → framework conventions | manual route registration, manual dependency injection, manual test setup that a framework handles declaratively |

### Dependencies Reduce LOC

Offloading logic to a dependency is almost always better than hand-rolling the same
logic. The process is:

1. Create a regression test asserting behavioral equivalence between the bespoke
   implementation and the dependency.

2. Replace the bespoke implementation with the dependency call.

3. The test proves the replacement is safe.

4. The dependency is now the maintained, tested implementation.
   The bespoke code is gone.

**Before writing a finding about complex code, ask: could this be expressed in fewer
lines using the idiomatic patterns of this language?** If yes, the complexity is slop —
the agent did not know the idiom and wrote the operation longhand.

* * *

## Enterprise Patterns in Bespoke Software

**Most software this LLM reviews is ONE USER’S BESPOKE SOFTWARE, running on THEIR
SYSTEM.** It is not an enterprise product for unknown users.
It is private, on this system, designed to tightly couple to this system’s programs and
dependencies. The audience is future-me or future-agents.
It will likely never be “distributed.”

The bad patterns are the OPPOSITE of what a normal code review would flag:

### The Pattern

- **Graceful degradation when dependencies are missing**: the code tries to “work” even
  when its required tools are not installed.
  WRONG for bespoke software.
  Fail loudly. The dependency IS available.
  This is enterprise thinking for unknown deployment targets.

- **Squishy input shapes**: the code accepts many different input formats, “normalizes”
  them, handles “various” data shapes.
  WRONG for bespoke software.
  Enforce the shape. Fail loudly on wrong input.
  Do not write defensive code for data that should never arrive.

- **Over-generalization to other platforms or users**: the code tries to work on Windows
  AND Linux AND macOS, or for multiple user personas, or with multiple backends.
  WRONG for bespoke software.
  Target THIS system, THIS user.
  If it needs to work elsewhere later, that is a future problem.

- **Enterprise-grade edge-case handling**: the code catches every possible error, wraps
  everything in try/catch, handles every conceivable malformed input.
  WRONG for bespoke software.
  Work on the happy path, fail loudly outside of it.

### Detection

For every defensive pattern (try/catch, input normalization, platform detection,
fallback paths):

- Is this defending against a failure that cannot happen on this system?

- Is this accommodating a user or platform that does not exist?

- Is this “graceful degradation” for a dependency that IS available?

If yes, the defense is enterprise debris.
The correct behavior is to fail loudly and fix the input or install the dependency.

### Why This Matters

Enterprise patterns in bespoke software are not just unnecessary — they actively harm
maintainability. Every defensive branch is code that must be tested, maintained, and
understood. When the defense is against a failure that cannot happen, the code is pure
liability.
The philosophical principle: less bespoke code, more reliance on dependencies,
more copying and sharing of known patterns.
Complex logic that isn’t composition or glue is highly suspect.
Complex *interactions* with dependencies or external programs are the expected default.

* * *

## Brittleness as Blast-Radius Smell

**“Brittle” does NOT mean “doesn’t handle many edge cases.”** Edge-case handling is a
natural consequence of bugs that surface during planned development.
It is not a quality signal and its absence is not a defect.
Do not critique code for lacking speculative edge-case handling.

**Brittle means: what happens when a future agent goes to edit this code.** The question
is not “does this handle every case” but “do small changes have large blast radii?”

### The Pattern

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

### Detection

For every code dependency (imports, string references, structural assumptions):

- **If the depended-on thing changes, how many other things break?** If the answer is
  “many,” the code is brittle — not because it lacks edge cases, but because its
  dependencies are unstable.

- **Is the same concept defined in multiple places?** If yes, scattered truth is the
  brittleness, and the fix is consolidation, not defensive handling at each site.

- **Is the code using regex where simpler string operations would be equally correct?**
  If yes, the regex is a brittleness smell — harder to read, harder to modify, and more
  likely to break on unexpected input.
  Replace with the simplest correct approach.

- **Does the code depend on the exact shape of another module’s output?** If yes, the
  coupling is to an implementation detail that can change without notice.
  The fix is structural decoupling (typed interfaces, stable contracts), not defensive
  parsing.

### Why This Matters

Brittle code is the primary source of “this worked yesterday” failures.
A future agent makes a small, seemingly correct change to one module, and three other
modules break because they were coupled to the exact string output, the exact dictionary
key order, or the exact regex pattern that the change altered.
The fix is always structural: single source of truth, stable interfaces, simpler correct
approaches. Never speculative edge-case handling.

* * *

## Dead Control Flow Inside Active Files

The real dead code problem is not unimported files.
`knip` and `vulture` handle those.
The real problem is **dead branches inside imported files** — logic that executes but
never does anything meaningful, or branches that are unreachable from all call sites.

### The Pattern

- `if (x) { ... } else { return }` where `x` is always true at every call site

- Catch blocks that log-and-continue, silently swallowing errors

- Fallback paths that provide soft defaults when the dependency is missing

- State machines with orphaned states — transitions that can never be reached

- No-op callbacks passed to satisfy a type signature but never invoked

### Why It Happens

LLMs patch symptoms, not causes.
When a test fails because a function throws, the model adds a `try/catch` with
`console.log(e)` and continues.
When a type error occurs, the model adds `as any` or a runtime check.
When a linter complains about an unhandled case, the model adds a default branch that
returns `undefined`.

This introduces **dead control flow** that makes the program appear to work but actually
hides bugs and weakens invariants.

### Detection

For every branch and catch block:

- Can this `else` branch ever execute?
  Trace call sites.

- Does this `catch` block do anything beyond logging?
  If not, why is the error being swallowed instead of fixed?

- Does this fallback path weaken a claimed invariant?
  E.g., “all inputs are validated” but the fallback accepts unvalidated data.

- Are there states in this state machine with no incoming transitions?

* * *

## Myopic Patching & Patch Accretion

LLMs patch locally without understanding the global structure.
Over time, this produces **patch accretion**: evidence of continued monkey-patching with
no refactor.

### The Pattern

- **Stacked conditionals around prior mistakes**: `if (a) { if (b) { if (c) { ... }}}`
  where each layer was added to fix a bug the previous layer introduced

- **Parallel helpers**: Three similar functions that should be one, each adding a
  slightly different workaround

- **New adapters that preserve a bad shape**: Instead of replacing a bad data structure,
  the model writes a wrapper that adapts the bad shape into a slightly-less-bad shape

- **Flag proliferation**: Boolean flags added to functions to control behavior that
  should be separate concerns

### Why It Happens

The LLM sees the immediate error (test fails, linter complains) and adds the smallest
possible local fix.
It does not step back and ask: “Why is this structure producing these
errors? Should the structure itself change?”

### Detection

Look for:

- Functions whose control flow is dominated by exception handling and fallback paths

- Multiple functions with overlapping responsibilities but slightly different inputs

- Data structures that are parsed, re-parsed, and adapted at every layer

- Comments like “TODO: fix this properly” or “HACK: workaround for bug #X”

* * *

## Abstraction Inflation

LLMs are trained to produce “clean code” which often means “lots of small functions and
classes.” But abstraction is only valuable when it **uniformizes a construction** — when
the same pattern appears at many call sites and the abstraction captures that pattern.

### The Pattern

- **Helper function that indirects 3 LOC**: Used once, adds indirection without naming a
  real concept. This is an abstraction layer, likely not necessary UNLESS it uniformized
  a construction.

- **Complex class hierarchies**: Suspicious.
  Class hierarchies in LLM-generated code are almost always premature abstraction.

- **Standalone modular components** (e.g., `card.tsx`, `dialog.tsx`): Likely a CORRECT
  abstraction. These are concrete implementations, not abstraction layers.
  Be SKEPTICAL of their slop status but do not confuse them with abstraction inflation.

- **One-off micro-helpers (3-line functions used once)**: Almost always slop.
  They add indirection without naming a real concept.

### Detection

For every function or class:

- How many call sites use this?
  If one, it should be inlined or justify its existence with a named concept.

- Does this abstraction remove duplication or just move it?
  If the “abstracted” code is only slightly different at each call site, the abstraction
  is wrong.

- Is this a class hierarchy where composition would suffice?
  E.g., `FooBase` → `FooImpl` → `FooManager` when a single function + config object
  would work.

* * *

## Spaghetti Data Flow

Values that are parsed, re-parsed, stringified, re-shaped, or tunneled across files
without a canonical data model.

### The Pattern

- YAML frontmatter parsed to JS object → stringified to JSON → parsed back to JS →
  concatenated into HTML → regex-extracted back to text

- Configuration read from env vars, then overridden by CLI flags, then overridden by
  hardcoded defaults in code, with no clear precedence

- The same data structure defined in three places: the database schema, the API response
  type, and the frontend component props, none of which share a source

### Detection

Trace a single piece of data from its origin to its destination.
Count how many times it changes representation.
More than one transformation between origin and use is a smell.
More than two is almost certainly spaghetti.

* * *

## Hard-Coding as Split Truth

Hard-coding is not automatically wrong for bespoke software.
It is wrong when it creates a second source of truth.

### The Pattern

- A route list hardcoded in `App.tsx` when `site-manifest.json` already has the
  canonical route list

- A component registry that duplicates the component names from the Pandoc filter that
  generates `data-component` attributes

- Test fixtures that contain copy-pasted config instead of importing from the config
  file they test

### Detection

For every literal string, number, or array in source code:

- Does this value also appear somewhere else in the codebase?

- If that other value changes, will this one be updated?

- If the answer is “maybe” or “no,” this is split truth.

* * *

## Introspection Red Flags

Runtime type/shape introspection (`isinstance`, `hasattr`, `getattr`, `type()`,
`issubclass`, `callable()`) is a diagnostic signal that code is guessing about input
shapes at runtime rather than having asserted and type-checked shapes up front.

This section is retained from the original `code-patterns.md` because the reasoning
framework (the Core Signal, the Reasoning Chain, the Acceptance Criteria Table) is
genuinely useful for structural analysis.
However, the framing is updated: runtime introspection is not “slop” per se but a **flag
that the type system boundary is broken**. The question is not “is this good style” but
“why doesn’t the code already know the shape of this object?”

### The Core Signal

Every use of these functions raises the same question: **why doesn’t the code already
know the shape of this object?**

### The Reasoning Chain

1. **Is this a legitimate boundary?** Typed/untyped interface, external library, JSON
   deserialization. If yes → 2. If no → design smell.

2. **Is the check minimal and localized?** Boundary checks should appear once at the
   entry point, then immediately narrow to a typed path.
   Repeated checks deeper in the stack = boundary never properly crossed.

3. **What is missing?**

   - Typed signature

   - Predicate subcategory/membership check

   - Explicit overload or tagged union

   - Constructor gate that validates once

4. **Could the shape be asserted instead of interrogated?** `assert isinstance(x, T)`
   documents precondition, fails loudly, does not silently recover.
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

- **`../../reviewing-llm-code/references/pattern-catalog.md`** — Central catalog of
  regex against semantic formats, fallback laundering, no-op behavior, QC appeasement
  code, and recipe bypasses.
  Always load this first.

- **`../SKILL.md`** — The main anti-slop skill with hard rules, dependency inversion
  principle, explicit anti-patterns, and the abstraction taxonomy.
  Read that before this reference.

- **`test-patterns.md`** — Testing-specific structural failures (content-free
  verification, tautological testing, mock-first evasion, masking over failure).

- **`llm-failure-modes`** — Cognitive failure modes (overconfidence, confabulation,
  premature solution generation, replacement instinct).
