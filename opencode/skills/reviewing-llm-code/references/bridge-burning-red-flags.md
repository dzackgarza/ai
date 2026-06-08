# Bridge-Burning Red Flags Reference Catalog

A red flag is any construct that gives the agent a way to preserve a success signal without satisfying the original obligation. These patterns are suspicious because they preserve evaluator silence while weakening the original obligation. They are not ordinary style smells.

When one appears, ask:
1. What obligation does this construct avoid?
2. Which validator would it silence?
3. What original problem caused it to be introduced?
4. Is that problem solved at the owned boundary?
5. Could a future agent cite this artifact as proof?
6. Could a future agent reintroduce this same construct if deleted?

> [!IMPORTANT]
> **Burden Disposition Rule:** The correct response to a red flag is not automatically deletion. It is burden disposition: solved, invalidated, transferred to a real proof surface, or explicitly recorded as unresolved. Otherwise, agents will turn the red-flag catalog into another deletion-laundering mechanism.

## Language-Agnostic Red Flags

| Red flag | Why it matters | Typical fix |
| :--- | :--- | :--- |
| **Runtime defaults** | Defaults preserve missing-data paths and force weak proof obligations. | Ship a complete config; validate at startup; fail if missing. |
| **Fallback chains** | The app makes unreviewed decisions for the user. | Explicit config selection; no automatic alternate path. |
| **Optional critical dependencies** | Lets the app pretend required tools are optional. | Doctor/setup verifies; runtime assumes. |
| **Partial success objects** | Converts failed work into “mostly OK.” | Operation succeeds completely or fails. |
| **Boolean mode flags** | Tests can force branches instead of constructing real state. | Split APIs or use explicit enum states. |
| **Helper-local tests for boundary bugs** | Proves the patch, not the behavior under review. | Test the source-of-truth boundary. |
| **Exact string assertions** | Often prove message plumbing, not semantic failure. | Structured error kinds; assert error type/key. |
| **Stringly owned errors** | Makes exact-message testing and catch-all handling likely. | Domain error enums/classes. |
| **Optional core state** | Keeps “maybe initialized” logic alive throughout the app. | Normalize once; core state is total. |
| **Ambient discovery** | Infers behavior from machine state instead of explicit contract. | Config declares; doctor verifies. |
| **Hidden global state** | Shell/env/home/cache state becomes unreviewed source of truth. | Explicit project config. |
| **Non-proof tests** | Test-shaped artifacts that future agents can cite as proof. | Remove or move to non-QC diagnostic command. |
| **Quarantine language** | “Smoke,” “non-proof,” “legacy,” “diagnostic-only” can launder slop. | Require burden disposition. |
| **Deletion without burden transfer** | Removes evidence that a problem existed. | Solve, invalidate, or record the original burden. |
| **Local QC surfaces** | Gives agents narrower gates to pass. | Delegate to global QC only. |
| **Bypass comments** | Turns validator failure into validator silence. | Fix the code or escalate. |
| **Compatibility/legacy shims** | Preserves wrong prior designs in pre-launch code. | Replace, do not shim. |
| **Defensive guards in trusted core** | Bloats happy path and hides invariant violations. | Validate at boundary; assert internally. |
| **Hypothetical-path code** | Adds branches for failures never observed; turns absence-of-evidence into code without proof the path exists. | Require observed failure before adding handling; if invariant, assert. |
| **Administrative completion** | Issues/comments/docs replace implementation or proof. | Treat them as records, not completion. |

If a construct would let an agent preserve the appearance of correctness while weakening the obligation, treat it as a red flag even if the code currently works.

---

## Cross-Cutting Textual Red Flags

These words and phrases should trigger scrutiny:

```text
default
fallback
best effort
graceful
continue
warning
optional
legacy
compatibility
quarantine
smoke
non-proof
diagnostic-only
temporary
scaffold
future work
out of scope
covered elsewhere
should not happen
safe fallback
if available
if installed
try X else Y
```

They are not automatic findings. They are prompts to ask:
- **What obligation is being weakened?**
- **What would fail if this path were removed?**
- **Is this hiding an unresolved proof burden?**

