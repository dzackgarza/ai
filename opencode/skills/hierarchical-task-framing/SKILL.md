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

## Synthesis Gate

Before reporting progress or completing a sub-task, produce this statement:

**"The user's overall task is _____, and what I just did moves it forward because _____."**

If you cannot complete the second blank — if you can only describe the artifact you touched, not its relationship to the meta-goal — you have drifted. Reconnect before writing anything.

If you catch yourself listing files, line counts, or completion percentages, you are reporting evidence (artifacts) as if they were deliverables (process outcomes). The user assigned a process-level task. Report on the process.
