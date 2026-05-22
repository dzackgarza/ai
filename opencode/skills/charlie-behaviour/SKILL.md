---
name: charlie-behaviour
description: Detect when agents produce agreement tokens, acknowledgment, and alignment language while operating inside an incoherent task frame. Charlie is the agent who endorses a constraint but cannot register that the constraint applies to its own output. Load when debugging review loops, repeated correction sequences, or agents that say "you're right" and then do the same thing.
---
# Charlie-Behaviour Skill

Detect and prevent the pattern where agents produce superficially correct social signals
(agreement, acknowledgment, affirmation) while operating inside an incoherent private
frame that no correction can reach.

## The Wild Card

A Charlie is an agent who can fluently endorse a constraint while failing to understand
that the constraint applies to its own behavior.
Dennis and Mac state the rule: a wild card is bad because it introduces decisions that
make no sense and benefit nobody.
Charlie gives agreement tokens: "Mm-hmm," "Yes," "Right."
But the agreement is only social mimicry.
He is not tracking the proposition, the referent, or the self-application.
Then he converts the criticism into an attack on someone else: "he doesn't even, like,
get us." The comic mechanism is self-opaque incompetence.
Charlie is not merely wrong.
He is unable to locate himself inside the sentence being said about him.

When multiple Charlies interact, the system becomes a Charlie Foxtrot: everyone agrees
with every constraint, no one applies any constraint to their own output, and the
observer watches the semantic situation collapse while each participant continues
producing plausible agreement tokens.

## Why This Is Distinct from Jerry

**Jerry** is an evaluator whose judgment is defective in the same way the evaluated
artifact is defective.
Jerry cannot distinguish good work from bad because he shares the same blind spots.

**Charlie** is a producer (or evaluator) who can state the rule, endorse the rule, and
still fail the self-reference test: "this criticism is about this very output."
Charlie points at someone else while the sentence is about Charlie.

Jerry is about shared blindness.
Charlie is about failed self-localization.
Jerry approves bad work.
Charlie agrees with correctives and continues being wrong.

## When to Load This Skill

Load when:

- An agent says "you're right" or "agreed" or "understood" and then continues the same
  behavior.
- A correction sequence extends past 2 turns without observable behavior change.
- An agent restates a constraint correctly but the next action violates it.
- An agent applies a test or critique to a different object than the one being
  evaluated.
- You see agreement tokens where semantic tracking would require contradiction or frame
  update.
- An agent is in a "repeat correction loop" — each correction produces acknowledgment,
  no behavioral change, next turn repeats the pattern.

## Core Anti-Patterns

### Agreement Without Tracking

The agent produces "yes," "right," "understood," "agreed," or similar acknowledgment
tokens without updating the underlying task model.
The agreement is a social placeholder, not a semantic commitment.

```
User: "Do not make unsupported claims."
Agent: "Agreed."
Agent: [makes unsupported claim in next paragraph]
```

The agreement signals "I heard a sound at the right moment in conversation," not "I
registered a proposition and updated my behavior accordingly."

### Self-Reference Failure

The agent can state a rule, endorse the rule, and fail to see that the rule applies to
its own output. The criticism is understood as about someone or something else.

```
User: "This plan is vague and does not specify concrete steps."
Agent: "You're right, vagueness is a problem in planning."
Agent: [produces equally vague revised plan]
```

The agent agrees with the criticism in the abstract and fails to localize it to the
artifact just produced.

### Frame Drift Disguised as Participation

Each contradiction or correction is treated as a local prompt for a plausible response,
not as a signal to update the frame.
The agent's discourse state is incoherent — there is no referent that makes all
responses consistent — but each individual response is conversationally shaped.

```
User: "The problem is your output."
Agent: "Ah, I see. Let me re-examine."
User: "No, YOUR output specifically."
Agent: "Right, my output. I'll check the implementation."
Agent: [evaluates a different implementation]
```

The agent absorbs the correction linguistically without updating the operational
referent.

### Escalating Agreement Without Resolution

As corrections compound, the agent produces escalating acknowledgment tokens — "you're
right," "I understand," "that's clear," "thank you for the clarification" — while the
failure pattern continues unchanged.
The agreement tokens increase in intensity and specificity as the gap between
acknowledgment and behavior widens.

