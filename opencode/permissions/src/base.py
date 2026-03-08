from __future__ import annotations

"""base.py — Abstract base class for agent permission definitions."""

from abc import ABC, abstractmethod
from src.models import BaseType


class Agent(ABC):
    """Interface every agent definition must satisfy.

    Subclasses define ``name``, ``base_type``, and ``permission_layers()``.
    The ``compile()`` method is provided and should not be overridden.
    """

    def __init__(self, prompt_template: str) -> None:
        self._prompt_template = prompt_template

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique agent name as it appears in opencode config files."""

    @property
    @abstractmethod
    def base_type(self) -> BaseType:
        """Whether this is a primary agent or a subagent."""

    @abstractmethod
    def permission_layers(self) -> list[dict]:
        """Ordered permission dicts applied after global defaults and base type.

        Each dict is merged left-to-right; later layers override earlier ones.
        Use preset and mixin helpers to build these layers.
        """

    @property
    def prompt_template(self) -> str:
        """Prompt template path relative to PROMPTS_DIR."""
        return self._prompt_template

    @property
    def overrides(self) -> dict:
        """Final overrides applied after all layers. Override in subclass if needed."""
        return {}

    @property
    def output_filename(self) -> str:
        """Markdown filename written into opencode/agents."""
        return f"{self.name}.md"

    def compile(self) -> dict:
        """Compile all layers into a single flat permission dict."""
        from src.compiler import compile_agent

        return compile_agent(self)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(name={self.name!r}, base_type={self.base_type!r}, "
            f"prompt_template={self.prompt_template!r})"
        )


class PureAgent(Agent):
    """Convenience base for primary agents."""

    @property
    def base_type(self) -> BaseType:
        return "pure_agent"


class Subagent(Agent):
    """Convenience base for subagents."""

    @property
    def base_type(self) -> BaseType:
        return "subagent"
