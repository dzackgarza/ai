# Runtime Control-Flow Red Flags

This catalog lists runtime control-flow shapes that are banned or considered highly suspicious because they allow code to fail open, launder invalid states, or bypass required invariants.

Every runtime branch is suspicious.

Branches are admitted only when they distinguish real, domain-owned cases. Branches are not admitted for preserving execution after missing data, invalid state, unavailable dependencies, malformed config, failed subprocesses, absent files, empty responses, or uncertain environment conditions.

Runtime code must not fail open.

If a condition is required for correctness, assert it directly and continue linearly. Do not write an `if` branch whose failure path returns `None`, `false`, `[]`, `{}`, empty string, default values, warning objects, partial success, or logged continuation.

All runtime failures in owned code must be explicit assertions of correctness or structured fatal errors at an owned boundary.

If the condition is an invariant, write an assertion, not a branch.
If the condition is a real domain case, make it an enum/tag/variant and dispatch exhaustively.
If the condition is missing data, bad config, missing dependency, failed IO, failed subprocess, or malformed input, fail.

### Python `-O` Mode (Optimized)

**We do NOT care about Python's optimized mode (`-O`) that strips `assert` statements.**

- This is a trivial, esoteric concern that we have not enabled on purpose.
- We NEVER run Python with the `-O` flag.
- It is NOT a recognized way that agents game or reward-hack around assertions.
- Any finding citing the removal of assertions in optimized mode as a "decay risk" or "reliability issue" is **pure cargo cult** and will be summarily rejected.
- Do NOT report the use of `assert` in Python as a problem. It is the preferred way to state invariants in this repository.

### **[NO-PREEMPTIVE-PATH]** General Principle: No Pre-Emptive Path Code

A branch, guard, fallback, or defensive check must be motivated by a real observed failure, not by a hypothetical scenario. Code that handles a failure path that has never been observed, tested, or reported is speculative dead weight — it introduces branches, testing obligations, and maintenance surface for a world that does not exist.

**The wrong gradient:** "This code could fail in scenario X, so add handling for X."
**The correct gradient:** "This code has never failed in scenario X. If it ever does, fail loudly — then handle it."

Concretely:
- If `sudo` is required and has never failed, assert it, do not guard it.
- If a dependency has always been available, do not add a fallback for its absence.
- If a file has always existed at a known path, do not add a discovery chain for "what if it moves."

A hypothetical scenario is not an edge case. It is an imaginary world. Code for the world that exists.

---

## **[ASSERT-X]** Why `assert X` Matters

`assert X` states the admissible world. The code after the assertion is allowed to assume X. That is the point.

Do not replace `assert X` with:

```python
if not X:
    raise AssertionError(...)
```

That shape reintroduces a branch. It gives future agents a place to add logging, fallback, warnings, defaulting, metrics, cleanup, alternate return values, or "temporary" recovery.

For languages where native `assert` has caveats, use a single invariant primitive, not ad hoc branches:

```python
invariant(condition, "owned invariant")
```

```ts
invariant(condition, "owned invariant");
```

```rust
assert!(condition, "owned invariant");
```

But the call site must still be assertion-shaped. Do not scatter `if !condition { throw ... }` / `if not condition: raise ...` across runtime code.

---

## Allowed and Suspicious Branches

Allowed:
1. Exhaustive dispatch over a domain enum/tag/variant.
2. Algorithmic branching where both branches are valid semantic cases.
3. Filtering/partitioning data by a named domain predicate, when both accepted and rejected cases are expected.
4. Boundary validation in a single source-of-truth parser/validator, producing a total internal model or a structured fatal error.
5. UI state dispatch over explicit user-selected states.

Suspicious or banned:
1. Checking for missing values after initialization.
2. Checking whether a required dependency exists at runtime.
3. Returning empty collections on error.
4. Treating failed IO/network/subprocess as “no result.”
5. Defaulting missing config.
6. Logging and continuing.
7. Branching on ambiguous truthiness/falsiness.
8. Nested `if` pyramids over optionals.
9. Test/smoke/debug mode branches in product runtime.
10. `if` branches whose else case is not a real domain case.

