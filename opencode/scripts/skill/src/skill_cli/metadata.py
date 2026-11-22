"""Typed firewall for the untyped Python Frontmatter package."""

from __future__ import annotations

from pathlib import Path

import frontmatter

from skill_cli.models import SkillMetadata


def read_metadata(path: Path) -> SkillMetadata | None:
    """Return skill metadata, or no metadata for a plain Markdown resource."""
    document = frontmatter.load(str(path))
    if "name" not in document.metadata:
        return None
    return SkillMetadata.model_validate(document.metadata)
