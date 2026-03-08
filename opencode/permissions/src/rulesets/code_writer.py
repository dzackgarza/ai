from src.mixins import mixin_code_writer, mixin_git


class CodeWriter:
    """Read src and plans, write src, commit."""

    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_code_writer(), mixin_git()]
