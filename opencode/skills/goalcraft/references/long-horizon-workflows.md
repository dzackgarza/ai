# Long-Horizon Goal Workflows

Use this reference when a Codex goal is too large, repetitive, review-sensitive, or context-heavy to fit honestly inside one compact `/goal` objective.

## Consequence Compiler

Agents often treat a path toward completion as equivalent to completion. Do not ask the writer to notice that distinction directly. Make the writer compile both meanings into observable consequences.

Request completion witness:

- What would be true in the repo, artifact set, external system, research state, or user-visible workflow if the original request were complete?
- What scale words matter: all, every, the whole repo, the entire corpus, the full PR, all review comments?
- What would the user no longer need to ask another agent to do?

Draft completion witness:

- What would be true if the candidate goal were marked complete exactly as written?
- Which artifacts would exist?
- Which user-visible capability, proof, result, batch, or repair would actually be finished?
- What work would still need another goal?

Compare witnesses by consequences, not by semantic labels. If the draft witness only creates a plan, sample, scaffold, first batch, status report, or future workflow while the request witness requires completed work, classify the draft as a setup phase. The goal remains the request witness.

## Writer-Side Preparation

This section is for the agent using `goalcraft`, not for the future worker. The future worker sees the `/goal` bootloader and retrieved docs; it does not inherit the writer's currently loaded skills.

Before designing the workflow pack, load the writer-side skills needed to decide its architecture:

- `writing-for-agent-audiences` and `prompt-engineering`: how to write compact agent-facing bootloader text, contracts, and phase instructions.
- `agent-memory`: how to choose searchable, canonical state and memory surfaces instead of loose docs.
- `llm-failure-modes`: how to design drift, reward-hacking, premature-completion, and goal-substitution gates.
- `creating-skills`: whether a recurring procedure belongs in `goalcraft`, a subskill, a standalone skill, or a workflow reference.
- `hard-problem-decomposition`: how failure states preserve the parent objective, recurse on residue, and avoid one-shot blocker claims.
- `subagent-delegation`: how orchestration phases should assign, track, and reconcile subagent lanes.
- `reviewing-subagent-work` and `jerry-behaviour`: how independent review avoids worker self-report, reviewer bias, and consensus-as-evidence.
- `anti-slop`: how to recognize generic success-shaped artifacts and prose.
- `hierarchical-task-framing` and `response-preparation`: how progress and completion reports preserve the parent task instead of presenting a sliver as the whole.

Use the smallest set that answers the design questions actually present, but every workflow-backed goal needs writer-side context for agent-facing wording, canonical state, and drift control before drafting. After that preparation, write worker-side skill routing into the workflow pack. A skill loaded by the writer but omitted from the bootloader/docs is lost to future workers; a skill listed in docs but not loaded by the writer cannot inform the design.

## Workflow Pack

A workflow-backed goal uses the `/goal` as the stable entrypoint and stores volatile context in canonical Markdown state docs or notes. The `/goal` text is the only instruction guaranteed to stay in context for the whole run, so it must be a bootloader to the workflow pack.

The bootloader goal must include enough to recover after compaction:

- destination: the request completion witness;
- canonical state surface and retrieval command or key;
- contract doc key/path and active state key/path;
- rule to load only the active phase doc after state reconciliation;
- explicit names of any skills that must be loaded before state retrieval or state decisions;
- rule to load any remaining always-on skills before work resumes;
- rule to load skills required by the active state or phase;
- rule to reload the contract before phase advancement, parent closure, outside-agent residue reporting, or final completion;
- completion and independent-review gate.

The workflow pack must exist before the bootloader goal is returned. If the contract, state, and needed phase docs are not created or returned as required companion text, the `/goal` would point to missing context and is not safe to activate.

## Canonical State Surfaces

Before drafting a workflow-backed goal, inspect the active project's docs for its canonical planning and memory surfaces. On this system, prefer project-local `iwe` for agent-facing workflow docs when available.

Use this storage split:

- Contract, state, phase, queue, and residue-ledger docs: project-local `iwe` notes, or the documented project planning surface if the repo already defines one.
- Reusable operational lessons, environment quirks, and cross-session execution context: `agent-memory` via `iwe`.
- Completed work history: git commits, not memory notes or state docs.
- Current gaps or external work requiring human/project tracking: GitHub issues or the project's documented backlog, not goal completion criteria.
- Search/discovery over notes and expository docs: `iwe find`, `iwe retrieve`, `iwe tree`, and semtools search when semantic search is needed.

