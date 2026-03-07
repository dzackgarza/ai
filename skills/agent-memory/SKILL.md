---
name: agent-memory
description: "Use when deciding what belongs in agent memory, defining memory policy, or converting historical notes into reusable operational rules."
---

# Agent Memory

Memory is persistent execution context that improves future agent behavior. Every entry must make a future agent faster, more correct, or less likely to repeat a mistake.

## Where Information Lives

| Information | Location | Example |
|-------------|----------|---------|
| What changed, why, tradeoffs | Git commit message body | "Chose process constraint over declarative rules because post-mortem proved..." |
| Reusable operational rules | Memory files | "Avoid unescaped `%` in crontab; build time strings in recipe/script" |
| Current state, outstanding gaps | Repo artifacts (LEDGER.md) | "TODO: rate-limit headers still unverified" |

Completed work belongs in commits. Lessons belong in memory. Current state belongs in repo artifacts. Never cross these boundaries.

**Common violation:** Adding "2026-02-26 Session Findings" to a ledger file. That is a changelog disguised as documentation. Fix: details → commit message; lessons → memory; unresolved issues → new ledger entries.

## Decision Test

Before writing a memory entry, answer all four:

1. **Will a future agent execute better with this?** If no → do not store.
2. **Is it stable across sessions?** If no → do not store.
3. **Is it already obvious from repo files?** If yes → do not duplicate.
4. **Is it primarily "what changed"?** If yes → commit message, not memory.

All four must pass. If any fails, the entry does not belong in memory.

## Entry Format

Every memory entry uses this structure:

```markdown
# <descriptive-kebab-name>
- Trigger: <when this guidance applies>
- Rule: <what to do>
- Command/Pattern: <exact command or code snippet, if applicable>
- Verify: <observable success condition>
- Scope: <project | user | environment>
```

**Each field is mandatory.** Entries without a trigger are unfindable. Entries without verification are unenforceable.

## Transforming Notes into Memory

Agents default to writing narrative. Memory requires policy. Convert timeline into trigger-rule-verify:

| Narrative (wrong) | Policy (correct) |
|-------------------|-----------------|
| "On Feb 25 we changed parser behavior and tried many fixes." | "If stdout has no JSON and stderr contains rate-limit marker, classify as RATE_LIMIT and send ntfy error notification." |
| "We edited cron commands several times." | "Avoid `%` date formatting directly in crontab commands; place time construction in recipe/script." |
| "Spent 2h debugging the auth token refresh." | "Auth tokens expire after 3600s. Refresh proactively at 3000s, not on 401 response." |
| "The test suite was flaky on CI." | "Rate limiter tests require Redis mock on CI. Real Redis connections cause intermittent timeouts." |

**The pattern:** Strip the timeline. Extract the trigger condition. Write the rule. Add how to verify it worked.

## Memory File Organization

### MEMORY.md (always loaded into context)

- Maximum 200 lines — every line costs attention budget.
- Contains the highest-signal entries and links to topic files.
- Organize by topic, not chronology. No dates in headers.

### Topic files (loaded on demand)

- Create when a topic accumulates 3+ related entries.
- Name descriptively: `cron-quirks.md`, `api-rate-limits.md`, `ci-flakiness.md`.
- Link from MEMORY.md: `See [cron-quirks.md](cron-quirks.md) for details.`

### Sizing rules

| Symptom | Action |
|---------|--------|
| MEMORY.md exceeds 200 lines | Extract topic clusters into separate files, keep summaries + links |
| A topic file exceeds 100 lines | Split further or prune stale entries |
| An entry hasn't been useful in 5+ sessions | Candidate for removal |

## Maintaining Memory

Memory rots just like code. Stale entries mislead future agents.

- **Before writing:** Check if an existing entry covers the topic. Update it instead of creating a duplicate.
- **After discovering an entry is wrong:** Correct or delete it immediately. Wrong memory is worse than no memory.
- **After a workflow changes:** Update affected entries. A rule about a removed tool is noise.
- **When entries contradict observed behavior:** Investigate. Either the entry is stale or the behavior is a bug. Resolve the contradiction — never leave both standing.

## Quality Bar

An entry is acceptable only if all four are true:

- **Actionable** — contains a concrete behavior, command, or decision rule
- **Durable** — likely useful in future sessions (not session-specific)
- **Non-duplicative** — not already covered by git history, repo docs, or another entry
- **Specific** — includes clear trigger and verification, not vague guidance

| Candidate | Verdict | Why |
|-----------|---------|-----|
| "Commit abc changed parser logic" | Reject | Git tracks this |
| "If API returns rate-limit in stderr with no JSON, classify as RATE_LIMIT" | Accept | Reusable failure-handling rule |
| "Spent 2h debugging issue X" | Reject | Timeline, not policy |
| "Topic mismatch is common; verify exact topic string before concluding delivery failure" | Accept | Reusable verification guardrail |
| "PR #123 decided to rename module" | Reject | Decision log, belongs in commit |

## Reference

- `references/source-notes.md` — Research grounding for this policy (Reflexion, Voyager, MemGPT, Anthropic, OpenAI)
- `references/memory-rubric.md` — Keep/drop matrix and transformation examples
