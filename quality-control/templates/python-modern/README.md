# Python Modern Seed

Use this seed when creating a small Python project that should inherit the standard
quality-control posture without bringing in obsolete Claude hook scaffolding.

## Files

- `AGENTS.md`: agent-facing project rules.

- `justfile`: canonical command entrypoints delegating to global QC.

- `pyproject.toml`: `uv` project metadata and pytest configuration seed.

- `src/example_project/__init__.py`: package placeholder.

- `tests/test_contract.py`: example owned-contract test.

Rename `example_project` to the real package name before first commit.
