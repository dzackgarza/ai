import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.base import PureAgent
from src.rulesets.planner import Planner


class PlanAgent(PureAgent):
    @property
    def name(self) -> str:
        return "plan"

    def permission_layers(self) -> list[dict]:
        return Planner.layers()


AGENT = PlanAgent()
