import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.base import Subagent
from src.rulesets.reviewer import Reviewer


class LatticeReviewerTestCoverage(Subagent):
    @property
    def name(self) -> str:
        return "(Lattice) Reviewer: Test Coverage"

    def permission_layers(self) -> list[dict]:
        return Reviewer.layers()


AGENT = LatticeReviewerTestCoverage("worker_agents/lattice_interface/subagents/lattice_test_coverage_auditor/prompt.md")
