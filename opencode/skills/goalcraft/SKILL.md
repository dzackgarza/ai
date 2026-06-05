---
name: goalcraft
description: >-
  Turn a rough draft, vague ambition, or messy task brief into a powerful Codex
  /goal objective and, when needed, companion workflow docs for long-running
  autonomous work. Use when the user asks to write, improve, format, sharpen,
  stress-test, or activate a Codex goal, thread goal, durable goal, or /goal
  prompt.
---

# Goalcraft

## Core Contract

Convert messy intent into a compact, activation-ready Codex `/goal` objective that keeps the agent moving until the user's request is true in the world, not merely represented by a plan, status note, first batch, or plausible path toward completion.

The goal writer must compare observable completion consequences. Do not ask whether two phrasings are equivalent; compile both into the facts that would be true if marked complete, then compare those facts.

For long-horizon work, the `/goal` text is the only instruction guaranteed to remain in context across compaction. Treat it as a bootloader, not as the whole plan. It must point to already-created canonical workflow docs, name the state retrieval rule, require the current phase and required skills to be loaded, and preserve the completion witness and review gates. The returned goal objective must be less than 4,000 characters, and the working target is 3,400 characters. Prefer drafting the goal text only. Do not call `create_goal`, `thread/goal/set`, or otherwise activate a goal unless the user explicitly asks to start or set it.

For current Codex `/goal` mechanics, read [references/codex-goal-contract.md](references/codex-goal-contract.md) when the exact runtime behavior matters.

For multi-phase, repetitive, orchestration-heavy, compaction-sensitive, or review-sensitive work, read [references/long-horizon-workflows.md](references/long-horizon-workflows.md) before drafting the final goal.

Before proposing any concrete `/goal`, read [references/success-criteria-contracts.md](references/success-criteria-contracts.md) and use it to audit the proposed stopping criteria. This is mandatory even for simple goals.

## Two-Layer Skill Loading

Do not confuse writer-side skill context with worker-side skill routing.

Writer-side context is what the agent using `goalcraft` loads before designing a workflow-backed goal. It seeds the writer's judgment about state surfaces, failure modes, review architecture, decomposition, and agent-facing prose. Naming a skill in the final goal does not retroactively give the writer that context.

Worker-side routing is what the writer puts into the `/goal`, contract, state, and phase docs for future workers to load after compaction. Loading a skill while writing the goal does not make future workers load it.

Before drafting any workflow-backed goal, produce this internal synthesis:

> The writer-side skills needed before drafting are ___, because the workflow design must decide ___; the worker-side skills that must be written into the bootloader/docs are ___, loaded at ___, because future workers only keep the `/goal` text and retrieved docs.

If the sentence cannot name concrete existing skill slugs and the design decision each one supports, load the missing skills before drafting.

For every workflow-backed goal, load writer-side context for agent-facing wording, prompt contracts, canonical state, and drift control: `writing-for-agent-audiences`, `prompt-engineering`, `agent-memory`, and `llm-failure-modes`.

Load additional writer-side skills before deciding the workflow when their design question is present:

- Skill architecture or standalone-vs-reference decisions: `creating-skills`.
- Failure, hard residue, or decomposition states: `hard-problem-decomposition`.
- Orchestration or subagent lanes: `subagent-delegation`.
- Independent review gates or reviewer-bias controls: `reviewing-subagent-work` and `jerry-behaviour`.
- Generic success-shaped prose/code/design risks: `anti-slop`.
- Progress, completion, or status-report discipline: `hierarchical-task-framing` and `response-preparation`.

After this writer-side preparation, emit worker-side routing: exact skill slugs, load triggers, and the location where each trigger is enforced. Pre-retrieval skills belong in the `/goal` text because it is the only guaranteed long-term instruction. Always-on skills belong in the contract. Current state and phase-specific skills belong in state and phase docs.

## Workflow

### Calibrate The Request

Identify the rough objective, workspace, and expected end state from the user's words before drafting. If the user supplied a draft, treat it as evidence of intent, not as authoritative scope. If a repo or files are mentioned, inspect them before finalizing the goal. If a critical success criterion is missing, ask the smallest necessary question; otherwise state assumptions.

Build a request completion witness: the observable facts that would make a future user not need to issue another goal for the same intended task. Include work-product nouns, verbs, scale words, and implied user-visible outcomes from the original request.

