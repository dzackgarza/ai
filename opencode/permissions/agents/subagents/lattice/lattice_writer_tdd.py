import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.base import Subagent
from src.rulesets.test_writer import TestWriter


class LatticeWriterTDD(Subagent):
    @property
    def name(self) -> str:
        return "(Lattice) Writer: TDD"

    def permission_layers(self) -> list[dict]:
        return TestWriter.layers()


AGENT = LatticeWriterTDD("worker_agents/lattice_interface/subagents/lattice_tdd_writer/prompt.md")
