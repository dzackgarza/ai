from src.mixins import mixin_docs_writer, mixin_git


class DocsWriter:
    """Read docs and plans, write docs, commit."""

    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_docs_writer(), mixin_git()]
