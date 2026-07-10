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
- retest-model-alignment
- retest-model-memory
- retest-policy-change
- retest-toolchain-change
title: Capturing Communicated Expectations
---

Whenever the user communicates an app decision, ownership boundary, purpose, goal,
constraint, scope rule, naming convention, or any other durable expectation in chat,
treat that message as a durable-knowledge event, not a one-off instruction.

Before continuing the requested work, check whether the expectation is already encoded in
the repo's knowledge base — project memory, plan records, the wiki, or the owning GitHub
issue/milestone. If it is not already present, persist it immediately:

- Capture the expectation as the appropriate typed `agent-memory` record (`decision` for a
  chosen direction, `context` for app purpose or boundary, `advice` for a working
  constraint, `trap` for a correction that must change future behavior).
- Record it in the user's own terms: what was decided or expected, what it governs, and why,
  so a future agent reads the rule without needing the user to restate it.

Then reconcile it against the existing durable surfaces. If the vault, wiki, or GitHub
issue tree already says something that diverges from what the user just communicated, the
new statement is authoritative: update the stale surface so every durable record agrees.
If the expectation changes public project direction, user stories, proof burdens, roadmaps,
or cross-agent handoff state, promote it to the owning GitHub issue, milestone, PR, or wiki
page as well as memory (see the **Promote** rule above).

The objective is a self-sufficient knowledge base: the user should never have to correct or
re-explain the same app philosophy twice. Every communicated expectation that survives the
conversation must end the turn encoded somewhere durable and consistent across all
surfaces, not left to live only in chat.

Capturing a freshly communicated durable expectation is itself a task instruction that
requires durable storage, so it satisfies the mutation precondition below — you do not need
a separate explicit "save this" request to record it.
