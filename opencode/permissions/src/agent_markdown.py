"""Generate OpenCode markdown agent files from prompt templates."""
from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

from scripts.llm import load_micro_agent

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


def render_agent_markdown(agent: Agent) -> str:
    """Render a managed agent into the OpenCode markdown-agent format."""
    template = load_micro_agent(agent.prompt_template)
    frontmatter = _ordered_frontmatter(template.frontmatter, agent.compile())
    body = template.render().rstrip()
    dumped = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=False).strip()
    if body:
        return f"---\n{dumped}\n---\n\n{body}\n"
    return f"---\n{dumped}\n---\n"


def write_agent_markdown(agent: Agent, output_dir: str | Path) -> Path:
    """Write one generated markdown agent file."""
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    output_path = target_dir / agent.output_filename
    output_path.write_text(render_agent_markdown(agent))
    return output_path
