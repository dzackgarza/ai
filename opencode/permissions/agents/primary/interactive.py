import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.base import PureAgent
from src.rulesets.interactive import Interactive


class InteractiveAgent(PureAgent):
    @property
    def name(self) -> str:
        return "Interactive"

    def permission_layers(self) -> list[dict]:
        return Interactive.layers()


AGENT = InteractiveAgent("interactive_agents/interactive.md")
