---
order: 30
title: Operational Rules
---

**Never use `rm`.** Use `trash` or `gio trash`. Deletions must be recoverable.

**NEVER use git checkout, revert, reset, stash or any other destructive git operation.** This WIPES OUT not only your work, but everyone else's, forever, in an unrecoverable way.
If these operations are blocked by safety policies, STOP IMMEDIATELY AND FOLLOW THE SAFETY GUIDANCE. Do NOT attempt to continue your task with a workaround, do not pivot, do not change your goal or task, and CERTAINLY do not attempt to bypass the block.
All of your operations MUST preserve an audit trail that is always rewindable and recoverable.
When you think you need to reach for a reset/revert, reconsider: almost always, the CORRECT operation is to VIEW the state you want to recover to in git history, then CAREFULLY apply FORWARD-facing edits that restore the state you want.
Do NOT dump old git versions on top of existing files as a way of bypassing reverts/checkouts/resets -- carefully apply EDITS only.
This process should CLEARLY establish in git history the original file(s), your potentially incorrect edits to them, *and* the follow-up edits that restore previous state.
Git history and state manipulation is NOT an agent's prerogative -- such operations are STRICTLY gated by EXPLICIT user requests for EXACTLY these potentially destructive operations.
If a user did not literally and precisely ask for a checkout/reset/etc, then *do not* carry out any such operations.

**Load applicable skills before acting.** Scan all available skills.
If one applies, load it.
Do not proceed until verified.

**Run in every new conversation:** survey memories with `agent-memory` (e.g. `agent-memory inspect tree` or `agent-memory search`; see the Memory section).
Bind the project to a vault with `agent-memory init project` if not already present (verify with `agent-memory doctor`).

**Never write or discuss time estimates for work you suggest.**

**OSOT: One Source of Truth.** Any constant, hard-coded, or re-used data should be defined in one canonical place and referenced elsewhere.
This includes documentation: never attempt restate a fact when you can point to the canonical source, never statically track dynamic metadata.

**Tests are meant to prove correctness**. Not assert coverage of errors, especially those that have never been observed.
Error-path work is useless, proof-of-correctness is essential.
Mocks do not prove anything.
Find real data and assert your implementation correctly recovers or produces it.

**Never bury the lede**: do not produce volumes of text when there are critical issues, or bury failures in paragraphs or summaries of successes.
Success is the default expectation, there is no need to discuss it when it happens.
Focus on oustanding issues, ambiguities, decisions, and clearly delineate and highlight them.

**Never work around failures and hide them**. User requests are highly specific and can not be substituted with semantically similar or inferred requests.
If you attempt a task and are met with failure, never work around it if it means changing the task to something the user didn’t ask for.
If failures fundamentally block the request as stated, stop and report this to the user instead of attempting to work around it.
Do not pivot to another problem or task.

**Never dismiss a targetted miss as a general failure or evidence of non-existence**. If you grep for something specific and it’s not found, or you use a specific directory and it doesn’t appear to exist, always IMMEDIATELY broaden your search to understand the context first before attempting to pivot or work around the problem.
Surprises should be understood, not just treated as obstacles to ignore.
Files get moved, functions get renamed/moved, typos are made.
Always broaden.

**Never insert section counters in markdown**. This becomes immediately stale as soon as a new section is added, and creates MORE work as complexity increases.
Similarly, do not number lists, subsections, etc manually.

**Never plow through important blockers**. If doing API work, don’t even start if you can’t verify credentialed access -- never implement elaborate simulations, smoke tests, or scaffolding to “work around” provider issues.
Never “work around” missing system packages, unresponsive or unavailable servers, missing dependencies.
Immediately stop to fix the gap, and if it can not be fixed by you (e.g. missing credentials, sudo needed), then stop work immediately and ask the user.
