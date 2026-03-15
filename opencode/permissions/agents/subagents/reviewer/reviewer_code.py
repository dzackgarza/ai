import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.base import Subagent
from src.rulesets.reviewer import Reviewer


class ReviewerCode(Subagent):
    @property
    def name(self) -> str:
        return "Reviewer: Code"

    def permission_layers(self) -> list[dict]:
        return Reviewer.layers()


AGENT = ReviewerCode("sub-agents/code-reviewer")
