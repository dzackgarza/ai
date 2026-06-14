# Policy Red Flags Database

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

## **[LANG-AGNOSTIC]** Language-Agnostic Red Flags

| Red flag | Why it matters |
| :--- | :--- |
| **[RUNTIME-DEFAULTS] Runtime defaults** | Defaults preserve missing-data paths and force weak proof obligations. |
| **[FALLBACK-CHAINS] Fallback chains** | The app makes unreviewed decisions for the user. |
| **[OPTIONAL-DEPS] Optional critical dependencies** | Lets the app pretend required tools are optional. |
| **[PARTIAL-SUCCESS] Partial success objects** | Converts failed work into "mostly OK." |
| **[BOOLEAN-FLAGS] Boolean mode flags** | Tests can force branches instead of constructing real state. |
| **[HELPER-BOUNDARY] Helper-local tests for boundary bugs** | Proves the patch, not the behavior under review. |
| **[EXACT-STRING] Exact string assertions** | Often prove message plumbing, not semantic failure. |
| **[STRINGLY-ERRORS] Stringly owned errors** | Makes exact-message testing and catch-all handling likely. |
| **[OPTIONAL-STATE] Optional core state** | Keeps "maybe initialized" logic alive throughout the app. |
| **[AMBIENT-DISCOVERY] Ambient discovery** | Infers behavior from machine state instead of explicit contract. |
| **[GLOBAL-STATE] Hidden global state** | Shell/env/home/cache state becomes unreviewed source of truth. |
| **[NON-PROOF-TESTS] Non-proof tests** | Test-shaped artifacts that future agents can cite as proof. |
| **[QUARANTINE-LANG] Quarantine language** | "Smoke," "non-proof," "legacy," "diagnostic-only" can launder slop. |
| **[DELETION-BURDEN] Deletion without burden transfer** | Removes evidence that a problem existed. |
| **[LOCAL-QC] Local QC surfaces** | Gives agents narrower gates to pass. |
| **[BYPASS-COMMENTS] Bypass comments** | Turns validator failure into validator silence. |
| **[LEGACY-SHIMS] Compatibility/legacy shims** | Preserves wrong prior designs in pre-launch code. |
| **[DEFENSIVE-GUARDS] Defensive guards in trusted core** | Bloats happy path and hides invariant violations. |
| **[HYPOTHETICAL-PATH] Hypothetical-path code** | Adds branches for failures never observed; turns absence-of-evidence into code without proof the path exists. |
| **[UNTYPED-IMPORT] Untyped dependency ingress** | Missing stubs or `py.typed` lets an external library enter owned code as `Any`; remediation restores a typed boundary rather than changing libraries. |
| **[DYNAMIC-FILE] Dynamic file creation from code** | Writing configs, scripts, or any file from raw strings in code or shell destroys observability and is extremely brittle — the file cannot be reviewed, diffed, or tracked independently. |
| **[INLINE-STRINGS-DATA] Inline large strings / prompts as data** | Embedding agent prompts, user-facing messages, or any non-code text (>5 lines or containing structured instructions) directly in source files conflates code with data. Strings are not reviewable as separate artifacts, cannot be independently versioned, and encourage ad-hoc editing that bypasses normal review. |
| **[CODE-IN-CODE] Code within code / embedded cross-language programs** | Python that assembles and runs bash strings, shell scripts that inline Python/Perl, or any program that generates another program inline. Destroys syntax checking, breaks static analysis, and hides the real intent inside string concatenation. The embedded language cannot be reviewed, linted, or debugged independently. |
| **[ADMIN-COMPLETION] Administrative completion** | Issues/comments/docs replace implementation or proof. |

If a construct would let an agent preserve the appearance of correctness while weakening the obligation, treat it as a red flag even if the code currently works.

### **[VERBOSITY-COMPLEXITY]** Code Verbosity and Complexity Red Flags

These patterns produce code that is harder to read, maintain, and review — the opposite of concise, provably correct code. They are not always bridge-burning (some are style failures) but they reliably indicate that the author was optimizing for "looks complete" instead of "is correct."

