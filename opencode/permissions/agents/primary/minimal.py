import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.base import PureAgent
from src.mixins import mixin_bash_unrestricted, mixin_orchestrator


class MinimalAgent(PureAgent):
    @property
    def name(self) -> str:
        return "Minimal"

    def permission_layers(self) -> list[dict]:
        return [mixin_bash_unrestricted(), mixin_orchestrator()]

    @property
    def overrides(self) -> dict:
        return {
            "plan_exit": "deny",
            "external_directory": {"/tmp/opencode_test/*": "allow"},
        }


AGENT = MinimalAgent("interactive-agents/minimal")
