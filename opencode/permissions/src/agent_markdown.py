"""Generate OpenCode markdown agent files from prompt templates."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any

import tiktoken
import yaml

from scripts.llm import load_micro_agent, resolve_prompt_path

from src.base import Agent

_FRONTMATTER_ORDER = (
    "description",
    "mode",
    "model",
    "temperature",
    "top_p",
    "steps",
    "disable",
    "hidden",
    "color",
)

DEFAULT_PROMPT_TOKEN_ENCODING = os.environ.get(
    "OPENCODE_AGENT_TOKEN_ENCODING",
    "cl100k_base",
)
PROMPT_TOKEN_WARNING_THRESHOLD = int(
    os.environ.get("OPENCODE_AGENT_TOKEN_WARNING_THRESHOLD", "5000")
)


@dataclass(frozen=True)
class GeneratedAgentArtifact:
    """Rendered markdown-agent artifact plus validation metadata."""

    name: str
    output_filename: str
    markdown: str
    prompt_body: str
    frontmatter: dict[str, Any]
    token_count: int
    model: str | None
    source_template: str


def _ordered_frontmatter(source: Mapping[str, Any], permission: dict[str, Any]) -> dict[str, Any]:
    frontmatter: dict[str, Any] = {}
    for key in _FRONTMATTER_ORDER:
        value = source.get(key)
        if value is not None:
            frontmatter[key] = value

    for key, value in source.items():
        if key in frontmatter or key == "system":
            continue
        if value is not None:
            frontmatter[key] = value

    frontmatter["permission"] = permission
    return frontmatter


def _split_markdown_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ValueError("Generated markdown agent is missing YAML frontmatter")
    end_idx = text.find("\n---\n", 4)
    if end_idx == -1:
        raise ValueError("Generated markdown agent is missing closing YAML frontmatter marker")
    frontmatter = yaml.safe_load(text[4:end_idx]) or {}
    body = text[end_idx + len("\n---\n"):].lstrip("\n")
    return frontmatter, body


def _encoding_for_model(model: str | None):
    candidates: list[str] = []
    if model:
        candidates.append(model)
        tail = model.split("/", 1)[-1]
        candidates.append(tail)
        if ":" in tail:
            candidates.append(tail.split(":", 1)[0])

    seen: set[str] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        try:
            return tiktoken.encoding_for_model(candidate)
        except KeyError:
            continue
    return tiktoken.get_encoding(DEFAULT_PROMPT_TOKEN_ENCODING)


def count_prompt_tokens(prompt_body: str, model: str | None = None) -> int:
    """Count tokens for a rendered prompt body."""
    encoding = _encoding_for_model(model)
    return len(encoding.encode(prompt_body))


def render_agent_artifact(agent: Agent) -> GeneratedAgentArtifact:
    """Render one managed agent into a build artifact."""
    template = load_micro_agent(agent.prompt_template)
    frontmatter = _ordered_frontmatter(template.frontmatter, agent.compile())
    body = template.render().rstrip()
    dumped = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=False).strip()
    markdown = f"---\n{dumped}\n---\n"
    if body:
        markdown = f"{markdown}\n{body}\n"
    return GeneratedAgentArtifact(
        name=agent.name,
        output_filename=agent.output_filename,
        markdown=markdown,
        prompt_body=body,
        frontmatter=frontmatter,
        token_count=count_prompt_tokens(body, frontmatter.get("model")),
        model=frontmatter.get("model"),
        source_template=agent.prompt_template,
    )


def load_static_markdown_artifact(template_path: str, output_name: str) -> GeneratedAgentArtifact:
    """Load a static markdown template into a build artifact."""
    source = resolve_prompt_path(template_path)
    markdown = source.read_text()
    frontmatter, body = _split_markdown_frontmatter(markdown)
    return GeneratedAgentArtifact(
        name=Path(output_name).stem,
        output_filename=output_name,
        markdown=markdown,
        prompt_body=body.rstrip(),
        frontmatter=frontmatter,
        token_count=count_prompt_tokens(body.rstrip(), frontmatter.get("model")),
        model=frontmatter.get("model"),
        source_template=template_path,
    )


def render_agent_markdown(agent: Agent) -> str:
    """Render a managed agent into the OpenCode markdown-agent format."""
    return render_agent_artifact(agent).markdown


def write_agent_markdown(agent: Agent, output_dir: str | Path) -> Path:
    """Write one generated markdown agent file."""
    artifact = render_agent_artifact(agent)
    return write_markdown_artifact(artifact, output_dir)


def write_markdown_artifact(artifact: GeneratedAgentArtifact, output_dir: str | Path) -> Path:
    """Write a generated markdown artifact into the runtime agents directory."""
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    output_path = target_dir / artifact.output_filename
    output_path.write_text(artifact.markdown)
    return output_path


def write_static_markdown_template(
    template_path: str,
    output_name: str,
    output_dir: str | Path,
) -> Path:
    """Copy a static upstream-shadow template into the runtime agents directory."""
    artifact = load_static_markdown_artifact(template_path, output_name)
    return write_markdown_artifact(artifact, output_dir)
