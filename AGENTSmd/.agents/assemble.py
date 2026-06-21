#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["python-frontmatter>=1.1"]
# ///
"""Assemble the AGENTSmd fragment tree into a single AGENTS.md.

The filesystem tree IS the structure. This walker does ONLY structure mapping:
it reads each fragment's YAML frontmatter (title, order), sorts siblings by
`order`, and emits a pandoc outline of synthesized section headings plus
`{.include}` directives. All markdown processing -- transclusion, heading-level
rebasing, normalization -- is delegated to pandoc + the standard include-files.lua
filter (`-M include-auto` shifts each fragment's own headings to sit under its
synthesized section heading). Frontmatter is stripped by pandoc.read automatically.

A directory is a section: its heading text comes from its `index.md` frontmatter,
its body is `index.md`'s content. The root `index.md` is the preamble (no heading).
Every non-root directory MUST have an `index.md`; every fragment MUST declare
`title` and `order`. Anything missing is a hard error -- no fallbacks.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import frontmatter

INDEX = "index.md"


def fail(msg: str) -> None:
    raise SystemExit(f"assemble: {msg}")


def load(md: Path) -> tuple[str | None, int | None, str]:
    """Return (title, order, body) for a fragment, validating frontmatter."""
    try:
        post = frontmatter.load(md)
    except Exception as exc:  # malformed YAML -> fail loud, naming the file
        fail(f"{md}: invalid frontmatter ({exc})")
    return post.get("title"), post.get("order"), post.content


def require_meta(md: Path) -> tuple[str, int]:
    title, order, _ = load(md)
    if not title or not isinstance(title, str):
        fail(f"{md}: missing or non-string `title` frontmatter")
    if not isinstance(order, int):
        fail(f"{md}: missing or non-integer `order` frontmatter")
    return title, order


def include_block(md: Path) -> str:
    return f"```{{.include}}\n{md.resolve()}\n```\n\n"


SKIP: set[Path] = set()

# Non-fragment files in the content tree (tooling lives under .agents/, already skipped
# as a dotdir; only the module README sits alongside the fragments).
MACHINERY = {"README.md"}


def children(d: Path) -> list[Path]:
    """Section children: subdirectories and non-index .md fragments."""
    out: list[Path] = []
    for entry in d.iterdir():
        if entry.resolve() in SKIP or entry.name in MACHINERY or entry.name.startswith("."):
            continue
        if entry.is_dir():
            out.append(entry)
        elif entry.suffix == ".md" and entry.name != INDEX:
            out.append(entry)
        elif entry.is_file() and entry.suffix != ".md":
            fail(f"{entry}: unexpected non-markdown file in tree")
    return out


def order_of(entry: Path) -> int:
    idx = entry / INDEX if entry.is_dir() else entry
    if entry.is_dir() and not idx.exists():
        fail(f"{entry}: directory has no {INDEX}")
    return require_meta(idx)[1]


def emit_dir(d: Path, level: int, is_root: bool) -> str:
    parts: list[str] = []
    index = d / INDEX

    if is_root:
        if not index.exists():
            fail(f"{d}: root requires an {INDEX} preamble")
        parts.append(include_block(index))  # preamble, no heading
    else:
        if not index.exists():
            fail(f"{d}: directory has no {INDEX}")
        title, _ = require_meta(index)
        parts.append(f"{'#' * level} {title}\n\n")
        parts.append(include_block(index))

    for child in sorted(children(d), key=order_of):
        if child.is_dir():
            parts.append(emit_dir(child, level + 1, is_root=False))
        else:
            title, _ = require_meta(child)
            parts.append(f"{'#' * (level + 1)} {title}\n\n")
            parts.append(include_block(child))

    return "".join(parts)


def main() -> None:
    if len(sys.argv) != 3:
        fail("usage: assemble.py <tree-root> <output-file>")
    root = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    SKIP.add(out)  # never treat the generated artifact as a source fragment
    filt = Path(__file__).resolve().parent / "filters" / "include-files.lua"
    if not filt.exists():
        fail(f"missing required filter: {filt}")

    outline = emit_dir(root, level=0, is_root=True)
    outline_file = root / ".outline.tmp.md"
    outline_file.write_text(outline, encoding="utf-8")

    try:
        subprocess.run(
            [
                "pandoc",
                str(outline_file),
                "--lua-filter", str(filt),
                "-M", "include-auto",
                "-f", "markdown",
                "-t", "gfm",
                "--wrap=preserve",
                "-o", str(out),
            ],
            check=True,
        )
    finally:
        outline_file.unlink()

    print(f"assembled -> {out}")


if __name__ == "__main__":
    main()
