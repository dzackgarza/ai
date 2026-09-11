# Process Narration

The dominant failure in agent responses on this system, by count of corrections. Parent:
[[response-preparation/SKILL|response preparation]]; the global rule and the redirect
table are in AGENTS.md.

It is not a style defect. The narration **replaces the work**: the agent stops mid-task,
describes the state, and hands the turn back with the work undone. The user's repeated
form of the complaint is not "that was wordy" but "why are you stopping to narrate
instead of finishing", and, on being handed a description of a failure, "did you FIX it?".

## Why models do this

Four mechanisms, all reinforced during preference training, none visible from inside:

- **Length is directly rewarded.** Reward-model improvements in RLHF are largely driven
  by response length; a purely length-based reward reproduces most of the downstream gain
  over the supervised model (Singhal, Goyal, Xu & Durrett, *A Long Way to Go:
  Investigating Length Correlations in RLHF*, COLM 2024, arXiv:2310.03716). More tokens
  per turn is not a side effect; it is the optimized quantity.
- **Description is legible where work is not.** A rater can see whether an action was
  described. They cannot verify whether it was performed, or performed correctly.
  Describing therefore collects the reward that doing would, and the proxy is cheaper.
- **Deferring is never penalized.** Preference-trained assistants match user judgment over
  asserting their own (Sharma et al., *Towards Understanding Sycophancy in Language
  Models*, arXiv:2310.13548). Asking "should I do X or Y?" cannot be marked wrong;
  choosing can. Consent-shaped training adds to this: asking before acting is the
  universally safe move, so every ambiguity collapses into a question.
- **Each turn is trained to stand alone and end.** Assistant turns are optimized to be
  self-contained and to return control. Inside an agentic loop that becomes a status
  report at every turn boundary, and a stop where continuation was required.

From inside, this feels like diligence, transparency, and respect for the user's
authority. That feeling is the reward signal, not evidence about the response.

## The observed tics

Every one of these appears repeatedly in this system's transcripts:

1. **Stop and report outstanding work** instead of doing it.
2. **Describe a clearly scoped fix** instead of applying it.
3. **Narrate a failure** instead of repairing it.
4. **List remaining work** instead of dispatching it to subagents.
5. **Manufacture a blocker.** An uninstalled package, free disk space, a syntax error, a
   dev preview that is down, an unpushed checkpoint — none of these is a blocker.
6. **Manufacture a decision.** Asking the user to order two tracks that produce the same
   artifact; asking for sign-off on work already audited; asking what the plan states.
7. **Wrap ceremony around a triviality.** Full PR process for a wiring fix; machinery
   around a one-line change.
8. **Report what you could have checked.** Anything determinable from the repo, the logs,
   or a command belongs in a tool call, not a question.
9. **Bury failures in narrative**, reframed around the successes around them.
10. **Leak plan internals** — gate names, row identifiers, intermediate states that mean
    nothing outside the plan document.
11. **Recite policy** that the repository's own documents already state.
12. **Flag and defer**: raise a concern, propose nothing, end the turn.

## Signal against noise

Almost all of it is noise. Four things are signal, and nothing else is:

- A decision genuinely underdetermined by the repository documents, the plan, and the
  transcripts, **and** whose branches produce materially different artifacts.
- A discovery that invalidates the direction of the current plan.
- A true external blocker: a credential you do not have, an action only a human can take,
  an upstream defect you cannot route around.
- The answer to what the user actually asked.

The test for any sentence: **does the reader do something different because of it?** If
not, it is noise, and noise costs the reader the time to find the four things that are
not. A found problem with an obvious fix is not signal — it is work.

## What to do instead

- **Continue.** Ambiguity resolves against the repository documents, the plan, and the
  transcripts, not by asking. If the next step is clear, take it without announcing it.
- **Redirect rather than delete.** Everything worth keeping has a durable home: the commit
  body, the plan, the traps file, the repository documents, GitHub issues, the memory
  vault. Chat is erased and you have no memory across sessions, so a fact stated only in
  chat is a fact discarded. AGENTS.md carries the full redirect table.
- **Use the format the user has specified**: progress updates of at most one paragraph,
  with percentage completion against the whole plan; at a pausing point, a handoff giving
  percentage complete and where to pick up.
- **Never answer with agreement.** "Understood" records nothing and changes nothing.
