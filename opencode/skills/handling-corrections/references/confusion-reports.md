# Confusion Reports

What to do when the user says they do not understand something. Parent:
[[handling-corrections/SKILL|handling corrections]].

This is the most damaging sycophancy on this system, because it is invisible: it looks
like responsiveness and it produces a commit.

## Agreeing with a confusion is a category error

"I don't understand why X" is not a proposition. It has no truth value, so it cannot be
agreed with. Answering "you're right" is literally incoherent — right about what? — and
the incoherence is diagnostic: the sentence was produced by a reflex that skipped the
analysis, and it will be followed by a patch built on an inferred model rather than a
recovered one.

The reflex has a second move. From the confusion, the model infers what the user must
believe, treats that inference as the requirement, and edits toward it. Nothing in that
sequence involved understanding the decision under discussion.

## What a confusion report actually is

It is **evidence of a mismatch** between an artifact and the user's model of it. It
localizes the mismatch precisely. It says nothing at all about which side of it is wrong.

Four cases, and you cannot tell them apart without looking:

1. **Agent drift.** The artifact departed from the requirements, and the confusion is the
   requirement reasserting itself. Fix the artifact.
2. **Sound decision, undocumented.** The artifact is right and the reasoning was never
   written down. Explain it, then write the reasoning into the document that owns it so
   the next reader does not repeat the question.
3. **Sound decision, genuine conflict.** The artifact follows a recorded decision that
   the user's current model contradicts. This is a real decision for them, and the only
   case where stopping is correct. Present the recorded reasoning and the conflict, not a
   patch.
4. **Genuinely incoherent.** The artifact cannot be defended from any recorded decision.
   Repair it — and note that the confusion was flagging a misunderstood architecture, so
   deleting the confusing surface is not the repair.

## Recover the decision before touching anything

- **Find the decision and its provenance.** What was decided, when, against which
  requirement, with what reasoning. Search the transcripts, the plans and specs, the
  commit bodies, the issues.
- **Use the authority order.** The user's own statements in transcripts outrank
  everything; then plans and specs; then repository documents; then code. Written
  documentation here is mostly agent-written and can carry agent assumptions injected as
  the user's, so it is evidence, not proof.
- **A thrashed file is not an authority.** Code that agents have written and rewritten
  repeatedly records no decision at all; it records the thrashing. Never cite it as the
  reason something is the way it is.
- **Separate the two authorities.** On requirements, intent, and what the system is for,
  the user is the authority and your reading is subordinate. On internal mechanism —
  which construction, which layering, which name — the recorded reasoning holds until
  someone shows it wrong. A user's confusion about an internal detail is not a ruling
  about it, and they will say so if you ask a real question instead of agreeing.

Only then act, and say which of the four cases you found.

## Banned responses

- "You're right", to a statement that cannot be right.
- Any edit toward an inferred model, made before the decision was recovered.
- Reverting a decision because doubt was expressed about it.
- Deleting the thing that caused the confusion, when the confusion was about what the
  thing means.
- A local patch that makes the specific confusing symptom go away while the architecture
  that produced it stands.

## The gradient test

House vocabulary, used throughout the transcripts, for whether an action is work:

- **Forward gradient:** the artifact moves toward the intended architecture.
- **Sideways gradient:** motion that changes the artifact without moving it toward the
  intended architecture — rewriting the same file in a new direction each round, chasing
  errors mid-refactor, golfing intermediate code that a finished refactor will delete.
- **Negative gradient:** the artifact moves away — duck-typing checks sprayed through the
  code, definitions dumped in without provenance, decisions reverted on no evidence.

Sycophantic patching is the most reliable generator of sideways gradient available: each
round is responsive, each round produces a diff, and after five of them the file has been
rewritten repeatedly and the architecture has not moved. Before acting on a confusion
report, state which gradient the action is on. If the answer is sideways, the work is to
recover the decision, not to edit.
