#!/usr/bin/env python3
"""
Micro-agent runner — thin CLI wrapper over scripts.llm.

Loads a micro-agent template, renders it with supplied variables, and runs it
against the model declared in the template (or a CLI override). All provider
resolution, API key validation, model listing, and LLM dispatch are handled by
the scripts.llm package; this script only owns CLI parsing and I/O.

Usage:
    python scripts/run_micro_agent.py <template> [--model provider/model]
                                       [--file var=path] [--var var=value]
                                       [--temperature T] [--output file]
    python scripts/run_micro_agent.py --models [provider]   # list available models
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
from pathlib import Path

from scripts.llm import (  # noqa: E402
    call_llm,
    list_models,
    load_micro_agent,
    resolve_prompt_path,
    validate,
)
from scripts.llm.templates import MissingVariablesError  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def fail(message: str) -> None:
    logger.error("%s", message)
    print(json.dumps({"ok": False, "error": message}))
    sys.exit(1)


# ---------------------------------------------------------------------------
# CLI variable helpers
# ---------------------------------------------------------------------------


def build_variables(file_args: list[str], var_args: list[str]) -> dict[str, str]:
    """Build variables dict from --file and --var arguments."""
    variables: dict[str, str] = {}

    for file_arg in file_args:
        if "=" not in file_arg:
            fail(f"Invalid --file format {file_arg!r} — expected var=path")
        key, path = file_arg.split("=", 1)
        content = Path(path.strip()).expanduser().read_text()
        sep = "\n\n===\n\n" if key.strip() in variables else ""
        variables[key.strip()] = variables.get(key.strip(), "") + sep + content

    for var_arg in var_args:
        if "=" not in var_arg:
            fail(f"Invalid --var format {var_arg!r} — expected var=value")
        key, value = var_arg.split("=", 1)
        variables[key.strip()] = value.strip()

    return variables


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Run a micro-agent template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("template", nargs="?", help="Path to .md template file")
    parser.add_argument(
        "--file",
        "-f",
        action="append",
        default=[],
        metavar="VAR=PATH",
        help="Load a file into a template variable",
    )
    parser.add_argument(
        "--var",
        "-v",
        action="append",
        default=[],
        metavar="VAR=VALUE",
        help="Set a template variable inline",
    )
    parser.add_argument(
        "--model",
        "-m",
        metavar="PROVIDER/MODEL",
        help="Override the model declared in the template",
    )
    parser.add_argument(
        "--temperature",
        "-t",
        type=float,
        help="Override the temperature declared in the template",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="-",
        help="Output file (default: stdout)",
    )
    parser.add_argument(
        "--models",
        nargs="?",
        const="__all__",
        metavar="PROVIDER",
        help="List available models (optionally for a specific provider) and exit",
    )
    parser.add_argument(
        "--verbose",
        "-V",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # --models listing
    if args.models is not None:
        provider = None if args.models == "__all__" else args.models
        try:
            for slug in list_models(provider):
                print(slug)
        except ValueError as exc:
            fail(str(exc))
        sys.exit(0)

    if not args.template:
        parser.print_usage(sys.stderr)
        fail("template argument required")

    template_file = resolve_prompt_path(args.template)
    if not template_file.exists():
        fail(f"Template not found: {template_file}")

    try:
        agent = load_micro_agent(template_file)
    except (ValueError, OSError) as exc:
        fail(str(exc))

    model = args.model or agent.frontmatter.get("model")
    if not model:
        fail("--model required or 'model:' must be set in template frontmatter")

    try:
        validate(model)
    except ValueError as exc:
        fail(str(exc))

    variables = build_variables(args.file, args.var)

    try:
        prompt = agent.render(**variables)
    except MissingVariablesError as exc:
        fail(str(exc))

    messages: list[dict[str, str]] = []
    if agent.system:
        messages.append({"role": "system", "content": agent.system})
    messages.append({"role": "user", "content": prompt})

    temperature: float = (
        args.temperature
        if args.temperature is not None
        else agent.frontmatter.get("temperature", 0.0)
    )

    schema = agent.schema_class()

    try:
        result = asyncio.run(
            call_llm(model, messages, schema=schema, temperature=temperature)
        )
    except (RuntimeError, ValueError) as exc:
        fail(str(exc))

    payload: dict[str, object]
    if hasattr(result, "model_dump"):
        payload = {"ok": True, "result": result.model_dump()}
    else:
        payload = {"ok": True, "result": {"response": str(result)}}
    output = json.dumps(payload, indent=2)

    if args.output == "-":
        print(output)
    else:
        Path(args.output).write_text(output)
        logger.info("Output written to %s", args.output)


if __name__ == "__main__":
    main()
