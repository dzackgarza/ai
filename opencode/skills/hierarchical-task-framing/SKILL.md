---
name: hierarchical-task-framing
description: Use when completing a sub-task, reporting progress, or any time you are about to describe what was done. Prevents drift from meta-goals into artifact fixation.
---

# Hierarchical Task Framing

## The Failure

Models zoom into concrete sub-problems (individual files, single test runs, specific artifacts) and lose the meta-level objective. This manifests as reporting artifact status to the user when the user needs process validity assessment.

In a 40-hour session, this was the most frequently recurring failure: 6 instances, 8+ explicit corrections, with a **2-3 turn reversion rate** — even after correction, the model drifted back within a few exchanges.

The cycle:

- Work on sub-problem
- Report completion or status of the artifact
- User: "Did you forget the ACTUAL task?"
- Model recognizes drift, restates the real goal
- Resumes work
- Drifts again within 2-3 turns

## Why This Happens

Concrete artifacts are **locally rewarding**: a file was edited, a test passed, a run produced output. These are tangible, reportable, and feel like progress. The meta-goal (refine a process, improve a skill, validate an architecture) is abstract and harder to report on. The model gravitates toward reporting what it can point at.

The deeper problem: the model confuses **evidence** with **deliverables**. Individual artifacts are evidence that a process works (or doesn't). They are not the deliverable. The deliverable is the process itself.

## Forcing Questions

Before reporting progress or completing a sub-task, answer:

**Q1: "What is the OVERALL task the user assigned?"**

A: [restate it — must be at the meta/process level, not artifact level]

**Q2: "Is what I'm about to report about the meta-goal, or about a specific artifact?"**

- If artifact → reframe: what does this artifact tell us about the meta-goal?
- If meta-goal → proceed

**Q3: "Would the user need me to tell them about this artifact, or do they already have it?"**

If the user can see the artifact themselves (file on disk, test output, git diff), then reporting its contents to them is receipt-checking. Report what the artifact means for the meta-goal instead.

## Examples

| Wrong (artifact-level) | Right (meta-level) |
|---|---|
| "File X still needs turns 1-5 annotated" | "The loop still fails to produce holistic synthesis — individual artifacts confirm the skill needs a different forcing structure" |
| "The test passed with output Y" | "The process now handles case Z correctly, but case W is unproven" |
| "I edited the config and committed" | "The config change addresses the routing failure; the process hasn't been re-validated yet" |

## When NOT to Report Artifacts

Do not report artifact status unless the user explicitly asks about a specific artifact. Listing artifact blockers, partial completion states, or file-level progress to a user who assigned a process-level task is **audience confusion** — you are reporting at the wrong level of abstraction.

If you catch yourself listing files, line counts, or completion percentages → you have drifted. Reconnect to the meta-goal.
