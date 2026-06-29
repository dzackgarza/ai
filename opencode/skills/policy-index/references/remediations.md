# Policy Remediations

Load this file only when acting as the remediation/fixer agent after triage provides a
`POLICY.*` code.

Do not load this file while acting as the issue-seeing reviewer, detector author, or QC
triage classifier. The reviewer classifies the weakened obligation; the fixer reads the
remediation map.

## Remediation Registry

| Code | Applies to | Required remediation |
| --- | --- | --- |
| `REMEDIATE.TOTAL_CONFIG_MODEL` | `POLICY.RUNTIME_DEFAULT`, `POLICY.NO_HIDDEN_CONFIG`, `POLICY.TOTAL_CORE_STATE` | Put required configuration in the declared config surface. Validate once at startup into a total model. Missing, malformed, partial, or unknown config fails loudly. |
| `REMEDIATE.FAIL_LOUD_BOUNDARY` | `POLICY.FAIL_OPEN`, `POLICY.CRITICAL_DEPENDENCY`, `POLICY.NO_PARTIAL_SUCCESS`, `POLICY.NO_ERROR_DISCARD`, `POLICY.NO_AMBIENT_DISCOVERY`, `POLICY.NO_DEFENSIVE_HOTPATH` | Assert or check required resources at the owned boundary, then execute without fallback. Let unexpected errors propagate. Catch only observed, specific, recoverable domain errors and handle them in the same scope. |
| `REMEDIATE.REAL_PROOF_LOOP` | `POLICY.NO_SMOKE_PROOF`, `POLICY.NO_MOCK_PROOF`, `POLICY.NO_SKIP_MASK`, `POLICY.NO_HELPER_PROOF`, `POLICY.NO_EXACT_STRING_PROOF` | Replace fake or masked proof with tests that cross the real boundary, use real fixtures/data/services available to the project, and assert semantic output or side effects. Commit red proof before green fixes for reported bugs. |
| `REMEDIATE.API_SPLIT_OR_VARIANT` | `POLICY.NO_BOOLEAN_MODE` | Split behavior into named functions when the modes are separate operations. Use an explicit enum/tagged variant only when the mode is domain data, and dispatch exhaustively. |
| `REMEDIATE.STRUCTURED_TYPES` | `POLICY.NO_TYPE_ESCAPE` | Replace casts, `Any`, broad `Partial`, string errors, and dict-shaped owned data with explicit domain types, schemas, enums, and structured errors. Tests assert semantic variants, not string rendering or shape. |
| `REMEDIATE.TYPED_DEPENDENCY_BOUNDARY` | `POLICY.NO_UNTYPED_IMPORT_LEAK` | Preserve the correct library. Restore type information with stubs when practical; otherwise isolate the untyped import in one typed firewall module that returns project-owned typed values. |
| `REMEDIATE.REMOVE_SUPPRESSION_WITH_EXCEPTION_PROTOCOL` | `POLICY.NO_QC_SILENCING` | Remove the suppression and fix the underlying invariant. If a validator is wrong, stop for explicit policy exception approval with policy code, justification, replacement invariant, boundary proof, and audit trail. |
| `REMEDIATE.DELEGATE_GLOBAL_QC` | `POLICY.GLOBAL_QC_AUTHORITY` | Route public `test` and `test-ci` through `~/ai-review-ci/justfiles/<language>.just`. Keep project-specific semantic checks private and composed after the global gate. |
| `REMEDIATE.TRACK_STATIC_ARTIFACT` | `POLICY.NO_DYNAMIC_ARTIFACTS` | Move owned prompts, scripts, configs, templates, and static data into tracked files. Runtime code loads the reviewed artifact rather than constructing it from inline strings. |
| `REMEDIATE.REPLACE_LEGACY_PATH` | `POLICY.NO_LEGACY_SHIM` | Migrate all callers to the new path, prove the migrated behavior, then remove the obsolete interface with burden disposition. |
| `REMEDIATE.OBSERVE_BEFORE_BRANCHING` | `POLICY.NO_HYPOTHETICAL_PATH` | Do not add code. Preserve the invariant as an assertion or fail-loud boundary. Add a branch only after a real observed incident establishes the domain case. |
| `REMEDIATE.PREFER_ASSERTION` | `POLICY.PREFER_ASSERTION`, `POLICY.NO_HYPOTHETICAL_PATH` | Reject suggestions to replace `assert` with `if/raise` (especially the `python -O` argument). Keep the assertion, make it ADDD-shaped, delete any `AssertionError` catch path, and strengthen it to the strongest provably-true invariant. See `[ASSERT-OVER-RAISE]`. |
| `REMEDIATE.BURDEN_DISPOSITION` | `POLICY.NO_QUARANTINE_REMEDIATION`, `POLICY.NO_ADMIN_COMPLETION`, `POLICY.NO_DELETION_LAUNDERING` | Reconstruct the original obligation, then mark it solved, invalidated, transferred to a real proof surface, or recorded unresolved. Do not treat labels, docs, deletion, or comments as resolution. |
| `REMEDIATE.BLAST_RADIUS_REPAIR` | Any slop finding | Inspect the owning boundary, adjacent call sites, tests, config surface, and history for the same failure process. Fix the full damaged obligation, not only the matched token. |

