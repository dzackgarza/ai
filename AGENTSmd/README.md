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
title: Hard Rules        # the rendered section heading
order: 30                # integer; sibling sort key (gaps of 10 leave room)
---
```

Anything else you add to the frontmatter is preserved and ignored by the build — it is
the metadata surface for future tooling. Missing `title`/`order`, malformed YAML, or a
directory without an `index.md` is a hard error: the build fails loudly and names the file.

## How it is built

`.agents/assemble.py` (run via `uv`) does only the structure mapping: it reads frontmatter,
sorts siblings, and emits a pandoc outline of synthesized section headings plus `{.include}`
directives. All markdown processing — transclusion, heading-level rebasing, frontmatter
stripping, normalization — is delegated to **pandoc** and the standard
`.agents/filters/include-files.lua` filter (`-M include-auto` shifts each fragment's own
headings to sit under its section). The build is deterministic: same tree in, same output out.
