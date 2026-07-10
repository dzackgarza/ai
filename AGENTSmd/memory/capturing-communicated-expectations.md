---
order: 15
tags:
- source-system-contract
- source-observed-model-failure
- function-define
- function-constrain
- function-procedure
- function-route
- function-allocate
- failure-state-misplacement
- failure-context-loss
- failure-process-overproduction
- retest-model-alignment
- retest-model-memory
- retest-policy-change
- retest-toolchain-change
title: Capturing Communicated Expectations
---

Treat a communicated expectation as durable knowledge only when it clearly governs future
sessions or workers: an app decision, stable ownership boundary, durable purpose,
long-lived constraint, or recurring naming convention.
A task-local instruction or obvious course correction is not automatically a memory
event.

Complete the immediate bounded action first unless the missing knowledge would cause an
unsafe or immediately repeated mistake. Then check whether the durable expectation is
already encoded in its owning knowledge surface. If not, persist it:

- Capture the expectation as the appropriate typed `agent-memory` record (`decision` for a
  chosen direction, `context` for app purpose or boundary, `advice` for a working
  constraint, `trap` for a correction that must change future behavior).
- Record it in the user's own terms: what was decided or expected, what it governs, and why,
  so a future agent reads the rule without needing the user to restate it.

Reconcile only the surfaces that actually own or publish the fact. If the vault, wiki, or
GitHub issue tree says something divergent, the new statement is authoritative: update
the stale owning surface rather than copying the same fact everywhere.
If the expectation changes public project direction, user stories, proof burdens, roadmaps,
or cross-agent handoff state, promote it to the owning GitHub issue, milestone, PR, or wiki
page as well as memory (see the **Promote** rule above).

The objective is a self-sufficient knowledge base without making memory maintenance a
prerequisite for direct work. A durable expectation should end the turn in its canonical
surface; ephemeral instructions should not be promoted.

Capturing a freshly communicated durable expectation is itself a task instruction that
requires durable storage, so it satisfies the mutation precondition below — you do not need
a separate explicit "save this" request to record it.