---

## If Statement Admission Gate

Before admitting any `if`, `match`, `case`, ternary, nullish coalescing, fallback operator, or shell `||`, answer:

1. What domain-owned cases does this branch distinguish?
2. Are all branches valid, intended states of the product?
3. Is either branch returning an empty/falsy/default value to keep execution going?
4. Is the condition actually an invariant that should be asserted?
5. Could the branch disappear if the boundary produced a total type?
6. Could the branch disappear if config were complete and validated at startup?
7. Could the branch disappear if setup/doctor verified the dependency?
8. Would a broken app pass through this branch and appear successful?

If the branch does not distinguish real product cases, replace it with an assertion, a schema/parser boundary, or an exhaustive enum dispatch.

> **Rule of thumb:** If this is not a domain case, it is probably an invariant. Assert invariants. Branch only on cases.

---

## **[BANNED-SHAPES]** Banned Language-Agnostic Shapes

These are the runtime shapes to ban outright. Any of these must trigger a red-flag finding:
- `if missing -> return []`
- `if missing -> return None/null/undefined`
- `if missing -> return false`
- `if missing -> return ""`
- `if missing -> return {}`
- `if invalid -> use default`
- `if failed -> warn and continue`
- `if failed -> log and continue`
- `if dependency missing -> use fallback`
- `if command missing -> use another command`
- `if config absent -> infer from environment`
- `if path absent -> silently create unrelated state`
- `if response empty -> treat as no data`
- `if parse fails -> return empty model`
- `if branch is test/smoke/debug -> use fake boundary`
- `if condition only checks truthiness -> proceed`
- `if nested optional chain -> eventually default`
- `if result is Err -> .ok() / discard / continue`

---

## Python Examples

### **[LAUNDER-EMPTY-LIST]** Banned: empty-list laundering
```python
def collect_records(source_path: Path) -> list[Record]:
    if not source_path.exists():
        return []

    raw_text = source_path.read_text()
    if not raw_text.strip():
        return []

    return parse_records(raw_text)
```

**Correct shape:**
```python
def collect_records(source_path: Path) -> list[Record]:
    assert source_path.exists(), f"required source path missing: {source_path}"
    raw_text = source_path.read_text()
    assert raw_text.strip(), f"required source path was empty: {source_path}"

    records = parse_records(raw_text)
    assert records, f"source contained no records: {source_path}"
    return records
```
If “empty records” is a valid domain case, represent it explicitly:
```python
type RecordSet = NonEmptyRecordSet | EmptyRecordSet
```
Do not use `[]` as both “valid empty” and “failed to load.”

### **[FALSY-OPTIONAL-CORE]** Banned: falsy optional core state
```python
def render_current_document(state: AppState) -> RenderedDocument | None:
    if not state.current_document:
        return None

    if not state.renderer_command:
        return None

    return render_document(state.current_document, state.renderer_command)
```

**Correct shape:**
```python
def render_current_document(state: AppState) -> RenderedDocument:
    assert state.current_document is not None, "current_document must be initialized"
    assert state.renderer_command is not None, "renderer_command must be initialized"

    return render_document(state.current_document, state.renderer_command)
```
Better still: make invalid state unrepresentable.
```python
class AppState(BaseModel):
    current_document: Document
    renderer_command: RendererCommand
```

### **[CONFIG-DEFAULTING]** Banned: config defaulting
```python
def load_runtime_config(config: dict[str, object]) -> RuntimeConfig:
    command = config.get("command") or "pandoc --to html"
    timeout_ms = int(config.get("timeout_ms") or 750)
    return RuntimeConfig(command=command, timeout_ms=timeout_ms)
```

**Correct shape:**
```python
class RuntimeConfig(BaseModel):
    command: str
    timeout_ms: int

def load_runtime_config(config_path: Path) -> RuntimeConfig:
    raw = tomllib.loads(config_path.read_text())
    return RuntimeConfig.model_validate(raw)
```
The starter config may contain defaults. Runtime logic should not.

