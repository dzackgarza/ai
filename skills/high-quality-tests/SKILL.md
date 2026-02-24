---
name: high-quality-tests
description: Use when writing or reviewing tests for new features, bug fixes, or improving existing test quality
---

# High Quality Tests

This skill provides quality requirements for writing substantive, verifiable tests.

## 0. Coverage Goals

- Cover every interesting algorithm/method surfaced by the supported systems.
- Require explicit consideration of optional packages and add-on libraries before declaring testing complete.
- Prevent useful methods from going untested.
- Exclude only generic routines that are standard functionality, unless the method is specialized to nonstandard domains or structures.

Standard generic algorithms usually excluded:
- generic kernel/image/rank/eigenvalue routines over standard domains
- generic arithmetic and format conversion methods

Standard algorithms that must be included when specialized:
- methods whose contract depends on domain-specific structure
- methods tied to specialized regimes
- methods with domain-specific semantics

Example (mathematical): Generic `eigenvalues()` over `RR` is excluded, but `eigenvalues()` over number fields or p-adics is included because it has lattice-specific semantics (genus, local densities, discriminant forms).

## 1. Assertions Must Be Substantive

- Every test must assert a meaningful property, identity, invariant, or equivalence.
- Assertions should go beyond API existence and check correctness of output content.
- Prefer properties like:
  - invariant preservation (discriminant, determinant, signature, rank)
  - algebraic identities (polarization, duality, reciprocity)
  - structural equivalence
  - exact reconstruction/roundtrip behavior

Example (mathematical): Assert `L.discriminant() == expected_disc` instead of `assert L.discriminant() is not None`.

## 2. Keep Runtime Small; Mark Heavy Tests

- Avoid tests that take more than ~30 seconds.
- Use minimal examples that still validate correctness.
- For expensive algorithms, test small but representative inputs.
- If a heavy test is unavoidable, mark it explicitly (for example with `pytest.mark.slow`) and keep it out of default fast runs when possible.

## 3. No Content-Free Assertions

The following are disallowed as primary assertions:

- `is not None`
- `hasattr(...)`
- `isinstance(...)` (unless type is itself a core contract and accompanied by a substantive assertion)
- non-emptiness existence checks such as:
  - `len(x) > 0`
  - `len(x) >= 1`
  - `bool(x)`
  - `x != []`
  - placeholders such as:
    - `assert len(reps) > 0`
  - wrappers of the above like:
    - `actual = len(x) > 0; expected = True; assert actual == expected`

Why this is not useful:
- It validates object presence, not correctness.
- It can pass even when the implementation is wrong.
- It does not document expected behavior.

Instead, assert relations between computed values and expected outcomes.

### 3.1 No Trivial Primary Witnesses

- Do not use trivial objects as the primary witness for a test.
- Trivial objects include:
  - zero values/empty defaults,
  - identity elements,
  - empty structural objects.
- Use nontrivial witnesses as the primary example.
- Trivial objects may appear only as secondary consistency checks after a nontrivial primary assertion.

Example (mathematical): Testing a reflection method with the zero vector is trivial. Test with a nonzero root: assert `s(r) == -r` and `s(v) == v - 2*v.dot_product(r)/r.dot_product(r)*r`.

Examples of acceptable replacements:

- Verify exact known values for canonical small examples.
- Verify invariants/identities (determinant, discriminant, rank, product formulas).
- Verify reconstruction/roundtrip correctness.
- For returned collections, assert specific expected content, not just non-emptiness.

Representative-list replacement pattern:

- Bad:
  - `reps = method(...)`
  - `assert len(reps) > 0`
- Good:
  - `reps = method(...)`
  - assert at least one representative is exactly the expected canonical object, or
  - assert every representative satisfies the defining invariant with explicit diagnostics.

Example (mathematical): `assert reps[0] == expected_canonical_representative` or `assert all(r.is_equivalent(expected) for r in reps)`.

## 4. Use Precise Types

- Do not use vague types like `object` or `Any` where concrete types are known.
- Use explicit types where relevant.
- Input types should match method contracts.

Example (mathematical): Use `ZZ`, `QQ`, vectors, matrices rather than generic types.

## 4.5 Keep Assertions Direct (Avoid Ceremony)

- Avoid synthetic tuple wrappers that restate the same value just to format assertions.
- Do not build helper pairs like `(actual, baseline)` vs `(expected, baseline)` when the contract is a single equality.
- Prefer direct assertions with explicit diagnostics.

Why this matters:
- Wrapper assertions add noise without increasing signal.
- Repeating the same baseline term can hide what is actually being tested.
- Direct assertions make the contract obvious.

