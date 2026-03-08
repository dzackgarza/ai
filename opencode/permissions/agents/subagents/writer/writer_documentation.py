import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.base import Subagent
from src.rulesets.docs_writer import DocsWriter


class WriterDocumentation(Subagent):
    @property
    def name(self) -> str:
        return "Writer: Documentation"

    def permission_layers(self) -> list[dict]:
        return DocsWriter.layers()


AGENT = WriterDocumentation()
