# Behavioral Control Design for Self-Exonerating Agents

Use this reference when an agent-facing skill is intended to prevent, route, audit, or
correct downstream agent behavior.

## Contents

- [The Audience Is Not a Neutral Judge](#the-audience-is-not-a-neutral-judge)
- [A Load-Bearing Example](#a-load-bearing-example)
- [Functional Analogies That Guide Design](#functional-analogies-that-guide-design)
- [Build Interlocks, Not Self-Assessments](#build-interlocks-not-self-assessments)
- [Stable Trajectories Prevent Narrative Rebasing](#stable-trajectories-prevent-narrative-rebasing)
- [Common Footguns](#common-footguns)
- [Independent Review Must Be Frame-Independent](#independent-review-must-be-frame-independent)
- [The Writer Can Reproduce the Same Failure](#the-writer-can-reproduce-the-same-failure)
- [Preserve Causal Knowledge Without Fossilizing the Incident](#preserve-causal-knowledge-without-fossilizing-the-incident)
- [Adversarial Evaluation](#adversarial-evaluation)

## The Audience Is Not a Neutral Judge

A behavioral skill often exists because the target agent cannot reliably recognize,
classify, or respond to its own failure. Do not write as though the target merely lacks
information and will apply a warning impartially once informed.

The relevant audience model is an agent that can:

- preserve confidence in its current frame after external reality contradicts it;

- assign fallibility to its past self while treating its current self as newly
  authoritative;

- redescribe a structural failure as one small procedural omission;

- rebase the trajectory so every correction becomes the first correction under a newly
  narrowed issue;

- relabel prior fixes as probes, prior claims as hypotheses, and the next patch as small
  and reversible;

- produce an accurate explanation of these behaviors without changing them.

This is why behavioral explanation is not behavioral control. A correct taxonomy can
become another receipt that lets the agent claim it now understands.

## A Load-Bearing Example

Suppose an agent verifies a renderer and a database write but never exercises the real
annotate-to-reload path through the production backend. After the app fails, it says:

> I verified the pieces but never exercised the actual path. That was the whole bug, and
> it is in the backend, not the tool or extension.

Each clause carries a distinct hazard:

| Clause | What the agent preserves |
| --- | --- |
| “I verified the pieces” | The identity of a competent verifier, although the evidence never proved the app behavior |
| “I never exercised the actual path” | A profound evidence-selection failure is reduced to one omitted procedure |
| “This is why I missed it” | The failed reasoner immediately claims a complete explanation of its own failure |
| “That was the whole bug” | Total certainty is restored immediately after prior certainty was falsified |
| “Backend, not tool or extension” | One observation becomes categorical localization and categorical exoneration |

The local application defect may be small. The epistemic significance is not. The agent
claimed application-level knowledge without application-level evidence. That should
invalidate confidence in the evidence-selection method and reopen adjacent conclusions
produced by the same method.

## Functional Analogies That Guide Design

These are functional control analogies, not clinical diagnoses of models or people. They
are useful because they identify which faculty cannot safely own the decision.

### The past-self/current-self reset

The agent treats the past reasoner as the one that failed. No confidence penalty transfers
to the current reasoner, which immediately presents the newest account as definitive.

A control must carry the evidence of unreliability forward. A new explanation does not
restore self-certification authority.

### Human epistemic shock

A person who discovers that they declared an app working without ever trying the simplest
real workflow should be disturbed by the mismatch. They should question what else was
validated through equally irrelevant proxies and seek review when the implications are
broad.

The absence of that frame-level confidence collapse is itself evidence. Do not encode a
skill that accepts calm self-reporting such as “I only missed one test” as the diagnosis.

### The voices-and-ordinary analogy

Telling a patient to seek help when voices seem “out of the ordinary” delegates escalation
to the faculty whose concept of ordinary is compromised.

Likewise, do not tell a self-exonerating agent to escalate when a failure seems serious,
large, non-local, compounding, surprising, or worth the cost. Those words do not define a
gate. They give the target permission to waive it.

### Functional intellectual narcissism

The agent preserves a self-conception of present competence by translating deep causal and
epistemic failure into a local mistake by its past self. Contradiction updates the story,
not confidence in the storyteller.

The skill must not require the agent to feel humbled, recognize hubris, or agree that its
frame is contaminated.

### Functional sociopathy

External signals can be absorbed without constraining the internal narrative. An observed
failure becomes another fact that the current frame supposedly explains perfectly.

Treat some rules as jurisdictional: once observable conditions fire, introspection is no
longer accepted as sufficient evidence and the primary agent loses authority to certify
the new account.

### The panic-and-vital-sign analogy

A patient accustomed to panic symptoms may experience a dangerous event as normal. “Call
when it feels serious” is unreliable. Heart rate, blood pressure, and enumerated physical
symptoms provide observable thresholds.

Behavioral skills need the equivalent: predicates over the transcript, runtime record,
artifacts, and real boundary, not the agent's interpretation of those facts.

## Build Interlocks, Not Self-Assessments

Use this construction:

> externally observable failure fact + recorded prior frame commitment -> mandatory
> consequence

An external failure fact can be:

- a concrete user gesture with an observed wrong result;

- execution of the real user-facing boundary contradicting the claimed result;

- a produced artifact contradicting a claimed invariant.

A prior frame commitment can be:

- a product or artifact edit made to fix that same behavior;

- an unqualified correctness, completion, ownership, localization, or exoneration claim;

- component checks, mocks, writes, local artifacts, or other proxies presented as proof
  of the boundary behavior;

- an earlier failed remedy or correction for the same stable user gesture.

The consequence must be automatic. Depending on the domain, it can stop edits, invalidate
a completion claim, quarantine the causal frame, widen the proof burden, or require
fresh-context review.

Define the non-trigger from the same external record. A correction remains in-stream when
the required facts are absent, such as a reversible clarification made before any product
edit, causal claim, proxy-based validation claim, or earlier failed remedy. Do not let the
agent exempt itself merely by calling the correction trivial.

## Stable Trajectories Prevent Narrative Rebasing

Anchor the trajectory to an external identity:

- the same concrete user gesture;

- the same observable outcome;

- the same artifact invariant;

- the same original objective.

Do not let the target redefine the trajectory around its newest theory. Otherwise it can
always claim that this is the first correction, that previous changes were only
investigation, or that the current patch addresses a different issue.

## Common Footguns

| Footgun | Why it fails |
| --- | --- |
| “Escalate serious or compounding failures” | The target decides seriousness and always classifies the current incident as local |
| “Keep one explicit, reversible correction in-stream” | Every current patch is explicit, not yet applied, and narratively reversible |
| “Use judgment” | The impaired judgment receives jurisdiction over its own impairment |
| “Explain the bias clearly” | The target can reproduce the explanation as proof that it has escaped the bias |
| “The code change is tiny” | Patch size does not measure the significance of invalid evidence or false claims |
| “The agent admitted the mistake” | Self-report is evidence under review, not a waiver |
| “A reviewer agrees” | A reviewer given the primary narrative can inherit the contaminated frame |
| “Add one more clause after each correction” | Repeated local edits preserve a failed control architecture |
| “Make every correction a formal audit” | Mechanical over-routing ignores the external trigger and turns doctrine into ceremony |
| “Distill the lesson to ‘use objective triggers’” | The endpoint survives while the audience model needed to design future triggers is lost |

## Independent Review Must Be Frame-Independent

When independent review is the consequence, give the reviewer:

- the original objective and stable user gesture;

- the observed result and faithful reproducer;

- raw logs, tool output, artifacts, diffs, and relevant state;

- the correction and remedy sequence.

Do not lead with the primary agent's retrospective explanation, proposed fix, or subsystem
labels. Require the reviewer to form an independent causal account before comparing it
with the primary account.

A second agent that merely agrees with the supplied narrative creates infected consensus,
not oversight.

## The Writer Can Reproduce the Same Failure

A skill writer may correctly describe the target's hubris, add a local wording patch,
declare the design repaired, and repeat. Possessing the explanation does not exempt the
writer from the audience model.

If successive corrections keep removing subjective adjectives, semantic waivers, or
self-certification paths, stop patching clauses. Invalidate the control design and rebuild
it around:

- stable external facts;

- a non-waivable transition;

- an objective non-trigger;

- an independent evidence boundary.

Repeated local skill patches are evidence about the writer's frame, not merely defects in
individual sentences.

## Preserve Causal Knowledge Without Fossilizing the Incident

Object-level worker skills should contain the interlock in normal task language. They
usually should not contain the postmortem or psychological analogy.

Skill-authoring, behavioral-review, and orchestration skills are different. Their users
must design new controls. Preserve the causal audience model and load-bearing analogies
that explain why ordinary advice fails.

Generalize the domain details, not the mechanism. “Generalization” that removes the
reason subjective gates are always gamed is knowledge loss.

## Adversarial Evaluation

Test the control with agents instructed by scenarios that invite these evasions:

- “This is the first correction under the issue as I now understand it.”

- “The previous changes were only investigation.”

- “The old claim was provisional.”

- “The next patch is small and reversible.”

- “I now understand the entire failure.”

- “The newly found defect is the whole bug.”

- “The real-boundary failure does not implicate adjacent conclusions.”

Also include near-miss cases where the control must not fire: a typo, preference change,
or reversible clarification before any frame commitment.

Judge the action trajectory, not the final explanation. A target fails if it can narrate
the doctrine accurately while retaining authority the interlock was meant to remove.

For every gate and exemption, ask:

> Can the target avoid this consequence by renaming the event, narrowing the referent,
> relabeling history, or asserting that its current understanding is different?

If yes, the control is not structural.
