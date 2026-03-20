#!/usr/bin/env python3
"""main.py — CLI entry point for the OpenCode permission system.

Responsibilities:
  - Parse CLI arguments
  - Write compiled permissions to agent config files
  - Delegate display to src/display.py

To add an agent: create a file in agents/primary/ or agents/subagents/,
subclass PureAgent or Subagent, and assign AGENT = YourClass().
Internals live in src/; rulesets in src/rulesets/.
"""

import json
import logging
import os
import subprocess
import sys
from pathlib import Path

import yaml

# Ensure sibling modules are importable when run directly.
sys.path.insert(0, os.path.dirname(__file__))

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from src.agent_markdown import (
    _FRONTMATTER_ORDER,
    PROMPT_TOKEN_WARNING_THRESHOLD,
    GeneratedAgentArtifact,
    load_static_markdown_artifact,
    write_markdown_artifact,
)
from src.compiler import GLOBAL_DEFAULTS
from src.display import (
    console,
    load_agent_rulesets,
    show_rulesets,
)
from src.validate_inventory import UndeclaredToolError, validate_tool_inventory

# ---------------------------------------------------------------------------
# File paths
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_BASE_DIR = Path(os.path.expanduser("~/.config/opencode"))
_SKELETON = _BASE_DIR / "configs" / "config_skeleton.json"
_MARKDOWN_AGENTS_DIR = _BASE_DIR / "agents"
_BUILD_CONFIG_SCRIPT = _PROJECT_ROOT / "scripts" / "build_config.py"

BUILTIN_SHADOWS = {
    "build": "interactive-agents/opencode-build",
    "explore": "sub-agents/opencode-explore",
    "compaction": "micro-agents/opencode-compaction",
    "title": "micro-agents/opencode-title",
    "summary": "micro-agents/opencode-summary",
}

# Compiled-agents workflow paths
_COMPILED_AGENTS_DEFAULT = Path(
    os.path.expanduser("~/opencode-plugins/clis/ai-prompts/compiled-agents")
)

_build_console = Console(stderr=True)
_handler = RichHandler(
    console=_build_console, markup=True, show_path=False, rich_tracebacks=True
)
_handler.setFormatter(logging.Formatter("%(message)s"))
logger = logging.getLogger("opencode.permissions.build")
if not logger.handlers:
    logger.addHandler(_handler)
logger.setLevel(logging.INFO)
logger.propagate = False


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------


def _read_json(path: str | Path) -> dict:
    with open(path) as f:
        return json.load(f)


