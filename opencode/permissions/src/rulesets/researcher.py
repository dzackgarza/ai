from src.mixins import mixin_researcher


class Researcher:
    """Read all, write nothing."""

    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_researcher()]
