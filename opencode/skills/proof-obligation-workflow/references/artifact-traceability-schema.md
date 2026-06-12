# Artifact and Traceability Schema

Read this reference when creating the workflow artifact tree, assigning stable IDs,
checking traceability, or representing workflow state.

## Default Layout

Use the repository's existing convention.
If no convention exists, use:

```text
.agents/proof-obligation-workflow/
  requirements/
    requirements-dossier.md
    domain-glossary.md
    canonical-scenarios.yaml
  obligations/
    abstract-proof-obligations.yaml
    implementation-specific-obligations.yaml
  planning/
    mvp-viability-plan.md
    implementation-plan.md
    standard-app-surface-checklist.yaml
    drift-risk-register.md
    plan-minimization-review.md
  architecture/
    owned-surface-ledger.yaml
    dependency-survey.md
    similar-project-survey.md
    ADR-0001.md
  testing/
    test-plan.yaml
    test-adequacy-report.md
  qc/
    implementation-diff-audit.md
    qc-local-report.json
    qc-global-report.json
    qc-triage.md
    remediation-report.md
    upstream-qc-issue.md
  pr/
    pr-review-triage.md
```

If a project already uses `.ai/` for this workflow, keep the existing path as the OSOT.
Do not maintain duplicate trees.

## Primary Artifacts

| Artifact | Purpose |
| --- | --- |
| `requirements-dossier.md` | User-facing requirements in nontechnical language. |
| `domain-glossary.md` | Domain terms as the user uses them. |
| `canonical-scenarios.yaml` | Concrete user workflows and unacceptable behaviors. |
| `abstract-proof-obligations.yaml` | Implementation-independent obligations. |
| `mvp-viability-plan.md` | Thin vertical slice proving product viability. |
| `standard-app-surface-checklist.yaml` | Baseline expected app behaviors. |
| `drift-risk-register.md` | Ways the MVP could game or drift from real requirements. |
| `owned-surface-ledger.yaml` | Locally owned versus delegated behavior. |
| `dependency-survey.md` | Libraries, tools, APIs, OS features, and forks considered. |
| `similar-project-survey.md` | Existing apps to fork, extend, script, or replace. |
| `ADR-*.md` | Accepted implementation route and rejected alternatives. |
| `implementation-plan.md` | Concrete modules, APIs, schemas, commands, and files. |
| `implementation-specific-obligations.yaml` | Architecture-specific obligations. |
| `test-plan.yaml` | Tests mapped to obligations. |
| `test-adequacy-report.md` | Independent review of test proof strength. |
| `implementation-diff-audit.md` | Check against plan and owned-surface budget. |
| `qc-local-report.json` | Deterministic local QC outputs. |
| `qc-global-report.json` | Independent global AI QC outputs. |
| `qc-triage.md` | Classification of all QC findings. |
| `upstream-qc-issue.md` | Systemic false-positive report for global QC. |
| `remediation-report.md` | True-positive remediation record. |
| `pr-review-triage.md` | PR comment and CI review disposition. |

Do not create all artifacts reflexively.
Create the artifacts required by the current state and the traceability edges needed for
the current task.

## Stable IDs

Use stable IDs for machine-checkable traceability:

```text
REQ-USER-001
AOB-001
IOB-001
TEST-001
ADR-001
RISK-001
QC-001
PR-001
```

Do not renumber IDs after deletion or deferral.
If an item is invalidated, mark its status and preserve the traceability record.

## Traceability Edges

Maintain these relations:

```text
REQ -> AOB
AOB -> MVP scenario or deferred scope
AOB -> IOB or dependency-contract evidence
IOB -> TEST or non-test evidence
TEST -> code behavior
code behavior -> owned-surface ledger entry
QC finding -> policy clause or requirement
remediation -> finding
commit -> requirements + obligations + tests
PR comment -> triage classification
```

Required consistency checks:

- every MVP requirement has at least one abstract obligation;
- every abstract obligation has a source;
- every MVP abstract obligation has implementation evidence, dependency-contract
  evidence, or explicit deferral;
- every implementation obligation has proof evidence or approved non-test evidence;
- every test maps to an implementation obligation or approved regression;
- every nontrivial code module maps to a plan component;
- every plan component maps to an owned-surface entry;
- every dependency maps to delegated behavior or infrastructure need;
- every QC suppression or rejection maps to a policy rationale;
- every deletion or quarantine has burden disposition.

## Machine State Schema

Represent workflow stages with this schema when an orchestrator needs machine-readable
state:

```yaml
state:
  id:
  name:
  agent:
  inputs:
  outputs:
  allowed_actions:
  forbidden_actions:
  entry_conditions:
  exit_conditions:
  failure_routes:
  artifacts_written:
  artifacts_read:
  independence_constraints:
```

Example:

```yaml
state:
  id: TEST_DESIGN
  name: Test Design
  agent: Test Designer
  inputs:
    - obligations/implementation-specific-obligations.yaml
    - planning/implementation-plan.md
    - architecture/owned-surface-ledger.yaml
  outputs:
    - testing/test-plan.yaml
    - test_files
  allowed_actions:
    - create proof-bearing tests
    - create representative fixtures
    - document coverage matrix
  forbidden_actions:
    - edit production code
    - weaken obligations
    - change architecture
  entry_conditions:
    - implementation obligations accepted
  exit_conditions:
    - every MVP implementation obligation has mapped evidence
    - plausible bad implementations are excluded
  failure_routes:
    - IMPLEMENTATION_SPECIFIC_OBLIGATIONS
    - CONCRETE_IMPLEMENTATION_PLANNING
```

## Role Roster

Use these role boundaries for nontrivial workflows:

| Role | Writes | Must not write |
| --- | --- | --- |
| Requirements Interviewer | raw interview notes | implementation plan |
| Requirements Normalizer | requirements dossier | tests or code |
| Abstract Obligation Writer | abstract obligations | concrete stack choices |
| MVP Planner | MVP plan | production code |
| Drift/Gaming Reviewer | drift register | production code |
| Architecture Minimizer | dependency/fork survey, owned-surface ledger | implementation |
| Architecture Arbiter | ADRs | tests or code |
| Concrete Planner | implementation plan | tests or code |
| Plan Minimization Adversary | minimization review | implementation |
| Implementation Obligation Writer | implementation-specific obligations | tests or code |
| Test Designer | tests and test plan | production code |
| Test Adequacy Auditor | adequacy report | production code |
| Implementation Agent | production code | tests or obligations |
| Scope Auditor | diff audit | production code |
| Local QC Runner | QC report | product decisions |
| Global QC Runner | global review output | remediation |
| QC Triage Reviewer | finding classifications | remediation code |
| Remediation Agent | fixes | test weakening |
| Commit Agent | commit | product reinterpretation |
| PR Manager | PR body | arbitrary code |
| PR Triage Reviewer | PR finding classifications | remediation code |
| PR Remediation Agent | PR fixes | test or policy weakening |