State commands for `iwe` workflows should be concrete enough for the worker to resume:

```bash
iwe find "<goal slug or completion witness>"
iwe retrieve -k <state-key>
iwe update -k <state-key> -c "<updated state>"
npx -y -p @llamaindex/semtools search "<semantic query>" <doc-paths>
```

Use `iwe new "<title>"` only after `iwe find` shows no existing contract/state note for the same goal. Do not rely on raw file reads of `.agents/memories`; use `iwe retrieve` so links and graph context remain available.

Do not create loose `notes.md`, `progress.md`, `scratch.md`, or unindexed state files when a canonical surface exists. A state artifact that cannot be found by the next agent is not durable state.

The contract doc is stable. It contains the request completion witness, scope boundaries, accepted evidence, future user rejection tests, and final review standard.

The state doc is active state. It contains the current state, active phase doc path, current focus, established evidence, current residue, known inconsistencies, and next useful action. If decomposition can branch or span compaction, it also owns the residue ledger. It is a fallible memory aid; artifacts outrank the state doc.

Phase docs are loaded only when active. A phase doc contains the context needed now, required skills, local advancement evidence, review trigger, and next state after success or failure.

Create only the docs the task needs. A small two-phase goal may need only a contract doc, a state doc, and one active phase doc. Do not build a bureaucracy around simple work.

## Reference Skills By State

Every workflow doc that can be active after compaction must have a `Reference Skills` section. Name concrete existing skill slugs and the trigger for loading each one. Do not paste skill content into the workflow docs, and do not use vague labels such as "review skill", "debug skill", or "slop check" without the exact skill slug.

The bootloader goal owns pre-retrieval skills: any skill needed before reading state or deciding what to load next must be named directly in `/goal` text. The contract doc owns the rest of the always-load skill set: skills the worker must load at every continuation before doing object-level work. Keep this set small and justified by the task's failure modes. Examples: a long-running review-sensitive goal may require `hierarchical-task-framing` before progress/completion reports and `llm-failure-modes` before accepting a shortcut, while a routine queue may require only the domain extraction skill and the state-update rule.

- `DECOMPOSE`: load `hard-problem-decomposition`.
- `REVIEW`: load `reviewing-subagent-work` for agent artifacts and `jerry-behaviour` when the reviewer could reward agent-shaped output; load `research-gate-review` when the review is a substantive research/code gate.
- Orchestration phases: load `subagent-delegation` before assigning or reconciling lanes.
- Drift, reward-hacking, goal-substitution, or premature-completion suspicion: load `llm-failure-modes` before accepting artifacts or summaries.
- Generic prose/code/design quality or success-shaped filler suspicion: load `anti-slop` before accepting artifacts or summaries.
- Response/progress states: load `hierarchical-task-framing` before reporting progress, and `response-preparation` before final or status responses when the workflow requires user-visible reports.

If the required skill is unavailable, keep the state open and record the missing review/decomposition capability in state. Do not replace it with the worker's own judgment.

State docs must include the active skill context, not just the active phase. At minimum:

```markdown
Reference Skills:
- Always load now: <skill slugs>
- Load for active phase: <skill slugs and triggers>
- Load before advancement/review: <skill slugs and triggers>
- Load on drift/slop suspicion: llm-failure-modes; anti-slop; jerry-behaviour when reviewing agent-produced artifacts
```

## Sliding Context Protocol

At every continuation, the worker reads the goal and state doc, then reconciles the state doc with artifacts. The worker loads only the active phase doc unless it is advancing phases, recovering drift, or performing final review.

The contract doc is loaded at phase transitions, before final completion, when state and artifacts disagree, and whenever the worker is tempted to treat a plan, sample, report, or blocker note as completion.

This keeps the worker focused on the current sliver while preserving the full destination outside the context window.

If drift, reward-hacking, unsupported state, or success-shaped artifact production is detected, return to `RECONCILE`. Treat the current state doc and worker summaries as claims, not truth. Rebuild the current residue from the contract and artifacts, remove or mark unsupported state claims, load `llm-failure-modes`, and load `anti-slop` if the artifact or report has generic success-shaped language. If reviewing agent-produced artifacts or prior reviews, also load `reviewing-subagent-work` and `jerry-behaviour`. Only then choose `FOCUS`, `DECOMPOSE`, or `REVIEW`.

