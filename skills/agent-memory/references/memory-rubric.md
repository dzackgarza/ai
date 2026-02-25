# Memory Rubric

Use this rubric to decide if something belongs in memory.

## Keep / Drop Matrix

| Candidate note | Keep in memory? | Why |
|---|---|---|
| "Commit abc changed parser logic" | No | Git already tracks this exactly |
| "Cron treats unescaped % specially; keep prompt-time construction in recipe/script" | Yes | Durable operational constraint |
| "Spent 2h debugging issue X" | No | Timeline/audit content |
| "If API returns rate-limit marker in stderr with no JSON, classify as RATE_LIMIT and notify" | Yes | Reusable failure-handling rule |
| "PR #123 decided to rename module" | No | Decision/changelog content |
| "Topic mismatch is common; verify exact topic string before concluding delivery failure" | Yes | Reusable verification guardrail |

## Transformation Rules

Convert this kind of note:
- Timeline form: "we tried A then B then C"

Into this form:
- Trigger: when does this happen?
- Rule: what to do next time?
- Verify: what observable confirms success?

## Quality Bar

A memory entry is acceptable only if all are true:
- Actionable: contains a concrete behavior or command
- Durable: likely useful in future sessions
- Non-duplicative: not already covered by git/docs
- Specific: includes clear trigger and verification

## Example Entry

```markdown
# cron-percent-handling
- Trigger: editing cron command strings that include date formatting
- Rule: avoid unescaped '%' in crontab command body; build time strings in justfile/script
- Command/Pattern: run recipe wrapper instead of inline date formatting in cron entry
- Verify: `crontab -n` succeeds and scheduled command runs intact
- Scope: project
```

