#!/usr/bin/env python3
"""
Compatibility smoke test for scripts/llm.py.

For each provider that has an API key set, runs a Classification call on a
fixed test prompt and verifies the response parses correctly.

Usage:
    .venv/bin/python scripts/test_llm_compat.py

Exit code 0 = all tested providers passed.
Exit code 1 = at least one failure.

Run this after any change to llm.py, before deploying to production.
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

# Allow running from repo root without installing the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.llm import PROVIDERS, Classification, call_llm, load_template  # noqa: E402

# ---------------------------------------------------------------------------
# Fixed test probe — consistent across all runs
# ---------------------------------------------------------------------------

TEST_PROMPT = "What is the latest stable release of TypeScript?"
EXPECTED_TIER = "knowledge"

# Representative model per provider (override with env var SMOKE_MODEL=slug)
PROBE_MODELS: dict[str, str] = {
    "groq": "groq/llama-3.3-70b-versatile",
    "nvidia": "nvidia/mistralai/mistral-small-3.1-24b-instruct-2503",
    "openrouter": "arcee-ai/trinity-large-preview:free",
    "ollama": "ollama/llama3.2",
}


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------


async def probe(provider: str, slug: str, playbook: str) -> tuple[bool, str]:
    """Return (passed, message)."""
    try:
        result = await call_llm(
            slug,
            [
                {"role": "system", "content": playbook},
                {
                    "role": "user",
                    "content": f"Classify the following prompt:\n\n===\n{TEST_PROMPT}\n===",
                },
            ],
            schema=Classification,
            temperature=0,
            max_tokens=200,
        )
        if not isinstance(result, Classification):
            return False, f"unexpected result type: {type(result)}"
        if result.tier == EXPECTED_TIER:
            return True, f"tier={result.tier!r}"
        return (
            False,
            f"wrong tier: expected {EXPECTED_TIER!r} got {result.tier!r} | reasoning: {result.reasoning[:80]}",
        )
    except Exception as exc:
        return False, str(exc)


async def main() -> int:
    playbook = load_template("classifier/playbook")

    # Respect env override
    if override := os.environ.get("SMOKE_MODEL"):
        prefix = override.split("/")[0]
        probe_list = [(prefix, override)]
    else:
        probe_list = [
            (p, slug)
            for p, slug in PROBE_MODELS.items()
            if p == "ollama" or os.environ.get(PROVIDERS[p].env_var or "", "")
        ]

    if not probe_list:
        print("No providers with API keys set. Set GROQ_API_KEY, NVIDIA_API_KEY,")
        print("OPENROUTER_API_KEY, or use SMOKE_MODEL=slug to force a provider.")
        return 0

    results: list[tuple[str, str, bool, str]] = []
    for provider, slug in probe_list:
        print(f"  {slug} ... ", end="", flush=True)
        passed, msg = await probe(provider, slug, playbook)
        status = "PASS" if passed else "FAIL"
        print(f"{status} — {msg}")
        results.append((provider, slug, passed, msg))

    passed_count = sum(1 for _, _, p, _ in results if p)
    total = len(results)
    print(f"\n{passed_count}/{total} passed")
    return 0 if passed_count == total else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
