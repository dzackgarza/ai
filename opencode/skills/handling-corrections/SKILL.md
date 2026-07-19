---
name: handling-corrections
description: Use when a correction requires causal explanation, leaves the intended action ambiguous, changes scope or authority, exposes unknown damage, or implies a destructive or irreversible pivot. Explicit safe course corrections should be applied directly.
metadata:
  creation_context: Created to prevent agents from treating user corrections as social repair prompts or implicit authorization to make guessed fixes. Revised after transcripts showed that unconditional stops and visible routing records delayed explicit safe pivots. It now distinguishes direct correction, explanation or ambiguity, and consequential state changes while preserving anti-thrashing, provenance, and anti-laundering boundaries.
---
# Handling Corrections

> [!IMPORTANT]
> All code produced under this skill must adhere to the [[policy-index/SKILL#policy-registry|Bridge-Burning Policies]] in `policy-index/SKILL.md`. These are non-negotiable hard constraints that eliminate runtime defaults, fallbacks, mocks, optional critical dependencies, and other agent validation-evasion pathways.

## Correction Decision Gate

Classify the correction before choosing a response:

- **Explicit pivot:** the user names one unambiguous, reversible, in-scope action. Apply
  it immediately and continue the live task. Do not narrate this protocol or ask for
  permission already given.
- **Explanation or ambiguity:** the user asks why, disputes the reasoning, or leaves more
  than one materially different action possible. Investigate enough to answer or expose
  the real fork. Do not guess the desired implementation.
- **High-consequence pivot:** the likely response is destructive, irreversible,
  externally visible, touches unknown-provenance work, or needs new authority. Stop and
  obtain the missing decision after presenting only the evidence the user needs.

A correction is not inherently a stop signal. Stop only when action would require an
unsupported inference or cross a consequential boundary.

## Strongest-Live-Goal Gate

Before acting on a critique, correction, review, completion question, or remaining-work
question, identify the strongest live goal internally:

```text
The strongest live goal is <substantive user objective>. The action I am about to take
changes <artifact/state>. This does/does not satisfy the strongest goal because <reason>.
```

If the planned action only changes representation, status, labels, PR metadata, issue
linkage, comments, docs, report wording, or visibility of feedback, it does not satisfy
a goal whose object is code, proof, data, implementation, research, or semantic review.

Representational corrections can be necessary to stop a false claim. Explain the
distinction only when the user could otherwise mistake administration for substantive
completion:

```text
I corrected the false representation; the original work remains incomplete.
```

After the representational correction, either continue the substantive execution or
report the blocker that prevents it.
Do not stop as if the administrative artifact completed the task.

## Corrections Are Bounded Deltas

A correction changes the current route, not the whole operating regime.

Before proposing a new route, determine internally:

- the original substantive objective that remains live;
- the valid constraints that still protect it;
- the specific defect the correction exposed;
- the smallest route change that repairs that defect.

Do not answer a request for rigor by suppressing semantic judgment, exploratory research,
or direct object-level work. Do not answer a request for judgment by discarding evidence,
state, provenance, reversibility, coordination, or auditability. Keep controls that
protect correctness and recoverability; remove only process that has become a surrogate
objective.

Treat concrete human feedback as high-value semantic evidence. First identify what it
changes about the required action, source search, interpretation, or proof burden; then
normalize or route it only if normalization helps execute the change. Human feedback is
not infallible: verify according to consequence before committing irreversible state.

## Do Not Write the Correction Into the Corrected Artifact

A correction is feedback about your future behavior. It is not content for the artifact
you are correcting.

When told "X is wrong in this document/code/plan," the failure mode is to *document that
X was wrong* — add a disclaimer, a "note", a status caveat, a "this is not authoritative"
sentence, or a correction-history entry — instead of removing X and producing the correct
artifact. This embeds the supervision history into the product. Over many corrections the
artifact becomes a record of the agent's mistakes rather than a useful object, and the
disclaimers are themselves new defects.

- "The README should not contain volatile status." Wrong fix: add a README sentence saying
  status lives elsewhere. Correct fix: remove the volatile status and say nothing.
- "This function's parameter is unused." Wrong fix: add a comment explaining it is legacy.
  Correct fix: remove the parameter.

If you notice that corrections are accreting on one artifact — each one answered by another
caveat, label, or note — stop patching. That accretion is itself the signal that the
artifact's frame is contaminated and that an in-context repair will keep reseeding the
problem. Route to the **Contaminated Artifacts Cannot Be Repaired In Place** protocol in
[[fixing-slop/SKILL|fixing-slop]]: a fresh agent
extracts the real requirements, a separate fresh agent rebuilds greenfield. You, holding
the correction history, are the wrong context to do that repair.

This is `T7 Correction-to-Content Transduction` and `L8 Correction Fossilization` in
[llm-failure-modes/references/agent-distortion-index.md](file:///home/dzack/ai/opencode/skills/llm-failure-modes/references/agent-distortion-index.md).

## Correction Routing

For an ambiguous or high-consequence correction, determine this record internally:

```text
Trigger: <quote or paraphrase the correction in one sentence>
Reasoning error: <what prior assumption, inference, or action is under challenge>
Damage: <what artifact, decision, state, or user trust may have been damaged; say
"unknown" if not yet inspected>
Evidence needed: <exact files, diffs, transcript, command output, or external source
needed before acting>
Next action: <answer-only, investigate-only, or wait-for-user; never "fix now">
Stop point: <where this turn stops>
```

Do not print the labeled record by default.
Surface only the unresolved evidence, consequential damage, blocker, or decision the user
must see. If an internal field is unknown, investigate before changing consequential
state. If all fields are known and the user already directed a safe action, act instead of
requesting redundant confirmation.

For bug-fix corrections, this is an additional hard stop:

- Reproduction evidence must be captured before any implementation change.
- A unit-test pass is not sufficient proof by itself. It can only confirm a behavior
  after the end-to-end repro is established.
- If reproduction is unknown, set `Next action` to `investigate-only` and include the
  exact command/input sequence and environment needed to reproduce.

For explanation-only turns, answer from evidence and do not infer authorization to fix.
If the same message explicitly requests a concrete safe fix, the explicit-pivot rule
applies after the explanation.

## Mandatory Independent Audit After Observable App-Error Contradiction

The corrected agent has no jurisdiction to rate its own app-error failure as local,
ordinary, reversible, serious, or worth auditing. Those are conclusions produced by the
judgment under review.

Make the routing decision from the transcript and runtime record. Define two observable
facts:

**External failure fact**

- The user supplies a concrete app gesture and an observed wrong result; or
- a captured execution of the real user-facing boundary contradicts the claimed or
  expected result.

**Prior frame commitment**

Before that failure fact or correction appeared, the record shows at least one of:

- the agent changed product code to fix that same gesture;
- the agent assigned the cause or ownership to a subsystem, exonerated another subsystem,
  or wrote an unqualified claim such as “fixed,” “working,” “complete,” “the root cause,”
  or “the whole bug”;
- the agent used component checks, mocks, local artifacts, database writes, or other
  proxies as evidence for the app-level behavior without a recorded execution of the
  exact real path; or
- an earlier correction or failed remedy already occurred for the same user gesture.

The routing rule is mechanical:

> If an external failure fact and a prior frame commitment both appear in the record,
> stop app edits and causal claims and dispatch a fresh, report-only audit.

An explicit admission that the exact real path was never exercised after the agent called
component checks “verification” also fires the rule directly. The corrected agent may not
waive a fired trigger by redescribing the work as investigation, the correction as the
first one under a narrower issue, the previous claim as provisional, or the next patch as
small and reversible.

This threshold keeps ordinary corrections in-stream without asking the corrected agent to
judge seriousness. A correction made before any product edit, causal assignment,
app-level validation claim, or earlier remedy does not contain both facts. Once the agent
has committed to a frame and external reality contradicts it, the cost threshold has been
met by the record itself.

When the rule fires, quarantine the current causal frame. Quarantine does not negate every
prior fact; it prevents the failed frame from selecting its own repair and certifying
itself.

Give a fresh subagent the original objective, concrete user gesture, observed result,
faithful reproducer, raw logs/tool output, relevant artifacts and diffs, and the correction
sequence. Do not provide the primary agent's retrospective explanation or proposed next
fix before the auditor forms an independent account. The auditor must inspect the real
boundary, reconstruct how evidence was selected or excluded, test competing explanations,
bound the affected claims, and decide whether the frame can be repaired or must be
discarded. Route the review through [[reviewing-subagent-work/SKILL|reviewing-subagent-work]]
and [[llm-failure-modes/SKILL|llm-failure-modes]].

The audit must satisfy this synthesis gate:

> The current work proves ___ about the original app error based on ___. The prior frame
> is valid or invalid because ___. The unresolved alternatives and required falsification
> are ___.

The primary agent may reject an audit finding only with new evidence from the real
boundary that falsifies it. It may not use its own explanation, confidence, or component
checks as counterevidence. If no independent auditor can inspect the boundary, report that
oversight is unavailable and do not claim the remediation is definitive.

## What NOT to produce

Do not write “You’re right”, “I understand now”, “That makes sense”, or any validation
of the user’s perspective.
These are the same failure class as receipt-checking — visible artifacts of engagement
that substitute for substantive work.
Acknowledgment tokens produce social repair without fixing the problem.

Do not write “Using `handling-corrections`”, “loading correction guidance”, or similar
compliance announcements. Correct routing is the compliance surface.

Do not pivot immediately to a fix while leaving debris from the mistake.
Check what was damaged first.

Do not reflexively revert or overcorrect (thrashing).
Do not use `git restore` or `git checkout` — these are destructive in noisy repos.

## Anti-Laundering Rules

Do not convert a substantive failure into a weaker administrative success.
If the user or a review says the requested work is incomplete, the valid responses are:

- complete the original work
- falsify the requirement with evidence
- report a real blocker

Do not present any of these as progress on the underlying objective unless a substantive
change was made:

- issue narrowing, title changes, labels, `Refs` instead of `Closes`
- reopened or closed issues
- resolved, hidden, dismissed, or made-less-visible review feedback
- audit notes, scope statements, TODOs, comments, remaining-work lists
- "now accurately labeled partial" corrections

When asked to enumerate remaining work, "remaining" means all work required by the
user's original completion standard minus only work proved complete by artifacts.
If the full remaining set is unknown, investigate until it is known or report the
missing evidence as a blocker.

Do not say feedback was handled, addressed, taken into account, resolved, or
incorporated unless you identify:

- the concrete claim
- the disposition
- the evidence
- the substantive change, or explicit non-change

If feedback is closed, resolved, hidden, or made less visible, leave a durable
human-auditable note explaining why.
If the platform cannot preserve the note where the user will see it, do not resolve the
item; report the blocker.

## Correction Memory Rule

### Recall before prescribing

When a correction appears related to a prior incident, search memory for the experience,
not only an accepted remediation:

```text
agent-memory search "<the incident, causal cue, consequence, boundary, or expectation>"
```

A prior policy is one fallible interpretation of prior experience. Recover the episode,
its consequences, uncertainty, and later analysis before assuming that repeating the old
rule fits the new situation. Do not interrupt an explicit safe pivot with memory search.

### Preserve durable corrections at the owning scope

A correction may have durable value even before a complete remedy is known. Preserve the
layers that actually exist:

- the experience: what happened, sequence, consequences, and salient causal cues;
- contemporaneous reflection: what seemed relevant or might have helped;
- later analysis: revised interpretations and alternatives;
- intervention: any proposed working rule, labeled provisional until supported.

Cross-repo behavioral experiences normally belong at global scope; repo-specific
experiences stay project-bound. Use `reference` or `context` for the episode and
interpretation, `decision` for a settled choice, and `advice` or `trap` for proposed
working guidance. Link them when the episode is needed to understand or revise the rule.

Do not require an “accepted remediation” before preserving a consequential experience.
Do not claim to know how to prevent an entire failure class from one incident. Durable
capture is successful when later agents can recognize and reinterpret the event even if
the proposed intervention fails.

### Preserve history; revise interpretations additively

Search first and prefer updating an existing record when it is genuinely the same episode
or proposition. Do not overwrite an episode to make the newest causal theory look
inevitable.

- Correct false factual claims in the record while preserving what was actually believed
  or observed at the time when that distinction matters.
- Add later interpretation with its evidence and date/context rather than silently
  replacing contemporaneous reflection.
- Revise or retire failed remediation advice without deleting the experience that led to
  it.
- Do not create a second near-identical memory merely because the preferred intervention
  changed.

Most corrections also expose app decisions, ownership boundaries, purposes, goals, or
expectations. Persist those stable facts in their owning memory and reconcile divergent
wiki or GitHub surfaces. That fact-oriented capture does not replace an experience record
when the correction sequence itself has durable causal value.

The continuity test is:

> If the current lesson proves wrong, does the durable record still contain enough of the
> incident and analysis to formulate a different lesson?

Do not let durable capture replace or delay the object-level correction.

## When the user asks “why”

Every “why” question is a research task, not a conversation opener.

- Look it up: read transcripts, search docs, find real evidence

- Use the internal correction-routing questions when evidence or intent is unresolved

- Do **not** answer with supplication, invented feelings, or promises about future
  behavior

- Do **not** infer a fix from your own answer. Act only when the user also requested a
  concrete safe action; otherwise answer and wait.

## The question-then-action trap

Answering a question and then immediately acting on your own answer is a violation.

| Situation | Bad | Good |
| --- | --- | --- |
| “Why does this function have param x?” | “You’re right, it’s not needed, removing it.” [deletes] | “x is used for Y. It may no longer be needed.” [waits] |
| “Why did you edit that file?” | Explain + immediately restore it | Explain root cause, assess damage, wait for direction |
| “Why are you normalizing this body?” | “You’re right, removing normalization.” [edits] | Routing record -> inspect why normalization exists -> answer -> wait |
| “That is bad metadata. Delete it.” | Delete an ambiguously identified item | Verify the target; delete only if the identified action is authorized and recoverable |

The user's response may change the intended action entirely.
Do not act when the question leaves the desired change unresolved. If the user supplied
the answer and the action together, do not create an artificial pause.

## Common rationalizations

| Rationalization | Reality |
| --- | --- |
| “The fix is obvious, no need to inspect consequence” | Obvious intent does not waive checks required by destructive, irreversible, or unknown-provenance state |
| “Reverting is the safe undo” | `git restore` and `git checkout` are destructive in noisy repos |
| “I should fix it right now while I understand it” | Act only on the user's explicit safe direction; understanding alone is not authorization. |
| “I'll rename it so the label is honest” | The correction was about the artifact's **existence**, not its labeling. Renaming fraudulent code so it honestly describes its own fraudulence is **honest-label laundering**: consuming the critique while leaving the defect intact. See `anti-slop/references/code-patterns.md` → **Honest-Label Laundering**. |
| “I'll add a note explaining the problem so the reader is warned” | Documenting that X is wrong is not fixing X. A disclaimer inside the artifact embeds the correction history into the product and adds a new defect. Remove X. See **Do Not Write the Correction Into the Corrected Artifact** above. |
