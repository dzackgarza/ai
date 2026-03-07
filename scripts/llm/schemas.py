"""
Output schema registry.

Add a pydantic BaseModel subclass here and register it in SCHEMAS to make it
available to TS subprocess callers via schema name string, and to templates
declaring a 'schema:' field in their frontmatter.

CLI:
    python -m scripts.llm.schemas          # list registered schema names
    python -m scripts.llm.schemas <name>   # print JSON schema for a registered schema
"""

from __future__ import annotations

import json

from pydantic import BaseModel


class Classification(BaseModel):
    """Tier classification for a user prompt."""

    tier: str  # "model-self" | "knowledge" | "C" | "B" | "A" | "S"
    reasoning: str


# ---------------------------------------------------------------------------
# Registry — add new schemas here
# ---------------------------------------------------------------------------

SCHEMAS: dict[str, type[BaseModel]] = {
    "Classification": Classification,
}


def resolve_schema(name: str) -> type[BaseModel] | None:
    """Return the schema class registered under name, or None if unknown.

    Used by MicroAgent.schema_class() to resolve frontmatter 'schema:' fields.
    Prefer this over direct SCHEMAS lookup so callers don't import SCHEMAS
    directly and the registry stays as a single point of change.
    """
    return SCHEMAS.get(name)


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        for name in SCHEMAS:
            print(name)
    elif len(sys.argv) == 2:
        name = sys.argv[1]
        if name not in SCHEMAS:
            print(f"Unknown schema: {name!r}. Known: {list(SCHEMAS)}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(SCHEMAS[name].model_json_schema(), indent=2))
    else:
        print("Usage: python -m scripts.llm.schemas [<name>]", file=sys.stderr)
        sys.exit(1)
