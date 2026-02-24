# Example Task: Test Quality Repair

## Goal

Take tests flagged as inadequate in a previous audit. Repair them to meet `TEST_QUALITY.md` requirements.

## Prerequisites

This task assumes a prior audit identified specific tests with specific inadequacies. Do not start this task without audit results.

## Allowed Repairs

### Replace Content-Free Assertions

```python
# Before (INADEQUATE)
result = L.genus()
assert result is not None

# After (ADEQUATE)
result = L.genus()
assert len(result.representatives()) == 2, "E8⊕E8 and D16+ should be only genus reps"
assert all(r.determinant() == 1 for r in result.representatives())
```

### Replace Trivial Witnesses

```python
# Before (INADEQUATE) — zero vector
v = L.zero()
assert L.shortest_vector() == v

# After (ADEQUATE) — nontrivial example
L = IntegralLattice("E8")
v = L.shortest_vector()
assert v.norm() == 2, "E8 shortest vectors have norm 2"
assert v in L.roots(), "Shortest vectors in E8 are roots"
```

### Strengthen Interoperability-Only Tests

```python
# Before (INADEQUATE) — only cross-API check
from_root = r.reflection()
from_lattice = L.reflection(r)
assert from_root == from_lattice

# After (ADEQUATE) — add independent oracle
from_root = r.reflection()
from_lattice = L.reflection(r)
assert from_root == from_lattice
# Independent contract: reflection is involution
assert from_root.apply(from_root) == r
# Independent contract: hyperplane orthogonal to root
assert from_root * r == -r
```

### Remove Assertion Ceremony

```python
# Before (INADEQUATE)
actual_pair = (L.pairing(x, y), x * y)
expected_pair = (x * y, x * y)
assert actual_pair == expected_pair

# After (ADEQUATE)
assert L.pairing(x, y) == x * y, f"pairing mismatch for x={x}, y={y}"
```

## What NOT To Do

- **Do NOT run tests** — code correctness is verified by reading, not execution
- **Do NOT change test logic** — only fix assertion quality
- **Do NOT add new tests** — only repair flagged tests
- **Do NOT remove `xfail` markers** — that requires separate task with user approval
- **Do NOT fix environment/dependency issues**
- **Do NOT "fix" tests by making them simpler** — make them mathematically stronger

## Repair Constraints

- Preserve the original test's intent and method under test
- Use the same test file location and function name
- Keep runtime reasonable (~30s max)
- Do not introduce new dependencies
- Use strongly typed inputs matching method contracts

## Output

For each repaired test:
```markdown
## `test_<name>` in `<file>`
- Inadequacy: [e.g., "content-free assertion"]
- Repair: [e.g., "Added assertion checking determinant of genus representatives"]
- Lines changed: [e.g., "45-47"]
```

## Success Criteria

- All flagged inadequacies addressed
- No new inadequacies introduced
- Tests still test the same methods
- No tests were run during this task