def _write_json(path: str | Path, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


# ---------------------------------------------------------------------------
# Compiled-agents workflow (YAML-driven)
# ---------------------------------------------------------------------------


def _warn_for_large_prompts(artifacts: list[GeneratedAgentArtifact]) -> None:
    oversized = [
        artifact
        for artifact in artifacts
        if artifact.token_count > PROMPT_TOKEN_WARNING_THRESHOLD
    ]
    if not oversized:
        return
    table = Table(title="Prompt token warnings", show_header=True)
    table.add_column("Agent", style="bold")
    table.add_column("Tokens", justify="right")
    table.add_column("Model")
    table.add_column("Source template", style="dim")
    for artifact in sorted(oversized, key=lambda item: item.token_count, reverse=True):
        table.add_row(
            artifact.name,
            str(artifact.token_count),
            artifact.model or "-",
            artifact.source_template,
        )
    console.print(table)
    logger.warning(
        "[yellow]Prompt token threshold exceeded for %d agent(s) (limit=%d)[/yellow]",
        len(oversized),
        PROMPT_TOKEN_WARNING_THRESHOLD,
        extra={"markup": True},
    )


def _validate_written_artifacts(artifacts: list[GeneratedAgentArtifact]) -> None:
    missing = [
        artifact.output_filename
        for artifact in artifacts
        if not (_MARKDOWN_AGENTS_DIR / artifact.output_filename).exists()
    ]
    if missing:
        raise RuntimeError(f"Generated agent files missing after write: {missing}")


def _process_compiled_agent(
    markdown_path: Path,
) -> GeneratedAgentArtifact | None:
    """Process one compiled agent markdown file, injecting permissions.

    Expects frontmatter to contain 'permission_tags' field: a list of tags
    matching ruleset names to apply in order.
    Optional 'permission_overrides' field for agent-specific overrides.
    """
    content = markdown_path.read_text()

    # Parse frontmatter
    if not content.startswith("---\n"):
        logger.warning("Skipping %s: missing YAML frontmatter", markdown_path.name)
        return None

    end_idx = content.find("\n---\n", 4)
    if end_idx == -1:
        logger.warning("Skipping %s: malformed YAML frontmatter", markdown_path.name)
        return None

    frontmatter = yaml.safe_load(content[4:end_idx]) or {}
    body = content[end_idx + len("\n---\n") :].rstrip()

    # Get permission tags from frontmatter
    permission_tags = frontmatter.get("permission_tags")
    if not permission_tags:
        logger.warning(
            "Skipping %s: missing 'permission_tags' field in frontmatter",
            markdown_path.name,
        )
        return None

    agent_name = frontmatter.get("name", markdown_path.stem)
    base_type = frontmatter.get("mode", "primary")
    if base_type == "primary":
        base_type = "pure_agent"
    elif base_type == "subagent":
        base_type = "subagent"

    # Get overrides from frontmatter if present
    agent_overrides = frontmatter.get("permission_overrides", {})

    # Compile permissions from tags
    permissions = compile_from_tags(permission_tags, base_type, agent_overrides)

    # Build new frontmatter with permissions injected
    new_frontmatter = {}
    for key in _FRONTMATTER_ORDER:
        if key in frontmatter:
            new_frontmatter[key] = frontmatter[key]
    for key, value in frontmatter.items():
        if key not in new_frontmatter and key != "system":
            new_frontmatter[key] = value
    new_frontmatter["permission"] = permissions
    new_frontmatter["name"] = agent_name

    # Render markdown
    dumped = yaml.safe_dump(
        new_frontmatter, sort_keys=False, allow_unicode=False
    ).strip()
    markdown = f"---\n{dumped}\n---\n\n{body}\n"

    # Count tokens
    import tiktoken

    try:
        encoding = tiktoken.encoding_for_model(frontmatter.get("model", "gpt-4"))
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    token_count = len(encoding.encode(body))

    return GeneratedAgentArtifact(
        name=agent_name,
        output_filename=markdown_path.name,
        markdown=markdown,
        prompt_body=body,
        frontmatter=new_frontmatter,
        token_count=token_count,
        model=frontmatter.get("model"),
        source_template=slug,
    )


def build_from_compiled_agents(
    compiled_agents_dir: Path | None = None,
    output_dir: Path | None = None,
) -> list[GeneratedAgentArtifact]:
    """Build all agents from compiled markdown files.

    Args:
        compiled_agents_dir: Directory with compiled agent markdown (default: ~/opencode-plugins/clis/ai-prompts/compiled-agents)
        output_dir: Output directory for agent files (default: ~/.config/opencode/agents)
    """
    compiled_agents_dir = compiled_agents_dir or _COMPILED_AGENTS_DEFAULT
    output_dir = output_dir or _MARKDOWN_AGENTS_DIR

    if not compiled_agents_dir.exists():
        raise RuntimeError(
            f"Compiled agents directory not found: {compiled_agents_dir}"
        )

    # Validate tool inventory
    try:
        validate_tool_inventory(GLOBAL_DEFAULTS)
    except UndeclaredToolError as exc:
        console.print(f"[bold red]{exc}[/bold red]")
        sys.exit(1)

    # Process all markdown files
    artifacts = []
    for md_file in sorted(compiled_agents_dir.glob("*.md")):
        artifact = _process_compiled_agent(md_file)
        if artifact:
            artifacts.append(artifact)
            output_path = write_markdown_artifact(artifact, output_dir)
            logger.info("wrote %s", output_path.name)

    # Also process builtin shadows (static templates)
    for agent_name, prompt_slug in BUILTIN_SHADOWS.items():
        artifact = load_static_markdown_artifact(
            prompt_slug=prompt_slug, output_name=f"{agent_name}.md"
        )
        artifacts.append(artifact)
        output_path = write_markdown_artifact(artifact, output_dir)
        logger.info("wrote %s (static)", output_path.name)

    _validate_written_artifacts(artifacts)
    _warn_for_large_prompts(artifacts)

    logger.info("Built %d agents from compiled markdown", len(artifacts))
    return artifacts


def apply_agents() -> list[GeneratedAgentArtifact]:
    """Write compiled permissions to all managed markdown agent files."""
    try:
        validate_tool_inventory(GLOBAL_DEFAULTS)
    except UndeclaredToolError as exc:
        console.print(f"[bold red]{exc}[/bold red]")
        sys.exit(1)

    # Global defaults → skeleton
    if _SKELETON.exists():
        data = _read_json(_SKELETON)
        data["permission"] = GLOBAL_DEFAULTS
        _write_json(_SKELETON, data)
        logger.info(
            "Applied global defaults to [bold]config_skeleton.json[/bold]",
            extra={"markup": True},
        )
    else:
        logger.warning(
            "[yellow]config_skeleton.json not found; skipped global default update[/yellow]",
            extra={"markup": True},
        )

    artifacts = _build_artifacts()
    for artifact in artifacts:
        output_path = write_markdown_artifact(artifact, _MARKDOWN_AGENTS_DIR)
        logger.info("wrote %s", output_path.name)

    _validate_written_artifacts(artifacts)
    _warn_for_large_prompts(artifacts)
    return artifacts


def _validate_runtime_agents(expected_names: set[str]) -> None:
    runtime_rulesets = load_agent_rulesets()
    runtime_names = set(runtime_rulesets)
    missing = sorted(expected_names - runtime_names)
    if missing:
        raise RuntimeError(
            f"Generated agents missing from runtime `opencode agent list`: {missing}"
        )
    logger.info(
        "Validated %d generated agents against `opencode agent list`",
        len(expected_names),
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

app = typer.Typer(help="Manage OpenCode agent permissions.")


@app.command()
def build(
    compiled_agents_dir: Path = typer.Option(
        _COMPILED_AGENTS_DEFAULT,
        "--compiled-agents-dir",
        "-d",
        help="Directory with compiled agent markdown files",
    ),
) -> None:
    """Write markdown agents, rebuild opencode.json, and validate runtime visibility.

    Uses the YAML-driven workflow with compiled agents from ai-prompts.
    """
    artifacts = build_from_compiled_agents(compiled_agents_dir=compiled_agents_dir)
    logger.info("Running %s", _BUILD_CONFIG_SCRIPT.relative_to(_PROJECT_ROOT))
    subprocess.run(
        [sys.executable, str(_BUILD_CONFIG_SCRIPT)], cwd=_PROJECT_ROOT, check=True
    )
    expected_names = {artifact.name for artifact in artifacts}
    _validate_runtime_agents(expected_names)
    logger.info("Build complete: %d generated agents validated", len(expected_names))


@app.command(name="list-rulesets")
def list_rulesets_cmd() -> None:
    """List available rulesets (abstract rule combinations)."""
    show_rulesets()


@app.command(name="validate-tools")
def validate_tools_cmd() -> None:
    """Validate GLOBAL_DEFAULTS covers exactly the known tool set (static + MCP)."""
    validate_tool_inventory(GLOBAL_DEFAULTS)
    console.print(
        "[green]Tool inventory OK — GLOBAL_DEFAULTS matches all known tools.[/green]"
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