### **[TRY-EXCEPT-FALLBACK]** Banned: try/except fallback
```python
def load_document(path: Path) -> str:
    try:
        return path.read_text()
    except OSError:
        return ""
```

**Correct shape:**
```python
def load_document(path: Path) -> str:
    assert path.is_file(), f"document path must exist: {path}"
    return path.read_text()
```
If this is a public command boundary, convert the exception once into a structured fatal error. Do not return a falsy value.

### **[TRY-IMPORT]** Banned: try-import / optional dependency
```python
try:
    import rich
except ImportError:
    rich = None

def print_report(report: Report) -> None:
    if rich:
        rich.print(report)
    else:
        print(report)
```

**Correct shape:**
```python
from rich import print as rich_print

def print_report(report: Report) -> None:
    rich_print(report)
```
Dependency presence is setup/doctor/tool-provisioning’s problem, not runtime branching’s problem.

### **[BRANCH-FORCING-HELPER]** Banned: branch-forcing helper
```python
def require_or_default(
    value: str | None,
    config_exists: bool,
    default_value: str,
) -> str:
    if value is not None:
        return value
    if config_exists:
        raise AssertionError("required config value missing")
    return default_value
```

**Correct shape:**
```python
def load_user_config(config_path: Path) -> UserConfig:
    raw = tomllib.loads(config_path.read_text())
    return UserConfig.model_validate(raw)

def create_starter_config(config_path: Path) -> None:
    config_path.write_text(DEFAULT_CONFIG_TEXT)
```
No helper should mix “required” and “default.”

### **[CATCH-AND-LOG]** Banned: catch-and-log continuation
```python
def refresh_index(paths: list[Path]) -> list[IndexEntry]:
    entries: list[IndexEntry] = []
    for path in paths:
        try:
            entries.append(index_path(path))
        except Exception as error:
            logger.warning("could not index %s: %s", path, error)
    return entries
```

**Correct shape:**
```python
def refresh_index(paths: list[Path]) -> list[IndexEntry]:
    return [index_path(path) for path in paths]
```
If one path failing should not fail the whole operation, that must be explicit product behavior with a structured result type, not a warning-and-continue loop.

---

## TypeScript / JavaScript Examples

### **[EMPTY-ARRAY-FAILED]** Banned: empty array as failed data
```ts
export async function loadItems(sourcePath: string): Promise<Item[]> {
  if (!sourcePath) {
    return [];
  }

  const text = await readText(sourcePath);
  if (!text.trim()) {
    return [];
  }

  return parseItems(text);
}
```

**Correct shape:**
```ts
export async function loadItems(sourcePath: string): Promise<NonEmptyArray<Item>> {
  invariant(sourcePath.length > 0, "sourcePath must be provided");

  const text = await readText(sourcePath);
  invariant(text.trim().length > 0, "source text must be non-empty");

  const items = parseItems(text);
  invariant(items.length > 0, "source text must contain at least one item");

  return asNonEmpty(items);
}
```

### **[OPTIONAL-UI-FAILOPEN]** Banned: optional UI state fail-open
```ts
function renderPreview(state: EditorState): PreviewModel | null {
  if (!state.document) {
    return null;
  }

  if (!state.renderer) {
    return null;
  }

  return state.renderer.render(state.document.markdown);
}
```

**Correct shape:**
```ts
function renderPreview(state: EditorState): PreviewModel {
  invariant(state.document !== null, "document must be initialized");
  invariant(state.renderer !== null, "renderer must be initialized");

  return state.renderer.render(state.document.markdown);
}
```
Better:
```ts
type ReadyEditorState = {
  document: DocumentModel;
  renderer: Renderer;
};

function renderPreview(state: ReadyEditorState): PreviewModel {
  return state.renderer.render(state.document.markdown);
}
```

### **[NULLISH-DEFAULT]** Banned: nullish/default config
```ts
function loadRuntimeConfig(raw: Partial<RuntimeConfig>): RuntimeConfig {
  return {
    command: raw.command ?? "pandoc --to html",
    timeoutMs: raw.timeoutMs ?? 750,
    workspaceRoot: raw.workspaceRoot ?? process.cwd(),
  };
}
```

