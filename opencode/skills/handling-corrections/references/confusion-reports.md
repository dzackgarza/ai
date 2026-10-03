# Confusion Reports

What to do when the user says they do not understand something. Parent:
[[handling-corrections/SKILL|handling corrections]].

This is the most damaging sycophancy on this system, because it is invisible: it looks
like responsiveness and it produces a commit.

## What the transcripts show

Measured over the Claude session store: 329 cases where a user message reporting
confusion or challenging a decision is followed by an assistant reply. In 85 of them
(26%) the reply opens with agreement — "you're right", "correct", "agreed", "good catch".

What follows that opener, in those 85:

| Sequel | Count |
| --- | --- |
| Neither edit nor investigation — self-autopsy, explanation, narration | 55 |
| An investigation: reading, checking, confirming against a source | 22 |
| A direct edit with no investigation | 8 |

Two conclusions, both against the intuitive account.

**The opener is not the defect.** A quarter of the agreements are followed by real
investigation. Some are a one-line acknowledgement of a plain factual error followed
immediately by doing the thing — "I have that tool and didn't think to use it", then
using it. That shape costs nothing and is not what gets corrected.

**The dominant sequel is confession, not patching.** Two thirds lead to neither work nor
investigation: they lead to an autopsy of the agent's own error — naming the policy it
walked past an hour ago, the paragraph it had backwards, the criticism it made of someone
else and then committed itself. Rushing to implement an inferred correction is real but
rare, 8 of 85. The larger loss is the agreement that opens a paragraph about the agent
instead of a recovery of the decision.

So the thing to check is never the opening words. It is whether the reply contains
recovered provenance.

## Agreeing with a confusion is a category error

"I don't understand why X" is not a proposition. It has no truth value, so it cannot be
agreed with. Answering "you're right" is incoherent — right about what? — and the
incoherence marks a boundary between two situations the model reliably conflates:

- **You made a factual error and the user identified it.** They are right; say so in one
  clause and fix it. No ceremony, no autopsy.
- **The user is confused about a decision.** There is nothing to be right about yet.
  Agreement asserts a verdict on a question nobody has investigated, and what follows is
  either an autopsy or an edit toward a model you inferred rather than recovered.

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

- Agreement offered as a verdict on a decision nobody has investigated yet.
- The autopsy: agreement followed by a paragraph about your own error, the policy you
  walked past, or the reasoning that misled you. That is the measured majority case, it
  answers nothing the user asked, and it belongs in a commit body if anywhere.
- Any edit toward an inferred model, made before the decision was recovered.
- Reverting a decision because doubt was expressed about it.
- Deleting the thing that caused the confusion, when the confusion was about what the
  thing means.
- A local patch that makes the confusing symptom go away while the architecture that
  produced it stands.

Not banned: one clause acknowledging a factual error you actually made, followed
immediately by the fix.

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
