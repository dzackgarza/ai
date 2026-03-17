from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.base import PureAgent
from src.rulesets.coordinator import Coordinator


class ZoteroLibrarianAgent(PureAgent):
    @property
    def name(self) -> str:
        return "Zotero Librarian"

    def permission_layers(self) -> list[dict]:
        return Coordinator.layers()

    @property
    def overrides(self) -> dict:
        return {
            "edit": {"*": "deny"},
            "apply_patch": {"*": "deny"},
        }


AGENT = ZoteroLibrarianAgent("interactive-agents/zotero-librarian")
