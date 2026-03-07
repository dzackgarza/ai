"""
Template loading and rendering for micro-agent prompts.

Micro-agent templates (prompts/micro_agents/**/*.md) use YAML frontmatter.
Use load_micro_agent(path) to parse them into a MicroAgent.

Frontmatter fields:
    model:       Default model slug (provider/model). Required unless --model passed.
    temperature: Default temperature. Optional, default 0.0.
    system:      System prompt (YAML block scalar). Optional.
    schema:      Schema name from schemas.SCHEMAS for structured output. Optional.
    inputs:      List of {name, description, required} input variable declarations.

Variable validation:
    MicroAgent.render(**variables) validates that all required inputs are provided
    before rendering. Missing required variables raise MissingVariablesError.

Schema resolution:
    MicroAgent.schema_class() returns the pydantic BaseModel subclass registered
    under the frontmatter 'schema:' name, or None if no schema is declared.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml
from jinja2 import Template

if TYPE_CHECKING:
    from pydantic import BaseModel


class MissingVariablesError(ValueError):
    """Raised when required template variables are not provided to render()."""

    def __init__(self, missing: list[str]) -> None:
        self.missing = missing
        super().__init__(f"Missing required template variable(s): {', '.join(missing)}")


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
    _required_inputs: list[str] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        inputs: list[dict] = self.frontmatter.get("inputs") or []
        self._required_inputs = [
            inp["name"] for inp in inputs if inp.get("required", False)
        ]

    def render(self, **variables: str) -> str:
        """Render the body as a Jinja2 template.

        Raises MissingVariablesError if any required inputs (declared in
        frontmatter 'inputs:') are absent from variables.
        """
        missing = [k for k in self._required_inputs if k not in variables]
        if missing:
            raise MissingVariablesError(missing)
        return Template(self.body).render(**variables)

    def schema_class(self) -> type[BaseModel] | None:
        """Return the pydantic schema class declared in frontmatter, or None.

        Handles two forms:
          - String name: resolved against scripts.llm.schemas.SCHEMAS registry.
          - Dict {field: type_str}: dynamically builds a pydantic model via
            schemas.make_schema_from_dict(). The class is named "InlineSchema".

        Returns None if no schema is declared.
        """
        schema_value = self.frontmatter.get("schema")
        if not schema_value:
            return None
        # Import here to avoid circular import at module load time.
        from scripts.llm.schemas import make_schema_from_dict, resolve_schema  # noqa: PLC0415

        if isinstance(schema_value, dict):
            return make_schema_from_dict("InlineSchema", schema_value)
        return resolve_schema(str(schema_value))


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
