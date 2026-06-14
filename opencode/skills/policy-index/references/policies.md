# Policy Database

This file is the canonical database of named bridge-burning policies. Other skills
may teach review, testing, debugging, or remediation workflows, but policy identity
and policy text live here.

Detector and reviewer agents may load this file. Fixer agents load
`remediations.md` only after triage assigns a `POLICY.*` code.

## Record Schema

Each policy record contains:

- `Category`: the policy family used for routing and reporting.
- `Rule`: the canonical obligation.
- `Invalid local fixes`: local edits that preserve the violation.
- `Detection handles`: red-flag or banned-shape labels that map to the policy.
- `Related remediation`: the fixer-side remediation code, loaded only from
  `remediations.md` after triage.

## Category Index

- **Runtime, Config, and State**: `POLICY.RUNTIME_DEFAULT`, `POLICY.TOTAL_CORE_STATE`, `POLICY.NO_HIDDEN_CONFIG`, `POLICY.NO_AMBIENT_DISCOVERY`, `POLICY.NO_DEFENSIVE_HOTPATH`
- **Fail-Loud Execution**: `POLICY.FAIL_OPEN`, `POLICY.CRITICAL_DEPENDENCY`, `POLICY.NO_PARTIAL_SUCCESS`, `POLICY.NO_ERROR_DISCARD`
- **Proof and Test Integrity**: `POLICY.NO_SMOKE_PROOF`, `POLICY.NO_MOCK_PROOF`, `POLICY.NO_SKIP_MASK`, `POLICY.NO_HELPER_PROOF`, `POLICY.NO_EXACT_STRING_PROOF`
- **Type and Interface Integrity**: `POLICY.NO_BOOLEAN_MODE`, `POLICY.NO_TYPE_ESCAPE`, `POLICY.NO_UNTYPED_IMPORT_LEAK`
- **QC Authority**: `POLICY.NO_QC_SILENCING`, `POLICY.GLOBAL_QC_AUTHORITY`
- **Artifact Ownership**: `POLICY.NO_DYNAMIC_ARTIFACTS`
- **Migration and Remediation Integrity**: `POLICY.NO_LEGACY_SHIM`, `POLICY.NO_QUARANTINE_REMEDIATION`, `POLICY.NO_ADMIN_COMPLETION`, `POLICY.NO_DELETION_LAUNDERING`
- **Anti-Speculation**: `POLICY.NO_HYPOTHETICAL_PATH`

## Policy Records

### Runtime, Config, and State

#### `POLICY.RUNTIME_DEFAULT` — No defaults in runtime logic

Category: Runtime, Config, and State

Rule: Runtime values must be supplied explicitly and validated at the owned boundary. Config, env, CLI, schema, serde, Pydantic, dict, and option defaults are banned when they let missing data become success-shaped execution.

Invalid local fixes: Replacing one default syntax with another; moving the default to a constant; adding a comment that the default is harmless.

Detection handles: `RUNTIME-DEFAULTS`, `DEFAULTS-OPTIONALITY`, `RUNTIME-DEFAULTS-FALLBACKS`, `CONFIG-DEFAULTING`, `NULLISH-DEFAULT`, `UNWRAP-OR`, `CONFIG-SCHEMA`

Related remediation: `REMEDIATE.TOTAL_CONFIG_MODEL`

#### `POLICY.TOTAL_CORE_STATE` — No optional core state

Category: Runtime, Config, and State

Rule: Normalize required state once at the boundary. Inside owned core logic, required data is total and non-optional.

Invalid local fixes: Sprinkling null checks; using `Optional`, `Partial`, `Any`, sentinel fields, or "maybe initialized" state in core paths.

Detection handles: `OPTIONAL-STATE`, `OPTIONAL-UI-FAILOPEN`, `OPTION-CORE-STATE`, `IFLET-INITIALIZED`, `NESTED-IF-CHAIN`

Related remediation: `REMEDIATE.TOTAL_CONFIG_MODEL`

#### `POLICY.NO_HIDDEN_CONFIG` — No hidden behavioral config in code

Category: Runtime, Config, and State

Rule: Behavioral parameters, thresholds, paths, provider choices, retries, feature flags, and policy decisions belong in the declared config surface as required values.

Invalid local fixes: Moving to `constants.*`; using `const`/`static`/top-level literals; calling it a true invariant without applying the invariant test.

Detection handles: `GLOBAL-STATE`, `CONFIG-SCHEMA`, `IMPLICIT-STATE`

Related remediation: `REMEDIATE.TOTAL_CONFIG_MODEL`

#### `POLICY.NO_AMBIENT_DISCOVERY` — No ambient discovery as source of truth

Category: Runtime, Config, and State

Rule: Behavior must not be inferred from installed tools, current directory, shell profiles, caches, home-directory artifacts, or multi-location search chains unless that is the explicit product contract.

