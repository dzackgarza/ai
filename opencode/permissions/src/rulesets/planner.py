from src.mixins import mixin_planner


class Planner:
    """Read all, write plans only, can exit plan mode."""

    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_planner()]
