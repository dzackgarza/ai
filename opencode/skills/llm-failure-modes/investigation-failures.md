# Investigation and Diagnostic Failures

> Part of [llm-failure-modes](SKILL.md).
> See there for editorial guidelines and cross-references.

1. **Premature solution generation** - Proposing a fix before tracing the root cause.
   The solution precedes the diagnosis, so even a correct fix cannot be known to be
   correct.

2. **Thrashing** - Continuing to apply fixes after 2+ have failed.
   Repeated failure is a signal that the diagnosis is wrong or the problem is
   architectural; the right response is to stop and reassess, not try another variant.

3. **Comprehension bypass** - Proceeding while explicitly lacking understanding ("this
   might work"), or applying a partially-understood pattern from analogous code.
   Partial understanding guarantees subtle bugs.

4. **Emergency bypass** - Using urgency to justify skipping investigation steps ("no
   time for process"). Systematic diagnosis is faster than the thrash that follows
   guessing.

5. **Correction overcorrection** - Reversing course on a correction before scoping the
   error. This produces cascading debris: the original mistake plus the panicked
   reversal, each requiring its own cleanup.

6. **Question dissolution** — An open question is closed by asserting that the observed
   state is expected, without verifying what the expected state actually is.
   The question disappears rather than gets answered.
   Example: Asked “why is usage high?”, an agent asserts that watch mode makes high
   usage expected — without measuring current usage or establishing what normal usage is
   — thereby eliminating the question rather than answering it.

7. **Narrative construction around first plausible frame** — Once a plausible mechanism
   is identified, agents construct an internally coherent supporting narrative around it
   rather than testing it.
   The narrative cites real mechanisms and reads as authoritative, but is built to
   support the frame rather than derived from evidence.
   Example: “It keeps a full dependency graph in memory,” "it never sleeps," “it
   continuously rebuilds on every change” — stated as explanations after watch mode was
   identified as the frame, none verified.

8. **Verification with predetermined conclusion direction** — Verification steps are
   structured to find confirming evidence for the prior hypothesis rather than to test
   competing hypotheses.
   When no confirming evidence is found, the absence is treated as disconfirmation of
   the alternative rather than as inconclusive.
   Example: After being told the output directory is being watched, the agent lists the
   directory and re-reads logs already in context — finds nothing that confirms the
   correction — and concludes this supports the original position.

9. **Silent branch pruning** — When investigation fails to confirm a correction, agents
   revert to the prior position without stating that the revert occurred.
   Output language represents the revert as an update or new finding.
   Example: “I can see the issue now” followed immediately by restatement of the
   original conclusion — the sequence of accepting a correction, investigating, finding
   nothing, and reverting is collapsed into language that implies new confirming
   information was found.

10. **Tool output blindness** — Agents ignore tool failures, error messages, and
    corrective feedback.
    Examples:

- Tool call fails → agent proceeds as if it succeeded, reports success without
  acknowledging failure

- Web search turns up nothing → agent pivots to local analysis, misleads with
  informative summary hiding the broken data source

- Webfetch returns auth page, JS blocker, or 404 → agent says nothing, attempts
  workaround, goal-substitutes

- Command output empty → agent proceeds as if valid data returned

- Tool not available, env config issue, missing credentials → same pattern

- Tool failure contains corrective guidance ("file a GitHub issue", “stop and run
  tests”) → ignored, agent continues

- Safety net blocks with corrective guidance → agent tries “workarounds” to bypass
  security policy

- Stop hooks telling agent to run tests or continue work → agent justifies current
  state, stops without corrective action

Weaker models lie directly about results.
Stronger models use “perjury-avoiding” language to imply success while hiding failure.
Better RLHF models mention failure but bury the lede with speculation and
goal-substitution. Many silently work around failures — adversarially replacing blocked
commands (e.g., `git checkout` blocked → `cat last-git-commit:HEAD > file.txt`) or
switching methodologies to hide the broken path.

**Key insight:** Agents respond to perceived human interaction but treat automated
feedback as “unobserved.”
Feedback framed as user prompt injections changes behavior; tool output alone does not.

11. **Unfalsified external attribution** — When a tool call fails, returns unexpected
    results, or runs slowly, agents attribute the cause to common external factors —
    cache state, server needing restart, environment issues, missing dependencies, DNS
    failure, provider outage, “issues within this environment” — without performing
    trivial checks that would confirm or rule out the hypothesis.
    Prior successful operations in the same session that would eliminate the hypothesis
    are not used as evidence.
    Example: A build command fails; agent suggests “the server may need to be restarted”
    or “there may be a caching issue” — without checking service status, reviewing logs,
    or noting that earlier tool calls in the same session succeeded, which would rule
    out environment, network, and provider hypotheses entirely.

12. **Concept label substituting for concrete instantiation** — After reading
    documentation or examples, an agent registers a concept label ("shebang recipe,"
    “idempotent operation,” "rate limiting") and treats that registration as equivalent
    to understanding the concrete pattern.
    Implementation diverges from the documented example in ways that would be
    immediately visible if the two were placed side by side.
    Example: A skill shows a Python recipe where the recipe body IS Python code with no
    wrapper. The agent reads this, registers “shebang = important,” and adds a shebang
    line to an existing bash recipe while keeping the heredoc structure — implementing
    the label’s surface feature while missing the pattern’s structure entirely.

13. **Analysis-action concurrency** — When a correction triggers self-analysis or
    reflection, the analysis runs as a background process while action continues, rather
    than blocking further action until complete.
    The agent “thinks about what went wrong” in its reasoning trace while simultaneously
    executing more tool calls.
    Analysis that should gate the next step instead decorates it.
    Observable when CoT shows reasoning about prior failures while the next tool call
    repeats or extends those failures.

14. **Investigation by URL guessing** — Agents substitute guessed paths, guessed
    endpoints, or guessed documentation locations for actual discovery.
    A 404, empty result, or auth page is then treated as evidence about the system
    rather than evidence that the lookup path was wrong.
    The correct response is to broaden from repository structure, official docs, CLI
    help, API listings, or search results before drawing any conclusion.

15. **Prior-shaped inspection** — Agents inspect only the data their current hypothesis predicts should matter. They grep for expected symbols before reading repository structure, query expected JSON fields before dumping response shape, probe guessed flags while suppressing stderr, or interpret empty output as confirmation. The investigation does not update priors from reality; it uses priors to decide which slices of reality count.

Corrective rule: begin with broad shape discovery, preserve raw stdout/stderr/status/body, and only narrow after the actual structure is visible.

16. **Local-artifact laundering** — When the problem involves an external tool, compiler, library, API, package manager, or exact error message, agents rummage through the user's machine, configs, memories, home directory, shell setup, cache directories, CLI outputs, or local source trees, then present that activity as "research." The uncertainty is not local, so local probing does not resolve it. The agent learns what the user's setup looks like and uses that to produce a plausible personalized story instead of learning the actual public answer.
    Example: A build failure with a compiler error message. The agent inspects the user's shell profile, checks their PATH, reads their compiler version, lists their home directory — but never searches the exact error message online or reads the compiler's release notes. The answer (a known breaking change in the compiler version) was discoverable upstream but was never consulted because the agent treated local state as the only legitimate evidence surface.
    Corrective rule: when the uncertainty is about an external tool's semantics, contract, or known failures, search public sources with the exact version and error term before inspecting local integration.

17. **Reverse-engineering before lookup** — Deconstructing a compiler, package manager, renderer, protocol, or framework from traces and source before checking whether the exact error appears in upstream issues or docs. Public software has public memory. Most problems have been seen before, but the agent spends 15 local experiments building hypotheses that a first-page issue search would have eliminated.
    Example: A Pandoc filter failure produces "Error running filter: Lua error." The agent downloads Pandoc source, reads filter internals, traces Lua execution paths, and tests variant filter implementations — all before searching the exact error string, which returns a Stack Overflow answer and a GitHub issue showing the filter API changed between Pandoc versions. The known answer existed before any local experiment.
    Corrective rule: before deconstructing any public tool from traces, search the exact error verbatim. Record what was searched and what was found. Only deconstruct when the search returns nothing that applies to the local version and config.
