#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6", "python-frontmatter>=1.1"]
# ///

"""Assemble the AGENTSmd fragment tree into a single AGENTS.md.

The filesystem tree defines document structure. Each fragment may carry
classification tags from the build configuration. The compiler validates the
taxonomy, omits fragments matching active exclusions, emits a Pandoc outline,
and reports the selection decision for every discovered fragment.

A directory is a section: its heading text comes from its `index.md`
frontmatter, and its body is that file's content. The root `index.md` is the
preamble and has no synthesized heading. If a directory index is excluded, its
heading remains when included descendants still require the section structure.
"""

from __future__ import annotations

import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Never

import frontmatter
from yaml import YAMLError

INDEX = "index.md"
SKIP: set[Path] = set()

# Non-fragment files in the content tree. Tooling lives under the hidden
# .agents directory and is already skipped by children().
MACHINERY = {"README.md"}


@dataclass(frozen=True)
class BuildConfig:
    allowed_tags: frozenset[str]
    exclude_tags: frozenset[str]


@dataclass(frozen=True)
class FragmentMeta:
    title: str | None
    order: int | None
    tags: tuple[str, ...]


@dataclass(frozen=True)
class SelectionRecord:
    path: Path
    tags: tuple[str, ...]
    excluded_by: tuple[str, ...]

    @property
    def included(self) -> bool:
        return not self.excluded_by


def fail(msg: str) -> Never:
    raise SystemExit(f"assemble: {msg}")


