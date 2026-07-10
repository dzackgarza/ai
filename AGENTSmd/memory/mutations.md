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
- failure-process-overproduction
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
Capturing a clearly durable expectation the user has just communicated — an app decision,
stable ownership boundary, purpose, or long-lived constraint — is such an instruction.
Persist it per **Capturing Communicated Expectations** after the immediate bounded action;
do not promote task-local directions or interrupt an obvious correction for memory work.
Do not mutate memories as a substitute for committing, documenting, or completing the
requested work.
