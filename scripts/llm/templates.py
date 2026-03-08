"""
Template loading and rendering for markdown prompt templates.

Templates may use either standard markdown frontmatter:

    ---
    key: value
    ---
    body

or the legacy workspace format:

    key: value
    ---
    body

Use load_micro_agent(path) to parse them into a MicroAgent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import os
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


class TemplateFormatError(ValueError):
    """Raised when a micro-agent template file is structurally invalid."""


def default_prompts_dir() -> Path:
    """Return the workspace prompt root.

    PROMPTS_DIR may override the workspace default.
    """
    workspace_root = Path(__file__).resolve().parents[2]
    return Path(os.environ.get("PROMPTS_DIR", workspace_root / "prompts")).expanduser()


def resolve_prompt_path(path: str | Path) -> Path:
    """Resolve a prompt template path against PROMPTS_DIR."""
    candidate = Path(path).expanduser()
    if candidate.is_absolute():
        return candidate
    return default_prompts_dir() / candidate


def _parse_yaml_block(frontmatter_text: str) -> dict:
    try:
        metadata = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as exc:
        raise TemplateFormatError(f"Invalid YAML frontmatter: {exc}") from exc
    if not isinstance(metadata, dict):
        raise TemplateFormatError("Template frontmatter must be a YAML mapping")
    return metadata


def _split_frontmatter(content: str) -> tuple[dict, str]:
    """Split YAML frontmatter from template body."""
    if content.startswith("---\n"):
        end_marker = "\n---\n"
        end_idx = content.find(end_marker, 4)
        if end_idx == -1:
            raise TemplateFormatError("Opening markdown frontmatter marker missing closing '---'")
        frontmatter_text = content[4:end_idx]
        body = content[end_idx + len(end_marker):].lstrip("\n")
        return _parse_yaml_block(frontmatter_text), body

    lines = content.split("\n")
    sep_idx = next((i for i, line in enumerate(lines) if line == "---"), None)
    if sep_idx is None:
        return {}, content

    frontmatter_text = "\n".join(lines[:sep_idx])
    body = "\n".join(lines[sep_idx + 1:]).lstrip("\n")
    metadata = _parse_yaml_block(frontmatter_text)
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

    Raises TemplateFormatError if the template is structurally invalid.
    """
    resolved_path = resolve_prompt_path(path)
    content = resolved_path.read_text()
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
