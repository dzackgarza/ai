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

For the canonical inventory of these banned patterns and their allowed replacements, see the [Banned Test Shapes Catalog](file:///home/dzack/ai/opencode/skills/test-guidelines/references/banned-test-shapes.md).

---

## **[REMEDIATION-POLICIES]** Remediation Policies

A red flag says "this is suspicious." A remediation policy says "replace it with this exact shape." Every remediation converts a slop-enabling pattern into a fail-loud, minimal-cruft equivalent.

### **[FALLBACK-HEDGE]** Remediation: Fallback / Optional-Dependency / File-Availability Hedge

**Slop pattern:** A guard checks whether a dependency, file, binary, or resource exists before using it, with a silent fallback when absent.

```python
# BAD: silent hedge
if shutil.which("ffmpeg"):
    subprocess.run(["ffmpeg", ...])
else:
    logger.warning("ffmpeg not found, skipping")

# BAD: optional critical dependency
try:
    import magic
except ImportError:
    magic = None
```

**Remediation:** Assert availability at the program boundary. If the resource is required, failure to find it is a hard error. Do not provide a silent branch.

```python
# Remediation: boundary assertion
assert shutil.which("ffmpeg"), "ffmpeg is required for video processing"
subprocess.run(["ffmpeg", ...])
```

Remediation applies when:
- The dependency, file, or binary is required for the operation being performed.
- The app controls deployment (it can guarantee the dependency is present).
- The only purpose of the guard is to avoid an error that would be correct to raise.

Do not apply remediation when:
- The app legitimately supports multiple optional backends chosen by config.
- The resource is genuinely external and its absence is a valid runtime condition (e.g., network availability for a cache).

### **[SWALLOW-CATCH]** Remediation: try/catch That Swallows or Hedges

**Slop pattern:** A try/catch around an operation that is expected to succeed, converting a useful diagnostic into a silent continuation or a weak log line.

```python
# BAD: swallows diagnostic
try:
    result = api_call()
except Exception:
    result = None

# BAD: hedges with a log that no one reads
try:
    data = read_file(path)
except Exception as e:
    logger.error(f"failed to read {path}: {e}")
    data = []
```

**Remediation:** Let the error propagate. If the caller cannot handle the error, it should not catch it. If a specific error type is expected and recoverable, catch only that type and handle it in the same scope.

```python
# Remediation: propagate
data = read_file(path)  # raises if file is missing or unreadable

# When recovery IS the intent: narrow and handle immediately
try:
    config = read_config(path)
except FileNotFoundError:
    config = default_config()  # explicit recovery for a known condition
```

Remediation applies when:
- The try block wraps a single operation (not a sequence where partial failure is meaningful).
- The catch clause is broad (`Exception`, bare `except`, or a type that does not match the recoverable error).
- Recovery produces a sentinel value (`None`, `[]`, `""`, `False`) distinct from real results.

### **[DATA-PEEK]** Remediation: Data-Peeking Inside Loops

**Slop pattern:** A loop that checks a condition on each element and routes logic inside the loop body, mixing filtering with processing and making the control flow harder to read.

```python
# BAD: peeking inside the loop
results = []
for item in items:
    if item.status == "active":
        if item.owner is not None:
            results.append(process(item))
        else:
            logger.warning(f"item {item.id} has no owner")
    # items with other statuses are silently ignored
```

**Remediation:** Filter and assert invariants before the loop. The loop body should only contain the processing logic, with preconditions already satisfied.

```python
# Remediation: filter then process
active = [i for i in items if i.status == "active"]
assert all(i.owner is not None for i in active), "all active items must have an owner"
results = [process(i) for i in active]
```

Remediation applies when:
- The filter conditions are knowable before the loop (no dependence on loop-local state).
- Filtering and processing can be separated without changing semantics.
- The loop body has 2+ conditional branches that route on element properties.

### **[NESTED-CONDITIONAL]** Remediation: Nested / Stacked Conditional Chains

**Slop pattern:** A cascade of `if`/`elif`/`else` that branches on a single discriminant (type, enum, status, state) with implicit fall-through for unhandled cases.

```python
# BAD: stacked if/elif chain with implicit unhandled cases
if event.type == "click":
    handle_click(event)
elif event.type == "focus":
    handle_focus(event)
elif event.type == "blur":
    handle_blur(event)
# other event types silently ignored
```

**Remediation:** Use a match/case (Python 3.10+, TypeScript, Rust, etc.) or an explicit dispatch table that enumerates all expected cases and fails hard on unexpected input.

```python
# Remediation (match/case): explicit, exhaustive, fails on unexpected
match event.type:
    case "click": handle_click(event)
    case "focus": handle_focus(event)
    case "blur":  handle_blur(event)
    case _:       raise ValueError(f"unexpected event type: {event.type}")

# Remediation (dispatch table): equally explicit
_HANDLERS = {
    "click": handle_click,
    "focus": handle_focus,
    "blur":  handle_blur,
}
handler = _HANDLERS.get(event.type)
assert handler is not None, f"unexpected event type: {event.type}"
handler(event)
```

Remediation applies when:
- The chain is 3+ branches on the same discriminant.
- The default/else branch is missing, empty, or just logs and continues.
- The discriminant is a bounded set (enum, string literal union, known type variants).

### **[DYNAMIC-FILE-CREATION]** Remediation: Dynamic File / Config Creation from Code

**Slop pattern:** Code that writes a file (config, script, data file) by assembling content from raw strings, shell heredocs, or inline byte buffers — making the content invisible to review, diff, and static analysis.

```python
# BAD: writing config from a string literal in code
config_content = f"""
[server]
host = {host}
port = {port}
timeout = {timeout}
"""
Path("/etc/app/config.ini").write_text(config_content)

# BAD: generating a JSON config from a dict that was constructed ad-hoc
# (same problem — no independent file to review)
```

**Remediation:** Commit a static version of the file as a tracked artifact. Read or copy it at runtime. If dynamic content is genuinely required (not for config — for user data), use a real templating engine (Jinja2, Mustache, etc.) with a template file that IS the reviewed artifact.

```python
# Remediation: tracked static file, read at runtime
config = configparser.ConfigParser()
config.read("/etc/app/config.ini")  # file is committed, reviewed, diffable

# When dynamic content IS genuinely needed: real template engine
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader("templates"))
rendered = env.get_template("report.html").render(data=data)
Path("/tmp/report.html").write_text(rendered)
```

Remediation applies when:
- The generated file is a config, script, or static data file the app owns.
- The content is assembled from string literals, f-strings, template literals, or shell heredocs inline in code.
- The file would be more reviewable, diffable, and auditable as a static committed artifact.

Do not apply remediation when:
- The app's express purpose IS file generation (template parser, code generator, build tool).
- The content comes from genuine user data, not from strings embedded in the app's own code.

### **[INLINE-STRINGS]** Remediation: Inline Large Strings / Prompts Embedded as Code

**Slop pattern:** Embedding agent prompts, user-facing messages, instruction blocks, or any text longer than ~5 lines directly in source files as string literals. This treats data (strings) as code, making the text invisible to separate review, unversioned independently, and vulnerable to ad-hoc inline edits that bypass normal review.

```python
# BAD: agent prompt embedded as a string literal in application code
PROMPT = """You are a helpful research assistant.
Analyze the following paper:
{paper_text}

Consider:
1. Main contributions
2. Methodology
3. Limitations

Provide a structured summary with citations.
"""
```

**Remediation:** Extract all non-code strings to a standard data file (TOML, YAML, JSON) keyed by label. Load them at runtime via a library. The data file is the reviewed, diffable artifact; the code is a thin accessor.

```toml
# prompts.toml — reviewed artifact, independently versioned
[paper_analysis]
template = """
You are a helpful research assistant.
Analyze the following paper:
{paper_text}

Consider:
1. Main contributions
2. Methodology
3. Limitations

Provide a structured summary with citations.
"""
```

```python
# Remediation: load from config, strings are data not code
import tomllib
with open("prompts.toml", "rb") as f:
    prompts = tomllib.load(f)
prompt = prompts["paper_analysis"]["template"].format(paper_text=paper_text)
```

Remediation applies when:
- The string is an agent prompt, instruction block, user-facing message, or any text that is primarily data rather than code logic.
- The string exceeds ~5 lines or contains structured multi-part instructions.
- The string would benefit from independent review, versioning, or editing by non-developers.

Do not apply remediation when:
- The string is a short label, error message, or single-line log format (< 5 lines, no structured sub-instructions).
- The string is part of a test assertion where proximity to the assertion logic matters for readability.

### **[IMPLICIT-STATE]** Remediation: Implicit / Defaulted / Discovered State

**Slop pattern:** The app relies on runtime defaults, ambient discovery (inferring config from machine state), hidden global state (shell/env/cache), or optional core state with "maybe initialized" logic — all of which bury configuration in unreviewable surfaces and make behavior depend on ephemeral external conditions.

These are distinct variants of the same failure: state that should be explicit is implicit, discoverable only by reading non-code surfaces.

**Remediation:** Declare all configuration explicitly in a committed project config file. Validate the config at startup; fail hard if values are missing or invalid. Core state is total — normalized once at initialization, never optional.

```
File layout:
  config/app.toml         ← reviewed, diffable, committed
  src/config/loader.py    ← reads app.toml, validates, fails on missing keys
  src/app.py              ← imports config, uses total (non-optional) state
```

Remediation applies when:
- Behavior changes based on ambient machine state (env vars, home dir, cache presence, installed tools).
- Core app state is `None | T` (optional) when it could be `T` after initialization.
- Configuration values have defaults that hide from explicit review.

Do not apply remediation when:
- The value is genuinely a runtime choice the user makes per-invocation (e.g., `--output-format json`).
- The ambient state is the domain (e.g., a file manager inspecting the filesystem).

### **[PARTIAL-RESULT]** Remediation: Partial / Sentinel Results

**Slop pattern:** An operation that can partially succeed produces a result object with some fields populated and others sentinel (None, empty, -1) — forcing every caller to check which parts are valid.

```python
# BAD: partial success object
result = fetch_data(url)
if result.status == "ok":
    process(result.data)
# else: caller must check every access
```

**Remediation:** An operation either succeeds completely or fails with a clear error. Do not return objects that are "mostly OK" with missing parts. If the operation genuinely has partial results, represent them as explicit alternatives (union type, enum variant, tagged sum).

```python
# Remediation: complete success or clear failure
data = fetch_data(url)  # raises if any part fails
# or, if partial results are domain-meaningful:
match result:
    case Complete(data=all_data): process(all_data)
    case Partial(data=some_data, missing=ids): handle_missing(ids)
    case Failure(error=err): raise err
```

Remediation applies when:
- A function returns a result where some fields can be `None`, empty, or otherwise sentinel after partial failure.
- Callers must check sentinel values on every access.
- A single success/failure boolean would be sufficient.

Do not apply remediation when:
- The domain genuinely models multiple valid outcomes (e.g., a batch job where some items succeed and others fail).
- The sentinel is the domain contract (e.g., `dict.get(key)` returns `None` for missing keys).

### **[BOOLEAN-MODE]** Remediation: Boolean Mode Parameters

**Slop pattern:** A function takes a boolean parameter that changes its behavior between two modes, forcing callers to read the function body to understand what each value means.

```python
# BAD: boolean mode flag
process_data(data, validate=True)   # what does False mean?
send_notification(user, urgent=False)  # which behavior is default?
```

**Remediation:** Split into separate functions with descriptive names, or use an explicit enum where each variant name describes the mode.

```python
# Remediation: split API
process_data_with_validation(data)
process_data_fast(data)

# Remediation: explicit enum
NotificationPriority = enum(ROUTINE, URGENT)
send_notification(user, NotificationPriority.URGENT)
```

Remediation applies when:
- The boolean controls which code path is taken (not just a simple toggle of a single behavior like `verbose`).
- The meaning of `True` vs `False` is not obvious from the function name alone.

Do not apply remediation when:
- The flag is a simple pass-through to a well-known standard library or external API that uses the same convention.

### **[BOUNDARY-BYPASS]** Remediation: Boundary Test Bypass

**Slop pattern:** A test for a boundary condition (e.g., a null input, an edge case, a security check) tests the helper function that performs the check rather than the boundary where the check is enforced.

```python
# BAD: tests the helper, not the boundary
def test_sanitize_input():
    assert sanitize_input("<script>") == "&lt;script&gt;"

# The real question: does the endpoint reject or escape XSS?
```

**Remediation:** Test the source-of-truth boundary — the public API, the route handler, the middleware, the validation gateway — not the internal helper. If the helper is the boundary (standalone library function), test it there. Otherwise, test through the boundary.

```python
# Remediation: test through the boundary
def test_xss_prevention():
    response = client.post("/comment", data={"text": "<script>alert('xss')</script>"})
    assert response.status_code == 200
    assert "<script>" not in response.text
```

Remediation applies when:
- The test asserts behavior of an internal function that is called by a boundary function.
- The boundary function could change its implementation (e.g., use a different helper) and the test would still pass while the boundary behavior breaks.
- The failure mode is user-visible (crash, XSS, data loss) but the test only covers the internal helper.

Do not apply remediation when:
- The helper function is a public reusable library with its own contract independent of the boundary.
- The boundary is explicitly tested separately and the helper test catches additional cases the boundary test cannot reach (pure logic, combinatorial).

### **[STRINGLY-ERROR]** Remediation: String-Based Error Types

**Slop pattern:** Errors are represented as strings (string literals, error messages, or string enums) that force callers to match on exact text rather than structured error types. This makes error handling brittle, tests assert on message wording instead of error semantics, and catch-all handling becomes inevitable.

```python
# BAD: stringly error
def process_file(path):
    if not os.path.exists(path):
        return "file not found"  # string error
    # ... caller must compare strings

# BAD: exact string assertion in test
assert "file not found" in str(result)
```

**Remediation:** Define domain error types as explicit classes, enums, or exception types. Assert on error type/tag, not error message. Tests that need to verify error semantics should match on the error kind, not the rendered text.

```python
# Remediation: domain error type
class FileError(Exception):
    def __init__(self, kind: str, path: str):
        self.kind = kind  # "not_found", "permission_denied", etc.
        self.path = path

# Remediation: test asserts on error type, not message
with pytest.raises(FileError) as exc:
    process_file("/nonexistent")
assert exc.value.kind == "not_found"
```

Remediation applies when:
- Callers use string comparisons to distinguish error cases.
- Tests assert on error message text rather than error type.
- Error handling uses broad `except` because the error type is too vague.

Do not apply remediation when:
- The string is a user-facing message that is also the error identifier (and a structured alternative exists for programmatic handling).
- The error is from an external library where you cannot control the type.

### **[ADMIN-ARTIFACT]** Remediation: Non-Proof / Administrative Artifacts

**Slop pattern:** Test-shaped artifacts that prove nothing (smoke tests, coverage-only tests, import tests, constructor tests), quarantine labels that launder slop ("smoke", "non-proof", "diagnostic-only", "legacy"), and administrative records (issues, comments, docs) presented as completion of an implementation or proof obligation.

All three patterns share the same root: an artifact that looks like evidence but carries no proof weight, creating a surface future agents can cite as "already handled."

**Remediation:** For each artifact, determine whether it carries a real proof burden:
- Remove test-shaped artifacts that add no proof (they will be cited later as evidence of a real test suite).
- Move non-proof diagnostics to a non-QC diagnostic surface (separate tool, separate command, separate directory, not in the test suite).
- Require burden disposition for quarantine labels — either the artifact is real proof or it is removed.
- Administrative records (issues, comments, docs) document what remains to be done; they do not close the obligation.

Remediation applies when:
- The test file uses "smoke", "non-proof", "diagnostic-only", or similar disclaimers.
- The test asserts nothing about the source-of-truth boundary (imports, constructor, status labels).
- An issue, PR comment, or doc change is presented as completion of a code/proof task.

Do not apply remediation when:
- The diagnostic surface is explicitly maintained for debugging and never cited in QC or reviews.
- The administrative record genuinely closes the task (e.g., a research decision documented in an issue is the completion).

### **[QC-BYPASS]** Remediation: Local QC Bypass

**Slop pattern:** A project defines quality gates (test runner, type checker, linter) through local scripts or configs that bypass the global quality control system, giving agents a narrower set of checks to pass.

**Remediation:** Route all quality gates through the global QC system (`quality-control/justfile`). Local justfiles may compose global recipes but must not define independent checks that duplicate or override global gates. A local QC surface that passes when global QC fails is a bypass.

Remediation applies when:
- A project-local test/lint/type-check recipe exists that does not delegate to global QC.
- The local recipe uses different flags, coverage thresholds, or exclusion patterns than the global equivalent.

Do not apply remediation when:
- The local recipe ADDS checks beyond the global baseline (stricter, not looser).
- The global QC system does not cover the project's language or toolchain.

### **[VALIDATOR-BYPASS]** Remediation: Validator Bypass Markers

**Slop pattern:** A comment, annotation, or config suppresses a validator (linter, type checker, test requirement) without fixing the underlying issue, converting validator failure into silent acceptance.

```python
# BAD: bypass comment
# type: ignore  # no explanation of why
# pylint: disable=unused-argument  # used in template expansion but linter can't see it
```

**Remediation:** Either fix the code to satisfy the validator, or escalate the decision. If the validator is wrong (false positive), document the reason in a durable, specific comment and keep the suppression narrow. If the validator is right, fix the code. A bypass comment with no rationale is equivalent to silencing a diagnostic without addressing it.

Remediation applies when:
- The suppression covers more than one specific line (broad suppression that silences multiple diagnostics).
- The suppression has no comment explaining why the validator is wrong.
- The suppression is in project-owned code (not vendored or generated).

Do not apply remediation when:
- The suppression targets a known false positive with a documented upstream bug link.
- The suppression is temporary and tracked by an active issue.

### **[LEGACY-SHIM]** Remediation: Compatibility / Legacy Shims

**Slop pattern:** Wrappers, adapters, deprecated-function stubs, or feature flags that preserve a wrong earlier interface alongside the replacement — keeping dead code alive and multiplying the surface area that must be maintained and reviewed.

```python
# BAD: keeps old interface alive
def old_api(x, y):
    return new_api(x=x, y=y)
old_api.__doc__ = "Deprecated: use new_api instead"
```

**Remediation:** Replace the callers, then delete the old interface. In pre-launch code there are no legacy consumers — every shim is dead weight that doubles the review surface and preserves wrong patterns that future code will copy.

Remediation applies when:
- The shim exists "for compatibility" in pre-launch code with no known callers outside the repo.
- The old interface is worse (wrong names, wrong types, wrong defaults) and the replacement is complete.
- A deprecation warning or docstring is used instead of deleting the old code.

Do not apply remediation when:
- The old interface has external consumers outside the repo (published library, public API).
- Migration requires coordinated changes across multiple repos and the shim is temporary with an owner and deadline.

### **[UNOBSERVED-FAILURE]** Remediation: Unobserved-Failure Branches

**Slop pattern:** Code that handles a failure case, edge condition, or error path that has never been observed in practice — branching on an event the author hypothesizes might happen rather than one demonstrated by a real failure.

```python
# BAD: branch for a failure never observed
try:
    data = api.fetch()
except TimeoutError:
    data = None  # API calls have never timed out in this environment
```

**Remediation:** Do not add handling for failure modes that have not been observed. If the condition is logically impossible (invariant already guaranteed upstream), assert rather than branch. When a failure IS observed, add targeted handling for that specific case.

```python
# Remediation: assert the invariant
data = api.fetch()  # raises if network fails — correct behavior

# When the invariant is guaranteed by the caller:
assert data is not None, "upstream guarantees api.fetch returns data"
process(data)
```

Remediation applies when:
- The failure branch has no corresponding test that reproduces it.
- The handler produces a sentinel or silent continuation.
- The condition is logically impossible given upstream invariants.

Do not apply remediation when:
- The failure is well-known in the domain and occurs regularly (e.g., network timeout on HTTP calls to external services).
- The handling is required by the API contract (e.g., an interface method that must handle all enum variants).

### **[CODE-VERBOSITY]** Remediation: Code Verbosity and Complexity

**Slop pattern:** Code that is longer, noisier, or more abstract than it needs to be — filler documentation, verbose comments that restate the obvious, unnecessary intermediate variables, verbose variable names ("currentUserAuthenticationStatusBoolean"), "just in case" dead code, excessive defensive checks on already-validated data, boilerplate explosion (one trivial operation = one file/class), and over-abstraction (interface with one implementation, factory with one product, strategy pattern that never diverges).

**Remediation:** Delete the noise. Every line that carries no proof or instruction burden is a liability:
- Filler docstrings: delete; let the signature and body speak.
- Verbose comments restating the obvious: delete; restructure the code if it is not self-explanatory.
- Unnecessary intermediate variables: inline; keep only if the expression genuinely needs a name.
- Verbose names that obscure intent: replace with short type-signaling names.
- "Just in case" code: delete until a real call site demonstrates the need.
- Defensive checks on already-validated data: delete; validate at the boundary, assert inside.
- Boilerplate abstraction (one-class-per-trivial-operation): inline to a free function or expression.
- Over-abstraction (interface with one impl, factory with one product): delete the abstraction layer until a second caller or implementation exists.

Remediation applies when:
- The code carries more lines than the logic warrants.
- A reader must scan past filler to find the actual behavior.
- The abstraction exists for hypothetical future variation.

Do not apply remediation when:
- The verbosity is required by the project's public API contract (e.g., comprehensive docstrings for a published library).
- The defensive check protects against an observed (not hypothetical) upstream invariant violation.

### **[CODE-WITHIN-CODE]** Remediation: Code Within Code / Embedded Cross-Language Programs

**Slop pattern:** A program in language A assembles and executes language B as a string — Python calling `subprocess.run("bash -c '...'")`, shell scripts inlining Perl/Python with `$(python -c '...')`, or any template-like generation where one language builds another inline. The embedded language is invisible to syntax checking, linting, static analysis, and independent debugging.

```python
# BAD: Python embedding bash as a string
subprocess.run(
    f"ffmpeg -i {input_file} -vf 'scale={width}:{height}' {output_file}",
    shell=True, check=True
)
# The bash is a string — no syntax check, no shellcheck, no debugger
```

**Remediation (narrative reconstruction):** This pattern signals a missing abstraction layer. Trace through three approximations to find the correct boundary:

**1st approximation — externalize the embedded language into its own file:** Extract the bash into a standalone script. Python calls the script, not a constructed string. The script is now syntax-checkable, lintable, and reviewable independently.

```bash
# scripts/transcode.sh — reviewed, shellcheck-passing artifact
#!/usr/bin/env bash
set -euo pipefail
ffmpeg -i "$1" -vf "scale=$2:$3" "$4"
```

```python
# Python calls the script — no string construction
subprocess.run(["scripts/transcode.sh", input_file, str(width), str(height), output_file], check=True)
```

**2nd approximation — lift to ambient workflow:** The Python and bash run sequentially in the same automation context (CI pipeline, Makefile, just recipe). Call them as separate steps rather than nesting one inside the other.

```yaml
# CI workflow — steps are peers, not nested
steps:
  - name: Prepare metadata
    run: python prepare.py
  - name: Transcode video
    run: bash scripts/transcode.sh
  - name: Upload result
    run: python upload.py
```

**3rd approximation — eliminate the embedded language entirely:** The bash was never needed. The CI workflow orchestration (or justfile/ Makefile) is the correct abstraction for running sequenced commands. The Python step does Python work; the shell step does shell work; neither embeds the other. Each tool operates at its native level, and the workflow definition provides the sequencing.

```yaml
# CI workflow — correct solution: each tool at its own level
steps:
  - run: python process_metadata.py
  - run: ffmpeg ...  # no wrapping script needed either
  - run: python upload_results.py
```

Remediation applies when:
- Language A constructs language B as a string and executes it (subprocess with shell=True, eval, inline script).
- The embedded code could be its own file with syntax checking and linting.
- The embedding destroys debugging, stack traces, or error reporting for the inner language.

Do not apply remediation when:
- The inner language is a genuine data query (SQL, XPath, JMESPath) where the query string is data, not control flow.
- The embedding uses a safe, non-executing template engine (Jinja2, Mustache) that produces static output files, not executed code.

---

### **[EXISTENCE-AS-PROOF]** Remediation: Existence / Truthy / Shape as Proof

**Slop pattern:** A test asserts only that a value exists, is truthy, non-empty, or has the right type/shape, without checking its semantic content. Examples: `assert result is not None`, `assert items`, `assert len(output) > 0`, `assert isinstance(result, dict)`, `assert hasattr(payload, "items")`, `expect(result).toBeDefined()`.

```python
# BAD: asserts existence, not semantics
def test_result_exists():
    result = run_owned_operation(input_payload)
    assert result is not None

def test_items_returned():
    items = collect_domain_items(source_path)
    assert items  # truthy — empty list would also fail but for wrong reason

def test_file_created(tmp_path):
    output_path = produce_artifact(tmp_path)
    assert output_path.exists()  # empty file passes
```

These assertions pass even on broken output: `None` proves nothing; an empty file exists; a junk dict `{"x": 1}` is truthy.

**Remediation:** Assert on exact expected values against real fixtures. The assertion should prove the output is correct, not just that it exists. Every existence assertion should be replaceable with a concrete value assertion against known test fixtures.

```python
# Remediation: assert exact semantics against fixtures
def test_artifact_contains_expected_semantics(tmp_path):
    output_path = produce_artifact(tmp_path, source=fixture_path("valid_input.md"))
    assert output_path.read_text() == expected_text("valid_output.html")

def test_collects_expected_ordered_items():
    items = collect_domain_items(fixture_path("source_with_two_items.md"))
    assert items == [
        DomainItem(key="alpha", title="First"),
        DomainItem(key="beta", title="Second"),
    ]

def test_loads_correct_payload():
    payload = load_payload(fixture_path("config.toml"))
    assert payload == {"host": "localhost", "port": 8080}
```

Remediation applies when:
- The assertion proves only that a value exists (is not None, is truthy, is non-empty, has a field) but not that the value is correct.
- A broken implementation could return a plausible-looking but wrong value and the test would still pass.

Do not apply remediation when:
- The existence check is one assertion among many in a test that also verifies semantic content (e.g., a precondition guard before the real assertion).
- The test is explicitly a liveness/health check that only needs to prove the endpoint responds.

### **[NO-CRASH-PROOF]** Remediation: No-Throw / No-Crash as Proof

**Slop pattern:** A test calls a function and asserts nothing about the result — it only proves the function did not crash. Examples: calling `run_operation()` without asserting on the output, asserting that `run()` returns without error but ignoring what it returns.

```python
# BAD: no-crash is not proof of correctness
def test_operation_does_not_crash():
    run_operation(input_data)  # no assertion — any output passes

def test_parse_does_not_raise():
    result = parse_document(text)  # result is never inspected
```

**Remediation:** Assert exact output values or side effects. A test that proves nothing about correctness is noise. If the function returns a value, assert on it. If the function produces a side effect (file write, database insert, API call), assert on the side effect's result.

```python
# Remediation: assert on the output
def test_operation_produces_correct_result():
    result = run_operation(input_data)
    assert result == ExpectedOutput(...)

# Remediation: assert on the side effect
def test_operation_writes_correct_file(tmp_path):
    output_path = run_operation(input_data, output_dir=tmp_path)
    assert output_path.read_text() == expected_content
```

Remediation applies when:
- The test has no assertion on the function's output or side effects.
- The test would pass if the function returned `None` or produced no side effects.
- The only thing the test proves is that the code path was reachable.

Do not apply remediation when:
- The function is a void-returning command whose correctness is verified by a separate integration test that asserts on the system state.
- The function genuinely has no observable output and is tested through its caller's boundary.

### **[MOCK-AS-PROOF]** Remediation: Mock/Spy/Call-Count as Proof

**Slop pattern:** A test asserts that a mock was called, or called N times, with certain arguments, without asserting on the real effect at the boundary. The mock assertion proves the internal wiring is connected but not that the system produces correct output.

```python
# BAD: asserts mock was called, not that output is correct
def test_sends_notification():
    mock_send = Mock()
    notifier = Notifier(mock_send)
    notifier.notify(user_email)
    assert mock_send.called
    mock_send.assert_called_once_with(to=user_email, body="...")
```

**Remediation:** Assert on the real boundary effect — the file that was written, the database row that was inserted, the API response that was returned. If the code path is simple enough that a mock assertion is the only way to verify it, consider whether the test adds value at all (the path is trivially correct by inspection) or whether an integration test would cover it.

```python
# Remediation: assert on the real effect
def test_notification_logged_in_database():
    service.notify(user_email)
    log_entry = Log.query.filter_by(email=user_email).first()
    assert log_entry is not None
    assert log_entry.body contains expected_body
```

Remediation applies when:
- The primary assertion is on mock call count or call arguments.
- No real boundary effect is verified (no database, no file, no API response).
- The mock is standing in for a side effect that is observable in the test environment.

Do not apply remediation when:
- The boundary is an external API that cannot be called in tests (third-party service, hardware) AND the mock is paired with a separate integration test that verifies the real interaction.
- The mock assertion is supplementary to a real boundary assertion.

### **[SOURCE-POLICING]** Remediation: Source Policing in Tests

**Slop pattern:** A test reads the source code of the application and asserts that certain strings, patterns, or symbols do or do not appear in the text. Examples: asserting `"fallback" not in source` to verify there are no fallback branches, scanning files for deprecated function names, asserting on line counts.

```python
# BAD: test asserts on source code text
def test_no_fallback():
    source = Path("src/module.py").read_text()
    assert "fallback" not in source  # source policing instead of behavior testing
```

**Remediation:** Move source-text assertions to global QC (lint rules, AST checks, dedicated static analysis). Tests assert on runtime behavior, not on source text. The runtime behavior — whether a fallback is actually reachable — is what matters; source text is an unreliable proxy.

```python
# Remediation: test the runtime behavior
def test_no_fallback_used():
    result = process_with_valid_input()
    assert result == expected_output  # tests behavior, not source text
    # Fallback reachability is a static analysis concern, not a test concern.

# If static enforcement is needed:
# .semgrep/ or .pre-commit-config.yaml — not in a test file
```

Remediation applies when:
- The test reads `.py`, `.ts`, `.rs`, or other source files as strings and asserts on their text content.
- The assertion is about code structure rather than runtime behavior.
- A lint rule or AST check exists that could enforce the same constraint.

Do not apply remediation when:
- The test operates on generated/compiled code (not hand-written source) and verifies code generation output.
- The test is explicitly a meta-test that validates codegen templates produce expected output.

### **[DELETION-LAUNDERING]** Remediation: Deletion Laundering / Proof-Burden Erasure

**Slop pattern:** A criticized slop artifact is deleted without solving or recording the original problem it attempted to address. The codebase looks cleaner, but the proof burden is now hidden. The next agent is likely to recreate the same fake proof, fallback, wrapper, or harness because the original requirement is absent from the new PR narrative.

Detection:
- deletion follows review or user criticism;
- commit message emphasizes cleanup, removal, or simplification;
- no replacement proof or capability exists;
- no issue, contract, or blocker records the original problem;
- final report says the review item is resolved because the artifact is gone;
- the original requirement is absent from the new PR narrative.

**Remediation:** Require a burden disposition: the original problem must be either solved, invalidated, transferred to real proof, or explicitly recorded as unresolved. Deletion is not a disposition — it is the removal of an artifact. The record of what was wrong and why must survive the deletion.

```python
# BAD: commit message says "removed dead code" — the original problem is gone
# BAD: PR says "addressed review feedback by deleting the test" — no replacement

# CORRECT dispositions:
# - Solved: the problem was real and the replacement proof covers it
# - Invalidated: the problem was spurious and has been demonstrated irrelevant
# - Transferred: the proof burden moved to a different artifact (integration test, QC check)
# - Recorded unresolved: the problem is real but deferred, with a visible issue or blocker
```

Remediation applies when:
- A deletion follows criticism and the commit message frames it as cleanup.
- The deleted artifact was the only coverage for a requirement, edge case, or failure mode.
- The review finding was about existence of a proof, not about the artifact's labeling.

Do not apply remediation when:
- The artifact was genuinely dead code with no corresponding requirement (no one asked for it, no test covered it, no spec mentioned it).
- The deletion is part of a larger replacement that demonstrably covers the original requirement.

### **[BESPOKE-DEP]** Remediation: Bespoke Dependency Reinvention

**Slop pattern:** Application code reimplements what an existing, installed dependency already provides — custom React components when a UI library has them, hand-rolled YAML generation when a YAML library is installed, bespoke string parsing when a parser exists, custom pagination when a framework provides it. The model perceives the generic, tested solution as "abstraction layer bloat" and the bespoke reinvention as "clean, minimal code."

Examples:
- Custom `AcademicCard.tsx` (~60 LOC) when `card.tsx` exists in the UI inventory.
- Custom `FilterControls.tsx` with hand-rolled popover logic when `select.tsx`, `dropdown-menu.tsx`, and `scroll-area.tsx` already exist.
- Custom `PaginatedScroller.tsx` with bespoke scroll logic when `scroll-area.tsx` + `pagination.tsx` already exist.
- Custom string-concatenated YAML generation when a YAML library is installed.
- Custom hand-rolled AST stringifier when the parser library already provides stringification.

**Remediation:** REFINE, REPLACE, REFACTOR — migrate the bespoke implementation to use the dependency. For every custom function or component, ask: "Is there a standard library or installed dependency that already solves this?" If yes, the custom code is technical debt. Do not delete the dependency because it is "unused" — it was unused because the bespoke code was written instead of using it.

Remediation applies when:
- A dependency provides exactly the functionality reimplemented in custom code.
- The custom code is larger, less tested, or less maintainable than the library alternative.
- The library is already installed (the import is missing, not the package).

Do not apply remediation when:
- The dependency does not exist in the project and adding it would be disproportionate for the use case.
- The custom code has genuinely different requirements that the library does not support.
- The library is deprecated, unmaintained, or has known security issues.

---

> **Agent-resistant codebases should be designed so that the easiest code to write is also the hardest code to fake.**

Defaults, fallbacks, mocks, skips, helper proofs, string errors, and local QC gates all make faking easier. The bridge-burning policies remove those moves from the game.

