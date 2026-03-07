"""
stdin/stdout JSON bridge for TypeScript subprocess callers.

Reads a single JSON request from stdin, dispatches to call_with_fallback or
load_template, and writes a single JSON response to stdout.

Protocol (unchanged from the previous opencode/scripts/llm.py interface):

  Request (call):
    {
      "models": ["groq/llama-3.3-70b-versatile", ...],
      "messages": [{"role": "user", "content": "..."}],
      "schema": "Classification",   // optional — name from schemas.SCHEMAS
      "temperature": 0.0,           // optional, default 0.0
      "max_tokens": 500,            // optional, default 500
      "retries": 3                  // optional, default 3
    }

  Request (load_template):
    { "action": "load_template", "template": "classifier/playbook" }
    { "action": "load_template", "path": "/abs/path/to/file.md" }

  Request (load_micro_agent):
    { "action": "load_micro_agent", "path": "/abs/path/to/prompt.md" }
    Response result: { "system": "...", "body": "...", "frontmatter": {...} }

  Response (success):  { "ok": true, "result": ... }
  Response (error):    { "ok": false, "error": "..." }

CLI:
    python -m scripts.llm.bridge   # reads from stdin
    echo '{"models":["groq/llama-3.3-70b-versatile"],"messages":[{"role":"user","content":"ping"}]}' | python -m scripts.llm.bridge
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys

from pydantic import BaseModel

from scripts.llm.call import call_with_fallback
from scripts.llm.schemas import SCHEMAS
from scripts.llm.templates import load_micro_agent, load_template, render_body

logger = logging.getLogger(__name__)


async def _main() -> None:
    raw = sys.stdin.read()
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(json.dumps({"ok": False, "error": f"Invalid JSON input: {exc}"}))
        sys.exit(1)

    # ------------------------------------------------------------------
    # Action: load_template
    # ------------------------------------------------------------------
    if req.get("action") == "load_template":
        template_name: str = req.get("template", "")
        template_path: str | None = req.get("path") or None
        if not template_name and not template_path:
            print(
                json.dumps({"ok": False, "error": "No template name or path specified"})
            )
            sys.exit(1)
        try:
            content = load_template(template_name, path=template_path)
            print(json.dumps({"ok": True, "result": content}))
        except FileNotFoundError as exc:
            print(json.dumps({"ok": False, "error": str(exc)}))
            sys.exit(1)
        return

    # ------------------------------------------------------------------
    # Action: load_micro_agent
    # ------------------------------------------------------------------
    if req.get("action") == "load_micro_agent":
        agent_path: str = req.get("path", "")
        if not agent_path:
            print(
                json.dumps(
                    {"ok": False, "error": "No path specified for load_micro_agent"}
                )
            )
            sys.exit(1)
        try:
            agent = load_micro_agent(agent_path)
            print(
                json.dumps(
                    {
                        "ok": True,
                        "result": {
                            "system": agent.system,
                            "body": agent.body,
                            "frontmatter": agent.frontmatter,
                        },
                    }
                )
            )
        except FileNotFoundError as exc:
            print(json.dumps({"ok": False, "error": str(exc)}))
            sys.exit(1)
        return

    # ------------------------------------------------------------------
    # Action: render_template
    # ------------------------------------------------------------------
    if req.get("action") == "render_template":
        body: str = req.get("body", "")
        variables: dict = req.get("variables", {})
        if not body:
            print(
                json.dumps(
                    {"ok": False, "error": "No body specified for render_template"}
                )
            )
            sys.exit(1)
        try:
            rendered = render_body(body, **variables)
            print(json.dumps({"ok": True, "result": rendered}))
        except Exception as exc:
            print(json.dumps({"ok": False, "error": str(exc)}))
            sys.exit(1)
        return

    # ------------------------------------------------------------------
    # Action: call (default)
    # ------------------------------------------------------------------
    models: list[str] = req.get("models", [])
    messages: list[dict[str, str]] = req.get("messages", [])
    schema_name: str | None = req.get("schema")
    temperature: float = req.get("temperature", 0.0)
    max_tokens: int = req.get("max_tokens", 500)
    retries: int = req.get("retries", 3)

    if not models:
        print(json.dumps({"ok": False, "error": "No models specified"}))
        sys.exit(1)

    schema: type[BaseModel] | None = None
    if schema_name:
        schema = SCHEMAS.get(schema_name)
        if schema is None:
            known = list(SCHEMAS)
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": f"Unknown schema: {schema_name!r}. Known: {known}",
                    }
                )
            )
            sys.exit(1)

    try:
        result = await call_with_fallback(
            models,
            messages,
            schema=schema,
            temperature=temperature,
            max_tokens=max_tokens,
            retries=retries,
        )
        if isinstance(result, BaseModel):
            print(json.dumps({"ok": True, "result": result.model_dump()}))
        else:
            print(json.dumps({"ok": True, "result": result}))
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
    asyncio.run(_main())
