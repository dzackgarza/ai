## Intended result

Repositories governed by an `itree` issue tree use the published `itree new` command with
an explicit parent when creating work units. Although `dzackgarza/itree#22` is closed and
its implementation PR is merged, the `itree milestone` route is not presented as current
behavior before an immutable release and its real GitHub boundary proof are available.

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
  - Evidence required: an immutable release containing the #22 command, a reread of that
    release's `itree milestone --help`, and real GitHub-boundary proof.
  - Current evidence: #22 closed and #23 merged at `8044d0b`; the releases endpoint
    returns no immutable release, and #22's recorded live GitHub-boundary proof remains
    unchecked. This PR remains draft and references #36 rather than closing it.
