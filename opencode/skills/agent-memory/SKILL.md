---
name: agent-memory
description: "Use when deciding what belongs in agent memory, preserving significant experiences or reflections, managing plan records and the central vault, defining memory policy, or converting historical material without erasing its evidential value."
---
# Agent Memory

## What Memory Is

Memory is the durable substrate of experience and continuing interpretation, not a
technical ledger of instructions for a future agent.

A valuable memory may preserve:

- an episode: what happened, in what context, and in what sequence;
- consequences and salience: what failed, what changed, and why it mattered;
- causal cues visible at the time;
- contemporaneous reflections, hypotheses, and counterfactuals, labeled as such;
- later reinterpretations that supplement rather than rewrite the original episode;
- stable facts, decisions, or working guidance when those really are known.

Do not assume that an incident yields a complete prevention rule. One episode can suggest
causes or interventions without establishing them. A proposed lesson such as “avoid X next
time” is a time-localized hypothesis, not proof that X caused the incident or that the
intervention prevents the whole failure class.

Keep these layers distinguishable when each carries durable value:

1. **Experience/evidence** — what occurred and the observable sequence.
2. **Reflection/interpretation** — what seemed causally important, including uncertainty
   and alternative explanations.
3. **Policy/intervention** — a proposed future action, explicitly provisional until
   experience supports it.

A policy may link to a memory, but it must not replace the experience that made the policy
seem plausible. If the policy later fails, the preserved episode must still support a new
interpretation.

## Requirements

Every memory entry must be:

- **Durable** — likely useful in future sessions, whether for recognition,
  reconsideration, resumption, or action.
- **Non-duplicative** — not merely a copy of git history, public execution state, or an
  existing memory.
- **Specific** — preserves the concrete facts, context, sequence, causal cues, or decision
  needed to understand it later.
- **Epistemically labeled** — distinguishes observation, contemporaneous interpretation,
  later analysis, and proposed intervention where they differ.
- **Revisable** — later understanding can supplement or challenge the interpretation
  without rewriting the original experience to make the new theory look inevitable.

A memory does **not** need to contain a command, decision rule, remediation, or observable
success condition. Requiring actionability would systematically discard experiences whose
future value is recognition and reinterpretation.

### When to Save Memories

Preserve an experience while its sequence, consequences, causal cues, and
contemporaneous reflections are still available when:

- a surprising or consequential failure occurred;
- several corrections revealed a pattern that cannot be understood from the final rule
  alone;
- the cause remains uncertain or several explanations remain plausible;
- a proposed remedy has not been validated;
- future recognition of a similar situation may matter even if no instruction is known;
- later reinterpretation would require details that a compressed lesson would erase.

Also preserve stable findings, decisions, rationale, environment knowledge, and resumption
context when they outlive the current session.

Do not create a memory merely because a command succeeded or a task finished. Preserve
what a future agent would otherwise be unable to reconstruct from the owning source.

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

- significant experiences, causal sequences, contemporaneous reflections, and unresolved
  interpretations -> `reference` or `context` memories;
- reusable working guidance and proposed interventions -> `advice` or `trap` memories,
  linked to the experience that grounds them when that experience matters;
- stable decisions and rationale -> `decision` memories;
- plans, phase state, queues, and residue ledgers -> [[plan/SKILL|plan]] records;
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
| Significant experiences and their consequences | `reference` or `context` memories | Correction sequence preserving what happened, what seemed causally important, and what remains uncertain |
| Later interpretations and provisional lessons | Linked memories or additive sections in the experience record | “At the time, rushing and missing directions appeared relevant; leaving earlier might help” |
| Reusable operational guidance and proposed interventions | `advice` or `trap` memories | “Avoid unescaped `%` in crontab; build time strings in recipe/script” |
| Decisions with future agent relevance | `decision` memories | “Treat generated AGENTS output as derived; edit fragments instead” |
| Plans, phase state, contracts, queues, and residue ledgers | `agent-memory` plan records | “Current phase is extraction; active residue is parser boundary proof” |
| Durable project doctrine, architecture rationale, and readable roadmap/proof projections | GitHub wiki | Feature page linked to stories, proof burdens, issues, and roadmap projections |
| Active public stories, roadmap nodes, proof burdens, execution state, bugs, gaps, handoffs, and TODOs | GitHub issue trees, milestones, and PR claim maps | Story issue with proof obligations; draft PR linked to milestone and claim set |

Completed work belongs in commits. The experience of doing the work belongs in memory
only when its sequence, consequences, interpretation, or emotional/epistemic salience has
future value beyond the diff. TODOs and gaps belong in GitHub issues, not repo artifacts.