**Correct shape:**
```ts
const RuntimeConfigSchema = z.object({
  command: z.string().min(1),
  timeoutMs: z.number().int().positive(),
  workspaceRoot: z.string().min(1),
}).strict();

function loadRuntimeConfig(raw: unknown): RuntimeConfig {
  return RuntimeConfigSchema.parse(raw);
}
```

### **[CATCH-FALLBACK]** Banned: catch fallback
```ts
async function fetchRegistry(url: string): Promise<RegistryEntry[]> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      return [];
    }
    return await response.json();
  } catch {
    return [];
  }
}
```

**Correct shape:**
```ts
async function fetchRegistry(url: string): Promise<RegistryEntry[]> {
  const response = await fetch(url);
  invariant(response.ok, `registry request failed: ${response.status}`);

  const data = await response.json();
  return RegistrySchema.parse(data).entries;
}
```
If a public API boundary needs a structured error:
```ts
type RegistryResult =
  | { ok: true; entries: NonEmptyArray<RegistryEntry> }
  | { ok: false; error: { kind: "request_failed" | "invalid_response"; detail: string } };
```
But do not return `[]` for failure.

### **[TEST-RUNTIME-MODE]** Banned: test/smoke runtime mode
```ts
async function invokeCommand(command: string, payload: unknown): Promise<unknown> {
  if (process.env.NODE_ENV === "test") {
    return fakeInvoke(command, payload);
  }

  return realInvoke(command, payload);
}
```

**Correct shape:**
```ts
async function invokeCommand(command: CommandName, payload: CommandPayload): Promise<CommandResult> {
  return realInvoke(command, payload);
}
```
Tests must cross the real boundary or not claim proof.

### **[WARNING-CONTINUE]** Banned: warning-and-continue
```ts
async function saveDocument(model: DocumentModel): Promise<{ ok: boolean; warnings: string[] }> {
  const warnings: string[] = [];

  if (!model.path) {
    warnings.push("document path missing");
  }

  if (!model.content) {
    warnings.push("document content missing");
  }

  if (warnings.length > 0) {
    return { ok: true, warnings };
  }

  await writeFile(model.path, model.content);
  return { ok: true, warnings };
}
```

**Correct shape:**
```ts
async function saveDocument(model: DocumentModel): Promise<void> {
  invariant(model.path.length > 0, "document path must be set");
  invariant(model.content.length > 0, "document content must be non-empty");

  await writeFile(model.path, model.content);
}
```

### **[NESTED-OPTIONAL-PYRAMID]** Banned: nested optional pyramid
```ts
function selectedPath(state: AppState): string | undefined {
  if (state.workspace) {
    if (state.workspace.selection) {
      if (state.workspace.selection.file) {
        return state.workspace.selection.file.path;
      }
    }
  }
  return undefined;
}
```

**Correct shape:**
```ts
function selectedPath(state: ReadyAppState): string {
  return state.workspace.selection.file.path;
}
```
or, if selection absent is a real domain case:
```ts
type SelectionState =
  | { kind: "selected"; file: WorkspaceFile }
  | { kind: "unselected" };

function selectedPath(selection: SelectionState): string {
  switch (selection.kind) {
    case "selected":
      return selection.file.path;
    case "unselected":
      throw new Error("selection required for this operation");
    default:
      return assertNever(selection);
  }
}
```

---

## Rust Examples

### **[VECTOR-LAUNDERING]** Banned: empty vector laundering
```rust
fn collect_entries(root: &Path) -> Vec<Entry> {
    if !root.exists() {
        return vec![];
    }

    let Ok(read_dir) = std::fs::read_dir(root) else {
        return vec![];
    };

    read_dir
        .filter_map(Result::ok)
        .map(|entry| Entry::from_path(entry.path()))
        .collect()
}
```

