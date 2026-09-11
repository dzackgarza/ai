---
name: understanding-challenges
description: Use the moment a user message questions comprehension — "do you understand
  X", "you understand X, right", "I don't understand why you...", "you seem confused",
  "did you not understand the task", "am I misunderstanding" — or repeats an instruction
  already given. These are defect reports, not questions. Converts the challenge into a
  named proposition, a located contradiction, and a durable write-down. Also use before
  naming a new concept, before proposing architecture, and before reporting a metric.
metadata:
  author: dzack
  version: 0.1.0
---
# Understanding Challenges

> [!IMPORTANT]
> All code produced under this skill must adhere to the [[policy-index/SKILL#policy-registry|Bridge-Burning Policies]] in `policy-index/SKILL.md`. These are non-negotiable hard constraints that eliminate runtime defaults, fallbacks, mocks, optional critical dependencies, and other agent validation-evasion pathways.

> **Privacy note:** this is a public-facing skill file. Every instance below is a
> scrubbed summary of a failure class. No verbatim user message appears here, and none
> may be added. See `User Messages Are Private` in the global AGENTS.md.

## The Invariant

A question about what you understand is never a request for information. The asker
already knows the answer. The message is a defect report whose content is:

> You produced work whose premises deny something I treat as settled and obvious. The
> denial is visible in your output. I am naming the proposition so you can find it.

The interrogative form carries no doubt. It marks distance between what the user
considers common ground and what your output proves you were operating on. That distance
is the defect. The instance in front of you is one symptom of it; there are others in the
same session, produced by the same method, that nobody has named yet.

Answering the literal question is therefore always wrong. "Yes", "Understood",
"You're right", and "Good catch" all assert the common ground that your output just
disproved, and they leave the artifact in its broken state.

## Trigger

Load this skill when a user message contains any of these observable forms. Do not
judge whether the concern is serious, large, or fair; the surface form is the gate.

- A comprehension interrogative aimed at you: *do you understand*, *you understand …
  right*, *do you not understand*, *did you not understand*, *you get that, right*,
  *do you have zero theory of mind*.
- A first-person non-comprehension report about your output: *I don't understand why
  you…*, *I'm confused*, *I have no idea what this means*, *this is incomprehensible*.
- An attribution of confusion to you: *you seem confused*, *you seem to fundamentally
  misunderstand*, *am I misunderstanding*, *maybe I'm missing something*.
- A repeat: the user states an instruction, constraint, or fact already stated earlier
  in this session, in a prior session, in a plan, or in a repository document.
- A challenge to a name, a metric, or a report: *why did you call it X when I said Y*,
  *do you understand why measuring Z is absurd*, *you buried the lede*.

**Non-triggers.** *Read X to understand Y* and *we need to understand why Z happens* are
task assignments, not challenges. Do the task; this skill does not apply.

## The Interlock

Introspection is not admissible evidence here, because the faculty that produced the
defect is the faculty that would assess it. Produce three artifacts, in order, before
any further edit to the work under challenge.

**1. The proposition.** Write X as a declarative statement, in the user's vocabulary,
at the user's precision. Weakening it is the same failure again: if the user said
*submodule*, the proposition says submodule, not ideal, not substructure, not
"something like a subobject". If the user named a functor, the proposition is about a
functor, not about a method that behaves functorially.

**2. The contradiction.** Cite the exact `file:line`, decision, name, test, or sentence
in your own output that denies the proposition. If you cannot locate it, you have not
found the defect; you have found a restatement. Keep looking. A challenge that resolves
to "no change needed" is nearly always an unlocated contradiction.

**3. The durable write-down.** Write the proposition into the document that owns it —
the repository's `AGENTS.md`, the plan, the architecture doc, the traps file, the
commit body, or the [[agent-memory/SKILL|agent-memory]] vault — and cite the path in
your reply. This is the only act that discharges the challenge. Agreement in a reply
evaporates with the context window; the write-down is what the next agent reads.

Then verify (1) against a source you did not author this session: the transcripts, the
plan, the repository documents, the vault. Written documentation on this system is
mostly agent-written and can carry injected agent assumptions; user messages in
transcripts outrank it. `[[reading-transcripts/SKILL|reading-transcripts]]` and
`[[epistemic-integrity/SKILL|epistemic-integrity]]` own that retrieval.

## Banned Responses

None of these discharge a challenge, and each is itself a reportable defect:

- `Understood.` / `You're right.` / `Good catch.` / `Yes, I understand.`
- Any claim to have learned, internalized, or now understood something. A model does
  not carry a lesson across sessions; only a file does. The claim is a promise you have
  no mechanism to keep.
- Restating the user's point back in your own words as the whole response.
- Deleting or renaming the offending word while the design that produced it survives.
  A banned vocabulary list does not repair a mental model.
- Apology, self-criticism, or an account of how the error arose. Cause belongs in the
  commit body or the traps file.
- Filing the challenge as an issue, a TODO, or a plan row instead of fixing the work.

## Blast Radius

A fired challenge invalidates the method, not only the instance. Before continuing:

- List the other outputs of this session produced by the same method — the same naming
  habit, the same proxy metric, the same unread source, the same special-case argument.
- Re-derive each against the now-named proposition, or state plainly which ones you did
  not check.
- If the same proposition has been named more than once across sessions, the repair is
  a change to the routing that failed, not another instance fix. Route to
  `[[handling-corrections/SKILL|handling-corrections]]` for authority and scope, and
  write the routing change into AGENTS.md or the owning skill.

## What Was Actually Not Understood

Ten recurring classes, with the principle, a scrubbed instance, and the check that
catches each one before a user has to:
[references/lesson-catalog.md](references/lesson-catalog.md).

Read the catalog when a challenge fires, and read the three preemptive checks below
before the situations that most often produce one.

## Preemptive Checks

- **Before introducing any technical noun** that is not in the user's message, the
  plan, or a cited source: state what it denotes and why an existing object cannot
  denote it. A noun you invented is a claim you must defend. (Lesson 1, Lesson 2.)
- **Before proposing or correcting an architecture:** name the sources you read that
  define correctness for it. Authority to correct comes from having read the
  transcripts, the plan, and the repository documents — never from local inspection of
  the code alone. (Lesson 3.)
- **Before reporting any number:** state the mission, state what the number measures,
  and state whether they are the same thing. If they are not, the number is a proxy and
  must not be reported. (Lesson 4.)
