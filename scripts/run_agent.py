#!/usr/bin/env python3
"""
Micro-agent runner using Jinja2 templates with YAML frontmatter.

Entry point for micro-agent execution. Delegates provider registry, model
validation, and LLM calls to the scripts.llm package.

Usage:
    python scripts/run_agent.py <template> [--model groq/llama-3.3-70b-versatile]
    python scripts/run_agent.py --models        # list all available models
"""

import sys
import argparse
import logging
from pathlib import Path

import litellm

# Allow running from repo root without installing the package.
# Must be set before the scripts.llm imports below.
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.llm.providers import PROVIDERS, resolve, api_key  # noqa: E402

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Template parsing — delegated to scripts.llm.templates
# ---------------------------------------------------------------------------
# load_micro_agent(path) returns a MicroAgent with .frontmatter, .system, .body
# and .render(**variables). Used in main() below.


def build_variables(file_args: list[str], var_args: list[str]) -> dict:
    """Build variables dict from --file and --var arguments."""
    variables: dict[str, str] = {}

    for file_arg in file_args:
        if "=" not in file_arg:
            logger.error("Invalid --file format: %s", file_arg)
            sys.exit(1)
        key, path = file_arg.split("=", 1)
        content = Path(path.strip()).expanduser().read_text()
        sep = "\n\n===\n\n" if key.strip() in variables else ""
        variables[key.strip()] = variables.get(key.strip(), "") + sep + content

    for var_arg in var_args:
        if "=" not in var_arg:
            logger.error("Invalid --var format: %s", var_arg)
            sys.exit(1)
        key, value = var_arg.split("=", 1)
        variables[key.strip()] = value.strip()

    return variables


# ---------------------------------------------------------------------------
# Completion (delegates to litellm using provider config from scripts.llm)
# ---------------------------------------------------------------------------


def validate_model(model_slug: str) -> None:
    """Validate model slug and API key availability. Exits on error."""
    if "/" not in model_slug:
        logger.error("Invalid model format %r. Expected: provider/model", model_slug)
        sys.exit(1)
    provider_prefix = model_slug.split("/", 1)[0]
    if provider_prefix not in PROVIDERS:
        logger.error(
            "Unsupported provider %r. Supported: %s",
            provider_prefix,
            ", ".join(PROVIDERS),
        )
        sys.exit(1)
    cfg = PROVIDERS[provider_prefix]
    key = api_key(cfg)
    if not key and cfg.env_var is not None:
        logger.error("%s not set. Run: export %s=your-key", cfg.env_var, cfg.env_var)
        sys.exit(1)
    available = cfg.get_models()
    if not available:
        logger.warning(
            "Skipping model validation for %s (no model list available)",
            provider_prefix,
        )
        return
    model_id = model_slug.split("/", 1)[1]
    if model_id not in available:
        sample = available[:20]
        lines = "\n  ".join(f"{provider_prefix}/{m}" for m in sample)
        extra = f"\n  ... and {len(available) - 20} more" if len(available) > 20 else ""
        logger.error("Model %r not found. Available:\n  %s%s", model_slug, lines, extra)
        sys.exit(1)


def get_completion(
    model_slug: str,
    messages: list[dict],
    temperature: float,
) -> str:
    """Plain-text LLM completion via litellm."""
    cfg, model_id = resolve(model_slug)
    if cfg.drop_params:
        litellm.drop_params = True
    litellm_model = f"{cfg.litellm_prefix}/{model_id}"
    logger.info("Calling %s with temperature=%s", litellm_model, temperature)
    kwargs: dict = {
        "model": litellm_model,
        "messages": messages,
        "temperature": temperature,
    }
    if cfg.base_url and cfg.litellm_prefix not in ("groq", "openrouter", "mistral"):
        kwargs["api_base"] = cfg.base_url
    response = litellm.completion(**kwargs)
    return response.choices[0].message.content  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# list_all_models — mirrors old behaviour
# ---------------------------------------------------------------------------


def list_all_models() -> None:
    for provider_name, cfg in PROVIDERS.items():
        for model_id in cfg.get_models():
            print(f"{provider_name}/{model_id}")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a micro-agent")
    parser.add_argument("template", nargs="?", help="Template file path")
    parser.add_argument(
        "--file", "-f", action="append", default=[], help="Load variable: var=path"
    )
    parser.add_argument(
        "--var", "-v", action="append", default=[], help="Set variable: var=value"
    )
    parser.add_argument("--model", "-m", help="Model slug (provider/model)")
    parser.add_argument("--temperature", "-t", type=float, help="Temperature")
    parser.add_argument(
        "--output", "-o", default="-", help="Output file (- for stdout)"
    )
    parser.add_argument(
        "--models", action="store_true", help="List all available models and exit"
    )
    parser.add_argument("--verbose", "-V", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.models:
        list_all_models()
        sys.exit(0)

    if not args.template:
        logger.error("template argument required")
        sys.exit(1)

    template_file = Path(args.template).expanduser()
    if not template_file.exists():
        logger.error("Template not found: %s", template_file)
        sys.exit(1)

    agent = load_micro_agent(template_file)

    model = args.model or agent.frontmatter.get("model")
    if not model:
        logger.error("--model required or 'model:' field in template frontmatter")
        sys.exit(1)

    validate_model(model)

    variables = build_variables(args.file, args.var)
    prompt = agent.render(**variables)

    messages: list[dict] = [{"role": "user", "content": prompt}]
    if agent.system:
        messages.insert(0, {"role": "system", "content": agent.system})

    temperature = (
        args.temperature
        if args.temperature is not None
        else agent.frontmatter.get("temperature", 0.0)
    )

    result = get_completion(model, messages, temperature)

    if args.output == "-":
        print(result)
    else:
        Path(args.output).write_text(result)
        logger.info("Output written to %s", args.output)


if __name__ == "__main__":
    main()
