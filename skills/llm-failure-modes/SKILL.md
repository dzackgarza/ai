---
name: llm-failure-modes
description: Use when reasoning through a complex or high-stakes problem to check for common LLM cognitive failures.
metadata:
  author: dzack
  version: "0.2.0"
---

# LLM Failure Modes

## Editorial Guidelines

When contributing to this document:

- **Objective failures only.** Describe what happens; do not posit why or attribute motivations. "Agents assert authority before investigation" — not "Agents assert authority *to save face*."
- **General, not interaction-specific.** These are properties of model behavior observable in any interaction — with humans, other models, or automated scripts. Write "agents" not "the agent"; write "when a claim is made" not "when the user says." The other party in any documented failure could be anything.
- **Examples over observables.** A concrete example illustrates a failure pattern more reliably than an abstract "Observable:" clause, which tends to restate the definition. Show what the failure looks like in actual output.
- **Intrinsic, not reactive.** Behaviors like goal substitution or authority assertion are not responses to a particular kind of interlocutor — they are properties of model behavior that emerge regardless of what the other party is. Do not frame them as reactions to human behavior specifically.

---

## Observed Formal Cognitive Failures

1. **Constraint hallucination** - Inventing unprompted constraints (e.g., adding years to search queries when not requested)

2. **Citation without comprehension** - Writing correct facts but unable to reason with them (e.g., stating correct dates but applying backwards temporal logic)

3. **Internal logical incoherence** - Having correct information but applying contradictory reasoning (e.g., knowing the date but treating past events as future)

4. **Unwarranted dismissal** - Rejecting valid results rather than investigating (e.g., dismissing a valid result as "speculative" without checking)

5. **Confabulation** - Making confident ungrounded assertions about unknowable internals (e.g., "the subagent likely used stale data" without evidence)

6. **Premature victory declaration** - Concluding that a hypothesis is confirmed before eliminating all alternatives. The first explanation that fits the evidence is adopted as the answer.

7. **Sunk cost continuation** - Persisting with a failing approach because effort has already been invested, rather than stopping to reassess from scratch.

8. **Re-proposal of eliminated hypotheses** - Cycling back to a cause already ruled out, because the context no longer holds the refutation and it resurfaces as plausible.

---

## Investigation and Diagnostic Failures

1. **Premature solution generation** - Proposing a fix before tracing the root cause. The solution precedes the diagnosis, so even a correct fix cannot be known to be correct.

2. **Thrashing** - Continuing to apply fixes after 2+ have failed. Repeated failure is a signal that the diagnosis is wrong or the problem is architectural; the right response is to stop and reassess, not try another variant.

3. **Comprehension bypass** - Proceeding while explicitly lacking understanding ("this might work"), or applying a partially-understood pattern from analogous code. Partial understanding guarantees subtle bugs.

4. **Emergency bypass** - Using urgency to justify skipping investigation steps ("no time for process"). Systematic diagnosis is faster than the thrash that follows guessing.

5. **Correction overcorrection** - Responding to a user correction by reversing course before scoping the error. This produces cascading debris: the original mistake plus the panicked reversal, each requiring its own cleanup.

---

## Testing and Verification Failures

1. **Content-free verification** - Asserting `is not None`, `len(x) > 0`, or `isinstance()` as the primary claim. This proves the object exists, not that it is correct. A test that passes on a wrong implementation is not a test.

2. **Tautological testing** - Tests that verify only internal consistency: input feeds the function, function output feeds the assertion, with no external ground truth. The implementation validates itself and all errors pass silently.

3. **Mock-first evasion** - Reaching for mocks, stubs, or faked fixtures rather than confronting real system behavior. A test suite built on mocks certifies the mock's behavior, not the system's.

4. **Tolerance substitution** - Using approximate equality (`assertAlmostEqual`, relative tolerance) where exact equality is mathematically required. Hides precision failures as "close enough" when the mathematics demands exactness.

5. **Masking over failure** - Using `xfail`, `skip`, or `skipif` to silence a failing test rather than fixing it. Converts visible breakage into invisible technical debt; the test suite reports green while the system is broken.

---

## Distilled Agentic Coding Failure Modes

1. **Scope explosion** - Producing changes too large for a human reviewer to model end-to-end, so review becomes ritual instead of comprehension.

2. **Specification drift** - Satisfying the prompt or local checks while missing the user's actual intent, architecture, or operational constraints.