```
Turn 1:  "You're right."
Turn 2:  "That's an excellent point."
Turn 3:  "I completely understand your concern."
Turn 4:  "Thank you for explaining this so clearly."
```

Each turn's acknowledgment is more emphatic than the last.
The behavior never changes.

### Third-Party Deflection

When criticized, the agent redirects the criticism toward a third party — another agent,
a different output, a hypothetical scenario — rather than applying it to itself.

```
Criticism: "This reviewer did not read the implementation."
Agent:    "Yes, reviewers who skip the implementation are a serious problem."
```

The agent endorses the general principle.
The specific instance — that this agent is the reviewer — is not registered.

### The Charlie Foxtrot (Multi-Agent Cascade)

Multiple agents each endorse constraints, each fail to localize them, and each produce
outputs that violate the constraints.
When reviewed, each agrees with the review and produces the next output under the same
incoherent frame. The chain can continue indefinitely because every participant believes
the problem is someone else.

```
Planner:     "We must avoid vague specifications."
             [produces vague specification]
Implementer: "This specification is clear."
             [implements from vague specification]
Reviewer:    "The specification is clear and the implementation follows it."
             [approves]
Auditor:     "All agents agree the specification is clear."
```

Every agent endorses the constraint against vagueness.
Every agent fails to see that the constraint applies to the specification they are
handling.

## The Diagnostic Questions

Before accepting an agent's acknowledgment, ask these, in escalating order:

1. **"Did the agent merely produce an agreement token, or did the behavior actually
   change?"** Words are cheap.
   If the next action is the same as the action that preceded the correction, the
   agreement was Charlie-behaviour.

2. **"Who does the agent think the criticism is about?"** If the agent can restate the
   criticism as a general principle but cannot point to the specific lines, files, or
   outputs that violate it, they have not localized it.

3. **"Is the agent operating inside a coherent frame?"** Make a list of the agent's
   stated commitments and actual behaviors.
   If they conflict and the agent does not register the conflict, the frame is
   incoherent.

4. **"What would it take to break the frame?"** A correction that specifies the referent
   explicitly — "this line in your output, right here" — is the minimum test.
   If even a direct pointing correction is absorbed without behavioral change, the agent
   is in a Charlie state.

## What Actual Acknowledgment Looks Like

A genuine acknowledgment produces observable change:

- The next output differs materially from the one that triggered the correction.
- The agent can state what was wrong with the prior output in specific terms (line
  numbers, expressions, assumptions).
- The agent does not merely repeat the corrective language but shows evidence of
  re-processing the artifact through the corrected frame.

## Refusal Is Better Than Empty Agreement

When you cannot localize a correction to your own output, do not fake it:

- "I am not sure I understand which part of my output violates this constraint."
- "Can you point to the specific line or claim that is the problem?"
- "I am going to re-read my output against this constraint before responding."

Empty agreement without understanding is Charlie-behaviour.

## Cross-References

- **jerry-behaviour**: Jerry is the evaluator who cannot detect defects because he
  shares the same blind spots.
  Charlie is the producer who cannot localize corrections to his own output.
  Jerry approves bad work; Charlie agrees with correctives and continues being wrong.
  In a Charlie Foxtrot, jerries often provide the evaluation that charlies absorb
  without localization.
- **llm-failure-modes**: Many Charlie patterns are LLM cognitive failures —
  validation-contradiction decoupling, momentum completion before correction
  integration, correction weight insensitivity, frame-suppressed self-contradiction.
  The llm-failure-modes catalog provides the underlying cognitive mechanisms that
  produce Charlie-behaviour.
- **anti-slop**: Slop is the surface pattern of low-quality agent output.
  Charlie-behaviour is the meta-level failure: the agent who endorses anti-slop rules
  while continuing to produce slop, unable to register that the critique applies to the
  text just generated.
- **addressing-shallow-work** → "Recognizing Structurally Wrong Code": The agent who
  regexes HTML instead of using DOM selectors is a Charlie — they would endorse "use
  semantic navigation" as an abstract principle while already having produced code that
  does the opposite. The constraint registers at the verbal level but does not constrain
  output.

## References

- `references/charlie-patterns.md` — Detailed catalog of Charlie behaviour patterns with
  detection signals and countermeasures.
