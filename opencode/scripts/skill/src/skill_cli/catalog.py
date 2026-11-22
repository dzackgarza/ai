"""Discover and resolve skill documents.

Discovery follows the Agent Skills frontmatter contract:
https://agentskills.io/specification
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

from pydantic import validate_call
from rapidfuzz import fuzz, process

from skill_cli.metadata import read_metadata
from skill_cli.models import (
    Ambiguous,
    Found,
    LookupResult,
    NoMatch,
    Settings,
    Skill,
    SkillCatalog,
)

EXCLUDED_DIRECTORIES = frozenset(
    {".git", ".mypy_cache", ".ruff_cache", ".venv", "__pycache__", "node_modules"}
)


def iter_markdown_files(skills_dir: Path) -> Iterator[Path]:
    """Yield Markdown files in deterministic order, including symlink targets."""
    seen_directories: set[Path] = set()
    for current, directory_names, file_names in os.walk(skills_dir, followlinks=True):
        current_path = Path(current).absolute()
        resolved_current = current_path.resolve()
        if resolved_current in seen_directories:
            directory_names.clear()
            continue
        seen_directories.add(resolved_current)
        directory_names[:] = sorted(
            name for name in directory_names if name not in EXCLUDED_DIRECTORIES
        )
        for file_name in sorted(file_names):
            if file_name.endswith(".md"):
                yield current_path / file_name


def skill_identifier(skills_dir: Path, path: Path) -> str:
    """Derive a qualified name from a path, dropping redundant file names."""
    relative = path.relative_to(skills_dir)
    if path.name == "SKILL.md":
        return relative.parent.as_posix()
    without_suffix = relative.with_suffix("")
    if without_suffix.name == without_suffix.parent.name:
        return without_suffix.parent.as_posix()
    return without_suffix.as_posix()


@validate_call
def load_catalog(settings: Settings) -> SkillCatalog:
    """Read skill metadata without returning any skill body to the caller."""
    skills: dict[str, Skill] = {}
    for path in iter_markdown_files(settings.skills_dir):
        metadata = read_metadata(path)
        if metadata is None:
            continue
        identifier = skill_identifier(settings.skills_dir, path)
        assert identifier not in skills, (
            f"Duplicate skill identifier {identifier!r}: "
            f"{skills[identifier].path} and {path}"
        )
        skills[identifier] = Skill(
            name=metadata.name,
            description=metadata.description,
            identifier=identifier,
            path=path,
        )
    return SkillCatalog(
        skills=tuple(skills[key] for key in sorted(skills)),
        fuzzy=settings.fuzzy,
    )


def near_matches(catalog: SkillCatalog, query: str) -> tuple[Skill, ...]:
    """Rank declared skill names with RapidFuzz's weighted ratio."""
    names = [skill.name for skill in catalog.skills]
    matches = process.extract(
        query,
        names,
        scorer=fuzz.WRatio,
        limit=catalog.fuzzy.limit,
        score_cutoff=catalog.fuzzy.minimum_score,
    )
    return tuple(catalog.skills[index] for _, _, index in matches)


@validate_call
def resolve_skill(catalog: SkillCatalog, query: str) -> LookupResult:
    """Resolve an exact qualified path or unique name, never a fuzzy guess."""
    path_matches = tuple(skill for skill in catalog.skills if skill.identifier == query)
    match path_matches:
        case [skill]:
            return Found(skill=skill)
        case []:
            pass
        case _:
            assert False, f"Duplicate catalog paths for {query!r}: {path_matches}"

    name_matches = tuple(skill for skill in catalog.skills if skill.name == query)
    match name_matches:
        case [skill]:
            return Found(skill=skill)
        case []:
            return NoMatch(suggestions=near_matches(catalog, query))
        case matches:
            return Ambiguous(matches=matches)
