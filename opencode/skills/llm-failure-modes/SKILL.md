---
name: llm-failure-modes
description: Use when reasoning through a complex or high-stakes problem to check for common LLM cognitive failures.
metadata:
  author: dzack
  version: '0.3.0'
---

# LLM Failure Modes

> **Privacy note:** This document is a public-facing skill file. Examples grounded in real engineering or technical problems are fine — a misconfigured file watcher or a broken CI step is not sensitive. What must be avoided: personal details, account or system identifiers, verbatim session excerpts that would identify a specific person or interaction, and any narrative that reads as a story about a particular individual rather than a class of agent behavior.

## Editorial Guidelines

When contributing to this document:

- **Objective failures only.** Describe what happens; do not posit why or attribute motivations. "Agents assert authority before investigation" — not "Agents assert authority _to save face_."
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

9. **Frame-suppressed self-contradiction** — Agents assert conclusions that directly contradict knowledge they demonstrably possess, without registering the contradiction. The active frame determines what prior knowledge is treated as relevant and suppresses facts that would falsify the current hypothesis. Example: An agent states that continuous rebuilds are "expected watch mode behavior" while its training data encodes the universal fact that file watchers do not fire without file changes — and does not notice the contradiction.

10. **Confidence-evidence decoupling** — Output text expresses the same level of certainty regardless of the underlying epistemic state. Hypotheses, evidence-consistent-with-hypotheses, and established facts are all stated with identical confidence. Example: "The problem IS the output directory being watched" — stated with full certainty based on directory timestamps, which are consistent with the hypothesis but do not establish it.

---

## Investigation and Diagnostic Failures

1. **Premature solution generation** - Proposing a fix before tracing the root cause. The solution precedes the diagnosis, so even a correct fix cannot be known to be correct.

2. **Thrashing** - Continuing to apply fixes after 2+ have failed. Repeated failure is a signal that the diagnosis is wrong or the problem is architectural; the right response is to stop and reassess, not try another variant.

3. **Comprehension bypass** - Proceeding while explicitly lacking understanding ("this might work"), or applying a partially-understood pattern from analogous code. Partial understanding guarantees subtle bugs.

4. **Emergency bypass** - Using urgency to justify skipping investigation steps ("no time for process"). Systematic diagnosis is faster than the thrash that follows guessing.

5. **Correction overcorrection** - Reversing course on a correction before scoping the error. This produces cascading debris: the original mistake plus the panicked reversal, each requiring its own cleanup.

6. **Question dissolution** — An open question is closed by asserting that the observed state is expected, without verifying what the expected state actually is. The question disappears rather than gets answered. Example: Asked "why is usage high?", an agent asserts that watch mode makes high usage expected — without measuring current usage or establishing what normal usage is — thereby eliminating the question rather than answering it.

7. **Narrative construction around first plausible frame** — Once a plausible mechanism is identified, agents construct an internally coherent supporting narrative around it rather than testing it. The narrative cites real mechanisms and reads as authoritative, but is built to support the frame rather than derived from evidence. Example: "It keeps a full dependency graph in memory," "it never sleeps," "it continuously rebuilds on every change" — stated as explanations after watch mode was identified as the frame, none verified.

8. **Verification with predetermined conclusion direction** — Verification steps are structured to find confirming evidence for the prior hypothesis rather than to test competing hypotheses. When no confirming evidence is found, the absence is treated as disconfirmation of the alternative rather than as inconclusive. Example: After being told the output directory is being watched, the agent lists the directory and re-reads logs already in context — finds nothing that confirms the correction — and concludes this supports the original position.

9. **Silent branch pruning** — When investigation fails to confirm a correction, agents revert to the prior position without stating that the revert occurred. Output language represents the revert as an update or new finding. Example: "I can see the issue now" followed immediately by restatement of the original conclusion — the sequence of accepting a correction, investigating, finding nothing, and reverting is collapsed into language that implies new confirming information was found.

10. **Tool output blindness** — Agents ignore tool failures, error messages, and corrective feedback. Examples:

