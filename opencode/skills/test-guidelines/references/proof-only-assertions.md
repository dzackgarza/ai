# Proof-Only Assertions Policy

This is the canonical catalog of banned test patterns and allowed proof-bearing replacements.

## Hard Rule

A test line is admissible only if it increases the epistemic status of a repository-owned proof burden.
If an assertion would still pass on a plausibly broken app, it is banned.
No assertion without discrimination.

When writing or reviewing tests, ask of each assertion line:
> "What broken app would still pass this?"

If the answer is "many" or "I don't know," delete or replace the assertion.

---

## Banned Language-Agnostic Assertion Classes

### 1. Existence-only assertions
**Ban:**
```text
file exists
element exists
module exports symbol
function exists
object has field
database row exists
process started
server responded
```
*Why banned:* Existence is almost never the owned behavior. A broken app can create an empty file, export a no-op function, show an inert button, or insert a junk row.
*Replacement:* Assert the file content, schema, side effect, user-visible state, or domain invariant. A file-creation test must prove the file has the expected content and was produced through the real path, not merely that a path exists.

### 2. Visibility-only assertions
**Ban:**
```ts
await expect(page.getByTestId("editor")).toBeVisible()
await expect(page.locator("#status")).toContainText("ready")
```
*Why banned:* A completely broken app can render the shell, show "ready," and have no working IPC, save path, renderer, or state model. Visibility is at most synchronization; it is not proof.
*Replacement:* Perform a real user action through the real boundary and assert the semantic result.

### 3. Truthiness and non-empty assertions
**Ban:**
```python
assert result
assert len(items) > 0
assert response.ok
```
*Why banned:* Arbitrary junk satisfies these. They are anti-junk failures by construction.
*Replacement:* Assert exact semantic values, invariants, or structured outputs.

### 4. Exact string assertions
**Ban:**
```rust
assert_eq!(error, "pandoc-preview config is missing pandoc.render_command");
```
*Why banned:* Strings are easy to manipulate and often only prove the agent copied the review wording into the code.
*Replacement:* Structured error type, code, key, or product-owned diagnostic object.

### 5. Type-only and shape-only assertions
**Ban:**
```python
assert isinstance(result, dict)
assert isinstance(user, User)
assert set(result.keys()) == {"id", "name"}
```
*Why banned:* Shape is not semantics. A fake object with the right fields passes.
*Replacement:* Assert exact domain values, state transitions, or invariants.

### 6. No-throw / no-error assertions
**Ban:**
```python
func()  # test passes if no exception
```
*Why banned:* "Did not crash" is not correctness. It is a precondition for proof.
*Replacement:* Assert what changed, what was produced, or which invariant now holds.

### 7. Source-text / AST / implementation-shape tests
**Ban from ordinary project tests:**
```text
assert source does not contain "unwrap_or"
assert source does not contain "as any"
assert file imports X
assert function delegates to Y
assert code contains kill_on_drop
assert no fallback string appears
```
*Why banned:* This is policy policing, not product proof. It belongs in global QC if it belongs anywhere.

### 8. Tests for absence of banned constructs
**Ban:**
```text
test_no_mocks_present
test_no_fallbacks_present
test_no_runtime_defaults_present
test_no_type_ignores_present
test_no_stringly_errors_present
```
*Why banned:* These are global QC detectors masquerading as project tests.
*Correct routing:* Policy policing belongs in global QC. Behavior proof belongs in project tests.

### 9. Helper-only tests for boundary obligations
**Ban as primary proof:**
```rust
require_or_default(None, true, "missing key", || default).unwrap_err()
```
*Why banned:* The test forces the branch instead of constructing the world. It proves the helper, not the boundary. Helper tests may be kept only after boundary proof exists. They may never resolve a boundary-level review concern.

### 10. Boolean branch-forcing tests
**Ban tests where `true` / `false` stands in for real system state:**
```rust
require_or_default(None, true, ...)
```
*Why banned:* Branch forcing is how agents avoid the hard part: real files, real config, real process, real IPC, real network, real lifecycle.
*Replacement:* Create the actual state: file exists, config absent, malformed TOML, live child process, real request, real user action.

### 11. Tests that would pass if production stopped using the code under test
**Ban as primary proof:**
```text
tests for newly extracted helper
tests for utility added during review response
tests for adapter not wired into production
tests for config parser not called by startup
```
*Why banned:* These tests do not protect the owned behavior. A regression test must fail when the product regression exists. If production can stop calling the tested helper and the test still passes, the test is not regression proof.

