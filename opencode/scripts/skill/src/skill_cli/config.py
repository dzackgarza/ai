"""Load and validate the skill CLI's TOML configuration."""

from __future__ import annotations

import tomllib
from pathlib import Path

from pydantic import validate_call

from skill_cli.models import Settings

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "skill" / "config.toml"


@validate_call
def load_settings(config_path: Path, skills_dir: Path | None) -> Settings:
    """Load settings, applying an explicit skills-directory override when given.

    Args:
        config_path: TOML file containing the complete settings.
        skills_dir: One-off replacement for the configured skills directory.
    """
    with config_path.expanduser().open("rb") as config_file:
        settings = Settings.model_validate(tomllib.load(config_file))

    match skills_dir:
        case None:
            return settings
        case Path():
            return Settings(skills_dir=skills_dir, fuzzy=settings.fuzzy)
