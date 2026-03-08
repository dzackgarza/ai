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
from jinja2 import BaseLoader, Environment
from jinja2.exceptions import TemplateNotFound

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


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    deduped: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved in seen:
            continue
        deduped.append(resolved)
        seen.add(resolved)
    return deduped


def _template_name_for_path(path: Path) -> str:
    resolved = path.resolve()
    prompts_dir = default_prompts_dir().resolve()
    try:
        return str(resolved.relative_to(prompts_dir))
    except ValueError:
        return str(resolved)


class PromptTemplateLoader(BaseLoader):
    """Load prompt-template markdown files, stripping child frontmatter."""

    def __init__(self, search_paths: list[Path]) -> None:
        self.search_paths = _dedupe_paths(search_paths)

    def get_source(
        self,
        environment: Environment,
        template: str,
    ) -> tuple[str, str, Any]:
        candidate = Path(template).expanduser()
        paths: list[Path]
        if candidate.is_absolute():
            paths = [candidate]
        else:
            paths = [search_path / candidate for search_path in self.search_paths]

        for path in paths:
            if not path.exists() or not path.is_file():
                continue
            source = path.read_text()
            _, body = _split_frontmatter(source)
            mtime = path.stat().st_mtime

            def uptodate(path: Path = path, mtime: float = mtime) -> bool:
                try:
                    return path.stat().st_mtime == mtime
                except OSError:
                    return False

            return body, str(path), uptodate

        raise TemplateNotFound(template)


class PromptTemplateEnvironment(Environment):
    """Jinja environment for prompt-template composition."""

    def join_path(self, template: str, parent: str) -> str:
        if template.startswith(("./", "../")):
            parent_path = Path(parent)
            if not parent_path.is_absolute():
                parent_path = (default_prompts_dir() / parent_path).resolve()
            return str((parent_path.parent / template).resolve())
        return template


def build_prompt_environment(template_path: str | Path | None = None) -> PromptTemplateEnvironment:
    """Create a Jinja environment rooted at PROMPTS_DIR and the template parent."""
    search_paths = [default_prompts_dir()]
    if template_path is not None:
        search_paths.insert(0, Path(template_path).expanduser().resolve().parent)
    return PromptTemplateEnvironment(loader=PromptTemplateLoader(search_paths))


def _render_with_environment(
    body: str,
    *,
    variables: dict[str, str],
    template_path: str | Path | None = None,
) -> str:
    environment = build_prompt_environment(template_path)
    if template_path is not None:
        template_name = _template_name_for_path(Path(template_path).expanduser())
        return environment.get_template(template_name).render(**variables)
    return environment.from_string(body).render(**variables)


@dataclass
class MicroAgent:
    """Parsed micro-agent template."""

    path: Path
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
        return _render_with_environment(
            self.body,
            variables=variables,
            template_path=self.path,
        )

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
    return MicroAgent(path=resolved_path, frontmatter=frontmatter, system=system, body=body)


def render_body(body: str, *, template_path: str | Path | None = None, **variables: str) -> str:
    """Render a Jinja2 template body string with the given variables."""
    return _render_with_environment(body, variables=variables, template_path=template_path)


if __name__ == "__main__":
    import sys

    print(
        "Usage: use load_micro_agent(path) to load micro-agent templates.",
        file=sys.stderr,
    )
    sys.exit(1)
