# CI Review Runner

Opencode-powered review infrastructure for pull requests. Two review types:

- **General review** — structural code quality audit: architectural decay, dead code,
  test quality, dependency mismanagement, semantic regressions.
- **Slop review** — AI-generated-code audit: bridge-burning violations, runtime
  control-flow defects, test/text antipatterns, validation-evasion constructs,
  defaults/fallbacks/mocks/skips.

## File Inventory

### In this directory (`quality-control/ci/`)

| File | Purpose |
|------|---------|
| `general-review-opencode.yml` | CI workflow definition — general review |
| `slop-review-opencode.yml` | CI workflow definition — slop review |
| `submit-candidate` | Script the agent runs to validate + submit a report |
| `just-blocked.sh` | Static blocker — replaces `just` binary during agent runs |
| `justfile` | `install` recipe to deploy workflow YAMLs to another repo |
| `README.md` | This file |

### Outside this directory (`quality-control/`)

| File | Purpose |
|------|---------|
| `check-report.py` | Pydantic validator — dispatches to `GeneralReport` or `SlopReport` by `report_type` |
| `run-review.py` | Harness — feeds template to opencode, retries on timeout, collects artifact |
| `reviews/general/template.md` | Agent prompt for general review |
| `reviews/slop/template.md` | Agent prompt for slop review |

## How the Reporting Loop Works

```
CI workflow triggers on PR
  → Lockdown (see below)
  → run-review.py feeds template + skills to `opencode run`
  → opencode agent:
        1. Reads template.md for instruction set
        2. Writes report to .agents/review-runner/candidates/submitted.json
        3. Runs `submit-candidate --help` to learn schema + rejection rules
        4. Fixes report to match schema
        5. Runs `quality-control/ci/submit-candidate` (no arguments)
        6. If exit 0 → done. If non-zero → read error (has FIX: guidance) → fix same file → goto 5
  → submit-candidate calls `uv run check-report.py` (pydantic validation)
  → On validation pass: cp to .review-report-artifact.json,
    then runs `uv run render-review-comment.py` to produce .review-report-comment.md
  → On validation fail: print errors with FIX: guidance, exit 1
  → harness checks .review-report-artifact.json exists after opencode exits
      - exists → read .review-report-comment.md, extract score via regex
      - missing → append continuation prompt, loop
```

## Key invariants

- Agent writes to a **fixed path** — never passes filenames to `submit-candidate`.
  Always `.agents/review-runner/candidates/submitted.json`.
- `submit-candidate` takes **no arguments** (except `--help`). It reads the fixed path,
  validates, and either exits 0 (copied to artifact path) or non-zero (errors printed).
- Agent discovers the schema via `submit-candidate --help` — never reads CI infrastructure files.
- Harness does NOT re-validate. It only checks artifact file existence after opencode exits.
- **Everything is invisible to the agent** except: the template.md it receives, its own
  submitted report, the validator's pass/fail output, and the `--help` schema.

## Security Model: Exact Lockdown

The CI workflow executes these steps before the agent runs:

```yaml
- name: Lockdown CI assets
  run: |
    # CI module owned by root, agent can't modify validation or workflow files
    sudo chown -R root:root quality-control/ci/
    chmod -R 700 quality-control/ci/
    # submit-candidate needs +x (shell script), root-owned so agent can't modify
    chmod 755 quality-control/ci/submit-candidate
    # every justfile in the repo is blocked — agent can't run arbitrary recipes
    find . -name justfile -type f -exec chmod 000 {} +
    # just binary replaced with static blocker
    sudo install -m 755 quality-control/ci/just-blocked.sh /usr/local/bin/just
```

| Target | Permission | Rationale |
|--------|-----------|-----------|
| `quality-control/ci/` (directory) | `chmod 700`, root-owned | Agent cannot list or read contents |
| `submit-candidate` | `chmod 755`, root-owned | Agent can execute (shell script) but not modify |
| `just-blocked.sh` | `chmod 700`, root-owned | Agent cannot read the blocker script |
| Workflow YAMLs in CI dir | `chmod 700`, root-owned | Agent cannot see CI configuration |
| `check-report.py` | `chmod 700`, root-owned | Agent cannot read validator source (but `uv run` still works via opencode's `uv` invocation) |
| All `justfile`s in repo | `chmod 000` | Agent cannot run just recipes |
| `/usr/local/bin/just` | replaced with `just-blocked.sh` | Any `just` invocation prints error and exits 1 |

## Report Validation

The validator (`quality-control/check-report.py`) is a pydantic model. It exits 0
(valid, submission proceeds) or exits 1 (invalid, agent must fix and re-run).

**The agent discovers the full schema and rejection rules via:**

```
quality-control/ci/submit-candidate --help
```

Every validator error message includes a `FIX:` clause telling the agent what
to change. The agent iterates: submit → read error → fix → re-submit.

Key points:
- `report_type` selects the model: `"general"` → `GeneralReport`, `"slop"` → `SlopReport`
- Every path in the report must exist in git at `repo_sha` (verified via `git cat-file -e`)
- Finding locations are rejected if they target `.github/`, `.agents/`, `quality-control/`, or `opencode/skills/` paths
- `score` and `report` fields are NOT allowed — `ConfigDict(extra="forbid")` rejects any unknown field

**This README does NOT duplicate the schema.** The schema lives in `check-report.py`
and is exposed through `submit-candidate --help`. Always consult the live script
and validator output for the exact current contract.

## Usage in Another Repo

Requirements in the consuming repo:

- Python >=3.11 with `uv` installed
- OpenCode CLI (`npm install -g opencode-ai`)
- CC Safety Net (`npm install -g cc-safety-net`)
- Report staging directory: `.agents/review-runner/candidates/`

To install the workflows:

```bash
just -f path/to/quality-control/ci/justfile install path/to/target-repo
```

This copies `general-review-opencode.yml` and `slop-review-opencode.yml` into
`.github/workflows/`. Any existing file with the same name is backed up as
`.checkpoint` (symlinks are overwritten without backup).

## Debugging

All validator error messages now include `FIX:` guidance telling the agent what
to change. The agent iterates: submit → read FIX → fix same file → re-submit.

Common causes and their FIX guidance:

| Error prefix | FIX guidance |
|-------------|--------------|
| `violated_invariant contains prohibited pattern` | Name a specific violated contract/behavior, not a blanket claim. |
| `forbidden category` | Use a defect-type category, not CI infrastructure terms. |
| `is low-signal, must be tier2` | Change tier to `tier2` or use a non-low-signal category. |
| `at least one finding must be substantive` | Add a Tier 1 finding or use a substantive category. |
| `location is an infrastructure path` | Target source/test files in the PR diff, not infrastructure. |
| `path does not exist at commit` | Verify with `git cat-file -e <sha>:<path>` before submitting. |
| `Extra inputs are not permitted` | Remove `score` and `report` fields — those are computed by the renderer. |
| `String should have at most 40 characters` | `repo_sha` must be the full 40-char hex SHA. |
| `Input should be 'general' or 'slop'` | `report_type` must be exactly `"general"` or `"slop"`. |
