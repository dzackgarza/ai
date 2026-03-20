from src.mixins import mixin_reviewer


class Reviewer:
    """Read all, write nothing."""

    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_reviewer()]
