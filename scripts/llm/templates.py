"""
Template loading and rendering.

Templates live in scripts/templates/ (sibling of scripts/llm/).
Callers pass names like "classifier/playbook" or "tiers/A" — no extension.

Supports Jinja2 rendering with keyword variables.

CLI:
    python -m scripts.llm.templates <name>               # print raw template
    python -m scripts.llm.templates <name> var=value ... # render with variables
"""

from __future__ import annotations

import sys
from pathlib import Path

from jinja2 import Template

# Canonical templates directory: scripts/templates/ (sibling of scripts/llm/)
_TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


def load_template(name: str) -> str:
    """Load a template by name (e.g. 'classifier/playbook', 'tiers/A').

    Searches for <name>.md then <name>.yaml then <name> (no extension).
    Raises FileNotFoundError if not found.
    """
    for ext in (".md", ".yaml", ""):
        p = _TEMPLATES_DIR / (name + ext)
        if p.exists():
            return p.read_text()
    raise FileNotFoundError(f"Template {name!r} not found in {_TEMPLATES_DIR}")


def render_template(name: str, **variables: str) -> str:
    """Load and Jinja2-render a template with the given variables."""
    content = load_template(name)
    return Template(content).render(**variables)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python -m scripts.llm.templates <name> [var=value ...]",
            file=sys.stderr,
        )
        sys.exit(1)

    name = sys.argv[1]
    variables: dict[str, str] = {}
    for arg in sys.argv[2:]:
        if "=" not in arg:
            print(f"Invalid var format: {arg!r} (expected key=value)", file=sys.stderr)
            sys.exit(1)
        k, v = arg.split("=", 1)
        variables[k.strip()] = v.strip()

    try:
        if variables:
            print(render_template(name, **variables))
        else:
            print(load_template(name))
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