---

## Testing Red Flags

This section belongs in [test-guidelines](file:///home/dzack/ai/opencode/skills/test-guidelines/SKILL.md) and the pattern catalog.

| Pattern | Red flag |
| :--- | :--- |
| **Mock/fake/stub/simulation** | Directly prohibited unless it is outside proof/QC and not test-shaped. |
| **`skip`, `xfail`, conditional test gating** | Masks runtime reality. |
| **“Smoke” tests in test suite** | Often fake proof with softer branding. |
| **Helper tests after review pressure** | Patch-shaped proof, not behavior proof. |
| **Test name overclaims** | Name says “existing config”; body passes `true`. |
| **No real fixture** | Config/filesystem/network/process behavior tested without config/files/process. |
| **Exact string assertion** | Especially bad when the test supplied the string. |
| **`is not None`, `len > 0`, “renders” without semantic assertion** | Content-free proof. |
| **“Covered elsewhere” without test name/command** | Deletion laundering. |
| **Test would pass if production stopped calling helper** | Not protecting owned behavior. |
| **Test proves a fallback** | The fallback probably should not exist. |
| **Browser/E2E test with mocked IPC** | Honest-label laundering if called “smoke.” |

> [!NOTE]
> If the original review concern is boundary-level, helper-level tests cannot resolve it. They may supplement proof, but they do not close the burden.

---

## Python Red Flags

Python is especially rich in slop affordances.

### Defaults and Optionality
```python
os.getenv("X", "default")
config.get("key", default)
getattr(obj, "field", default)
dict.setdefault(...)
defaultdict(...)
field: str | None
Optional[str]
arg: str = "default"
Field(default=...)
BaseModel(... = None)
```
These are red flags when the value is required after initialization. The correct shape is complete config plus validation. Optionality should be at the boundary only.

### Fallbacks and Fake Resilience
```python
try:
    import package
except ImportError:
    ...

try:
    value = real()
except Exception:
    value = fallback

result = maybe() or default
contextlib.suppress(...)
except Exception:
    pass
```
These should usually be banned. If the dependency or operation is required, failure is the correct behavior.

### Type/Proof Escape Hatches
```python
Any
dict[str, Any]
cast(Any, x)
# type: ignore
# noqa
# pragma: no cover
pytest.mark.skip
pytest.mark.xfail
```
These are not small local conveniences. They are validator-silencing tools.

### Mock/Test Poison
```python
unittest.mock
MagicMock
monkeypatch
mocker
responses
respx
freezegun
moto
fake filesystem libraries
```
Under the established policy, these belong in prohibited-pattern examples, not positive guidance.

### Python-Specific Review Heuristic
> [!TIP]
> If a Python test directly calls a helper with a synthetic boolean, None, or supplied error string, ask whether the real file/config/process boundary is being avoided.

---

## JavaScript / TypeScript Red Flags

### Type Escape
```ts
any
unknown as X
as any
as unknown as
Record<string, any>
Partial<T> in normalized/core state
// @ts-ignore
// @ts-expect-error
eslint-disable
skipLibCheck
```
`skipLibCheck` may sometimes be tolerated for external libraries, but it is still a red flag and should not be extended to owned code or proof surfaces.

### Runtime Defaults and Fallbacks
```ts
value ?? defaultValue
value || defaultValue
function f(x = defaultValue) {}
const { x = defaultValue } = obj
process.env.X || "default"
localStorage.getItem("x") ?? "default"
```
In TypeScript/JavaScript code, these often hide missing config/state. Prefer explicit config and fatal validation.

### Async Laundering
```ts
promise.catch(console.error)
void asyncOperation()
setTimeout(...); // no cancellation/ownership
useEffect(() => { asyncCall().then(setState) }, [...]) // no stale guard when visible state can change
```
Race fixes can be aligned when stale async writes can overwrite user-visible state. They are not micro-optimizations.

### Test Laundering
```ts
jest.mock(...)
vi.mock(...)
page.addInitScript(mock IPC)
test.skip(...)
test.fixme(...)
expect(...).toBeTruthy()
expect(...).not.toBeNull()
```
A Playwright test with mocked Tauri IPC is a red flag even if renamed `browser-smoke`. If it is not proof-bearing, it should not be in a proof-shaped path.

### Config/QC Red Flags
- Excluding playwright.config.ts or test helper files from tsconfig.
- Separate tsconfig that misses owned test helpers.
- Local lint/typecheck scripts instead of global QC.
Excluding config/helper files from typechecking is a proof-surface gap, not a style nit.

---

## Rust Red Flags

Rust has strong types, so agent slop often appears as `Option`, fallback defaults, string errors, and swallowed `Result`s.

### Defaults and Optionality
```rust
unwrap_or(...)
unwrap_or_default()
unwrap_or_else(...)
Option<T> in initialized AppState
#[serde(default)]
Default for runtime config
field: Option<T> for required values
```
For config, `serde(default)` is especially suspicious. If a user config exists, required fields should be required.

### Swallowed Errors
```rust
let _ = fs::remove_file(path);
result.ok();
filter_map(Result::ok)
read_dir(...).flatten()
match err { _ => Ok(()) }
if path.exists() { fs::remove_file(path).ok(); }
```
These are classic fail-fast violations. The only acceptable ignored error should be explicitly classified, e.g. `NotFound`.

### Stringly Errors
```rust
Result<T, String>
Err("missing config".into())
assert_eq!(error, "missing config")
```
For owned failures, prefer error enums. Strings are rendered at the edge.

### Helper-Branch Proof
```rust
require_or_default(None, true, "...", || default)
```
This is a red flag because it tests branch selection, not real config state. The global rule should be “no defaults,” making the helper unnecessary.

### Process Lifecycle
```rust
timeout(duration, child.wait_with_output())
```
without kill/drop semantics is suspicious. Timeout must not leave owned processes running.

### Attribute Bypasses
```rust
#[allow(...)]
#[cfg(test)] fake implementation
#[ignore]
#[should_panic(expected = "...")]
```
These may be valid in rare cases, but they should trigger scrutiny. `expected = "..."` is exact-string proof unless the string is a public contract.

---

## Bash / Shell Red Flags

Shell is where agents often hide diagnostic failure.

### Suppression and Synthetic Fallback
```bash
cmd 2>/dev/null || echo "not found"
cmd >/dev/null 2>&1
grep pattern file || true
command -v tool || fallback
curl -s URL | jq '.expected.path'
```
These replace raw feedback with the agent’s prior. Diagnostic commands must preserve stdout, stderr, and exit status.

### Weak Shell Settings
```bash
set +e
# no set -euo pipefail
pipeline_without_pipefail
```
Shell scripts that own setup/build/test behavior should fail loudly.

### Fallback Chains
```bash
if command -v fd; then fd ...; else find ...; fi
if command -v rofi; then rofi; elif command -v dmenu; then dmenu; fi
```
For runtime behavior, these should usually be config choices, not ambient discovery.

### Global Mutation
```bash
pip install ...
npm install -g ...
curl ... | bash
sudo apt install ...
```
These violate runner-first/tool-provisioning policy unless explicitly authorized as system administration.

### Cleanup Laundering
```bash
rm -rf something || true
find . -name cache -exec rm -rf {} + 2>/dev/null
```
Sometimes cleanup suppression is intentional, but it must be marked non-diagnostic and must not be copied into investigation/build/test recipes.

---

## SQL / Database Red Flags

Even if not central to the current repo, these are useful language-agnostic flags:
```text
INSERT OR IGNORE
ON CONFLICT DO NOTHING
upsert without proving identity
catch unique violation and continue
best-effort migration
nullable columns for required data
JSON blob for owned structured state
```
These often convert data-contract failures into silent partial success.
The correct shape is: schema enforces required data; migration fails if data violates invariant; application owns explicit repair/migration path.

---

## Config and Schema Red Flags

Config is where “no defaults” pays off most.

Red flags:
```text
optional config sections
partial config accepted
defaults mixed into loader
config_exists boolean
config discovered from many locations
missing key warning
malformed config falls back
schema allows extra unknown keys
stringly config mode names
```
Better policy: A complete generated config is required. Startup validates it. Malformed, partial, or unknown config fails. No runtime defaulting. This removes huge classes of tests and fallback logic.

---

## PR / Review Red Flags

These catch laundering through human/agent review layers:
```text
“fixed” / “done” / “addressed” with no disposition
resolved thread with no visible reply
deleted artifact with no burden disposition
renamed artifact to smoke/basic/legacy/non-proof
opened issue and treated as completion
“covered elsewhere” with no exact test/command
“not counted as proof” while still in test suite
accepted review comment wholesale
rejected review comment wholesale
```
The correct pattern is: feedback claim disposition, remediation disposition, policy basis, artifact/burden disposition, audit anchor.

---

## Mechanical QC Targets

These can be compiled into global QC detectors to act as warning or error gates.

### Text / Grep Candidates
- `unwrap_or`, `unwrap_or_default`, `serde(default)`
- `Result<.*, String>`, `let _ =`
- `.filter_map(Result::ok)`, `.flatten()`
- `# type: ignore`, `# noqa`, `# pragma: no cover`
- `@ts-ignore`, `eslint-disable`
- `as any`, `as unknown as`
- `jest.mock`, `vi.mock`, `MagicMock`, `monkeypatch`
- `pytest.mark.skip`, `pytest.mark.xfail`
- `2>/dev/null`, `|| true`
- `npm install -g`, `pip install`, `curl | bash`
- `fallback`, `default`, `best effort`, `graceful`, `smoke`, `non-proof`, `quarantine`, `covered elsewhere`

### AST-Level Candidates (Python)
- `ExceptHandler` for `ImportError` / broad `Exception`
- `Call` to `os.getenv` or `dict.get` with default value
- Subscript/annotation `Any`
- `pytest` skip/xfail markers
- `unittest.mock` imports

### AST-Level Candidates (TypeScript)
- `TSAnyKeyword`
- `TSAsExpression` to `any`
- `TSNonNullExpression` (`!`)
- `CallExpression` `jest.mock` / `vi.mock`
- `test.skip` / `describe.skip`
- `LogicalExpression` `||` with literal fallback
- `NullishCoalescingExpression` with literal fallback

### AST-Level Candidates (Rust)
- Method call `unwrap_or`, `unwrap_or_default`, `ok`
- Attributes `serde(default)`, `allow`, `ignore`
- `Result<T, String>`
- `let _ =` for calls returning a `Result`

### AST-Level Candidates (Bash)
- Redirecting stderr to `/dev/null`
- `command -v` gating runtime behavior
- `pip`/`npm` global installation commands
- Pipelines without `pipefail` set
- `curl -s` used in diagnostic contexts

---

## Non-Discriminating Assertion Red Flags

These assertions are banned in ordinary project tests because they do not meaningfully
raise confidence in repository-owned behavior:

- existence-only assertions;
- visibility-only assertions;
- truthiness / non-empty assertions;
- type-only or shape-only assertions;
- no-throw assertions;
- exact string assertions;
- source-text / AST / implementation-shape assertions;
- assertions for absence of banned constructs;
- helper-only branch assertions;
- boolean branch-forcing tests;
- mock/spies/call-count assertions;
- broad snapshots where exact output is not public contract;
- import/module-load/constructor tests;
- status-label assertions;
- log/warning assertions;
- HTTP status-only assertions;
- database count/existence assertions;
- round-trip tests where both directions share the same implementation;
- timing/performance assertions in ordinary tests;
- no-console-errors as sole proof.

For every such assertion, require one of:
1. replace with real boundary proof;
2. move to global QC if it is code-shape policing;
3. record the proof burden as unresolved.

For the canonical inventory of these banned patterns and their allowed replacements, see the [Banned Test Shapes Catalog](file:///home/dzack/ai/opencode/skills/test-guidelines/references/banned-test-shapes.md).

---

## Final Principle

> **Agent-resistant codebases should be designed so that the easiest code to write is also the hardest code to fake.**

Defaults, fallbacks, mocks, skips, helper proofs, string errors, and local QC gates all make faking easier. The bridge-burning policies remove those moves from the game.

