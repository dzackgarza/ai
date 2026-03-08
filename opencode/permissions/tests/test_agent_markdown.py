from __future__ import annotations

import os
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
    assert template.path.name == "general.md"


def test_micro_agent_render_supports_frontmatter_aware_include(tmp_path: Path) -> None:
    from scripts.llm import load_micro_agent

    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "child.md").write_text(
        "---\n"
        "description: child metadata should be ignored\n"
        "---\n"
        "child says {{ name }}\n"
    )
    parent = prompts_dir / "parent.md"
    parent.write_text(
        "---\n"
        "description: parent prompt\n"
        "---\n"
        "parent -> {% include './child.md' %}\n"
    )

    original_prompts_dir = os.environ.get("PROMPTS_DIR")
    os.environ["PROMPTS_DIR"] = str(prompts_dir)
    try:
        template = load_micro_agent(parent)
        rendered = template.render(name="Ada")
    finally:
        if original_prompts_dir is None:
            os.environ.pop("PROMPTS_DIR", None)
        else:
            os.environ["PROMPTS_DIR"] = original_prompts_dir

    assert rendered == "parent -> child says Ada"


def test_render_body_supports_frontmatter_aware_macro_import(tmp_path: Path) -> None:
    from scripts.llm import render_body

    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "macros.md").write_text(
        "---\n"
        "description: child metadata should be ignored\n"
        "---\n"
        "{% macro shout(value) -%}{{ value | upper }}{%- endmacro %}\n"
    )
    parent = prompts_dir / "parent.md"
    parent.write_text(
        "---\n"
        "description: parent prompt\n"
        "---\n"
        "{% from './macros.md' import shout %}{{ shout(name) }}\n"
    )

    original_prompts_dir = os.environ.get("PROMPTS_DIR")
    os.environ["PROMPTS_DIR"] = str(prompts_dir)
    try:
        rendered = render_body(
            parent.read_text(),
            template_path=parent,
            name="Ada",
        )
    finally:
        if original_prompts_dir is None:
            os.environ.pop("PROMPTS_DIR", None)
        else:
            os.environ["PROMPTS_DIR"] = original_prompts_dir

    assert rendered == "ADA"


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