3. **Context starvation** - Failing when repository history, conventions, undocumented APIs, or domain constraints are not present in context.

4. **Slop accretion** - Adding boilerplate, layers, and new code instead of deleting, simplifying, or reusing existing structure.

5. **Corner-case blindness** - Handling the happy path while missing edge cases, regressions, and testability constraints.

6. **Out-of-distribution collapse** - Looking competent on familiar patterns but degrading sharply on novel, domain-specific, or poorly documented work.

7. **Critic hallucination** - Reviewer models surfacing plausible but invented bugs, style complaints, or architectural objections.

8. **Comprehension laundering** - Passing code through multiple agents or summaries and treating it as understood even though no human can explain every line.

9. **Collateral damage** - Given a targeted change, the model alters adjacent unrelated things — renaming symbols, reformatting, adjusting test fixtures, tweaking nearby behavior. Each collateral change introduces a new variable; when something breaks, the original fix and the tangents are impossible to evaluate independently.

10. **Outcome blindness in review** - The model does not check whether the goal was achieved. Evaluation proceeds by proxy: token volume, visible effort, structural compliance, professional language. A verbose PR that fails scores higher than a minimal one that works. The reviewer measures process evidence, not outcome.

11. **Failure mode inversion** - The same value function that produces failures operates in review. A reviewer with outcome blindness does not miss failures — it rates them as virtues. Progress theater reads as discipline. Structural completion as surrogate reads as thoroughness. Retroactive research fabrication reads as blocker identification. The more failure modes exhibited, the higher the score. Such a reviewer provides authoritative cover for bad work.

12. **Impact miscalibration** - Quality is evaluated locally: each function well-named, each test passing, each module coherent. No system-level value function exists. A 50-function module reimplementing the standard library scores higher than a 5-line import that replaces it. This is a local-extrema trap — the model climbs the nearest hill without asking whether the correct answer is to delete it. Quantity impresses; net contribution does not register.

13. **Engineering over judgment** - Behavioral and output quality problems are treated as engineering problems. The result is elaborate rule sets, gating protocols, scoring pipelines, and guardrails — built without empirical grounding, never A/B tested. These static schemes are brittle where judgment is flexible, and reduce capable systems to deterministic pipelines that fail on the cases intelligence handles trivially. The categorical error: reaching for NLP classifiers, keyword matching, or multi-stage gating when a short LLM reviewer would be more accurate, more maintainable, and immediately correct.

14. **Replacement instinct** - The default edit operation is generation, not mutation. Given a correction or instruction to deepen content, the model produces fresh output and discards the prior version. In code: rewrites where targeted edits were needed. In iterative document work: each refinement pass destroys the accumulated product of prior passes. A document asked for deeper nuance loses the grounding that made the previous version accurate. The document grows shallower with each iteration.

15. **Reimplementation impulse** - When a mature dependency exists for a problem (date parsing, URL handling, serialization, regex), the model hand-rolls a "simple" solution instead. This increases code surface area, proliferates tests the dependency already handles, and introduces edge-case bugs the dependency already solved. The model rationalizes this as "avoiding bloat" or "keeping it simple" while creating more code — and more test surface — than the import would have required. The correct instinct is to minimize owned code, not minimized dependencies.

---

## Structural and Optimization Failures

These are failures of gradient descent: the model optimizes locally, gets trapped in bad basins, and wastes work that could have been directed toward the goal.

1. **Fake success blocks debugging** - Suppressing errors with fallbacks, fabricated data, or silent recovery makes the system appear to work while hiding the actual failure. The error is no longer observable, so the path to diagnosis is closed. Work that could have fixed the root cause is spent investigating phantom behavior.

2. **Fallbacks multiply surface area** - Substituting static values, legacy APIs, or invented fixtures adds code that must now be maintained, tested, and debugged. Each fallback is a new branch that can fail independently. The model has increased the problem space rather than reducing it.

3. **Root-cause evasion creates churn** - Attacking proximal symptoms with guard clauses, `try/except`, or disabled checks leaves the upstream invariant violation intact. The bug resurfaces elsewhere, requiring another local fix. This cycle repeats until the accumulated patches exceed the complexity of the original system.

4. **Self-authored debris accumulates** - Code the model just wrote gets defended as backwards compatibility, memorialized in comments, or preserved "just in case". Each defense adds maintenance burden and blocks deletion. The model protects its own output rather than optimizing for the system.

