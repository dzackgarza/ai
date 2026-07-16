---
name: agent-memory
description: "Use when deciding what belongs in agent memory, plan records, the central vault, GitHub, or wiki; defining memory policy; or converting historical notes into reusable operational rules."
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

- Corrections that should change future agent behavior

- Decisions whose rationale should be available to future agents

- In-progress work that may be resumed later

### When to Check Memories

Check memories when starting related work:

- Before investigating a problem area

- When working on a feature you’ve touched before

- When resuming work after a conversation break

## Agent Memory Setup and Usage

`agent-memory` is the only agent-facing interface for durable memories and
project planning state. Agents do not need to know or call the storage backend
during normal project work.

### Central Vault Policy

The configured vault is the only durable agent-facing store for memory and plan state.
Do not create loose repo-local Markdown plans, correction logs, decision ledgers, or
agent-facing doctrine files as substitutes for typed `agent-memory` records.

Use repo-local files only as temporary scratchpads while working through in-the-weeds
investigation. Before handoff, delete the scratchpad or promote its durable content:

- reusable agent behavior, corrections, traps, and decisions -> typed memories;
- plans, phase state, queues, and residue ledgers -> `plan` records;
- durable product/project doctrine, architecture rationale, and readable roadmap/proof
  projections -> wiki;
- active public user stories, roadmap nodes, feature contracts, proof burdens,
  execution state, bugs, gaps, and handoff contracts -> GitHub issue trees,
  milestones, or PR claim maps.

If the same fact appears in multiple surfaces, choose one authoritative owner and replace
other copies with links or delete them. Memory can point at GitHub or wiki artifacts, but
it should not duplicate their live status.

The project binding is `.agent-memory.toml` at the repository root. Memory files
live in the configured vault and are managed by `agent-memory`; do not create,
inspect, edit, or reorganize memory directories by hand.

### Tool Availability

Use the GitHub `uvx` runner as the canonical no-install invocation:

```bash
uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory --help
uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory doctor
```

Use a bare `agent-memory` command only after a verified setup has placed it on `PATH`.
If the `uvx` runner exits before showing help because a required runtime dependency is
missing, treat that as a setup failure. Do not bypass the doctor gate and do not call
`iwe` directly for normal memory work.

To provision persistent runtime dependencies, use the checkout:

```bash
cd /home/dzack/gitclones/agent-memory
just install
```

### First-time Setup

Initialize the global vault once:

```bash
uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory maintain init-global --vault /path/to/vault
```

Bind a repository to that vault:

```bash
uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory init project --vault /path/to/vault
uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory doctor
```

### Creating and Managing Memories

Prefer the wrapper commands for normal work. Examples below use the short command for readability after tool availability has been verified; otherwise use the full `uvx` runner prefix above:

```bash
agent-memory search "search term"
agent-memory add --scope project --type decision --title "Memory Title" --content "..."
agent-memory retrieve projects/<project-id>/decisions/<key>
agent-memory update <key> --title "New Title"
agent-memory delete <key>
agent-memory inspect --help
```

Use the `uvx` runner with `--help`, or a verified installed `agent-memory` command,
to discover the current command surface before relying on old examples.

## Memory Interaction Workflow

1. **Search first** — Before writing a new memory, search existing memories with
   `agent-memory search`

2. **Prefer update** — If relevant memory exists, update it with
   `agent-memory update` instead of creating a duplicate

3. **Never refactor or remove behind the tool** — Do not attempt to refactor,
   reorganize, or remove existing memory content outside `agent-memory`

4. **Create via `agent-memory add`** — If no relevant memory exists, create a new
   typed entry through the wrapper

## Where Information Lives

| Information | Location | Example |
| --- | --- | --- |
| Reusable operational rules, traps, and corrections | Typed memories in the vault | “Avoid unescaped `%` in crontab; build time strings in recipe/script” |
| Decisions with future agent relevance | Typed memories in the vault | “Treat generated AGENTS output as derived; edit fragments instead” |
| Plans, phase state, contracts, queues, and residue ledgers | `agent-memory` plan records in the vault | “Current phase is extraction; active residue is parser boundary proof” |
| Durable project doctrine, architecture rationale, and readable roadmap/proof projections | GitHub wiki | Feature page linked to stories, proof burdens, issues, and roadmap projections |
| Active public stories, roadmap nodes, proof burdens, execution state, bugs, gaps, handoffs, and TODOs | GitHub issue trees, milestones, and PR claim maps | Story issue with proof obligations; draft PR linked to milestone and claim set |

