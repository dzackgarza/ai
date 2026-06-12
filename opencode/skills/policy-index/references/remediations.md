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
| `REMEDIATE.REMOVE_SUPPRESSION_WITH_EXCEPTION_PROTOCOL` | `POLICY.NO_QC_SILENCING` | Remove the suppression and fix the underlying invariant. If a validator is wrong, stop for explicit policy exception approval with policy code, justification, replacement invariant, boundary proof, and audit trail. |
| `REMEDIATE.DELEGATE_GLOBAL_QC` | `POLICY.GLOBAL_QC_AUTHORITY` | Route public `test` and `test-ci` through `~/ai-review-ci/justfiles/<language>.just`. Keep project-specific semantic checks private and composed after the global gate. |
| `REMEDIATE.TRACK_STATIC_ARTIFACT` | `POLICY.NO_DYNAMIC_ARTIFACTS` | Move owned prompts, scripts, configs, templates, and static data into tracked files. Runtime code loads the reviewed artifact rather than constructing it from inline strings. |
| `REMEDIATE.REPLACE_LEGACY_PATH` | `POLICY.NO_LEGACY_SHIM` | Migrate all callers to the new path, prove the migrated behavior, then remove the obsolete interface with burden disposition. |
| `REMEDIATE.OBSERVE_BEFORE_BRANCHING` | `POLICY.NO_HYPOTHETICAL_PATH` | Do not add code. Preserve the invariant as an assertion or fail-loud boundary. Add a branch only after a real observed incident establishes the domain case. |
| `REMEDIATE.BURDEN_DISPOSITION` | `POLICY.NO_QUARANTINE_REMEDIATION`, `POLICY.NO_ADMIN_COMPLETION`, `POLICY.NO_DELETION_LAUNDERING` | Reconstruct the original obligation, then mark it solved, invalidated, transferred to a real proof surface, or recorded unresolved. Do not treat labels, docs, deletion, or comments as resolution. |
| `REMEDIATE.BLAST_RADIUS_REPAIR` | Any slop finding | Inspect the owning boundary, adjacent call sites, tests, config surface, and history for the same failure process. Fix the full damaged obligation, not only the matched token. |

## Assignment Rule

The fixer receives the policy code from triage and chooses the remediation code in this
file. The detector and issue-seeing reviewer must not prescribe the remediation code.

If more than one remediation applies, choose the one that restores the original
obligation at the widest real boundary. Do not pick the smallest local edit.
