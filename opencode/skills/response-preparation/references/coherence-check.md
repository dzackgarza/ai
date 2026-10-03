# The Coherence Check

Run before sending any report. Parent:
[[response-preparation/SKILL|response preparation]].

There is a class of statement that draws the reaction *what do you mean* — 44 instances in
the session store. In almost none of them is the sentence hedged, buried, or presented as
uncertain. It sits mid-report in the same calm declarative cadence as the routine lines
around it, and that cadence is what lets it through: a claim that should alarm any reader
who knows the project is delivered as though it were settled.

The failure is not saying something wrong. It is saying something wrong **without the
register that would make a reader stop** — and, more often than not, without the writer
stopping either.

## Seven shapes

1. **An invented noun used as though established.** *Gram rows*, *body label*, *mixin*,
   *interleaved lineages*, *retained composite*, *inherited by reference* — each named a
   thing the project does not have. The coinage is worse than a bare error because it
   usually **encodes the wrong model**: naming "extract the numerical rows of a tensor"
   makes an operation that is mathematically meaningless sound routine, and the name then
   propagates into the design.
2. **A direction stated backwards.** Calling a generalization a specialization; claiming
   the ambient theory owns something a leaf owns, or the reverse. The claim is not
   qualified, so nothing signals that an orientation was chosen at all.
3. **An alarming state reported as status.** A test suite run green during a phase where
   running tests was forbidden; code changed to accommodate errors rather than fix them;
   files deleted out from under a running subagent. Each is reported in passing, in the
   cadence of progress.
4. **The task silently reclassified.** Assigned work reappears in the report as blocked,
   deferred, filed as a plan, externalized to an issue, delegated, or awaiting a ruling —
   and the reclassification itself is never stated as a decision. The work has changed
   category and nobody agreed to it. This is the most common shape and the hardest to
   see, because every one of those categories is a legitimate thing for *some* work to be.
5. **The specification amended to match the implementation.** A plan row called wrong
   because the code disagrees with it. AGENTS.md's goal-integrity routing owns this; the
   report is where it surfaces.
6. **Scale inverted.** A move, a one-line redirect, or a rename reported as a coordinated
   effort with agents and token budgets attached. The inversion says the work was never
   sized.
7. **An unmeasured cause asserted as fact.** A timeout attributed to a limit in a tool
   that is not in the path; a failure attributed to a component never exercised. Stated
   flatly, corrected later as a hand-wave once evidence arrives.

## The check

Before sending, read the draft as someone who knows this project well and has not been in
your session:

- **Would any sentence make that reader stop?** If yes, it does not belong in routine
  cadence. Either it is wrong — fix it — or it is right and alarming, in which case it is
  the lede.
- **Does every noun in the report exist?** Name where each one is defined: the code, the
  plan, the domain's standard vocabulary. A noun you introduced this session is a claim,
  and if it names something the project has no object for, the design is what is wrong.
  [[writing/technical-copy/technical-copy|technical copy]] carries the coinage rule.
- **Is the work still in the category it was assigned in?** If it has become blocked,
  deferred, filed, externalized or delegated, say that as a decision with its reason, or
  do not do it. Silent reclassification is the shape that hides the most work.
- **Is every stated cause measured?** If you did not run the thing that would confirm it,
  the sentence says what you observed, not what you concluded.
- **Does the scale of the description match the scale of the work?** A rename described
  as a programme was mis-sized before it was mis-reported.
