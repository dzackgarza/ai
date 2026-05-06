from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from src.agent_markdown import get_prompt
from llm_templating_engine import (
    Bindings,
    RenderTemplateRequest,
    TemplateReference,
    load_template_document,
    render_body,
    render_template,
)
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT.parent.parent
VENV_PYTHON = WORKSPACE_ROOT / "opencode" / ".venv" / "bin" / "python"
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


def _run_llm_run(request: dict[str, object]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["uv", "run", "--python", str(VENV_PYTHON), "llm-run"],
        check=True,
        capture_output=True,
        text=True,
        input=json.dumps(request),
        cwd=str(WORKSPACE_ROOT),
    )


def test_llm_run_returns_run_response_for_plain_text_prompt(tmp_path: Path) -> None:
    prompt = tmp_path / "plain-text.md"
    prompt.write_text(
        "---\n"
        "description: plain text test\n"
        "kind: llm-run\n"
        "models:\n"
        "  - groq/llama-3.3-70b-versatile\n"
        "temperature: 0.0\n"
        "system_template:\n"
        "  text: |\n"
        "    Reply with exactly OK and nothing else.\n"
        "inputs:\n"
        "  - name: prompt\n"
        "    required: true\n"
        "---\n"
        "{{ prompt }}\n"
    )

    proc = _run_llm_run(
        {
            "template": {"path": str(prompt)},
            "bindings": {"data": {"prompt": "Say OK."}},
            "overrides": {},
        }
    )
    payload = json.loads(proc.stdout)

    assert payload["response"]["raw_text"].strip() == "OK"
    assert payload["final_output"]["text"].strip() == "OK"


def test_llm_run_returns_structured_run_response() -> None:
    prompt = get_prompt("micro-agents/prompt-difficulty-classifier")

    proc = _run_llm_run(
        {
            "template": {"text": prompt.text, "name": prompt.slug},
            "bindings": {
                "data": {
                    "prompt": "Describe every tool you have access to.",
                }
            },
            "overrides": {},
        }
    )
    payload = json.loads(proc.stdout)

    assert payload["response"]["structured"]["tier"] == "model-self"
    assert payload["final_output"]["data"]["tier"] == "model-self"
    assert "AI" in payload["response"]["structured"]["reasoning"]


def test_ai_prompts_returns_opencode_general_prompt() -> None:
    prompt = get_prompt("sub-agents/opencode-general")

    assert prompt.frontmatter["description"].startswith("General-purpose agent")
    assert prompt.frontmatter["mode"] == "subagent"
    assert prompt.body == ""
    assert prompt.slug == "sub-agents/opencode-general"


def test_micro_agent_render_supports_frontmatter_aware_include(tmp_path: Path) -> None:
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
        rendered = render_template(
            RenderTemplateRequest(
                template=TemplateReference(path=str(parent)),
                bindings=Bindings(data={"name": "Ada"}),
            )
        ).rendered.body
    finally:
        if original_prompts_dir is None:
            os.environ.pop("PROMPTS_DIR", None)
        else:
            os.environ["PROMPTS_DIR"] = original_prompts_dir

    assert rendered == "parent -> child says Ada"


def test_render_body_supports_frontmatter_aware_macro_import(tmp_path: Path) -> None:
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
        template = load_template_document(TemplateReference(path=str(parent)))
        rendered = render_body(
            template.body_template,
            template_name=template.path,
            bindings={"name": "Ada"},
        )
    finally:
        if original_prompts_dir is None:
            os.environ.pop("PROMPTS_DIR", None)
        else:
            os.environ["PROMPTS_DIR"] = original_prompts_dir

    assert rendered == "ADA"


def test_render_agent_markdown_inlines_child_prompt_body_only(tmp_path: Path) -> None:
    from src.agent_markdown import render_agent_markdown
    from agents.primary.ralph_planner import AGENT

    rendered = render_agent_markdown(AGENT)

    frontmatter, body = _split_markdown_frontmatter(rendered)
    assert frontmatter["description"].startswith("Collaborative loop builder")
    assert frontmatter["mode"] == "primary"
    assert frontmatter["model"] == "github-copilot/gpt-4.1"
    assert "Ralph Command Standards" in body
    assert "{% include" not in body


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
