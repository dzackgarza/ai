from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

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
    prompt = WORKSPACE_ROOT / "prompts" / "micro_agents" / "prompt_difficulty_classifier" / "prompt.md"

    proc = _run_llm_run(
        {
            "template": {"path": str(prompt)},
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


def test_load_template_document_resolves_relative_prompt_path() -> None:
    original_prompts_dir = os.environ.get("PROMPTS_DIR")
    os.environ["PROMPTS_DIR"] = str(WORKSPACE_ROOT / "prompts")
    try:
        template = load_template_document(
            TemplateReference(path="opencode_builtin/general.md")
        )
    finally:
        if original_prompts_dir is None:
            os.environ.pop("PROMPTS_DIR", None)
        else:
            os.environ["PROMPTS_DIR"] = original_prompts_dir

    assert template.frontmatter["description"].startswith("General-purpose agent")
    assert template.frontmatter["mode"] == "subagent"
    assert template.body_template == ""
    assert Path(template.path).name == "general.md"


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
    from src.base import PureAgent

    class IncludedPromptAgent(PureAgent):
        def __init__(self, prompt_template: str) -> None:
            super().__init__(prompt_template=prompt_template)

        @property
        def name(self) -> str:
            return "Included Prompt Agent"

        def permission_layers(self) -> list[dict]:
            return [{"bash": "allow"}]

    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "child.md").write_text(
        "---\n"
        "description: child metadata should be ignored\n"
        "mode: subagent\n"
        "model: ignored/model\n"
        "---\n"
        "child body only\n"
    )
    parent = prompts_dir / "parent.md"
    parent.write_text(
        "---\n"
        "description: parent metadata should dominate\n"
        "mode: primary\n"
        "model: test/model\n"
        "temperature: 0.2\n"
        "---\n"
        "parent start\n"
        "{% include './child.md' %}\n"
        "parent end\n"
    )

    original_prompts_dir = os.environ.get("PROMPTS_DIR")
    os.environ["PROMPTS_DIR"] = str(prompts_dir)
    try:
        rendered = render_agent_markdown(
            IncludedPromptAgent(prompt_template=str(parent))
        )
    finally:
        if original_prompts_dir is None:
            os.environ.pop("PROMPTS_DIR", None)
        else:
            os.environ["PROMPTS_DIR"] = original_prompts_dir

    frontmatter, body = _split_markdown_frontmatter(rendered)
    assert frontmatter["description"] == "parent metadata should dominate"
    assert frontmatter["mode"] == "primary"
    assert frontmatter["model"] == "test/model"
    assert frontmatter["temperature"] == 0.2
    assert frontmatter["permission"]["bash"] == "allow"
    assert "ignored/model" not in rendered
    assert "child metadata should be ignored" not in rendered
    assert body == "parent start\nchild body only\nparent end\n"


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
