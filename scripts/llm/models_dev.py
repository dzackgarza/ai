"""
models.dev API fetcher.

Fetches the models.dev provider+model catalogue once (lazily) and provides
per-provider model-list lookup. Used by ModelsDevProvider in providers.py
to validate model slugs and enumerate available models.

CLI:
    python -m scripts.llm.models_dev <provider-slug>
    # prints one model ID per line, e.g.:
    python -m scripts.llm.models_dev groq
"""

from __future__ import annotations

import json
import logging
from typing import Optional
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)


class ModelsDevFetcher:
    """Fetches models.dev API data once, provides lookup by provider slug."""

    _URL = "https://models.dev/api.json"

    def __init__(self) -> None:
        self._data: Optional[dict] = None

    @property
    def data(self) -> dict:
        if self._data is None:
            try:
                req = Request(self._URL, headers={"User-Agent": "ai-scripts/llm"})
                with urlopen(req, timeout=10) as resp:
                    self._data = json.loads(resp.read().decode())
            except Exception as exc:
                logger.error("Failed to fetch models.dev: %s", exc)
                self._data = {}
        return self._data or {}

    def get_models(self, slug: str) -> list[str]:
        """Return model IDs for a models.dev provider slug.

        Returns an empty list if the slug is not found or the fetch failed.
        """
        data = self.data
        if slug not in data:
            logger.warning("Provider %r not found in models.dev", slug)
            return []
        return list(data[slug].get("models", {}).keys())


# Module-level singleton — fetched at most once per process.
fetcher = ModelsDevFetcher()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print(
            "Usage: python -m scripts.llm.models_dev <provider-slug>", file=sys.stderr
        )
        sys.exit(1)
    for model_id in fetcher.get_models(sys.argv[1]):
        print(model_id)
