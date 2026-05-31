# DAG Completeness Audit

Use this when asked to “carry out all tasks from cards” or “continue until all tasks are
blocked/need-human-decisions” and you need to verify whether there is genuinely
remaining executable work.

## Core question

Does every card in the DAG fit into exactly one of these buckets?

- **complete** — ACs satisfied, implementation done, and the workflow allows closure

- **needs-agent-review** — implementation/research done and ACs checked, but waiting for
  independent agent review

- **needs-human-input** — agent review passed or work otherwise requires human judgment,
  acceptance, or a decision

- **blocked** — ready current-phase leaf stopped by an external prerequisite not
  satisfiable through the DAG

- **unstarted with unmet dependsOn** — correctly placed as unstarted because declared
  dependencies are incomplete

- **downstream-phase** — blocked by GOAL.md phase policy, not by a card-local dependency

If any card is **unstarted without unmet dependsOn** and within the active phase, there
is executable work remaining.

## Audit procedure

### Step 1: Get status distribution from plan-dag.md

The plan-dag.md mermaid graph embeds statuses in bracket notation:

```bash
grep -E '\[unstarted\]|\[in-progress\]|\[needs-agent-review\]|\[needs-human-input\]|\[complete\]' plans/plan-dag.md \
  | grep -v 'status_' \
  | sort | uniq -c | sort -rn
```

The `| grep -v 'status_'` filter is critical — mermaid also emits CSS class labels like
`status_needs_agent_review` alongside the actual bracket status.
Only the bracket notation represents the canonical DAG status.

### Step 2: Cross-reference with card-progress-report

Read `plans/card-progress-report.md`. It aggregates stats from the Nimbalyst tracker
schema. It may show different counts than the DAG because it reads actual card
frontmatter rather than mermaid labels.

Discrepancy signal: if the report says 0 unstarted but the DAG shows unstarted nodes,
check whether those unstarted nodes have `dependsOn` edges that are incomplete — that’s
the correct “unstarted with unmet deps” state.

### Step 3: Check AGENTS.md blocker rules

Per the repo’s AGENTS.md:

- “Follow the planning DAG literally.
  Do not even attempt a task whose declared dependencies are incomplete.
  A task with unmet dependsOn edges is unstarted, not blocked.”

- “Reserve blocked for a ready current-phase leaf that cannot proceed because it needs
  an external decision, source, credential, missing theory, or other prerequisite that
  is not currently satisfiable through the DAG.”

- “Blockers are phase-local and path-local unless proven otherwise.
  A downstream-phase guard, implementation-only gate, QC failure outside a
  transition/integration pass, oversized card, missing vocabulary, or missing backend
  bridge is not a reason to exit the active goal while approved phase-local spec,
  research, decision, or decomposition cards remain.”

- “Do not report 'no path forward' until the active phase, approved plans, and active
  leaf cards have been checked and every remaining leaf has a concrete blocker that
  applies to that leaf in the current phase.”

### Step 4: Check individual card bodies for actual AC progress

For needs-agent-review cards, the frontmatter status only tells you so much.
Read the actual card body to verify:

- Are ACs checked `[x]` or unchecked `[ ]`?

- Is there a work log showing what was done?

- Has a 6-gate review been applied and documented?

- Has the card been reviewed by someone other than the implementer?

A card marked needs-agent-review with all ACs checked, a work log showing completed
implementation, and no 6-gate review log still needs independent agent review.

A card marked needs-agent-review with a passing 6-gate review should not remain in that
status.
Move it to `complete` if the workflow permits agent closure; otherwise move it to
`needs-human-input` with the concrete human signoff or decision required.

A card marked needs-agent-review with unchecked ACs may have remaining executable work.

### Step 5: Verify the active phase boundary

Read `.agents/current-goal-phase.md`. Identify which features belong to the active
phase. Cards in other features (e.g., Coble research features, lattice phases) are:

- **downstream-phase** if they depend on foundation vocabulary that hasn’t settled yet

- Only actionable if they are concrete approved leaves within the active phase

### Step 6: Check for stale references

Search for stale file references that could indicate unfinished migration:

```bash
grep -rn "plans/todo\.md" plans/ category_specs/ 2>/dev/null
```

But evaluate critically: are these actionable cleanup items, or intentional provenance
notes pointing to `git show ...` for history recovery?
The latter pattern (e.g., “Recover with `git show <commit>:plans/todo.md`”) is normal
provenance documentation and should not be treated as a stale reference.

## Decision table

| DAG shows | Individual card shows | Meaning | Action |
| --- | --- | --- | --- |
| needs-agent-review | ACs all `[x]`, work log complete, no review log | Agent review still required | Dispatch independent review. |
| needs-agent-review | 6-gate passed but human acceptance required | Waiting for human input, not agent review | Move to `needs-human-input` with the concrete signoff question. |
| needs-agent-review | Some ACs `[ ]`, no review log | Work may be incomplete | Read the card and determine what remains. If dependencies are satisfied, execute the remaining work. |
| needs-human-input | Review passed or decision needed | Human judgment is required | Do not substitute agent review for the human decision. |
| unstarted | No `dependsOn` or all deps complete | Needs work | Execute if within active phase and not blocked by policy. |
| unstarted | has incomplete `dependsOn` | Correctly placed | Do not start. |
| in-progress | — | Something is actively being worked on | Check current branch/worktree for in-progress state. |
| approved-and-unstarted | — | Approved but not yet scoped for execution | Check if the phase transition has been authorized. |

## Pitfalls

- **Do not conflate needs-agent-review with human signoff.** A card in
  `needs-agent-review` requires independent agent review.
  A reviewed card waiting for human approval belongs in `needs-human-input`.

- **Do not conflate unstarted with blocked.** A card is unstarted because its declared
  dependencies are incomplete.
  It is not “blocked” in the DAG sense — it has simply not yet been reachable.

- **Do not conflate downstream-phase with stuck.** Features in later GOAL.md phases are
  intentionally gated.
  Their unstarted status is correct per the staged program, not a sign of stalled work.

- **The 6-gate review must be substantively reading code, not just checking metadata.**
  See research-gate-review skill for the non-checkboxing mandate.

- **A card whose ACs reference a deleted file (e.g., `plans/todo.md`) may still have
  actionable ACs** if the intent is to verify against recovered git history.
  Check whether the AC is marked done and whether the reference is provenance (pointing
  to `git show`) vs a live requirement.