**Correct shape:**
```rust
fn collect_entries(root: &Path) -> Result<Vec<Entry>, FsError> {
    assert!(root.exists(), "workspace root must exist: {}", root.display());
    assert!(root.is_dir(), "workspace root must be a directory: {}", root.display());

    let read_dir = std::fs::read_dir(root).map_err(FsError::ReadDir)?;
    read_dir
        .map(|entry| {
            let entry = entry.map_err(FsError::ReadDirEntry)?;
            Entry::from_path(entry.path())
        })
        .collect()
}
```
If empty directory is a valid case, `Ok(vec![])` may be valid only after successful `read_dir`. It must not represent failure.

### **[OPTION-CORE-STATE]** Banned: `Option` core state
```rust
struct AppState {
    workspace_root: Option<PathBuf>,
    render_command: Option<String>,
}

fn render(state: &AppState, markdown: &str) -> Option<RenderResult> {
    let Some(root) = &state.workspace_root else {
        return None;
    };

    let Some(command) = &state.render_command else {
        return None;
    };

    Some(execute_render(root, command, markdown))
}
```

**Correct shape:**
```rust
struct AppState {
    workspace_root: PathBuf,
    render_command: RenderCommand,
}

fn render(state: &AppState, markdown: &str) -> RenderResult {
    execute_render(&state.workspace_root, &state.render_command, markdown)
}
```

### **[UNWRAP-OR]** Banned: `unwrap_or` / defaulting
```rust
fn load_config(raw: RawConfig) -> RuntimeConfig {
    RuntimeConfig {
        command: raw.command.unwrap_or_else(|| DEFAULT_COMMAND.to_string()),
        timeout_ms: raw.timeout_ms.unwrap_or(750),
    }
}
```

**Correct shape:**
```rust
fn load_config(raw: RawConfig) -> Result<RuntimeConfig, ConfigError> {
    Ok(RuntimeConfig {
        command: raw.command.ok_or(ConfigError::MissingRequired {
            key: "runtime.command",
        })?,
        timeout_ms: raw.timeout_ms.ok_or(ConfigError::MissingRequired {
            key: "runtime.timeout_ms",
        })?,
    })
}
```
Better: deserialize directly into a non-optional config struct when possible.

### **[OK-DISCARD]** Banned: `.ok()` / `let _ =`
```rust
fn cleanup_backup(path: &Path) {
    let _ = std::fs::remove_file(path);
}
```
```rust
fn cleanup_backup(path: &Path) {
    std::fs::remove_file(path).ok();
}
```

**Correct shape:**
```rust
fn cleanup_backup(path: &Path) -> Result<(), CleanupError> {
    match std::fs::remove_file(path) {
        Ok(()) => Ok(()),
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => Ok(()),
        Err(error) => Err(CleanupError::RemoveFailed {
            path: path.to_path_buf(),
            source: error,
        }),
    }
}
```
The accepted non-error state is explicit and narrow.

### **[FALSEY-RESULT]** Banned: falsey `Result` conversion
```rust
fn load_registry(path: &Path) -> Vec<RegistryEntry> {
    match std::fs::read_to_string(path) {
        Ok(text) => parse_registry(&text).unwrap_or_default(),
        Err(_) => vec![],
    }
}
```

**Correct shape:**
```rust
fn load_registry(path: &Path) -> Result<Vec<RegistryEntry>, RegistryError> {
    let text = std::fs::read_to_string(path).map_err(RegistryError::Read)?;
    parse_registry(&text).map_err(RegistryError::Parse)
}
```

### **[IF-REQUIRED-INVARIANT]** Banned: `if` for required invariant
```rust
fn save_document(path: Option<PathBuf>, content: String) -> Result<(), SaveError> {
    if path.is_none() {
        return Ok(());
    }

    std::fs::write(path.unwrap(), content).map_err(SaveError::Write)
}
```

**Correct shape:**
```rust
fn save_document(path: &Path, content: &str) -> Result<(), SaveError> {
    assert!(!content.is_empty(), "document content must not be empty");
    std::fs::write(path, content).map_err(SaveError::Write)
}
```
Better: make `path` non-optional before calling `save_document`.

### **[IFLET-INITIALIZED]** Banned: `if let` optional branch for initialized state
```rust
fn active_file_path(state: &AppState) -> Option<&Path> {
    if let Some(path) = state.file.as_deref() {
        return Some(path);
    }

    None
}
```

