# Global QC Bridge-Burning Policy Detectors — Implementation Plan

**Goal:** Add automated detectors to the global QC stack that flag bridge-burning
policy violations across Python, TypeScript, Rust, and Shell.

**Architecture:** Extend the existing `semgrep.yml` with ~30 new language-specific
rules (no new files needed for semgrep). Add 3 ast-grep rules for structural patterns
semgrep cannot express well. Both tools are already in the test chain — new rules
activate automatically. Only the Rust justfile needs a wiring fix (missing
`_ast-grep`).

**Key design choice:** All new rules start at severity WARNING (non-blocking) to avoid
breaking existing projects. Escalation to ERROR is a separate pass after the rules
have been validated on real codebases.

---

## Task 1: Python semgrep rules — defaults and optionality

**Objective:** Add 6 rules for runtime defaulting and optionality patterns.

**Files:** `~/ai/quality-control/semgrep.yml`

**Rules:**

| id | Pattern | Policy |
|----|---------|--------|
| `py-no-getenv-default` | `os.getenv($KEY, $DEFAULT)` — warns on any env-var defaulting | #1: No defaults |
| `py-no-dict-get-default` | `$DICT.get($KEY, $DEFAULT)` — dict get with default | #1: No defaults |
| `py-no-getattr-default` | `getattr($OBJ, $ATTR, $DEFAULT)` — attribute defaulting | #1: No defaults |
| `py-no-setdefault` | `$DICT.setdefault($KEY, $DEFAULT)` — setdefault | #1: No defaults |
| `py-no-defaultdict` | `defaultdict($DEFAULT)` — implicit default factory | #1: No defaults |
| `py-no-optional-type` | `$VAR: Optional[$TYPE]` or `$VAR: $TYPE \| None` — optional types in core state | #1: No defaults |

**Verify:** `uvx --from semgrep semgrep scan --config ~/ai/quality-control/semgrep.yml` returns 0.

---

## Task 2: Python semgrep rules — fallbacks, mocks, test skips

**Objective:** Add 8 rules for fallback chains, mock imports, test skipping, and
silent error handling.

**Files:** `~/ai/quality-control/semgrep.yml`

**Rules:**

| id | Pattern | Policy |
|----|---------|--------|
| `py-no-try-import` | `try:\n    import $MOD\nexcept ImportError:` — optional dep | #3: No optional critical deps |
| `py-no-bare-except` | `except:\n    pass` — braindead catch | #2: No fallbacks |
| `py-no-except-pass` | `except $EXC:\n    pass` — silent catch | #2: No fallbacks |
| `py-no-suppress` | `contextlib.suppress($EXC)` — suppressed exception | #2: No fallbacks |
| `py-no-mock-import` | `from unittest.mock import $X` or `import unittest.mock` | #6: No mocks |
| `py-no-magicmock` | `MagicMock(...)` or `Mock(...)` — mock objects | #6: No mocks |
| `py-no-monkeypatch` | `monkeypatch.setattr(...)` — test seam | #6: No mocks |
| `py-no-skip-test` | `@pytest.mark.skip` or `@pytest.mark.xfail` — test bypass | #5: No proof-free smoke tests |

---

## Task 3: TypeScript semgrep rules

**Objective:** Add 7 rules for TypeScript bridge-burning patterns.

**Files:** `~/ai/quality-control/semgrep.yml`

**Rules:**

| id | Pattern | Policy |
|----|---------|--------|
| `ts-no-nullish-default` | `$X ?? $DEFAULT` where `$DEFAULT` is a literal | #1: No defaults |
| `ts-no-or-default` | `$X \|\| $DEFAULT` where `$DEFAULT` is a literal | #1: No defaults |
| `ts-no-env-default` | `process.env.$KEY \|\| $DEFAULT` | #1: No defaults |
| `ts-no-jest-mock` | `jest.mock(...)` | #6: No mocks |
| `ts-no-vi-mock` | `vi.mock(...)` | #6: No mocks |
| `ts-no-skip-test` | `test.skip(...)` / `describe.skip(...)` / `test.fixme(...)` | #5: No proof-free smoke tests |
| `ts-no-catch-console` | `.$ERR.catch(console.error)` — async error laundering | #2: No fallbacks |

