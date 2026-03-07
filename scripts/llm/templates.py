"""
Template loading and rendering.

Templates live in scripts/templates/ (sibling of scripts/llm/).
Callers pass names like "classifier/playbook" or "tiers/A" — no extension.

Micro-agent templates (prompts/micro_agents/**/*.md) use YAML frontmatter.
Use load_micro_agent(path) to parse them into {frontmatter, system, body}.

Supports Jinja2 rendering with keyword variables.

CLI:
    python -m scripts.llm.templates <name>               # print raw template
    python -m scripts.llm.templates <name> var=value ... # render with variables
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Template

# Canonical templates directory: scripts/templates/ (sibling of scripts/llm/)
_TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


def _split_frontmatter(content: str) -> tuple[dict, str]:
    """Split YAML frontmatter from template body.

    The format is: a YAML block followed by a bare '---' separator line
    (at column 0, on its own line), then the Jinja2 body. Content inside
    YAML block scalars (e.g. system: |) is indented, so their internal
    '---' markers never appear at column 0 and are not mistaken for the
    separator.

    Returns (metadata_dict, body_text). If no bare '---' separator is
    found, returns ({}, content).
    """
    lines = content.split("\n")
    sep_idx = next((i for i, line in enumerate(lines) if line == "---"), None)
    if sep_idx is None:
        return {}, content

    frontmatter_text = "\n".join(lines[:sep_idx])
    body = "\n".join(lines[sep_idx + 1 :]).lstrip("\n")
    metadata = yaml.safe_load(frontmatter_text) or {}
    return metadata, body


@dataclass
class MicroAgent:
    """Parsed micro-agent template."""

    frontmatter: dict[str, Any]
    system: str | None
    body: str

    def render(self, **variables: str) -> str:
        """Render the body as a Jinja2 template."""
        return Template(self.body).render(**variables)


def load_micro_agent(path: str | Path) -> MicroAgent:
    """Parse a micro-agent .md file into frontmatter, system prompt, and body.

    The system prompt is taken from the 'system:' field in the YAML frontmatter.
    The body is the Jinja2 template below the frontmatter separator.
    """
    content = Path(path).read_text()
    frontmatter, body = _split_frontmatter(content)
    system = frontmatter.get("system")
    return MicroAgent(frontmatter=frontmatter, system=system, body=body)


def render_body(body: str, **variables: str) -> str:
    """Render a Jinja2 template body string with the given variables."""
    return Template(body).render(**variables)


def load_template(name: str, *, path: str | None = None) -> str:
    """Load a template by name or absolute path.

    If *path* is given, it is used directly (absolute path to the file).
    Otherwise, *name* is resolved against the canonical templates directory,
    searching for <name>.md then <name>.yaml then <name> (no extension).

    Raises FileNotFoundError if not found.
    """
    if path is not None:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Template path {path!r} not found")
        return p.read_text()

    for ext in (".md", ".yaml", ""):
        p = _TEMPLATES_DIR / (name + ext)
        if p.exists():
            return p.read_text()
    raise FileNotFoundError(f"Template {name!r} not found in {_TEMPLATES_DIR}")


def render_template(name: str, *, path: str | None = None, **variables: str) -> str:
    """Load and Jinja2-render a template with the given variables."""
    content = load_template(name, path=path)
    return Template(content).render(**variables)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python -m scripts.llm.templates <name> [var=value ...]",
            file=sys.stderr,
        )
        sys.exit(1)

    name = sys.argv[1]
    variables: dict[str, str] = {}
    for arg in sys.argv[2:]:
        if "=" not in arg:
            print(f"Invalid var format: {arg!r} (expected key=value)", file=sys.stderr)
            sys.exit(1)
        k, v = arg.split("=", 1)
        variables[k.strip()] = v.strip()

    try:
        if variables:
            print(render_template(name, **variables))
        else:
            print(load_template(name))
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