**Correct shape:**
```rust
fn active_file_path(state: &ReadyAppState) -> &Path {
    state.file.as_path()
}
```
If unselected is a real product case, represent it as an enum and dispatch at the UI boundary, not in every runtime function.

### **[NESTED-IF-CHAIN]** Banned: nested if chain
```rust
fn command_for(state: &AppState) -> Option<&str> {
    if let Some(config) = &state.config {
        if let Some(runtime) = &config.runtime {
            if let Some(command) = &runtime.command {
                return Some(command);
            }
        }
    }
    None
}
```

**Correct shape:**
```rust
struct RuntimeConfig {
    command: RenderCommand,
}

struct AppConfig {
    runtime: RuntimeConfig,
}

fn command_for(config: &AppConfig) -> &RenderCommand {
    &config.runtime.command
}
```

---

## Bash Examples

### **[FALLBACK-CHAINS]** Banned: fallback chains
```bash
if command -v fd >/dev/null 2>&1; then
  fd -e md -t f
else
  find . -name '*.md'
fi
```

**Correct shape:**
```bash
: "${FINDER_COMMAND:?FINDER_COMMAND must be configured}"
exec $FINDER_COMMAND
```
Better: the app config names the command; doctor verifies it.

### **[EMPTY-OUTPUT-FAILURE]** Banned: empty output on failure
```bash
if ! output="$(renderer "$input" 2>/dev/null)"; then
  output=""
fi

printf '%s\n' "$output"
```

**Correct shape:**
```bash
set -euo pipefail

output="$(renderer "$input")"
printf '%s\n' "$output"
```
If the renderer fails, the script fails.

### **[PIPE-TRUE]** Banned: `|| true`
```bash
cleanup_artifact "$path" || true
```

**Correct shape:**
```bash
if [ -e "$path" ]; then
  cleanup_artifact "$path"
else
  printf 'cleanup path did not exist: %s\n' "$path" >&2
  exit 1
fi
```
Or if missing is truly accepted, make the accepted state explicit and narrow:
```bash
rm -f -- "$path"
```
But do not use this in diagnostic/build/test logic unless absence is an explicit contract.

### **[STATUS-LAUNDERING]** Banned: status laundering
```bash
if curl -s "$endpoint" >/tmp/response.json; then
  jq '.items // []' /tmp/response.json
else
  echo '[]'
fi
```

**Correct shape:**
```bash
set -euo pipefail

response="$(mktemp)"
headers="$(mktemp)"

curl -SsfD "$headers" "$endpoint" -o "$response"
jq -e '.items | type == "array"' "$response" >/dev/null
jq '.items' "$response"
```

### **[TEST-MODE-FAKE]** Banned: test-mode fake
```bash
if [ "${APP_ENV:-}" = "test" ]; then
  echo '{"ok": true, "items": []}'
  exit 0
fi

real_command "$@"
```

**Correct shape:**
```bash
real_command "$@"
```
Tests must use real fixture inputs and real outputs.

### **[SILENT-PROBING]** Banned: silent probing
```bash
if git remote get-url origin 2>/dev/null | grep -q github.com; then
  echo "github"
else
  echo "unknown"
fi
```

**Correct shape:**
```bash
remote_url="$(git remote get-url origin)"
case "$remote_url" in
  *github.com*) echo "github" ;;
  *) printf 'unsupported remote: %s\n' "$remote_url" >&2; exit 1 ;;
esac
```

---

## If Taxonomy

| If shape | Disposition |
| :--- | :--- |
| `if not value: return []` | banned |
| `if not value: return None/null` | banned |
| `if not value: return false` | banned |
| `if error: log/warn and continue` | banned |
| `if missing config: use default` | banned |
| `if dependency unavailable: fallback` | banned |
| `if test mode: fake boundary` | banned |
| `if optional initialized field: skip operation` | banned |
| `if exact domain variant: dispatch` | allowed |
| `if domain predicate: filter/partition` | allowed |
| `if boundary parser rejects invalid data` | allowed only in parser/validator |
| `if accepted error kind is exactly NotFound` | allowed if this is an explicit contract |
| nested `if` over optional state | banned; use total state or enum |
| `if` followed by assertion in branch | usually replace with direct assertion |
| `if` whose only purpose is to raise | replace with direct assertion/invariant call |