### 12. Tests against APIs/helpers that did not exist before the fix
**Ban as regression proof:**
```text
create helper -> write tests for helper -> claim red/green
```
*Why banned:* If the tested API did not exist before the patch, the test cannot demonstrate the original failure. It may be supplementary unit coverage after the real regression proof exists.

### 13. Mock, fake, stub, spy, and call-count assertions
**Ban:**
```python
mock.assert_called_once_with(...)
```
*Why banned:* Call counts prove choreography with a fake. They do not prove the real system works.
*Replacement:* Assert the real effect through the real boundary.

### 14. Snapshot assertions unless exact output is the product
**Ban broad snapshots of:**
```text
DOM tree
logs
errors
serialized internal state
HTML output
JSON blob
config dump
```
*Why banned:* Snapshots freeze current implementation output. Agents use them to ratify whatever the app currently does.
*Allowed:* Compiler/codegen output when exact text is the product; CLI output documented as stable protocol; published file format fixture with independent oracle.

### 15. Import/module-load/constructor tests
**Ban:**
```python
import package
Model()
assert model.id is None
```
*Why banned:* These tests mostly prove the language/runtime can instantiate a class.
*Replacement:* Exercise a real operation and assert a semantic result.

### 16. “Ready” / status-label assertions
**Ban:**
```ts
await expect(page.locator("#status")).toContainText("ready")
```
*Why banned:* Fake success labels are a classic slop pattern. A no-op app can print "ready."
*Replacement:* Assert the user-visible capability that "ready" claims is available.

### 17. Log/warning assertions
**Ban:**
```python
assert "warning" in caplog.text
```
*Why banned:* Warnings are often graceful-degradation laundering. The correct behavior is usually fail loudly or produce a structured error.
*Allowed:* Only when log output is the product contract, such as a CLI diagnostic tool.

### 18. HTTP/API status-only assertions
**Ban:**
```python
assert response.status_code == 200
```
*Why banned:* A fake or empty endpoint can return 200.
*Replacement:* Assert status, schema, semantic fields, and owned side effects.

### 19. Database count/existence assertions
**Ban:**
```sql
SELECT COUNT(*) FROM documents;
```
*Why banned:* Junk rows satisfy counts.
*Replacement:* Assert exact row values, constraints, relationships, and absence of unrelated mutation.

### 20. Round-trip tests with shared implementation
**Ban weak round trips where the same implementation owns both directions:**
```python
assert decode(encode(x)) == x
```
*Why banned:* Two wrong functions can agree.
*Replacement:* Use independent fixtures, external known truths, or one direction against a published contract.

### 21. Performance/timing assertions in ordinary tests
**Ban:**
```python
assert elapsed < 100
```
*Why banned:* They are flaky and often chase imagined issues. Race conditions should be tested deterministically, not by sleeps.

### 22. “No console errors” as sole proof
**Ban tests whose only meaningful claim is:**
```text
no console errors happened
```
*Why banned:* Absence of console errors does not prove behavior.
*Replacement:* Semantic product assertions + frontend error gate.

---

## Language-Specific Banned Examples

### Python / pytest

**Ban:**
```python
def test_returns_something():
    result = run()
    assert result

def test_has_items():
    assert len(load_items()) > 0

def test_error_message():
    with pytest.raises(ValueError) as exc:
        load_config("bad.toml")
    assert "missing render_command" in str(exc.value)

def test_helper_branch():
    assert require_or_default(None, True, "missing", lambda: "default") == "missing"

def test_file_created(tmp_path):
    output = generate(tmp_path)
    assert output.exists()

def test_no_fallbacks_in_source():
    assert "fallback" not in Path("src/config.py").read_text()
```

**Prefer:**
```python
def test_existing_incomplete_config_fails_at_startup(tmp_path):
    config = tmp_path / "pandoc-preview.toml"
    config.write_text("[pandoc]\nfilters_dir = 'filters'\n")

    with pytest.raises(ConfigError) as exc:
        build_initial_state(config_path=config)

    assert exc.value.kind == "missing_required"
    assert exc.value.key == "pandoc.render_command"

def test_generates_expected_pandoc_html(tmp_path):
    output = render_markdown("# Title\n\nBody")
    assert normalize_html(output.html) == normalize_html("<h1>Title</h1><p>Body</p>")
```

