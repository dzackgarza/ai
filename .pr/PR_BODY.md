## Intended result

The installed skill tree has one progressively disclosed PR-feedback workflow. The
canonical state machine lives in
[dzackgarza/ai-review-ci#272](https://github.com/dzackgarza/ai-review-ci/pull/272);
this repository installs it by symlink, routes Git and review guidance to it, and keeps
the OpenCode workflow as a thin A/B/C harness adapter.

## Scope

- Included: PR-feedback routing in AGENTS fragments and Git leaves; removal of the
  duplicate local feedback skill and tracked disposition ledger; the thin OpenCode
  adapter; installed-skill path/frontmatter normalization; WikiLink traversal; official
  skill validation and Lychee checks in the repository test recipe.
- Excluded: the upstream canonical state-machine implementation, which is claimed by
  dzackgarza/ai-review-ci#272; the unperformed evaluation and calibration work in #14,
  #15, and #20.

## GitHub tracking

- Target work unit: Closes #39.
- Milestone: Agent Orchestration & Evaluation Research.
- Dependency: [dzackgarza/ai-review-ci#272](https://github.com/dzackgarza/ai-review-ci/pull/272).
- References only: #14, #15, and #20.

## Claim map

- [x] **One feedback owner**
  - Git and review entrypoints route to pr-feedback-triage instead of restating its
    collection, disposition, remediation, reply, resolution, or convergence rules.
  - The originating GitHub thread or comment surface is the canonical audit trail.
- [x] **Thin harness adapter**
  - A owns state and evidence, B independently dispositions stable findings, and C
    receives only a first-principles specification plus exact policy/style routing.
  - The adapter cannot create a top-level ledger or tracked review-log artifact.
- [x] **Auditable installed skill tree**
  - Installed directory names match skill frontmatter names.
  - Cross-skill traversal uses WikiLinks, including routed Git leaves.
  - The repository test recipe runs the official Agent Skills validator and Lychee.
- [x] **Post-dependency proof**
  - A temporary assembly pointing the installed pr-feedback-triage and style-guide
    symlinks at the upstream PR worktree validates 179 installed skills.
  - Lychee checks 1,291 links (317 unique): 1,050 accepted, 241 excluded, 0 errors.
  - node --check opencode/workflows/pr-feedback-triage.js succeeds.
- [x] **Installation dependency before ready-for-review**
  - Upstream #272 is merged and the installed ~/ai-review-ci checkout is updated to
    c688812, so this branch's real pre-push gate exercises the assembled tree.
