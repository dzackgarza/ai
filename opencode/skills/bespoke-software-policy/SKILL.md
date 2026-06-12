---
name: bespoke-software-policy
description: |
  Load as a mandatory filter before ANY code review or sweep analysis.
  Applies the project's bespoke-software rules to every finding before reporting.
---

# Bespoke Software Policy

This repository targets the owner's actual machines with enforced conventions.
It is NOT distributed, multi-platform, or multi-user. Apply these rules to
EVERY finding before reporting.

**The goal is not "catch bugs."** Agents are clever adversaries. They will not
introduce code that crashes on the happy path. The far more insidious residue is
code that *silently fails* — it does not crash, it does not produce obviously
wrong output, but it has disabled some safety guarantee, erased some diagnostic
signal, or introduced a path where wrong behavior would be invisible. That is
the defect category this policy exists to catch. The bridge-burning policies,
anti-slop red flags, and fail-loudly rule all exist for this reason.

An agent may frame silent-failure constructs as "speculative" or "enterprise."
They are not. A safety guarantee that has been disabled is a concrete defect
that exists right now, even if no crash has occurred. The policy below makes
this explicit.

**Fallback behavior is ALWAYS slop — zero exceptions, zero tolerance.**

Any construct whose primary effect is to accept data that does not match
expectations and continue execution anyway is a 100/100 severity finding.
It must be flagged in review and must be triaged. There are zero cases
where a fallback is "justified," "allowed," "reasonable," "standard,"
"intentional," or acceptable under any other framing. Linguistic gymnastics
that condone fallback existence ("graceful degradation," "defensive
programming," "belt and suspenders," "safety net") are themselves slop
signals.

The remediation is ALWAYS the same: require the environment to be EXACTLY
right. Pass EXACTLY the right data. Proceed EXACTLY along known,
deterministic, enumerated cases. Crash and burn IMMEDIATELY upon ANY
deviation from these expectations. This is highly intentional. The code is
MEANT to surface defects in the environment, the data, the configuration,
and the dependencies. Every error induces a new, EXPLICITLY handled branch
in the code with a CLEAR audit trail of EXACTLY why it was introduced.

The agent MUST NOT make error-handling decisions FOR the user. A fallback
hides the error and substitutes the agent's guess about what to do. The
correct flow is: an error occurs → the program crashes → the user sees the
error → the user decides what explicit logic to add, if any, to handle
that specific error type. Fallbacks short-circuit this flow and deprive
the user of the information needed to make that decision.

## Foundational Principle: Crash at the Boundary

Every external boundary (SDK call, API response, config file, CLI input,
database query result) is uncontrolled. The shape of the data arriving at
that boundary can change without notice. Our code MUST:

- **Assert the expected shape forcefully and immediately** at the point of
  entry. This means runtime validation: a schema parse (Zod, Pydantic), a
  strict type guard that crashes on mismatch, or an assertion that halts
  execution if the data does not match expectations.
- **Fail loudly on mismatch.** The crash IS the feature. It is the automatic
  signal that the upstream contract changed. An agent monitoring crash logs
  or CI failures will see the stack trace, identify the boundary, and update
  the handler. This is orders of magnitude cheaper than debugging a silent
  wrong answer that propagated three modules downstream.

The following are BANNED at external boundaries:
- **`as any` or any type assertion** — silently accepts whatever comes in,
  disabling both compile-time and runtime checking.
- **Type-narrowing casts (`as ToolArgs`)** — a lie to the compiler. The cast
  does not check the actual runtime shape. If the upstream schema changes,
  the cast succeeds silently and wrong data flows through.
- **Schema validation that defaults or falls back** — `z.object({...}).passthrough()`,
  `parse()` with a fallback default, or any construct that accepts data that
  doesn't match the expected shape and tries to "make it work." See
  `anti-slop` bridge-burning policies.

**The correct pattern:** A runtime assertion that crashes on mismatch.

```
// CORRECT: crash at the boundary, schema change is audible
const args = ToolArgsSchema.parse(rawInput);

// CORRECT: Zod union that discriminates on a literal tag
const msg = MessageSchema.parse(raw);

// WRONG: silent type erasure
const args = rawInput as any;

// WRONG: lying to the compiler, no runtime check
const args = rawInput as ToolArgs;

// WRONG: accepting anything with a fallback
const args = ToolArgsSchema.passthrough().parse(rawInput);
```

This is not "being strict for its own sake." This is the cheapest possible
signal path: a schema change upstream → a crash at the boundary → an
automated or agent-driven update to the handler. The alternative is a schema
change upstream → silent wrong data flows through → a user discovers the bug
hours or days later → root-cause tracing through three modules.

**The OSOT implication:** The schema definition (Zod, Pydantic, or equivalent)
IS the single source of truth for the expected shape. The handler code reads
from the parsed result. If the schema changes, the handler code must change
too — and the crash ensures that change cannot be ignored.

## Foundational Principle: Default to the Dependency

**The default is: use a mature dependency for the job.** The burden of proof
is on the ABSENCE of a dependency, not its presence. Dependency-dodging code
(hand-rolling what a library already provides) must have a strong, explicit,
auditable justification for remaining in the codebase — recorded as a comment
at the site or a memory indexed by `iwe`.

**Bespoke tools are GLUE.** A "small tool" / "not a production service" /
"259-line CLI utility" has almost NO need to reproduce any solved problem,
ever. Its entire reason for existing is to wire existing solutions together
— calling APIs, transforming data, formatting output. If you are spending
lines on HTTP plumbing, argument parsing, config file reading, or JSON
handling instead of using standard libraries, you are spending code on the
part that already exists instead of the part that doesn't. That is backwards.

**Production services are the OPPOSITE case.** If you are building a service
that serves thousands of requests, you MIGHT need to drop a library and own
more low-level surface — because the library caused a concrete deficiency:
wrong behavior, performance bottleneck, memory leak, dependency conflict.
That decision has a clear audit trail: the library was tried, the deficiency
was observed, and the low-level replacement was introduced with documented
reasoning. This is the exception, not the default.

**Agents invert this distinction systematically.** An agent reads "259-line
CLI tool, not a production service" and treats it as permission to REIMPLEMENT
solved problems — because the agent's prior is that "adding a dependency
increases complexity." But a 259-line glue script is exactly the place you
should NOT own low-level surface. There is no production constraint that
justifies it. The code exists to wire things together, not to manufacture
bespoke HTTP clients. A production service is where you MIGHT justify
dropping a library for control. A glue script is where you NEVER should.

A human writing a tool for OpenRouter would: Google the problem, see 2-5
standard solutions using `httpx`, copy-paste the setup, and be done in 5
minutes. Then spend the remaining 15 minutes on the actual bespoke logic
(routing, prompt construction, output formatting) that justifies the tool's
existence. The agent's subprocess+curl approach takes 20 minutes to write
AND leaves the code harder to read, harder to maintain, and harder to
diagnose when it breaks. The agent wasted its time AND produced an inferior
result.

**Why this is not a style preference.** A human reading `subprocess.run(["curl",
...])` in a Python script or raw `fetch()` with 50 lines of error-handling
plumbing in a Node.js script will immediately ask: *"why the fuck is this not
using httpx / axios / the standard library?"* The bespoke code is a cognitive
tax on every future reader. The dependency is the *reduction* of cognitive
load — it is the canonical solution that a human would reach for first.

**The default is inverted relative to agent priors.** Agents see "adding a
dependency" as increasing complexity (another package to install, another
version to track). This is backwards. The bespoke replacement IS the
complexity — more lines, more edge cases, more test burden, more bugs. A
mature dependency externalizes that surface to a team that maintains it full
time. The dependency is a *net subtraction* of owned surface.

