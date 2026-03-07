"""
Core LLM call logic — pydantic-ai-backed structured output with fallback.

This is the single call surface for all LLM invocations in the workspace.
Plain-text completion (no schema) is supported; pass schema=None.

CLI:
    python -m scripts.llm.call <model-slug> <prompt>
    # e.g. python -m scripts.llm.call groq/llama-3.3-70b-versatile "Classify: hello"
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, TypeVar

from pydantic import BaseModel
from pydantic_ai import Agent

from scripts.llm.providers import make_model, resolve, api_key

logger = logging.getLogger(__name__)

OutputT = TypeVar("OutputT", bound=BaseModel)


async def call_llm(
    model_slug: str,
    messages: list[dict[str, str]],
    schema: type[OutputT] | None = None,
    temperature: float = 0.0,
    max_tokens: int = 500,
    retries: int = 3,
) -> OutputT | str:
    """Call one model. Returns a pydantic model instance or plain string.

    Raises on API error or schema parse failure after retries exhausted.
    """
    cfg, model_id = resolve(model_slug)
    key = api_key(cfg)
    if not key and cfg.env_var is not None:
        raise ValueError(f"{cfg.env_var} not set (required for {model_slug})")

    model = make_model(cfg, model_id, model_slug)
    output_type: Any = schema if schema is not None else str

    # Extract system prompt; concatenate remaining messages into prompt string
    system: str | None = None
    user_parts: list[str] = []
    for msg in messages:
        if msg.get("role") == "system":
            system = msg["content"]
        elif msg.get("content"):
            user_parts.append(msg["content"])
    prompt = "\n\n".join(user_parts)

    agent: Agent[None, Any] = Agent(
        model,
        output_type=output_type,
        system_prompt=system or "",
        retries=retries,
    )

    result = await agent.run(prompt)
    return result.output


async def call_with_fallback(
    model_slugs: list[str],
    messages: list[dict[str, str]],
    schema: type[OutputT] | None = None,
    temperature: float = 0.0,
    max_tokens: int = 500,
    retries: int = 3,
) -> OutputT | str:
    """Try each model in order; return the first success. Raises if all fail."""
    last_exc: Exception | None = None
    for slug in model_slugs:
        cfg, _ = resolve(slug)
        if api_key(cfg) == "" and cfg.env_var is not None:
            logger.debug("Skipping %s: %s not set", slug, cfg.env_var)
            continue
        try:
            return await call_llm(
                slug,
                messages,
                schema=schema,
                temperature=temperature,
                max_tokens=max_tokens,
                retries=retries,
            )
        except Exception as exc:
            logger.warning("Model %s failed: %s", slug, exc)
            last_exc = exc
    raise RuntimeError(f"All models failed. Last error: {last_exc}") from last_exc


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(
            "Usage: python -m scripts.llm.call <model-slug> <prompt>", file=sys.stderr
        )
        sys.exit(1)

    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
    slug = sys.argv[1]
    prompt_text = sys.argv[2]
    result = asyncio.run(call_llm(slug, [{"role": "user", "content": prompt_text}]))
    print(result)
