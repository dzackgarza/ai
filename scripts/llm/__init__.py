"""
scripts.llm — canonical LLM package for the ai/ workspace.

Public API (import these; don't import submodules directly unless needed):

    from scripts.llm import call_llm, call_with_fallback
    from scripts.llm import load_micro_agent, render_body
    from scripts.llm import PROVIDERS, SCHEMAS
    from scripts.llm import Classification   # convenience re-export

Provider slug conventions:
    groq/<model>            → Groq
    openrouter/<model>      → OpenRouter (also bare slugs)
    nvidia/<model>          → NVIDIA NIM
    mistral/<model>         → Mistral
    replicate/<model>       → Replicate
    cloudflare/<model>      → Cloudflare Workers AI
    ollama/<model>          → Local Ollama (no auth)
    ollama-cloud/<model>    → Ollama Cloud

Subprocess bridge (for TypeScript callers):
    python -m scripts.llm.bridge
"""

from scripts.llm.call import call_llm, call_with_fallback
from scripts.llm.providers import PROVIDERS, list_models, validate
from scripts.llm.schemas import SCHEMAS, Classification, resolve_schema
from scripts.llm.templates import (
    MissingVariablesError,
    TemplateFormatError,
    default_prompts_dir,
    load_micro_agent,
    render_body,
    resolve_prompt_path,
)

__all__ = [
    "call_llm",
    "call_with_fallback",
    "load_micro_agent",
    "render_body",
    "MissingVariablesError",
    "TemplateFormatError",
    "default_prompts_dir",
    "PROVIDERS",
    "list_models",
    "validate",
    "SCHEMAS",
    "Classification",
    "resolve_schema",
    "resolve_prompt_path",
]
