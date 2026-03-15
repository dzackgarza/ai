import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.base import Subagent
from src.rulesets.code_writer import CodeWriter


class LatticeWriterInterfaceImplementer(Subagent):
    @property
    def name(self) -> str:
        return "(Lattice) Writer: Interface Implementer"

    def permission_layers(self) -> list[dict]:
        return CodeWriter.layers()


AGENT = LatticeWriterInterfaceImplementer("sub-agents/lattice-interface-implementer")
