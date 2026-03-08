from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.base import PureAgent
from src.rulesets.orchestrator import Orchestrator


class OrchestratorCustomAgent(PureAgent):
    @property
    def name(self) -> str:
        return "Orchestrator (Custom)"

    def permission_layers(self) -> list[dict]:
        return Orchestrator.layers()

    @property
    def overrides(self) -> dict:
        return {"write_plan": "deny"}


AGENT = OrchestratorCustomAgent("interactive_agents/orchestrator.md")
