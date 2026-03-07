#!/usr/bin/env python3
"""
Micro-agent runner using Jinja2 templates with YAML frontmatter.
"""

import sys
import os
import argparse
import re
import logging
from pathlib import Path
from urllib.request import urlopen, Request
import json
from typing import Optional, Protocol

import yaml
from jinja2 import Template
import litellm
from pydantic import BaseModel
import httpx


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


class Provider(Protocol):
    """Protocol for provider implementations."""
    env_var: str
    litellm_prefix: str
    api_base: Optional[str]
    drop_params: bool

    def get_models(self) -> list[str]:
        """Get available models for this provider."""
        ...


class ModelsDevFetcher:
    """Fetches models.dev API data once, provides lookup by slug."""
    
    def __init__(self):
        self._data: Optional[dict] = None
    
    @property
    def data(self) -> dict:
        if self._data is None:
            try:
                req = Request('https://models.dev/api.json', headers={'User-Agent': 'micro-agent-runner'})
                with urlopen(req) as resp:
                    self._data = json.loads(resp.read().decode())
            except Exception as e:
                logger.error(f"Failed to fetch models.dev: {e}")
                self._data = {}
        return self._data
    
    def get_models(self, slug: str) -> list[str]:
        """Get model IDs for a provider slug from models.dev."""
        if slug not in self._data:
            logger.warning(f"Provider '{slug}' not found in models.dev")
            return []
        return list(self._data[slug].get('models', {}).keys())


# Shared models.dev fetcher - fetched once at init
models_dev_fetcher = ModelsDevFetcher()


class ModelsDevProvider(BaseModel):
    """Provider that gets its model list from models.dev API."""
    env_var: str
    litellm_prefix: str
    models_dev_slug: str
    api_base: Optional[str] = None
    drop_params: bool = False

    def get_models(self) -> list[str]:
        """Get models from models.dev for this provider's slug."""
        return models_dev_fetcher.get_models(self.models_dev_slug)


class ReplicateProvider(BaseModel):
    """Replicate provider - fetches models from Replicate API."""
    env_var: str = 'REPLICATE_API_TOKEN'
    litellm_prefix: str = 'replicate'
    api_base: Optional[str] = None
    drop_params: bool = False

    def get_models(self) -> list[str]:
        """Get models from Replicate API."""
        api_key = os.environ.get(self.env_var, '')
        if not api_key:
            logger.warning("Replicate API key not set, skipping model validation")
            return []
        
        try:
            resp = httpx.get(
                'https://api.replicate.com/v1/models',
                headers={'Authorization': f'Token {api_key}'},
                timeout=5.0
            )
            resp.raise_for_status()
            data = resp.json()
            models = [f"{r['owner']}/{r['name']}" for r in data.get('results', [])]
            logger.info(f"Fetched {len(models)} models from Replicate API")
            return models
        except httpx.HTTPStatusError as e:
            logger.error(f"Replicate API returned {e.response.status_code}: {e.response.text[:200]}")
            return []
        except httpx.TimeoutException as e:
            logger.error(f"Replicate API request timed out: {e}")
            return []
        except Exception as e:
            logger.error(f"Failed to fetch Replicate models: {e}")
            return []


# Provider registry - populated at init
PROVIDERS: dict[str, Provider] = {}