| Red flag | Why it matters |
| :--- | :--- |
| **[FILLER-DOCS] Filler documentation** | JSDoc/docstrings/block comments that restate the signature add no information. They make the real code harder to scan and give agents a cheap "documentation" checkbox. |
| **[VERBOSE-COMMENTS] Overly verbose comments** | `// increment counter by 1` above `counter++` restates the obvious and buries real intent. |
| **[INTERMEDIATE-VARS] Unnecessary intermediate variables** | A variable assigned once and used on the next line as a "documentation step" adds length without clarity. |
| **[VERBOSE-NAMES] Verbose variable names that obscure intent** | `currentUserAuthenticationStatusBoolean` vs `isAuthenticated` — more characters, less meaning. Every reader must parse the longer name and still infer the type. |
| **[JUST-IN-CASE] "Just in case" code** | Unused parameters, dead code paths, unreachable branches, features built for hypothetical future needs. Every line that never executes is a review burden and a future confusion. |
| **[DEFENSIVE-EXCESS] Excessive defensive programming** | Superfluous null checks, try-catches, `is not None` guards, or validations on data that has already been validated upstream. These bloat the happy path and convert invariant violations into silent continuations. |
| **[BOILERPLATE] Boilerplate explosion** | Separate class/function/file for a trivial operation that should be a simple expression. Every extra artifact is a review surface. |
| **[OVER-ABSTRACTION] Over-abstraction** | Interface with exactly one implementation, factory that creates one concrete thing, strategy pattern wired for exactly two options that never diverge. |

---

## **[TEXTUAL-RED-FLAGS]** Cross-Cutting Textual Red Flags

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

## **[TESTING-RED-FLAGS]** Testing Red Flags

