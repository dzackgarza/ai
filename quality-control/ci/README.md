# CI Review Runner

OpenCode-powered review infrastructure. Two review types:

- **General review** — structural code quality audit: architectural decay, dead code,
  test quality, dependency mismanagement, semantic regressions.
- **Slop review** — AI-generated-code audit: bridge-burning violations, runtime
  control-flow defects, test/text antipatterns, validation-evasion constructs,
  defaults/fallbacks/mocks/skips.

Each type runs in two scopes:

- **Repo scope** — full-repository sweep (weekly cron, push to main, manual dispatch).
- **Diff scope** — PR review confined to the diff against the base branch
  (every pull request).

Findings are uploaded as SARIF to GitHub code scanning alerts, providing persistent
state (open / dismissed / fixed) across runs. PR runs upload under the same SARIF
categories as the repo-wide runs, so code scanning natively computes "new alerts
introduced by this PR" and annotates the diff — no comment posting, no thread
maintenance.

## File Inventory

### Workflows (`.github/workflows/`)

| Path | Purpose |
|------|---------|
| `_review.yml` | Reusable workflow — parameterized by `report_type` (general/slop), `scope` (repo/diff), optional `fail_below` |
| `review-general.yml` | Caller — general/repo on dispatch, weekly (Mon), push to main |
| `review-slop.yml` | Caller — slop/repo on dispatch, weekly (Thu), push to main |
| `review-pr.yml` | Caller — both types, diff-scoped, on every pull request |

### Runner-owned (`quality-control/ci/` — visible to CI, not visible to reviewer)

| Path | Purpose |
|------|---------|
| `runner.just` | Justfile with all CI setup/run/collect/convert recipes |
| `private/submit-candidate` | Root-owned validator — validates report JSON |
| `private/check-report.py` | Pydantic models, schema printer, validator, metadata |
| `report-to-sarif.py` | Converts validated artifact to SARIF 2.1.0 for code scanning upload |
| `fetch-reviewer-context.py` | Queries existing code scanning alerts (and, on PR runs, existing PR review threads) for reviewer context |
| `post-review-threads.py` | PR runs only — posts the artifact as one review: summary body + one resolvable thread per finding |
| `reviewer_home/` | Static template for `/home/reviewer` — opencode config (incl. model), cc-safety-net rules, public wrapper |

### Review definitions (`quality-control/reviews/`)

| Path | Purpose |
|------|---------|
| `general/template.md`, `slop/template.md` | Agent task prompt per review type |
| `general/manifest.txt`, `slop/manifest.txt` | Static list of documents (skills, guides) inlined into the prompt |
| `scope-repo.md`, `scope-diff.md` | Scope framing prepended to the prompt |

### Harness (`quality-control/`)

| Path | Purpose |
|------|---------|
| `run-review.py` | Assembles prompt (context + scope + manifest + repo docs + template), loops opencode until a validated artifact exists |

### Reviewer-visible (inside `/home/reviewer`)

| Path | Purpose |
|------|---------|
| `bin/submit-candidate` | Public wrapper — delegates to `/opt/ai-review/private/submit-candidate` via sudo |

## How the Reporting Loop Works

```
Workflow caller triggers (cron / dispatch / push main / pull_request)
  → _review.yml: install tools, fetch-context, prepare reviewer
  → [diff scope only] stage-pr-diff writes .reviewer-diff.patch into reviewer repo
  → run-review (as `reviewer` user): run-review.py assembles the prompt and
    loops `opencode run` (continuing the session) until the artifact exists
  → opencode agent:
      1. Reads scope instructions, inlined skills, and task template
      2. Reads reviewer context (existing alerts — do not re-report)
      3. Writes report to .agents/review-runner/candidates/submitted.json
      4. Runs `submit-candidate --help` to learn schema + rejection rules
      5. Runs `submit-candidate` (no arguments)
      6. If exit 0 → done. If non-zero → read error (has FIX: guidance) → fix same file → repeat
   → submit-candidate (public wrapper, /home/reviewer/bin/submit-candidate)
     → sudo to /opt/ai-review/private/submit-candidate (root-owned, not readable by reviewer)
       → calls `uv run check-report.py validate` (pydantic validation)
       → on pass: cp to .review-report-artifact.json
       → on fail: print errors with FIX: guidance, exit 1
   → collect-output copies the artifact to the control repo
   → convert-sarif converts it (report-to-sarif.py)
   → github/codeql-action/upload-sarif@v4 → code scanning alerts
   → [diff scope only] post-threads posts the artifact to the PR as one
     review: summary body + one resolvable thread per finding
```

## Data Flow