## Decision Test

Before writing a memory, ask:

1. **What would be lost if this fades?** A sequence, consequence, causal cue, reflection,
   stable fact, rationale, or resumption context must be identifiable.
2. **Can the owning source reconstruct it?** If git, an issue, a paper, or current docs
   already preserve the same meaning, link or rely on that source instead of duplicating
   it.
3. **Does the value depend on the episode, not only a rule?** If later reinterpretation
   would need what happened and in what order, preserve the experience before extracting
   advice.
4. **What is known versus suspected?** Label direct observation, contemporary inference,
   later analysis, and proposed intervention separately.
5. **Is this live execution state?** TODOs and public work status belong in GitHub; plans
   belong in plan records; neither should be disguised as memory.

A memory is warranted when future recognition or understanding would materially degrade
without it. It need not prescribe what the future agent should do.

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

Memory entries should make their own epistemic role clear. Depending on the record, include:

- **Experience:** what happened, context, sequence, consequences, and salient details.
- **Reflection:** what seemed important at the time and why.
- **Later analysis:** revised interpretations, alternative explanations, and evidence
  boundaries.
- **Proposed intervention:** what might help, with uncertainty and validation status.
- **Stable fact or decision:** the fact, source, rationale, and scope.
- **Resumption state:** what a future session needs to continue.

Do not force every memory to contain all of these. In particular, do not invent an action
or verification test for an experience whose durable value is recognition and
reinterpretation.

Write titles and summaries that tell a future agent whether the record is an episode,
reflection, hypothesis, decision, reference, or working rule.

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

- **Git-history duplication** — a bare list of commits or file changes with no experience,
  consequence, or interpretation beyond what git preserves.
- **Status mirrors** — live TODOs, current issue state, or manually copied project status.
- **Contentless summaries** — accomplishments without salient detail or future
  interpretive value.
- **Premature normative compression** — replacing a consequential episode with only the
  rule currently believed to prevent recurrence.
- **Retrospective certainty** — rewriting tentative contemporary impressions as if the
  final causal account was known during the event.
- **Universal prevention claims from one incident** — preserve likely contributing
  factors and possible counterfactuals without claiming complete control of the failure
  class.

Chronology is not automatically noise. Preserve sequence when cause and effect,
correction assimilation, escalation, or changing interpretation depends on it. Omit dates
and step-by-step narration only when they add no meaning beyond the owning source.

## Related Design Notes

- `references/opencode-memory-design-notes.md` records durable design ideas salvaged
  from older Claude-local assistant and hook systems.
  Use it when designing or reviewing [[opencode/SKILL|OpenCode]] memory/todo tooling; do not reintroduce
  the retired hook/session implementations.

## Transforming Historical Material into Memory

### Preserve before interpreting

When the value lies in an incident or experience, preserve enough of the episode to make
future reinterpretation possible:

- the context and sequence;
- observed consequences;
- causal cues noticed at the time;
- contemporaneous reactions or lessons;
- later analysis and alternative explanations;
- what remains unknown;
- proposed interventions, clearly separated from the memory itself.

Do not rewrite the episode into a morality tale that makes the current policy look
inevitable. Add later interpretations rather than silently replacing earlier ones.

When the source is merely noisy documentation of a stable technical fact, concise
extraction remains appropriate. The distinction is whether compression would remove
causal or experiential information needed to understand future similarities.

### Examples

| Source material | Durable form |
| --- | --- |
| A crash preceded by phone use, speeding, a missed light, rushing, and absent directions | Preserve the episode and consequences; note that distraction, speed, and rushing seemed relevant; record “leave earlier / avoid phone use” only as provisional counterfactuals |
| A correction sequence where each objection caused more schema machinery | Preserve the sequence and the consequences of each assimilation; link any proposed frame-reset rule as a separate hypothesis |
| API stderr has a documented rate-limit marker and no JSON | Stable technical fact: classify that response as `RATE_LIMIT`, with the source and exact boundary |
| Several cron edits revealed `%` expansion semantics | Stable technical lesson plus the observed failure if it would help recognize related quoting problems |
| “Spent two hours debugging” with no consequential sequence or insight | Omit the duration; preserve only the facts, surprises, or interpretations that matter |

### Epistemic continuity test

Before saving, ask:

> If the proposed lesson proves wrong, does this memory still contain enough experience
> and analysis to understand the incident and formulate a different lesson?

If no, the record has been compressed too far.
