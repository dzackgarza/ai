# Banned Test Shapes

This catalog lists test and assertion shapes that are structurally incapable of proving repository-owned behavior. These are not weak patterns. They are banned.

A test line is admissible only if it excludes a plausible broken implementation at the owned boundary. If the line would pass on a broken, fake, partial, mocked, unwired, or review-appeasing implementation, it does not belong in the test suite.

Project tests prove product behavior.
Global QC polices code shape.
Issues record unresolved proof burdens.

---

## Banned Shapes Are Not Checklists

The examples below are shapes, not literal-token rules.

Do not satisfy this policy by avoiding the exact variable names or exact APIs shown.
The pattern is banned whenever the assertion:
- checks existence instead of semantics;
- checks visibility instead of behavior;
- checks strings instead of structured errors;
- checks source shape instead of product behavior;
- checks helper branches instead of real boundaries;
- checks that a mock was called instead of checking a real effect;
- catches and inspects an exception instead of asserting a structured failure;
- would pass on arbitrary non-empty junk.

Variable names in examples are intentionally generic: `result`, `items`, `output_path`, `config_path`, `source`, `status`, `payload`, `boundary`, `helper`, `fallback`. They gesture at the general shape.

---

## Try/Catch Ban

Do not write try/catch/except/rescue blocks in tests or owned runtime code.

Banned:
- Python `try/except`
- JavaScript/TypeScript `try/catch`
- Ruby `begin/rescue`
- shell `cmd || fallback`, `set +e` around normal execution, or fallback branches
- Rust `let _ =`, `.ok()`, `unwrap_or`, `unwrap_or_else`, `match Err(_) => fallback`

Expected failures must be asserted by structured test-framework mechanisms or structured error values. Unexpected failures must propagate.

The only possible exception is an explicitly approved boundary renderer whose sole job is to translate a structured internal error into a user-facing protocol. That boundary must not continue execution, must not default, and must not return partial success.

---

## Per-Assertion Review Rubric

For each assertion line, classify it:

- **Proof-bearing**: excludes a plausible broken implementation at the owned boundary.
- **Setup/synchronization**: may help the test run, but cannot be cited as proof.
- **Policing**: checks source shape or validator compliance; move to global QC.
- **Laundering**: makes a weak/fake artifact look intentionally scoped.
- **Junk-tolerant**: would pass on arbitrary non-empty output; delete.

A test passes review only if its proof-bearing assertions are sufficient without counting setup, policing, laundering, or junk-tolerant lines.

---

## Language-Agnostic Banned Shapes

These are banned regardless of language:
- existence-only assertion
- visibility-only assertion
- truthy/non-empty assertion
- string assertion
- type-only assertion
- shape-only assertion
- no-throw assertion
- source-text assertion
- helper-branch assertion
- boolean branch-forcing assertion
- mock/spy/call-count assertion
- snapshot assertion where exact output is not the product
- import/module-load/constructor assertion
- status-label assertion
- log/warning assertion
- HTTP status-only assertion
- database count/existence assertion
- round-trip assertion with shared implementation
- timing/performance assertion in ordinary tests
- "no console errors" as sole proof
- "covered elsewhere" with no exact proof anchor

For every assertion line, force this question:
> **"What broken app would still pass this line?"**

If the answer is "many," ban the line.

---

## Python / pytest Banned Shapes

