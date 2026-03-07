#!/usr/bin/env python3
"""
General-purpose micro-agent runner.

Supports PromptL-style templates with YAML frontmatter.
Uses litellm for unified provider support.
"""

import sys
import os
import argparse
import re
from pathlib import Path

import yaml
from jinja2 import Template
import litellm


def parse_promptl(content):
    """Parse PromptL format: YAML frontmatter + template."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return {}, content
    
    frontmatter = yaml.safe_load(match.group(1))
    template = match.group(2)
    return frontmatter, template


def load_template(template_path):
    """Load a PromptL template."""
    p = Path(template_path).expanduser()
    if not p.exists():
        prompt_dir = Path.home() / 'ai' / 'prompts' / 'micro_agents'
        p = prompt_dir / template_path
        if not p.exists():
            p = prompt_dir / f'{template_path}.promptl'
    
    if not p.exists():
        print(f"Error: Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)
    
    return parse_promptl(p.read_text()), p.parent


def validate_inputs(frontmatter, provided_vars):
    """Validate that required inputs are provided."""
    inputs = frontmatter.get('inputs', [])
    required = [inp['name'] for inp in inputs if inp.get('required', False)]
    
    missing = [name for name in required if name not in provided_vars]
    if missing:
        print(f"Error: Missing required inputs: {missing}", file=sys.stderr)
        sys.exit(1)


def run_agent(template_path, variables, model=None, temperature=None, max_tokens=None):
    """Run a micro-agent with the given inputs."""
    
    (frontmatter, template_str), _ = load_template(template_path)
    
    # Determine model
    if model:
        model_slug = model
    else:
        model_slug = frontmatter.get('model')
    
    if not model_slug:
        print("Error: No model specified. Use --model or set 'model:' in template.", file=sys.stderr)
        sys.exit(1)
    
    # Validate inputs
    validate_inputs(frontmatter, variables)
    
    # Render template
    template = Template(template_str)
    prompt = template.render(**variables)
    
    # Call LLM via litellm
    try:
        response = litellm.completion(
            model=model_slug,
            messages=[
                {"role": "system", "content": frontmatter.get('system', 'You are a helpful assistant.')},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature if temperature is not None else frontmatter.get('temperature', 0.0),
            max_tokens=max_tokens if max_tokens else frontmatter.get('max_tokens')
        )
        return response.choices[0].message.content
    except litellm.exceptions.AuthenticationError as e:
        print(f"Error: Authentication failed for {model_slug}. Check API key.", file=sys.stderr)
        print(f"Required env vars: {get_required_env_vars(model_slug)}", file=sys.stderr)
        sys.exit(1)
    except litellm.exceptions.NotFoundError as e:
        print(f"Error: Model '{model_slug}' not found.", file=sys.stderr)
        print(f"\nTip: Check model name or run 'python run_agent.py --models --model {model_slug.split('/')[0]}/'", file=sys.stderr)
        sys.exit(1)
    except litellm.exceptions.BadRequestError as e:
        print(f"Error: Invalid request for {model_slug}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def get_required_env_vars(model_slug):
    """Get required env vars for a model (litellm handles this)."""
    provider = model_slug.split('/')[0] if '/' in model_slug else 'unknown'
    env_map = {
        'groq': 'GROQ_API_KEY',
        'openai': 'OPENAI_API_KEY',
        'anthropic': 'ANTHROPIC_API_KEY',
        'azure': 'AZURE_API_KEY',
        'cohere': 'COHERE_API_KEY',
        'replicate': 'REPLICATE_API_TOKEN',
        'huggingface': 'HUGGINGFACE_API_KEY',
    }
    return env_map.get(provider, f'{provider.upper()}_API_KEY')


def list_models(provider):
    """List available models for a provider."""
    try:
        if provider == 'groq':
            from groq import Groq
            client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
            models = client.models.list()
            print(f"Available models for {provider}:")
            for m in models.data:
                print(f"  - {provider}/{m.id}")
        else:
            print(f"Model listing not supported for {provider}. Check provider docs.", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error listing models: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Run a PromptL micro-agent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    python run_agent.py evaluator \\
        --file request=prompt.txt \\
        --file deliverable=output.txt \\
        --file reference_materials=src1.txt \\
        --file reference_materials=src2.txt

    python run_agent.py evaluator \\
        --var request="Evaluate this" \\
        --file deliverable=output.txt \\
        --model groq/llama-3.3-70b-versatile
'''
    )
    
    parser.add_argument('template', nargs='?', help='Template file or name')
    parser.add_argument('--file', '-f', action='append', default=[], 
                        help='Load variable from file: var_name=path')
    parser.add_argument('--var', '-v', action='append', default=[], 
                        help='Set variable: var_name=value')
    parser.add_argument('--model', '-m', help='Model slug (provider/model)')
    parser.add_argument('--temperature', '-t', type=float, help='Override temperature')
    parser.add_argument('--max-tokens', type=int, help='Override max tokens')
    parser.add_argument('--output', '-o', default='-', help='Output file')
    parser.add_argument('--list', action='store_true', help='List templates')
    parser.add_argument('--models', action='store_true', help='List models for provider')
    
    args = parser.parse_args()
    
    # List templates
    if args.list:
        prompt_dir = Path.home() / 'ai' / 'prompts' / 'micro_agents'
        if prompt_dir.exists():
            print("Available templates:")
            for p in sorted(prompt_dir.glob('*.promptl')):
                print(f"  - {p.stem}")
        sys.exit(0)
    
    # List models
    if args.models:
        if not args.model:
            print("Error: --models requires --model with provider (e.g., --model groq/)", file=sys.stderr)
            sys.exit(1)
        
        provider = args.model.rstrip('/').split('/')[0]
        list_models(provider)
        sys.exit(0)
    
    # Build variables
    variables = {}
    for file_arg in args.file:
        if '=' not in file_arg:
            print(f"Error: Invalid --file format: {file_arg}", file=sys.stderr)
            sys.exit(1)
        
        key, path = file_arg.split('=', 1)
        key = key.strip()
        path = Path(path.strip()).expanduser()
        
        if not path.exists():
            print(f"Error: File not found: {path}", file=sys.stderr)
            sys.exit(1)
        
        content = path.read_text()
        if key in variables:
            variables[key] = variables[key] + '\n\n===\n\n' + content
        else:
            variables[key] = content
    
    for var_arg in args.var:
        if '=' not in var_arg:
            print(f"Error: Invalid --var format: {var_arg}", file=sys.stderr)
            sys.exit(1)
        
        key, value = var_arg.split('=', 1)
        variables[key.strip()] = value.strip()
    
    # Run agent
    result = run_agent(
        args.template,
        variables,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens
    )
    
    # Write output
    if args.output == '-':
        print(result)
    else:
        Path(args.output).write_text(result)


if __name__ == '__main__':
    main()
