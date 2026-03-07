"""
Output schema registry.

Add a pydantic BaseModel subclass here and register it in SCHEMAS to make it
available to TS subprocess callers via schema name string, and to templates
declaring a 'schema:' field in their frontmatter.

Inline dict schemas:
    Templates may also declare 'schema:' as a plain YAML dict mapping field names
    to type strings (e.g. "str", "int", "float", "bool"). Call
    make_schema_from_dict(name, d) to produce a dynamic pydantic BaseModel subclass.

    Supported type strings: str, int, float, bool (default: str for unknowns).

CLI:
    python -m scripts.llm.schemas          # list registered schema names
    python -m scripts.llm.schemas <name>   # print JSON schema for a registered schema
"""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, create_model


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


# ---------------------------------------------------------------------------
# Inline dict → pydantic model factory
# ---------------------------------------------------------------------------

_TYPE_MAP: dict[str, type] = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
}


def make_schema_from_dict(name: str, fields: dict[str, Any]) -> type[BaseModel]:
    """Dynamically build a pydantic BaseModel subclass from a {field: type_str} dict.

    Supported type strings: "str", "int", "float", "bool".
    Unknown type strings default to str.

    Example:
        make_schema_from_dict("Result", {"label": "str", "score": "float"})
        → class Result(BaseModel): label: str; score: float
    """
    field_definitions: dict[str, Any] = {
        field_name: (_TYPE_MAP.get(str(type_str).lower(), str), ...)
        for field_name, type_str in fields.items()
    }
    return create_model(name, **field_definitions)


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