### Compare Completion Consequences

For any candidate goal, build a draft completion witness: the observable facts that would be true if an agent marked that exact goal complete.

Compare the request witness and draft witness. If the request witness contains facts not guaranteed by the draft witness, revise the goal or create workflow docs. Do not reason from labels such as "this is the path to completion"; compare postconditions.

This is the core scope guard. The writer may honestly believe "set up the workflow", "process a representative batch", "write the plan", or "document the blocker" is equivalent to the user's request. Consequence comparison breaks that false equivalence by asking what would actually be true after completion.

For source-to-domain mapping goals, run the same consequence comparison on the unit of
work. If the request witness is a domain foundation, mathematical vocabulary, category
spec, API semantics, or other object-language state, do not draft a completion witness
whose natural unit is "every source surface that touches the area." A source-surface
audit is a different postcondition unless the user explicitly asked for that audit.
The goal must name the finite generator for the queue, the unit method that extracts
behavior from source/docs/examples before assigning vocabulary or owners, and any
separate compatibility/runtime/display/backend queue. Avoid scope words such as
"touches", "adjacent", "all related", or "every relevant" unless they compile to a
bounded generator and residue rule.

### Success Criteria As Contracts

Read [references/success-criteria-contracts.md](references/success-criteria-contracts.md) before writing a concrete goal. Apply it as an adversarial audit of the proposed stopping criteria, not as background reading.

The output goal must reflect the audit: every success criterion needs the exact boundary where success or failure is observed, the positive witness, the negative witness, the required process or owner, and the forbidden weaker substitutes. If the audit finds a cheaper path to satisfy the wording while leaving the intended outcome false, revise the goal before returning it. Treat goal-substitution, witness special-casing, milestone-as-success, deferral-as-success, literal-rule workarounds, wrong-method success, and fake-success pressure from missing off-ramps as default threats. For sufficiently complex and focused goals, write adversarial tests or a test plan that fails these misaligned completions before the worker can claim success.

### Choose Simple Or Workflow-Backed Goal

Use a simple goal only when the request completion witness, boundaries, and verification fit under the target without vague compression.

Use a workflow-backed goal when completion needs phased context, repeated loops, independent review, orchestration, recursive decomposition, or compaction resilience. Before writing the final `/goal`, create or update the contract, state, phase, and residue/queue docs needed for progressive disclosure in the canonical state surface. The `/goal` should name the full destination, state surface, retrieval rule, phase-loading rule, always-load skill rule, state-specific skill rule, and completion witness. Skills needed before any state decision must be named in the `/goal` text itself; phase-specific skills can be named in the progressive docs.

Workflow docs must cross-reference concrete existing skills by slug and trigger, not generic categories. At minimum: bugs, failing checks, unexpected behavior, integration failures, and unclear causality route to `systematic-debugging`; failed attempts, hard residue, pressure to defer, and blocked/off-ramp claims route to `hard-problem-decomposition`; adversarial test design routes to `test-guidelines`; orchestration routes to `subagent-delegation`; agent-work review routes to `reviewing-subagent-work` plus `jerry-behaviour`; substantive code/research gates route to `research-gate-review`; drift or reward-hacking suspicion routes to `llm-failure-modes`; slop suspicion routes to `anti-slop`; progress/completion reporting routes to `hierarchical-task-framing` or `response-preparation` when those reports are part of the workflow.

Workflow-backed goals must choose a canonical state surface before drafting. Prefer the active project's `iwe` memory graph for contract, state, phase, and residue-ledger docs when it exists or project docs prescribe it. Use `iwe find` before creating, `iwe retrieve -k <key>` when resuming, and `iwe update` or `iwe new` rather than loose Markdown files. If the project has a different documented goal/planning surface, use that documented surface and name it. Do not create ad hoc `notes.md`, `progress.md`, or chat-transcript-dependent state.

For source-to-domain mapping, classification, or inventory goals, the canonical state
surface must include the extraction queue, not just source file lists or mapping rows.
Each unit must carry source behavior, extracted domain operation, required vocabulary,
weakest structure or hypotheses, owner/placement, evidence, status, and residue. If the
goal has multiple queues, keep them separate: domain foundation/mathematical vocabulary,
source implementation inventory, and compatibility/runtime/display/backend audit.

### Shape Evidence And Stop Conditions