---

## Task 4: Rust semgrep rules

**Objective:** Add 7 rules for Rust bridge-burning patterns.

**Files:** `~/ai/quality-control/semgrep.yml`

**Rules:**

| id | Pattern | Policy |
|----|---------|--------|
| `rs-no-unwrap-or` | `.$X.unwrap_or($DEFAULT)` — default fallback | #1: No defaults |
| `rs-no-unwrap-or-default` | `.$X.unwrap_or_default()` — default via Default trait | #1: No defaults |
| `rs-no-result-ok` | `.$X.ok()` on Result — swallowed error | #13: No swallowed errors |
| `rs-no-filter-map-ok` | `filter_map(Result::ok)` — batch-swallowed errors | #13: No swallowed errors |
| `rs-no-stringly-error` | `Result<$OK, String>` — string errors | #11: No stringly typed errors |
| `rs-no-serde-default` | `#[serde(default)]` on struct fields — config defaults | #1: No defaults |
| `rs-no-allow-attr` | `#[allow(...)]` — bypass attribute | #14: No bypass comments |

---

## Task 5: Shell semgrep rules

**Objective:** Add 3 rules for Shell bridge-burning patterns.

**Files:** `~/ai/quality-control/semgrep.yml`

**Rules:**

| id | Pattern | Policy |
|----|---------|--------|
| `sh-no-command-v-runtime` | `if command -v $TOOL >/dev/null 2>&1; then $CMD; else $FALLBACK; fi` — runtime fallback chain | #2: No fallbacks |
| `sh-no-or-true` | `\|\| true` — error suppression | #13: No swallowed errors |
| `sh-no-pip-install` | `pip install` — violates tool-provisioning policy | Cross-cutting |

---

## Task 6: ast-grep rules for structural patterns

**Objective:** Add 3 rules for structural patterns semgrep cannot express well.

**Files:**
- Create: `~/ai/quality-control/ast-grep/rules/no-boolean-param.yml`
- Create: `~/ai/quality-control/ast-grep/rules/no-field-default.yml`

**Python `no-boolean-param.yml`:**

Detects boolean parameters in Python function definitions (policy #8: no boolean mode
flags). Flagged at WARNING — some boolean params are legitimate flags, but all deserve
scrutiny.

**Python `no-field-default.yml`:**

Detects `Field(default=...)` in pydantic model definitions (policy #1: no defaults in
runtime logic). The config should be complete; Field defaults let agents silently
bypass the completeness requirement.

---

## Task 7: Wire `_ast-grep` into Rust test chain

**Objective:** The Rust justfile does not include `_ast-grep` in its `test` chain.
Since we are adding ast-grep rules for bridge-burning patterns, we need to include
them for Rust projects too.

**Files:** `~/ai/quality-control/justfile-rust`

**Change:** Add `_ast-grep` to the `test` recipe dependency list:

```
-test: _check-rust-project _check-no-local-qc-override _clippy _rustfmt _cargo-test _no-bypass _semgrep _jscpd _lizard _codeql _vibecheck _slop
+test: _check-rust-project _check-no-local-qc-override _clippy _rustfmt _cargo-test _no-bypass _semgrep _jscpd _lizard _codeql _vibecheck _slop _ast-grep
```

---

## Future work (not in scope)

- Escalate rules from WARNING to ERROR after validation
- Add rule for `Partial<T>` in TypeScript normalized/core state
- Add rule for `match` on `bool` in Rust (`ast-grep` cannot yet express this well)
- Add rule for `#[cfg(test)]` fake implementations that override production behavior
- Add rule for `2>/dev/null` stderr suppression in diagnostic/build contexts

---

## Commit strategy

7 tasks → 7 commits. Each commit is self-contained (adds rules for one language or
aspect). This makes it easy to revert or adjust individual rule sets without affecting
others.