This section belongs in [test-guidelines](file:///home/dzack/ai/opencode/skills/test-guidelines/SKILL.md) and the pattern catalog.

| Pattern | Red flag |
| :--- | :--- |
| **[MOCK-STUB] Mock/fake/stub/simulation** | Directly prohibited unless it is outside proof/QC and not test-shaped. |
| **[TEST-GATING] `skip`, `xfail`, conditional test gating** | Masks runtime reality. |
| **[SMOKE-TEST] “Smoke” tests in test suite** | Often fake proof with softer branding. |
| **[HELPER-PATCH] Helper tests after review pressure** | Patch-shaped proof, not behavior proof. |
| **[OVERCLAIM] Test name overclaims** | Name says “existing config”; body passes `true`. |
| **[NO-FIXTURE] No real fixture** | Config/filesystem/network/process behavior tested without config/files/process. |
| **[TEST-EXACT-STRING] Exact string assertion** | Especially bad when the test supplied the string. |
| **[CONTENT-FREE] `is not None`, `len > 0`, “renders” without semantic assertion** | Content-free proof. |
| **[COVERED-ELSEWHERE] “Covered elsewhere” without test name/command** | Deletion laundering. |
| **[STOPPED-HELPER] Test would pass if production stopped calling helper** | Not protecting owned behavior. |
| **[FALLBACK-PROOF] Test proves a fallback** | The fallback probably should not exist. |
| **[MOCKED-IPC] Browser/E2E test with mocked IPC** | Honest-label laundering if called “smoke.” |

> [!NOTE]
> If the original review concern is boundary-level, helper-level tests cannot resolve it. They may supplement proof, but they do not close the burden.

---

## **[PYTHON-RED-FLAGS]** Python Red Flags

Python is especially rich in slop affordances.

### **[DEFAULTS-OPTIONALITY]** Defaults and Optionality
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

### **[FALLBACKS-FAKE-RESILIENCE]** Fallbacks and Fake Resilience
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

### **[TYPE-PROOF-ESCAPE]** Type/Proof Escape Hatches
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

### **[UNTYPED-IMPORT]** Untyped Dependency Ingress
```text
mypy: Skipping analyzing "library": module is installed, but missing library stubs or py.typed marker [import-untyped]
```
This means the import would enter owned code as `Any`. Treat it as a boundary problem, not a library-selection problem.

Red flags:
- direct imports of the untyped dependency throughout owned code;
- replacing a correct library with a weaker typed-looking library to appease mypy;
- `# type: ignore[import-untyped]`, `ignore_missing_imports`, or local mypy excludes;
- wrappers that re-export untyped objects without named project-owned types.

Allowed detector carve-out: a global-QC-owned typed-firewall convention may exempt the single module that imports the untyped dependency. That module must be named and shaped as a boundary, and global QC must still forbid direct imports elsewhere.

### **[MOCK-TEST-POISON]** Mock/Test Poison
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

### **[PYTHON-HEURISTIC]** Python-Specific Review Heuristic
> [!TIP]
> If a Python test directly calls a helper with a synthetic boolean, None, or supplied error string, ask whether the real file/config/process boundary is being avoided.

---

## **[TS-RED-FLAGS]** JavaScript / TypeScript Red Flags

### **[TYPE-ESCAPE]** Type Escape
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

### **[RUNTIME-DEFAULTS-FALLBACKS]** Runtime Defaults and Fallbacks
```ts
value ?? defaultValue
value || defaultValue
function f(x = defaultValue) {}
const { x = defaultValue } = obj
process.env.X || "default"
localStorage.getItem("x") ?? "default"
```
In TypeScript/JavaScript code, these often hide missing config/state. Prefer explicit config and fatal validation.

### **[ASYNC-LAUNDERING]** Async Laundering
```ts
promise.catch(console.error)
void asyncOperation()
setTimeout(...); // no cancellation/ownership
useEffect(() => { asyncCall().then(setState) }, [...]) // no stale guard when visible state can change
```
Race fixes can be aligned when stale async writes can overwrite user-visible state. They are not micro-optimizations.

### **[TEST-LAUNDERING]** Test Laundering
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

### **[CONFIG-QC]** Config/QC Red Flags
- Excluding playwright.config.ts or test helper files from tsconfig.
- Separate tsconfig that misses owned test helpers.
- Local lint/typecheck scripts instead of global QC.
Excluding config/helper files from typechecking is a proof-surface gap, not a style nit.

---

## **[RUST-RED-FLAGS]** Rust Red Flags

Rust has strong types, so agent slop often appears as `Option`, fallback defaults, string errors, and swallowed `Result`s.

### **[DEFAULTS-OPTIONALITY]** Defaults and Optionality
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

### **[SWALLOWED-ERRORS]** Swallowed Errors
```rust
let _ = fs::remove_file(path);
result.ok();
filter_map(Result::ok)
read_dir(...).flatten()
match err { _ => Ok(()) }
if path.exists() { fs::remove_file(path).ok(); }
```
These are classic fail-fast violations. The only acceptable ignored error should be explicitly classified, e.g. `NotFound`.

### **[STRINGLY-ERRORS]** Stringly Errors
```rust
Result<T, String>
Err("missing config".into())
assert_eq!(error, "missing config")
```
For owned failures, prefer error enums. Strings are rendered at the edge.

### **[HELPER-BRANCH-PROOF]** Helper-Branch Proof
```rust
require_or_default(None, true, "...", || default)
```
This is a red flag because it tests branch selection, not real config state. The global rule should be “no defaults,” making the helper unnecessary.

### **[PROCESS-LIFECYCLE]** Process Lifecycle
```rust
timeout(duration, child.wait_with_output())
```
without kill/drop semantics is suspicious. Timeout must not leave owned processes running.

### **[ATTRIBUTE-BYPASSES]** Attribute Bypasses
```rust
#[allow(...)]
#[cfg(test)] fake implementation
#[ignore]
#[should_panic(expected = "...")]
```
These may be valid in rare cases, but they should trigger scrutiny. `expected = "..."` is exact-string proof unless the string is a public contract.

---

## **[BASH-RED-FLAGS]** Bash / Shell Red Flags

Shell is where agents often hide diagnostic failure.

### **[SUPPRESSION-FALLBACK]** Suppression and Synthetic Fallback
```bash
cmd 2>/dev/null || echo "not found"
cmd >/dev/null 2>&1
grep pattern file || true
command -v tool || fallback
curl -s URL | jq '.expected.path'
```
These replace raw feedback with the agent’s prior. Diagnostic commands must preserve stdout, stderr, and exit status.

### **[WEAK-SHELL]** Weak Shell Settings
```bash
set +e
# no set -euo pipefail
pipeline_without_pipefail
```
Shell scripts that own setup/build/test behavior should fail loudly.

### **[FALLBACK-CHAINS]** Fallback Chains
```bash
if command -v fd; then fd ...; else find ...; fi
if command -v rofi; then rofi; elif command -v dmenu; then dmenu; fi
```
For runtime behavior, these should usually be config choices, not ambient discovery.

### **[GLOBAL-MUTATION]** Global Mutation
```bash
pip install ...
npm install -g ...
curl ... | bash
sudo apt install ...
```
These violate runner-first/tool-provisioning policy unless explicitly authorized as system administration.

### **[CLEANUP-LAUNDERING]** Cleanup Laundering
```bash
rm -rf something || true
find . -name cache -exec rm -rf {} + 2>/dev/null
```
Sometimes cleanup suppression is intentional, but it must be marked non-diagnostic and must not be copied into investigation/build/test recipes.

---

## **[SQL-RED-FLAGS]** SQL / Database Red Flags

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

## **[CONFIG-SCHEMA]** Config and Schema Red Flags

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

## **[PR-REVIEW]** PR / Review Red Flags

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

## **[QC-TARGETS]** Mechanical QC Targets

These can be compiled into global QC detectors to act as warning or error gates.

### **[TEXT-GREP-CANDIDATES]** Text / Grep Candidates
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
- `import-untyped`, `missing library stubs`, `py.typed`, `ignore_missing_imports`

### **[AST-PYTHON]** AST-Level Candidates (Python)
- `ExceptHandler` for `ImportError` / broad `Exception`
- `Call` to `os.getenv` or `dict.get` with default value
- Subscript/annotation `Any`
- `pytest` skip/xfail markers
- `unittest.mock` imports

### **[AST-TYPESCRIPT]** AST-Level Candidates (TypeScript)
- `TSAnyKeyword`
- `TSAsExpression` to `any`
- `TSNonNullExpression` (`!`)
- `CallExpression` `jest.mock` / `vi.mock`
- `test.skip` / `describe.skip`
- `LogicalExpression` `||` with literal fallback
- `NullishCoalescingExpression` with literal fallback

### **[AST-RUST]** AST-Level Candidates (Rust)
- Method call `unwrap_or`, `unwrap_or_default`, `ok`
- Attributes `serde(default)`, `allow`, `ignore`
- `Result<T, String>`
- `let _ =` for calls returning a `Result`

### **[AST-BASH]** AST-Level Candidates (Bash)
- Redirecting stderr to `/dev/null`
- `command -v` gating runtime behavior
- `pip`/`npm` global installation commands
- Pipelines without `pipefail` set
- `curl -s` used in diagnostic contexts

---

## **[NON-DISCRIM-ASSERTIONS]** Non-Discriminating Assertion Red Flags

These assertions are banned in ordinary project tests because they do not meaningfully
raise confidence in repository-owned behavior:

- **[LA-EXISTENCE]** existence-only assertions;
- **[LA-VISIBILITY]** visibility-only assertions;
- **[LA-TRUTHY]** truthiness / non-empty assertions;
- **[LA-SHAPE]** type-only or shape-only assertions;
- **[LA-NO-THROW]** no-throw assertions;
- **[LA-STRING]** exact string assertions;
- **[LA-SOURCE-TEXT]** source-text / AST / implementation-shape assertions;
- **[LA-SOURCE-TEXT]** assertions for absence of banned constructs;
- **[LA-HELPER-BRANCH]** helper-only branch assertions;
- **[LA-BOOLEAN-FORCING]** boolean branch-forcing tests;
- **[LA-MOCK-COUNT]** mock/spies/call-count assertions;
- **[LA-SNAPSHOT]** broad snapshots where exact output is not public contract;
- **[LA-IMPORT]** import/module-load/constructor tests;
- **[LA-STATUS-LABEL]** status-label assertions;
- **[LA-LOG-WARNING]** log/warning assertions;
- **[LA-HTTP-STATUS]** HTTP status-only assertions;
- **[LA-DB-COUNT]** database count/existence assertions;
- **[LA-ROUND-TRIP]** round-trip tests where both directions share the same implementation;
- **[LA-TIMING-PERF]** timing/performance assertions in ordinary tests;
- **[LA-NO-CONSOLE-ERRORS]** no-console-errors as sole proof.

For every such assertion, require one of:
1. replace with real boundary proof;
2. move to global QC if it is code-shape policing;
3. record the proof burden as unresolved.

For the canonical inventory of these banned patterns and their allowed replacements, see the [Test Proof Rules](file:///home/dzack/ai/opencode/skills/policy-index/references/test-proof-rules.md).

---



## Remediation Boundary

This detector-facing catalog names suspicious constructs and maps them to policy.
Fixer-side remediation instructions live in `remediations.md` and are loaded only after
triage assigns a `POLICY.*` code.