## State Machine

Use states as decision modes.

`RECONCILE`: compare state doc against artifacts and decide the current mode.

`FOCUS`: work the active phase's current sliver.

`CHECK`: gather evidence that the current sliver changed the world, not just the narrative.

`REVIEW`: send the contract, phase doc, and artifacts to an independent reviewer when judgment is required.

`ADVANCE`: update state only when phase evidence and required review pass.

`DECOMPOSE`: turn drift, failed attempts, or false completion pressure into smaller attempted work, subtracting solved pieces from the residue.

Externally owned preconditions are not a normal workflow state. They are residue leaves produced by `DECOMPOSE` only after smaller attainable work has been attempted or completed.

## Residue Ledger

Use a residue ledger only when decomposition can outlive the current context or branch. Do not make a ledger for a local failure that can be solved immediately.

The ledger is not an inventory of everything that could be done. It is the durable call stack for the current decomposition:

- root completion witness;
- active leaf being attempted now;
- parent chain from the root to the active leaf;
- open frontier siblings not yet attempted;
- closed siblings with artifact evidence proving solved or irrelevant.

Before entering a child leaf, record what parent residue the child is meant to decide and what artifact-level change would remove it from the parent. After the child changes state, reconcile the parent from evidence: solved children are subtracted, irrelevant children are justified from sources or artifacts, failed children remain open or become the next active leaf.

Do not close a parent from memory. A parent advances only when the ledger and artifacts show that its children cover the parent residue and each child is solved, irrelevant, or reduced to a smaller remaining leaf. If the parent spans context windows or the worker wants to report externally owned residue, require independent review of the contract, ledger branch, and artifacts before closing that parent or reporting the residue. If no independent review surface exists, the parent remains open for completion purposes. If the active path cannot be reconstructed after compaction, enter `RECONCILE` and rebuild the path from the contract, state doc, ledger, and artifacts before doing more work.

## Recursive Decomposition And Residue

A failed one-shot attempt is not yet a blocker, plan, or hard core. It is an observation about the current residue.

`DECOMPOSE` is a work state, not a reporting state:

- Restate the original objective and the residue still false in artifacts.
- Split the residue into smaller subpieces whose success or failure can be observed.
- If the work can branch or survive compaction, add the active child and its parent chain to the residue ledger before attempting it.
- Attempt one smaller subpiece with the real tools, data, proof method, or artifact standard.
- If it succeeds, integrate the result into the real work, record the evidence, and subtract it from the parent residue.
- If it fails, recurse on that smaller subpiece rather than naming the whole residue hard.
- Continue until all attainable sibling pieces have been completed, verified irrelevant, or reduced to a smaller failing leaf.

A residual hard core is earned, not declared. It is the residue left after this solve-and-slice loop, with completed subpieces named by artifact paths, command outputs, proof steps, processed units, review dispositions, or other durable evidence.

An externally owned precondition may be recorded only when the remaining residue leaf is missing authority or approval, missing credentialed access, unavailable external service or dependency proven by direct command/API evidence, contradictory source requirements quoted from sources, or destructive action outside approved boundaries. If that is not proven, stay in `DECOMPOSE` or return to `FOCUS` with the next smaller attempted piece.

Examples:

- "Tests fail and I do not know why" decomposes to the first failing command, then the first failing fixture or assertion. Passing fixtures stay fixed; only the failing fixture remains residue.
- "OCR quality is poor on equations" decomposes to one representative PDF and one expected equation preservation check. Pages or methods that pass are recorded; only the failing page/method boundary remains residue.
- "The reviewer rejected the implementation" decomposes to the first contract invariant the artifact violates. Corrected invariants are removed from the residue before addressing the next violation.
- "The API returns 401 and no credentials are available in the environment" can become an externally owned residue leaf only after the access boundary is verified on the smallest credentialed call.

## Independent Review

Use independent review when completion depends on judgment, when a parent residue spans context windows, or when the worker proposes externally owned residue. The reviewer receives the contract doc, active phase doc or ledger branch, and artifacts. The reviewer should not receive the worker's success narrative as evidence, and the worker should not paraphrase the acceptance criteria into the review prompt when the canonical docs can be provided directly.

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
