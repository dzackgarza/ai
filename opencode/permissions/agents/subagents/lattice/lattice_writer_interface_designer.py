import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.base import Subagent
from src.rulesets.code_writer import CodeWriter


class LatticeWriterInterfaceDesigner(Subagent):
    @property
    def name(self) -> str:
        return "(Lattice) Writer: Interface Designer"

    def permission_layers(self) -> list[dict]:
        return CodeWriter.layers()


AGENT = LatticeWriterInterfaceDesigner("worker_agents/lattice_interface/subagents/lattice_interface_designer/prompt.md")
