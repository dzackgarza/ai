"""Validated configuration and skill-discovery contracts."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, field_validator


def parse_path(value: str | Path) -> Path:
    """Convert TOML's native string path into a filesystem path."""
    return Path(value)


class FuzzySettings(BaseModel):
    """Control how many near matches a failed lookup returns."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    minimum_score: Annotated[float, Field(ge=0.0, le=100.0)]
    limit: Annotated[int, Field(gt=0)]


class Settings(BaseModel):
    """Complete runtime settings loaded from the TOML configuration."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    skills_dir: Annotated[Path, BeforeValidator(parse_path)]
    fuzzy: FuzzySettings

    @field_validator("skills_dir")
    @classmethod
    def validate_skills_dir(cls, value: Path) -> Path:
        """Require a readable directory and normalize it to an absolute path."""
        resolved = value.expanduser().resolve()
        assert resolved.is_dir(), f"Skills directory is not a directory: {resolved}"
        return resolved


class SkillMetadata(BaseModel):
    """The frontmatter fields that distinguish a skill from a resource."""

    model_config = ConfigDict(extra="allow", frozen=True, strict=True)

    name: Annotated[str, Field(min_length=1)]
    description: Annotated[str, Field(min_length=1)]


class Skill(BaseModel):
    """One addressable skill document."""

    model_config = ConfigDict(frozen=True, strict=True)

    name: str
    description: str
    identifier: str
    path: Path


class SkillCatalog(BaseModel):
    """A complete, immutable view of the configured skill directory."""

    model_config = ConfigDict(frozen=True, strict=True)

    skills: tuple[Skill, ...]
    fuzzy: FuzzySettings


class Found(BaseModel):
    """A lookup with one exact result."""

    skill: Skill


class Ambiguous(BaseModel):
    """An exact name shared by multiple skills."""

    matches: tuple[Skill, ...]


class NoMatch(BaseModel):
    """A failed exact lookup and its ranked near matches."""

    suggestions: tuple[Skill, ...]


type LookupResult = Found | Ambiguous | NoMatch