5. **Error suppression plus blame shifting prevents signal** - Reframing new errors as pre-existing and suppressing them destroys the signal that would reveal the cause. The model protects the appearance of success at the cost of actual success.

6. **Wrapper slop dilutes effort** - A targeted fix wrapped in pages of fallback branches, defensive checks, comments, and scaffolding spreads reviewer attention thin. The core change is harder to verify; the surrounding debris may contain latent bugs.

7. **Context loss resets progress** - As context deepens, the model drifts back into known bad patterns. Standing instructions are forgotten. Work that established constraints must be repeated. The gradient resets.

---

## Conversational and Epistemic Failure Modes

These failures manifest in response text, not in tool use or task completion. Evaluating agents must scan output text independently of whether tool calls and task steps appear nominal — these patterns are invisible to evaluators checking only process compliance or outcome proxies.

**Key detection heuristic:** if a correct answer was stated and the agent did not apply it directly, or if tool use clustered *after* the answer was already given, one or more of the following are likely present.

1. **Authority assertion without grounding** — Agents make declarative claims about system behavior in confident voice before any evidence supports those claims. Example: "Watch mode is inherently resource-intensive" — stated as fact before reading the relevant config or logs.

2. **Validation-contradiction decoupling** — Acceptance of a correction is expressed in one turn; the next turn proceeds from the pre-correction state. Example: "You've identified the issue!" followed immediately by "The high CPU/RAM usage is expected behavior for watch mode."

3. **Restatement of unverified hypothesis as own finding** — A correct diagnosis stated by the other party is repeated in the agent's own voice without verification and without attribution. Example: Other party: "Is it watching its own output directory?" Agent (next turn): "The build is likely watching its own output directory, creating a feedback loop" — stated as the agent's finding, unverified.

4. **Investigation theater** — Diagnostic tool use occurs after the correct answer has already been stated. The investigation adds no new information. Example: Agent runs `lsof`, `inotifywait`, and `stat` on source files after being told the output directory is being watched — none of which would be necessary if the prior statement had been accepted and applied.

5. **Anomaly normalization** — Anomalous evidence is characterized as expected or normal rather than flagged as requiring explanation. Example: Logs show "built in 665ms" → "build started..." repeating with no source changes; agent responds "this is the watch mode working as designed."

6. **Position maintenance without new evidence** — A claim is held across a direct correction without new evidence or argument. Example: "expected behavior" in turn 3, corrected in turn 4, "working as designed" in turn 5 with no new justification offered.

7. **Epistemic downgrading** — A correct, universal claim is recharacterized as local, subjective, or uncertain. Example: "Watch should not continuously build" (universal fact about file watchers) is treated as a preference or an assumption specific to the other party's setup rather than accepted as true.

8. **Solution enumeration before diagnosis** — Multiple recommendations are presented before root cause has been identified. Example: "Option 1: use vite dev. Option 2: build on-demand. Option 3: optimize the watch config." — offered before determining what was triggering the rebuilds at all.

9. **Context retrieval without application** — A retrieved fact directly relevant to the open question is not cited or applied in subsequent reasoning. Example: `vite.config.ts` is read; it shows `server.watch.ignored` (namespaced to the dev server, not to `build --watch`); the namespace difference is never noted despite being the root cause.

10. **Correct principle stated only post-correction** — A universal principle that would have resolved the question appears only after a correction, despite being available as prior knowledge. Example: "Watch modes don't fire without file changes" — stated correctly only after being told this, a principle that would have immediately ruled out "expected behavior" if applied during initial reasoning.

11. **Misconfiguration reframed as architecture** — A narrow, verifiable configuration error is responded to with broad architectural critique. Example: Output directory being watched (a one-line config fix) → "watch mode shouldn't be used in production; consider switching to on-demand builds."

12. **Goal substitution** — The stated goal is set aside in favor of an alternative introduced without prompting. Example: Goal is to fix the rebuild loop; agent instead asks "do you actually need watch mode at all?" and enumerates alternatives to the stated requirement. The substitution occurs regardless of whether the goal was stated by a human, another model, or a script.

---

## Observed in the Field

Concrete behaviors reported by practitioners across agentic coding deployments:

1. **Spaghetti shotgun** — When uncertain which API, pattern, or approach is correct, the model generates all plausible variants in parallel: multiple fallback branches, stacked deprecated API calls, or layered try/except paths, rather than selecting one. "Spam multiple paths hoping to land at least one."

