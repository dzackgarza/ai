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
  - role-remediation
  - stability-model-contingent
---
```

`title` supplies the rendered heading, and `order` is the integer sibling sort key.
The optional `tags` list classifies a fragment on two independent axes:

- Role: `role-context` communicates project or machine facts an agent cannot infer;
  `role-preference` communicates durable local style, tool, or ownership choices;
  `role-remediation` communicates guardrails or workflows introduced in response to
  observed agent mistakes.
- Stability: `stability-timeless` is independent of current model capability;
  `stability-model-contingent` may become unnecessary as models improve.

A fragment may carry multiple role tags, but at most one stability tag.
Classification is incremental: an untagged fragment remains included and is reported as
untagged rather than being forced into an ambiguous category.
The allowed taxonomy and active exclusions live in `.agents/build.toml`.
Adding a tag to `selection.exclude_tags` omits matching fragment bodies.
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