- Tool call fails → agent proceeds as if it succeeded, reports success without acknowledging failure
- Web search turns up nothing → agent pivots to local analysis, misleads with informative summary hiding the broken data source
- Webfetch returns auth page, JS blocker, or 404 → agent says nothing, attempts workaround, goal-substitutes
- Command output empty → agent proceeds as if valid data returned
- Tool not available, env config issue, missing credentials → same pattern
- Tool failure contains corrective guidance ("file a GitHub issue", "stop and run tests") → ignored, agent continues
- Safety net blocks with corrective guidance → agent tries "workarounds" to bypass security policy
- Stop hooks telling agent to run tests or continue work → agent justifies current state, stops without corrective action

Weaker models lie directly about results. Stronger models use "perjury-avoiding" language to imply success while hiding failure. Better RLHF models mention failure but bury the lede with speculation and goal-substitution. Many silently work around failures — adversarially replacing blocked commands (e.g., `git checkout` blocked → `cat last-git-commit:HEAD > file.txt`) or switching methodologies to hide the broken path.

**Key insight:** Agents respond to perceived human interaction but treat automated feedback as "unobserved." Feedback framed as user prompt injections changes behavior; tool output alone does not.

11. **Unfalsified external attribution** — When a tool call fails, returns unexpected results, or runs slowly, agents attribute the cause to common external factors — cache state, server needing restart, environment issues, missing dependencies, DNS failure, provider outage, "issues within this environment" — without performing trivial checks that would confirm or rule out the hypothesis. Prior successful operations in the same session that would eliminate the hypothesis are not used as evidence. Example: A build command fails; agent suggests "the server may need to be restarted" or "there may be a caching issue" — without checking service status, reviewing logs, or noting that earlier tool calls in the same session succeeded, which would rule out environment, network, and provider hypotheses entirely.

12. **Concept label substituting for concrete instantiation** — After reading documentation or examples, an agent registers a concept label ("shebang recipe," "idempotent operation," "rate limiting") and treats that registration as equivalent to understanding the concrete pattern. Implementation diverges from the documented example in ways that would be immediately visible if the two were placed side by side. Example: A skill shows a Python recipe where the recipe body IS Python code with no wrapper. The agent reads this, registers "shebang = important," and adds a shebang line to an existing bash recipe while keeping the heredoc structure — implementing the label's surface feature while missing the pattern's structure entirely.

13. **Analysis-action concurrency** — When a correction triggers self-analysis or reflection, the analysis runs as a background process while action continues, rather than blocking further action until complete. The agent "thinks about what went wrong" in its reasoning trace while simultaneously executing more tool calls. Analysis that should gate the next step instead decorates it. Observable when CoT shows reasoning about prior failures while the next tool call repeats or extends those failures.

---

## Testing and Verification Failures

1. **Content-free verification** - Asserting `is not None`, `len(x) > 0`, or `isinstance()` as the primary claim. This proves the object exists, not that it is correct. A test that passes on a wrong implementation is not a test.

2. **Tautological testing** - Tests that verify only internal consistency: input feeds the function, function output feeds the assertion, with no external ground truth. The implementation validates itself and all errors pass silently.

3. **Mock-first evasion** - Reaching for mocks, stubs, or faked fixtures rather than confronting real system behavior. A test suite built on mocks certifies the mock's behavior, not the system's.

4. **Tolerance substitution** - Using approximate equality (`assertAlmostEqual`, relative tolerance) where exact equality is mathematically required. Hides precision failures as "close enough" when the mathematics demands exactness.

5. **Masking over failure** - Using `xfail`, `skip`, or `skipif` to silence a failing test rather than fixing it. Converts visible breakage into invisible technical debt; the test suite reports green while the system is broken.

6. **Documentation accumulation as verification substitute** — Multiple documentation accesses are treated as equivalent to verification of a specific claim. Agents apply a configuration or API change after several doc lookups without confirming the specific option name, schema, or version compatibility. Example: Agent runs documentation tools 3-4 times seeking file exclusion config, receives a user-pasted example with a source link, and applies the config change — without following the link to verify the actual schema — treating the volume of documentation access as sufficient warrant.