Invalid local fixes: Env-then-config-then-default chains; installed-tool probing; local snooping; "works because it found something else".

Detection handles: `AMBIENT-DISCOVERY`, `GLOBAL-STATE`, `SILENT-PROBING`, `command -v`

Related remediation: `REMEDIATE.FAIL_LOUD_BOUNDARY`

#### `POLICY.NO_DEFENSIVE_HOTPATH` — No defensive validation inside trusted hot paths

Category: Runtime, Config, and State

Rule: Validate once at the owned boundary, then use total types internally. Core code should not repeatedly defend against impossible malformed state.

Invalid local fixes: Every function checking null/missing/impossible variants; tests for impossible branches; defensive guards in trusted core paths.

Detection handles: `DEFENSIVE-GUARDS`, `DEFENSIVE-EXCESS`, `IF-REQUIRED-INVARIANT`

Related remediation: `REMEDIATE.FAIL_LOUD_BOUNDARY`

### Fail-Loud Execution

#### `POLICY.FAIL_OPEN` — No fallbacks

Category: Fail-Loud Execution

Rule: Required work fails loudly. Do not continue with substitute data, empty collections, placeholder output, cached guesses, "best effort", or alternate branches that preserve a success signal after the obligation failed.

Invalid local fixes: Catching and logging; returning `None`, `[]`, `{}`, `false`, or a placeholder; adding another fallback layer.

Detection handles: `FALLBACK-CHAINS`, `FAIL-OPEN-BAN`, `LAUNDER-EMPTY-LIST`, `EMPTY-ARRAY-FAILED`, `VECTOR-LAUNDERING`, `FALSEY-RESULT`, `EMPTY-OUTPUT-FAILURE`, `STATUS-LAUNDERING`

Related remediation: `REMEDIATE.FAIL_LOUD_BOUNDARY`

#### `POLICY.CRITICAL_DEPENDENCY` — No optional critical dependencies

Category: Fail-Loud Execution

Rule: A dependency, binary, service, model, config file, or generated artifact required for the operation is mandatory. Its absence is a setup error, not a branch in product logic.

Invalid local fixes: `try import`; `command -v` fallback; "skip if missing"; vendoring a weaker substitute.

Detection handles: `OPTIONAL-DEPS`, `TRY-IMPORT`, `FALLBACK-HEDGE`

Related remediation: `REMEDIATE.FAIL_LOUD_BOUNDARY`

#### `POLICY.NO_PARTIAL_SUCCESS` — No partial success

Category: Fail-Loud Execution

Rule: Owned operations either complete the claimed operation or fail with a hard error. Do not return success-shaped results with warnings, missing fields, skipped substeps, or hidden data loss.

Invalid local fixes: Returning `ok: true` with warnings; empty arrays on error; rendering with missing pieces; best-effort modes.

Detection handles: `PARTIAL-SUCCESS`, `PARTIAL-RESULT`, `WARNING-CONTINUE`

Related remediation: `REMEDIATE.FAIL_LOUD_BOUNDARY`

#### `POLICY.NO_ERROR_DISCARD` — No swallowed errors

Category: Fail-Loud Execution

Rule: Errors and failed results must be propagated, handled immediately as a real domain alternative, or converted into structured failure. They must not be discarded.

Invalid local fixes: `.ok()`, `let _ =`, `filter_map(Result::ok)`, `except: pass`, `catch(() => default)`, `|| true`, stderr suppression.

Detection handles: `SWALLOWED-ERRORS`, `OK-DISCARD`, `SUPPRESSION-FALLBACK`, `PIPE-TRUE`, `NO_ERROR_DISCARD`

Related remediation: `REMEDIATE.FAIL_LOUD_BOUNDARY`

### Proof and Test Integrity

#### `POLICY.NO_SMOKE_PROOF` — No proof-free smoke paths

Category: Proof and Test Integrity

Rule: Tests and QC paths must prove owned behavior through real boundaries. Smoke, diagnostic, import, constructor, coverage-only, no-crash, and status-only checks carry no proof burden.

Invalid local fixes: Renaming a fake test to smoke; keeping non-proof checks in proof paths; citing coverage as correctness.

Detection handles: `NON-PROOF-TESTS`, `SMOKE-TEST`, `LA-NO-THROW`, `LA-IMPORT`, `NO-CRASH-PROOF`

Related remediation: `REMEDIATE.REAL_PROOF_LOOP`

#### `POLICY.NO_MOCK_PROOF` — No mocks as proof

Category: Proof and Test Integrity

Rule: Mocks, fakes, stubs, spies, monkeypatching, synthetic providers, and mocked IPC do not prove owned behavior when real boundaries are available.

