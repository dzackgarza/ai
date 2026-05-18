---
name: research-project-workflow
description: Use when handling research repo planning, root `plans/` Nimbalyst
  tracker files, layer-gated plan decomposition, TODO triage, retired cards,
  visual windows, or card metadata. This is the entry-point skill for the
  research repo workflow.
---

# Research Project Workflow

This skill is the canonical repo-level workflow authority for Nimbalyst-backed features, specs, plans, phases, tasks, decisions, and project-management state in the research repo.

## Canonical source

The source of truth is this skill plus `references/project-workflow.md` (loaded from
`.agents/skills/research-project-workflow/references/project-workflow.md`), interpreted
against the reusable framework in `/home/dzack/ai/planning/AGENTS.md` and the
installed local schemas in `.nimbalyst/trackers/`.

Read `references/project-workflow.md` before creating, migrating, normalizing,
retiring, or interpreting root `plans/` tracker files.

## How to load repo-local skills

Skills referenced by the research repo's `AGENTS.md` (research-state-machine,
research-project-workflow, research-orchestration, research-proof-auditing,
research-code-style, research-repo-structure, research-math-boundary,
research-software-wiring, research-source-acquisition, vinberg-algorithm,
category-spec-*, git-guidelines, etc.) live under `.agents/skills/*/` as plain
markdown files. They are NOT registered Hermes skills — `skill_view(name)` will not
find them. To load one, read it as a file: `.agents/skills/<name>/SKILL.md`.
Likewise, their reference files live under `.agents/skills/<name>/references/<file>.md`.

## Startup routine for this repo

Every new session must:

1. Read `GOAL.md`, `.agents/current-goal-phase.md`, and root `AGENTS.md`.
2. Load the matching local skills from `.agents/skills/` by reading their SKILL.md
   files — especially `research-state-machine` (for plan-to-execution routing and
   the review protocol) and `research-project-workflow` (for Nimbalyst mechanics).
3. Before touching any card in `needs-agent-review` status, read
   `research-state-machine/references/review-kernel.md` — it defines the 6-gate
   ordered protocol that must be applied by an independent reviewer.
4. Read `plans/AGENTS.md` for planning workspace structure and DAG rules.
5. Run `iwe` to load project memory under `.agents/memories`.

## Task execution posture

When the user gives an explicit goal, execute it. Do not ask for permission to
proceed or offer a menu of options unless you have genuinely hit a decision boundary
that cannot be resolved from the repo docs and established conventions. "Carry out
all tasks" means do the work, not ask which to do first. A question signals a
blocking ambiguity, not a polite default.

## The needs-agent-review protocol

**Load `research-gate-review` BEFORE touching any card in `needs-agent-review` status** — it contains
anti-boxchecking rules, bug-pattern references, subagent dispatch mechanics, and review-log
writing discipline that operationalize the abstract 6-gate protocol. Do not apply the gates
inline in your own session; delegate to fresh-context subagents per the review kernel.

A card in `needs-agent-review` status is not waiting for a human. It needs the
6-gate ordered protocol from `research-state-machine/references/review-kernel.md`
applied by an independent reviewer (not the implementer):

1. Gate 1: Definition Grounding — every definition traces to a source
2. Gate 2: Acceptance Criteria — criteria are met or revised with evidence
3. Gate 3: Spec-Weakening — no obligations deleted without replacement
4. Gate 4: Gradient — no backsliding on previous decisions
5. Gate 5: Mathematical Correctness — claims are well-typed and coherent
6. Gate 6: Style and Compliance — repo rules followed

Stop at the first failing gate. Outcome: complete/done, revision-required, or blocked.
Document in a `## Review Log` section in the card body.

## Core policy

- Root `plans/` is the active repo-local tracker workspace.
- The GUI is the index; do not create aggregate tracker indexes.
- Use only registered standard tracker types from `.nimbalyst/trackers/*.yaml`.
- Use the root feature/plan/phase/task hierarchy for workflow dimensions. Tags are secondary grouping aids.
- There is no separate backlog; active cards are the outstanding work set.
- Completed feature trees should be moved under `plans/features/completed/` rather
  than left alongside active feature roots.
- Execute according to the DAG. Unmet declared dependencies mean a card remains
  `unstarted`; `blocked` is reserved for ready leaves stopped by a prerequisite that is
  not currently satisfiable through the DAG.
- Work top-down through feature/spec, plan, phase, and task gates. Do not create
  lower-layer cards before the owning layer is approved.
- Plans are human + LLM collaborative artifacts and must be approved before
  decomposition or execution.
- Executable work belongs in dedicated tracked files, not chat-only plans or inline markers.
- Decision cards are feature-level blockers only; do not leave unresolved decision
  language inside feature, spec, plan, phase, or task bodies.
- Validate planning edits with the repo-local recipe and stage generated tag or DAG
  changes deliberately.

## Hook auto-fix policy

Repo hooks (lint, format, validate) may auto-modify files in your working tree.
Observed auto-fix targets:

- `.agents/skills/*.md` — hook-added cross-references and routing notes
- `.nimbalyst/trackers/*.yaml` — schema additions (e.g., new status values)
- `.agents/scripts/*.py` — report generator updates
- `plans/plan-dag.md`, `plans/card-progress-report.md` — auto-regenerated by
  plan validation

Per AGENTS.md: auto-fixes are carried forward, not rolled back. If you see
unexpected changes to these paths, check `git diff` to verify the change is
cosmetic/structure-only. If it touches code or definitions, report it.

Do not treat hook auto-fixes as evidence that you accidentally modified
things — they are normal repo hygiene.

## References

- `references/review-workflow.md` — 6-gate ordered review protocol for needs-agent-review cards
- `references/dag-completeness-audit.md` — methodology for verifying whether all DAG-executable work is exhausted; use when asked to "carry out all tasks" or verify goal completion

## Load with

- Load `task` or `track` before creating individual tracker items.
- Load `category-spec-workflow` for category-spec-specific planning, triage, priority, visuals, or retirement.
- Load `research-state-machine` when planned work moves into execution, preflight, replay/attack, promotion, rejection, splitting, or `GOAL.md` discharge. Load `research-orchestration` for delegation, worktrees, self-check, adversarial audit, and artifact handoff.
- Load `research-scheduling` when a plan or card needs a delayed wakeup, recurring maintenance, autonomous cadence, or migration from fixed schedule thinking.
