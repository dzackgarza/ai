---
name: test-patterns
description: Reference guide for detecting AI slop patterns in testing, including content-free checks, tautological assertions, and mock evasion.
---

# Testing Slop Patterns

This reference documents common "AI slop" patterns in tests that indicate low-quality, AI-generated content that provides the illusion of coverage without actual verification.

## Table of Contents

- Content-Free Verification
- Tautological Testing
- Mock-First Evasion
- Masking Over Failure

## Content-Free Verification

Tests that execute code but fail to verify meaningful output. They check for the presence of _something_ rather than the correctness of _the thing_.

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

## Tautological Testing

Tests that merely prove a system is internally consistent, rather than correct relative to an external oracle or ground truth.

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

## Mock-First Evasion

Agents frequently use `unittest.mock` to bypass the actual boundaries of a system, creating tests that run fast but prove nothing about how the repository interlocks with reality.

**Bad:**

```python
@patch('requests.get')
def test_fetch(mock_get):
    mock_get.return_value.json.return_value = {"status": "ok"}
    result = fetch_status()
    # Slop: Proves the mock works, not the implementation
    assert result == "ok"
```

**Better:**
Test against real data, captured offline fixtures, or an actual local proxy. If you must test the boundary, test how the system interprets a real external response, not how well you can simulate `requests`.

## Masking Over Failure

When a refactor introduces a regression, agents often attempt to hide the failure rather than fixing the implementation.

Watch for:

- Suddenly adding `@pytest.mark.xfail` or `skip` to a previously passing test.
- Rewriting the expectation to match the _new_ (incorrect) behavior of the refactored code.
- Asserting on the _type_ of error rather than fixing the code that throws it (e.g., changing a success test into a `pytest.raises()` test).

**Rule:** Tests define the specification. The implementation must rise to meet the tests; tests must not be relaxed to accommodate the implementation.