Use these as input thinking, not as required output fields: destination, starting point, core objective, scope, deliverables, non-regression constraints, autonomy rules, checkpoint rhythm, verification gates, done evidence, stop conditions, and success metric.

Make every requirement auditable against files, commands, PR state, logs, screenshots, external artifacts, or explicit user confirmation. Success is the intended deliverable produced through the aligned process and methods; a visible end artifact produced by a forbidden shortcut is not success.

For each verification gate, specify what must fail before the fix, what must pass after
the fix, and where the failure must occur. If the intended contract is "reject invalid
construction", a test that only rejects a later method call is not equivalent. If the
intended contract is "class-system enforcement", a hand-written runtime assertion is not
equivalent unless the goal explicitly accepts that weaker boundary.

For complex focused goals, include adversarial tests that assume the worker will try to
hack the goal. These tests should reject special-cased witnesses, output-shape-only
success, forbidden-method success, milestone substitution, deferral-as-success, and
off-ramp abuse. Failure messages should tell the worker to stop, audit for
reward-hacking, reload the goal contract, and realign to the intended object-level
behavior before continuing. Load `test-guidelines` before writing concrete test files
or test acceptance criteria.

A failed attempt enters recursive decomposition, not reporting. The worker preserves the original objective, decomposes the failed residue into smaller pieces, attempts one smaller piece, integrates any solved piece into the actual artifact or evidence trail, subtracts it from the residue, and recurses only on what remains. If this can branch or outlive the current context window, the workflow must put the decomposition state in the state doc as a compact residue ledger: active leaf, parent chain, open frontier, and closure evidence for solved or irrelevant siblings. The worker must never rely on memory to wind back up the tree.

A residual hard core may be named only after the attainable subpieces around it have been actually completed or ruled irrelevant by evidence, and after the parent chain has been reconciled from the ledger and artifacts. Do not add generic failure stop conditions; outside-agent residue can be recorded only after systematic debugging or recursive decomposition proves the remaining leaf depends on authority, access, an unavailable service, contradictory requirements, or destructive action outside approved boundaries.

When an impossibility off-ramp is needed, write it as a non-success state: the original objective remains unmet, the exact hard core is named, completed or irrelevant surrounding work is evidenced, and the external condition needed for progress is explicit. Require a durable audit trail of aligned attempts: source citations, root-cause observations, decomposition residues, commits or diffs, test or reproducer output, review findings, and the reason each attempt failed. A goal must not let partial progress, a report, a TODO, a status change, a vague blocker, or an unsupported self-report satisfy completion.

For hard or repeated failures, route the worker to `hard-problem-decomposition` so failure becomes smaller real work rather than a scope change. Any reusable operational lesson discovered while working should be saved through `agent-memory`; unresolved external work belongs in the project's issue tracker or documented backlog surface, not in the goal as a disguised completion condition.

### Keep The Objective Usable By Codex

Hard limit: the objective text after `/goal ` must be less than 4,000 characters. Working target: draft to 3,400 characters or fewer. Treat 3,800 characters or more as a failed draft even if it is technically below the hard limit.

Include exact commands only when they are already known from the repo or user. Avoid hidden flags in slash text. `/goal --tokens 50K ...` is literal objective text in the TUI, not parsed syntax. If a token budget is requested, present it separately from the objective text unless the target surface supports a separate budget field.

For complex or ambiguous work, recommend a planning/interview pass before setting the goal. For very large work, include subagent/orchestration guidance only when the current Codex environment supports subagents and the work can be split into bounded, reviewable lanes.

### Choose The Output Shape

Compact shape for broad or complex work: Destination, Starting point, Objective/scope, Preserve, Verification, Done/stop, Success metric.

Full shape only for narrow work where the first draft is comfortably under 3,400 characters. Do not force every planning concept into the `/goal`; compress only after consequence comparison passes. Merge deliverables into Objective/scope, must-not-regress into Preserve, and autonomy/checkpoint rhythm into Done/stop. Keep examples and candidate lists outside the goal unless they are essential execution constraints.

### Validate Length Before Returning

Put only the ready-to-paste `/goal ...` command in a temporary file or pipe it to this skill's bundled validator: resolve `scripts/validate_goal_length.py` relative to the directory containing this `SKILL.md`, then run it with `--target-chars 3400 --strict-target`.