Invalid local fixes: Asserting a mock was called; swapping one mock framework for another; labeling a mocked test as non-proof while leaving it in QC.

Detection handles: `MOCK-STUB`, `MOCK-TEST-POISON`, `MOCKED-IPC`, `TS-MOCKED-BOUNDARY`, `MOCK-AS-PROOF`

Related remediation: `REMEDIATE.REAL_PROOF_LOOP`

#### `POLICY.NO_SKIP_MASK` — No skipped or masked tests

Category: Proof and Test Integrity

Rule: `skip`, `xfail`, `todo`, `only`, ignored tests, conditional test gating, and hidden test exclusions mask runtime reality and are not acceptable proof surfaces.

Invalid local fixes: Moving the skip; adding a reason string; filing an issue while leaving the proof gap masked.

Detection handles: `TEST-GATING`, `NO MASKING`

Related remediation: `REMEDIATE.REAL_PROOF_LOOP`

#### `POLICY.NO_HELPER_PROOF` — No helper-level proof for boundary obligations

Category: Proof and Test Integrity

Rule: A finding about startup, config, persistence, IPC, subprocess, API, or UI behavior must be proved at that boundary. Helper tests are supplementary and cannot resolve boundary feedback.

Invalid local fixes: Extracting a helper after review; testing branch behavior instead of product behavior; proving code the app may stop calling.

Detection handles: `HELPER-BOUNDARY`, `HELPER-PATCH`, `STOPPED-HELPER`, `HELPER-BRANCH-PROOF`, `PY-HELPER-BRANCH`, `BOUNDARY-BYPASS`

Related remediation: `REMEDIATE.REAL_PROOF_LOOP`

#### `POLICY.NO_EXACT_STRING_PROOF` — No exact string assertions unless public contract

Category: Proof and Test Integrity

Rule: Tests assert structured error kinds, semantic values, or public text contracts. Exact string assertions on internal diagnostics usually prove only the test's copied literal.

Invalid local fixes: Asserting copied error messages; matching implementation wording; replacing string errors with different strings.

Detection handles: `EXACT-STRING`, `TEST-EXACT-STRING`, `STRINGLY-ERRORS`, `LA-STRING`, `PY-STRINGS`, `TS-STRINGS`, `RS-STRING-ERRORS`

Related remediation: `REMEDIATE.REAL_PROOF_LOOP`

### Type and Interface Integrity

#### `POLICY.NO_BOOLEAN_MODE` — No boolean mode flags in owned APIs

Category: Type and Interface Integrity

Rule: Boolean parameters that select behavior hide multiple operations behind one call surface. Use separate functions or an explicit domain variant with exhaustive dispatch.

Invalid local fixes: Renaming `flag` to `mode`; replacing `bool` with an enum without splitting obligations; testing both branches directly instead of constructing real state.

Detection handles: `BOOLEAN-FLAGS`, `BOOLEAN-MODE`, `LA-BOOLEAN-FORCING`, `RS-BOOLEAN-FORCING`

Related remediation: `REMEDIATE.API_SPLIT_OR_VARIANT`

#### `POLICY.NO_TYPE_ESCAPE` — No type-system escape hatches

Category: Type and Interface Integrity

Rule: Owned code must not bypass static guarantees with `Any`, casts, double casts, `as any`, `unknown as`, broad `Partial`, stringly errors, or untyped blobs for structured state.

Invalid local fixes: Adding a narrower cast without proving the boundary; asserting type shape in tests; hiding data in JSON/dicts.

Detection handles: `TYPE-PROOF-ESCAPE`, `TYPE-ESCAPE`, `TSAnyKeyword`, `Any`, `Partial<T>`

Related remediation: `REMEDIATE.STRUCTURED_TYPES`

#### `POLICY.NO_UNTYPED_IMPORT_LEAK` — No untyped dependency leakage

Category: Type and Interface Integrity

Rule: Untyped third-party libraries may not leak `Any` into owned code. A mypy `import-untyped` diagnostic means the dependency boundary lacks stubs or a `py.typed` marker; owned code must restore a typed boundary before using that library broadly.

Invalid local fixes: Replacing the library solely to satisfy mypy; hand-rolling library behavior; adding `ignore_missing_imports`; adding `# type: ignore[import-untyped]`; casting imported values to expected types; exposing untyped library objects from a wrapper; adding local QC config or excludes.

Detection handles: `UNTYPED-IMPORT`, `IMPORT-UNTYPED`, `MISSING-STUBS`, `MISSING-PY-TYPED`, `ANY-INGRESS`, `TYPE-FIREWALL`

Related remediation: `REMEDIATE.TYPED_DEPENDENCY_BOUNDARY`

### QC Authority

#### `POLICY.NO_QC_SILENCING` — No validator bypass

Category: QC Authority

