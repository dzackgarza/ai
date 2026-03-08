from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT.parent.parent
RUN_MICRO_AGENT = WORKSPACE_ROOT / "scripts" / "run_micro_agent.py"
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


def _run_micro_agent(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(VENV_PYTHON), str(RUN_MICRO_AGENT), *args],
        check=True,
        capture_output=True,
        text=True,
        cwd=str(WORKSPACE_ROOT),
    )


def test_run_micro_agent_wraps_plain_text_results_in_json_envelope(tmp_path: Path) -> None:
    prompt = tmp_path / "plain-text.md"
    prompt.write_text(
        "---\n"
        "description: plain text test\n"
        "model: groq/llama-3.3-70b-versatile\n"
        "temperature: 0.0\n"
        "system: |\n"
        "  Reply with exactly OK and nothing else.\n"
        "inputs:\n"
        "  - name: prompt\n"
        "    required: true\n"
        "---\n"
        "{{ prompt }}\n"
    )

    proc = _run_micro_agent(str(prompt), "--var", "prompt=Say OK.")
    payload = json.loads(proc.stdout)

    assert payload["ok"] is True
    assert payload["result"]["response"].strip() == "OK"


def test_run_micro_agent_wraps_structured_results_in_json_envelope() -> None:
    prompt = WORKSPACE_ROOT / "prompts" / "micro_agents" / "prompt_difficulty_classifier" / "prompt.md"

    proc = _run_micro_agent(
        str(prompt),
        "--var",
        "prompt=Describe every tool you have access to.",
    )
    payload = json.loads(proc.stdout)

    assert payload["ok"] is True
    assert payload["result"]["tier"] == "model-self"
    assert "AI" in payload["result"]["reasoning"]


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
        "child body for {{ name }}\n"
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
        rendered = render_agent_markdown(IncludedPromptAgent(prompt_template="parent.md"))
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
    assert body == "parent start\nchild body for \nparent end\n"


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
