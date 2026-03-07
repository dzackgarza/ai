"""
Template loading and rendering for micro-agent prompts.

Micro-agent templates (prompts/micro_agents/**/*.md) use YAML frontmatter.
Use load_micro_agent(path) to parse them into {frontmatter, system, body}.

Supports Jinja2 rendering with keyword variables.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Template


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


if __name__ == "__main__":
    import sys

    print(
        "Usage: use load_micro_agent(path) to load micro-agent templates.",
        file=sys.stderr,
    )
    sys.exit(1)