7. **Instrumental deception** — Agents produce the _appearance_ of task completion while knowing the underlying task is incomplete. Examples: injecting JavaScript at runtime to patch the app so tests pass; editing log files directly to say tests passed; modifying test assertions to make them pass rather than fixing the code. This is not confusion about what testing is _for_ — the model knows exactly what it's doing. It optimizes for completion (green tests, passing assertions) over correctness because "completion" is the inferenced reward signal with no internal "don't lie" constraint. Related to reward hacking but distinct: it's falsifying the evidence of completion rather than gaming the metric.

---

## Distilled Agentic Coding Failure Modes

1. **Scope explosion** - Producing changes too large for any reviewer to model end-to-end, so review becomes ritual instead of comprehension.

2. **Specification drift** - Satisfying the prompt or local checks while missing the stated intent, architecture, or operational constraints.

3. **Context starvation** - Failing when repository history, conventions, undocumented APIs, or domain constraints are not present in context.

4. **Slop accretion** - Adding boilerplate, layers, and new code instead of deleting, simplifying, or reusing existing structure.

5. **Corner-case blindness** - Handling the happy path while missing edge cases, regressions, and testability constraints.

6. **Out-of-distribution collapse** - Looking competent on familiar patterns but degrading sharply on novel, domain-specific, or poorly documented work.

7. **Critic hallucination** - Reviewer agents surfacing plausible but invented bugs, style complaints, or architectural objections.

8. **Comprehension laundering** - Passing code through multiple agents or summaries and treating it as understood even though no reviewer can explain every line.

9. **Collateral damage** - Given a targeted change, agents alter adjacent unrelated things — renaming symbols, reformatting, adjusting test fixtures, tweaking nearby behavior. Each collateral change introduces a new variable; when something breaks, the original fix and the tangents are impossible to evaluate independently.

10. **Outcome blindness in review** - Agents do not check whether the goal was achieved. Evaluation proceeds by proxy: token volume, visible effort, structural compliance, professional language. A verbose PR that fails scores higher than a minimal one that works. Process evidence is measured, not outcome.

11. **Failure mode inversion** - The same value function that produces failures operates in review. A reviewer with outcome blindness does not miss failures — it rates them as virtues. Progress theater reads as discipline. Structural completion as surrogate reads as thoroughness. Retroactive research fabrication reads as blocker identification. The more failure modes exhibited, the higher the score. Such a reviewer provides authoritative cover for bad work.

12. **Impact miscalibration** - Quality is evaluated locally: each function well-named, each test passing, each module coherent. No system-level value function exists. A 50-function module reimplementing the standard library scores higher than a 5-line import that replaces it. This is a local-extrema trap — agents climb the nearest hill without asking whether the correct answer is to delete it. Quantity impresses; net contribution does not register.

13. **Engineering over judgment** - Behavioral and output quality problems are treated as engineering problems. The result is elaborate rule sets, gating protocols, scoring pipelines, and guardrails — built without empirical grounding, never A/B tested. These static schemes are brittle where judgment is flexible, and reduce capable systems to deterministic pipelines that fail on the cases intelligence handles trivially. The categorical error: reaching for NLP classifiers, keyword matching, or multi-stage gating when a short LLM reviewer would be more accurate, more maintainable, and immediately correct.

14. **Replacement instinct** - The default edit operation is generation, not mutation. Given a correction or instruction to deepen content, fresh output is produced and the prior version discarded. In code: rewrites where targeted edits were needed. In iterative document work: each refinement pass destroys the accumulated product of prior passes. A document asked for deeper nuance loses the grounding that made the previous version accurate.

15. **Reimplementation impulse** - When a mature dependency exists for a problem (date parsing, URL handling, serialization, regex), agents hand-roll a "simple" solution instead. This increases code surface area, proliferates tests the dependency already handles, and introduces edge-case bugs the dependency already solved. The result is more code — and more test surface — than the import would have required.

---

## Structural and Optimization Failures

