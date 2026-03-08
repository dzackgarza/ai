import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.base import Subagent
from src.rulesets.reviewer import Reviewer


class ReviewerPlanContract(Subagent):
    @property
    def name(self) -> str:
        return "Reviewer: Plan Contract"

    def permission_layers(self) -> list[dict]:
        return Reviewer.layers()


AGENT = ReviewerPlanContract()
