# CI Review Runner

OpenCode-powered repo-wide review infrastructure. Two review types:

- **General review** — structural code quality audit: architectural decay, dead code,
  test quality, dependency mismanagement, semantic regressions.
- **Slop review** — AI-generated-code audit: bridge-burning violations, runtime
  control-flow defects, test/text antipatterns, validation-evasion constructs,
  defaults/fallbacks/mocks/skips.

Findings are uploaded as SARIF to GitHub code scanning alerts, providing persistent
state (open / dismissed / fixed) across runs without PR comment spam.

## File Inventory

### Runner-owned (visible to CI, not visible to reviewer)

| Path | Purpose |
|------|---------|
| `runner.just` | Justfile with all CI setup/run/collect/convert recipes |
| `private/submit-candidate` | Root-owned validator — validates report JSON, renders PR comment |
| `private/check-report.py` | Pydantic models, schema printer, validator, renderer |
| `report-to-sarif.py` | Converts validated artifact to SARIF 2.1.0 for code scanning upload |
| `fetch-reviewer-context.py` | Queries existing code scanning alerts for reviewer context |
| `reviewer_home/` | Template for `/home/reviewer` — configs, public wrapper, dotfiles |

### Reviewer-visible (inside `/home/reviewer/repo`)

| Path | Purpose |
|------|---------|
| `bin/submit-candidate` | Public wrapper — delegates to `/opt/ai-review/private/submit-candidate` via sudo |

### Outside this directory (`quality-control/`)

| Path | Purpose |
|------|---------|
| `run-review.py` | Harness — feeds template to opencode, retries on timeout, collects artifact |
| `reviews/general/template.md` | Agent prompt for general review |
| `reviews/slop/template.md` | Agent prompt for slop review |

## How the Reporting Loop Works

```
CI workflow triggers (scheduled / workflow_dispatch / push main)
  → runner.just prepares reviewer user, installs private tools, copies reviewer home
  → runner.just fetch-context (queries existing code scanning alerts)
  → runner.just run-review (feeds template + skills + context to `opencode` as reviewer)
  → opencode agent (runs as `reviewer` user):
      1. Reads template.md for instruction set
      2. Reads reviewer context (existing alerts — do not re-report)
      3. Writes report to .agents/review-runner/candidates/submitted.json
      4. Runs `submit-candidate --help` to learn schema + rejection rules
      5. Fixes report to match schema
      6. Runs `submit-candidate` (no arguments)
      7. If exit 0 → done. If non-zero → read error (has FIX: guidance) → fix same file → goto 6
   → submit-candidate (public wrapper, /home/reviewer/bin/submit-candidate)
     → sudo to /opt/ai-review/private/submit-candidate (root-owned, not readable by reviewer)
       → calls `uv run check-report.py validate` (pydantic validation)
   → On validation pass: cp to .review-report-artifact.json
   → On validation fail: print errors with FIX: guidance, exit 1
   → runner collects output (collect-output recipe)
   → runner converts to SARIF (convert-sarif recipe)
   → upload to code scanning
```

## Data Flow

```
Review artifact (.review-report-artifact.json)
  → report-to-sarif.py
    → .review-report.sarif
      → github/codeql-action/upload-sarif@v4
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
- Runner does NOT re-validate. It only checks artifact file existence after opencode exits.
- **CI infrastructure is invisible to the agent**: no `.github/workflows/`,
  no `quality-control/ci/`, no `/opt/ai-review/private/`.

## Security Model: Two-User Isolation

The CI workflow runs as `runner`. A dedicated `reviewer` user runs opencode
with no passwordless sudo except one narrow rule permitting exactly one command.

### Sudo restriction

Only one sudo rule exists for the `reviewer` user:

```
reviewer ALL=(root) NOPASSWD: /opt/ai-review/private/submit-candidate *
```

`reviewer` may run exactly the private submit command as root. It cannot `sudo cat`,
`sudo chmod`, any other path, or any arbitrary command.

### Enforcement

The agent runs as `reviewer`. It can:

- Read the source checkout (sanitized copy in `/home/reviewer/repo`)
- Write its candidate report to the fixed path
- Execute `submit-candidate --help` (shows schema)
- Execute `submit-candidate` (validates via private impl)
- Read stdout/stderr of the private implementation

It cannot:

- Read or list `quality-control/ci/`
- Read or list `.github/workflows/`
- Read `/opt/ai-review/private/check-report.py` or `submit-candidate`
- Run any other `sudo` command
- Access sudo without `--preserve-env=REPORT_TYPE,REVIEWER_REPO,CONTROL_REPO`

## Report Validation

The schema and rejection rules are defined in `submit-candidate --help`:

```
submit-candidate --help
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

## Workflows

Two workflows in `.github/workflows/`:

- `general-review-opencode.yml` — runs weekly (Mon) and on push to main
- `slop-review-opencode.yml` — runs weekly (Thu) and on push to main

Both install `just` inline, then delegate all setup/review/collect/convert steps
to `just -f quality-control/ci/runner.just`.

## Usage in Another Repo

Requirements in the consuming repo:

- Python >=3.11 with `uv` installed
- OpenCode CLI (`npm install -g opencode-ai`)
- CC Safety Net (`npm install -g cc-safety-net`)
- Report staging directory: `.agents/review-runner/candidates/`
- GitHub Code Security / code scanning enabled (free for public repos)

Copy `.github/workflows/general-review-opencode.yml` and
`slop-review-opencode.yml` into the target repo, then copy the entire
`quality-control/ci/` directory.

## Debugging

Validator error messages include `FIX:` guidance. The agent reads the error,
fixes the report, and re-submits. The script's output is the debugging surface.

For SARIF debugging, run the converter locally:

```bash
uv run quality-control/ci/report-to-sarif.py \
  --artifact .review-report-artifact.json \
  --output .review-report.sarif
```

For workflow debugging, use `gh`:

```bash
gh workflow run "General Review (OpenCode)" --ref <branch>
gh run list --branch <branch> --limit 10
gh run view <RUN_ID> --log-failed
```
