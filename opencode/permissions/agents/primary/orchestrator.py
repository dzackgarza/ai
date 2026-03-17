from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.base import PureAgent
from src.rulesets.orchestrator import Orchestrator


class OrchestratorAgent(PureAgent):
    @property
    def name(self) -> str:
        return "orchestrator"

    def permission_layers(self) -> list[dict]:
        return Orchestrator.layers()

    @property
    def overrides(self) -> dict:
        return {}


AGENT = OrchestratorAgent("interactive-agents/orchestrator")
