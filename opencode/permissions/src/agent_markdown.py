"""Minimal stub: get_prompt fetches a prompt entry by slug from ai-prompts."""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path


_AI_PROMPTS_PKG = "git+https://github.com/dzackgarza/ai-prompts"


@dataclass(frozen=True)
class _PromptEntry:
    text: str
    frontmatter: dict
    body: str


def get_prompt(slug: str) -> _PromptEntry:
    """Fetch a prompt by slug. Tries local library first, then uvx."""
    try:
        import sys

        _AI_PROMPTS_ROOT = (
            Path(__file__).resolve().parents[3] / "opencode-plugins" / "ai-prompts"
        )
        _AI_PROMPTS_SRC = _AI_PROMPTS_ROOT / "src"

        if _AI_PROMPTS_SRC.exists():
            if str(_AI_PROMPTS_SRC) not in sys.path:
                sys.path.insert(0, str(_AI_PROMPTS_SRC))
            if "PROMPTS_DIR" not in os.environ:
                os.environ["PROMPTS_DIR"] = str(_AI_PROMPTS_ROOT / "prompts")

            from ai_prompts import get_prompt as _get_prompt_lib

            p = _get_prompt_lib(slug)
            return _PromptEntry(text=p.text, frontmatter=p.frontmatter, body=p.body)
    except Exception:
        pass

    result = subprocess.run(
        ["uvx", "--from", _AI_PROMPTS_PKG, "ai-prompts", "get", slug, "--json"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise ValueError(f"Unknown prompt slug: {slug}\n{result.stderr.strip()}")
    data = json.loads(result.stdout)
    return _PromptEntry(
        text=data["text"],
        frontmatter=data.get("frontmatter", {}),
        body=data.get("body", ""),
    )
