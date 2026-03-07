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

import yaml
from jinja2 import Template
import litellm


# Static provider list - matches models.dev provider slugs to env vars
# NOTE: one should restrict openrouter to free models only.
PROVIDERS = {
    'groq': 'GROQ_API_KEY',
    'openrouter': 'OPENROUTER_API_KEY',
    'mistral': 'MISTRAL_API_KEY',
    'replicate': 'REPLICATE_API_TOKEN',
    'cloudflare': 'CLOUDFLARE_API_KEY',
    'ollama': 'OLLAMA_API_KEY',
    'nvidia': 'NVIDIA_API_KEY',
}

API_KEYS = {p: os.environ.get(e) for p, e in PROVIDERS.items()}


def fetch_models_dev():
    """Fetch models.dev API data."""
    req = Request('https://models.dev/api.json', headers={'User-Agent': 'micro-agent-runner'})
    with urlopen(req) as resp:
        return json.loads(resp.read().decode())


def validate_model(model_slug, models_dev):
    """Validate model slug and API key. Exit on error."""
    if '/' not in model_slug:
        print(f"Error: Invalid model format '{model_slug}'. Expected: provider/model", file=sys.stderr)
        sys.exit(1)
    
    provider, model_id = model_slug.split('/', 1)
    
    if provider not in PROVIDERS:
        print(f"Error: Unsupported provider '{provider}'", file=sys.stderr)
        print(f"Supported: {', '.join(PROVIDERS.keys())}", file=sys.stderr)
        sys.exit(1)
    
    if not API_KEYS[provider]:
        print(f"Error: {PROVIDERS[provider]} not set", file=sys.stderr)
        print(f"Set: export {PROVIDERS[provider]}=your-key", file=sys.stderr)
        sys.exit(1)
    
    if provider not in models_dev:
        print(f"Error: Provider '{provider}' not found in models.dev", file=sys.stderr)
        sys.exit(1)
    
    if model_id not in models_dev[provider]['models']:
        print(f"Error: Model '{model_slug}' not found", file=sys.stderr)
        print(f"Available models for {provider}:", file=sys.stderr)
        for m in models_dev[provider]['models']:
            print(f"  {provider}/{m}", file=sys.stderr)
        sys.exit(1)


def parse_template(content):
    """Parse YAML frontmatter + template body."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return {}, content
    return yaml.safe_load(match.group(1)), match.group(2)


def main():
    parser = argparse.ArgumentParser(description='Run a micro-agent')
    parser.add_argument('template', nargs='?', help='Template file path')
    parser.add_argument('--file', '-f', action='append', default=[], help='Load variable from file: var=path')
    parser.add_argument('--var', '-v', action='append', default=[], help='Set variable: var=value')
    parser.add_argument('--model', '-m', help='Model slug (provider/model)')
    parser.add_argument('--temperature', '-t', type=float, help='Temperature')
    parser.add_argument('--max-tokens', type=int, help='Max tokens')
    parser.add_argument('--output', '-o', default='-', help='Output file')
    parser.add_argument('--models', action='store_true', help='List available models')
    
    args = parser.parse_args()
    
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
    variables = {}
    for file_arg in args.file:
        if '=' not in file_arg:
            print(f"Error: Invalid --file format: {file_arg}", file=sys.stderr)
            sys.exit(1)
        key, path = file_arg.split('=', 1)
        content = Path(path.strip()).expanduser().read_text()
        variables[key.strip()] = variables.get(key, '') + ('\n\n===\n\n' if key in variables else '') + content
    
    for var_arg in args.var:
        if '=' not in var_arg:
            print(f"Error: Invalid --var format: {var_arg}", file=sys.stderr)
            sys.exit(1)
        variables[var_arg.split('=', 1)[0].strip()] = var_arg.split('=', 1)[1].strip()
    
    # Render and execute
    template = Template(template_str)
    prompt = template.render(**variables)

    system_prompt = frontmatter.get('system')
    messages = [{"role": "user", "content": prompt}]
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})

    response = litellm.completion(
        model=model,
        messages=messages,
        temperature=args.temperature if args.temperature is not None else frontmatter.get('temperature', 0.0),
        max_tokens=args.max_tokens or frontmatter.get('max_tokens')
    )
    result = response.choices[0].message.content

    if args.output == '-':
        print(result)
    else:
        Path(args.output).write_text(result)


if __name__ == '__main__':
    main()
