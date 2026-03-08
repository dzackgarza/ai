import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.base import Subagent
from src.rulesets.reviewer import Reviewer


class LatticeReviewerDocumentationLibrarian(Subagent):
    @property
    def name(self) -> str:
        return "(Lattice) Reviewer: Documentation Librarian"

    def permission_layers(self) -> list[dict]:
        return Reviewer.layers()


AGENT = LatticeReviewerDocumentationLibrarian("worker_agents/lattice_interface/subagents/lattice_documentation_librarian/prompt.md")
