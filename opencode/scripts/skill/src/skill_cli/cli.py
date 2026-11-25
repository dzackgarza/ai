"""Command-line presentation for skill discovery."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import assert_never

from cyclopts import App
from rich.console import Console
from rich.text import Text
from rich.tree import Tree

from skill_cli.catalog import load_catalog, resolve_skill
from skill_cli.config import DEFAULT_CONFIG_PATH, load_settings
from skill_cli.models import (
    Ambiguous,
    Found,
    LookupResult,
    NoMatch,
    Skill,
    SkillCatalog,
)

app = App(name="skill-cli", help="List agent skills and print their absolute paths.")


def skill_label(skill: Skill, display_name: str, descriptions: bool) -> Text:
    """Format one skill name and its optional description."""
    label = Text(display_name)
    if descriptions:
        description = " ".join(skill.description.split())
        label.append(f" — {description}", style="dim")
        label.no_wrap = True
        label.overflow = "ellipsis"
    return label


def print_catalog(catalog: SkillCatalog, descriptions: bool) -> None:
    """Render roots and their descendants as a compact tree."""
    tree = Tree("Skills", hide_root=True, guide_style="dim")
    roots = [skill for skill in catalog.skills if "/" not in skill.identifier]
    for root in roots:
        branch = tree.add(skill_label(root, root.name, descriptions))
        prefix = f"{root.identifier}/"
        descendants = [
            skill for skill in catalog.skills if skill.identifier.startswith(prefix)
        ]
        for skill in descendants:
            relative_name = skill.identifier.removeprefix(prefix)
            branch.add(skill_label(skill, relative_name, descriptions))
    Console().print(tree)


def print_lookup_failure(result: Ambiguous | NoMatch, query: str) -> None:
    """Print exact choices for an ambiguous or unknown lookup."""
    match result:
        case Ambiguous(matches=matches):
            print(
                f"Skill name {query!r} is ambiguous. Use a qualified path:",
                file=sys.stderr,
            )
            for skill in matches:
                print(f"  {skill.identifier}", file=sys.stderr)
        case NoMatch(suggestions=suggestions):
            print(f"No exact skill named {query!r}.", file=sys.stderr)
            match suggestions:
                case []:
                    print("No near matches. Run 'skill-cli list'.", file=sys.stderr)
                case _:
                    print("Did you mean one of these?", file=sys.stderr)
                    for skill in suggestions:
                        print(
                            f"  {skill.identifier}  (retry: skill-cli get {skill.identifier})",
                            file=sys.stderr,
                        )
        case _:
            assert_never(result)


@app.command(name="list")
def list_command(
    descriptions: bool = False,
    config: Path = DEFAULT_CONFIG_PATH,
    skills_dir: Path | None = None,
) -> int:
    """List top-level skills and nested subskills by name.

    Args:
        descriptions: Include descriptions, truncated to the terminal width.
        config: Settings file (default: ~/.config/skill/config.toml).
        skills_dir: Override only the configured skills directory.
    """
    catalog = load_catalog(load_settings(config, skills_dir))
    print_catalog(catalog, descriptions)
    return 0


@app.command(name="get")
def get_command(
    name: str,
    config: Path = DEFAULT_CONFIG_PATH,
    skills_dir: Path | None = None,
) -> int:
    """Print one skill's absolute path without printing the skill's contents.

    NAME is an exact frontmatter name or qualified path such as
    mathematics/objects-in-code. Misses return nonzero and suggest near matches.

    Args:
        name: Exact skill name or qualified path.
        config: Settings file (default: ~/.config/skill/config.toml).
        skills_dir: Override only the configured skills directory.
    """
    catalog = load_catalog(load_settings(config, skills_dir))
    result: LookupResult = resolve_skill(catalog, name)
    match result:
        case Found(skill=skill):
            print(skill.path)
            return 0
        case Ambiguous() | NoMatch():
            print_lookup_failure(result, name)
            return 1
        case _:
            assert_never(result)
