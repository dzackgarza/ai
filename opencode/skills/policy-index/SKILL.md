---
name: policy-index
description: Use before code review, slop review, PR feedback triage, testing, QC changes, or remediation when deciding which global policy rule owns the obligation. Central source of truth for bridge-burning policy identity, red-flag catalogs, proof/test rules, QC authority, and slop remediation routing.
---

# Policy Index

Canonical source of truth for bridge-burning policy identity and policy-owned reference
catalogs.

Other skills may teach how to review, test, debug, or remediate within their domains.
They must not define competing bridge-burning policy text. They point here for policy
codes, red flags, runtime control-flow rules, banned test shapes, exception rules, and
remediation routing.

Remediation instructions are deliberately separated from detector instructions. The
agent that sees or classifies an issue must not see the preferred remediation, because
that couples detection to fixing and trains local appeasement. Remediation lives in
`references/remediations.md` and is loaded only by the remediation agent after triage
assigns a policy code.

## Use Protocol

- Load this skill before code review, slop review, PR feedback triage, test review, QC
  changes, or remediation.
- Use `POLICY.*` codes from this skill and `references/policies.md` as authoritative.
- Use `references/red-flags.md` to classify validation-evasion constructs.
- Use `references/runtime-control-flow.md` to classify runtime branch shapes.
- Use `references/test-proof-rules.md` to classify proof and assertion shapes.
- Do not remediate from the detector message alone.
- State the weakened obligation before editing.
- Use a separate reviewer/fixer context when QC triage requires it.
- If acting as the issue-seeing reviewer, do not open `references/remediations.md`.
- If acting as the remediation/fixer agent, open `references/remediations.md` only after
  receiving the policy code from triage.
- Treat local token replacement as invalid unless the remediation reference explicitly
  says the finding is mechanical.

## Database Files

| File | Audience | Contents |
| --- | --- | --- |
| `references/policies.md` | Reviewers, triage agents, fixers after code assignment | Categorized policy database with named `POLICY.*` records. |
| `references/red-flags.md` | Reviewers and detector authors | Validation-evasion red flags, language-specific signatures, and QC detector targets. |
| `references/runtime-control-flow.md` | Reviewers and detector authors | Runtime branch admission rules, banned branch shapes, assertion guidance, and examples. |
| `references/test-proof-rules.md` | Test writers, test reviewers, detector authors | Banned test/assertion shapes and proof-admission rules. |
| `references/remediations.md` | Fixers only after triage | Remediation registry and detailed restoration procedures keyed by policy/remediation code. |

## Policy Categories

- Runtime, Config, and State
- Fail-Loud Execution
- Proof and Test Integrity
- Type and Interface Integrity
- QC Authority
- Artifact Ownership
- Migration and Remediation Integrity
- Anti-Speculation

## Policy Registry

