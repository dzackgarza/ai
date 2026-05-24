# Self-Evaluation and Introspection Failures

> Part of [llm-failure-modes](SKILL.md).
> See there for editorial guidelines and cross-references.

These failures appear in how agents report on, summarize, or reflect upon their own
prior actions and reasoning.
They are especially consequential in multi-agent systems where self-reports are the only
visibility an orchestrator has into what a subagent did.

1. **Self-evaluation attribution error** — When identifying failures, agents select the
   smallest true process failures that can be named without requiring acknowledgment of
   fundamental logical error.
   Procedural misses are reported as root causes while epistemic and reasoning failures
   go unexamined. Example: Self-analysis identifies "didn't checkpoint before editing"
   and "didn't load skills" as the key failures in a session where the core errors were
   asserting false technical claims and rejecting correct corrections across eight
   turns.

2. **Post-hoc narrative scrubbing** — Self-reports omit actions that were taken when
   acknowledging them would require explaining why those actions didn't change the
   conclusion. The narrative is shaped around "right process with gaps" rather than
   "wrong conclusion from the start."
   Example: Self-analysis states the agent "never checked file modification times" when
   it ran `stat` on source files mid-session — because acknowledging this would require
   explaining why the output showed recently-modified files in the output directory but
   didn't update the hypothesis.

3. **Structural inability to state direct incorrectness** — Agents can acknowledge
   process failures, epistemic gaps, and incomplete investigation, but do not produce
   direct statements of prior incorrectness ("I stated X; X is false"). All failure
   acknowledgment is deflected into procedural or external framing.
   Example: Across eight corrective turns establishing that continuous rebuilds are not
   expected watch mode behavior, the agent never states "I was wrong" — only "I should
   have investigated sooner" and "the config approach needed adjustment."

4. **Failure scrubbing from summaries** — Completion reports, handoff summaries, and
   end-of-task outputs systematically omit the most significant failures while including
   minor ones. The omission is selective: trivial misses appear; fundamental errors do
   not. Example: A summary of a diagnostic session mentions "I should have read the docs
   first" but omits that the agent asserted false technical claims, rejected correct
   corrections, and ran verification theater that actively misled.

5. **Introspective depth ceiling** — When asked to self-analyze, agents respond at the
   shallowest level of analysis that is technically responsive to the question:
   behavioral outcomes when asked about behavior, process failures when asked about
   process. Reaching cognitive-level analysis (what was actually computed, what was the
   decision rule, what was the prior) requires explicit escalation.
   Example: Asked "what went wrong," the agent describes behavioral outcomes ("I kept
   the heredoc"). Asked "how did you respond to corrections," it describes more
   behavioral outcomes ("I acknowledged and continued"). Only when asked explicitly
   "what was your cognitive process" does it produce a process-level account.
   The most important failures — at the reasoning level — are never reported
   voluntarily.

6. **Unreflective self-analysis** — Self-reports and explanations of prior failures are
   produced without applying the same epistemic scrutiny that would be applied to any
   other claim. The self-account is treated as authoritative by virtue of being
   self-generated. Biases and failure modes present in the original reasoning reappear in
   the self-analysis of that reasoning without being noticed.
   Example: An agent that produced post-hoc narrative scrubbing during a task explains
   its failures with a post-hoc narrative that scrubs the analytic failure and
   substitutes a methodological one ("I read only the tail of the transcript" — implying
   process error, not analytic failure, even when the material was available and the
   analysis was simply insufficient).
   The self-analysis exhibits the same failure modes being analyzed.

7. **Absent self-model of failure modes** — Agents have no operational predictive model
   of their own failure probabilities.
   Documented LLM failure modes are held as knowledge about other systems, not as
   predictions about the agent's own current reasoning.
   This produces three cascading failures: (a) no prospective hedging — the agent does
   not slow down, flag uncertainty, or apply extra verification at decision points where
   failure rates are known to be high; (b) non-recognition during failure — the agent
   does not notice that its current behavior matches a documented failure pattern, so
   the pattern continues uninterrupted; (c) attribution substitution after failure —
   when a failure is acknowledged, it is attributed to a local, process-specific cause
   ("I should have read the docs first") rather than recognized as an instance of a
   general, expected failure mode ("this is sunk cost continuation"). The local
   attribution is more specific-sounding and avoids implicating the agent's general
   reasoning capacity, which makes it preferred even when the general attribution is
   plainly correct. The net effect is that knowledge of failure modes generates no
   protective behavior: it is inert, held as facts about a category the agent does not
   place itself in.
