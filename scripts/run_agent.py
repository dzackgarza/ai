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
from typing import Optional, Protocol
from functools import cached_property

import yaml
from jinja2 import Template
import litellm
from pydantic import BaseModel


class ModelsDevSource(BaseModel):
    """Models fetched from models.dev API."""
    data: dict

    def get_models(self, slug: str) -> list[str]:
        """Get model IDs for a provider slug."""
        if slug not in self.data:
            return []
        return list(self.data[slug].get('models', {}).keys())


class Provider(Protocol):
    """Protocol for provider implementations."""

    env_var: str
    litellm_prefix: str
    api_base: Optional[str]
    drop_params: bool

    def get_models(self) -> list[str]:
        """Get available models for this provider."""
        ...


class ModelsDevProvider(BaseModel):
    """Provider that fetches models from models.dev API."""
    env_var: str
    litellm_prefix: str
    models_dev_slug: str
    api_base: Optional[str] = None
    drop_params: bool = False
    models_dev: ModelsDevSource

    def get_models(self) -> list[str]:
        """Get models from models.dev for this provider's slug."""
        return self.models_dev.get_models(self.models_dev_slug)


class ReplicateProvider(BaseModel):
    """Replicate provider - fetches models from Replicate API."""
    env_var: str = 'REPLICATE_API_TOKEN'
    litellm_prefix: str = 'replicate'
    api_base: Optional[str] = None
    drop_params: bool = False

    def get_models(self) -> list[str]:
        """Get models from Replicate API."""
        # Replicate doesn't have a simple model listing API
        # Return empty list - validation will pass through
        return []


def fetch_models_dev() -> ModelsDevSource:
    """Fetch models.dev API data."""
    req = Request('https://models.dev/api.json', headers={'User-Agent': 'micro-agent-runner'})
    with urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    return ModelsDevSource(data=data)


# Provider registry - populated at runtime
PROVIDERS: dict[str, ModelsDevProvider | ReplicateProvider] = {}


def init_providers() -> None:
    """Initialize provider registry with models.dev data."""
    models_dev = fetch_models_dev()

    PROVIDERS.update({
        'groq': ModelsDevProvider(
            env_var='GROQ_API_KEY',
            litellm_prefix='groq',
            models_dev_slug='groq',
            models_dev=models_dev,
        ),
        'openrouter': ModelsDevProvider(
            env_var='OPENROUTER_API_KEY',
            litellm_prefix='openrouter',
            models_dev_slug='openrouter',
            models_dev=models_dev,
        ),
        'mistral': ModelsDevProvider(
            env_var='MISTRAL_API_KEY',
            litellm_prefix='mistral',
            models_dev_slug='mistral',
            models_dev=models_dev,
        ),
        'replicate': ReplicateProvider(),
        'cloudflare-workers-ai': ModelsDevProvider(
            env_var='CLOUDFLARE_API_KEY',
            litellm_prefix='cloudflare',
            models_dev_slug='cloudflare-workers-ai',
            drop_params=True,
            models_dev=models_dev,
        ),
        'ollama-cloud': ModelsDevProvider(
            env_var='OLLAMA_API_KEY',
            litellm_prefix='ollama',
            models_dev_slug='ollama-cloud',
            api_base='https://ollama.com',
            models_dev=models_dev,
        ),
        'nvidia': ModelsDevProvider(
            env_var='NVIDIA_NIM_API_KEY',
            litellm_prefix='nvidia_nim',
            models_dev_slug='nvidia',
            models_dev=models_dev,
        ),
    })


def validate_model(model_slug: str) -> None:
    """Validate model slug and API key. Exit on error."""
    if '/' not in model_slug:
        print(f"Error: Invalid model format '{model_slug}'. Expected: provider/model", file=sys.stderr)
        sys.exit(1)

    provider_name, model_id = model_slug.split('/', 1)

    if provider_name not in PROVIDERS:
        print(f"Error: Unsupported provider '{provider_name}'", file=sys.stderr)
        print(f"Supported: {', '.join(PROVIDERS.keys())}", file=sys.stderr)
        sys.exit(1)

    provider = PROVIDERS[provider_name]

    if not os.environ.get(provider.env_var):
        print(f"Error: {provider.env_var} not set", file=sys.stderr)
        print(f"Set: export {provider.env_var}=your-key", file=sys.stderr)
        sys.exit(1)

    # Get available models for this provider
    available_models = provider.get_models()

    # Skip validation if provider doesn't have model list (e.g., replicate)
    if not available_models:
        return

    if model_id not in available_models:
        print(f"Error: Model '{model_slug}' not found", file=sys.stderr)
        print(f"Available models for {provider_name}:", file=sys.stderr)
        for m in available_models[:20]:  # Limit output
            print(f"  {provider_name}/{m}", file=sys.stderr)
        if len(available_models) > 20:
            print(f"  ... and {len(available_models) - 20} more", file=sys.stderr)
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


def get_completion(model: str, messages: list[dict], temperature: float, provider_name: str) -> str:
    """Get completion from LLM provider."""
    provider = PROVIDERS[provider_name]

    # Apply provider-specific settings
    if provider.drop_params:
        litellm.drop_params = True

    # Build litellm model string
    model_id = model.split('/', 1)[1]
    litellm_model = f"{provider.litellm_prefix}/{model_id}"

    # Build completion kwargs
    completion_kwargs = {
        'model': litellm_model,
        'messages': messages,
        'temperature': temperature,
    }

    if provider.api_base:
        completion_kwargs['api_base'] = provider.api_base

    response = litellm.completion(**completion_kwargs)
    return response.choices[0].message.content


def list_all_models() -> None:
    """List all available models from all providers."""
    for provider_name, provider in PROVIDERS.items():
        models = provider.get_models()
        for model_id in models:
            print(f"{provider_name}/{model_id}")


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

    # Initialize providers (fetches models.dev once)
    init_providers()

    # List models mode
    if args.models:
        list_all_models()
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

    # Validate model
    validate_model(model)

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
    provider_name = model.split('/', 1)[0]
    temperature = args.temperature if args.temperature is not None else frontmatter.get('temperature', 0.0)
    result = get_completion(model, messages, temperature, provider_name)

    # Output result
    if args.output == '-':
        print(result)
    else:
        Path(args.output).write_text(result)


if __name__ == '__main__':
    main()