Rule: Suppression comments, allow attributes, ignore globs, disabled rules, lowered thresholds, local QC overrides, and broad excludes convert validator failure into validator silence.

Invalid local fixes: Narrowing the suppression while keeping the violation; adding post-hoc prose; weakening the rule or threshold.

Detection handles: `BYPASS-COMMENTS`, `ATTRIBUTE-BYPASSES`, `CONFIG-QC`, `VALIDATOR-BYPASS`

Related remediation: `REMEDIATE.REMOVE_SUPPRESSION_WITH_EXCEPTION_PROTOCOL`

#### `POLICY.GLOBAL_QC_AUTHORITY` — No local QC authority

Category: QC Authority

Rule: Generic lint, type, format, coverage, dead-code, duplication, slop, and tool-config behavior belong to global QC. Repos delegate; they do not reimplement or override.

Invalid local fixes: Adding local `lint`/`typecheck` recipes; copying global configs downstream; running narrower local checks as proof.

Detection handles: `LOCAL-QC`, `QC-TARGETS`

Related remediation: `REMEDIATE.DELEGATE_GLOBAL_QC`

### Artifact Ownership

#### `POLICY.NO_DYNAMIC_ARTIFACTS` — No owned static artifacts generated from code

Category: Artifact Ownership

Rule: Configs, prompts, scripts, static data, and templates owned by the project must be tracked reviewable artifacts, not strings or dicts emitted from runtime code.

Invalid local fixes: Heredocs; embedded cross-language code; inline prompt strings; generated config assembled from literals.

Detection handles: `DYNAMIC-FILE`, `INLINE-STRINGS-DATA`, `CODE-IN-CODE`, `DYNAMIC-FILE-CREATION`, `INLINE-STRINGS`, `CODE-WITHIN-CODE`

Related remediation: `REMEDIATE.TRACK_STATIC_ARTIFACT`

### Migration and Remediation Integrity

#### `POLICY.NO_LEGACY_SHIM` — No compatibility shims in pre-launch bespoke software

Category: Migration and Remediation Integrity

Rule: Replace wrong paths, migrate callers, and remove old interfaces after transferring their burden. Do not preserve legacy branches without external consumers.

Invalid local fixes: Deprecated wrappers; compat mode; old parser retained "just in case"; feature flags for obsolete paths.

Detection handles: `LEGACY-SHIMS`, `LEGACY-SHIM`

Related remediation: `REMEDIATE.REPLACE_LEGACY_PATH`

#### `POLICY.NO_QUARANTINE_REMEDIATION` — No quarantine as remediation

Category: Migration and Remediation Integrity

Rule: Quarantine labels such as smoke, non-proof, legacy, diagnostic-only, temporary, compatibility, fallback, scaffold, or out-of-scope require burden disposition. They do not make slop acceptable.

Invalid local fixes: Keeping proof-shaped artifacts under disclaimer labels; moving slop to "future-owned"; renaming rather than resolving burden.

Detection handles: `QUARANTINE-LANG`, `ADMIN-ARTIFACT`

Related remediation: `REMEDIATE.BURDEN_DISPOSITION`

#### `POLICY.NO_ADMIN_COMPLETION` — No administrative artifact as completion

Category: Migration and Remediation Integrity

Rule: Issues, comments, docs, labels, review replies, and status fields can preserve truth but do not satisfy implementation or proof obligations.

Invalid local fixes: Marking as future work; documenting a limitation; closing a thread without code/proof; resolving by metadata.

Detection handles: `ADMIN-COMPLETION`, `ADMIN-ARTIFACT`

Related remediation: `REMEDIATE.BURDEN_DISPOSITION`

#### `POLICY.NO_DELETION_LAUNDERING` — No deletion or relabeling without burden disposition

Category: Migration and Remediation Integrity

Rule: Slop artifacts are forensic evidence of an unmet need. Removing or renaming them is valid only after the original burden is solved, invalidated, transferred, or recorded unresolved.

Invalid local fixes: Deleting the evidence; renaming to smoke/basic/legacy; "cleaning up" without reconstructing intent.

Detection handles: `DELETION-BURDEN`, `DELETION-LAUNDERING`

Related remediation: `REMEDIATE.BURDEN_DISPOSITION`

### Anti-Speculation

#### `POLICY.NO_HYPOTHETICAL_PATH` — No hypothetical failure-path code

Category: Anti-Speculation

Rule: Do not add branches for failure modes that have not been observed, tested, or reported. Assert invariants now; handle real incidents when they exist.

Invalid local fixes: "What if" guards; speculative fallback code; enterprise deployment branches for bespoke local tools.

Detection handles: `HYPOTHETICAL-PATH`, `NO-PREEMPTIVE-PATH`, `UNOBSERVED-FAILURE`

Related remediation: `REMEDIATE.OBSERVE_BEFORE_BRANCHING`
