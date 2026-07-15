# Commit and PR Routing Playbook

Read this reference for commit gates, push-vs-PR routing, PR body requirements, CI,
review triage, and PR remediation.

## Commit Gate

Use `Commit Agent` mode only after traceability, scope audit, tests, and QC gates are
clean for the current change.
Load `git-guidelines` before staging or committing.

Do not commit if:

- tests fail;
- true-positive QC findings are unresolved;
- requirements traceability is broken;
- implementation diff audit failed;
- unapproved test edits exist;
- target files have unrelated uncommitted changes that are not part of the coherent
  change.

Commit messages are the canonical record.
Include:

- feature or fix summary;
- requirements covered;
- obligation IDs covered;
- test evidence;
- QC status;
- notable architecture decisions.

## Push or PR Routing

Use `Release Router` mode after commit.

Direct push may be allowed only for greenfield bootstrapping, trivial maintenance, or an
explicitly low-risk solo workflow permitted by repo policy.

Branch and PR are required for:

- significant features extending existing implementation;
- security-sensitive changes;
- architecture-changing changes;
- dependency-changing changes unless policy treats them as trivial;
- changes requiring independent review.

Branch names should be short and purpose-specific:

```text
feature/<short-feature-name>
fix/<short-bug-name>
refactor/<short-scope>
qc/<policy-or-review-fix>
```

## PR Body

Use `PR Manager` mode to open a PR with enough context for independent review.

Include:

```markdown
## Intended result
Externally observable project or user result.

## GitHub tracking
- Target issue set / subtree:
- Milestone:
- Closes on merge:
- References only:

## User-facing requirements
REQ IDs and short descriptions.

## Proof claims
- Claimed obligations:
- Partially claimed obligations:
- Explicitly not claimed:

## Scope
Included and excluded MVP or feature scope.

## Implementation plan
Stacked work, parallel work, and integration point.

## Architecture
Chosen route, key dependencies, owned-surface reductions.

## Evidence
Tests, CI, screenshots, logs, artifacts, and review evidence mapped to each obligation.

## QC
Local and global QC status.

## Risk
Threat model, data risks, migration risks, dependency risks.

## Deferred work
Explicit non-MVP items and linked follow-up issues.
```

Gate:

- required CI passes;
- global AI QC findings are triaged;
- true positives are remediated;
- false positives are answered or upstreamed;
- PR guidance is satisfied.

For build or release artifacts, preserve enough provenance to identify the source,
dependencies, and build process that produced the artifact.
If citing SLSA levels or controls, verify the current upstream SLSA documentation first.

## PR Review Triage

Use `PR Finding Triage Reviewer` mode for every PR comment, review thread, automated
review summary, and check annotation.
Load [[pr-feedback-triage/SKILL|pr-feedback-triage]], [[git-guidelines/SKILL|git-guidelines]], [[test-guidelines/SKILL|test-guidelines]], and relevant policy references.

Classify each finding:

- valid policy violation;
- valid improvement requiring a separate requirement or PR route;
- false positive;
- threat-model-inapplicable;
- duplicate;
- requires human/product decision.

For every finding, separate the claim from the suggested remediation.
A true claim does not make the proposed fix acceptable.
A bad proposed fix does not make the underlying claim false.

False-positive responses must cite:

- local threat model;
- global policy;
- requirement or obligation IDs;
- owned-surface ledger entry;
- why the finding does not apply;
- whether an upstream QC issue was filed.

## PR Remediation

Use `PR Remediation Agent` mode after triage accepts a finding.
The remediation agent:

- fixes the issue;
- adds or updates proof only when a real proof burden exists;
- preserves green state;
- does not expand bespoke code without rerouting;
- updates artifact references;
- pushes to the same branch.

Do not resolve or hide feedback without a visible disposition note anchored to evidence.
