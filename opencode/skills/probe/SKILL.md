---
name: probe
description: Use for ALL codebase searching and discovery. REPLACES list_directory, grep, and ripgrep for semantic discovery, AST-aware extraction, and structural queries. Mandatory for turn-efficient navigation.
---

# Probe Agentic Primer (Python)

**Always invoke via `npx -y @probelabs/probe`**. `probe` is your primary tool for codebase navigation. Do not use `grep` or `find` for architectural discovery; `probe` is 10x faster and context-aware.

## 1. Semantic Search (Ranked Discovery)
Ideal for finding "where" a feature is implemented. REPLACES `grep`.

**Pattern**: `npx -y @probelabs/probe search "<KEYWORDS>" <PATH> -l python -o plain --max-results <N>`

**Discovery Tips**:
- **Python Source**: Use `-l python` to focus on implementations.
- **Documentation**: Use `ext:md` to find design patterns or examples in docs.
  - *Example*: `npx -y @probelabs/probe search "class User(BaseModel)" . ext:md`

## 2. AST-Aware Symbol Retrieval
REPLACES `read_file` line-guessing. Always use to get complete implementations.

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
REPLACES complex `grep` pipelines for finding architectural patterns in source code.

**Pattern**: `npx -y @probelabs/probe query "<PATTERN>" <PATH> --language python`

| Wildcard | Matches |
|--- |--- |
| `$VAR` | Single AST node (identifier, expression) |
| `$$$VAR` | Multiple sibling nodes (arguments, statements) |

**Common Structural Patterns**:
- **BaseModels with validators**: `npx -y @probelabs/probe query "class $NAME(BaseModel): \n  $$$BEFORE \n  @model_validator(mode='after') \n  def $VAL(self) -> Self: $$$BODY" . --language python`
- **Error Handling**: `npx -y @probelabs/probe query "try: $$$BODY\nexcept $ERR: $$$HANDLER" .`

## Common Failures (RED FLAGS)
- **`ast-grep` Panics**: If `probe query` fails with syntax or `MultipleNode` errors, the pattern is too complex. **Fallback immediately** to `probe search` + `probe extract`.
- **Searching Docs with Query**: `probe query` is for source code. Use `probe search` with `ext:md` for documentation.
- **Manual Line Guessing**: Never use `read_file` to guess class bounds. Use `probe extract file#Symbol`.
- **Omission of `npx`**: `probe` is not globally installed. Always prefix with `npx -y @probelabs/probe`.

## Agentic Heuristics (Turn Efficiency)
1. **Discover (Turn 1)**: Use `probe search` to identify candidate files and symbols.
2. **Retrieve (Turn 2)**: Use `probe extract "file#Symbol"` to pull the implementation.
3. **Audit (Optional)**: Use `probe query` ONLY for finding consistent patterns across many source files.
4. **Context Management**: Use `--max-tokens` or `--max-results` to prevent context explosion. One `probe search` + `probe extract` sequence usually replaces 5-10 turns of standard tools.