```
Review artifact (.review-report-artifact.json)
  → report-to-sarif.py
    → .review-report.sarif
      → github/codeql-action/upload-sarif@v4
        → GitHub code scanning alerts (persistent state)

Next review run (any scope):
  → fetch-reviewer-context.py queries code scanning alerts
    → .reviewer-context.md
      → opencode agent (instructed not to re-report existing findings)

PR runs: same category as repo runs → code scanning diffs alerts against
the base analysis → "new alerts" annotations appear on the PR.
```

## Prompt Assembly

`run-review.py` builds the reviewer prompt from static files, in order:

1. `.reviewer-context.md` — existing tracked findings (do-not-re-report)
2. `reviews/scope-{repo,diff}.md` — what to look at
3. `reviews/<type>/manifest.txt` — every listed document inlined verbatim
   (a directory entry inlines its top-level `*.md`, sorted; missing entries fatal)
4. Repo docs — all README/AGENTS files in the reviewer's copy
5. `reviews/<type>/template.md` — the task and output contract

The reviewer model is set in `reviewer_home/.config/opencode/opencode.json`,
not in code.

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
| (category + path) | `partialFingerprints.reviewFindingKey` (SHA256) |

### Fingerprint stability

The `reviewFindingKey` fingerprint is a deterministic hash of
`category | path`.  It deliberately excludes line numbers, timestamps,
commit SHAs, and the agent-chosen label (free text reinvented each run) so
the same defect class in the same file maps to one identity across runs and
code movement.  Two distinct same-category findings in one file merge — the
accepted cost of making "don't re-raise pending remediation" stick.

### SARIF categories

| Review type | Tool name (`tool.driver.name`) | `upload-sarif` category |
|-------------|-------------------------------|------------------------|
| General | `ai-review/general` | `ai-general-review` |
| Slop | `ai-review/slop` | `ai-slop-review` |

Both scopes of a type share one category. The alerts API filters by the
**tool name** (`tool.driver.name`), not the upload category —
`fetch-reviewer-context.py` queries with `ai-review/general` /
`ai-review/slop`.

## Key invariants

- Agent writes to a **fixed path** — never passes filenames to `submit-candidate`.
  Always `.agents/review-runner/candidates/submitted.json`.
- `submit-candidate` takes **no arguments** (except `--help`). It reads the fixed path,
  validates, and either exits 0 (copied to artifact path) or non-zero (errors printed).
- Agent discovers the schema via `submit-candidate --help` — never reads CI infrastructure files.
- Runner does NOT re-validate. It only checks artifact file existence after opencode exits.
- **CI infrastructure is invisible to the agent**: no `.github/workflows/`,
  no `quality-control/ci/`, no `/opt/ai-review/private/`.
- Everything the reviewer sees is statically declared in the repo: home dir
  template, model, manifests, scope files, task templates.

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

## PR Review Threads

On diff-scoped runs, `post-review-threads.py` consumes the validated artifact
plus the staged diff and posts a single PR review: a top-level body (run link,
finding counts, off-diff list) with one inline, individually-resolvable
comment per finding. The reviewer agent is not involved — this is pure
artifact post-processing.

Anchor classification is computed from the diff before posting:

| Finding location | Surfacing |
|------------------|-----------|
| Line visible in the diff | Line-anchored resolvable thread |
| File in diff, lines outside hunks | Thread on the file's first visible line (body carries the real range) |
| File not in the diff | Top-level body list only (already in code scanning) |

Each thread body embeds `ai-review-fingerprint: <sha256(category|path)>`
(same components as the SARIF `reviewFindingKey`). Before posting, existing
threads on the PR are scanned for these markers and matching findings are
skipped — resolved threads count as dispositions and stay skipped. Thread
bodies are diagnosis-only; remediation is out of scope for reviewers and is
never rendered.

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
previously reported findings, across both repo-wide and PR runs.

On PR runs the context additionally includes alerts on the PR ref and a
digest of every review thread already on the PR (any author — including
other bots), each marked open or resolved, with the same do-not-re-raise
instruction.

## Usage in Another Repo

Requirements in the consuming repo:

- Python >=3.11 with `uv` installed
- OpenCode CLI (`npm install -g opencode-ai`)
- CC Safety Net (`npm install -g cc-safety-net`)
- GitHub Code Security / code scanning enabled (free for public repos)

Copy `.github/workflows/{_review,review-general,review-slop,review-pr}.yml`,
the `quality-control/ci/` directory, `quality-control/run-review.py`, and
`quality-control/reviews/` into the target repo.

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
gh workflow run "General Review" --ref <branch>
gh run list --branch <branch> --limit 10
gh run view <RUN_ID> --log-failed
```