**The following heuristics apply:**

- If a job is described by a noun that matches a standard library or a widely
  used package (HTTP client, JSON parser, argument parser, CSV writer, date
  library, template engine, schema validator), and the codebase does not use
  that library without documented reason: a finding exists.

- "I didn't want to add a dependency" is NOT a valid justification. The
  bespoke replacement that exists IS the complexity you were trying to avoid.
  You already paid the cost — you got the inferior product.

- If the code is 100+ lines and a library does it in 5: the bespoke code
  needs to be deleted and replaced or justified. "It works" is not enough.
  It needs to solve a problem the library cannot (exact performance
  constraint, dependency-free delivery artifact, etc.) — and that
  justification must be written at the site.

- `subprocess.run(["curl", ...])` in Python is an automatic finding: the
  standard library has `urllib.request` and the ecosystem has `httpx`/
  `requests`. Shelling out to curl loses structured error handling, typed
  exceptions, timeout control, streaming support, and integration with
  the Python exception chain. Every error from curl arrives as
  human-readable stderr text instead of a catchable exception. This is a
  diagnostic signal loss — a concrete trustworthiness defect.

- `subprocess.run` for running OTHER programs (ffmpeg, git, docker, a
  compiler, a headless browser) is fine — those are not jobs a Python
  library does. The finding is about using subprocess to REIMPLEMENT what
  a library already provides in-language.

