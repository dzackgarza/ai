import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.base import Subagent
from src.rulesets.code_writer import CodeWriter


class WriterGeneralCode(Subagent):
    @property
    def name(self) -> str:
        return "Writer: General Code"

    def permission_layers(self) -> list[dict]:
        return CodeWriter.layers()


AGENT = WriterGeneralCode()
