from src.mixins import mixin_code_writer


class CodeWriter:
    """Read src and plans, write src."""

    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_code_writer()]