def require_exact_keys(
    value: object,
    expected: set[str],
    *,
    location: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{location}: expected a table")
    actual = set(value)
    if actual != expected:
        fail(f"{location}: expected keys {sorted(expected)}, found {sorted(actual)}")
    return value


def require_tag_list(value: object, *, location: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        fail(f"{location}: expected a list of tags")
    if any(not isinstance(tag, str) or not tag or tag.strip() != tag for tag in value):
        fail(f"{location}: tags must be non-empty strings without outer whitespace")
    tags = tuple(value)
    if len(set(tags)) != len(tags):
        fail(f"{location}: duplicate tags are not allowed")
    return tags


def load_config(path: Path) -> BuildConfig:
    if not path.is_file():
        fail(f"missing build config: {path}")
    try:
        with path.open("rb") as handle:
            raw = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        fail(f"{path}: invalid TOML ({exc})")

    top = require_exact_keys(
        raw,
        {"selection", "taxonomy"},
        location=str(path),
    )
    selection = require_exact_keys(
        top["selection"],
        {"exclude_tags"},
        location=f"{path} [selection]",
    )
    taxonomy = require_exact_keys(
        top["taxonomy"],
        {"allowed_tags"},
        location=f"{path} [taxonomy]",
    )

    allowed = require_tag_list(
        taxonomy["allowed_tags"],
        location=f"{path} taxonomy.allowed_tags",
    )
    if not allowed:
        fail(f"{path} taxonomy.allowed_tags: at least one tag is required")
    excluded = require_tag_list(
        selection["exclude_tags"],
        location=f"{path} selection.exclude_tags",
    )
    unknown_exclusions = sorted(set(excluded) - set(allowed))
    if unknown_exclusions:
        fail(f"{path} selection.exclude_tags: unknown tags {unknown_exclusions}")

    return BuildConfig(
        allowed_tags=frozenset(allowed),
        exclude_tags=frozenset(excluded),
    )


def load_fragment(
    md: Path,
    config: BuildConfig,
    *,
    require_title_order: bool,
) -> FragmentMeta:
    try:
        post = frontmatter.load(md)
    except YAMLError as exc:
        fail(f"{md}: invalid frontmatter ({exc})")

    title = post.metadata["title"] if "title" in post.metadata else None
    order = post.metadata["order"] if "order" in post.metadata else None
    raw_tags = post.metadata["tags"] if "tags" in post.metadata else []
    tags = require_tag_list(raw_tags, location=f"{md} tags")

    unknown_tags = sorted(set(tags) - config.allowed_tags)
    if unknown_tags:
        fail(f"{md}: unknown tags {unknown_tags}")

    if require_title_order:
        if not isinstance(title, str) or not title:
            fail(f"{md}: missing or non-string `title` frontmatter")
        if type(order) is not int:
            fail(f"{md}: missing or non-integer `order` frontmatter")

    return FragmentMeta(title=title, order=order, tags=tags)


def fragment_meta(
    md: Path,
    config: BuildConfig,
    cache: dict[Path, FragmentMeta],
    *,
    require_title_order: bool,
) -> FragmentMeta:
    if md not in cache:
        cache[md] = load_fragment(
            md,
            config,
            require_title_order=require_title_order,
        )
    return cache[md]


def include_block(md: Path) -> str:
    return f"```{{.include format=markdown+wikilinks_title_after_pipe}}\n{md.resolve()}\n```\n\n"


def children(directory: Path) -> list[Path]:
    """Return section children: subdirectories and non-index Markdown files."""
    result: list[Path] = []
    for entry in directory.iterdir():
        if entry.resolve() in SKIP:
            continue
        if entry.name.startswith(".") or entry.name in MACHINERY:
            continue
        if entry.is_dir():
            result.append(entry)
        elif entry.is_file() and entry.suffix == ".md" and entry.name != INDEX:
            result.append(entry)
        elif entry.is_file() and entry.suffix != ".md":
            fail(f"{entry}: unexpected non-markdown file in tree")
    return result


def order_of(
    entry: Path,
    config: BuildConfig,
    cache: dict[Path, FragmentMeta],
) -> int:
    index = entry / INDEX if entry.is_dir() else entry
    if entry.is_dir() and not index.exists():
        fail(f"{entry}: directory has no {INDEX}")
    meta = fragment_meta(
        index,
        config,
        cache,
        require_title_order=True,
    )
    assert meta.order is not None
    return meta.order


def record_selection(
    md: Path,
    meta: FragmentMeta,
    config: BuildConfig,
    records: list[SelectionRecord],
) -> bool:
    excluded_by = tuple(sorted(set(meta.tags) & config.exclude_tags))
    records.append(
        SelectionRecord(
            path=md,
            tags=meta.tags,
            excluded_by=excluded_by,
        )
    )
    return not excluded_by


def emit_dir(
    directory: Path,
    level: int,
    is_root: bool,
    config: BuildConfig,
    cache: dict[Path, FragmentMeta],
    records: list[SelectionRecord],
) -> str:
    index = directory / INDEX
    if not index.exists():
        kind = "root requires an" if is_root else "directory has no"
        fail(f"{directory}: {kind} {INDEX}")

    index_meta = fragment_meta(
        index,
        config,
        cache,
        require_title_order=not is_root,
    )
    index_included = record_selection(index, index_meta, config, records)

    child_parts: list[str] = []
    ordered_children = sorted(
        children(directory),
        key=lambda entry: order_of(entry, config, cache),
    )
    for child in ordered_children:
        if child.is_dir():
            child_outline = emit_dir(
                child,
                level + 1,
                False,
                config,
                cache,
                records,
            )
            if child_outline:
                child_parts.append(child_outline)
            continue

        child_meta = fragment_meta(
            child,
            config,
            cache,
            require_title_order=True,
        )
        if not record_selection(child, child_meta, config, records):
            continue
        assert child_meta.title is not None
        child_parts.append(f"{'#' * (level + 1)} {child_meta.title}\n\n")
        child_parts.append(include_block(child))

    index_part = include_block(index) if index_included else ""
    descendants = "".join(child_parts)
    if is_root:
        return index_part + descendants
    if not index_part and not descendants:
        return ""

    assert index_meta.title is not None
    heading = f"{'#' * level} {index_meta.title}\n\n"
    return heading + index_part + descendants


def print_report(
    root: Path,
    config_path: Path,
    records: list[SelectionRecord],
    out: Path,
) -> None:
    print(f"fragment selection config: {config_path}")
    for record in records:
        path = record.path.relative_to(root).as_posix()
        tags = ", ".join(record.tags) if record.tags else "untagged"
        if record.included:
            print(f"INCLUDED {path} tags=[{tags}]")
        else:
            matched = ", ".join(record.excluded_by)
            print(f"EXCLUDED {path} tags=[{tags}] matched=[{matched}]")

    included = sum(record.included for record in records)
    excluded = len(records) - included
    untagged = sum(not record.tags for record in records)
    print(
        f"fragments: {len(records)} discovered, {included} included, "
        f"{excluded} excluded, {untagged} untagged"
    )
    print(f"assembled -> {out}")


def main() -> None:
    if len(sys.argv) != 4:
        fail("usage: assemble.py <tree-root> <output-file> <config-file>")

    root = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    config_path = Path(sys.argv[3]).resolve()
    SKIP.add(out)

    config = load_config(config_path)
    filt = Path(__file__).resolve().parent / "filters" / "include-files.lua"
    if not filt.exists():
        fail(f"missing required filter: {filt}")

    cache: dict[Path, FragmentMeta] = {}
    records: list[SelectionRecord] = []
    outline = emit_dir(
        root,
        level=0,
        is_root=True,
        config=config,
        cache=cache,
        records=records,
    )
    outline_file = root / ".outline.tmp.md"
    outline_file.write_text(outline, encoding="utf-8")

    try:
        subprocess.run(
            [
                "pandoc",
                str(outline_file),
                "--lua-filter",
                str(filt),
                "-M",
                "include-auto",
                "-f",
                "markdown",
                "-t",
                "gfm",
                "--wrap=preserve",
                "-o",
                str(out),
            ],
            check=True,
        )
    finally:
        outline_file.unlink()

    print_report(root, config_path, records, out)


if __name__ == "__main__":
    main()
