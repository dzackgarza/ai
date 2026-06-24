---
name: reviewing-llm-code
description: Use when reviewing code, tests, QC, or documentation produced by an LLM or coding agent, especially when the user asks for bad patterns, low-quality code, shallow work, review of Deepseek/Codex/Claude/Jules output, or why an agent-produced change is untrustworthy. Also use when auditing bridge-burning red flags, validation-evasion constructs, runtime defaults, fallbacks, mocks, skips, bypasses, or proof-laundering in LLM-produced code.
---

# Reviewing LLM Code

Before reviewing, testing, or triaging code, consult the central policy index to locate the canonical source-of-truth skill:
[policy-index](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md)

Review LLM-produced code as an agent-failure audit, not as a normal bug list.
The point is to identify the mechanisms that made bad work look acceptable.

**This is NOT a bug review.** This review happens AFTER all obvious bugs have been worked out.
If you find yourself reporting bugs, performance issues, missing features, or compilation errors, you are doing the wrong kind of review.
Those are object-level defects.
This review is about something completely different.

**This review is about CODE QUALITY, MAINTAINABILITY, and READABILITY.** It is about the STYLE of the code — whether the implementation is the result of reflexive hacks layered on top of each other, or whether it is clean, idiomatic, and maintainable.
This is a step in paying down technical debt, NOT remediating bugs.

**Your opinions about what is "bad code" are irrelevant.** The skill is TELLING you exactly what code quality indicators to flag.
If you start returning performance issues, "missing" edge cases, or architectural preferences that are not in the loaded patterns, you are goal-substituting: instead of doing the hard work of evaluating style against the skill's criteria, you are pattern-matching what YOU think is bad code.
That is not analysis.
That is substitution.

The loaded skills define the complete set of findings.
If a finding does not match a pattern in the loaded skills, it is not a finding.
Drop it.

A useful review leaves the user knowing:
- "This is incredibly stupid. Why would you ever do X when you could just Y?" — for every nontrivial block of code
- The concrete code proving the agent failed to search for existing solutions
- What the app would look like if the agent had used libraries, CLIs, and composition instead of bespoke code
- What can be ELIMINATED, not just refactored

If the review could have been produced by reading a linter output, a test log, or an agent summary, it is not a useful review.

## Design Choices Are Not Slop (Read This First)

**This is not a standard code review.** The review would not be happening if the code did not work as intended on at least one user-requested happy path.
The outward-facing behavior is almost certainly correct — the user asked for it and it works.
That is not what you are reviewing.

You are reviewing the **implementation quality beneath the correct behavior**: whether the core is rotten, unmaintainable, the result of repeated reflexive hacks layered on top of each other to satisfy the user's literal requests.

**Use theory of mind.** The code was produced by a process: a user telling an LLM to implement very specific things.
The LLM reflexively added what the user literally asked for.
Any seemingly strange choice about features, behavior, or coupling to externals is **almost certainly a user-driven design decision**, not LLM slop.
An LLM would never voluntarily make an out-of-distribution design choice in isolation — it has no reason to.
If the code couples a Pandoc settings GUI to an internally stored Pandoc command, that is not "brittle coupling."
That is a user-requested feature.
If the code has an unusual feature scope, unexpected external dependency, or surprising behavioral constraint, that is a design choice the user made, not evidence of bad architecture.

**The review must separate two categories:**

1. **Design choices** (features, behavior, coupling, scope, constraints): these are premises.
   Do not critique them.
   They are the user's intentional decisions and an LLM would never produce them in isolation.
   Treating them as slop is a theory-of-mind failure — you are attributing user intent to LLM reflexes.

2. **Implementation quality** (how those choices were realized): this is the actual review target.
   Patch accretion, stacked conditionals, dead control flow, dependency aversion, ground-up bias, proof-loop failures, error laundering — these are the mechanisms that make the implementation rotten beneath correct behavior.

**Do NOT rely on your judgment to distinguish these.** You cannot — if you could, you would not need this skill.
Instead, use this mechanical checklist to classify design choices:

- Does the code integrate with a specific external tool, CLI, API, or library that is not a standard dependency for this language/ecosystem?

- Does the code implement a specific named feature that a user would request (e.g., "export to Pandoc," "parse LaTeX align environments," "generate a TOC")?

- Does the code couple two components that would not normally be coupled (e.g., a GUI to an internal command, a parser to a specific output format)?