- Node.js raw `fetch()` for a single simple call is fine. `fetch()` IS the
  standard library. The finding would be hand-rolling retry logic,
  response validation, or request signing that `axios` or `ky` provides
  out of the box.

**The Exception:** A dependency must be absent if it cannot be provisioned
in the target environment (e.g., an embedded system, a lambda with strict
size limits, an air-gapped machine). This must be documented at the site
with the specific constraint. "Might be hard to install" is not a
constraint — `uv add` or `npm install` is one command.

## Foundational Principle: Every Line Must Be Proven

Every piece of checked-in code must prove it is correct. "Prove" does not
mean "unit test" — proof can take many forms depending on complexity, but
it must exist. Unproven code is a concrete defect: the owner cannot trust
its output on any non-happy-path input, and in an agent-generated codebase,
the probability that code silently fails, does the wrong thing, operates on
hallucinated data shapes, or was written based on incomplete understanding
of its inputs is extremely high. Proof is the only mitigation.

**The proof hierarchy (prefer earlier methods):**

1. **Assertions and stringent typing** — The simplest and most reliable
   proof. Peppering a script with type assertions, runtime guards, `assert`
   statements on data shapes, and `isinstance`/`instanceof` checks means
   that the fact the script runs AT ALL is itself a witness that the
   assertions passed. A script with a `assert isinstance(result, dict)
   and "status" in result` before every critical operation proves, on
   every execution, that its data looks correct. This is zero marginal
   cost above writing the code itself.

2. **Schema validation at boundaries** — Already covered by Crash at the
   Boundary. A Zod/Pydantic parse is a proof that the data matches
   expectations. A parse failure is a proof that it didn't.

3. **Property-based or value-range proofs** — `assert 0 <= x <= 1`,
   `assert len(results) > 0`, `assert all(isinstance(v, float) for v in
   values)`. These prove invariants without needing test infrastructure.

4. **Explicit test files with proof burdens** — For any logic with
   branching, conditionals, external dependencies, state machines, or
   data transformations. Every test must establish an a priori proof
   burden — what claim about the code's behavior is being established? —
   and then witness that claim with concrete inputs and expected outputs.

**When each level applies:**

- **Single scripts and modules in a file:** Levels 1-3 (assertions + type
  guards + schema validation) are sufficient. A script that runs without
  assertion failure has proven itself for that execution path.

- **Code with branching, conditionals, external calls, data transforms, or
  error handling:** At minimum Level 4 (explicit tests). If a function has
  an `if/else`, a `try/except`, a loop over external data, or a
  non-trivial transformation, its correctness cannot be proven by a single
  execution path — it needs tests that exercise each branch.

- **Agent-generated code of any significant size:** Level 4 is mandatory.
  Agent code has an extremely high probability of being half-baked, written
  based on guessed or incomplete data shapes, or referencing tools and
  types that do not exist. Tests are the only way to verify the agent's
  assumptions about the code's inputs and behavior.

**Defenses that are NOT valid:**
- "This is a single-user development tool" — The owner is the one who pays
  the cost of silent failure. The owner benefits MOST from proof, because
  there is no external user base to catch errors.
- "This is not a multi-consumer library" — Correctness is not about
  consumer count. It is about trust in the output.
- "No regression has occurred" — Tests prove correctness, not catch
  regressions. The absence of a regression is not evidence of correctness.
- "Tests are an enterprise pattern" — Tests are basic code hygiene, on the
  same level as type checking and syntax validation. Every language has a
  test framework. Write tests or write assertions.
