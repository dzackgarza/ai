## Intended result

Repositories governed by an `itree` issue tree use the published `itree new` command with
an explicit parent when creating work units. The future `itree milestone` route is not
presented as current behavior before `dzackgarza/itree#22` ships an immutable release and
its real GitHub boundary proof is available.

## Scope

- Included: `AGENTSmd/git-guidelines/issues.md`, its assembled `AGENTS.md`, and
  `opencode/skills/git-guidelines/{SKILL.md,issues.md,creating-prs.md,pr-workflow.md}`.
- Excluded: ai #31, `dzackgarza/itree` implementation, `ai-review-ci`, wrappers,
  compatibility routes, queues, sidecars, and unrelated Git/PR doctrine.

## GitHub tracking

- Target work unit: Refs #36.
- Milestone: `Agent Orchestration & Evaluation Research`.
- References only:
  - Refs #18
  - Refs dzackgarza/itree#22

## Claim map

- [x] **Current published command guidance**
  - `itree new --under` remains the current governed work-unit creation route.
  - Omitted `--under` is documented as non-mutating placement guidance.
  - Existing structural commands use their published syntax, including
    `itree detach PARENT CHILD`.
- [x] **Source and assembled guidance consistency**
  - The AGENTSmd source and generated `AGENTS.md` expose the same current/future command
    boundary.
  - Ledger body files and returned-ledger placeholders use
    `MILESTONE_LEDGER.md` and `MILESTONE_LEDGER_NUMBER` consistently.
- [ ] **#36 future milestone-and-ledger behavior**
  - `dzackgarza/itree#22` must ship a released immutable command commit.
  - Record that commit, reread released `itree milestone --help`, and prove the real
    GitHub boundary before marking this behavior complete or closing #36.

## Evidence

- The published CLI help currently exposes `new`, `attach`, `move`, and `detach`; it does
  not expose `milestone`.
- #22 defines the future milestone command and its live-boundary proof obligations; its
  implementation PR #23 remains draft with an empty checkpoint commit.
- This PR remains draft and references #36 rather than closing it.