| Code | Name | Canonical rule | Invalid local fixes |
| --- | --- | --- | --- |
| `POLICY.RUNTIME_DEFAULT` | No defaults in runtime logic | Runtime values must be supplied explicitly and validated at the owned boundary. Config, env, CLI, schema, serde, Pydantic, dict, and option defaults are banned when they let missing data become success-shaped execution. | Replacing one default syntax with another; moving the default to a constant; adding a comment that the default is harmless. |
| `POLICY.FAIL_OPEN` | No fallbacks | Required work fails loudly. Do not continue with substitute data, empty collections, placeholder output, cached guesses, "best effort", or alternate branches that preserve a success signal after the obligation failed. | Catching and logging; returning `None`, `[]`, `{}`, `false`, or a placeholder; adding another fallback layer. |
| `POLICY.CRITICAL_DEPENDENCY` | No optional critical dependencies | A dependency, binary, service, model, config file, or generated artifact required for the operation is mandatory. Its absence is a setup error, not a branch in product logic. | `try import`; `command -v` fallback; "skip if missing"; vendoring a weaker substitute. |
| `POLICY.NO_PARTIAL_SUCCESS` | No partial success | Owned operations either complete the claimed operation or fail with a hard error. Do not return success-shaped results with warnings, missing fields, skipped substeps, or hidden data loss. | Returning `ok: true` with warnings; empty arrays on error; rendering with missing pieces; best-effort modes. |
| `POLICY.NO_SMOKE_PROOF` | No proof-free smoke paths | Tests and QC paths must prove owned behavior through real boundaries. Smoke, diagnostic, import, constructor, coverage-only, no-crash, and status-only checks carry no proof burden. | Renaming a fake test to smoke; keeping non-proof checks in proof paths; citing coverage as correctness. |
| `POLICY.NO_MOCK_PROOF` | No mocks as proof | Mocks, fakes, stubs, spies, monkeypatching, synthetic providers, and mocked IPC do not prove owned behavior when real boundaries are available. | Asserting a mock was called; swapping one mock framework for another; labeling a mocked test as non-proof while leaving it in QC. |
| `POLICY.NO_SKIP_MASK` | No skipped or masked tests | `skip`, `xfail`, `todo`, `only`, ignored tests, conditional test gating, and hidden test exclusions mask runtime reality and are not acceptable proof surfaces. | Moving the skip; adding a reason string; filing an issue while leaving the proof gap masked. |
| `POLICY.NO_HELPER_PROOF` | No helper-level proof for boundary obligations | A finding about startup, config, persistence, IPC, subprocess, API, or UI behavior must be proved at that boundary. Helper tests are supplementary and cannot resolve boundary feedback. | Extracting a helper after review; testing branch behavior instead of product behavior; proving code the app may stop calling. |
| `POLICY.NO_EXACT_STRING_PROOF` | No exact string assertions unless public contract | Tests assert structured error kinds, semantic values, or public text contracts. Exact string assertions on internal diagnostics usually prove only the test's copied literal. | Asserting copied error messages; matching implementation wording; replacing string errors with different strings. |
| `POLICY.NO_BOOLEAN_MODE` | No boolean mode flags in owned APIs | Boolean parameters that select behavior hide multiple operations behind one call surface. Use separate functions or an explicit domain variant with exhaustive dispatch. | Renaming `flag` to `mode`; replacing `bool` with an enum without splitting obligations; testing both branches directly instead of constructing real state. |
| `POLICY.TOTAL_CORE_STATE` | No optional core state | Normalize required state once at the boundary. Inside owned core logic, required data is total and non-optional. | Sprinkling null checks; using `Optional`, `Partial`, `Any`, sentinel fields, or "maybe initialized" state in core paths. |
| `POLICY.NO_TYPE_ESCAPE` | No type-system escape hatches | Owned code must not bypass static guarantees with `Any`, casts, double casts, `as any`, `unknown as`, broad `Partial`, stringly errors, or untyped blobs for structured state. | Adding a narrower cast without proving the boundary; asserting type shape in tests; hiding data in JSON/dicts. |
| `POLICY.NO_UNTYPED_IMPORT_LEAK` | No untyped dependency leakage | Untyped third-party libraries may not leak `Any` into owned code. Direct imports of untyped libraries belong behind stubs or a typed firewall module that returns project-owned typed values. | Replacing the library solely to satisfy mypy; adding `ignore_missing_imports`, `# type: ignore[import-untyped]`, casts, local QC excludes, or untyped wrapper pass-throughs. |
| `POLICY.NO_ERROR_DISCARD` | No swallowed errors | Errors and failed results must be propagated, handled immediately as a real domain alternative, or converted into structured failure. They must not be discarded. | `.ok()`, `let _ =`, `filter_map(Result::ok)`, `except: pass`, `catch(() => default)`, `\|\| true`, stderr suppression. |
| `POLICY.NO_QC_SILENCING` | No validator bypass | Suppression comments, allow attributes, ignore globs, disabled rules, lowered thresholds, local QC overrides, and broad excludes convert validator failure into validator silence. | Narrowing the suppression while keeping the violation; adding post-hoc prose; weakening the rule or threshold. |
| `POLICY.GLOBAL_QC_AUTHORITY` | No local QC authority | Generic lint, type, format, coverage, dead-code, duplication, slop, and tool-config behavior belong to global QC. Repos delegate; they do not reimplement or override. | Adding local `lint`/`typecheck` recipes; copying global configs downstream; running narrower local checks as proof. |
| `POLICY.NO_HIDDEN_CONFIG` | No hidden behavioral config in code | Behavioral parameters, thresholds, paths, provider choices, retries, feature flags, and policy decisions belong in the declared config surface as required values. | Moving to `constants.*`; using `const`/`static`/top-level literals; calling it a true invariant without applying the invariant test. |
| `POLICY.NO_AMBIENT_DISCOVERY` | No ambient discovery as source of truth | Behavior must not be inferred from installed tools, current directory, shell profiles, caches, home-directory artifacts, or multi-location search chains unless that is the explicit product contract. | Env-then-config-then-default chains; installed-tool probing; local snooping; "works because it found something else". |
| `POLICY.NO_DYNAMIC_ARTIFACTS` | No owned static artifacts generated from code | Configs, prompts, scripts, static data, and templates owned by the project must be tracked reviewable artifacts, not strings or dicts emitted from runtime code. | Heredocs; embedded cross-language code; inline prompt strings; generated config assembled from literals. |
| `POLICY.NO_LEGACY_SHIM` | No compatibility shims in pre-launch bespoke software | Replace wrong paths, migrate callers, and remove old interfaces after transferring their burden. Do not preserve legacy branches without external consumers. | Deprecated wrappers; compat mode; old parser retained "just in case"; feature flags for obsolete paths. |
| `POLICY.NO_DEFENSIVE_HOTPATH` | No defensive validation inside trusted hot paths | Validate once at the owned boundary, then use total types internally. Core code should not repeatedly defend against impossible malformed state. | Every function checking null/missing/impossible variants; tests for impossible branches; defensive guards in trusted core paths. |
| `POLICY.NO_QUARANTINE_REMEDIATION` | No quarantine as remediation | Quarantine labels such as smoke, non-proof, legacy, diagnostic-only, temporary, compatibility, fallback, scaffold, or out-of-scope require burden disposition. They do not make slop acceptable. | Keeping proof-shaped artifacts under disclaimer labels; moving slop to "future-owned"; renaming rather than resolving burden. |
| `POLICY.NO_HYPOTHETICAL_PATH` | No hypothetical failure-path code | Do not add branches for failure modes that have not been observed, tested, or reported. Assert invariants now; handle real incidents when they exist. | "What if" guards; speculative fallback code; enterprise deployment branches for bespoke local tools. |
| `POLICY.NO_ADMIN_COMPLETION` | No administrative artifact as completion | Issues, comments, docs, labels, review replies, and status fields can preserve truth but do not satisfy implementation or proof obligations. | Marking as future work; documenting a limitation; closing a thread without code/proof; resolving by metadata. |
| `POLICY.NO_DELETION_LAUNDERING` | No deletion or relabeling without burden disposition | Slop artifacts are forensic evidence of an unmet need. Removing or renaming them is valid only after the original burden is solved, invalidated, transferred, or recorded unresolved. | Deleting the evidence; renaming to smoke/basic/legacy; "cleaning up" without reconstructing intent. |

