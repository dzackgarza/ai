"""
scripts.llm — canonical LLM package for the ai/ workspace.

Public API (import these; don't import submodules directly unless needed):

    from scripts.llm import call_llm, call_with_fallback
    from scripts.llm import load_template, render_template
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
from scripts.llm.providers import PROVIDERS
from scripts.llm.schemas import SCHEMAS, Classification
from scripts.llm.templates import load_template, render_template

__all__ = [
    "call_llm",
    "call_with_fallback",
    "load_template",
    "render_template",
    "PROVIDERS",
    "SCHEMAS",
    "Classification",
]
