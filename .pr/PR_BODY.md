## Intended result

Repositories governed by an `itree` issue tree use the published `itree new` command with
an explicit parent when creating work units. Although `dzackgarza/itree#22` is closed and
its implementation PR is merged, the released `itree milestone` route is pinned to
`v0.1.0` for governed milestone-and-ledger creation.

## Scope

- Included: `AGENTSmd/git-guidelines/issues.md`, its assembled `AGENTS.md`, and
  `opencode/skills/git-guidelines/{SKILL.md,issues.md,creating-prs.md,pr-workflow.md}`.
- Excluded: ai #31, `dzackgarza/itree` implementation, `ai-review-ci`, wrappers,
  compatibility routes, queues, sidecars, and unrelated Git/PR doctrine.

## GitHub tracking

- Target work unit: Closes #36.
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
- [x] **#36 released milestone-and-ledger behavior**
  - Evidence: [v0.1.0](https://github.com/dzackgarza/itree/releases/tag/v0.1.0) is an
    annotated release tag resolving to `777ef91d9c290a819847db36e878ee6a35b9e528`; its
    [release workflow](https://github.com/dzackgarza/itree/actions/runs/29152942172)
    succeeded and attached the source archive and wheel.
  - Released boundary proof: `uvx --from git+https://github.com/dzackgarza/itree@v0.1.0
    itree milestone --help` succeeded, and `uvx --from
    git+https://github.com/dzackgarza/itree@v0.1.0 itree doctor dzackgarza/itree --json`
    returned `status: ok` with zero errors and warnings against live GitHub.
