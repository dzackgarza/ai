---
name: code-patterns-python
description: Use when writing, reviewing, or refactoring Python code, looking for Python style guides and system conventions, Python project structure, Pydantic models, uv scripts, type boundaries, or module public interfaces.
---
# Python Code Patterns

> [!IMPORTANT]
> All Python code produced under this skill must adhere to the [[policy-index/SKILL#policy-registry|Bridge-Burning Policies]] in `policy-index/SKILL.md`. These are non-negotiable hard constraints: no runtime fallback defaults, no optional critical dependencies, no mock proof, no swallowed errors, no hidden partial success, no broad type escapes.

Load after [[code-patterns/SKILL|code-patterns]] for Python-specific rules.

## Non-Negotiables

- Start every Python file with `from __future__ import annotations`.
- Target the latest Python used by the project. Do not add version guards or compatibility
  branches unless the user explicitly asks for multi-version support.
- Type every owned function signature. Avoid `Any`; use a typed boundary for untyped
  third-party libraries.
- Do not use `# type: ignore` comments in owned code. Resolve underlying signature mismatches instead.
- Use modern union syntax: `X | None`, not `Optional[X]`; `X | Y`, not `Union[X, Y]`.
- Treat Pydantic as the boundary where untyped external data becomes typed. Do not use
  `typing.cast` or return `Any` or `dict[str, Any]` outside of Pydantic models.
- Route external API communications through dedicated Response or API objects/types that
  encapsulate communication and validation rather than using stateless helper functions returning raw JSON dictionaries.
- Pydantic models validate automatically on construction. Do not write manual checks or manually
  invoke internal/external validation helpers; simply construct the type directly or use `.model_validate()`.
- Use Pydantic models for structured data and external contracts. Do not introduce
  dataclasses or `NamedTuple` for new data containers unless the project already owns that
  representation and the local boundary requires it.
- Use `uv`, `pyproject.toml`, and the project [[justfile/SKILL|justfile]]; do not use pip, poetry,
  pip-tools, ad hoc requirements files, or direct test/lint commands when a recipe exists.
- Fail fast with assertions for invariants. Do not add speculative `try`/`except` blocks,
  broad catches, or missing-tool guards for failures that have not been observed.
- Do not return `None` on deterministic paths. If caller invariants make absence
  impossible, assert and dump the relevant data.
- Do not use `*args`, `**kwargs`, positional-only parameters, or opaque option bags in
  owned APIs except for framework-mandated hooks or genuine forwarding wrappers.
- Keep required runtime values explicit at the boundary. Defaults are allowed only for real
  domain defaults, not to turn missing config, env, CLI, or external data into success.

## Structure Rules

- Keep modules cohesive: one concept or tightly related concept group per file.
- Prefer flat package structure. Add nesting only for a real subdomain or boundary.
- Define public package/module interfaces with `__all__` when consumers import from them.
- Use absolute imports by default. Relative imports are for local package internals only
  when they improve clarity and match the repo's convention.
- Match names to concepts: module names are `snake_case`; class names describe domain
  objects, not vague managers or processors.
- Place tests according to the repo convention. If no convention exists, choose one and
  apply it consistently rather than mixing colocated and parallel layouts.

## Boundary Patterns

- Parse external input into Pydantic models at the boundary; keep owned core code typed and
  total.
- Use `validate_call` on orchestration functions that can be invoked outside the CLI layer.
- Wrap untyped libraries behind a typed firewall that returns project-owned types.
- Let subprocess, network, and filesystem errors propagate unless a specific observed
  failure has an owned domain meaning.
- Use PEP 723 inline metadata for standalone Python scripts with non-stdlib dependencies.

## References

Read only when needed:

- `references/python-patterns.md` — original detailed Python pattern source.
- `references/project-structure.md` — original Python project-structure guide.
