"""Shared Vulture whitelist for framework-driven false positives."""

# Pydantic reads this class attribute during model construction.
model_config

# Cyclopts registers default commands through decorators and dispatches them indirectly.
compile_agent
