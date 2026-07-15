---
name: github-issues
description: Create, triage, label, assign GitHub issues via gh, itree, or REST.
license: MIT
metadata:
  hermes:
    tags:
    - GitHub
    - Issues
    - Project-Management
    - Bug-Tracking
    - Triage
    related_skills:
    - '[[git-guidelines/SKILL|git-guidelines]]'
  version: 2.0.0
  author: Hermes Agent
---

# GitHub Issues

Load [[git-guidelines/git-operational-policy/SKILL|the Git operational baseline]].
This leaf owns issue admission, governance, and writing policy.
Use [[git-guidelines/issues|the issue mechanics reference]] for viewing, editing, triage, sub-issues, dependencies, and raw API commands.

## Owned repository improvement loop

For repositories owned by this system, an observed defect should not remain only in chat or memory.
Before handoff, either fix it in the current coherent work unit, file an evidence-backed issue on the owning repository, or ask when ownership is ambiguous.
Do not file speculative bugs or vague dissatisfaction.

## Filing issues

Label every issue immediately after creation.
Before creating public execution state, classify the repository:

- If the repository has an `itree` root or assigns execution state to `itree`, use the governed route.
- Absence of a root is not permission to bypass governance; initialize or repair the tree first.
- Use raw `gh` or REST creation only when the repository is explicitly outside `itree` governance.

For a governed repository without a root:

```bash
uvx --from git+https://github.com/dzackgarza/itree itree init <owner>/<repo> "<root title>"
gh issue edit <new-root-issue-number> --repo <owner>/<repo> --add-label "<label>"
uvx --from git+https://github.com/dzackgarza/itree itree doctor <owner>/<repo>
```

When doctor reports a diagnostic, read its exact route:

```bash
uvx --from git+https://github.com/dzackgarza/itree itree doctor <owner>/<repo> --explain <CODE>
```

When that route identifies an orphan, run `itree triage <owner>/<repo>`, execute one supported absorb, attach, or close choice, then repeat triage and doctor until the tree is coherent.

Create a governed work unit beneath an explicit grouping parent:

```bash
uvx --from git+https://github.com/dzackgarza/itree \
  itree new <owner>/<repo> "<title>" \
  --under <owner>/<repo>#<grouping-issue> \
  --body-file issue.md
gh issue edit <new-issue-number> --repo <owner>/<repo> --add-label "<label>"
```

`itree new` without `--under` is a non-mutating placement inquiry.
It creates nothing, prints existing work units and grouping targets plus exact placement commands, and exits nonzero.

For an explicitly non-governed repository:

```bash
gh issue create --repo <owner>/<repo> --title "..." --body-file issue.md --label "<label>"
```

Roadmap, feature, PRD, proof-bearing, and cross-agent issues first route through [[plan/references/externalization|plan externalization]].
Use native sub-issues for hierarchy, dependencies only for blockers, and the GitHub Milestone for the delivery slice.

## Released milestone-and-ledger route

`itree milestone` is released in [v0.1.0](https://github.com/dzackgarza/itree/releases/tag/v0.1.0).
The annotated tag resolves to `777ef91d9c290a819847db36e878ee6a35b9e528`, and its [release workflow](https://github.com/dzackgarza/itree/actions/runs/29152942172) completed successfully with source and wheel artifacts.

Pin that release when creating a governed milestone and ledger:

```bash
uvx --from git+https://github.com/dzackgarza/itree@v0.1.0 \
  itree milestone <owner>/<repo> "<milestone>" \
  --under <owner>/<repo>#<grouping-issue> \
  --body-file .pr/MILESTONE_LEDGER.md \
  --issues <owner>/<repo>#<work-unit> ...
gh issue edit <MILESTONE_LEDGER_NUMBER> --repo <owner>/<repo> --add-label "<label>"
```

The command performs one complete preflight before ordered remote writes.
Omitting `--under` creates nothing and prints placement guidance.
A rejected or indeterminate write stops the untouched suffix without rollback; reread live GitHub and `itree` state before recovery.
Do not replace this governed command with a manual write sequence.

## Issue writing contract

Every issue must provide:

1. A deep technical description of what is happening or missing.
2. Evidence such as logs, error traces, source facts, or concrete examples.
3. Concrete expected behavior, including TDD-style pseudocode when behavior is involved.
4. Plain informative language without marketing.
5. No implementation code that pre-decides the fix.
6. No step-by-step implementation plan; optional high-level phases are allowed.
7. No time estimates.

Use this body shape:

```markdown
# Description

<Deep description of the observed problem or requested capability.>

# Evidence

<Logs, outputs, source facts, and examples.>

# Expected Behavior

<Concrete contract and TDD-style pseudocode.>

# Suggested Phases (Optional)

<High-level phases only.>
```

Use `bug` for observed incorrect behavior, `enhancement` for improvements or design requests, and `documentation` for documentation work.
