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
  → submit-candidate calls `uv run check-report.py validate` (pydantic validation)
  → On validation pass: cp to .review-report-artifact.json,
    then runs `uv run check-report.py render` to produce .review-report-comment.md
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

The schema and rejection rules are defined in `submit-candidate --help`:

```
quality-control/ci/submit-candidate --help
```

The agent reads this to learn the expected JSON format and constraints before
submitting. On validation failure, error messages include `FIX:` guidance
telling the agent what to change.

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

Validator error messages include `FIX:` guidance. The agent reads the error,
fixes the report, and re-submits. The script's output is the debugging surface.
