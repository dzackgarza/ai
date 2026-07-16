# Clean Code

## Overview

Clean code reads like well-written prose.

**Authority note:** This skill is subordinate to repo-specific policies.
Where this skill's patterns conflict with higher-ranked skills in the authority
hierarchy (see `quality-control`), the higher-ranked skill wins. In particular:

- `code-patterns-python`' "fail fast, no speculative try/catch" overrides "start with
  try-catch-finally" (see `error-handling.md`).

- `test-guidelines`'s "no mocks, no exceptions" overrides any mock-enabling rationale.

- The fail-loud policy means special cases and default objects are allowed only as
  explicit domain semantics, not as defensive soft defaults.

- **Bridge-Burning Policies** (see [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md#policy-registry)) are HARD, non-negotiable rules that eliminate validation-evasion pathways (such as runtime defaults, mocks, and fallbacks) and must be strictly followed.

Every name reveals intent.
Every function tells a story.
Every class has a single purpose.
The goal isn't just working code—it's code that others can understand quickly, modify
safely, and extend confidently.

> “Clean code always looks like it was written by someone who cares.”
> — Michael Feathers

> “You know you are working on clean code when each routine turns out to be pretty much
> what you expected.” — Ward Cunningham

**The Boy Scout Rule:** Leave the code cleaner than you found it.
Every commit should improve quality, even if just slightly.
Small improvements compound.

## Chapter References

This skill provides an overview with quick references.
For detailed guidance with examples, see the chapter files:

- `names.md` - Meaningful Names (intention-revealing, searchable,
  pronounceable)

- `functions.md` - Functions (small, do one thing, few arguments)

- `comments.md` - Comments (why to avoid, what’s acceptable)

- `objects-and-data.md` - Objects and Data Structures (Law of Demeter, DTOs)

- `error-handling.md` - Error Handling (exceptions, null handling, Special Case
  Pattern)

- `tests.md` - Unit Tests (TDD, F.I.R.S.T., clean tests)

- `classes.md` - Classes (SRP, cohesion, OCP, DIP)

- `smells-and-heuristics.md` - Complete code smells reference (66 smells with
  explanations)

## Quick Reference: Names

Names should reveal intent and be searchable.

| Rule | Bad | Good |
| --- | --- | --- |
| Reveal intent | `d` | `elapsedTimeInDays` |
| Avoid disinformation | `accountList` (not a List) | `accounts` |
| Make distinctions | `a1, a2` | `source, destination` |
| Pronounceable | `genymdhms` | `generationTimestamp` |
| Searchable | `7` | `MAX_CLASSES_PER_STUDENT` |
| Classes = nouns | `Process` | `Customer`, `Account` |
| Methods = verbs | `data` | `postPayment()`, `save()` |

**Avoid:** `Manager`, `Processor`, `Data`, `Info` in class names—they hint at unclear
responsibilities.

**Key insight:** If you need a comment to explain what a variable is, rename it instead.

## Quick Reference: Functions

### Size and Scope

- **Ideal:** 4-10 lines, rarely over 20

- **Indent level:** Never more than one or two

- **Do one thing** — if you can extract another function with a non-restating name, it’s
  doing too much

### Arguments

| Count | Guidance |
| --- | --- |
| 0 | Best |
| 1 | Good |
| 2 | Acceptable |
| 3+ | Avoid—wrap in object |

**Flag arguments (booleans) are ugly.** They proclaim the function does two things.
Split it:

```python
# Bad
def render(is_suite: bool): ...

# Good
def render_for_suite(): ...
def render_for_single_test(): ...
```

### Key Rules

- **Command Query Separation:** Do something OR answer something, not both

- **No side effects:** If `checkPassword()` also initializes a session, it lies

- **Prefer exceptions to error codes:** Separates happy path from error handling

- **Extract try/catch blocks:** Error handling is one thing

## Quick Reference: Comments

> Comments are, at best, a necessary evil.
> The proper use of comments is to compensate for our failure to express ourselves in
> code.

### Delete These Comments

- **Redundant** — restating what code says

- **Journal/changelog** — use git

- **Commented-out code** — an abomination, git remembers

- **Noise** — `// default constructor`, `// increment i`

- **Closing brace** — `} // end if` means too much nesting

### Acceptable Comments

- Legal notices

- Explanation of intent (why, not what)

- Warning of consequences (`// takes 30 minutes`)

- TODO (but clean them up)

- Clarifying external library behavior

**The Rule:** When you feel the urge to comment, first try to refactor the code so the
comment would be unnecessary.

## Quick Reference: Error Handling

**Error handling is important, but if it obscures logic, it’s wrong.**

| Rule | Details |
| --- | --- |
| Use exceptions over return codes | Separates algorithm from error handling |
| Provide context | Include operation that failed and type of failure |
| Wrap third-party APIs | Defines owned semantic boundary, centralizes contract validation |
| Use Special Case Pattern | Return object that handles special case (empty list, default values) |
| **Don’t return null** | Creates work, invites NullPointerException |
| **Don’t pass null** | Worse than returning null—forbid it by default |

```python
# Bad - null checks everywhere
if employees is not None:
    for e in employees:
        total += e.pay

# Good - return empty collection instead of null
for e in get_employees():  # Returns [] if none
    total += e.pay
```

## Quick Reference: Classes

### Single Responsibility Principle (SRP)

> A class should have one, and only one, reason to change.

**Tests:**

- Can you derive a concise name?
  (Avoid `Manager`, `Processor`, `Super`)

- Can you describe it in 25 words without “if,” "and," “or,” "but"?

### Cohesion

Methods should use the class’s instance variables.
When methods cluster around certain variables but not others, the class should be split.

### Open-Closed Principle (OCP)

Classes should be open for extension but closed for modification.
Add new behavior via subclassing, not modifying existing code.

### Dependency Inversion Principle (DIP)

Depend on abstractions, not concrete details.
Inject dependencies for explicit dependency flow and boundary control.

```python
# Bad - can't test without network
class Portfolio:
    def __init__(self):
        self.exchange = TokyoStockExchange()

# Good - explicit dependency flow, boundary control
class Portfolio:
    def __init__(self, exchange: StockExchange):
        self.exchange = exchange
```

## Quick Reference: Tests

### The Three Laws of TDD

1. Don’t write production code until you have a failing test

2. Don’t write more test than sufficient to fail

3. Don’t write more production code than sufficient to pass

### F.I.R.S.T. Principles

- **Fast** — Run quickly so you run them often

- **Independent** — Don’t depend on each other

- **Repeatable** — Same result in any environment

- **Self-Validating** — Boolean output (pass/fail)

- **Timely** — Written just before production code

### Clean Tests

- **Readability** is paramount

- Use **BUILD-OPERATE-CHECK** pattern

- Create domain-specific testing language

- **One concept per test** (not necessarily one assert)

**Warning:** Test code is just as important as production code.
If you let tests rot, your code will rot too.

## Objects vs Data Structures

| Concept | Hides | Exposes | Easy to add … |
| --- | --- | --- | --- |
| Objects | Data | Functions | New types |
| Data Structures | Nothing | Data | New functions |

**The idea that everything is an object is a myth.** Sometimes you want simple data
structures with procedures operating on them.

### Law of Demeter

A method should only call methods of:

- The class itself

- Objects it creates

- Objects passed as arguments

- Objects held in instance variables

**Don’t** call methods on objects returned by allowed functions (train wrecks):

```python
# Bad
output_dir = ctxt.get_options().get_scratch_dir().get_absolute_path()

# Good - tell the object to do the work
bos = ctxt.create_scratch_file_stream(class_file_name)
```

## The Most Critical Smells

From Chapter 17’s comprehensive list, these are the most important:

### G5: Duplication

**The root of all evil in software.** Every duplication is a missed abstraction
opportunity:

- Identical code → extract to function

- Repeated switch/if-else → polymorphism

- Similar algorithms → Template Method or Strategy pattern

### G30: Functions Should Do One Thing

If you can extract another function from it, the original was doing more than one thing.

### N1: Choose Descriptive Names

Names are 90% of what makes code readable.
Take time to choose wisely.

### F1: Too Many Arguments

Zero is best, then one, two, three.
More requires justification.

### F3: Flag Arguments

Boolean parameters mean the function does two things.
Split it.

### G9: Dead Code

Code that isn’t executed.
Delete it—version control remembers.

### G11: Inconsistency

If you do something one way, do all similar things the same way.

### C5: Commented-Out Code

An abomination. Delete it immediately.

## The Craft

> “Writing clean code requires the disciplined use of a myriad little techniques applied
> through a painstakingly acquired sense of 'cleanliness.'
> The code-sense is the key.”

Clean code isn’t written by following rules mechanically.
It comes from values that drive disciplines—caring about craft, respecting readers of
your code, and taking pride in professional work.

**How do you write clean code?** First drafts are clumsy—long functions, nested loops,
arbitrary names, duplication.
You refine: break out functions, change names, eliminate duplication, shrink methods.
Nobody writes clean code from the start.

Getting software to work and making it clean are different activities.
Most of us have limited room in our heads, so we focus on getting code to work first.
**The problem is that too many of us think we are done once the program works.** We fail
to switch to organization and cleanliness.
We move on to the next problem rather than going back and breaking overstuffed classes
into decoupled units.

Don’t. Go back. Clean it up.
Leave it better than you found it.

## Cross-References

- **anti-slop → deepening** — This skill's SRP and DIP guidance overlaps with the deepening vocabulary in `anti-slop/references/deepening-vocabulary.md`. Where this skill says "classes should be small" and "depend on abstractions," deepening gives precise language: a module should be **deep** (high leverage at the interface, high locality in the implementation), and seams should only be introduced where there are at least two adapters. The deletion test is a concrete check for SRP: if deleting the class makes complexity vanish, it was a pass-through, not a real responsibility.

- **anti-slop → deepening** — `anti-slop/references/deepening.md` provides the process for turning shallow modules (wide interfaces, pass-throughs) into deep ones. When this skill identifies cohesion breakdown or SRP violations, the deepening reference tells you how to consolidate them: classify dependencies (in-process, local-substitutable, ports & adapters, mock), place seams, and test through the deepened interface.

- **thermo-nuclear-code-quality-review** — For aggressive simplification that goes beyond "clean code" into restructuring, load thermo-nuclear alongside this skill.

- **policy-index → Bridge-Burning Policies** — Modern development requires adhering strictly to the [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md#policy-registry) defined in `policy-index/SKILL.md`. These represent non-negotiable constraints to prevent agent evasion (such as runtime defaults, fallbacks, and mocks). For a detailed catalog of code constructs that violate these policies, see the [Bridge-Burning Red Flags Catalog](file:///home/dzack/ai/opencode/skills/policy-index/references/red-flags.md) and the [Runtime Control-Flow Red Flags Catalog](file:///home/dzack/ai/opencode/skills/policy-index/references/runtime-control-flow.md).