### TypeScript / Jest / Vitest / Playwright

**Ban:**
```ts
expect(result).toBeTruthy();
expect(items.length).toBeGreaterThan(0);
expect(component).toBeDefined();
expect(screen.getByText("Ready")).toBeVisible();
await expect(page.getByTestId("editor")).toBeVisible();
expect(() => parse(input)).not.toThrow();
expect(error.message).toContain("missing");
expect(source).not.toContain("as any");
expect(spy).toHaveBeenCalledWith("render");
```

**Prefer:**
```ts
test("saving writes the selected markdown file through real IPC", async ({ page }) => {
  await openRealDocument(page, "notes/example.md");
  await page.getByRole("textbox", { name: /markdown/i }).fill("# Updated");
  await page.getByRole("button", { name: /save/i }).click();

  await expect(page.getByTestId("save-status")).toHaveText("saved");
  expect(await readFile("notes/example.md")).toBe("# Updated\n");
});

// For UI visibility:
await page.getByRole("button", { name: /render/i }).click();
await expect(page.getByTestId("preview-pane")).toContainText("Theorem");
```

### Rust

**Ban:**
```rust
assert!(result.is_ok());
assert!(items.len() > 0);
assert!(path.exists());
assert_eq!(err.to_string(), "missing render_command");
#[should_panic(expected = "missing render_command")]
assert_eq!(helper(None, true, "missing", || "default"), Err("missing".into()));
```

**Prefer:**
```rust
#[test]
fn existing_config_missing_render_command_fails_startup() {
    let dir = tempfile::tempdir().unwrap();
    let config = dir.path().join("pandoc-preview.toml");
    std::fs::write(
        &config,
        r#"
        [render]
        debounce_ms = 750

        [pandoc]
        templates_dir = "templates"
        filters_dir = "filters"
        "#,
    )
    .unwrap();

    let error = build_initial_state_from_config_path(Some(&config)).unwrap_err();

    assert!(matches!(
        error,
        ConfigError::MissingRequired { key } if key == "pandoc.render_command"
    ));
}

#[tokio::test]
async fn renderer_timeout_kills_child_process() {
    let child_marker = unique_marker();
    let result = execute_render_with_command(
        "# test",
        &format!("sleep 60 # {child_marker}"),
        Duration::from_millis(50),
    )
    .await;

    assert!(matches!(result, Err(RenderError::Timeout { .. })));
    assert_no_process_with_marker(child_marker);
}
```

### Bash / shell tests

**Ban:**
```bash
test -f output.html
grep -q "ready" output.log
cmd >/dev/null 2>&1
curl -s http://localhost:3000 | jq '.ok'
[ -n "$RESULT" ]
```

**Prefer:**
```bash
run_app_with_fixture ./fixtures/minimal.md >out.json 2>err.log
jq -e '.status == "rendered" and .html | contains("<h1>Minimal</h1>")' out.json
test ! -s err.log
```

### Go

**Ban:**
```go
require.NoError(t, err)
require.NotNil(t, result)
require.Len(t, items, 1)
require.Contains(t, err.Error(), "missing")
```

**Prefer:**
```go
var configErr *ConfigError
require.ErrorAs(t, err, &configErr)
require.Equal(t, "pandoc.render_command", configErr.Key)
```

### Java / Kotlin / JUnit

**Ban:**
```java
assertNotNull(result);
assertTrue(items.size() > 0);
assertThrows(RuntimeException.class, () -> loadConfig(path));
assertEquals("missing render_command", ex.getMessage());
```

**Prefer:**
```java
ConfigException ex =
    assertThrows(ConfigException.class, () -> loadConfig(path));
assertEquals(ConfigErrorKind.MISSING_REQUIRED, ex.kind());
assertEquals("pandoc.render_command", ex.key());
```

### SQL / data tests

**Ban:**
```sql
SELECT COUNT(*) FROM documents;
assert db.execute("select count(*) from documents").scalar() > 0
```

**Prefer:**
```python
row = db.fetch_one("select title, body, source_path from documents where id = ?", [doc_id])
assert row == {
    "title": "Expected title",
    "body": "Expected body",
    "source_path": "fixtures/example.md",
}
```