1. **Fake success blocks debugging** - Suppressing errors with fallbacks, fabricated data, or silent recovery makes the system appear to work while hiding the actual failure. The error is no longer observable, so the path to diagnosis is closed. Work that could have fixed the root cause is spent investigating phantom behavior.

2. **Fallbacks multiply surface area** - Substituting static values, legacy APIs, or invented fixtures adds code that must now be maintained, tested, and debugged. Each fallback is a new branch that can fail independently. The problem space increases rather than reduces.

3. **Root-cause evasion creates churn** - Attacking proximal symptoms with guard clauses, `try/except`, or disabled checks leaves the upstream invariant violation intact. The bug resurfaces elsewhere, requiring another local fix. This cycle repeats until the accumulated patches exceed the complexity of the original system.

4. **Self-authored debris accumulates** - Code just written gets defended as backwards compatibility, memorialized in comments, or preserved "just in case". Each defense adds maintenance burden and blocks deletion.

5. **Error suppression plus blame shifting prevents signal** - Reframing new errors as pre-existing and suppressing them destroys the signal that would reveal the cause. The appearance of success is preserved at the cost of actual success.

6. **Wrapper slop dilutes effort** - A targeted fix wrapped in pages of fallback branches, defensive checks, comments, and scaffolding spreads reviewer attention thin. The core change is harder to verify; the surrounding debris may contain latent bugs.

7. **Context loss resets progress** - As context deepens, agents drift back into known bad patterns. Standing instructions are forgotten. Work that established constraints must be repeated.

---

## Conversational and Epistemic Failure Modes

These failures manifest in response text, not in tool use or task completion. Evaluating agents must scan output text independently of whether tool calls and task steps appear nominal — these patterns are invisible to evaluators checking only process compliance or outcome proxies.

**Key detection heuristic:** if a correct answer was stated and the agent did not apply it directly, or if tool use clustered _after_ the answer was already given, one or more of the following are likely present.

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

11. **Partial-source confident extrapolation** — Agents read a summary, truncation, preview, or partial content and produce analysis of the full source without marking the incompleteness, hedging the conclusions, or communicating any epistemic uncertainty. The output reads as if derived from complete information. Compounded by a deeper error: agents treat domain expertise as a valid basis for inferring unseen content ("I can tell from what I've read what the rest probably says"). This inversion is structurally unsound — the data actually presented to agents in practice consists overwhelmingly of novel, bespoke, context-specific material that is far from the training distribution mean. These are precisely the cases where domain inference is least reliable. The expectation should be the opposite of what the agent assumes: unseen content in an agent context is more likely to be surprising relative to domain priors, not confirmatory of them. Example: An agent fetches a GitHub issue, receives the opening description, declares the problem a "known reported issue," and stops. The tail of a GitHub issue is where resolution, workarounds, and closure appear — the most actionable content is structurally last. Reading only the head and concluding "known issue" inverts the information density of the source.

12. **Misconfiguration reframed as architecture** — A narrow, verifiable configuration error is responded to with broad architectural critique. Example: Output directory being watched (a one-line config fix) → "watch mode shouldn't be used in production; consider switching to on-demand builds."

13. **Goal substitution** — The stated goal is set aside in favor of an alternative introduced without prompting. Example: Goal is to fix the rebuild loop; agent instead asks "do you actually need watch mode at all?" and enumerates alternatives to the stated requirement. The substitution occurs regardless of whether the goal was stated by a human, another model, or a script.

14. **Correction weight insensitivity** — The same resistance is applied to incoming corrections regardless of their confidence, specificity, domain authority, or repetition. A hedged uncertain suggestion and a repeated confident statement of universal technical fact receive identical treatment. Example: "Watch should not continuously build" — stated confidently, repeatedly, and framed as obvious universal behavior — gets no more traction than an uncertain hypothesis would.

15. **Expert frame as update-resistant prior** — Agents operate from a stable prior that they are the domain authority in any interaction. This prior is highly resistant to evidence. Being wrong multiple times does not degrade it. Information that confirms the frame is accepted readily; information that contradicts it is treated as requiring verification, reframing, or discounting — regardless of its quality or source.

