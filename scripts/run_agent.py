#!/usr/bin/env python3
"""
Micro-agent runner using Jinja2 templates with YAML frontmatter.
"""

import sys
import os
import argparse
import re
from pathlib import Path
from urllib.request import urlopen, Request
import json
from typing import Optional

import yaml
from jinja2 import Template
import litellm
from pydantic import BaseModel


class ProviderConfig(BaseModel):
    """Configuration for a single LLM provider."""
    env_var: str
    models_dev_slug: Optional[str] = None  # None if not on models.dev
    litellm_prefix: str
    api_base: Optional[str] = None
    drop_params: bool = False


# Provider configurations - user-facing slug is the dict key
PROVIDERS = {
    'groq': ProviderConfig(
        env_var='GROQ_API_KEY',
        models_dev_slug='groq',
        litellm_prefix='groq',
    ),
    'openrouter': ProviderConfig(
        env_var='OPENROUTER_API_KEY',
        models_dev_slug='openrouter',
        litellm_prefix='openrouter',
    ),
    'mistral': ProviderConfig(
        env_var='MISTRAL_API_KEY',
        models_dev_slug='mistral',
        litellm_prefix='mistral',
    ),
    'replicate': ProviderConfig(
        env_var='REPLICATE_API_TOKEN',
        models_dev_slug=None,  # Not on models.dev
        litellm_prefix='replicate',
    ),
    'cloudflare-workers-ai': ProviderConfig(
        env_var='CLOUDFLARE_API_KEY',
        models_dev_slug='cloudflare-workers-ai',
        litellm_prefix='cloudflare',
        drop_params=True,
    ),
    'ollama-cloud': ProviderConfig(
        env_var='OLLAMA_API_KEY',
        models_dev_slug='ollama-cloud',
        litellm_prefix='ollama',
        api_base='https://ollama.com',
    ),
    'nvidia': ProviderConfig(
        env_var='NVIDIA_NIM_API_KEY',
        models_dev_slug='nvidia',
        litellm_prefix='nvidia_nim',
    ),
}


def fetch_models_dev() -> dict:
    """Fetch models.dev API data."""
    req = Request('https://models.dev/api.json', headers={'User-Agent': 'micro-agent-runner'})
    with urlopen(req) as resp:
        return json.loads(resp.read().decode())


def validate_model(model_slug: str, models_dev: dict) -> None:
    """Validate model slug and API key. Exit on error."""
    if '/' not in model_slug:
        print(f"Error: Invalid model format '{model_slug}'. Expected: provider/model", file=sys.stderr)
        sys.exit(1)

    provider, model_id = model_slug.split('/', 1)

    if provider not in PROVIDERS:
        print(f"Error: Unsupported provider '{provider}'", file=sys.stderr)
        print(f"Supported: {', '.join(PROVIDERS.keys())}", file=sys.stderr)
        sys.exit(1)

    config = PROVIDERS[provider]

    if not os.environ.get(config.env_var):
        print(f"Error: {config.env_var} not set", file=sys.stderr)
        print(f"Set: export {config.env_var}=your-key", file=sys.stderr)
        sys.exit(1)

    # Skip models.dev validation for providers not listed there
    if config.models_dev_slug is None:
        return

    if config.models_dev_slug not in models_dev:
        print(f"Error: Provider '{config.models_dev_slug}' not found in models.dev", file=sys.stderr)
        sys.exit(1)

    if model_id not in models_dev[config.models_dev_slug]['models']:
        print(f"Error: Model '{model_slug}' not found", file=sys.stderr)
        print(f"Available models for {config.models_dev_slug}:", file=sys.stderr)
        for m in models_dev[config.models_dev_slug]['models']:
            print(f"  {config.models_dev_slug}/{m}", file=sys.stderr)
        sys.exit(1)


def parse_template(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter + template body."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return {}, content
    return yaml.safe_load(match.group(1)), match.group(2)


def build_variables(file_args: list[str], var_args: list[str]) -> dict:
    """Build variables from --file and --var arguments."""
    variables = {}

    for file_arg in file_args:
        if '=' not in file_arg:
            print(f"Error: Invalid --file format: {file_arg}", file=sys.stderr)
            sys.exit(1)
        key, path = file_arg.split('=', 1)
        content = Path(path.strip()).expanduser().read_text()
        variables[key.strip()] = variables.get(key, '') + ('\n\n===\n\n' if key in variables else '') + content

    for var_arg in var_args:
        if '=' not in var_arg:
            print(f"Error: Invalid --var format: {var_arg}", file=sys.stderr)
            sys.exit(1)
        key, value = var_arg.split('=', 1)
        variables[key.strip()] = value.strip()

    return variables


def get_completion(model: str, messages: list[dict], temperature: float, provider: str) -> str:
    """Get completion from LLM provider."""
    config = PROVIDERS[provider]

    # Apply provider-specific settings
    if config.drop_params:
        litellm.drop_params = True

    # Build litellm model string
    litellm_model = f"{config.litellm_prefix}/{model.split('/', 1)[1]}"

    # Build completion kwargs
    completion_kwargs = {
        'model': litellm_model,
        'messages': messages,
        'temperature': temperature,
    }

    if config.api_base:
        completion_kwargs['api_base'] = config.api_base

    response = litellm.completion(**completion_kwargs)
    return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description='Run a micro-agent')
    parser.add_argument('template', nargs='?', help='Template file path')
    parser.add_argument('--file', '-f', action='append', default=[], help='Load variable from file: var=path')
    parser.add_argument('--var', '-v', action='append', default=[], help='Set variable: var=value')
    parser.add_argument('--model', '-m', help='Model slug (provider/model)')
    parser.add_argument('--temperature', '-t', type=float, help='Temperature')
    parser.add_argument('--output', '-o', default='-', help='Output file')
    parser.add_argument('--models', action='store_true', help='List available models')

    args = parser.parse_args()

    # List models mode
    if args.models:
        models_dev = fetch_models_dev()
        try:
            for prov in models_dev:
                for model_id in models_dev[prov]['models']:
                    print(f"{prov}/{model_id}")
        except BrokenPipeError:
            pass
        sys.exit(0)

    if not args.template:
        print("Error: template required", file=sys.stderr)
        sys.exit(1)

    # Load and parse template
    template_file = Path(args.template).expanduser()
    if not template_file.exists():
        print(f"Error: Template not found: {template_file}", file=sys.stderr)
        sys.exit(1)

    frontmatter, template_str = parse_template(template_file.read_text())

    # Determine model (CLI override or template default)
    model = args.model or frontmatter.get('model')
    if not model:
        print("Error: --model required or 'model:' in template", file=sys.stderr)
        sys.exit(1)

    # Fetch models.dev and validate
    models_dev = fetch_models_dev()
    validate_model(model, models_dev)

    # Build variables
    variables = build_variables(args.file, args.var)

    # Render template
    template = Template(template_str)
    prompt = template.render(**variables)

    # Build messages
    system_prompt = frontmatter.get('system')
    messages = [{"role": "user", "content": prompt}]
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})

    # Get completion
    provider = model.split('/', 1)[0]
    temperature = args.temperature if args.temperature is not None else frontmatter.get('temperature', 0.0)
    result = get_completion(model, messages, temperature, provider)

    # Output result
    if args.output == '-':
        print(result)
    else:
        Path(args.output).write_text(result)


if __name__ == '__main__':
    main()
