---
name: agent-memory
description: "Use when deciding what belongs in agent memory, defining memory policy, or converting historical notes into reusable operational rules."
---
# Agent Memory

## Requirements

Every memory entry must satisfy ALL of:

- **Actionable** — contains a concrete behavior, command, or decision rule
- **Durable** — likely useful in future sessions (not session-specific)
- **Non-duplicative** — not already covered by git history, system context, or common
  SOTA agent knowledge
- **Specific** — includes clear trigger and verification, not vague guidance
- **Makes a future agent faster, more correct, or less likely to repeat a mistake**

### When to Save Memories

**Save immediately** when any of these occur:

- You make an incorrect choice or misstep
- You are surprised by anything
- New information contradicts your priors
- Functionality is uncovered through investigation
- A solution required new insight or research
- You discover something worth preserving that took effort to find

Save memories when you discover something worth preserving:

- Research findings that took effort to uncover
- Non-obvious patterns or gotchas in the codebase
- Solutions to tricky problems
- Architectural decisions and their rationale
- In-progress work that may be resumed later

### When to Check Memories

Check memories when starting related work:

- Before investigating a problem area
- When working on a feature you've touched before
- When resuming work after a conversation break

## iWe Setup and Usage

Memories are managed through `iwe`, a file-based knowledge graph for Markdown notes.
Each project contains a `.agents/memories/config.toml` after `iwe init`. The actual
`.md` files are stored in iwe's internal graph — use `iwe find`, `iwe retrieve`, and
`iwe tree` to inspect them, never raw file reads.

### First-time setup in a project

```bash
# Initialize the memory store in the project
iwe init
```

### Creating and managing memories

```bash
# Create a new memory (accepts content via stdin or editor)
iwe new "Memory Title"

# Search across all memories (fuzzy text + YAML field filters)
iwe find "search term"

# Retrieve a memory with surrounding context
iwe retrieve -k my-memory

# Overwrite a memory body
iwe update -k memory-key -c "new content"

# Update frontmatter fields
iwe update --filter 'status: draft' --set reviewed=true

# Rename a memory (all links update automatically)
iwe rename old-key new-key

# Delete a single memory (references cleaned up)
iwe delete memory-key

# Extract a section into its own memory
iwe extract memory-key --section "Title"

# Inline a referenced memory back into its parent
iwe inline memory-key --reference "other-memory"

# Attach a memory via a configured action (e.g., daily notes)
iwe attach --to today -k memory-key
```

### Browsing and inspecting

```bash
# View the hierarchy tree from any starting point
iwe tree

# Count memories matching criteria
iwe count --filter 'status: draft'

# Analyze the memory store
iwe stats

# Export the memory graph as DOT for visualization
iwe export -f dot

# Normalize all memories to consistent formatting
iwe normalize
```

Use `iwe --help` and `iwe <subcommand> --help` to discover the full set of commands and
options.

## Memory Interaction Workflow

1. **`iwe find` first** — Before writing a new memory, search existing memories
2. **Prefer `iwe update`** — If relevant memory exists, update it with
   `iwe update -k key -c "content"` instead of creating a duplicate
3. **Never refactor or remove** — Do not attempt to refactor, reorganize, or remove
   existing memory content outside of iwe
4. **Create via `iwe new`** — If no relevant memory exists, create a new entry via
   `iwe new "Title"`

## Where Information Lives

| Information | Location | Example |
| --- | --- | --- |
| Reusable operational rules | Memory files | "Avoid unescaped `%` in crontab; build time strings in recipe/script" |
| High-level decisions with future relevance | Memory files | "Chose process constraint over declarative rules because..." |
| Current gaps, TODOs | GitHub issues | Issue tagged `TODO` or `needs-investigation` |

Completed work belongs in commits.
Lessons and decisions needed for future work belong in memory.
TODOs and gaps belong in GitHub issues, not repo artifacts.

## Decision Test

Before writing a memory entry, answer all four:

1. **Will a future agent execute better with this?** If no → do not store.
2. **Is it persistent/derived from stable system properties?** If no → do not store.
   ("Session" here means a single agent invocation; stable means the info holds across
   invocations, not that it never changes.)
