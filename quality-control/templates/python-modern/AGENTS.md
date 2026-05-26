# Project Agent Instructions

Start every investigation by reading repository docs and the `justfile`.

Use `just` recipes for install, test, typecheck, lint, and format.
Do not bypass the canonical command surface with ad hoc commands when a recipe exists.

Tests must prove repository-owned behavior at public contracts or real boundaries.
Do not add tests that only assert non-empty output, constructor storage, framework
behavior, or type-system trivia.

Before editing, checkpoint the current state with git.
After editing, inspect the diff and run the relevant `just` recipe.
