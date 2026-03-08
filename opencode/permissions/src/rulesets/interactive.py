from src.mixins import mixin_orchestrator, mixin_session_tools, mixin_interactive, mixin_bash_unrestricted


class Interactive:
    """Full read/write/bash, orchestration, and session introspection."""

    @classmethod
    def layers(cls) -> list[dict]:
        return [
            mixin_orchestrator(),
            mixin_session_tools(),
            mixin_interactive(),
            mixin_bash_unrestricted(),
        ]