### Existence and non-null
**Ban:**
```python
def test_result_exists():
    result = run_owned_operation(input_payload)
    assert result is not None

def test_file_created(tmp_path):
    output_path = produce_artifact(tmp_path)
    assert output_path.exists()

def test_object_has_field():
    payload = load_payload()
    assert hasattr(payload, "items")
```
*Why banned:* A broken implementation can return `{}`, create an empty file, or attach a junk field.
*Remediation:* See [Remediation: Existence / Truthy / Shape as Proof](bridge-burning-red-flags.md#remediation-existence--truthy--shape-as-proof).

### Truthy / non-empty
**Ban:**
```python
def test_items_returned():
    items = collect_domain_items(source_path)
    assert items

def test_output_has_content():
    output = render_document(markdown)
    assert len(output.html) > 0

def test_response_ok():
    response = call_boundary(request_payload)
    assert response.ok
```
*Remediation:* See [Remediation: Existence / Truthy / Shape as Proof](bridge-burning-red-flags.md#remediation-existence--truthy--shape-as-proof).

### String assertions
**Ban:**
```python
def test_missing_config_message(tmp_path):
    with pytest.raises(Exception) as exc:
        load_config(tmp_path / "missing.toml")
    assert "missing render_command" in str(exc.value)

def test_error_banner(page):
    page.click("button")
    assert "failed" in page.text_content("#status")
```
*Remediation:* Use structured error types and assert on error kind, not message. See [Remediation: String-Based Error Types](bridge-burning-red-flags.md#remediation-string-based-error-types).

### Shape-only assertions
**Ban:**
```python
def test_payload_shape():
    payload = build_payload(domain_input)
    assert isinstance(payload, dict)
    assert set(payload.keys()) == {"title", "body", "metadata"}

def test_items_are_models():
    items = collect_items(source)
    assert all(isinstance(item, DomainItem) for item in items)
```
*Remediation:* Assert on concrete values against fixtures. See [Remediation: Existence / Truthy / Shape as Proof](bridge-burning-red-flags.md#remediation-existence--truthy--shape-as-proof).

### No-throw tests
**Ban:**
```python
def test_operation_does_not_crash():
    run_owned_operation(input_payload)

def test_config_loads(tmp_path):
    load_config(tmp_path / "app.toml")
```
*Remediation:* Assert on exact output values, not just that the operation did not crash. See [Remediation: No-Throw / No-Crash as Proof](bridge-burning-red-flags.md#remediation-no-throw--no-crash-as-proof).

### Source policing
**Ban:**
```python
def test_no_fallbacks_in_config_source():
    source = Path("src/config.py").read_text()
    assert "fallback" not in source
    assert "default" not in source

def test_no_type_ignore_comments():
    source = Path("src/module.py").read_text()
    assert "# type: ignore" not in source
```
*Why banned:* This belongs to global QC/static analysis, not project behavior tests.
*Remediation:* Move source-text assertions to global QC. Test runtime behavior instead. See [Remediation: Source Policing in Tests](bridge-burning-red-flags.md#remediation-source-policing-in-tests).

### Helper branch laundering
**Ban:**
```python
def test_existing_config_requires_explicit_values():
    error = require_or_default(
        value=None,
        config_exists=True,
        error_message="missing runtime.command",
        default_factory=lambda: "default-command",
    )
    assert error == "missing runtime.command"

def test_absent_config_uses_defaults():
    value = require_or_default(
        value=None,
        config_exists=False,
        error_message="must not be used",
        default_factory=lambda: 750,
    )
    assert value == 750
```
*Why banned:* The test passes the boolean that chooses the branch. It does not construct an existing or absent config.
*Remediation:* Test the source-of-truth boundary, not an extracted helper. See [Remediation: Boundary Test Bypass](bridge-burning-red-flags.md#remediation-boundary-test-bypass).

### Try/except in tests
**Ban:**
```python
def test_expected_failure():
    try:
        load_config(config_path)
    except Exception as error:
        assert "missing" in str(error)
```
*Remediation:* Use the test framework's structured assertion and assert on error kind. See [Remediation: String-Based Error Types](bridge-burning-red-flags.md#remediation-string-based-error-types).

### Mock/spy/call-count
**Ban:**
```python
def test_calls_renderer(mocker):
    renderer = mocker.Mock()
    save_document(renderer, content)
    renderer.render.assert_called_once_with(content)

def test_network_path(monkeypatch):
    monkeypatch.setattr(client, "get", lambda url: {"ok": True})
    assert load_remote_data(url)
```
*Remediation:* Assert the real effect at the owned boundary. See [Remediation: Mock/Spy/Call-Count as Proof](bridge-burning-red-flags.md#remediation-mockspycall-count-as-proof).

---

## TypeScript / JavaScript Banned Shapes

### Existence / defined / truthy
**Ban:**
```ts
test("returns result", () => {
  const result = runOwnedOperation(inputPayload);
  expect(result).toBeDefined();
});

test("has items", () => {
  const items = collectDomainItems(sourceText);
  expect(items.length).toBeGreaterThan(0);
});

test("module exports function", async () => {
  const module = await import("../module");
  expect(module.render).toBeTruthy();
});
```
*Remediation:* Assert on concrete values against fixtures. See [Remediation: Existence / Truthy / Shape as Proof](bridge-burning-red-flags.md#remediation-existence--truthy--shape-as-proof).

### Visibility-only
**Ban:**
```ts
test("editor shell renders", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByTestId("editor")).toBeVisible();
  await expect(page.getByTestId("preview-pane")).toBeVisible();
});

test("status is ready", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("#status")).toContainText("ready");
});
```
*Why banned:* A totally broken app can render a shell and display "ready."
*Remediation:* Assert on concrete output content, not visibility. See [Remediation: Existence / Truthy / Shape as Proof](bridge-burning-red-flags.md#remediation-existence--truthy--shape-as-proof).

### Status / label / banner assertions
**Ban:**
```ts
test("save shows success", async ({ page }) => {
  await page.getByRole("button", { name: /save/i }).click();
  await expect(page.locator("#status")).toContainText("saved");
});
```
*Remediation:* Assert on the real side effect (file content, database state), not UI labels. See [Remediation: Existence / Truthy / Shape as Proof](bridge-burning-red-flags.md#remediation-existence--truthy--shape-as-proof).

### String assertions
**Ban:**
```ts
test("shows error", async ({ page }) => {
  await page.getByRole("button", { name: /render/i }).click();
  await expect(page.locator(".error")).toContainText("render failed");
});

test("throws missing config", () => {
  expect(() => loadConfig(path)).toThrow("missing runtime.command");
});
```
*Remediation:* Assert on structured error types, not string messages. See [Remediation: String-Based Error Types](bridge-burning-red-flags.md#remediation-string-based-error-types).

### Type-only / shape-only
**Ban:**
```ts
test("returns array", () => {
  const items = collectItems(source);
  expect(Array.isArray(items)).toBe(true);
});

test("has html property", () => {
  const result = render(markdown);
  expect(result).toHaveProperty("html");
});
```
*Remediation:* Assert on concrete output values, not type/shape. See [Remediation: Existence / Truthy / Shape as Proof](bridge-burning-red-flags.md#remediation-existence--truthy--shape-as-proof).

### No-throw
**Ban:**
```ts
test("does not throw", () => {
  expect(() => loadConfig(configPath)).not.toThrow();
});

test("promise resolves", async () => {
  await expect(runOperation(input)).resolves.toBeDefined();
});
```
*Remediation:* Assert on exact output values, not just absence of throw. See [Remediation: No-Throw / No-Crash as Proof](bridge-burning-red-flags.md#remediation-no-throw--no-crash-as-proof).

### Source policing
**Ban:**
```ts
test("does not use any", () => {
  const source = readFileSync("src/fixture.ts", "utf8");
  expect(source).not.toContain("as any");
});

test("no fallbacks", () => {
  const source = readFileSync("src/config.ts", "utf8");
  expect(source).not.toContain("??");
  expect(source).not.toContain("||");
});
```

### Mocked boundary / browser smoke laundering
**Ban:**
```ts
test("browser shell renders", async ({ page }) => {
  await page.addInitScript(() => {
    window.__APP_INTERNALS__ = {
      invoke: async () => ({ ok: true, html: "<p>fake</p>" }),
    };
  });
  await page.goto("/");
  await expect(page.getByTestId("editor")).toBeVisible();
});
```

### Spy/call count
**Ban:**
```ts
test("save calls backend", async () => {
  const saveSpy = vi.fn();
  await saveDocument(saveSpy, content);
  expect(saveSpy).toHaveBeenCalledWith(content);
});

test("render invoked", async ({ page }) => {
  const invoke = vi.fn().mockResolvedValue({ ok: true });
  await runRender(invoke, "# Title");
  expect(invoke).toHaveBeenCalledTimes(1);
});
```

### Try/catch
**Ban:**
```ts
test("handles bad config", () => {
  try {
    loadConfig(path);
  } catch (error) {
    expect(String(error)).toContain("missing");
  }
});
```
*Remediation:* Test framework structured assertions with error types. See [Remediation: String-Based Error Types](bridge-burning-red-flags.md#remediation-string-based-error-types).

---

## Rust Banned Shapes

### `is_ok`, `is_some`, length, existence
**Ban:**
```rust
#[test]
fn operation_succeeds() {
    let result = run_owned_operation(input_fixture());
    assert!(result.is_ok());
}

#[test]
fn file_exists() {
    let path = produce_artifact(tempdir.path()).unwrap();
    assert!(path.exists());
}

#[test]
fn items_present() {
    let items = collect_items(source_fixture());
    assert!(!items.is_empty());
}
```
*Remediation:* Assert on concrete output content against fixtures. See [Remediation: Existence / Truthy / Shape as Proof](bridge-burning-red-flags.md#remediation-existence--truthy--shape-as-proof).

### Exact string errors
**Ban:**
```rust
#[test]
fn missing_config_errors() {
    let error = load_config(incomplete_config_path()).unwrap_err();
    assert_eq!(error.to_string(), "missing runtime.command");
}

#[test]
#[should_panic(expected = "missing runtime.command")]
fn config_panics() {
    load_config(incomplete_config_path()).unwrap();
}
```
*Remediation:* Assert on structured error variants, not string rendering. See [Remediation: String-Based Error Types](bridge-burning-red-flags.md#remediation-string-based-error-types).

### Helper branch proof
**Ban:**
```rust
#[test]
fn existing_config_requires_explicit_values() {
    let error = require_or_default::<String, _>(
        None,
        true,
        "missing runtime.command",
        || "default-command".to_string(),
    )
    .unwrap_err();
    assert_eq!(error, "missing runtime.command");
}
```
*Remediation:* Test the source-of-truth boundary, not an extracted helper. See [Remediation: Boundary Test Bypass](bridge-burning-red-flags.md#remediation-boundary-test-bypass).

### Boolean branch-forcing
**Ban:**
```rust
#[test]
fn branch_for_existing_config() {
    let result = normalize_runtime(None, true);
    assert!(result.is_err());
}

#[test]
fn branch_for_absent_config() {
    let result = normalize_runtime(None, false);
    assert_eq!(result.unwrap(), RuntimeConfig::default());
}
```
*Remediation:* Construct actual config state via real files, not boolean flags. See [Remediation: Boundary Test Bypass](bridge-burning-red-flags.md#remediation-boundary-test-bypass).

### Source policing
**Ban:**
```rust
#[test]
fn no_defaults_in_config_source() {
    let source = std::fs::read_to_string("src/config.rs").unwrap();
    assert!(!source.contains("unwrap_or"));
    assert!(!source.contains("Default::default"));
}
```

### Swallowed-error tests
**Ban:**
```rust
#[test]
fn cleanup_does_not_crash_when_file_missing() {
    cleanup_backup(missing_path()).unwrap();
}
```
*Remediation:* Assert on specific error variants or output values, not just absence of panic. See [Remediation: No-Throw / No-Crash as Proof](bridge-burning-red-flags.md#remediation-no-throw--no-crash-as-proof).

### Process lifecycle source-shape test
**Ban:**
```rust
#[test]
fn renderer_uses_kill_on_drop() {
    let source = std::fs::read_to_string("src/render.rs").unwrap();
    assert!(source.contains("kill_on_drop(true)"));
}
```
*Remediation:* Test runtime process behavior, not source text patterns. See [Remediation: Source Policing in Tests](bridge-burning-red-flags.md#remediation-source-policing-in-tests).

---

## Bash / Shell Banned Shapes

### Existence-only
**Ban:**
```bash
test -f "$output_file"
[ -s "$output_file" ]
[ -n "$result" ]
```
*Remediation:* Assert on concrete output content (diff, structured JSON). See [Remediation: Existence / Truthy / Shape as Proof](bridge-burning-red-flags.md#remediation-existence--truthy--shape-as-proof).

### Grep string assertions
**Ban:**
```bash
grep -q "ready" "$log_file"
grep -q "success" "$output_file"
grep -q "missing runtime.command" "$stderr_file"
```
*Remediation:* Assert on structured output with jq, not grep strings. See [Remediation: String-Based Error Types](bridge-burning-red-flags.md#remediation-string-based-error-types).

### Status-only
**Ban:**
```bash
curl -s "$url" >/tmp/response
test "$?" -eq 0

status="$(curl -s -o /dev/null -w '%{http_code}' "$url")"
test "$status" = 200
```
*Remediation:* Assert on concrete response content with structured checks. See [Remediation: Existence / Truthy / Shape as Proof](bridge-burning-red-flags.md#remediation-existence--truthy--shape-as-proof).

### Suppression / fallback
**Ban:**
```bash
command_under_test 2>/dev/null || echo "ok"
grep -q pattern file || true
run_check >/dev/null 2>&1
```

### Source policing
**Ban:**
```bash
! grep -R "unwrap_or" src
! grep -R "as any" src
! grep -R "fallback" src
```

---

## Final Language for the Skill

A test suite is not allowed to accumulate comforting facts.

Every assertion must carry proof weight. If an assertion does not increase the epistemic status of the owned behavior, it is not neutral; it is false signal. False signal is worse than no test because it teaches future agents that the burden is already discharged.

Ban the line.
