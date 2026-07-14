---
name: obsidian
description: Use when working with Obsidian vaults -- reading, listing, searching, creating, or editing notes. Also covers Obsidian Flavored Markdown syntax (wikilinks, embeds, callouts, properties, tags, math, diagrams). For vault content syntax, consult references/.
---
# Obsidian Vault

Filesystem-first Obsidian vault work: reading notes, listing notes, searching note
files, creating notes, appending content, and adding wikilinks.

For mathematical vault stewardship, inbox intake, source-backed semantic parsing,
provenance-sensitive incorporation, or note-taxonomy decisions, load
[[mathematical-obsidian-vault-steward/SKILL|mathematical-obsidian-vault-steward]] as the canonical behavioral policy.

For extracting, transforming, and integrating mathematical knowledge from raw source
material (chat logs, transcripts, handwritten notes, theorem sketches, failed proof
attempts) into durable structured notes, load [[knowledge-extraction/SKILL|knowledge-extraction]]. This skill covers
what to preserve, how to classify claims, how to build dependency graphs and proof-gap
ledgers, and how to reconcile new material with existing vault notes.

This generic Obsidian skill covers vault file mechanics and content syntax.

## Vault path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable,
for example from `~/.hermes/.env`. If it is unset, use `~/Documents/Obsidian Vault`.

File tools do not expand shell variables.
Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`,
`patch`, or `search_files`; resolve the vault path first and pass a concrete absolute
path. Vault paths may contain spaces, which is another reason to prefer file tools over
shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving
`OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists.
Once the path is known, switch back to file tools.

## Read a note

Use `read_file` with the resolved absolute path to the note.
Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path.
Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.

- To list a subfolder, search under that subfolder’s absolute path.

## Search

Use `search_files` for both filename and content searches.
Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.

- For note contents, use `search_files` with `target: "content"`, the content regex as
  `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown
  notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content.
Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and
returns structured results.

For content syntax -- wikilinks, embeds, callouts, properties, tags, math, diagrams,
footnotes -- see `references/obsidian-markdown.md`.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.

- Use `patch` for an anchored append when there is stable context, such as adding a
  section after an existing heading or appending before a known trailing block.

- Use `write_file` when rewriting the whole note is clearer than constructing a fragile
  patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new
content.

For a simple append with no stable context, `terminal` is acceptable if it is the
clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context.
Prefer this over shell text rewriting.

## Writing Obsidian Content

When creating or editing note content, use Obsidian Flavored Markdown syntax.
The canonical source is `references/obsidian-markdown.md`. Individual features are
expanded in:

| Feature | Reference |
| --- | --- |
| Callouts | `references/CALLOUTS.md` |
| Embeds | `references/EMBEDS.md` |
| Properties / Frontmatter | `references/PROPERTIES.md` |

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax.
When creating notes, use these to link related content.

For the full wikilink syntax (display text, heading links, block links), see
`references/obsidian-markdown.md`.
