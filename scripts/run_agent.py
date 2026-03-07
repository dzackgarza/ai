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
    except litellm.exceptions.AuthenticationError:
        provider = model.split('/')[0] if '/' in model else 'unknown'
        env_var = f"{provider.upper()}_API_KEY"
        print(f"Error: Authentication failed for {model}", file=sys.stderr)
        print(f"Set: export {env_var}=your-key", file=sys.stderr)
        sys.exit(1)
    except litellm.exceptions.NotFoundError:
        print(f"Error: Model '{model}' not found", file=sys.stderr)
        provider = model.split('/')[0] if '/' in model else None
        if provider:
            print(f"List models: python run_agent.py --models --model {provider}/", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def list_models(provider):
    """List available models for a provider."""
    if provider == 'groq':
        from groq import Groq
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            print("Error: GROQ_API_KEY not set", file=sys.stderr)
            sys.exit(1)
        client = Groq(api_key=api_key)
        models = client.models.list()
        print(f"Available models for {provider}:")
        for m in models.data:
            print(f"  - {provider}/{m.id}")
    else:
        print(f"Model listing not supported for {provider}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Run a micro-agent')
    
    parser.add_argument('template', help='Template file path')
    parser.add_argument('--file', '-f', action='append', default=[], 
                        help='Load variable from file: var_name=path')
    parser.add_argument('--var', '-v', action='append', default=[], 
                        help='Set variable: var_name=value')
    parser.add_argument('--model', '-m', help='Model slug (provider/model)')
    parser.add_argument('--temperature', '-t', type=float, help='Temperature')
    parser.add_argument('--max-tokens', type=int, help='Max tokens')
    parser.add_argument('--output', '-o', default='-', help='Output file')
    parser.add_argument('--models', action='store_true', help='List models for provider')
    
    args = parser.parse_args()
    
    if args.models:
        if not args.model:
            print("Error: --models requires --model", file=sys.stderr)
            sys.exit(1)
        provider = args.model.split('/')[0]
        list_models(provider)
        sys.exit(0)
    
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
