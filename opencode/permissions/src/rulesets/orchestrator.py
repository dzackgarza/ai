from __future__ import annotations

from src.mixins import (
    mixin_bash_unrestricted,
    mixin_git,
    mixin_interactive,
    mixin_orchestrator,
)


class Orchestrator:
    """Primary orchestration profile with full implementation authority."""

    @classmethod
    def layers(cls) -> list[dict]:
        return [
            mixin_orchestrator(),
            mixin_interactive(),
            mixin_bash_unrestricted(),
            mixin_git(),
        ]
