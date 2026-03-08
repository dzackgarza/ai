from __future__ import annotations

import sys
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT.parent.parent
for root in (PROJECT_ROOT, WORKSPACE_ROOT):
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))


def _split_markdown_frontmatter(text: str) -> tuple[dict, str]:
    assert text.startswith("---\n")
    end_idx = text.find("\n---\n", 4)
    assert end_idx != -1
    frontmatter = yaml.safe_load(text[4:end_idx])
    body = text[end_idx + len("\n---\n"):].lstrip("\n")
    return frontmatter, body


def test_load_micro_agent_resolves_relative_prompt_path() -> None:
    from scripts.llm import load_micro_agent

    template = load_micro_agent("opencode_builtin/general.md")

    assert template.frontmatter["description"].startswith("General-purpose agent")
    assert template.frontmatter["mode"] == "subagent"
    assert template.body == ""


def test_render_agent_markdown_embeds_template_metadata_and_permissions() -> None:
    from agents.primary.minimal import AGENT
    from src.agent_markdown import render_agent_markdown

    rendered = render_agent_markdown(AGENT)
    frontmatter, body = _split_markdown_frontmatter(rendered)

    assert frontmatter["description"] == "Matter-of-fact assistant"
    assert frontmatter["mode"] == "primary"
    assert frontmatter["model"] == "github-copilot/gpt-4.1"
    assert frontmatter["permission"]["bash"] == "allow"
    assert frontmatter["permission"]["question"] == "allow"
    assert "SYSTEM_ID: MINIMAL_MD" in body
