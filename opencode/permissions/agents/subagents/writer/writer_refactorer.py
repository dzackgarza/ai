import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.base import Subagent
from src.rulesets.code_writer import CodeWriter


class WriterRefactorer(Subagent):
    @property
    def name(self) -> str:
        return "Writer: Refactorer"

    def permission_layers(self) -> list[dict]:
        return CodeWriter.layers()


AGENT = WriterRefactorer()
