# AGENTSmd — the AGENTS.md module

This directory is the **source of truth** for the agent context file. The repo-root
`AGENTS.md` is a symlink to `AGENTSmd/.agents/AGENTS.md.generated`, which is compiled from
the markdown fragments in this tree.

The content tree holds **only fragments**. All tooling — the build script, the justfile,
the pandoc filter, and the generated artifact — lives under `.agents/`.

> **Never edit `AGENTS.md` (or `.agents/AGENTS.md.generated`) directly.** It is a build
> artifact and will be overwritten. Edit the fragments here and regenerate.

## Editing and regenerating

1. Edit, add, move, or delete fragment files in this tree (standard markdown, any IDE).
2. Regenerate:

   ```bash
   just -f AGENTSmd/.agents/justfile assemble
   ```

3. Optionally reflow the source fragments with semantic line breaks:

   ```bash
   just -f AGENTSmd/.agents/justfile format
   ```

## How the tree maps to the output

The **filesystem tree is the structure** — there is no separate manifest, and you never
write heading levels by hand.

- A **directory is a section.** Its `index.md` supplies the section's title (from
  frontmatter) and its body. Nesting depth determines the heading level automatically.
- A **non-`index.md` file is a subsection** of its directory.
- The **root `index.md`** is the preamble: it has no heading and is emitted first.
- **Ordering** among siblings comes from the `order` frontmatter key, not filename sort.

### Fragment frontmatter

Every fragment and every `index.md` (except the root preamble) must declare:

```yaml
---
title: Hard Rules
order: 30
tags:
  - source-system-contract
  - source-observed-model-failure
  - function-constrain
  - failure-tool-bypass
  - retest-model-alignment
  - retest-policy-change
---
```

`title` supplies the rendered heading, and `order` is the integer sibling sort key.
The `tags` list uses four independent, multi-label axes:

- Source records why the fragment exists. `source-owner-context` and
  `source-domain-context` supply otherwise unavailable facts; `source-owner-preference`
  records a chosen style or tool preference; `source-system-contract` records local
  architecture, ownership, or policy; `source-observed-model-failure` marks reflexive
  guidance authored in response to model behavior; and `source-document-structure` marks
  organization-only fragments.
- Function records what the fragment does: `function-orient`, `function-define`,
  `function-constrain`, `function-procedure`, `function-route`, `function-allocate`,
  `function-evaluate`, or `function-structure`.
- Failure records the behavior targeted by reflexive guidance:
  `failure-intent-assumption`, `failure-correction-thrashing`,
  `failure-reporting-distortion`, `failure-completion-laundering`,
  `failure-epistemic-overreach`, `failure-goal-substitution`, `failure-scope-drift`,
  `failure-premature-action`, `failure-proxy-evidence`,
  `failure-destructive-state-change`, `failure-process-overproduction`,
  `failure-tool-bypass`, `failure-proof-gaming`, `failure-state-misplacement`,
  `failure-feedback-laundering`, and `failure-context-loss`.
- Retest records what change would justify reevaluating the fragment:
  `retest-model-reasoning`, `retest-model-theory-of-mind`,
  `retest-model-alignment`, `retest-model-tool-use`,
  `retest-model-self-evaluation`, `retest-model-memory`, `retest-policy-change`,
  `retest-toolchain-change`, `retest-environment-change`, or
  `retest-corpus-change`.

These axes answer different questions. A fragment can encode a real system contract and
still have been authored reflexively because models repeatedly violated that contract.
Likewise, a retest tag is a hypothesis about when to rerun controlled comparisons, not a
claim that the guidance will eventually become unnecessary.

### How to classify fragments

- Read the complete fragment and compare it with related fragments. Never classify from a
  title, filename, frontmatter, snippet, or worker summary.
- Identify causal source before communicative function. Ask why this text was added, not
  merely whether some sentence in it remains true or expresses a local policy.
- Apply `source-observed-model-failure` whenever the fragment is reflexive to observed or
  clearly named model behavior, then name the targeted `failure-*` families. Every
  `failure-*` tag requires `source-observed-model-failure`.
- Add `retest-*` tags for the capability, policy, toolchain, environment, or corpus change
  that could alter the fragment's value. Do not use philosophical truth as a proxy for
  prompt necessity.
- Tags apply to the whole fragment and are intentionally non-exclusive. If independently
  testable concerns are too entangled for useful exclusion, split the fragment rather
  than pretending the metadata is sentence-level.

For example, `corrections.md` is both a system contract and a reflexive response to intent
assumption, correction thrashing, process overproduction, and context loss.
`chat-responses-after-completing-work.md` combines an owner preference with remediation
for reporting distortion, completion laundering, and proxy evidence. Those causal labels
remain even if parts of each fragment encode policies a future model would still need to
know.

### Routing and progressive disclosure

Tags record why guidance exists; they do not make every tagged procedure always active.
Each behavioral fragment and routed skill should make its positive trigger and important
non-triggers explicit.

Route work at the smallest sufficient scale:

| Work shape | Appropriate context |
| --- | --- |
| Direct answer, read-only inspection, classification, or analysis | Relevant sources only |
| Trivial reversible document, metadata, configuration, or data edit | Complete target plus nearby governing context and the smallest verification |
| Substantive implementation dependent on repository state | Task-relevant project discovery, implementation skills, and real-boundary verification |
| Cross-session, multi-agent, public, or review-track work | Project initialization, memory, plans, issues, milestones, PRs, or review procedures as required |

The mere presence of a repository, correction, bug, commit, or system-local tool does not
activate the heaviest corresponding workflow. A procedure should progressively disclose
context only when the requested object depends on that local system contract.
Loading one skill does not recursively activate adjacent skills unless their own triggers
are independently present.

Explicit user scope controls the route when safe: requests described as narrow, trivial,
direct, or outside the standard workflow should remain so. Authorization,
unknown-provenance preservation, secrets, destructive actions, and irreversible external
state remain hard boundaries.

Every current fragment is classified. The allowed taxonomy and active exclusions live in
`.agents/build.toml`. Adding a tag to `selection.exclude_tags` omits every whole fragment
carrying that tag.
If a directory's `index.md` is excluded, the compiler retains its structural heading
when included descendants still need it.

Every build prints one inclusion or exclusion line per discovered fragment, followed by
totals.
Unknown tags, malformed tag lists, invalid config, missing `title`/`order`, malformed
frontmatter, and directories without an `index.md` are hard errors.
Other frontmatter keys remain available for future tooling.

## How it is built

`.agents/assemble.py` (run via `uv`) does only the structure mapping: it reads frontmatter,
sorts siblings, and emits a pandoc outline of synthesized section headings plus `{.include}`
directives. All markdown processing — transclusion, heading-level rebasing, frontmatter
stripping, normalization — is delegated to **pandoc** and the standard
`.agents/filters/include-files.lua` filter (`-M include-auto` shifts each fragment's own
headings to sit under its section). The build is deterministic: same tree in, same output out.