3. **Did you have to look it up, search docs, search the web, or arrive at through trial
   and error?** If no → likely already known or obvious.
   If yes → good candidate to record.
4. **Is it primarily "what changed" (changelog)?** If yes → commit message, not memory.

All four must pass. If any fails, the entry does not belong in memory.

## Entry Format

Memories are stored as Markdown files with YAML frontmatter.
The frontmatter `title` is used as the canonical identifier.
Tags are used for filtering via `iwe find --filter`.

```yaml
---
title: Memory Title
status: active            # Optional: active, draft, reviewed, archived
tags: [tag1, tag2]
---
```

Memory entries should answer these questions:

1. **What is this?** — A clear, descriptive title or name
2. **When does this apply?** — The trigger condition or context
3. **What should be done?** — The actionable guidance
4. **How do you verify it worked?** — Observable success condition

Include any of these that are relevant:

- Command/Pattern: Exact command or code snippet
- Context: Goal, background, constraints
- Details: Key files, related symbols, code snippets
- Next steps: What to do next, open questions

Write summaries that answer: What is this memory about?
What is the key problem or topic?
Why does it matter?

## Use Cases

### Personal Wiki

- Store code snippets and patterns
- Document project decisions
- Keep reference material

### Learning Log

- Record things you learn
- Tag by topic for later retrieval
- Build knowledge over time

### Project Context

- Save project-specific knowledge
- Retrieve relevant context at session start
- Share knowledge across sessions

### Best Practices

- Use meaningful titles — they become searchable anchors
- Add tags — improves search and organization
- Use markdown — full support in content
- Search before writing — check if knowledge already exists
- Keep notes focused — one topic per note
- Update additively — prefer adding new entries over modifying existing ones

## Things to Avoid in Memories

- **Changelogs** — "2026-02-26 Session Findings", "what we did today"
- **Decision logs** — "PR #123 decided to rename module" (belongs in commit)
- **Timelines** — "Spent 2h debugging issue X"
- **Git history duplicates** — "Commit abc changed parser logic"
- **Contentless summaries** — Accomplishments without reusable guidance

## Related Design Notes

- `references/opencode-memory-design-notes.md` records durable design ideas
  salvaged from older Claude-local assistant and hook systems. Use it when
  designing or reviewing OpenCode memory/todo tooling; do not reintroduce the
  retired hook/session implementations.

## Transforming Notes into Memory

### Guidelines

- **Write for resumption:** Memories exist to resume work later.
  Capture all key points needed to continue without losing context — decisions made,
  reasons why, current state, and next steps.
- **Write self-contained notes:** Include full context so the reader needs no prior
  knowledge to understand and act on the content
- **Keep summaries decisive:** Reading the summary should tell you if you need the
  details
- **Be practical:** Save what's actually useful, not everything

### Pattern

Strip the timeline. Extract the trigger condition.
Write the rule. Add how to verify it worked.

| Narrative (wrong) | Policy (correct) |
| --- | --- |
| "On Feb 25 we changed parser behavior and tried many fixes." | "If stdout has no JSON and stderr contains rate-limit marker, classify as RATE_LIMIT and send ntfy error notification." |
| "We edited cron commands several times." | "Avoid `%` date formatting directly in crontab commands; place time construction in recipe/script." |
| "Spent 2h debugging the auth token refresh." | "Auth tokens expire after 3600s. Refresh proactively at 3000s, not on 401 response." |
| "The test suite was flaky on CI." | "Rate limiter tests require Redis mock on CI. Real Redis connections cause intermittent timeouts." |

## Quality Bar Examples

| Candidate | Verdict | Why |
| --- | --- | --- |
| "Commit abc changed parser logic" | Reject | Git tracks this |
| "If API returns rate-limit in stderr with no JSON, classify as RATE_LIMIT" | Accept | Reusable failure-handling rule |
| "Spent 2h debugging issue X" | Reject | Timeline, not policy |
| "Topic mismatch is common; verify exact topic string before concluding delivery failure" | Accept | Reusable verification guardrail |
| "PR #123 decided to rename module" | Reject | Decision log, belongs in commit |
