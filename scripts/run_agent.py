#!/usr/bin/env python3
"""
Micro-agent runner using Jinja2 templates with YAML frontmatter.
"""

import sys
import os
import argparse
import re
from pathlib import Path

import yaml
from jinja2 import Template
import litellm


# Provider configuration: provider -> API key env var
PROVIDERS = {
    'groq': 'GROQ_API_KEY',
    'openai': 'OPENAI_API_KEY',
    'anthropic': 'ANTHROPIC_API_KEY',
    'azure': 'AZURE_API_KEY',
    'cohere': 'COHERE_API_KEY',
    'replicate': 'REPLICATE_API_TOKEN',
    'huggingface': 'HUGGINGFACE_API_KEY',
}

# Load configured API keys at startup
API_KEYS = {provider: os.environ.get(env_var) for provider, env_var in PROVIDERS.items()}


def get_provider(model_slug):
    """Extract provider from model slug."""
    return model_slug.split('/')[0] if '/' in model_slug else None


def check_api_key(model_slug):
    """Check that API key is set for the provider."""
    provider = get_provider(model_slug)
    if not provider:
        print(f"Error: Invalid model format '{model_slug}'. Expected: provider/model", file=sys.stderr)
        sys.exit(1)
    
    if provider not in API_KEYS or not API_KEYS[provider]:
        print(f"Error: {PROVIDERS.get(provider, 'UNKNOWN')} not set", file=sys.stderr)
        print(f"Set: export {PROVIDERS.get(provider, 'UNKNOWN')}=your-key", file=sys.stderr)
        sys.exit(1)


def parse_template(content):
    """Parse YAML frontmatter + template body."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return {}, content
    
    frontmatter = yaml.safe_load(match.group(1))
    template = match.group(2)
    return frontmatter, template


def run_agent(template_path, variables, model=None, temperature=None, max_tokens=None):
    """Run a micro-agent."""
    
    template_file = Path(template_path).expanduser()
    if not template_file.exists():
        print(f"Error: Template not found: {template_file}", file=sys.stderr)
        sys.exit(1)
    
    frontmatter, template_str = parse_template(template_file.read_text())
    
    model = model or frontmatter.get('model')
    if not model:
        print("Error: --model required or 'model:' in template", file=sys.stderr)
        sys.exit(1)
    
    # Check API key before calling
    check_api_key(model)
    
    template = Template(template_str)
    prompt = template.render(**variables)
    
    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": frontmatter.get('system', 'You are a helpful assistant.')},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature if temperature is not None else frontmatter.get('temperature', 0.0),
            max_tokens=max_tokens if max_tokens else frontmatter.get('max_tokens')
        )
        return response.choices[0].message.content
    except litellm.exceptions.NotFoundError:
        print(f"Error: Model '{model}' not found", file=sys.stderr)
        provider = get_provider(model)
        if provider:
            print(f"List models: python run_agent.py --models --model {provider}/", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def list_models():
    """List available models."""
    import litellm
    for model in litellm.model_cost.keys():
        print(model)


def main():
    parser = argparse.ArgumentParser(description='Run a micro-agent')
    
    parser.add_argument('template', nargs='?', help='Template file path')
    parser.add_argument('--file', '-f', action='append', default=[], 
                        help='Load variable from file: var_name=path')
    parser.add_argument('--var', '-v', action='append', default=[], 
                        help='Set variable: var_name=value')
    parser.add_argument('--model', '-m', help='Model slug (provider/model)')
    parser.add_argument('--temperature', '-t', type=float, help='Temperature')
    parser.add_argument('--max-tokens', type=int, help='Max tokens')
    parser.add_argument('--output', '-o', default='-', help='Output file')
    parser.add_argument('--models', action='store_true', help='List available models')
    
    args = parser.parse_args()
    
    if args.models:
        list_models()
        sys.exit(0)
    
    if not args.template:
        print("Error: template required", file=sys.stderr)
        sys.exit(1)
    
    variables = {}
    for file_arg in args.file:
        if '=' not in file_arg:
            print(f"Error: Invalid --file format: {file_arg} (expected var=path)", file=sys.stderr)
            sys.exit(1)
        key, path = file_arg.split('=', 1)
        file_path = Path(path.strip()).expanduser()
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        content = file_path.read_text()
        variables[key.strip()] = variables.get(key, '') + ('\n\n===\n\n' if key in variables else '') + content
    
    for var_arg in args.var:
        if '=' not in var_arg:
            print(f"Error: Invalid --var format: {var_arg} (expected var=value)", file=sys.stderr)
            sys.exit(1)
        key, value = var_arg.split('=', 1)
        variables[key.strip()] = value.strip()
    
    result = run_agent(args.template, variables, model=args.model, 
                       temperature=args.temperature, max_tokens=args.max_tokens)
    
    if args.output == '-':
        print(result)
    else:
        Path(args.output).write_text(result)


if __name__ == '__main__':
    main()
