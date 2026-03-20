from __future__ import annotations

from src.mixins import mixin_orchestrator, mixin_session_tools


class Coordinator:
    """Lightweight coordination profile without orchestrator-level authority."""

    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_orchestrator(), mixin_session_tools()]
