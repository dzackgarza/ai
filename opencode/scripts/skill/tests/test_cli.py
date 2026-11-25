"""Behavioral tests for the public skill command."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


def add_skill(vault: Path, relative_path: str, name: str, description: str) -> Path:
    path = vault / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n")
    return path


def write_config(tmp_path: Path, skills_dir: Path) -> Path:
    config = tmp_path / "config.toml"
    config.write_text(
        f'skills_dir = "{skills_dir}"\n\n[fuzzy]\nminimum_score = 60.0\nlimit = 5\n'
    )
    return config


def run_skill(config: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    command, *command_arguments = arguments
    return subprocess.run(
        [
            "skill-cli",
            command,
            "--config",
            str(config),
            *command_arguments,
        ],
        check=False,
        capture_output=True,
        text=True,
        env=os.environ | {"COLUMNS": "80"},
    )


def make_vault(tmp_path: Path) -> tuple[Path, Path]:
    vault = tmp_path / "vault"
    add_skill(
        vault, "mathematics/SKILL.md", "mathematics", "Prove mathematical results."
    )
    add_skill(
        vault,
        "mathematics/objects-in-code/objects-in-code.md",
        "objects-in-code",
        "Represent mathematical objects in code.",
    )
    add_skill(
        vault,
        "mathematical-obsidian-vault-steward/SKILL.md",
        "mathematical-obsidian-vault-steward",
        "Maintain a mathematical vault.",
    )
    add_skill(
        vault,
        "mathematical-obsidian-vault-steward/references/original-draft.md",
        "original-draft",
        "Read the original draft.",
    )
    add_skill(vault, "code-patterns/SKILL.md", "code-patterns", "Route code patterns.")
    add_skill(
        vault,
        "code-patterns/general/general.md",
        "general",
        "General code patterns.",
    )
    add_skill(
        vault,
        "creating-skills/SKILL.md",
        "creating-skills",
        "Create agent skills.",
    )
    add_skill(
        vault,
        "creating-skills/general/general.md",
        "general",
        "General skill-authoring guidance.",
    )
    resource = vault / "mathematics/references/notation.md"
    resource.parent.mkdir(parents=True)
    resource.write_text("# Notation\n\nA resource, not a skill.\n")

    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    for name in (
        "code-patterns",
        "creating-skills",
        "mathematical-obsidian-vault-steward",
        "mathematics",
    ):
        (skills_dir / name).symlink_to(vault / name, target_is_directory=True)
    linked_nested = skills_dir / "mathematics/objects-in-code/objects-in-code.md"
    return linked_nested, write_config(tmp_path, skills_dir)


def test_list_shows_the_skill_tree_and_optional_descriptions(tmp_path: Path) -> None:
    """The list command includes nested skills but excludes plain resources."""
    _, config = make_vault(tmp_path)

    plain = run_skill(config, "list")
    described = run_skill(config, "list", "--descriptions")

    assert plain.returncode == 0
    assert described.returncode == 0
    assert "mathematics" in plain.stdout.splitlines()
    assert "objects-in-code" in plain.stdout
    assert "general" in plain.stdout
    assert "notation" not in plain.stdout
    assert "Prove mathematical results." not in plain.stdout
    assert "Prove mathematical results." in described.stdout
    assert "Represent mathematical objects in code." in described.stdout


def test_list_truncates_long_descriptions_to_one_terminal_line(tmp_path: Path) -> None:
    """Long and multiline descriptions preserve a scannable one-row tree."""
    _, config = make_vault(tmp_path)
    skill_dir = config.parent / "skills" / "mathematical-writing"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "---\n"
        "name: mathematical-writing\n"
        "description: |-\n"
        "  Review mathematical writing for clear claims, explicit definitions,\n"
        "  correct notation, and proofs supported by evidence.\n"
        "---\n\n"
        "# Mathematical writing\n"
    )

    result = run_skill(config, "list", "--descriptions")

    lines = result.stdout.splitlines()
    entries = [line for line in lines if line.startswith("mathematical-writing")]
    assert result.returncode == 0
    assert len(entries) == 1
    assert entries[0].startswith(
        "mathematical-writing — Review mathematical writing for clear claims,"
    )
    assert entries[0].endswith("…")
    assert len(entries[0]) <= 80
    assert all(line.strip() for line in lines)


def test_get_returns_an_absolute_path_for_top_level_and_nested_skills(
    tmp_path: Path,
) -> None:
    """Both a unique nested name and its qualified path resolve to its file."""
    nested, config = make_vault(tmp_path)

    by_name = run_skill(config, "get", "objects-in-code")
    by_path = run_skill(config, "get", "mathematics/objects-in-code")
    top_level = run_skill(config, "get", "mathematics")

    assert by_name.returncode == 0
    assert by_name.stdout == f"{nested}\n"
    assert by_path.returncode == 0
    assert by_path.stdout == f"{nested}\n"
    assert top_level.returncode == 0
    assert top_level.stdout == f"{nested.parent.parent / 'SKILL.md'}\n"


def test_get_rejects_a_near_miss_and_prompts_with_fuzzy_matches(
    tmp_path: Path,
) -> None:
    """A miss never selects a skill and instead names an exact retry."""
    nested, config = make_vault(tmp_path)

    result = run_skill(config, "get", "mathemtics")

    assert result.returncode == 1
    assert result.stdout == ""
    assert "mathematics" in result.stderr
    assert "skill-cli get mathematics" in result.stderr
    assert "original-draft" not in result.stderr
    assert str(nested) not in result.stderr


def test_get_rejects_an_ambiguous_subskill_name_with_qualified_choices(
    tmp_path: Path,
) -> None:
    """An exact leaf name must resolve uniquely or return qualified paths."""
    _, config = make_vault(tmp_path)

    result = run_skill(config, "get", "general")

    assert result.returncode == 1
    assert result.stdout == ""
    assert "code-patterns/general" in result.stderr
    assert "creating-skills/general" in result.stderr


def test_missing_lookup_command_does_not_execute_procps_skill(tmp_path: Path) -> None:
    """A missing lookup CLI fails even when the old executable name is on PATH."""
    sentinel = tmp_path / "skill"
    marker = tmp_path / "signal-command-ran"
    sentinel.write_text('#!/bin/sh\nprintf invoked > "$MARKER"\n')
    sentinel.chmod(0o755)

    readme = Path(__file__).resolve().parents[1] / "README.md"
    examples = readme.read_text().split("## Use", 1)[1]
    commands = examples.split("```bash\n", 1)[1].split("```", 1)[0].splitlines()
    assert commands
    for invocation in commands:
        result = subprocess.run(
            ["/bin/sh", "-c", invocation],
            check=False,
            capture_output=True,
            text=True,
            env=os.environ | {"PATH": str(tmp_path), "MARKER": str(marker)},
        )
        assert result.returncode != 0
        assert "skill-cli" in result.stderr
        assert not marker.exists()
