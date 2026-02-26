---
name: agent-memory
description: Use when deciding what belongs in agent memory, defining memory policy, explaining memory purpose versus git history/changelogs/audit trails, or converting historical notes into reusable operational rules
---

# Agent Memory

Memory is persistent execution context for future runs.
It exists to improve future agent behavior, not to duplicate repository history.

## Hard Boundary

Memory is **not**:
- an audit trail
- a decision log
- a changelog
- a summary of work performed

Those belong in git history, diffs, commits, and PRs.

Memory **is** for:
- reusable operational constraints
- stable environment quirks that affect execution
- runbook-like guidance that prevents repeat mistakes
- cross-session context needed to execute correctly

## The Three Buckets (Where Information Lives)

| Information type | Correct location |
|-----------------|-----------------|
| What changed and why | Git commit message body |
| Learned lessons, corrected workflows, calibration, common mistakes | Memory files |
| Outstanding gaps, current bugs, future directions | Repo artifacts (e.g. LEDGER.md) |

**Repo artifacts track current state + future work only.** Completed work, session findings, and historical summaries must never appear in repo documentation. They belong in commit messages (details) and memory (lessons).

**Common violation:** adding a "2026-02-26 Session Findings" section to a ledger file. That is a changelog entry disguised as documentation. The fix: details go in the commit message; lessons go in memory; any *still-unresolved* issues become new ledger entries.

## Decision Test (Memory vs Git)

Use this test before writing memory:

1. Is this primarily "what changed"?  
   If yes, keep it in git artifacts, not memory.
2. Will a future agent execute better with this information?  
   If no, do not store it.
3. Is the information stable and reusable across sessions?  
   If no, do not store it.
4. Is it already obvious from repo files/docs?  
   If yes, link or rely on repo; do not duplicate.

## What to Store

Good memory content:
- Trigger: when this guidance applies
- Rule: what to do
- Constraint: non-obvious limits/failure modes
- Action: exact command/pattern when applicable
- Verification: how to tell if it worked

Bad memory content:
- chronological timeline of events
- narrative progress updates
- broad retrospective summaries
- commit-like change logs

## Rewrite Pattern

Convert historical notes into reusable policy:

- Bad: "On Feb 25 we changed parser behavior and tried many fixes."
- Good: "If stdout has no JSON and stderr contains API rate-limit marker, classify as RATE_LIMIT and send ntfy error notification."

- Bad: "We edited cron commands several times."
- Good: "Avoid `%` date formatting directly in crontab commands; place time construction in recipe/script."

## Entry Format

Use this compact format for memory entries:

```markdown
# <memory-name>
- Trigger: <condition>
- Rule: <required behavior>
- Command/Pattern: <exact command or snippet>
- Verify: <observable success condition>
- Scope: <project|user|environment>
```

## Source Grounding

When discussing why this policy exists, cite `references/source-notes.md`.
For practical classification examples and transformations, use `references/memory-rubric.md`.

