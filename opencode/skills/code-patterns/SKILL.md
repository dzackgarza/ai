---
name: code-patterns
description: Use when writing, reviewing, or refactoring code, looking for style guides and system coding conventions, and deciding naming, function shape, module boundaries, error handling, code style, or language-specific implementation patterns.
---
# Code Patterns and Style

> [!IMPORTANT]
> All code produced under this skill must adhere to the [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md#policy-registry) in `policy-index/SKILL.md`. These are non-negotiable hard constraints that eliminate runtime defaults, fallbacks, mocks, optional critical dependencies, hidden partial success, and other validation-evasion pathways.

This is the canonical entry point for code pattern and style guidance. Load it for the
cross-language rules, then load the language subskill when one exists.

## Routing

- Python code, Python packages, Pydantic models, uv scripts, or Python module layout:
  load [[code-patterns/python/SKILL|code-patterns-python]].
- CLI or script interface design: also load [[writing-scripts-and-cli-interfaces/SKILL|writing-scripts-and-cli-interfaces]].
- JSON or YAML config edits: also load [[config-file-editing/SKILL|config-file-editing]].
- Tests or proof surfaces: [[test-guidelines/SKILL|test-guidelines]] owns admissible proof; this skill only owns
  readability and maintainability of test code.
- External library, framework, compiler, or package behavior: load [[known-solution-first/SKILL|known-solution-first]]
  before applying local style rules.

## Authority Order

1. User directive and local `AGENTS.md` instructions.
2. [[policy-index/SKILL|policy-index]], [[anti-slop/SKILL|anti-slop]], [[bespoke-software-policy/SKILL|bespoke-software-policy]], and [[test-guidelines/SKILL|test-guidelines]] for
   hard bridge-burning constraints.
3. Language subskill for language-specific rules.
4. This skill's cross-language style guidance.
5. Reference files under `references/` for detailed examples.

If a reference suggests a soft fallback, mock proof, runtime default, broad catch, special
case object, compatibility shim, or helper-level proof, the bridge-burning policy wins.
Do not negotiate this locally.

## Core Rules

- Read the surrounding code first. Match the repo's established module boundaries,
  naming, and validation patterns unless they violate a loaded hard policy.
- Preserve the smallest useful interface. Do not add managers, processors, adapters,
  flags, registries, or lifecycle states until the existing workflow proves they are
  necessary.
- Names must reveal domain intent. Rename before commenting when the comment only explains
  what a symbol is.
- Functions do one operation. Split command from query; split boolean-mode functions into
  named operations.
- Keep argument lists short and explicit. Group real domain concepts into typed objects;
  do not hide unrelated knobs in generic option bags.
- Comments explain non-obvious intent, external constraints, or consequences. They do not
  restate the code, preserve changelog history, or excuse dead/commented-out code.
- Validate at owned boundaries, then use total state internally. Do not add defensive
  guards in hot paths for states already excluded by the boundary contract.
- Prefer deep modules: small public surface, concentrated responsibility, useful internal
  complexity. Delete pass-through abstractions that only rename another API.
- Remove duplication when it expresses the same domain decision. Keep repetition when it
  represents distinct facts that merely look similar.
- Do not call code complete because it works once. Inspect the shape after the behavior is
  proven and simplify names, functions, and module boundaries before handoff.

## Reference Files

Read only the relevant reference:

- `references/names.md` — naming and intention-revealing symbols.
- `references/functions.md` — function size, arguments, side effects, command/query split.
- `references/comments.md` — when comments are useful and when they are residue.
- `references/classes.md` — cohesion, SRP, DIP, and class boundaries.
- `references/objects-and-data.md` — object/data-structure tradeoffs and Law of Demeter.
- `references/error-handling.md` — legacy clean-code error-handling guidance, subordinate
  to fail-loud policy and language subskills.
- `references/tests.md` — readability of tests, subordinate to [[test-guidelines/SKILL|test-guidelines]].
- `references/smells-and-heuristics.md` — detailed smell catalog for review sweeps.
