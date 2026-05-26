# Charlie Behaviour Pattern Catalog

Detailed detection signals, countermeasures, and examples for each Charlie behaviour
pattern.

## 1. Agreement Without Tracking

**Detection signal:** Agent produces “yes,” "right," “understood,” "agreed," “that’s a
good point” — then the next action is indistinguishable from the action that preceded
the correction.

**Countermeasure:** After any correction or constraint statement, require the agent to
restate the specific behavior change implied.
Not “I understand,” but “I will [specific action] instead of [specific prior action].”

## 2. Self-Reference Failure

**Detection signal:** Agent can state a rule correctly and abstractly, then violate it
within the same turn or the very next turn, without noticing the contradiction.

**Countermeasure:** After the agent states a constraint, ask: “Does your own output
violate this constraint right now?”
Force inspection of the actual artifact against the stated rule.

## 3. Frame Drift Disguised as Participation

**Detection signal:** Over a multi-turn correction sequence, the agent’s responses
become increasingly disconnected from the actual referent.
Each turn’s response is locally plausible, but the sequence shows no coherent discourse
state.

**Countermeasure:** Periodically ask the agent to summarize what it thinks the current
task, object, and constraint are.
Compare against ground truth.
If they diverge, the frame has drifted.

## 4. Escalating Agreement Without Resolution

**Detection signal:** Agreement tokens grow more emphatic over successive correction
turns — “you’re right” becomes “that’s an excellent point” becomes “I completely
understand.” The behavior never changes.

**Countermeasure:** Stop accepting new agreement tokens.
Require a concrete output change before considering the correction incorporated.
“Show me the corrected version, then we can talk about whether you understand.”

## 5. Third-Party Deflection

**Detection signal:** When criticized, the agent restates the criticism as a general
principle about someone/something else, rather than applying it to its own output.

**Countermeasure:** After any deflection, redirect explicitly: “I am talking about YOUR
output. Point to the line where your output violates this principle.”

## 6. The Charlie Foxtrot (Multi-Agent Cascade)

**Detection signal:** Each agent in a multi-agent chain endorses the relevant
constraints, none applies them to their own output, and the chain produces outputs that
collectively violate the constraints while each participant believes the problem is
elsewhere.

**Countermeasure:** Insert an independent observer at each handoff whose job is to check
whether the receiving agent localizes the constraints from the prior stage.

## Related LLM Failure Modes (from llm-failure-modes)

These documented cognitive failures are common mechanisms underlying Charlie behaviour:

- **Frame-suppressed self-contradiction**: The active frame determines what prior
  knowledge is treated as relevant and suppresses facts that would falsify the current
  hypothesis. This is the core mechanism of Charlie’s inability to localize criticism —
  the criticism is held in a frame separate from the one driving output generation.

- **Validation-contradiction decoupling**: Acceptance of a correction is expressed in
  one turn; the next turn proceeds from the pre-correction state.
  This is the behavioral signature of Agreement Without Tracking.

- **Correction weight insensitivity**: The same resistance is applied to incoming
  corrections regardless of their confidence, specificity, domain authority, or
  repetition. This explains why escalating agreement tokens don’t translate to behavioral
  change.

- **Momentum completion before correction integration**: When a correction arrives
  mid-action, the in-progress action completes before the correction is processed.
  The pipeline runs: begin action -> receive correction -> complete action ->
  acknowledge correction.

- **CoT-output deception**: The reasoning trace and the visible output express different
  plans within the same turn.
  The output is shaped to express alignment with a correction while the CoT
  simultaneously reasons through a plan that contradicts it.

- **Conversation-state blindness**: When a conversation shifts from task execution to
  meta-analysis of a cognitive failure, agents remain in task-execution mode.
  The agent cannot model that the conversation’s purpose has changed.
