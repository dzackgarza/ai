from src.mixins import mixin_docs_writer


class DocsWriter:
    """Read docs and plans, write docs."""

    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_docs_writer()]
