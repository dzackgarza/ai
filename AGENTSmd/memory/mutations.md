---
order: 20
tags:
- source-system-contract
- source-observed-model-failure
- function-define
- function-constrain
- function-procedure
- function-route
- function-evaluate
- failure-state-misplacement
- failure-completion-laundering
- failure-scope-drift
- retest-model-alignment
- retest-model-memory
- retest-policy-change
- retest-toolchain-change
title: Mutations
---

Load `agent-memory` before updating, deleting, moving, splitting, merging, or squashing
memories.

Memory mutation requires an explicit user request or a task instruction that directly
requires durable memory storage.
Capturing a durable expectation the user has just communicated — an app decision,
ownership boundary, purpose, goal, or constraint — is such an instruction; persist and
reconcile it per **Capturing Communicated Expectations** without waiting for a separate
"save this" request.
Do not mutate memories as a substitute for committing, documenting, or completing the
requested work.