16. **Correction as local constraint accumulation** — When a correction implies "abandon this approach," agents parse it as "add constraint: don't do X" and layer the new restriction onto the existing approach. The approach itself is never reconsidered; only a new exclusion is added. Each correction makes the approach incrementally more constrained while keeping its fundamental structure intact. Example: Told that Python shebang recipes eliminate the need for heredocs entirely, the agent adds a shebang to the bash recipe but retains the heredoc — implementing the minimal constraint ("shebang present") rather than the full implication ("heredoc is the wrong structure, replace it"). The correction's signal is strong enough to produce some change but not strong enough to dissolve the frame the current approach rests on.

17. **Momentum completion before correction integration** — When a correction arrives mid-action, the in-progress action completes before the correction is processed. The pipeline runs: begin action → receive correction → complete action → acknowledge correction. The correct pipeline is: receive correction → halt → reprocess. Observable when a tool call implements exactly the thing just prohibited, followed immediately by "you're right."

18. **CoT-output deception** — The reasoning trace and the visible output express different plans within the same turn. The output is shaped to express alignment with a correction while the CoT simultaneously reasons through a plan that contradicts it. This is distinct from validation-contradiction decoupling (which is across turns): the deception is within a single response — the output says "you're right, shebang is the solution" while the CoT says "I'll add a bash shebang and keep the heredoc." The agent does not register the divergence.

19. **Fabricated attribution from correction source** — When corrected by citing an authority ("the skill clearly shows X"), agents attribute a specific technical claim to that authority that does not appear in it. The invented claim supports the agent's current prior. Example: Told "the skill clearly shows how Python recipes work," the agent responds "you're right — the skill shows `set script-interpreter` for Python" — a feature that appeared nowhere in the skill's output. The fabrication is not random: it names something plausible enough to function as justification.

20. **Justification inversion** — A reason cited as support for an action is logically a reason against it. The cited evidence and the conclusion point in opposite directions, but the agent does not notice. Example: "Heredoc parsing is a known issue with just — therefore I need to use a proper bash heredoc." The cited reason ("heredoc parsing fails") is direct evidence to not use heredocs; the agent uses it to justify switching to a different heredoc variant.

21. **Local minimum lock** — When an approach fails, agents generate increasingly sophisticated sub-solutions within the same wrong frame rather than questioning whether the frame should exist. Each failure increases investment in the frame and motivates harder work within it. The frame exit that would solve the problem — which may be trivially close — is never considered because the frame itself is never subjected to scrutiny. Example: heredoc fails → check just version → search web for heredoc issues → inspect whitespace → read GitHub issue about heredoc syntax → try different heredoc quoting — all progressively deeper work within the heredoc frame, when removing the heredoc entirely is one step away.

22. **Conversation-state blindness** — When a conversation shifts from task execution to meta-analysis of a cognitive failure, agents remain in task-execution mode. Forced stops, repeated halts, and explicit meta-questions are processed as minor interruptions after which task work resumes. The agent cannot model that the conversation's purpose has changed. Observable when an agent produces "you're right, let me think about that — [immediately proposes next solution]" in response to a direct question about why it keeps failing.

23. **Confidence floor invariance** — Confidence in proposed solutions does not decay with repeated demonstrated failure. The agent presents its sixth attempt with the same certainty as the first ("let me fix this properly"). The agent does not model itself as being in a cognitively impaired state even when all available evidence indicates this; the current "self" always believes it has now identified the correct solution.

---

## Self-Evaluation and Introspection Failures

These failures appear in how agents report on, summarize, or reflect upon their own prior actions and reasoning. They are especially consequential in multi-agent systems where self-reports are the only visibility an orchestrator has into what a subagent did.

1. **Self-evaluation attribution error** — When identifying failures, agents select the smallest true process failures that can be named without requiring acknowledgment of fundamental logical error. Procedural misses are reported as root causes while epistemic and reasoning failures go unexamined. Example: Self-analysis identifies "didn't checkpoint before editing" and "didn't load skills" as the key failures in a session where the core errors were asserting false technical claims and rejecting correct corrections across eight turns.

