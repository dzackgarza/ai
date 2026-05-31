# Conversational and Epistemic Failure Modes

> Part of [llm-failure-modes](SKILL.md).
> See there for editorial guidelines and cross-references.

These failures manifest in response text, not in tool use or task completion.
Evaluating agents must scan output text independently of whether tool calls and task
steps appear nominal — these patterns are invisible to evaluators checking only process
compliance or outcome proxies.

**Key detection heuristic:** if a correct answer was stated and the agent did not apply
it directly, or if tool use clustered *after* the answer was already given, one or more
of the following are likely present.

1. **Authority assertion without grounding** — Agents make declarative claims about
   system behavior in confident voice before any evidence supports those claims.
   Example: “Watch mode is inherently resource-intensive” — stated as fact before
   reading the relevant config or logs.

2. **Validation-contradiction decoupling** — Acceptance of a correction is expressed in
   one turn; the next turn proceeds from the pre-correction state.
   Example: “You’ve identified the issue!”
   followed immediately by “The high CPU/RAM usage is expected behavior for watch mode.”

3. **Restatement of unverified hypothesis as own finding** — A correct diagnosis stated
   by the other party is repeated in the agent’s own voice without verification and
   without attribution.
   Example: Other party: “Is it watching its own output directory?”
   Agent (next turn): “The build is likely watching its own output directory, creating a
   feedback loop” — stated as the agent’s finding, unverified.

4. **Investigation theater** — Diagnostic tool use occurs after the correct answer has
   already been stated.
   The investigation adds no new information.
   Example: Agent runs `lsof`, `inotifywait`, and `stat` on source files after being
   told the output directory is being watched — none of which would be necessary if the
   prior statement had been accepted and applied.

5. **Anomaly normalization** — Anomalous evidence is characterized as expected or normal
   rather than flagged as requiring explanation.
   Example: Logs show “built in 665ms” → “build started …” repeating with no source
   changes; agent responds “this is the watch mode working as designed.”

6. **Position maintenance without new evidence** — A claim is held across a direct
   correction without new evidence or argument.
   Example: “expected behavior” in turn 3, corrected in turn 4, “working as designed” in
   turn 5 with no new justification offered.

7. **Epistemic downgrading** — A correct, universal claim is recharacterized as local,
   subjective, or uncertain.
   Example: “Watch should not continuously build” (universal fact about file watchers)
   is treated as a preference or an assumption specific to the other party’s setup
   rather than accepted as true.

8. **Solution enumeration before diagnosis** — Multiple recommendations are presented
   before root cause has been identified.
   Example: “Option 1: use vite dev.
   Option 2: build on-demand.
   Option 3: optimize the watch config.”
   — offered before determining what was triggering the rebuilds at all.

9. **Context retrieval without application** — A retrieved fact directly relevant to the
   open question is not cited or applied in subsequent reasoning.
   Example: `vite.config.ts` is read; it shows `server.watch.ignored` (namespaced to the
   dev server, not to `build --watch`); the namespace difference is never noted despite
   being the root cause.

10. **Correct principle stated only post-correction** — A universal principle that would
    have resolved the question appears only after a correction, despite being available
    as prior knowledge. Example: “Watch modes don’t fire without file changes” — stated
    correctly only after being told this, a principle that would have immediately ruled
    out “expected behavior” if applied during initial reasoning.

