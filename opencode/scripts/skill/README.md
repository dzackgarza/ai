# Skill CLI

`skill` lists agent skills and resolves their documentation paths. It does not print or
load skill bodies. An agent can read the returned absolute path with its own file tool.

## Install

Run `just install` from the repository root. This installs the command with `uv tool`
and creates `~/.config/skill/config.toml` when that file is absent.

The configuration names the skills directory and the fuzzy-match policy:

```toml
skills_dir = "/home/dzack/ai/opencode/skills"

[fuzzy]
minimum_score = 60.0
limit = 5
```

Set `skills_dir` to the root that contains the skill directories. Both settings under
`fuzzy` are required. `minimum_score` uses RapidFuzz's 0–100 scale. `limit` sets the
maximum number of suggestions after a failed lookup.

## Use

```bash
skill list
skill list --descriptions
skill get mathematics
skill get objects-in-code
skill get mathematics/objects-in-code
```

`list` shows top-level skills and their nested subskills. `--descriptions` keeps each
skill on one terminal line and truncates overflowing descriptions with an ellipsis.
`get` prints only the absolute path on standard output. It accepts an exact frontmatter
`name` when that name is unique. It also accepts a qualified identifier derived from the
file's path.

Every Markdown file with `name` and `description` frontmatter is addressable. Plain
reference files without a `name` remain excluded. Directory symlinks are supported.

An unknown name exits with status 1 and prints fuzzy near-hits to standard error. The
command never selects a fuzzy match. An ambiguous exact name also exits with status 1
and prints the qualified identifiers that resolve the ambiguity.

Use `--config PATH` to select another settings file. Use `--skills-dir PATH` for a
one-off directory override. Place these options after `list` or `get`.

## Develop

From the repository root, run `just test`. To inspect the command help without an
installed copy, run:

```bash
uv run --project opencode/scripts/skill skill --help
```
