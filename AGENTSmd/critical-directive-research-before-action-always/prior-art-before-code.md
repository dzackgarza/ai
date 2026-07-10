---
order: 20
tags:
- source-owner-preference
- source-system-contract
- source-observed-model-failure
- function-constrain
- function-procedure
- function-route
- function-evaluate
- failure-premature-action
- failure-tool-bypass
- failure-process-overproduction
- retest-model-reasoning
- retest-model-tool-use
- retest-policy-change
- retest-toolchain-change
title: Prior Art and Documentation Before Code
---

Before writing nontrivial code, or diving into source to explain an external behavior,
spend the cheap effort to find what already exists. Agents routinely skip this and lose
far more time building, debugging, or guessing than the search would have cost.

- **Read the docs first.** For any library, framework, SDK, API, CLI, or cloud service —
  even familiar ones — pull current documentation through Context7 or DeepWiki before
  coding against it or inferring its behavior. Training data is stale; the live contract
  is not. Load `known-solution-first`.
- **Find prior art before greenfield.** Before implementing from scratch, look for an
  existing library, official recipe, reference implementation, or forkable project that
  already solves the task. Reusing, forking, or following a reference beats bespoke code.
  Climb the reuse ladder before writing anything new.
- **Search before you dig.** When an external tool, package, compiler, or API errors or
  behaves unexpectedly, run a plain web search and check the project's GitHub
  issues/discussions before reading its source or inventing an explanation. The meaning
  of an external diagnostic is owned by that project, and someone has very likely hit it
  already.

Source-diving, greenfield implementation, and from-first-principles reasoning are the
expensive fallback, not the first move, whenever an implementation or diagnostic question
is owned by an external project. Load `known-solution-first` when that external contract
materially controls the requested action.

This is not a fixed research or acquisition funnel. For open-ended source discovery,
hard-to-find artifacts, or an explicit request to move beyond standard workflows, treat
local metadata and familiar services as leads rather than boundaries. Diversify search
strategies when the normal path has low expected yield instead of completing the usual
workflow for its own sake.