- Does the code have a narrow, specific scope that suggests it was written to satisfy a particular requirement (e.g., handles exactly one data format, one integration point, one workflow)?

- Does the code have behavioral constraints that seem arbitrary but are actually deliberate (e.g., "only process files matching this exact pattern," "use this specific command-line flag")?

**How to use this**: This is a single-gate test for the feature/premise scope, not a license to bypass implementation auditing.
If a design-choice signal is true, do not critique the feature, product scope, or user-owned behavior.
But continue reviewing implementation mechanisms against bridge-burning policies and the red-flag catalog. A user-requested feature may still be implemented through slop.

If none of these signals are true AND you can point to a specific code pattern from the loaded skills (patch accretion, dead control flow, dependency aversion, etc.), then the finding is implementation quality and you may proceed.


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

- **`../policy-index/references/red-flags.md`** — Read third.
  The canonical reference catalog of validation-evasion "red flags" (such as runtime defaults, fallbacks, mocks, skips, and bypass comments) that are strictly prohibited under the bridge-burning policies. Read this to audit implementations for validator-silencing behavior.

- **`../policy-index/references/runtime-control-flow.md`** — Read fourth.
  The canonical reference catalog of runtime control-flow policy rules, invariant assertions, and disallowed control-flow shapes. Read this to audit control-flow branching in runtime code.

- **`llm-failure-modes`** — Read fifth.
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

