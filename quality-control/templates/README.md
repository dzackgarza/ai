# Quality-Control Templates

This directory contains seed templates for new projects that should start with the local
quality-control expectations already wired in.

This is a minimal seed, not a wholesale project scaffold.
It intentionally excludes assistant-specific files, hook scaffolding, and workflow
debris. The template ideas retained here are:

- `uv` for Python dependency management.

- A repo-local `justfile` as the command surface.

- `ruff`, type checking, and pytest as normal quality gates.

- A minimal `AGENTS.md` pointing agents to repository-owned contracts and quality
  checks.

- Tests that prove owned behavior rather than framework or type-system trivia.

## Seeds

- `python-modern`: minimal Python project seed for libraries and CLIs.
