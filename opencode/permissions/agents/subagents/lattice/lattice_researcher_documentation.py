import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.base import Subagent
from src.rulesets.researcher import Researcher


class LatticeResearcherDocumentation(Subagent):
    @property
    def name(self) -> str:
        return "(Lattice) Researcher: Documentation"

    def permission_layers(self) -> list[dict]:
        return Researcher.layers()


AGENT = LatticeResearcherDocumentation("sub-agents/lattice-researcher-documentation")