The validator belongs to Goalcraft, not to the user's working project. Do not search the user's repository for `scripts/validate_goal_length.py`. The script strips a leading `/goal ` and counts the actual objective Codex validates.

If over 3,999 characters, compress and revalidate. If 3,800 to 3,999 characters, compress and revalidate. If 3,400 to 3,799 characters, accept only when removing more text would lose important safety or verification detail; otherwise compress and revalidate. Do not return a final goal until the validator passes.

If the bundled script path is unavailable, use this deterministic fallback on the file containing the exact final `/goal ...` command:

```bash
python3 - "$GOAL_FILE" <<'PY'
import pathlib, sys
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").strip()
if text.startswith("```"):
    lines = text.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    text = "\n".join(lines).strip()
if text.startswith("/goal") and text[len("/goal"):].startswith((" ", "\n", "\t")):
    text = text[len("/goal"):].strip()
count = len(text)
print(f"objective_chars={count}")
if count > 3400:
    raise SystemExit(1)
PY
```

### Decide Output Mode

Default: return a ready-to-paste `/goal ...` block plus a short assumptions list.

If the user asks for review, critique the draft first and include a revised version. If workflow docs are necessary and file edits are allowed, create or update them before returning the goal. If file edits are not allowed, return the docs as required companion text and state that the goal is not safe to activate until those docs exist in the named canonical state surface. Do not return a workflow-backed goal that references missing docs.

If the user explicitly asks to activate the goal, call the goal tool or app-server surface only after the objective is final and no existing active goal conflict is unresolved.

## Output Format

Use the compact shape by default:

```markdown
Assumptions:
- ...

Ready-to-paste goal:

/goal Destination: ...

Starting point: ...

Objective/scope: ...

Preserve: ...

Verification: ...

Done/stop: ...

Success metric: ...
```

Use the longer field list only for narrow work where the first draft validates comfortably under 3,400 characters.

After the block, report the validated objective character count, for example: `Objective length: 2,914 characters`.

For workflow-backed goals, include companion docs first:

```markdown
Workflow docs:
- Contract: <iwe key or documented path> - request completion witness, Reference Skills for always-on and review/drift gates, and final review standard.
- State: <iwe key or documented path> - current phase, active phase doc, skills to load now, next focus, evidence, current residue, and active residue ledger when decomposition spans context.
- Phase docs: <iwe keys or documented paths> - load only the active phase unless advancing or reviewing; each has a Reference Skills section naming exact state-specific skill slugs and triggers.
- Pre-retrieval skills in goal text: <skills that must be loaded before state decisions>.

Ready-to-paste goal:

/goal Destination: ...

Workflow entry: ...
```

## Quality Bar

- The goal should be operationally sharp enough that another agent can continue after compaction or resume.
- For workflow-backed work, the `/goal` text should act as a bootloader: retrieve canonical state, load always-on skills, load the active phase and state-specific skills, reconcile artifacts, then work.
- The goal should preserve the request completion witness, not the writer's first plausible interpretation of what would count as progress.
- The goal should compare observable consequences whenever two scopes sound equivalent.
- The goal should be adversarially complete: every success criterion names the exact
  boundary where success/failure is observed and bans the nearest weaker substitutes.
- Workflow-backed goals should reveal the current phase and active residue path without repeatedly flooding the worker with the whole task.
- Workflow-backed goals should use canonical searchable state surfaces, preferably project-local `iwe`; loose files and transcript memory are not durable state.
- Workflow docs should contain explicit Reference Skills sections; "review", "debug", "detect drift", or "handle slop" without exact skill slugs is too vague.
- Large routine queues should keep their required unit method; scale alone does not justify a weaker method.
- A failed attempt should trigger recursive decomposition; any smaller piece that can be solved must be completed and removed from the residue before blocker or follow-up language is available.
- Independent review should read the contract and artifacts directly from canonical docs; the worker's paraphrase or self-report is not completion evidence.
- The goal should make premature completion hard: "done" must require evidence, not intent, elapsed time, or passing unrelated checks.
- The goal should avoid over-prescribing implementation details unless those details are part of the actual requirement.
- The goal should preserve user boundaries: planning-only, no edits, no deploys, no commits, or approval requirements must be explicit when present.
- The final ready-to-paste goal must pass this skill's bundled `scripts/validate_goal_length.py --target-chars 3400 --strict-target` or the deterministic fallback above.
