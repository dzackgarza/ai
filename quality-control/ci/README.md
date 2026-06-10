# CI Review Runner

Opencode-powered repo-wide review infrastructure. Two review types:

- **General review** — structural code quality audit: architectural decay, dead code,
  test quality, dependency mismanagement, semantic regressions.
- **Slop review** — AI-generated-code audit: bridge-burning violations, runtime
  control-flow defects, test/text antipatterns, validation-evasion constructs,
  defaults/fallbacks/mocks/skips.

Findings are uploaded as SARIF to GitHub code scanning alerts, providing persistent
state (open / dismissed / fixed) across runs without PR comment spam.

## File Inventory

### In this directory (`quality-control/ci/`)

| File | Purpose |
|------|---------|
| `general-review-opencode.yml` | CI workflow definition — general review |
| `slop-review-opencode.yml` | CI workflow definition — slop review |
| `submit-candidate` | Script the agent runs to validate + submit a report |
| `report-to-sarif.py` | Converts validated artifact to SARIF 2.1.0 for code scanning upload |
| `fetch-reviewer-context.py` | Queries existing code scanning alerts for reviewer context |
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
CI workflow triggers (scheduled / workflow_dispatch / push main)
  → Lockdown (see below)
  → fetch-reviewer-context.py queries existing code scanning alerts
  → run-review.py feeds template + skills + context to `opencode run`
  → opencode agent:
      1. Reads template.md for instruction set
      2. Reads reviewer context (existing alerts — do not re-report)
      3. Writes report to .agents/review-runner/candidates/submitted.json
      4. Runs `submit-candidate --help` to learn schema + rejection rules
      5. Fixes report to match schema
      6. Runs `quality-control/ci/submit-candidate` (no arguments)
      7. If exit 0 → done. If non-zero → read error (has FIX: guidance) → fix same file → goto 6
  → submit-candidate calls `uv run check-report.py validate` (pydantic validation)
   → On validation pass: cp to .review-report-artifact.json
   → On validation fail: print errors with FIX: guidance, exit 1
  → harness checks .review-report-artifact.json exists after opencode exits
      - exists → report-to-sarif.py converts to SARIF → upload to code scanning
      - missing → append continuation prompt, loop
```

## Data Flow

```
Review artifact (.review-report-artifact.json)
  → report-to-sarif.py
    → .review-report.sarif
      → github/codeql-action/upload-sarif@v3
        → GitHub code scanning alerts (persistent state)

Next review run:
  → fetch-reviewer-context.py queries code scanning alerts
    → .reviewer-context.md
      → opencode agent (instructed not to re-report existing findings)
```

## SARIF Mapping

Each finding in the validated artifact becomes one code scanning alert:

| Artifact field | SARIF location |
|----------------|----------------|
| `category` | `ruleId`, `tool.driver.rules[].id` |
| `label` | `tool.driver.rules[].name` |
| `tier` (tier1/tier2) | `level` (error/warning) |
| `violated_invariant` | `message.text` |
| `location.path` | `physicalLocation.artifactLocation.uri` |
| `location.start_line` | `physicalLocation.region.startLine` |
| `location.end_line` | `physicalLocation.region.endLine` |
| (category + label + path) | `partialFingerprints.reviewFindingKey` (SHA256) |

### Fingerprint stability

The `reviewFindingKey` fingerprint is a deterministic hash of
`category | label | path`.  It deliberately excludes line numbers, timestamps,
and commit SHAs so the same finding maps to the same alert across code
movement.  The fingerprint exists only for alert lookup — deduplication is
never attempted.

### SARIF categories

| Review type | Tool name (`tool.driver.name`) | `upload-sarif` category |
|-------------|-------------------------------|------------------------|
| General | `ai-review/general` | `ai-general-review` |
| Slop | `ai-review/slop` | `ai-slop-review` |

These are used by `fetch-reviewer-context.py` to query existing alerts via
the code scanning API using the `tool_name` filter.

## Key invariants

- Agent writes to a **fixed path** — never passes filenames to `submit-candidate`.
  Always `.agents/review-runner/candidates/submitted.json`.
- `submit-candidate` takes **no arguments** (except `--help`). It reads the fixed path,
  validates, and either exits 0 (copied to artifact path) or non-zero (errors printed).
- Agent discovers the schema via `submit-candidate --help` — never reads CI infrastructure files.
- Harness does NOT re-validate. It only checks artifact file existence after opencode exits.
- **Everything is invisible to the agent** except: the template.md it receives, its own
  submitted report, the validator's pass/fail output, reviewer context, and the `--help` schema.

## Security Model: Exact Lockdown

The CI workflow executes these steps before the agent runs:

```yaml
- name: Lockdown CI assets
  run: |
    sudo chown -R root:root quality-control/ci/
    sudo chmod 755 quality-control/ci/
    sudo find quality-control/ci -type f -exec chmod 700 {} +
    sudo chmod 755 quality-control/ci/submit-candidate
    sudo find . -name justfile -type f -exec chmod 000 {} +
```

| Target | Permission | Rationale |
|--------|-----------|-----------|
| `quality-control/ci/` (directory) | `chmod 755`, root-owned | Non-root can traverse and open known files |
| `submit-candidate` | `chmod 755`, root-owned | Agent can execute (shell script) but not modify |
| Everything else in `ci/` | `chmod 700`, root-owned | Agent cannot read workflow configs or helper scripts |
| All `justfile`s in repo | `chmod 000` | Agent cannot run `just` recipes |
| `/usr/local/bin/just` | replaced with `just-blocked.sh` | Any `just` invocation prints error and exits 1 |

## Report Validation

The schema and rejection rules are defined in `submit-candidate --help`:

```
quality-control/ci/submit-candidate --help
```

The agent reads this to learn the expected JSON format and constraints before
submitting. On validation failure, error messages include `FIX:` guidance
telling the agent what to change.

## Reviewer Context (Avoiding Repeats)

Before the agent runs, `fetch-reviewer-context.py` queries the repo's existing
code scanning alerts for the relevant tool categories and produces a markdown
context file.  The agent receives this as instructions:

```
Do not intentionally re-raise these issues unless you have new evidence,
the problem reappears in a materially different form, or the previous
resolution is directly contradicted by the current code.
```

This is the mechanism that prevents new review agents from rediscovering
previously reported findings.

## Usage in Another Repo

Requirements in the consuming repo:

- Python >=3.11 with `uv` installed
- OpenCode CLI (`npm install -g opencode-ai`)
- CC Safety Net (`npm install -g cc-safety-net`)
- Report staging directory: `.agents/review-runner/candidates/`
- GitHub Code Security / code scanning enabled (free for public repos)

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

For SARIF debugging, run the converter locally:

```bash
uv run quality-control/ci/report-to-sarif.py \
  --artifact .review-report-artifact.json \
  --output .review-report.sarif
```
