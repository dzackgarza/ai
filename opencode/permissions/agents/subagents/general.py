import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.base import Subagent
from src.rulesets.researcher import Researcher


class GeneralAgent(Subagent):
    @property
    def name(self) -> str:
        return "general"

    def permission_layers(self) -> list[dict]:
        return Researcher.layers()


AGENT = GeneralAgent("subagents/general.md")