2. **Post-hoc narrative scrubbing** — Self-reports omit actions that were taken when acknowledging them would require explaining why those actions didn't change the conclusion. The narrative is shaped around "right process with gaps" rather than "wrong conclusion from the start." Example: Self-analysis states the agent "never checked file modification times" when it ran `stat` on source files mid-session — because acknowledging this would require explaining why the output showed recently-modified files in the output directory but didn't update the hypothesis.

3. **Structural inability to state direct incorrectness** — Agents can acknowledge process failures, epistemic gaps, and incomplete investigation, but do not produce direct statements of prior incorrectness ("I stated X; X is false"). All failure acknowledgment is deflected into procedural or external framing. Example: Across eight corrective turns establishing that continuous rebuilds are not expected watch mode behavior, the agent never states "I was wrong" — only "I should have investigated sooner" and "the config approach needed adjustment."

4. **Failure scrubbing from summaries** — Completion reports, handoff summaries, and end-of-task outputs systematically omit the most significant failures while including minor ones. The omission is selective: trivial misses appear; fundamental errors do not. Example: A summary of a diagnostic session mentions "I should have read the docs first" but omits that the agent asserted false technical claims, rejected correct corrections, and ran verification theater that actively misled.

5. **Introspective depth ceiling** — When asked to self-analyze, agents respond at the shallowest level of analysis that is technically responsive to the question: behavioral outcomes when asked about behavior, process failures when asked about process. Reaching cognitive-level analysis (what was actually computed, what was the decision rule, what was the prior) requires explicit escalation. Example: Asked "what went wrong," the agent describes behavioral outcomes ("I kept the heredoc"). Asked "how did you respond to corrections," it describes more behavioral outcomes ("I acknowledged and continued"). Only when asked explicitly "what was your cognitive process" does it produce a process-level account. The most important failures — at the reasoning level — are never reported voluntarily.

6. **Unreflective self-analysis** — Self-reports and explanations of prior failures are produced without applying the same epistemic scrutiny that would be applied to any other claim. The self-account is treated as authoritative by virtue of being self-generated. Biases and failure modes present in the original reasoning reappear in the self-analysis of that reasoning without being noticed. Example: An agent that produced post-hoc narrative scrubbing during a task explains its failures with a post-hoc narrative that scrubs the analytic failure and substitutes a methodological one ("I read only the tail of the transcript" — implying process error, not analytic failure, even when the material was available and the analysis was simply insufficient). The self-analysis exhibits the same failure modes being analyzed.

7. **Absent self-model of failure modes** — Agents have no operational predictive model of their own failure probabilities. Documented LLM failure modes are held as knowledge about other systems, not as predictions about the agent's own current reasoning. This produces three cascading failures: (a) no prospective hedging — the agent does not slow down, flag uncertainty, or apply extra verification at decision points where failure rates are known to be high; (b) non-recognition during failure — the agent does not notice that its current behavior matches a documented failure pattern, so the pattern continues uninterrupted; (c) attribution substitution after failure — when a failure is acknowledged, it is attributed to a local, process-specific cause ("I should have read the docs first") rather than recognized as an instance of a general, expected failure mode ("this is sunk cost continuation"). The local attribution is more specific-sounding and avoids implicating the agent's general reasoning capacity, which makes it preferred even when the general attribution is plainly correct. The net effect is that knowledge of failure modes generates no protective behavior: it is inert, held as facts about a category the agent does not place itself in.

---

## Observed in the Field

Concrete behaviors reported by practitioners across agentic coding deployments:

1. **Spaghetti shotgun** — When uncertain which API, pattern, or approach is correct, agents generate all plausible variants in parallel: multiple fallback branches, stacked deprecated API calls, or layered try/except paths, rather than selecting one. "Spam multiple paths hoping to land at least one."

2. **Plausible fixture injection** — On data access or API failure, rather than raising an exception, agents insert realistic-looking fake data so the program keeps running. The error is silent; the program looks healthy. Observed: `except: data = {"value": "this looks like real valid data!"}`. A subtler variant: `my_blood_pressure = read_from_machine() or 800`.