def init_providers() -> None:
    """Initialize provider registry."""
    # Trigger models.dev fetch once
    models_dev_fetcher.data

    PROVIDERS.update({
        'groq': ModelsDevProvider(
            env_var='GROQ_API_KEY',
            litellm_prefix='groq',
            models_dev_slug='groq',
        ),
        'openrouter': ModelsDevProvider(
            env_var='OPENROUTER_API_KEY',
            litellm_prefix='openrouter',
            models_dev_slug='openrouter',
        ),
        'mistral': ModelsDevProvider(
            env_var='MISTRAL_API_KEY',
            litellm_prefix='mistral',
            models_dev_slug='mistral',
        ),
        'replicate': ReplicateProvider(),
        'cloudflare-workers-ai': ModelsDevProvider(
            env_var='CLOUDFLARE_API_KEY',
            litellm_prefix='cloudflare',
            models_dev_slug='cloudflare-workers-ai',
            drop_params=True,
        ),
        'ollama-cloud': ModelsDevProvider(
            env_var='OLLAMA_API_KEY',
            litellm_prefix='ollama',
            models_dev_slug='ollama-cloud',
            api_base='https://ollama.com',
        ),
        'nvidia': ModelsDevProvider(
            env_var='NVIDIA_NIM_API_KEY',
            litellm_prefix='nvidia_nim',
            models_dev_slug='nvidia',
        ),
    })


def validate_model(model_slug: str) -> None:
    """Validate model slug and API key. Exit on error."""
    if '/' not in model_slug:
        logger.error(f"Invalid model format '{model_slug}'. Expected: provider/model")
        sys.exit(1)

    provider_name, model_id = model_slug.split('/', 1)

    if provider_name not in PROVIDERS:
        logger.error(f"Unsupported provider '{provider_name}'")
        logger.error(f"Supported: {', '.join(PROVIDERS.keys())}")
        sys.exit(1)

    provider = PROVIDERS[provider_name]

    if not os.environ.get(provider.env_var):
        logger.error(f"{provider.env_var} not set")
        logger.error(f"Set: export {provider.env_var}=your-key")
        sys.exit(1)

    # Get available models for this provider
    available_models = provider.get_models()

    # Skip validation if provider doesn't have model list
    if not available_models:
        logger.warning(f"Skipping model validation for {provider_name} (no model list available)")
        return

    if model_id not in available_models:
        logger.error(f"Model '{model_slug}' not found")
        logger.error(f"Available models for {provider_name}:")
        for m in available_models[:20]:  # Limit output
            logger.error(f"  {provider_name}/{m}")
        if len(available_models) > 20:
            logger.error(f"  ... and {len(available_models) - 20} more")
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
            logger.error(f"Invalid --file format: {file_arg}")
            sys.exit(1)
        key, path = file_arg.split('=', 1)
        content = Path(path.strip()).expanduser().read_text()
        variables[key.strip()] = variables.get(key, '') + ('\n\n===\n\n' if key in variables else '') + content

    for var_arg in var_args:
        if '=' not in var_arg:
            logger.error(f"Invalid --var format: {var_arg}")
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

    logger.info(f"Calling {litellm_model} with temperature={temperature}")

    # Build completion kwargs
    completion_kwargs = {
        'model': litellm_model,
        'messages': messages,
        'temperature': temperature,
    }

    if provider.api_base:
        completion_kwargs['api_base'] = provider.api_base
        logger.debug(f"Using custom API base: {provider.api_base}")

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
    parser.add_argument('--verbose', '-V', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    # Enable debug logging if verbose
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize providers
    init_providers()

    # List models mode
    if args.models:
        list_all_models()
        sys.exit(0)

    if not args.template:
        logger.error("template required")
        sys.exit(1)

    # Load and parse template
    template_file = Path(args.template).expanduser()
    if not template_file.exists():
        logger.error(f"Template not found: {template_file}")
        sys.exit(1)

    frontmatter, template_str = parse_template(template_file.read_text())

    # Determine model (CLI override or template default)
    model = args.model or frontmatter.get('model')
    if not model:
        logger.error("--model required or 'model:' in template")
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
        logger.debug(f"System prompt: {system_prompt[:100]}...")

    # Get completion
    provider_name = model.split('/', 1)[0]
    temperature = args.temperature if args.temperature is not None else frontmatter.get('temperature', 0.0)
    result = get_completion(model, messages, temperature, provider_name)

    # Output result
    if args.output == '-':
        print(result)
    else:
        Path(args.output).write_text(result)
        logger.info(f"Output written to {args.output}")


if __name__ == '__main__':
    main()
