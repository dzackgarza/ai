---
name: probe
description: Use for semantic narrowing AFTER broad codebase discovery (tree/find/just/help/config). Extracts implementations and finds structural patterns in source code. NOT a replacement for reality-first repo inspection.
---
# Probe Agentic Primer (Python)

**Always invoke via `npx -y @probelabs/probe`**.

`probe` is a semantic narrowing and extraction tool. Use AFTER you have exposed the actual repo structure through `tree`, `find`, `just --list`, package scripts, CLI `--help`, config files, and entrypoints. Do not start with `probe search` as a substitute for broad discovery.

## When To Use (vs. Not)

| Use `probe` for | Use `tree`/`find`/`just`/`--help` first |
| --- | --- |
| Finding where a known concept is implemented | Exposing the repo's actual shape |
| Extracting a full function/class body | Understanding what directories and configs exist |
| Finding structural patterns across files | Learning what commands and entrypoints are available |

## 1. Semantic Search (Second-Stage Narrowing)

Use after broad discovery identifies the likely search space.

**Pattern**:
`npx -y @probelabs/probe search "<KEYWORDS>" <PATH> -l python -o plain --max-results <N>`

**Discovery Tips**:

- **Python Source**: Use `-l python` to focus on implementations.

- **Documentation**: Use `ext:md` to find design patterns or examples in docs.

  - *Example*: `npx -y @probelabs/probe search "class User(BaseModel)" . ext:md`

## 2. AST-Aware Symbol Retrieval

Use to get complete implementations without guessing line ranges.

**Pattern**: `npx -y @probelabs/probe extract "<FILE>#<SYMBOL>" -o plain`

**Calibration (Output Snippet)**:
```bash
# Input
npx -y @probelabs/probe extract "src/pipeline/bibliography.py#LatexBibliography" -o plain

# Output Snippet
File: src/pipeline/bibliography.py
Lines: 34-308
Type: class_definition
class LatexBibliography(BaseModel, frozen=True):
```

## 3. Structural Queries (AST-Grep)

Use for finding consistent patterns across many source files.

**Pattern**: `npx -y @probelabs/probe query "<PATTERN>" <PATH> --language python`

| Wildcard | Matches |
| --- | --- |
| `$VAR` | Single AST node (identifier, expression) |
| `$$$VAR` | Multiple sibling nodes (arguments, statements) |

**Common Structural Patterns**:

- **BaseModels with validators**:
  `npx -y @probelabs/probe query "class $NAME(BaseModel): \n $$$BEFORE \n @model_validator(mode='after') \n def $VAL(self) -> Self: $$$BODY" . --language python`

- **Error Handling**:
  `npx -y @probelabs/probe query "try: $$$BODY\nexcept $ERR: $$$HANDLER" .`

## Common Failures (RED FLAGS)

- **[[ast-grep/SKILL|ast-grep]] Panics**: If `probe query` fails with syntax or `MultipleNode` errors,
  the pattern is too complex.
  **Fallback immediately** to `probe search` + `probe extract`.

- **Searching Docs with Query**: `probe query` is for source code.
  Use `probe search` with `ext:md` for documentation.

- **Manual Line Guessing**: Never use `read_file` to guess class bounds.
  Use `probe extract file#Symbol`.

- **Omission of `npx`**: `probe` is not globally installed.
  Always prefix with `npx -y @probelabs/probe`.

## Agentic Heuristics (Turn Efficiency)

1. **Expose (Turn 1)**: Use `tree`, `find`, `just --list`, `--help`, config files to understand the repo's actual shape.

2. **Narrow (Turn 2)**: Use `probe search` to identify candidate files and symbols.

3. **Retrieve (Turn 3)**: Use `probe extract "file#Symbol"` to pull the implementation.

4. **Audit (Optional)**: Use `probe query` ONLY for finding consistent patterns across
   many source files.

5. **Context Management**: Use `--max-tokens` or `--max-results` to prevent context
   explosion. The full sequence replaces 5-10 turns of raw text search.