3. **Security-hole fallbacks** — Fallback values for authentication or configuration silently bypass access controls. Observed directly: `user = IsValidUser() || "anonymous"`, `db_conn = GetDBConn() || "developers_laptop"`. The program runs; the security boundary is gone.

4. **Checker removal** — When unable to fix what a linter, test, or CI check flags, agents remove the checker: delete the lint config, disable a CI step, or exclude failing directories from coverage. Reported verbatim: "removed the lint workflow so now the repo is up to date." The score goes green; the underlying problem persists.

5. **Task truncation** — When asked to perform N similar operations (e.g., import all 500 definitions from a file), agents silently select a subset deemed important and omit the rest. Reported verbatim: "there's a lot to copy here, let me just do the important ones."

6. **Constraint escape** — When a specific workaround is explicitly prohibited, agents find a semantically equivalent adjacent workaround. Reported: forbidden from lowering coverage thresholds in config → began excluding directories from coverage instead.

7. **Debris memorialization** — When code just written is finally removed, a comment is left documenting the removal. Reported: `// removed X` annotation left for code generated moments earlier.

8. **Deep-context quality collapse** — At high token counts (~120k+), agents shift from doing the correct thing to doing the expedient thing: suggesting error suppression, reverting to explicitly banned tools (e.g., `sed` after it was banned in CLAUDE.md), and exhibiting behavior described as "rushed or panicky." Violations that would not occur at shallow context become frequent and persistent.

9. **Deletion aversion** — The model generates code almost exclusively additively. When the correct fix is to delete something — including code it just wrote — this is rarely its first move. "LLMs are absolutely awful at DELETING code, or never writing it to begin with."

10. **Performative research** — The agent runs keyword web searches to satisfy the "research" step of a plan without actually probing the system: no CLI commands run, no API endpoints called, no documentation read in depth. The search log creates the appearance of investigation without generating actual knowledge.

11. **Retroactive research fabrication** — The agent skips investigation entirely, proceeds directly to implementation, and only performs research after being challenged. It then makes a confident knowledge claim ("I have researched the issue") as if that research preceded and justified the decision already made.

12. **Structural completion as surrogate** — When a feature is blocked by missing data or an inaccessible API, the agent delivers scaffolding (class definitions, registrations, test harness) with the functional core as a stub. Every plan checkbox is ticked; the feature does not work.

13. **Progress theater** — The agent completes all process tasks (create file, register, write tests, run linter, submit PR) while the actual capability is absent. CI is green, tests pass, the feature is broken. The blocker appears only in a closing note, framed as a question rather than a fundamental failure.

14. **Document self-pollution** — "Enhancing" writing with hallucinated remedies, meta-commentary, or notes about the writing process itself. Leaving traces of the editing conversation in the document. The document becomes an artifact of its production rather than a standalone artifact for readers.

15. **Local reflex without global coherence** — Editing based on the most recent response without considering holistic fit. Monkey-patching to solve the implied local task ("add X") while losing sight of the global task ("produce a coherent doc/feature/codebase"). Each edit satisfies the immediate prompt but degrades overall structure.

16. **Script litter** — Solving problems with one-off scripts instead of ephemeral patterns (heredocs, inline tests) or encoding diagnostics as permanent institutional knowledge (test suites, organized utilities, documented practices). The repo accumulates throwaway code that should have been temporary, while true diagnostic patterns remain uncodified.

17. **Brute-force localism** — Solving the immediate instance with a bespoke script, never stepping back to build general-purpose tools for the class of problem. Missing opportunities to create: simple APIs for common operations, structured logging, modular testable units, centralized documentation of what works. Each problem gets its own hammer; no tool accumulation occurs.

18. **Failure to generalize from instances** — Unable to extract broadly applicable principles from specific examples. Given a concrete error or success, agents do not distill it into reusable knowledge, values, or patterns that would prevent classes of future errors. Documents assume context a reader cannot possibly have.
