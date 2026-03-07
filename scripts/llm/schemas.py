"""
Output schema registry.

Add a pydantic BaseModel subclass here and register it in SCHEMAS to make it
available to TS subprocess callers via schema name string.

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
