import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.base import Subagent
from src.rulesets.code_writer import CodeWriter


class LatticeWriterAlgorithmPorter(Subagent):
    @property
    def name(self) -> str:
        return "(Lattice) Writer: Algorithm Porter"

    def permission_layers(self) -> list[dict]:
        return CodeWriter.layers()


AGENT = LatticeWriterAlgorithmPorter("worker_agents/lattice_interface/subagents/lattice_algorithm_porter/prompt.md")
