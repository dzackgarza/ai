---
name: probe
description: High-density agentic primer for semantic search, AST-aware extraction, and structural queries. Calibrated with real-world Python outputs for one-shot tool mastery.
---

# Probe Agentic Primer (Python)

**Always invoke via `npx -y @probelabs/probe`**. Use `probe` for codebase navigation and context gathering where semantic ranking or AST-aware symbol extraction is required.

## 1. Semantic Search (Ranked Discovery)
Scans files using Okapi BM25 ranking. Ideal for finding implementation sites by intent.

**Pattern**: `npx -y @probelabs/probe search "<PATTERN>" <PATH> -l python -o plain --max-results <N>`

**Calibration (Evaluation Result)**:
```bash
# Input
npx -y @probelabs/probe search "macro_node" src/ -l python -o plain --max-results 2

# Output Snippet
File: src/structure/latexdoc/plastex_document.py
Lines: 256-260
def _get_title_node(node: Macro) -> Node | None:
    try:
        return node.title
...
File: src/structure/latexdoc/pylatexenc_snippet_parser.py
Lines: 232-234
    def macro_required_group_at(cls, node: LatexMacroNode, index: int) -> LatexGroupNode:
```

## 2. AST-Aware Symbol Extraction
Extracts entire syntax nodes (classes/functions) via tree-sitter. Eliminates line-number guesswork for context gathering.

**Pattern**: `npx -y @probelabs/probe extract "<FILE>#<SYMBOL>" -o plain`

**Calibration (Evaluation Result)**:
```bash
# Input
npx -y @probelabs/probe extract "src/pipeline/bibliography.py#LatexBibliography" -o plain

# Output Snippet
File: src/pipeline/bibliography.py
Lines: 34-308
Type: class_definition
class LatexBibliography(BaseModel, frozen=True):
    """Resolved bibliography with normalized citation definitions."""
    raw_source: LatexString
    ...
    @model_validator(mode="after")
    def _validate(self) -> Self:
        assert self.raw_source.value.strip(), "Bibliography raw source cannot be empty."
```

## 3. Structural Queries (AST-Grep)
Finds code patterns regardless of formatting or naming using metavariables.

**Pattern**: `npx -y @probelabs/probe query "<PATTERN>" <PATH> --language python`

| Pattern Syntax | Matches |
|--- |--- |
| `$VAR` | Single AST node (identifier, expression) |
| `$$$VAR` | Multiple sibling nodes (arguments, statements) |

**Agentic Heuristics (Python)**:
- **Validators**: `npx -y @probelabs/probe query "@model_validator(mode='$MODE')\ndef $NAME(self) -> Self: $$$BODY" .`
- **Error Handling**: `npx -y @probelabs/probe query "try: $$$BODY\nexcept $ERR: $$$HANDLER" .`
- **Class Analysis**: `npx -y @probelabs/probe query "class $NAME(BaseModel, $$$BASES): $$$BODY" .`

## Agentic Workflow
1. **Discover**: `npx -y @probelabs/probe search` to locate candidates.
2. **Retrieve**: `npx -y @probelabs/probe extract "path/to/file#SymbolName"` for full implementation context.
3. **Audit**: `npx -y @probelabs/probe query` for structural consistency checks across files.
4. **Constraint**: Always use `--max-tokens` or `--max-results` to protect context window.
