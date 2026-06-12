# Slop Report: `dzackgarza/ai`

## 1. Design Choices Spotted and Excluded

- **OCR/Document Extraction Tools:** The codebase maintains multiple independent scripts for document extraction (`extract_marker.py`, `extract_pymupdf.py`). While they seem redundant, this represents a deliberate design choice providing different integration strategies for specific external tools (a heavy, high-accuracy LLM approach vs. a lightweight local library).
- **Caveman CLI integrations:** The wrapper scripts and prompt management around Anthropic APIs and `gws` (Google Workspace CLI) clearly integrate with external tools according to specific user requirements.

## 2. Valid Slop Findings

- **Scattered Truth (Code Duplication)**
  - *Evidence:* `_normalize_authorized_user_payload` is defined separately in `opencode/skills/google-workspace/scripts/google_api.py`, `gws_bridge.py`, and `setup.py`.
  - *Explanation:* The exact same payload normalization logic is repeated across three files in the same directory instead of being extracted to a shared module. Small changes require editing multiple locations.
  - *Remediation:* Extract the function to a shared module (e.g., `_google_auth_utils.py`) and import it.

- **Regex Against Semantic Formats**
  - *Evidence:* `opencode/skills/creating-skills/scripts/quick_validate.py` (lines 24-25)
  - *Explanation:* Uses regex (`re.match(r"^---\n(.*?)\n---", content, re.DOTALL)`) to parse Markdown YAML frontmatter. This is brittle to formatting changes and violates the rule against using regex instead of standard parsers for Markdown/YAML.
  - *Remediation:* Use a proper frontmatter parsing library or strict string splitting with exact matching instead of regex.

- **Design by Accretion / Legacy Paths**
  - *Evidence:* `opencode/skills/git-guidelines/scripts/extract_unresolved_issues_old.py` exists alongside the refactored `extract_unresolved_issues/` package.
  - *Explanation:* The codebase has accumulated a new module but failed to delete the old implementation, violating the "No compatibility shims or legacy paths in pre-launch bespoke software" and "No deletion without burden disposition" policies.
  - *Remediation:* Delete the `_old.py` file completely.

## 3. Bridge-Burning Policy Violations

- **No optional critical dependencies (try-import stubs)**
  - *Evidence:* `opencode/skills/git-guidelines/scripts/extract_unresolved_issues/src/extract_unresolved_issues/cli.py` (lines 48-56)
  - *Explanation:* Uses a `try...except ImportError` block to optionally load `rich` for formatting, falling back to a standard `print` if missing. Graceful degradation is a violation.
  - *Remediation:* Make `rich` a strict requirement in the project configuration and remove the `try/except` block, failing loudly if it's missing.

- **No fallbacks, period (try A else B else C chains)**
  - *Evidence:* `opencode/skills/caveman-compress/scripts/compress.py` (lines 62-81)
  - *Explanation:* `call_claude` attempts to use the `ANTHROPIC_API_KEY` and the `anthropic` library. If it hits an `ImportError`, it silently catches it and falls back to invoking the `claude` CLI via subprocess. This violates the hard rule against ambient discovery and fallbacks.
  - *Remediation:* The script should expect exactly one method of execution. If it needs to support both, it should be an explicit configuration flag (e.g., `--use-cli`), and failure in one mode should halt execution.

- **No optional critical dependencies / Ambient fallback**
  - *Evidence:* `opencode/skills/google-workspace/scripts/_hermes_home.py` (lines 14-30)
  - *Explanation:* Attempts to import `get_hermes_home` from `hermes_constants`. If it fails (`except (ModuleNotFoundError, ImportError)`), it falls back to an inline re-implementation.
  - *Remediation:* Define the standard path resolution strictly or mandate the presence of `hermes_constants`.

- **No boolean mode flags in owned APIs**
  - *Evidence:* `opencode/skills/ocr-and-documents/scripts/extract_marker.py` (line 15)
  - *Explanation:* `def convert(path, output_dir=None, output_format="markdown", use_llm=False):` exposes `use_llm` as a boolean mode flag.
  - *Remediation:* Use an Enum (e.g., `ExtractionMode.STANDARD` vs `ExtractionMode.LLM_BOOSTED`) or separate functions.

## 4. Recommended Remediation Direction

1. **Remove all `except ImportError` blocks:** If a dependency is needed, declare it in the build configuration (e.g., `pyproject.toml` or `uv` dependencies). Fail fast and loudly if it is absent.
2. **Eliminate silent fallbacks:** Make configuration explicit. For tools like `compress.py`, remove the `anthropic` SDK fallback and rely on a single execution path, or force the user to provide an explicit `--provider` flag.
3. **Consolidate shared logic:** Move duplicate definitions (like payload normalizers) to single sources of truth.
4. **Remove legacy accretion:** Delete `_old.py` files to maintain a single canonical version of scripts.
5. **Update boolean flags:** Convert boolean API parameters into enums that make state and behavior explicit.

## 5. Areas Reviewed and Not Reviewed

- **Reviewed:** `opencode/skills/` directory Python and Markdown files, focusing on `.system/`, `google-workspace/`, `caveman-compress/`, `git-guidelines/`, `ocr-and-documents/`, and `creating-skills/`.
- **Not Reviewed:** Rust/TypeScript codebases outside the main Python scripts within `skills/`, `mcp/` integrations, `dotfiles/`, or internal tool configs (like `nginx.conf`, `.semgrep.yml`).