## QC Finding Contract

Every global QC detector that represents a policy finding should carry these fields in
tool metadata when the tool supports metadata:

```yaml
qc_lane: blocker
qc_class: bridge_burning | sentinel | policy_drift
policy_code: POLICY.RUNTIME_DEFAULT
failure_mode: fail_open | proof_laundering | hidden_config | qc_silencing | weak_type
bounce_required: true
local_fix_forbidden: true
```

Detector messages should be short. They identify the code and forbid local patching.
They do not restate the full policy text.

## Exception Protocol

A policy exception requires all of:

- Explicit user request or source-backed product requirement.
- Exact `POLICY.*` code being violated.
- Explanation of why the blanket rule blocks required behavior.
- Replacement invariant that prevents the old evasion.
- Boundary proof.
- Visible audit trail in commit, PR, or issue.

## Policy Routing Index

| Question | Canonical source |
| --- | --- |
| What named policy applies? | `references/policies.md` and [Policy Registry](#policy-registry). |
| What code/test red flags should I scan for? | `references/red-flags.md`. |
| What runtime control-flow shapes are banned? | `references/runtime-control-flow.md`. |
| What test assertion patterns are banned? | `references/test-proof-rules.md`. |
| What codenamed remediation applies? | `references/remediations.md`, loaded only by the remediation/fixer agent after triage. |
| What policy applies to creating files dynamically from code? | `POLICY.NO_DYNAMIC_ARTIFACTS` in `references/policies.md`. |
| What policy applies to embedding large strings/prompts/messages inline in code? | `POLICY.NO_DYNAMIC_ARTIFACTS` in `references/policies.md`. |
| What policy applies to embedding one language inside another? | `POLICY.NO_DYNAMIC_ARTIFACTS` in `references/policies.md`. |
| What policy applies to mypy `import-untyped`, missing stubs, or missing `py.typed`? | `POLICY.NO_UNTYPED_IMPORT_LEAK`; remediation is `REMEDIATE.TYPED_DEPENDENCY_BOUNDARY`, not dependency churn. |
| How do I review LLM-produced code? | [reviewing-llm-code/SKILL.md](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/SKILL.md). |
| How do I fix slop without laundering? | [fixing-slop/SKILL.md](file:///home/dzack/ai/opencode/skills/fixing-slop/SKILL.md) plus fixer-only `references/remediations.md`. |
| What makes a test valid proof? | [test-guidelines/SKILL.md](file:///home/dzack/ai/opencode/skills/test-guidelines/SKILL.md) plus `references/test-proof-rules.md`. |
| Who owns QC invocation/config/tooling? | `POLICY.GLOBAL_QC_AUTHORITY`; operational QC invocation remains in the global `quality-control` skill. |
| How do I triage PR feedback? | [pr-feedback-triage/SKILL.md](file:///home/dzack/ai/opencode/skills/pr-feedback-triage/SKILL.md). |
| How do I debug without prior-shaped probing? | [reality-grounded-debugging](file:///home/dzack/ai/opencode/skills/reality-grounded-debugging/SKILL.md) + [systematic-debugging](file:///home/dzack/ai/opencode/skills/systematic-debugging/SKILL.md). |
| How do I handle external tool/library/compiler uncertainty? | [known-solution-first](file:///home/dzack/ai/opencode/skills/known-solution-first/SKILL.md). |
| How do I provision tools? | [tool-provisioning-and-environment-hygiene](file:///home/dzack/ai/opencode/skills/tool-provisioning-and-environment-hygiene/SKILL.md). |
