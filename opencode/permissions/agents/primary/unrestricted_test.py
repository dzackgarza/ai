import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.base import PureAgent
from src.mixins import mixin_allow_all_permissions


class UnrestrictedTestAgent(PureAgent):
    @property
    def name(self) -> str:
        return "Unrestricted Test"

    def permission_layers(self) -> list[dict]:
        return [mixin_allow_all_permissions()]


AGENT = UnrestrictedTestAgent("interactive-agents/unrestricted-test")
