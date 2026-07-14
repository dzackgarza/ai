---
name: hard-problem-decomposition
description: Use when a hard task, repeated failure, unclear causality, or long-running goal creates pressure to pivot, defer, narrow scope, report blocked, or treat a failed one-shot attempt as an external blocker before recursive decomposition has reduced the residue.
---

# Hard Problem Decomposition

Use this skill to turn a failed attempt into recursive solve-and-slice work while preserving the original objective and the parent chain that gives each subproblem meaning.

## Core Contract

A failed one-shot attempt is raw evidence, not a diagnosis. The hard part is not whatever the worker first failed to do. The hard part is the residue left after decomposing the failed work, actually completing smaller attainable pieces, and recursing on what remains.

If no smaller piece has been attempted and either solved, integrated, or split into a strictly smaller failed leaf with evidence, no hard core has been isolated.

If decomposition may span context or branch, the active path must be externalized in [[agent-memory/SKILL|agent-memory]] before going deeper. Do not trust the chat transcript or the worker's memory to remember where the leaf came from.

## Residue Gate

Before any blocked, deferred, escalation, or hard-core language, the worker must be able to cite evidence for this statement:

> The original completion witness is still _____. The current residue is _____, evidenced by _____. Since the failed attempt, I decomposed it into _____; I completed or ruled irrelevant _____, evidenced by _____; the remaining unsolved piece is _____; the next smaller piece to attempt is _____.

If the completed-or-irrelevant slot is empty, the agent is still at the first failed attempt and must not name a hard core. If the evidence slots point only to the worker's explanation rather than artifacts, command output, source text, proof steps, processed units, or independent review findings, keep decomposing.

## Recursive Solve-And-Slice Loop

Freeze the original objective first. Load the goal, contract, issue, plan, or user request that defines completion. The failed attempt is interpreted against that objective, not used to rewrite it.

Define the current residue: the smallest statement of what remains false in the real artifact, proof, dataset, repo, or external system. Do not start from "what feels hard"; start from the completion witness facts not yet true.

Decompose the residue into smaller subpieces whose outcomes can be observed. Use the natural structure of the work: files, tests, invariants, pages, queue units, proof lemmas, data slices, API boundaries, UI states, review comments, or dependency edges.

Before descending into a subpiece that can outlive the context window, write the active path into the canonical state note or residue ledger: root objective, parent residue, active leaf, open siblings, and what evidence would remove the leaf from its parent. Use the canonical tool for that surface, such as `agent-memory search`, `agent-memory retrieve`, and `agent-memory update` for project memory. This is not optional bookkeeping; it is the only way a resumed worker can climb back to the parent without inventing state.

Attempt one smaller subpiece with the real toolchain, data, proof method, artifact standard, or reviewer standard. Planning the attempt is not an attempt. A useful attempt changes the artifact or produces decisive evidence about that subpiece.

When a smaller piece is solvable, finish it and integrate it into the real work. Change the code, process the unit, prove the lemma, correct the artifact, update the source-of-truth state, or record the durable evidence required by the workflow. Then subtract that piece from the residue.

When a smaller piece fails, recurse on that piece. Split it again if possible, attempt the next smaller subpiece, and keep any solved siblings. Do not promote the failed subpiece to "blocked" merely because the first attempt failed. If you descend, update the active path first.

Stop decomposing only when the remaining residue leaf cannot be split further without losing the decisive unknown, and the neighboring attainable pieces have been completed, verified irrelevant, or reduced to their own leaves with evidence.

For large routine workloads, the next queue unit is the smaller piece. Completing one unit is real progress and evidence for the method, but it does not complete or replace the full objective; the residue remains the unprocessed queue.

## Returning To The Parent

Do not wind back up the tree from memory. Read the parent chain from the canonical state surface or residue ledger and reconcile each parent from artifacts.

A child can be subtracted from its parent only when the artifact or evidence named before descent now exists. A parent can advance only when its open children cover the parent residue and each child is solved, irrelevant by source/artifact evidence, or reduced to a smaller remaining leaf. If that relation is unclear, the next task is reconciliation, not more decomposition.

If a parent spans context windows, or if the remaining leaf is about to be reported as outside-agent residue, ask an independent reviewer to read the original completion witness, the ledger branch, and the artifacts. The reviewer decides whether the child evidence really removes the parent residue; the worker's narrative does not decide that. If no independent review surface exists, the parent remains open for completion purposes.

Before marking the original objective complete, reload the root completion witness and verify that the root residue is empty. A solved deep leaf is never completion evidence for the root unless the parent chain shows how it removes the root residue.

## Failure Observations

Describe each failed attempt as an observation:

- what was attempted;
- what concrete output, error, review finding, or missing artifact resulted;
- what expected observation did not occur;
- what evidence was actually gathered.

Use observations to choose the next decomposition boundary: input data, source material, method/tool choice, implementation, environment/access, verification criteria, or artifact quality. If the boundary is unclear, the next action should distinguish boundaries.

## Evidence-Changing Actions

Good next actions change the residue:

- run the smallest reproducer for one failing behavior;
- compare two candidate methods on the same unit;
- prove or refute the next lemma needed by the proof;
- fix one violated invariant and rerun the relevant check;
- process the next queue unit with the required quality check;
- read the authoritative source that decides one contradiction;
- ask an independent reviewer to judge one contract invariant against artifacts.

Weak next actions preserve fog: "investigate issues", "document remaining work", "create a follow-up plan", "improve quality", "handle blockers", or "try again" without a smaller target.

## What Counts As Residue

Residue is the part of the original objective still false after solved pieces are subtracted.

Good residue statements are earned by completed neighboring work:

- "Find why command X exits with error Y on fixture Z."
- "Determine whether OCR service A or B preserves equations on this representative PDF."
- "Repair the first contract invariant the reviewer found false."
- "Prove or refute lemma L under hypothesis H."
- "Process the next corpus unit with the required quality check."

Weak residue statements are guesses from a failed one-shot:

- "Finish the hard part."
- "Investigate issues."
- "Improve quality."
- "Document remaining work."
- "Create a follow-up plan."

## Outside-Agent Residue Leaves

An outside-agent residue leaf exists only after recursive decomposition has reduced the problem to one of these directly evidenced leaves:

- missing user decision or authority;
- missing credentialed access;
- unavailable external service or dependency shown by direct command/API evidence;
- contradictory requirements quoted from source material;
- destructive or irreversible action outside approval boundaries.

Reporting one of these leaves keeps the original goal incomplete. The report must name the original objective, the current residue, the smaller pieces already completed or ruled irrelevant, the direct evidence for outside ownership, and the smallest user or environment change that would unblock the residue.