Completed work belongs in commits.
Lessons, corrections, decisions, and planning state needed for future work belong in the
vault. TODOs and gaps belong in GitHub issues, not repo artifacts.

## Decision Test

Before writing a memory entry, answer all four:

1. **Will a future agent execute better with this?** If no → do not store.

2. **Is it persistent/derived from stable system properties?** If no → do not store.
   ("Session" here means a single agent invocation; stable means the info holds across
   invocations, not that it never changes.)

3. **Did you have to look it up, search docs, search the web, or arrive at through trial
   and error?** If no → likely already known or obvious.
   If yes → good candidate to record.

4. **Is it primarily “what changed” (changelog)?** If yes → commit message, not memory.

All four must pass. If any fails, the entry does not belong in memory.

## Promotion Test

After deciding that a memory is warranted, decide whether memory alone is sufficient.
Also update GitHub or the wiki when the correction or decision affects:

- public project direction, requirements, user stories, roadmaps, or proof burdens;
- work that multiple agents, branches, repos, or future PRs must coordinate;
- observed bugs, inefficiencies, false greens, or follow-up gaps in an owned repo;
- handoff state that should be auditable without reading the private vault.

Use memory for the reusable lesson and GitHub/wiki for the public project state.
Do not use memory to hide actionable repo work from the owning repo's issue tracker.

## Entry Format

Memories are stored as typed Markdown records managed by `agent-memory`.

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

- **Changelogs** — “2026-02-26 Session Findings”, “what we did today”

- **Decision logs** — “PR #123 decided to rename module” (belongs in commit)

- **Timelines** — “Spent 2h debugging issue X”

- **Git history duplicates** — “Commit abc changed parser logic”

- **Contentless summaries** — Accomplishments without reusable guidance

## Related Design Notes

- `references/opencode-memory-design-notes.md` records durable design ideas salvaged
  from older Claude-local assistant and hook systems.
  Use it when designing or reviewing OpenCode memory/todo tooling; do not reintroduce
  the retired hook/session implementations.

## Transforming Notes into Memory

### Guidelines

- **Write for resumption:** Memories exist to resume work later.
  Capture all key points needed to continue without losing context — decisions made,
  reasons why, current state, and next steps.

- **Write self-contained notes:** Include full context so the reader needs no prior
  knowledge to understand and act on the content

- **Keep summaries decisive:** Reading the summary should tell you if you need the
  details

- **Be practical:** Save what’s actually useful, not everything

### Pattern

Strip the timeline. Extract the trigger condition.
Write the rule. Add how to verify it worked.

| Narrative (wrong) | Policy (correct) |
| --- | --- |
| “On Feb 25 we changed parser behavior and tried many fixes.” | “If stdout has no JSON and stderr contains rate-limit marker, classify as RATE_LIMIT and send ntfy error notification.” |
| “We edited cron commands several times.” | “Avoid `%` date formatting directly in crontab commands; place time construction in recipe/script.” |
| “Spent 2h debugging the auth token refresh.” | “Auth tokens expire after 3600s. Refresh proactively at 3000s, not on 401 response.” |
| “The test suite was flaky on CI.” | “Rate limiter tests require Redis mock on CI. Real Redis connections cause intermittent timeouts.” |

## Quality Bar Examples

| Candidate | Verdict | Why |
| --- | --- | --- |
| “Commit abc changed parser logic” | Reject | Git tracks this |
| “If API returns rate-limit in stderr with no JSON, classify as RATE_LIMIT” | Accept | Reusable failure-handling rule |
| “Spent 2h debugging issue X” | Reject | Timeline, not policy |
| “Topic mismatch is common; verify exact topic string before concluding delivery failure” | Accept | Reusable verification guardrail |
| “PR #123 decided to rename module” | Reject | Decision log, belongs in commit |