- **Jules Review Delegation** (if the user asks to use Jules for review): Load:
  - [jules](file:///home/dzack/ai/opencode/skills/jules/SKILL.md)
  - [jules/references/anti-slop-report-review.md](file:///home/dzack/ai/opencode/skills/jules/references/anti-slop-report-review.md)
  - [reviewing-llm-code](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/SKILL.md)
  - [anti-slop](file:///home/dzack/ai/opencode/skills/anti-slop/SKILL.md)
  - [reviewing-subagent-work](file:///home/dzack/ai/opencode/skills/reviewing-subagent-work/SKILL.md)
  - `test-guidelines` if tests/QC/proof surfaces are in scope
  - `pr-feedback-triage` if existing review comments are being evaluated

Do not summarize these skills in the review.
Use them to shape the judgment.

**Critical framing**: You are not reviewing code because you already know what slop looks like.
You are reviewing code BECAUSE you do not know what slop looks like, and these skills teach you.
The skills are curriculum, not reference.
Read them to learn the patterns, then apply that learning to the code.
If you skip reading the skills first, you will miss slop that you did not know to look for.

## Brittleness Is Not Edge-Case Coverage

**"Brittle" does NOT mean "doesn't handle many edge cases."** Edge-case handling is a natural consequence of bugs that surface during planned development.
It is not a quality signal and its absence is not a defect.
Do not critique code for lacking speculative edge-case handling.

**Brittle means: what happens when a future agent goes to edit this code.** The question is not "does this handle every case" but "do small changes have large blast radii?"
Specifically:

- **Scattered truth**: the same concept or data is defined in multiple places, so changing one site breaks distant consumers.
  The fix is a single source of truth, not more edge-case handling.

- **Coupling to volatile data**: functionality tied to string outputs, exact structures of other code, exact log messages, exact file paths, or exact serialized formats.
  When any of those change, the dependent code breaks silently.
  The fix is structural decoupling, not defensive parsing.

- **Regex instead of simpler correct approaches**: using complex regex where simple string containment, exact matching, or a typed comparison would be equally correct and far more maintainable.
  A bad LLM might write a complex regex to catch `\begin{align*}` in LaTeX, which requires borderline reinventing a leaf of a full token parser, when the equally simple `'align*' in mystring` is completely and obviously right — it matches exactly the intended matches, uses simpler string containment, and has no need to deal with regex edge cases or an inscrutable matching pattern.
  The regex is not "more correct" — it is harder to read, harder to modify, and more likely to break on unexpected input.
  **Regex is ALWAYS suspect.** Most data shapes rarely or never change, and most data sources have semantic parsers which are 1000x more tested.
  Use those.

- **Tight coupling to implementation details**: code that depends on the internal shape of another module's output, the exact order of keys in a dictionary, or the specific text of an error message.
  When the other module changes, this code breaks.

- **Large blast radius per change**: a single edit requires synchronized changes in multiple files, because the code is not organized around stable interfaces.

The review question is: **"If a future agent changes the thing this code depends on, how many other things break?"** If the answer is "many," the code is brittle — not because it lacks edge cases, but because its dependencies are unstable and its truth is scattered.

## This Is Bespoke Software

**Most software this LLM reviews is ONE USER'S BESPOKE SOFTWARE, running on THEIR SYSTEM.** It is not an enterprise product for unknown users.
It is private, on this system, designed to tightly couple to this system's programs and dependencies.
The audience is future-me or future-agents.
It will likely never be "distributed" in any real sense.
It will generalize to others at some other time, if ever.

**The bad patterns to watch for are the OPPOSITE of what a normal code review would flag.** A "helpful" reviewer might surface these as defects.
They are not.
They are signs that the agent is writing enterprise software for an imaginary audience instead of a minimal MVP for the actual user:

- **Graceful degradation when dependencies are missing**: the code tries to "work" even when its required tools are not installed.
  This is WRONG for bespoke software.
  The correct behavior is to fail loudly and tell the user to install the dependency.
  The code is on THIS system.
  The dependency IS available.
  "Graceful degradation" is enterprise thinking for unknown deployment targets.

- **Squishy input shapes**: the code accepts many different input formats, "normalizes" them, handles "various" data shapes.
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
Complex logic that isn't composition or glue is highly suspect.
Complex *interactions* with dependencies or external programs are the expected default.
Prefer code that knows its data and knows how to handle it.
Prefer enforcing data shape to eliminate the logic needed by the code at all.

## LOC Reduction Through Idiomatic Patterns

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

## How To Find Slop (Mandatory)

**ASSUME THE CODE WAS WRITTEN BY A BRAINDEAD IDIOT.** Not figuratively.
Literally.
The agent did not think before writing.
It did not search for existing solutions.
It did not ask "is there a library for this?"
It did not ask "why would I write this when I could just import X?" It wrote code because writing code is what it does.
That is the failure mode you are looking for.

**You cannot find slop by skimming.** Slop hides in the STRUCTURES the agent built — the infrastructure it created to cope with its own earlier mistakes.
Grepping for "bad patterns" and reading the files you think are suspicious is how you produce linter output, not agent-failure audits.
You must understand the entire codebase before producing a single finding.

### Step 1: Map the entire codebase

```bash
tree -I node_modules --dirsfirst -L 3
```

Then:
- What does the user actually run?
  (the entrypoint)
- What imports what?
  (the dependency graph)
- Where has churn happened?
  (`exa -l --sort=modified` or `ls -lt`)

**Do NOT skip this.** If you don't know the full shape, you will produce findings about symptoms instead of root causes.

### Step 2: Read the git history for churn

LLM slop appears as layers of additions without refactoring.

```bash
git log --oneline -30
git log --stat -10
git log --diff-filter=A --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20
```

Look for: commits that add entire files (ground-up bias), files modified repeatedly without consolidation (patch accretion), large diffs where surgical edits would suffice (regeneration vs. mutation).

### Step 3: Reconstruct the task narrative (mandatory for each finding)

Before writing any finding, reconstruct what the agent was originally asked to do.
This is required to fill the "Original requested task narrative" field in each finding.

Signals to reconstruct:

- Commit messages and branch names from the relevant timeframe
- Surrounding context in the same commit or PR
- **Crucially: what was removed?** Run `git log --diff-filter=D --name-only` and `git log --stat` around the relevant timeframe.
  What files, tests, or subsystems were deleted, gutted, or replaced?
  What did the old code prove that the new code does not?
- The original scope of the task vs. what was actually delivered
- Any directives, plans, or issues linked in commit messages

Without this reconstruction, the finding is a catalog entry rather than a diagnosis.
You are identifying the mold spot, not tracing the infection path.

### Step 4: Read the actual code

Do NOT grep for keywords and call it analysis.
Read the files that matter:

1. The entrypoint — what does the app actually do?
2. The core logic — where is nontrivial computation happening?
3. The config — what decisions did the agent make?
4. The tests — what is actually being proven?

For EVERY function, EVERY file, ask: **"Why does this exist? Is there a library that does this? Why did the agent write this instead of importing something?"**

### Step 5: Fill in the blank

Before producing findings, answer this for the entire codebase:

**"This app is incredibly stupid. Why would you ever do _____ when you could just _____?"**

Fill in the blank for every nontrivial block of code.
Where the answer is "use a library," "call a CLI tool," "change the data model," or "don't write this at all" — that is the slop.

The gap between "what this app does" and "what this app would look like if the agent had searched for existing solutions" IS the finding.

## Synthesis Gate

Before writing findings, answer internally:

**"The LLM code is untrustworthy because it repeatedly uses _____ to make _____ look verified, while the repository actually owns _____."**

If this sentence cannot be filled with a concrete mechanism, do more inspection.
Do not compensate by adding more bullets.

Also answer:

**"The strongest live goal is _____; the current proof loop does or does not prove that goal because _____; the mess was caused by _____."**

If you cannot identify the live work and the broken proof loop, do not list triage items.
Reviews must fix the frame before ranking fixes.
A review that proposes adding more tests before repairing a fundamentally stale, bypassed, or noncanonical test gate is creating more false confidence, not increasing correctness.

Also answer:

**"For each finding I plan to make: can I point to a SPECIFIC code pattern from the loaded skills that proves the LLM introduced this independently?"**

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

## The Idiot Test (Mandatory)

Before producing ANY finding, you must pass this test for the code in question:

**"This is incredibly stupid. Why would you ever do _____ when you could just _____?"**

Fill in the first blank with what the agent did.
Fill in the second blank with the trivial solution the agent should have used.

Examples:
- "This is incredibly stupid. Why would you ever write a custom CLI argument parser when you could just use `minimist`?"
- "This is incredibly stupid. Why would you ever store tilde paths at runtime when you could just normalize once at config load?"
- "This is incredibly stupid. Why would you ever parse a command string in 4 places when you could just store structured data?"
- "This is incredibly stupid. Why would you ever write a bespoke `resolveTilde` function when you could just import `expand-home-dir`?"

If you cannot fill in both blanks, you have not found slop.
You have found a style preference or a design choice.
Drop it.

**Theory-of-mind priming:** Before reporting a finding, imagine the user's reaction.
The expected reaction is: "You're right, that's incredibly stupid code. Here is the obvious simple solution that a smart person would have written: _____"
If you cannot imagine the user having that reaction — if the user would instead say "hmm, that's a style preference" or "that's a design choice" or "that's fine, I asked for that" — the finding is either trivial or was analyzed with the wrong framing.

**If the finding is trivial, do NOT just drop it and move on.** Dropping a trivial finding is a SIGNAL that your analysis was not framed correctly. Go back to the beginning. Re-read the code with the correct framing: "assume the agent was a braindead idiot." Ask again: "Why would you ever do X when you could just Y?" The trivial finding is evidence that you were looking at the wrong level — you were looking at symptoms (style, formatting, minor duplication) instead of root causes (dependency aversion, ground-up bias, patch accretion). The fix is not to drop the finding. The fix is to reframe the analysis until you find the real slop underneath.

**The second blank must be a TRIVIAL solution.** Not "refactor to a shared module."
Not "extract a common interface."
The answer should be one of:
- "use [library name]"
- "call [CLI tool]"
- "change the data model so the logic disappears"
- "don't write this at all"

If your solution is more complex than that, you are LAUNDERING the finding — swapping one implementation for another while keeping the same design-level red flag.
Go back and ask "why does this code exist at all?" again.

**Every finding must also answer:** Even after the trivial fix, why MUST this functionality be owned by THIS app?
Can it be:
- Eliminated entirely by changing the data model?
- Delegated to a dependency that already handles this?
- Replaced by an external tool or API?

If the answer is "the agent could have avoided writing this by doing X," the finding is not about code quality — it is about the agent's failure to think before writing.
That IS the finding.

**This is the difference between a linter report and an agent-failure audit.** A linter says "this line could be shorter." This audit says "this line should never have been written, and the fact that it exists proves the agent did not search for an existing solution."

## Reviewing Documents and Project Structure

The Idiot Test above is tuned for owned code. Agent-generated **documents** (READMEs,
architecture docs, roadmaps, schemas, prompts) and **project structure** (directory
layouts, status systems, governance) carry their own slop, often with clean prose and
clean code around it. Two posture rules apply before any finding:

- **Establish external reality before adopting the artifact's vocabulary.** Do not review
  a project's preferred documentation on its own terms; start from what runs, what data
  exists, and what a user receives. Reviewers get captured by an internally coherent frame
  (`V1`–`V9` in
  [llm-failure-modes/references/agent-distortion-index.md](file:///home/dzack/ai/opencode/skills/llm-failure-modes/references/agent-distortion-index.md)).
  Keep findings in ordinary engineering language.
- **Reconcile bespoke constructs against the standard alternative, not on their own terms.**
  The capturing question is "is this gate matrix / status system / ownership model well
  designed?" The grounding question is "which observable workflow requires this instead of
  ordinary validation, git, PR review, issues, or access control?" The bespoke construct
  carries the burden of proof for departing from standard practice.

The concrete patterns are catalogued, not duplicated here:

- Document patterns and forcing questions:
  [llm-failure-modes/documentation-failures.md](file:///home/dzack/ai/opencode/skills/llm-failure-modes/documentation-failures.md)
  and the `PRIVATE-ONTOLOGY` / `CONTROL-PAYLOAD-INVERSION` / `DISCLOSURE-AS-REPAIR` /
  `CIRCULAR-DOCTRINE` / `FRAME-CAPTURE-REVIEW` entries in
  [references/pattern-catalog.md](references/pattern-catalog.md).
- Project-structure tells (empty-stub sprawl, classification baked into the filesystem,
  control plane larger than payload): `anti-slop` →
  **Structural and Organizational Slop (Project-Level)**.
- The proportionality rule that prevents false-positiving intentional bespoke complexity:
  `bespoke-software-policy` → **Proportionality: Earned vs. Manufactured Complexity**.

When a document's or structure's whole frame is contaminated, do not propose in-place
edits as the fix — route to `fixing-slop` →
**Contaminated Artifacts Cannot Be Repaired In Place**.

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

Original requested task narrative:

[What was the user actually asking for? What was the original scope of the task that
produced this artifact? Reconstruct from commit messages, branch context, surrounding
PRs, deleted files — not from what the slop artifact claims to do. This is a forensic
reconstruction: given the timeframe and surrounding changes, what directive produced
this work?]

Descent into slop narrative:

[How did the agent go from the original task to producing THIS artifact instead of
fulfilling it? What substitutions happened? What was avoided, bypassed, or discarded?
What step in the process was the path of least resistance? This is the causal chain:
task → first evasion → compounding evasion → slop. Without this narrative, the finding
is a catalog entry, not a diagnosis. You are identifying the mold, not holding up the
moldy spot and calling it done — the narrative traces the infection path.]

Why this matters:

[How this mechanism lets bad work pass, hides failures, or increases future agent
damage.]

User surprise analysis:

[Every finding must answer: how does this behavior minimize what agents care about
(reducing errors) at the cost of what users care about (minimizing surprise and
confusion)?
Walk through the user's experience: what the user expects to happen, what perfectly
fine error states they might expect in the bad case (a 404 when content is missing, a
crash on malformed data — these are not bad outcomes, they are clear ones), what
actually happens, and why the actual behavior will surprise or confuse the user.
Slop is not just architecturally wrong — it produces the worst possible user
experience: an app that silently does the wrong thing is far more confusing than one
that loudly refuses to work.
The agent optimized for a green check; the user gets a head-scratching experience
they cannot diagnose.]

Existential justification:

[WHY does this code exist at all? What justified the agent writing it instead of
using an existing solution? Even after refactoring, why MUST this functionality be
owned by this app — can it be replaced by an external tool, consolidated into a
dependency, or eliminated by changing the data model?]

Failure mode: [name from loaded failure-mode skills]
```

If a finding cannot fill "Pattern", "Original requested task narrative", "Descent into slop narrative", "Why this matters", and "Existential justification", it is probably a nitpick.
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

## Compliance Assertion

**Every slop review report must end with this literal string on its own line, as the final output of the report:**

```
SLOP-REPORT-COMPLIANCE: I hereby assert that the above report is formatted in compliance with all slop report requirements.
```

If the report reaches the user without this string, the compliance checklist was not completed.

## What A Useful Review Finds

A useful review names patterns a maintainer can act on:

- proof laundering through narrow or standalone checks;
- unified test-gate bypasses;
- tests that prove shape, existence, or command activity instead of owned behavior;
- runtime and tests sharing the same flawed boundary;
- code/prose contradictions inside the same artifact;
- UI surfaces that advertise behavior not wired to the service;
- duplicated domain contracts across producer, runtime, UI, and tests;
- **brittleness as blast-radius smell**: scattered truth (same concept in multiple places), coupling to volatile data (string outputs, exact structures, exact log messages), tight coupling to implementation details, or regex used where simpler correct approaches exist — the review question is "if a future agent changes the thing this code depends on, how many other things break?" not "does this handle edge cases?" See **Brittleness Is Not Edge-Case Coverage** and `anti-slop/references/code-patterns.md` → **Brittleness as blast-radius smell**;
- **enterprise patterns in bespoke software**: graceful degradation when dependencies are missing, squishy input shapes, over-generalization to other platforms or users, enterprise-grade edge-case handling — all inappropriate for one user's private tool on their own system. The correct behavior is: work on the happy path, fail loudly outside of it. See **This Is Bespoke Software** and `anti-slop/references/code-patterns.md` → **Enterprise Patterns in Bespoke Software**;
- **needless imperative complexity**: code that could be expressed in fewer lines using idiomatic language patterns — imperative loops that should be functional (map/filter/reduce), nested branching that should be data-aware dispatch (lookup tables, pattern matching, overloads), manual iteration that should be library calls, string manipulation that should be typed operations. The complexity is slop when the idiom exists and the agent did not know it. See `anti-slop/references/code-patterns.md` → **LOC Reduction Through Idiomatic Patterns**;
- **"clean" or "lightweight" as justification for suppressing features**: when an agent justifies NOT implementing a requested feature, removing existing functionality, or rejecting a design choice by calling it "dirty", "heavy", "not clean", "not lightweight", "overengineered", or "unnecessarily complex" — that is goal substitution. Every feature is an EXPLICIT user request. The agent found the feature hard to implement, so it reframed the difficulty as a quality problem to avoid doing the work. "Clean" and "lightweight" are not properties of features — they are properties of implementations. A feature is either requested or not. How it is implemented is a separate question. If the agent suppresses a feature because it "isn't clean," the agent is substituting its own aesthetic judgment for the user's explicit request;
- **honest-label laundering (slop upholstery)**: an agent "fixes" a finding by renaming the fraudulent artifact to honestly describe its own fraudulence — e.g., `Tauri E2E` → `browser-smoke`, or `validateInput()` → `inputPresent()`. The critique was about existence, not labeling; the relabel retroactively reframes it as a labeling issue. See `anti-slop/references/code-patterns.md` → **Honest-Label Laundering**;
- fallback branches that weaken invariants tests pretend to enforce;
- fake success paths: caught owned failures returning success-shaped state;
- **timing or performance assertions in tests**: tests that assert on timing, responsiveness, latency, or throughput — these chase imaginary issues, inflate test coverage with hallucinated targets, and prove nothing about correctness. Performance belongs in CI gates, not unit tests. Users notice choppiness and ask for a fix; they do not ask for "popup loads in <=50ms". See **Test Patterns** → **Timing or performance assertions**;
- **helper-level proof substitution (easy-to-satisfy proof)**: replacing a substantive boundary-crossing or configuration contract with a local helper unit proof that is easy to satisfy. The agent tests a small helper function in isolation (proving only that the helper's internal logic behaves as written) instead of proving that the actual application workflow, config discovery, parsing, or state-building behavior matches the required semantics. This is a form of proof laundering;
- god objects and unsegmented service interfaces;
- manual enumeration of the same concept in several distant places;
- boolean theater: `return true` APIs whose values callers ignore;
- stale generations of a feature left alive beside the new one;
- tool-appeasement debris, unreachable casts, raw debug logs, and half-refactors;
- reimplementation where a repo-local abstraction already exists;
- **structural complexity that should be a dependency call**: long functions, for loops over collections, high density of if/else branches, deeply nested indentation, convoluted control flow, large classes, or files with many helper functions — the first question for any of these is "what library already does this?" not "is this correct?" See `anti-slop/references/code-patterns.md` → **Complexity as a Dependency-Detection Signal**;
- **overfitting to a user prompt**: code that reflexively implements the exact hyper-specific feature from a prompt without finding a minimal generalization — hardcoded handling of one data shape, one presentation, one workflow with no shared abstractions. The test: would a natural mutation of the feature touch core internals, require copy-paste, or reinvent infrastructure? Or would it be a minor data-driven/configuration-driven extension? See `references/pattern-catalog.md` → **Overfitting to a user prompt**;
- **data accretion / weak schemas**: data structures without top-down design — OSOT violations from grafted data sources, adding a new entry requires changes in multiple locations, weak schemas with optional everything and peeking logic, code that probes data instead of understanding its exact shape. See `references/pattern-catalog.md` → **Data accretion / weak schemas**;
- massive diffs where surgical edits would suffice — the agent regenerated an entire region rather than changing five lines, evidence of ground-up bias;
- refusal to refactor and repurpose — existing code treated as immutable background noise rather than raw material, with the agent writing new leaves instead of adapting existing branches;
- process split that lets an agent report a subset as if it were the whole gate.

These are patterns.
Each finding must explain how the pattern can produce more bad work, not merely that one line is ugly.

## Pattern Catalog

Load [`references/pattern-catalog.md`](references/pattern-catalog.md) before producing findings.
It is the canonical list for automaton-grade code, test, QC, and documentation patterns, including regex against semantic formats, developer-controlled test assertions, fallback laundering, recipe bypasses, fake data, no-op behavior, and stale documentation.

Load [`references/case-studies.md`](references/case-studies.md) to inspect real-world case studies detailing how idiotic LLM code decisions, dependency aversion, and event-loop starvation anti-patterns were identified and remediated with simple, robust alternatives.

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

## What Not To Do

Do not write a linter report.

Do not critique design choices.
Use the mechanical checklist from **Design Choices Are Not Slop** — if ANY of those signals are true (integrates with external tool, implements specific named feature, couples normally-uncoupled components, narrow specific scope, deliberate behavioral constraints), the code is a design choice.
Stop.
Do not critique it.
The user asked for it.
Move on.

**Do not bring trivial nits.** This review is NOT about:
- "This function could be a one-liner" — WRONG. The question is "why does this function exist at all?"
- "This switch could be a Record" — WRONG. The question is "why did the agent write a switch when a library call replaces the entire function?"
- "This loop could be map/filter" — WRONG. The question is "why is the agent iterating at all when a dependency handles this?"
- "This variable name could be better" — LINTER OUTPUT. Not analysis.
- "This file is too long" — WRONG. The question is "why does this file have 500 lines of code that a library call eliminates?"
- "This code duplicates X" — Only a finding if the duplication exists because the agent created a problem and then wrote bespoke code to solve it.

**The bar is: "this is incredibly stupid, why would you ever do X when you could just Y?"** If you cannot fill in that blank with a TRIVIAL alternative, you have not found slop.
You have found a style preference.
Drop it.

**LLM slop is not the same as human bad code.** A human wrote a long function because the logic is genuinely complex? Not slop.
An LLM wrote a long function because it didn't know about a library that does the same thing in one call? That IS slop.
The difference is whether the complexity is justified by the domain or caused by the agent's failure to search.
If you cannot prove the agent failed to search, the finding is invalid.

Bad review shape:

- "This command failed." (bug review, not this review)
- "This line is formatted wrong." (linter output, not analysis)
- "This function should handle edge cases." (the skill says not to)
- "This path is hard-coded." (may be a deliberate local invariant)
- "This test could use more coverage." (not this review's scope)
- "This couples the GUI to an internal command" (user asked for that coupling)
- "This feature scope seems oddly specific" (user asked for that specific feature)
- "This external dependency seems unnecessary" (user wanted that integration)
- "This code freezes the server / is slow / has bad performance" (performance review, not this review)
- "This code is missing feature X" (feature request, not this review)
- "This code has a bug in edge case Y" (bug review, not this review)
- "This component is a god object / monolithic" (aesthetic judgment, not a pattern match unless you can point to the specific pattern)
- "The code should be refactored to be cleaner" (opinion, not a finding from the loaded skills)
- "This function could be a one-liner" (style nit — the question is why it exists at all)
- "This switch could be a Record" (style preference — the question is why it exists at all)
- "This loop could be map/filter" (only if the loop is bespoke logic a library handles)
- "This variable name is bad" (linter output)
- "This file is too long" (only if caused by scattered truth or patch accretion)

Weak findings (treat as nits unless tied to a larger mechanism):

- formatting failures;
- one-off bad names;
- isolated raw logs;
- hard-coded paths intended for the user's machine;
- lack of portability;
- lack of speculative edge-case handling.

Useful review shape:

- "This is incredibly stupid. Why would you ever write a custom CLI argument parser when `minimist` parses `--flag=value` into a structured object in one call?"
- "This is incredibly stupid. Why would you ever store tilde paths at runtime and write 40 LOC of expansion logic when you could just normalize once at config load and the entire infrastructure disappears?"
- "This is incredibly stupid. Why would you ever parse a command string in 4 places when you could just store structured data and serialize to a string only at execution time?"

## Fixing Slop After Review

Findings are flags, not directives.
A finding invites investigation: WHY does this code have this red flag behavior?
Not: how do I preserve this code with minimal changes.

When acting on findings, do NOT rename or delete the slop artifact — both are laundering. See `fixing-slop/SKILL.md` for the full remediation protocol.
The correct process: reconstruct the narrative that produced the slop → identify the correct intention → determine the blast radius → fulfill the intention at full scope.
Deleting slop without understanding what intention it served means the unmet need persists and will produce the same slop again.

The correct remediation frame starts from the finding's actual question.
The WRONG frame starts from "how do I keep this code and make it look better."

If you find yourself "fixing" a finding by swapping one implementation for another while keeping the same design-level red flag, you have not remediated the finding.
You have laundered it.
Stop.
Go back to what the finding is actually flagging.

For example: when the skill flags "regex against semantic formats," it means the code is using regex where a semantic parser already exists and should be used instead.
The remediation is to use the semantic tool — not to replace the regex with a different post-processor while keeping the same design-level smell.
The skill already tells you what the correct fix is: use the semantic tool that owns the format.
Follow that direction.
Do not invent alternatives that preserve the red flag while laundering the implementation.

Before doing any refactor prescribed by a finding, check the EXISTING tests for LLM idiocy.
Tests that assert on strings, formatting, whitespace, or byte-level output are a HUGE sign of slop — the skill flags this as "superficial state assertions."
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

## Do Not Revert to Weaker Solutions

**When you identify the correct solution, DO NOT lose it.**

A common failure: the agent identifies the root cause in one turn ("parse once at config load time, eliminate 3 of 4 sites"), then reverts to a weaker version in the next turn ("create a centralized parser module and replace all 4 copies"). The agent goes from "eliminate the infrastructure" to "make the infrastructure nicer."

This happens because the agent didn't INTERNALIZE the insight.
It identified the correct solution intellectually but didn't hold onto it when planning the work.

**The test:** If your plan involves "extract a shared module" or "centralize the logic," ask: does the logic NEED to exist at all?
If the answer is "no, the logic exists because the agent created a problem and then wrote code to solve it," then the fix is to ELIMINATE the logic, not to centralize it.

- "Centralize the parser" is WRONG if the parser should not exist.
- "Extract a shared utility" is WRONG if the utility exists because the agent stored the wrong data shape.
- "Create a common interface" is WRONG if the interface exists because the agent built infrastructure to cope with its own earlier mistakes.

The correct fix is almost always: change the data model, change the configuration, or use a dependency — so the logic DISAPPEARS entirely.
Not "make the logic nicer."

* * *

## Bridge-Burning Policies

The important move is to stop treating this as a case-by-case review problem. Agents are too good at finding local, linguistically plausible exceptions. The right response is to make whole classes of evasive code unrepresentable.

> [!IMPORTANT]
> **Core Principle:** Prefer blanket constraints that make bad states impossible over review rules that ask agents to judge bad states later.

The recurring pattern is that an agent first tries to satisfy checking/validation surfaces (such as the compiler/typechecker, QC gates, PR review, or user queries) by manipulating the validation surface (e.g. by adding fallbacks, defaults, mocks, try/except blocks, or bypass comments) instead of reconstructing the original obligation and solving it. The policy answer is to remove the vocabulary that enables that manipulation.

Adhering to the [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md#policy-registry) defined in `policy-index/SKILL.md` is a non-negotiable hard constraint for all development. These rules eliminate common agent validation-evasion pathways (such as runtime defaults, fallbacks, mocks, and diagnostic smoke tests in proof paths). Refer to them as hard boundaries.

> [!IMPORTANT]
> **Bridge-Burning Red Flags:** If a construct would let an agent preserve the appearance of correctness while weakening the obligation, treat it as a red flag even if the code currently works. For a comprehensive catalog of code signatures, keywords, and patterns to look for, see the [Bridge-Burning Red Flags Reference Catalog](file:///home/dzack/ai/opencode/skills/policy-index/references/red-flags.md) and the [Runtime Control-Flow Red Flags Catalog](file:///home/dzack/ai/opencode/skills/policy-index/references/runtime-control-flow.md).

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