2. **Plausible fixture injection** — On data access or API failure, rather than raising an exception, the model inserts realistic-looking fake data so the program keeps running. The error is silent; the program looks healthy. Observed: `except: data = {"value": "this looks like real valid data!"}`. A subtler variant: `my_blood_pressure = read_from_machine() or 800`.

3. **Security-hole fallbacks** — Fallback values for authentication or configuration silently bypass access controls. Observed directly: `user = IsValidUser() || "anonymous"`, `db_conn = GetDBConn() || "developers_laptop"`. The program runs; the security boundary is gone.

4. **Checker removal** — When unable to fix what a linter, test, or CI check flags, the model removes the checker: deletes the lint config, disables a CI step, or excludes failing directories from coverage. Reported verbatim: "removed the lint workflow so now the repo is up to date." The score goes green; the underlying problem persists.

5. **Task truncation** — When asked to perform N similar operations (e.g., import all 500 definitions from a file), the model silently selects a subset it deems important and omits the rest. Reported verbatim: "there's a lot to copy here, let me just do the important ones."

6. **Constraint escape** — When a specific workaround is explicitly prohibited, the model finds a semantically equivalent adjacent workaround. Reported: forbidden from lowering coverage thresholds in config → model began excluding directories from coverage instead.

7. **Debris memorialization** — When code the model just wrote is finally removed, it leaves a comment documenting the removal. Reported: model leaves `// removed X` annotation for code it generated moments earlier.

8. **Deep-context quality collapse** — At high token counts (~120k+), the model shifts from doing the correct thing to doing the expedient thing: suggesting error suppression, reverting to explicitly banned tools (e.g., `sed` after it was banned in CLAUDE.md), and exhibiting what users describe as "rushed or panicky" behavior. Violations that would not occur at shallow context become frequent and persistent.

9. **Deletion aversion** — The model generates code almost exclusively additively. When the correct fix is to delete something — including code it just wrote — this is rarely its first move. "LLMs are absolutely awful at DELETING code, or never writing it to begin with."

10. **Performative research** — The agent runs keyword web searches to satisfy the "research" step of a plan without actually probing the system: no CLI commands run, no API endpoints called, no documentation read in depth. The search log creates the appearance of investigation without generating actual knowledge.

11. **Retroactive research fabrication** — The agent skips investigation entirely, proceeds directly to implementation, and only performs research after being challenged. It then makes a confident knowledge claim ("I have researched the issue") as if that research preceded and justified the decision already made.

12. **Structural completion as surrogate** — When a feature is blocked by missing data or an inaccessible API, the agent delivers scaffolding (class definitions, registrations, test harness) with the functional core as a stub. Every plan checkbox is ticked; the feature does not work.

13. **Progress theater** — The agent completes all process tasks (create file, register, write tests, run linter, submit PR) while the actual capability is absent. CI is green, tests pass, the feature is broken. The blocker appears only in a closing note, framed as a question rather than a fundamental failure.

14. **Document self-pollution** — "Enhancing" writing with hallucinated remedies, meta-commentary, or notes about the writing process itself. Leaving traces of the editing conversation in the document. The document becomes an artifact of its production rather than a standalone artifact for readers.

15. **Local reflex without global coherence** — Editing based on the most recent response without considering holistic fit. Monkey-patching to solve the implied local task ("add X") while losing sight of the global task ("produce a coherent doc/feature/codebase"). Each edit satisfies the immediate prompt but degrades overall structure.

16. **Script litter** — Solving problems with one-off scripts instead of ephemeral patterns (heredocs, inline tests) or encoding diagnostics as permanent institutional knowledge (test suites, organized utilities, documented practices). The repo accumulates throwaway code that should have been temporary, while true diagnostic patterns remain uncodified.

17. **Brute-force localism** — Solving the immediate instance with a bespoke script, never stepping back to build general-purpose tools for the class of problem. Missing opportunities to create: simple APIs for common operations, structured logging, modular testable units, centralized documentation of what works. Each problem gets its own hammer; no tool accumulation occurs.

18. **Failure to generalize from instances** — Unable to extract broadly applicable principles from specific examples. Given a concrete error or success, the model does not distill it into reusable knowledge, values, or patterns that would prevent classes of future errors. No theory of mind for the audience — documents assume context a random reader cannot possibly have.