## Assignment Rule

The fixer receives the policy code from triage and chooses the remediation code in this
file. The detector and issue-seeing reviewer must not prescribe the remediation code.

If more than one remediation applies, choose the one that restores the original
obligation at the widest real boundary. Do not pick the smallest local edit.

---

## [REMEDIATION-POLICIES] Detailed Remediation Policies

A red flag says "this is suspicious." A remediation policy says "replace it with this exact shape." Every remediation converts a slop-enabling pattern into a fail-loud, minimal-cruft equivalent.

All remediation code follows [ADDD: Assert, Dump Data, Direct](runtime-control-flow.md#addd-assert-dump-data-direct). Assert the invariant at the earliest owned boundary, include the related observed data in the failure payload, then direct the reader to the file, config, command, usage, or owned tool repo that fixes the cause. After the assertion, simplify the remaining code as if the invariant holds.

### [FALLBACK-HEDGE] Remediation: Fallback / Optional-Dependency / File-Availability Hedge

Slop pattern: A guard checks whether a dependency, file, binary, or resource exists before using it, with a silent fallback when absent.

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

Remediation: Assert availability at the program boundary. If the resource is required, failure to find it is a hard error. Do not provide a silent branch.

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

### [SWALLOW-CATCH] Remediation: try/catch That Swallows or Hedges

Slop pattern: A try/catch around an operation that is expected to succeed, converting a useful diagnostic into a silent continuation or a weak log line.

Catching `AssertionError` is worse than ordinary swallowing: an assertion is a proof claim about code state, not a runtime error. Do not recover from it, translate it, or test it as product behavior.

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

Remediation: Let the error propagate. If the caller cannot handle the error, it should not catch it. If a specific error type is expected and recoverable, catch only that type and handle it in the same scope.

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

### [DATA-PEEK] Remediation: Data-Peeking Inside Loops

Slop pattern: A loop that checks a condition on each element and routes logic inside the loop body, mixing filtering with processing and making the control flow harder to read.

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

Remediation: Filter and assert invariants before the loop. The loop body should only contain the processing logic, with preconditions already satisfied.

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

### [NESTED-CONDITIONAL] Remediation: Nested / Stacked Conditional Chains

Slop pattern: A cascade of `if`/`elif`/`else` that branches on a single discriminant (type, enum, status, state) with implicit fall-through for unhandled cases.

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

Remediation: Use a match/case (Python 3.10+, TypeScript, Rust, etc.) or an explicit dispatch table that enumerates all expected cases and fails hard on unexpected input.

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

### [DYNAMIC-FILE-CREATION] Remediation: Dynamic File / Config Creation from Code

Slop pattern: Code that writes a file (config, script, data file) by assembling content from raw strings, shell heredocs, or inline byte buffers — making the content invisible to review, diff, and static analysis.

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

Remediation: Commit a static version of the file as a tracked artifact. Read or copy it at runtime. If dynamic content is genuinely required (not for config — for user data), use a real templating engine (Jinja2, Mustache, etc.) with a template file that IS the reviewed artifact.

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

### [INLINE-STRINGS] Remediation: Inline Large Strings / Prompts Embedded as Code

Slop pattern: Embedding agent prompts, user-facing messages, instruction blocks, or any text longer than ~5 lines directly in source files as string literals. This treats data (strings) as code, making the text invisible to separate review, unversioned independently, and vulnerable to ad-hoc inline edits that bypass normal review.

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

Remediation: Extract all non-code strings to a standard data file (TOML, YAML, JSON) keyed by label. Load them at runtime via a library. The data file is the reviewed, diffable artifact; the code is a thin accessor.

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

### [IMPLICIT-STATE] Remediation: Implicit / Defaulted / Discovered State

Slop pattern: The app relies on runtime defaults, ambient discovery (inferring config from machine state), hidden global state (shell/env/cache), or optional core state with "maybe initialized" logic — all of which bury configuration in unreviewable surfaces and make behavior depend on ephemeral external conditions.

These are distinct variants of the same failure: state that should be explicit is implicit, discoverable only by reading non-code surfaces.

Remediation: Declare all configuration explicitly in a committed project config file. Validate the config at startup; fail hard if values are missing or invalid. Core state is total — normalized once at initialization, never optional.

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

### [PARTIAL-RESULT] Remediation: Partial / Sentinel Results

Slop pattern: An operation that can partially succeed produces a result object with some fields populated and others sentinel (None, empty, -1) — forcing every caller to check which parts are valid.

```python
# BAD: partial success object
result = fetch_data(url)
if result.status == "ok":
    process(result.data)
# else: caller must check every access
```

Remediation: An operation either succeeds completely or fails with a clear error. Do not return objects that are "mostly OK" with missing parts. If the operation genuinely has partial results, represent them as explicit alternatives (union type, enum variant, tagged sum).

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

### [BOOLEAN-MODE] Remediation: Boolean Mode Parameters

Slop pattern: A function takes a boolean parameter that changes its behavior between two modes, forcing callers to read the function body to understand what each value means.

```python
# BAD: boolean mode flag
process_data(data, validate=True)   # what does False mean?
send_notification(user, urgent=False)  # which behavior is default?
```

Remediation: Split into separate functions with descriptive names, or use an explicit enum where each variant name describes the mode.

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

### [UNTYPED-IMPORT-BOUNDARY] Remediation: Untyped Third-Party Imports

Slop pattern: A mypy `import-untyped` diagnostic appears because a dependency lacks stubs or a `py.typed` marker. The agent treats the diagnostic as a reason to change the dependency, hand-roll the feature, suppress mypy, or scatter casts.

```python
# BAD: direct untyped import in product code
from untyped_yaml import load

payload = load(text)
```

```toml
# BAD: local validator silence
[[tool.mypy.overrides]]
module = ["untyped_yaml.*"]
ignore_missing_imports = true
```

Remediation order:

- Preserve the correct library unless product requirements independently reject it. Do not replace a library solely because it is untyped.
- If maintained stubs exist, add the stub package through the approved dependency path. Generic reusable stubs belong in global QC/tooling; repo-specific runtime or test stubs belong in the repo only when they are part of the project’s declared dependency surface.
- If no maintained stubs exist and the needed API is small, add minimal `.pyi` stubs for the exact imported module and symbols. Stub only the surface the project uses.
- If stubbing would be large or brittle, isolate the untyped import in one typed firewall module. The firewall imports the untyped library, validates or converts its outputs, and returns project-owned named types. Owned code imports the firewall, not the untyped library.
- Global QC should provide the only allowed `import-untyped` carve-out: firewall modules may be exempt from that specific diagnostic, while direct imports elsewhere remain blockers.

Firewall shape:

```python
# src/project/_type_firewalls/untyped_yaml.py
from dataclasses import dataclass

from untyped_yaml import load


@dataclass(frozen=True)
class ParsedConfig:
    command: str
    timeout_ms: int


def parse_config(text: str) -> ParsedConfig:
    raw = load(text)
    assert isinstance(raw, dict), "config must parse to a mapping"
    command = raw["command"]
    timeout_ms = raw["timeout_ms"]
    assert isinstance(command, str), "command must be a string"
    assert isinstance(timeout_ms, int), "timeout_ms must be an integer"
    return ParsedConfig(command=command, timeout_ms=timeout_ms)
```

Firewall constraints:
- exactly one module imports the untyped dependency;
- no untyped dependency objects cross the firewall boundary;
- the firewall returns named project-owned types, not `dict[str, object]`, `Any`, or library-native objects;
- downstream code has no `Any`, casts, or mypy ignores for the dependency;
- semantic tests exercise the project boundary that consumes the typed result.

Canonical exclusion rule: global QC may ignore `import-untyped` only for modules under the project’s type-firewall convention, such as `src/<package>/_type_firewalls/<dependency>.py`. The same gate must still reject the untyped import outside that convention. Repo-local mypy config, file-level ignore comments, and blanket `ignore_missing_imports` remain validator bypasses.

Remediation applies when:
- mypy reports `import-untyped`, `missing library stubs`, or missing `py.typed`;
- the dependency is otherwise the correct library for the job;
- owned code would receive `Any` from that import.

Do not apply remediation when:
- the library is wrong for product reasons unrelated to type checking;
- a typed first-party API or official replacement is already the documented successor;
- the import is unused and can be deleted without changing the intended capability.

<a id="remediation-boundary-test-bypass"></a>

### [BOUNDARY-BYPASS] Remediation: Boundary Test Bypass

Slop pattern: A test for a boundary condition (e.g., a null input, an edge case, a security check) tests the helper function that performs the check rather than the boundary where the check is enforced.

```python
# BAD: tests the helper, not the boundary
def test_sanitize_input():
    assert sanitize_input("<script>") == "&lt;script&gt;"

# The real question: does the endpoint reject or escape XSS?
```

Remediation: Test the source-of-truth boundary — the public API, the route handler, the middleware, the validation gateway — not the internal helper. If the helper is the boundary (standalone library function), test it there. Otherwise, test through the boundary.

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

<a id="remediation-string-based-error-types"></a>

### [STRINGLY-ERROR] Remediation: String-Based Error Types

Slop pattern: Errors are represented as strings (string literals, error messages, or string enums) that force callers to match on exact text rather than structured error types. This makes error handling brittle, tests assert on message wording instead of error semantics, and catch-all handling becomes inevitable.

```python
# BAD: stringly error
def process_file(path):
    if not os.path.exists(path):
        return "file not found"  # string error
    # ... caller must compare strings

# BAD: exact string assertion in test
assert "file not found" in str(result)
```

Remediation: Define domain error types as explicit classes, enums, or exception types. Assert on error type/tag, not error message. Tests that need to verify error semantics should match on the error kind, not the rendered text.

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

### [ADMIN-ARTIFACT] Remediation: Non-Proof / Administrative Artifacts

Slop pattern: Test-shaped artifacts that prove nothing (smoke tests, coverage-only tests, import tests, constructor tests), quarantine labels that launder slop ("smoke", "non-proof", "diagnostic-only", "legacy"), and administrative records (issues, comments, docs) presented as completion of an implementation or proof obligation.

All three patterns share the same root: an artifact that looks like evidence but carries no proof weight, creating a surface future agents can cite as "already handled."

Remediation: For each artifact, determine whether it carries a real proof burden:
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

### [QC-BYPASS] Remediation: Local QC Bypass

Slop pattern: A project defines quality gates (test runner, type checker, linter) through local scripts or configs that bypass the global quality control system, giving agents a narrower set of checks to pass.

Remediation: Route all quality gates through the global QC system (`~/ai-review-ci/justfiles/<language>.just`). Local justfiles may compose global recipes but must not define independent checks that duplicate or override global gates. A local QC surface that passes when global QC fails is a bypass.

Remediation applies when:
- A project-local test/lint/type-check recipe exists that does not delegate to global QC.
- The local recipe uses different flags, coverage thresholds, or exclusion patterns than the global equivalent.

Do not apply remediation when:
- The local recipe ADDS checks beyond the global baseline (stricter, not looser).
- The global QC system does not cover the project's language or toolchain.

### [VALIDATOR-BYPASS] Remediation: Validator Bypass Markers

Slop pattern: A comment, annotation, or config suppresses a validator (linter, type checker, test requirement) without fixing the underlying issue, converting validator failure into silent acceptance.

```python
# BAD: bypass comment
# type: ignore  # no explanation of why
# pylint: disable=unused-argument  # used in template expansion but linter can't see it
```

Remediation: Either fix the code to satisfy the validator, or escalate the decision. If the validator is wrong (false positive), document the reason in a durable, specific comment and keep the suppression narrow. If the validator is right, fix the code. A bypass comment with no rationale is equivalent to silencing a diagnostic without addressing it.

Remediation applies when:
- The suppression covers more than one specific line (broad suppression that silences multiple diagnostics).
- The suppression has no comment explaining why the validator is wrong.
- The suppression is in project-owned code (not vendored or generated).

Do not apply remediation when:
- The suppression targets a known false positive with a documented upstream bug link.
- The suppression is temporary and tracked by an active issue.

### [LEGACY-SHIM] Remediation: Compatibility / Legacy Shims

Slop pattern: Wrappers, adapters, deprecated-function stubs, or feature flags that preserve a wrong earlier interface alongside the replacement — keeping dead code alive and multiplying the surface area that must be maintained and reviewed.

```python
# BAD: keeps old interface alive
def old_api(x, y):
    return new_api(x=x, y=y)
old_api.__doc__ = "Deprecated: use new_api instead"
```

Remediation: Replace the callers, then delete the old interface. In pre-launch code there are no legacy consumers — every shim is dead weight that doubles the review surface and preserves wrong patterns that future code will copy.

Remediation applies when:
- The shim exists "for compatibility" in pre-launch code with no known callers outside the repo.
- The old interface is worse (wrong names, wrong types, wrong defaults) and the replacement is complete.
- A deprecation warning or docstring is used instead of deleting the old code.

Do not apply remediation when:
- The old interface has external consumers outside the repo (published library, public API).
- Migration requires coordinated changes across multiple repos and the shim is temporary with an owner and deadline.

### [UNOBSERVED-FAILURE] Remediation: Unobserved-Failure Branches

Slop pattern: Code that handles a failure case, edge condition, or error path that has never been observed in practice — branching on an event the author hypothesizes might happen rather than one demonstrated by a real failure.

```python
# BAD: branch for a failure never observed
try:
    data = api.fetch()
except TimeoutError:
    data = None  # API calls have never timed out in this environment
```

Remediation: Do not add handling for failure modes that have not been observed. If the condition is logically impossible (invariant already guaranteed upstream), assert rather than branch. When a failure IS observed, add targeted handling for that specific case.

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

### [ASSERT-OVER-RAISE] Remediation: `if/raise` Where an Assertion Belongs

Policy: `POLICY.PREFER_ASSERTION`, `POLICY.NO_HYPOTHETICAL_PATH`

Slop pattern: An invariant or precondition is enforced with `if not cond: raise ValueError(...)`/`RuntimeError(...)` instead of `assert cond, "..."`, or an existing assertion is wrapped in `try/except AssertionError`. The most common trigger is a reviewer (often an automated one) recommending "replace `assert` with `if/raise` because assertions are stripped under `python -O`." Accepting that recommendation is the slop. Catching assertion failure is the same slop in catch-form: it turns a provable claim about state into runtime logic.

```python
# BAD: if/raise on what is an invariant, "to survive python -O"
def global_vault_path() -> Path:
    override = os.environ.get("AGENT_MEMORY_VAULT")
    if override is not None:
        if not override.strip():
            raise ValueError("AGENT_MEMORY_VAULT must not be empty when set")
        return Path(override).expanduser()
    ...

# BAD: catching an assertion turns proof into runtime behavior
def run_with_config(config: RuntimeConfig) -> None:
    try:
        assert config.command, "runtime command is required"
    except AssertionError:
        repair_or_continue()
    run(config.command)
```

Why this is wrong here: Assertions are the strongly-preferred idiom. An `assert` is an auditable proof of what the author believes must be true at that point; it forces the writer to engage with the data, name real failure modes, and narrow types so the checker can validate the branch. `if/raise` on an invariant is adjacent to timid, fail-open, splat-guessing slop and removes that proof. The `python -O` argument is hypothetical fiction (`POLICY.NO_HYPOTHETICAL_PATH`): these are bespoke tools that are never run with `-O`, the assertion-stripping failure has never been observed, and protecting downstream users who pass optimization flags is not an owned obligation.

```python
# Remediation: keep the assertion; if anything, make it stronger
def global_vault_path() -> Path:
    override = os.environ.get("AGENT_MEMORY_VAULT")
    if override is not None:
        assert override.strip(), (
            "AGENT_MEMORY_VAULT must name a path when set; "
            "config source=environment; "
            "fix ~/.envrc or unset the variable before running agent-memory"
        )
        return Path(override).expanduser()
    ...
```

Remediation: Reject the suggestion. Restore (or keep) the `assert`. Then audit the assertion itself: is it the strongest provably-true statement available at that point, does it dump the related data needed to repair the failure, and does it direct the maintainer to the owning config, data file, command, usage surface, or owned tool repository? Strengthen it if a more precise invariant or more useful ADDD payload holds. Do not add a raise-based escape hatch or a catch-based recovery path.

Do not apply remediation when:
- The raise is a genuine domain error on observed external input the app contractually owns (see `[STRINGLY-ERROR]` for using structured error types there) — not an internal invariant.
- The boundary is an approved error-translation renderer turning a structured internal error into a user-facing protocol (see `test-guidelines` Try/Catch Ban exception).

### [CODE-VERBOSITY] Remediation: Code Verbosity and Complexity

Slop pattern: Code that is longer, noisier, or more abstract than it needs to be — filler documentation, verbose comments that restate the obvious, unnecessary intermediate variables, verbose variable names ("currentUserAuthenticationStatusBoolean"), "just in case" dead code, excessive defensive checks on already-validated data, boilerplate explosion (one trivial operation = one file/class), and over-abstraction (interface with one implementation, factory with one product, strategy pattern that never diverges).

Remediation: Delete the noise. Every line that carries no proof or instruction burden is a liability:
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

### [CODE-WITHIN-CODE] Remediation: Code Within Code / Embedded Cross-Language Programs

Slop pattern: A program in language A assembles and executes language B as a string — Python calling `subprocess.run("bash -c '...'")`, shell scripts inlining Perl/Python with `$(python -c '...')`, or any template-like generation where one language builds another inline. The embedded language is invisible to syntax checking, linting, static analysis, and independent debugging.

```python
# BAD: Python embedding bash as a string
subprocess.run(
    f"ffmpeg -i {input_file} -vf 'scale={width}:{height}' {output_file}",
    shell=True, check=True
)
# The bash is a string — no syntax check, no shellcheck, no debugger
```

Remediation narrative reconstruction: This pattern signals a missing abstraction layer. Trace through three approximations to find the correct boundary:

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

<a id="remediation-existence--truthy--shape-as-proof"></a>

### [EXISTENCE-AS-PROOF] Remediation: Existence / Truthy / Shape as Proof

Slop pattern: A test asserts only that a value exists, is truthy, non-empty, or has the right type/shape, without checking its semantic content. Examples: `assert result is not None`, `assert items`, `assert len(output) > 0`, `assert isinstance(result, dict)`, `assert hasattr(payload, "items")`, `expect(result).toBeDefined()`.

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

Remediation: Assert on exact expected values against real fixtures. The assertion should prove the output is correct, not just that it exists. Every existence assertion should be replaceable with a concrete value assertion against known test fixtures.

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

<a id="remediation-no-throw--no-crash-as-proof"></a>

### [NO-CRASH-PROOF] Remediation: No-Throw / No-Crash as Proof

Slop pattern: A test calls a function and asserts nothing about the result — it only proves the function did not crash. Examples: calling `run_operation()` without asserting on the output, asserting that `run()` returns without error but ignoring what it returns.

```python
# BAD: no-crash is not proof of correctness
def test_operation_does_not_crash():
    run_operation(input_data)  # no assertion — any output passes

def test_parse_does_not_raise():
    result = parse_document(text)  # result is never inspected
```

Remediation: Assert exact output values or side effects. A test that proves nothing about correctness is noise. If the function returns a value, assert on it. If the function produces a side effect (file write, database insert, API call), assert on the side effect's result.

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

<a id="remediation-mockspycall-count-as-proof"></a>

### [MOCK-AS-PROOF] Remediation: Mock/Spy/Call-Count as Proof

Slop pattern: A test asserts that a mock was called, or called N times, with certain arguments, without asserting on the real effect at the boundary. The mock assertion proves the internal wiring is connected but not that the system produces correct output.

```python
# BAD: asserts mock was called, not that output is correct
def test_sends_notification():
    mock_send = Mock()
    notifier = Notifier(mock_send)
    notifier.notify(user_email)
    assert mock_send.called
    mock_send.assert_called_once_with(to=user_email, body="...")
```

Remediation: Assert on the real boundary effect — the file that was written, the database row that was inserted, the API response that was returned. If the code path is simple enough that a mock assertion is the only way to verify it, consider whether the test adds value at all (the path is trivially correct by inspection) or whether an integration test would cover it.

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

<a id="remediation-source-policing-in-tests"></a>

### [SOURCE-POLICING] Remediation: Source Policing in Tests

Slop pattern: A test reads the source code of the application and asserts that certain strings, patterns, or symbols do or do not appear in the text. Examples: asserting `"fallback" not in source` to verify there are no fallback branches, scanning files for deprecated function names, asserting on line counts.

```python
# BAD: test asserts on source code text
def test_no_fallback():
    source = Path("src/module.py").read_text()
    assert "fallback" not in source  # source policing instead of behavior testing
```

Remediation: Move source-text assertions to global QC (lint rules, AST checks, dedicated static analysis). Tests assert on runtime behavior, not on source text. The runtime behavior — whether a fallback is actually reachable — is what matters; source text is an unreliable proxy.

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

### [DELETION-LAUNDERING] Remediation: Deletion Laundering / Proof-Burden Erasure

Slop pattern: A criticized slop artifact is deleted without solving or recording the original problem it attempted to address. The codebase looks cleaner, but the proof burden is now hidden. The next agent is likely to recreate the same fake proof, fallback, wrapper, or harness because the original requirement is absent from the new PR narrative.

Detection:
- deletion follows review or user criticism;
- commit message emphasizes cleanup, removal, or simplification;
- no replacement proof or capability exists;
- no issue, contract, or blocker records the original problem;
- final report says the review item is resolved because the artifact is gone;
- the original requirement is absent from the new PR narrative.

Remediation: Require a burden disposition: the original problem must be either solved, invalidated, transferred to real proof, or explicitly recorded as unresolved. Deletion is not a disposition — it is the removal of an artifact. The record of what was wrong and why must survive the deletion.

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

### [BESPOKE-DEP] Remediation: Bespoke Dependency Reinvention

Slop pattern: Application code reimplements what an existing, installed dependency already provides — custom React components when a UI library has them, hand-rolled YAML generation when a YAML library is installed, bespoke string parsing when a parser exists, custom pagination when a framework provides it. The model perceives the generic, tested solution as "abstraction layer bloat" and the bespoke reinvention as "clean, minimal code."

Examples:
- Custom `AcademicCard.tsx` (~60 LOC) when `card.tsx` exists in the UI inventory.
- Custom `FilterControls.tsx` with hand-rolled popover logic when `select.tsx`, `dropdown-menu.tsx`, and `scroll-area.tsx` already exist.
- Custom `PaginatedScroller.tsx` with bespoke scroll logic when `scroll-area.tsx` + `pagination.tsx` already exist.
- Custom string-concatenated YAML generation when a YAML library is installed.
- Custom hand-rolled AST stringifier when the parser library already provides stringification.

Remediation: REFINE, REPLACE, REFACTOR — migrate the bespoke implementation to use the dependency. For every custom function or component, ask: "Is there a standard library or installed dependency that already solves this?" If yes, the custom code is technical debt. Do not delete the dependency because it is "unused" — it was unused because the bespoke code was written instead of using it.

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
