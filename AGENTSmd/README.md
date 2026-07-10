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
  - purpose-remediation
  - purpose-procedure
  - stability-model-contingent
---
```

`title` supplies the rendered heading, and `order` is the integer sibling sort key.
The `tags` list classifies a fragment on two independent, multi-label axes:

- Purpose: `purpose-context` supplies facts or definitions the agent would not otherwise
  have; `purpose-preference` records local style or tool choices; `purpose-policy` states
  required invariants; `purpose-procedure` prescribes a workflow or decision gate;
  `purpose-reference` routes to skills, tools, commands, or other canonical material;
  `purpose-remediation` counters recurring agent mistakes or misaligned priors; and
  `purpose-structure` marks heading-only fragments.
- Stability: `stability-model-independent` marks information that even an arbitrarily
  capable agent still needs explicitly because it comes from the user, domain, local
  environment, or chosen system policy. `stability-model-contingent` marks prompting that
  exists to compensate for current model limitations, misaligned priors, or recurring
  failure modes and may become unnecessary as models improve.
  `stability-policy-contingent` depends on current local workflow doctrine;
  `stability-tool-contingent` depends on named tools, commands, or APIs;
  `stability-environment-contingent` depends on current machine or repository facts; and
  `stability-corpus-contingent` depends only on the fragment tree's organization.

`stability-model-independent` does not mean “philosophically true forever.” It means the
information still has to be communicated to a more capable model. A preferred tool can be
model-independent while remaining tool-contingent. Conversely, “not found” does not imply
“does not exist” is a true epistemic principle, but an explicit reminder of that principle
is model-contingent when it exists to remediate bounded searches and weak inference.

### How to classify fragments

- Read the complete fragment and compare it with related fragments before assigning tags.
  Never classify from its title, frontmatter, filename, a snippet, or a worker summary.
- First run the AGI counterfactual: would an arbitrarily capable agent still need this
  supplied explicitly? User intent, domain conventions, local paths, tool preferences,
  and chosen ownership boundaries are model-independent. Reminders about object
  permanence, theory of mind, bounded search, goal preservation, or predictable reasoning
  failures are model-contingent.
- Then assign every purpose tag represented by the fragment's complete content.
- Tags apply to the whole fragment and are intentionally non-exclusive. A fragment mixing
  owner context with model remediation carries both model-independent and model-contingent
  tags. If those parts later need independent inclusion or exclusion, split the fragment
  rather than pretending the metadata is sentence-level.

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
