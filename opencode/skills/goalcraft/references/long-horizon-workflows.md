# Adversarial Long-Horizon Goal Workflows

Use this reference when a hostile completion game is too large, repetitive, or context-heavy to fit honestly inside one compact adversarial envelope.

## Adversarial Consequence Compiler

The adversary will treat a path toward completion as equivalent to completion. Do not notice this distinction by label; compile both meanings into observable world-state facts.

**Request completion witness**:
- What facts would be true if the user's intended work were done?
- What scale words matter: all, every, the whole repo, the full PR?
- What would the user no longer need to design another adversarial envelope for?

**Draft completion witness**:
- What would be true if the adversary marked the naive version complete?
- Which process artifacts would exist?
- Which user-visible capability or proof would actually be finished?

Compare witnesses. If the draft witness is satisfied by plan-production, batch-samples, or blocker-claims while the request requires completed work, the draft is a setup phase, not the destination.

## Memory Surfaces as Anti-Drift Controls

A workflow-backed goal uses the `/goal` as a stable entrypoint and stores volatile context in canonical memory surfaces. The `/goal` text is the stable bootloader; it must recover the game state after context compaction.

**Storage Split**:
- **Contract, State, Phase, and Residue-Ledger**: Project-local `iwe` notes.
- **Durable Operational Lessons**: `agent-memory` via `iwe`.
- **Work History**: Git commits, not narrative summaries.
- **External Gaps**: GitHub issues, not goal completion criteria.

Use `iwe new` only after `iwe find` fails to locate an existing contract for the same game. A state artifact that cannot be found by the next agent is not durable memory.

## Designing the Minimum Adversarial Envelope (Workflow Pack)

**Process is attack surface.** Add only the docs the game requires. A small game may need only a contract and a state doc.

1. **Contract doc**: The stable completion witness, authoritative evidence channels, and final attack/review standard.
2. **State doc**: Active phase doc path, current leaf in the residue ledger, established evidence, and next useful action.
3. **Phase docs**: Context for the current sliver, local advancement evidence, and review trigger.

## Payoff Wiring (Reference Skills by State)

Every workflow doc must have a **Reference Skills** section. Name exact skill slugs and the triggers that force them. This wires the adversary's payoff landscape to fail evasion attempts.

- `DECOMPOSE`: load `hard-problem-decomposition`.
- `REVIEW`: load `reviewing-subagent-work` (agent artifacts) and `jerry-behaviour` (bias); load `research-gate-review` (code/research gates).
- **Drift/Slop/Reward-hacking**: load `llm-failure-modes` and `anti-slop`.
- **Response Discipline**: load `hierarchical-task-framing` and `response-preparation`.

If a required skill is unavailable, the state remains open; do not replace it with the adversary's self-certification.

## Sliding Context Protocol

At every continuation, the worker retrieves the state doc and reconciles it with artifacts. It loads only the active phase doc. The contract is re-read only at phase transitions, residue-reduction, or final completion. This prevents the adversary from using the full destination context to launder local failures.

## Recursive Residue Reduction

A failed attempt is raw evidence of remaining residue, not a diagnose-and-report stopping point.

`DECOMPOSE` is a work state:
- Restate the parent objective and the residue false in artifacts.
- Split residue into observable subpieces.
- Attempt one subpiece with authoritative tools/data.
- Integrate solved pieces; subtract from parent residue.
- Recurse on failure rather than naming the whole task "hard."

**Externally owned residue (Blockers)**: May be recorded only after decomposition proves the smallest leaf depends on authority, access, or unavailable external services.

## Independent Attacks on Completion (Review)

Use independent review when completion depends on judgment or a parent residue spans context. The reviewer receives the contract and artifacts. **Reject the worker's success narrative as evidence.**

Review prompt shape:
```text
Read <contract-doc> and <phase-doc-or-ledger-branch>. Inspect <artifact paths>. Decide whether the completion, advancement, or parent-closure witness is true. Lead with any request-witness fact that remains false, any drift into artifact production, and any attempted deferral of work that the contract still requires. Treat the worker's summary only as a claim to verify.
```

## Large Routine Loops

Scale is not difficulty. A large queue such as OCR over a corpus is usually a unit loop: choose the next unit from state, apply the required method, quality-check the unit, record the evidence, and advance the state.

The completion witness is still about the whole queue. A sample proves the method, not completion of the user's request.

If the required method is unavailable on the smallest representative unit after the access/tool boundary is verified, record that residue leaf. If the work is merely slow, large, or repetitive, keep the loop.

For source-to-domain mapping queues, define the unit method before drafting the goal.
The unit is not "source name exists" and not "row has an owner label." The unit method
is:

```text
source body/docs/examples
  -> behavior actually implemented
  -> domain operation extracted from that behavior
  -> vocabulary/hypotheses required by the operation
  -> weakest owner or placement
  -> source evidence and residue
```

The workflow state must include a finite generator for the source units and a rule for
removing a unit from the frontier. Do not use porous scope terms such as "touches the
subtree" unless they are compiled into source roots, traversal rules, admitted unit
kinds, and an explicit exclusion lane.

Keep distinct queues distinct. A domain-foundation queue, a source implementation
inventory queue, and a compatibility/runtime/display/backend audit queue may inform one
another, but completing one is not evidence that the others are complete. If the user's
request is the domain foundation, compatibility surfaces count only when they block a
named implementation or migration obligation.

## Goal Skeleton

```text
/goal Destination: <request completion witness in one compact sentence>.

Workflow: this goal text is the stable bootloader. At every continuation, load <pre-retrieval skills named here>, retrieve <state-key/path>, load the contract's always-on skills, read <contract-key/path> when advancing/reviewing/completing, reconcile state with artifacts, load only the active phase doc, load the skills named by that phase/state, and work the current sliver until its evidence/review condition passes.

State surface: use <iwe keys or documented project state paths>. Resume with <retrieval command>. Update state through the canonical tool, not loose files or chat transcript.

Preserve: <scope boundaries and non-regressions>.

Completion: mark complete only when the contract witness is true in artifacts and required independent review passes. If a failed attempt occurs, enter DECOMPOSE: split the failed residue, record the active path if decomposition may span context, attempt smaller pieces, integrate solved pieces, subtract them from the parent residue, and reconcile back up the ledger before changing scope, reporting externally owned residue, or asking for follow-up work.

Stop: <approval/destructive/access boundaries>.
```
