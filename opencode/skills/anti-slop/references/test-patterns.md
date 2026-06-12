---
name: test-patterns
description: Reference guide for detecting AI slop patterns in testing, including content-free checks, tautological assertions, and mock evasion.
---
# Testing Slop Patterns

This reference documents common “AI slop” patterns in tests that indicate low-quality,
AI-generated content that provides the illusion of coverage without actual verification.

For adversarial review of LLM-produced test suites, also load
[`../../reviewing-llm-code/references/pattern-catalog.md`](../../reviewing-llm-code/references/pattern-catalog.md).
That file is the central catalog for developer-controlled assertions, regex
meta-testing, fake-data confidence, inflated suites, and QC bypasses.

## Table of Contents

- **[ CONTENT-FREE ]** Content-Free Verification

- **[ TAUTOLOGICAL ]** Tautological Testing
- **[ MOCK-FIRST ]** Mock-First Evasion
- **[ MASK-FAILURE ]** Masking Over Failure

## **[ CONTENT-FREE ]** Content-Free Verification

Tests that execute code but fail to verify meaningful output.
They check for the presence of *something* rather than the correctness of *the thing*.

**Bad:**

```python
def test_discriminant():
    L = Lattice(...)
    # Slop: Checks type and existence, not correctness
    assert L.discriminant() is not None
    assert isinstance(L.discriminant(), int)

def test_items():
    items = get_items()
    # Slop: Proves nothing about what the items actually are
    assert len(items) > 0
```

**Better:**

```python
def test_discriminant():
    L = Lattice(...)
    # Proves the exact nontrivial value
    assert L.discriminant() == -23

def test_items():
    items = get_items()
    # Proves the first item is the exact expected entity
    assert items[0] == ExpectedItem(...)
```

## **[ TAUTOLOGICAL ]** Tautological Testing

Tests that merely prove a system is internally consistent, rather than correct relative
to an external oracle or ground truth.

**Bad:**

```python
def test_group_order():
    G = SymmetricGroup(5)
    # Slop: Proves the length method matches the list method
    assert G.order() == len(G.list())
```

**Better:**

```python
def test_group_order():
    G = SymmetricGroup(5)
    # Proves the actual mathematical invariant
    assert G.order() == 120
```

## **[ MOCK-FIRST ]** Mock-First Evasion

Agents frequently use `unittest.mock` to bypass the actual boundaries of a system,
creating tests that run fast but prove nothing about how the repository interlocks with
reality.

**Bad:**

```python
@patch('requests.get')
def test_fetch(mock_get):
    mock_get.return_value.json.return_value = {"status": "ok"}
    result = fetch_status()
    # Slop: Proves the mock works, not the implementation
    assert result == "ok"
```

**Better:** Test against real data, captured offline fixtures, or an actual local proxy.
If you must test the boundary, test how the system interprets a real external response,
not how well you can simulate `requests`.

## **[ MASK-FAILURE ]** Masking Over Failure

When a refactor introduces a regression, agents often attempt to hide the failure rather
than fixing the implementation.

Watch for:

- Suddenly adding `@pytest.mark.xfail` or `skip` to a previously passing test.

- Rewriting the expectation to match the *new* (incorrect) behavior of the refactored
  code.

- Asserting on the *type* of error rather than fixing the code that throws it (e.g.,
  changing a success test into a `pytest.raises()` test).

**Rule:** Tests define the specification.
The implementation must rise to meet the tests; tests must not be relaxed to accommodate
the implementation.

## **[ HELPER-PROOF ]** Helper-Level Proof Substitution (Helper-Branch Proof Laundering)

Replacing a global or boundary-crossing contract with a local helper unit proof that is easy to satisfy.

The agent tests a small helper function in isolation (proving only that the helper's internal logic behaves as written) instead of proving that the actual application workflow, config discovery, parsing, or state-building behavior matches the required semantics. This is a form of proof laundering: the helper test passes, but the actual entrypoint remains unverified. It is often accompanied by brittle implementation assertions like matching exact non-public error strings.

### **[ HELPER-RED-FLAGS ]** Red Flags in Helper Tests

1. **Helper-local proof after boundary-level feedback:** Boundary feedback needs boundary proof. If the feedback is "startup config semantics are wrong," testing `require_or_default` is insufficient.
2. **Defaults existing inside a required-value pathway:** A helper named something like `require_or_default` indicates a suspicious conflation of required config values and default fallbacks. If a config exists and the value is required, there should be no fallback value in scope. The presence of a fallback closure in the same helper that enforces required explicit values preserves a slop surface, making it easy to call with the wrong boolean and default a required value.
3. **Boolean control flags to force branches:** Passing `true`/`false` flags (e.g., `require_or_default(None, true, ...)`) to simulate system state forces branches. The test does not construct the world where config exists or doesn't exist; it simply branches as desired. Ambient config discovery failures or path computation bugs will not be caught.
4. **Test names overclaiming system states:** Names like `existing_config_requires_explicit_values` or `absent_config_uses_defaults` are misleading if the body only passes `None` plus a boolean. The names claim product/system semantics; the bodies only prove helper semantics.
5. **Exact assertion on a string passed directly into the function under test:** Asserting that the function returned the exact string that the test itself passed to it is tautological. It proves plumbing, not behavior.
6. **Unused fallback closures in required-value paths:** If a test claims a fallback must not be used, passing a real fallback value is a weak check. A sentinel fallback that panics when evaluated (e.g., `|| panic!("must not be evaluated")`) is stronger, but boundary-level proof is still required.
7. **Prose encoded inside arguments:** The phrase `"must not be used"` passed as an argument to stand in for logic validation is a sign that the agent is checking its own local abstraction rather than product behavior.
8. **No real fixture representing the artifact:** A config contract should use actual TOML fixtures or temp config files. A filesystem boundary should use temp directories/files.
9. **No test for the successful explicit case:** Proving rejection of invalid input is not enough; there must be a complete config proving explicit values are accepted and used.
10. **The test would still pass if the app never called the helper:** If the application path stopped using the helper entirely, the unit tests would still pass. This proves they do not protect the behavior users depend on.

**Bad:**

The review feedback requested proof that "existing config with missing required render command fails loudly."

```rust
// Slop: Tests only the helper logic in isolation rather than the config parser/startup flow
#[test]
fn test_require_or_default() {
    let res = require_or_default(None, true, "missing pandoc.render_command", || DEFAULT_RENDER_COMMAND.to_string());
    assert!(res.is_err());
    assert_eq!(res.unwrap_err().to_string(), "pandoc-preview config is missing pandoc.render_command");
}
```

**Better:**

Exercise the real boundary (e.g. config loading and parsing) using a temp directory/file and structured errors:

```rust
#[test]
fn absent_config_uses_builtin_defaults() {
    let temp = tempdir();
    let state = build_initial_state_from_config_path(None, temp.path()).unwrap();

    assert_eq!(state.render_command, DEFAULT_RENDER_COMMAND);
    assert_eq!(state.timeout_ms, 750);
}

#[test]
fn existing_config_missing_render_command_fails_loudly() {
    let temp = tempdir();
    let config = temp.path().join("pandoc-preview.toml");
    fs::write(&config, r#"
        [render]
        debounce_ms = 750

        [pandoc]
        templates_dir = "templates"
        filters_dir = "filters"
    "#).unwrap();

    let error = build_initial_state_from_config_path(Some(&config), temp.path())
        .unwrap_err();

    assert!(matches!(
        error,
        ConfigError::MissingRequired { key } if key == "pandoc.render_command"
    ));
}
```