Example (mathematical):

- Overly verbose:
  - `actual_pairing_pair = (L.pairing(x, y), x * y)`
  - `expected_pairing_pair = (x * y, x * y)`
  - `assert actual_pairing_pair == expected_pairing_pair`
- Preferred:
  - `actual = L.pairing(x, y)`
  - `expected = x * y`
  - `assert actual == expected, f"pairing mismatch: actual={actual}, expected={expected}"`

## 5. Document Entry-Point Interoperability

For each module/entry point, test conversion routes into/out of related modules when applicable.

Examples (mathematical):
- `IntegralLattice` <-> discriminant module / genus / Gram matrix objects
- `TernaryQF` -> `QuadraticForm`
- `BinaryQF` <-> polynomial representations
- `NumberField` interactions with ideals/modules

The goal is to capture workflow boundaries, not just isolated methods.

## 5.5 Interoperability Checks Are Not Correctness Proofs

- Cross-entry-point equality checks are useful, but weak when used alone.
- Treat these as interface-consistency checks, not correctness tests.
- Do not rely only on "same result from two APIs" when both APIs may share the same implementation path.

Why this is weak by itself:
- Both calls can return the same wrong result and still pass.
- A single sampled object gives narrow coverage.
- It documents plumbing agreement, not the defining contract.

Required strengthening:
- Add at least one independent oracle assertion:
  - fundamental laws (involution laws, invariant preservation),
  - contract verification,
  - known canonical small-example outputs.
- Prefer checking multiple representative inputs instead of only index `0`.

Example (mathematical):

- Weak-only:
  - compute `from_root = r.reflection()` and `from_lattice = L.reflection(r)`
  - assert equality
- Stronger:
  - keep the equality assertion
  - AND add `assert s(s(x)) == x` (involution law)
  - AND add `assert s(root) == -root` (reflection law)

## 6. No xfail Masking

- Do not use `pytest.mark.xfail`, `xfail(strict=False)`, or similar expected-failure mechanisms.
- Do not hide known breakage behind pass-by-design markers.
- Suite status must reflect actual runtime functionality:
  - passing tests document behavior that works
  - failing tests document behavior that currently does not work

The target is not an artificial 100% green dashboard. The target is accurate documentation of the current implemented surface.

## 7. Optional Package Completeness Pass Is Mandatory

Before signing off on coverage completeness for a system:

- enumerate core methods and optional package methods relevant to the domain
- check each package for interesting algorithms, not only commonly used constructors
- classify each discovered method as:
  - tested and documented
  - irrelevant infrastructure
  - missing and requiring a new test entry
- do not assume package methods are out of scope simply because they are add-ons

Example (mathematical): For GAP, this includes crystallographic, toric/polyhedral, and integer-relation ecosystems when mathematically relevant to lattice workflows.

## 8. Method Triage: Interesting vs Generic

When deciding whether a method must be tested:

- Include if it changes or studies meaningful invariants/classification/search spaces.
- Include if it is algorithmically nontrivial and used in workflows.
- Exclude if it is purely generic plumbing with no specific contract.
- Re-include excluded generic methods if they are specialized to nonstandard domains or have domain-specific semantics.

Example (mathematical): `matrix_kernel()` over `ZZ` is included (lattice-specific, returns sublattice), but over `RR` is excluded (generic linear algebra).

## 9. Anti-Obfuscation

- Blacklists must never hide interesting algorithms.
- Every blacklist entry should be auditable as infrastructure-only; if uncertain, treat it as in-scope and test it.
- Coverage scope must be validated at the right abstraction level:
  - do not over-narrow module prefixes or types in a way that excludes higher-level methods users actually call
  - explicitly check for methods present on higher-level modules
- Completeness reviews must include a "hidden surface" pass:
  - methods excluded by blacklist
  - methods omitted due to tight filters
  - methods available on parent APIs but absent from test surfaces

## Practical Author Checklist

Before finalizing a test:

1. Does the assertion prove a nontrivial fact?
2. Would this still catch an implementation returning arbitrary non-empty junk?
3. Is the claim specific enough to fail on wrong output?
4. Is the case minimal but representative?
5. Is runtime reasonable for default test runs?
6. Are inputs strongly typed and contract-correct?
7. If this method bridges modules, does the test document the bridge?
8. Is the test result honest (no xfail masking)?
9. Was the optional-package surface checked and triaged?
10. If this is a generic method, is there a clear reason it is domain-relevant?
11. Could blacklist entries or narrow filters be hiding higher-level methods?