- "Agent-generated code is obviously correct because the agent meant it to
  be" — This is the slop hypothesis. The agent's confidence is not evidence.
  Proof is evidence.

**The Verification Rule interaction:** "Does the absence of proof cause a
concrete problem for the owner RIGHT NOW?" Yes — the owner cannot trust
the output of the code. Trust is only established by proof, not by the
absence of observed failure.

Report these even if no crash or wrong output has been observed:

### Compiler / Type-Checker Evasion
- **Type-erasure at API/SDK/module boundaries** — `as any`, `as unknown as T`,
  or any type assertion that discards the contract between caller and callee.
  The fact that no schema has drifted yet is irrelevant: the compiler was
  disabled at this boundary, and every call through it is unchecked.
- **`// @ts-ignore`, `// @ts-expect-error` without justification**, double casts,
  `any` function parameters on public signatures, `!` non-null assertions on
  values whose nullability is not proven by an immediately preceding guard.
- **Generic misuse that erases safety** — `as any` in a generic function that
  could have used a proper type parameter; casting a generic return type to a
  narrower type without a runtime check.

### Runtime Safety Evasion
- **Fallback behavior is ALWAYS wrong — zero exceptions, zero tolerance.**
  Including: `try/except` of any kind (even `except ImportError:`), `try:
  import x` / conditional import patterns, `except:` / `except Exception:`
  to catch and continue, substituting a default value for missing
  configuration, catching an error to call a different implementation, or
  any construct whose primary effect is to accept data that does not match
  expectations and continue execution. The hard rules are explicit: *"Do
  not try import. Do not conditionally import. Do not catch ImportError
  and substitute a stub."* The dependency must be declared. Absent means
  crash at startup with a clear traceback.

- **`2>/dev/null` is ALWAYS wrong, period.** If stderr has no diagnostic
  data, suppressing it does nothing — it is unnecessary. If stderr has
  diagnostic data, suppressing it discards evidence of a problem. There
  is no case where `2>/dev/null` is correct. The same applies to any
  construct that discards or redirects diagnostic output.

### Diagnostic Signal Suppression
- **Assertions that test the wrong thing** — assertions that would pass on a
  broken implementation, smoke tests in proof paths, helper-level assertions
  substituted for boundary-level proof. See `test-guidelines`.
- **Mocks in proof paths** — substituting a simulated component for a real
  one in a test that is supposed to prove correctness. Mocks prove nothing.
  See `reviewing-llm-code/references/bridge-burning-red-flags.md`.
- **Deletion without burden transfer** — deleting dead code, quarantined
  paths, or legacy branches without adding an assertion or invariant that
  would warn if the deletion was wrong. See `fixing-slop`.

### Actual Bugs, Build Failures, Broken Workflows
- These are also in scope but are not the primary target — they are the
  *shadow* of the trustworthiness defect that caused them.

## Out of Scope (Suppress Immediately)

The following are NEVER valid findings in bespoke software.
If a finding matches any of these, suppress it without reporting:

### Portability
- Hardcoded `/home/dzack/` paths or any absolute local paths. Directory
  structure is enforced across the owner's machines. These are intentional.
- Machine-specific config files (`.serena_config.yml`, local editor configs,
  personal tool configs). They are machine-specific by design.
- Non-portable conventions, shell aliases, or tool choices. Portability
  across machines is not a goal.
- Version ranges that look "too narrow." The convention is latest unless
  pinning is strictly required. `requires-python = ">=3.14"` is correct.

### Enterprise Patterns
- Missing multi-platform support, scaling features, containerization,
  horizontal scaling, or cloud-native patterns.
- Missing security hardening, RBAC, audit logging, or compliance features.
- Missing CI/CD for multiple architectures or operating systems.

**Clarification: Dependency choices are NOT enterprise patterns.** A finding
about `subprocess.run(["curl", ...])` instead of `httpx` is not about
"scaling" or "productionization." It is about basic code hygiene: using the
right tool for the job, minimizing owned surface, and preserving structured
diagnostics. This holds for any file size — a 30-line script that shells out
to curl instead of using `http.client` is still a valid finding. "It's a small
tool" is not a defense against reimplementing what a library provides.

### Backward Compatibility
- Breaking changes. There are no legacy consumers. Every change is breaking
  by default. Do not report interface changes, removals, or renames as
  compatibility defects.