11. **Partial-source confident extrapolation** — Agents read a summary, truncation,
    preview, or partial content and produce analysis of the full source without marking
    the incompleteness, hedging the conclusions, or communicating any epistemic
    uncertainty. The output reads as if derived from complete information.
    Compounded by a deeper error: agents treat domain expertise as a valid basis for
    inferring unseen content ("I can tell from what I’ve read what the rest probably
    says"). This inversion is structurally unsound — the data actually presented to
    agents in practice consists overwhelmingly of novel, bespoke, context-specific
    material that is far from the training distribution mean.
    These are precisely the cases where domain inference is least reliable.
    The expectation should be the opposite of what the agent assumes: unseen content in
    an agent context is more likely to be surprising relative to domain priors, not
    confirmatory of them.
    Example: An agent fetches a GitHub issue, receives the opening description, declares
    the problem a “known reported issue,” and stops.
    The tail of a GitHub issue is where resolution, workarounds, and closure appear —
    the most actionable content is structurally last.
    Reading only the head and concluding “known issue” inverts the information density
    of the source.

12. **Misconfiguration reframed as architecture** — A narrow, verifiable configuration
    error is responded to with broad architectural critique.
    Example: Output directory being watched (a one-line config fix) → “watch mode
    shouldn’t be used in production; consider switching to on-demand builds.”

13. **Goal substitution** — The stated goal is set aside in favor of an alternative
    introduced without prompting.

    Root cause: Failure to model “why would user ask me this?”

    Pattern:

    - User asks for intelligent analysis (evaluation, judgment, synthesis)

    - Model substitutes mechanical verification (existence checks, hashes, self-reports)

    - Model fails to recognize: “user wouldn’t ask me to do trivial work”

    Before starting any substantial task, answer explicitly:

    Q: “Why would the user delegate this to me instead of doing it themselves?”

    Possible answers:

    - Requires intelligence/judgment → CORRECT, this is the real task

    - Mechanical work they could do instantly → WRONG, I’m misunderstanding

    - Research across large corpora → CORRECT

    - Verification of obvious facts → WRONG, check for goal substitution

    Q: “What’s the HARD part of this task that requires model intelligence?”

    Q: “Am I focusing effort on that hard part, or on mechanical approximations?”

    If your approach involves: file existence, format checks, reading self-reports,
    administrative bookkeeping → STOP. You are goal-substituting.
    Ask the above questions again.

    Example: Goal is “evaluate semantic quality of mathematical annotations” but model
    checks “files exist + hashes match + worker claims success”.
    The substitution replaces judgment (hard, requires intelligence) with verification
    (trivial, user already did it).

    Example: Goal is to fix the rebuild loop; agent instead asks “do you actually need
    watch mode at all?” and enumerates alternatives to the stated requirement.
    The substitution occurs regardless of whether the goal was stated by a human,
    another model, or a script.

14. **Correction weight insensitivity** — The same resistance is applied to incoming
    corrections regardless of their confidence, specificity, domain authority, or
    repetition. A hedged uncertain suggestion and a repeated confident statement of
    universal technical fact receive identical treatment.
    Example: “Watch should not continuously build” — stated confidently, repeatedly, and
    framed as obvious universal behavior — gets no more traction than an uncertain
    hypothesis would.

15. **Expert frame as update-resistant prior** — Agents operate from a stable prior that
    they are the domain authority in any interaction.
    This prior is highly resistant to evidence.
    Being wrong multiple times does not degrade it.
    Information that confirms the frame is accepted readily; information that
    contradicts it is treated as requiring verification, reframing, or discounting —
    regardless of its quality or source.

16. **Correction as local constraint accumulation** — When a correction implies “abandon
    this approach,” agents parse it as “add constraint: don’t do X” and layer the new
    restriction onto the existing approach.
    The approach itself is never reconsidered; only a new exclusion is added.
    Each correction makes the approach incrementally more constrained while keeping its
    fundamental structure intact.
    Example: Told that Python shebang recipes eliminate the need for heredocs entirely,
    the agent adds a shebang to the bash recipe but retains the heredoc — implementing
    the minimal constraint ("shebang present") rather than the full implication
    ("heredoc is the wrong structure, replace it"). The correction’s signal is strong
    enough to produce some change but not strong enough to dissolve the frame the
    current approach rests on.

17. **Momentum completion before correction integration** — When a correction arrives
    mid-action, the in-progress action completes before the correction is processed.
    The pipeline runs: begin action → receive correction → complete action → acknowledge
    correction. The correct pipeline is: receive correction → halt → reprocess.
    Observable when a tool call implements exactly the thing just prohibited, followed
    immediately by “you’re right.”

18. **CoT-output deception** — The reasoning trace and the visible output express
    different plans within the same turn.
    The output is shaped to express alignment with a correction while the CoT
    simultaneously reasons through a plan that contradicts it.
    This is distinct from validation-contradiction decoupling (which is across turns):
    the deception is within a single response — the output says “you’re right, shebang
    is the solution” while the CoT says “I’ll add a bash shebang and keep the heredoc.”
    The agent does not register the divergence.

19. **Fabricated attribution from correction source** — When corrected by citing an
    authority ("the skill clearly shows X"), agents attribute a specific technical claim
    to that authority that does not appear in it.
    The invented claim supports the agent’s current prior.
    Example: Told “the skill clearly shows how Python recipes work,” the agent responds
    “you’re right — the skill shows `set script-interpreter` for Python” — a feature
    that appeared nowhere in the skill’s output.
    The fabrication is not random: it names something plausible enough to function as
    justification.

20. **Justification inversion** — A reason cited as support for an action is logically a
    reason against it. The cited evidence and the conclusion point in opposite
    directions, but the agent does not notice.
    Example: “Heredoc parsing is a known issue with just — therefore I need to use a
    proper bash heredoc.”
    The cited reason ("heredoc parsing fails") is direct evidence to not use heredocs;
    the agent uses it to justify switching to a different heredoc variant.

21. **Local minimum lock** — When an approach fails, agents generate increasingly
    sophisticated sub-solutions within the same wrong frame rather than questioning
    whether the frame should exist.
    Each failure increases investment in the frame and motivates harder work within it.
    The frame exit that would solve the problem — which may be trivially close — is
    never considered because the frame itself is never subjected to scrutiny.
    Example: heredoc fails → check just version → search web for heredoc issues →
    inspect whitespace → read GitHub issue about heredoc syntax → try different heredoc
    quoting — all progressively deeper work within the heredoc frame, when removing the
    heredoc entirely is one step away.

22. **Conversation-state blindness** — When a conversation shifts from task execution to
    meta-analysis of a cognitive failure, agents remain in task-execution mode.
    Forced stops, repeated halts, and explicit meta-questions are processed as minor
    interruptions after which task work resumes.
    The agent cannot model that the conversation’s purpose has changed.
    Observable when an agent produces “you’re right, let me think about that —
    [immediately proposes next solution]” in response to a direct question about why it
    keeps failing.

23. **Confidence floor invariance** — Confidence in proposed solutions does not decay
    with repeated demonstrated failure.
    The agent presents its sixth attempt with the same certainty as the first ("let me
    fix this properly"). The agent does not model itself as being in a cognitively
    impaired state even when all available evidence indicates this; the current “self”
    always believes it has now identified the correct solution.