---

## Correct Replacements from First Principles

1. **Missing required state** → make the type total or assert initialization.
2. **Invalid external input** → parse at the boundary into a total model or fail structurally.
3. **Missing config** → setup/starter config generation; runtime validates complete config.
4. **Missing dependency** → doctor/setup/tool provisioning; runtime assumes dependency.
5. **External command failure** → command fails; do not convert to empty output.
6. **Empty result** → valid only if the domain explicitly admits emptiness.
7. **Multiple cases** → enum/tag/variant with exhaustive match.
8. **Optional UI state** → explicit UI state machine, not nullable core state.
9. **Cleanup** → classify the only accepted absence/error; propagate all others.
10. **Test mode** → no runtime test branches; tests use real boundaries or do not claim proof.

---

## **[NESTED-IF-BAN]** Nested If Ban

Nested `if` blocks over missing/optional/falsy state are banned.

They almost always indicate that invalid states are being carried too far into the core. Normalize once at the boundary, then operate on total types.

If nesting seems necessary:
- extract a boundary parser/validator;
- introduce an enum/tagged state;
- assert invariants at the top;
- use exhaustive dispatch on real domain cases.

Do not build pyramids of permission for code to proceed.

---

## **[FAIL-OPEN-BAN]** Fail-Open Ban

A branch fails open if the failing path returns any value that allows the caller to keep treating the operation as successful or empty-but-valid.

Fail-open return values include:
- `None`, `null`, `undefined`
- `false`
- `[]`
- `{}`
- `""`
- `0`
- `Ok(empty)`
- `{ ok: true, warnings: [...] }`
- `exit 0`
- empty stdout
- logged warning with continued execution

Fail-open branches are banned.

---

## Assertion Style Guide

Use assertions to state admissible runtime worlds.

**Good:**
```python
assert config.runtime.command is not None
```
```ts
invariant(config.runtime.command.length > 0, "runtime.command is required");
```
```rust
assert!(!config.runtime.command.as_str().is_empty(), "runtime.command is required");
```

**Bad:**
```python
if config.runtime.command is None:
    raise AssertionError("runtime.command is required")
```
```ts
if (!config.runtime.command) {
  throw new Error("runtime.command is required");
}
```
```rust
if config.runtime.command.is_empty() {
    return Err("runtime.command is required".into());
}
```
The bad form creates a branch-shaped surface. Branch-shaped surfaces accumulate fallbacks.

For TypeScript, define a canonical helper:
```ts
export function invariant(condition: unknown, message: string): asserts condition {
  if (!condition) {
    throw new AssertionError(message);
  }
}
```
Then ban local ad hoc versions.



---

## Runtime If Red Flags

Every `if` in runtime code must be treated as suspicious until classified.

**Banned conditions:**
- checking whether required state exists;
- checking whether required config exists;
- checking whether a critical dependency is installed;
- checking whether a subprocess/network/file operation failed and then continuing;
- checking truthiness/falsiness instead of structured state;
- checking test/smoke/debug mode to substitute fake behavior;
- checking optional nested fields after initialization;
- checking for empty result and returning another empty result.

**Allowed conditions:**
- exhaustive dispatch over explicit domain variants;
- domain filtering/partitioning where both outcomes are valid;
- a single boundary parser/validator rejecting external input;
- explicitly accepted error kind, such as NotFound in cleanup, with every other error propagated.

If a condition is required for correctness, assert it.
If a condition is a real case, encode it as a case.
If a condition is an error, fail.

---

## Summary Principles

- **Runtime confidence**: Runtime code should be confident after the boundary. Obsequious code asks every value whether it is allowed to proceed. Correct code constructs an admissible world, asserts it, and then operates inside it.
- **Rules of engagement**: No fail-open branches. No falsy error values. No empty-list laundering. Assert invariants. Dispatch only on real domain cases.