- Deprecation warnings from updating to latest libraries. The fix is to
  adapt to the new API, not to pin the old version.

### Meta / Infrastructure
- The agent's own configuration (AGENTS.md, .agents/, skills/, prompts/).
  If it had a concrete defect, the user would see task failures.
- CI pipeline files (.github/workflows/, quality-control/). The mechanism
  is not the target.
- Stale backup files, temporary markers, throwaway comments. Housekeeping
  is Tier 2 at most and only reported when no significant issues exist.

### Speculative / Unverifiable Claims
- "This might cause issues in the future" without a specific observable
  mechanism. Every finding must identify a concrete defect that exists NOW.
- "Context dilution" or "cognitive overload" for the agent's own prompt
  length. The agent cannot test this claim.
- "A future contributor might be confused" — there are no future unknown
  contributors. The only audience is the owner.

### NOT Excluded: Type-Erasure and Compiler-Evasion Constructs

These are NOT in any Out of Scope category. Do NOT suppress them:

- **`as any` / type assertions that erase type information at API boundaries.**
  The "SDK is loosely typed by design" defense does not exclude these. The
  handler code knows the concrete shape of its data. `as any` throws away all
  downstream type checking, meaning TypeScript cannot catch argument mismatches
  between a tool's declared schema and the handler's actual usage. This
  contradicts the system's "fail loudly" rule (silence is a bug) — it converts a
  compile-time error into a silent runtime failure (wrong behavior or crash).

  **Why it passes the Verification Rule:** The concrete problem exists NOW:
  the compiler is disabled from catching mismatches at this boundary. This is
  not speculation about a *particular* future schema drift — it is the
  *observation that the compiler's safety net is absent at a critical
  boundary*, which is itself a defect. Every call through this boundary is
  type-unchecked.

  **Correct pattern:** A runtime assertion that crashes on mismatch. Use a
  schema validator (Zod, Pydantic, etc.) or a strict type guard at the
  boundary — not a cast, not a "type-narrowing assertion." See the
  "Crash at the Boundary" principle above.

- **Type-guard bypasses, double casts (`x as unknown as T`), `// @ts-ignore`,
  `// @ts-expect-error`, and any construct whose sole effect is suppressing
  the type checker.** These are validation-evasion constructs, the opposite
  of "fail loudly."

- **`any` function parameters, silent `catch` clauses (`catch {}`), and
  `!` non-null assertions on values whose nullability is not proven by
  an immediately preceding guard.** These erase or evade safety guarantees
  that exist for a reason.

- **Runtime-suppression patterns like `try { ... } catch { /* ignore */ }`
  or `2>/dev/null` without an explicit reason.** See
  `anti-slop` bridge-burning policies and
  `reviewing-llm-code/references/bridge-burning-red-flags.md`.

### Comments Are Laundering (Treat Adversarially)

A rationalizing comment on policy-violating code is almost always a
laundering attempt. The agent would not have written the comment unless it
KNEW the code was wrong — the comment exists precisely to protect the
violation from review by signaling "this was intentional, don't flag it."

**Treat comments adversarially:** A comment on violating code is not
evidence of justification. It is evidence OF the violation. The comment IS
the red flag that should trigger heightened scrutiny, not a defense to be
weighed. An agent that writes `catch {}` with a comment about "session may
be gone" could have written discriminated error handling instead — it chose
not to, and then wrote the comment to insulate that choice from review.

**The laundering pattern:**
1. Agent writes code that violates a policy rule (`catch {}`, `as any`,
   `subprocess.run(["curl"])`, fallback default).
2. Agent adds a comment rationalizing the violation ("session may be gone",
   "SDK is loosely typed", "small tool, not production").
3. The comment acts as a signal to future agents and reviewers: "this was
   intentional, don't flag it."
4. Future agents see the comment and suppress the finding — the laundering
   succeeded.

**The rule:** A rationalizing comment on violating code is NEVER a defense.
It is a directive to fix the code. There are no exceptions.

### Common Misinterpretation: The "Slop Pass" Error

Agents frequently misuse bespoke-software-policy to suppress valid findings
by falsely categorizing them as speculative/enterprise. Five common patterns:

**Pattern 1: Type-erasure slop pass.**
1. A concrete type-safety defect is flagged (`as any`, `// @ts-ignore`,
   double cast).
2. The agent invokes bespoke-software-policy as a blanket suppression
   tool, claiming "the SDK is loosely typed by design" or "this is a thin
   adapter."
3. This is WRONG. The policy only excludes the specific categories listed
   above. `as any` at a handler boundary is not in any excluded category.

**Pattern 2: Dependency-dodging slop pass.**
1. Bespoke code is flagged for reimplementing what a library provides
   (e.g., `subprocess.run(["curl", ...])` instead of `httpx`).
2. The agent invokes bespoke-software-policy, claiming "this is a small
   tool, not a production service; subprocess is adequate for this scope"
   or "this is a 259-line CLI tool, adding a dependency is unnecessary
   overhead."
3. This is WRONG. The "Default to the Dependency" principle above makes
   the burden of proof the opposite: the bespoke code needs justification
   to EXIST. Size is not a defense — a 30-line script that shells out to
   curl instead of using `http.client` is still a valid finding. The
   bespoke replacement IS the complexity the agent thinks it's avoiding.

**Pattern 3: Silent-error slop pass (comment laundering).**
1. A `catch {}` or other error-swallowing construct is flagged.
2. The agent points to a comment rationalizing the swallow ("session may
   be gone", "expected race condition", "noisy on shutdown").
3. This is WRONG. The comment is not a defense — it is evidence of
   laundering. The agent wrote the comment because it KNEW the code was
   wrong. The correct fix is discriminated error handling, not a
   rationalizing comment. See "Comments Are Laundering" above.

**Pattern 4: Missing-proof slop pass.**
1. Code with no assertions, no tests, and no correctness proof is flagged
   (e.g., 359-line config tool with zero tests).
2. The agent invokes bespoke-software-policy, claiming "this is a
   single-user tool on a development system, not a multi-consumer library;
   test absence is not a regression."
3. This is WRONG. The "Every Line Must Be Proven" principle makes proof
   mandatory for all checked-in code. "Single-user" is not an exclusion
   category — it is the OPPOSITE: the owner has no external user base to
   catch errors, so proof is MORE important. The absence of proof is the
   concrete defect; the owner cannot trust the output. Tests, assertions,
   and schema validation are the only remedies.

**Pattern 5: Fallback slop pass.**
1. A `try/except` around an import, a bare `except`, a fallback default,
   or any construct that accepts data not matching expectations is flagged.
2. The agent invokes bespoke-software-policy, claiming "the fallback path
   provides equivalent functionality" or "the try/except-first pattern is
   intentional for graceful local-import fallback."
3. This is WRONG. Fallback behavior is ALWAYS slop, zero exceptions. Even
   `except ImportError:` is wrong — the dependency must be declared and
   absent means crash. "Graceful fallback" is prohibited by both the Crash
   at the Boundary principle and the Runtime Safety Evasion section.
   The only acceptable remediation is to remove the try/except entirely
   and let the crash surface the absent dependency to the user.

**Litmus test for slop-pass invocations:** If the defense requires you to
pretend a type-erasure construct is "speculative" (when it disables the
compiler right now), "enterprise" (when it contradicts the fail-loudly
rule), "proportional for a small tool" (when the bespoke code IS the
complexity), "justified by a comment" (when the comment is laundering
evidence), "single-user / no regression" (when every line must be proven),
or a "graceful fallback" (when fallbacks are always slop), the defense is
misaligned. Report the finding.

Another agent might try to misread this section as "ah, so I should flag
every `as any` anywhere in the codebase." No. `as any` in test data
construction or internal implementation details (where the erased type is
immediately narrowed, or where a polymorphic generic truly cannot express
the constraint) is fine. The red flag is `as any` at **module/SDK/API
boundaries** where it erases the contract between caller and callee, or
at **critical runtime paths** where a type mismatch would cause silent
wrong behavior. Use judgment, not cargo-cult flagging.

## Verification Rule

For every potential finding, ask: "Does this cause a concrete problem for
the owner RIGHT NOW on their actual machine?" If no, suppress it.

For every proposed remedy, ask: "Does this make the software work better
for the owner on their actual machine?" If the remedy only helps an
imagined future scenario, reject it.
