# Plan: Review Thread Workflow

## Goal

- **Current state:** Review findings are rendered into a single markdown blob and posted as a top-level PR issue comment via `gh pr comment`. The reconcile-review-comment.py script referenced in CI does not exist. Findings are not represented as resolvable GitHub review threads.
- **Target state:** Each validated finding becomes an individual GitHub PR review comment (thread), anchorable to a file/line where possible. A separate gardener agent (Phase 2) maintains the thread index and folds orphan/bot comments into existing threads.
- **Why this matters:** Review concerns are currently buried in a single unreolvable blob. GitHub's native resolved/unresolved thread state cannot be used. Duplicate detection, per-finding discussion, and state tracking are impossible.

## Constraints

- **Required:** The review agent pipeline (run-review.py → submitted.json → check-report.py validate → artifact) stays unchanged. The agent does not touch GitHub.
- **Required:** `post-validated-findings-as-review-threads.py` is a mechanical adapter script, not an intelligent agent. No LLM calls, no fallback logic, no "best effort" posting.
- **Required:** Uses `gh api` for all GitHub API calls (already available in CI, uses `GH_TOKEN`).
- **Forbidden:** No hidden metadata ledgers, hash-based dedup as authority, custom state tracking, PR acceptance gates, or merge blocking.
- **Forbidden:** No deletion or rewriting of existing comments.
- **Forbidden:** No `try`/`except ImportError` or conditional dependency loading.

## Prerequisites

- `GH_TOKEN` must be available in CI (already set by `github.token`)
- `gh` CLI must be installed in CI (already available)
- The artifact JSON schema (GeneralReport/SlopReport) is stable

## Scope

### Included targets

- `quality-control/ci/post-validated-findings-as-review-threads.py` (new script)
- `.github/workflows/general-review-opencode.yml` (update)
- `.github/workflows/slop-review-opencode.yml` (update)
- `quality-control/ci/submit-candidate` (minor — output the commit SHA alongside the artifact for use by poster)
- `quality-control/run-review.py` (minor — expose the review commit SHA for the poster)
- `quality-control/check-report.py` (minor — add `render_metadata` command that emits machine-parseable metadata for the poster)

### Excluded targets (Phase 2 — completed)

- [x] Gardener agent (separate workflow, agent, and script)
- [x] Index comment generation
- [x] Reviewer context file generation
- [x] External bot comment folding (allowed gardener action)

### Phase 0: Pre-work — expose metadata for thread posting

The thread poster needs the PR number, repo, and commit SHA. Currently `run-review.py` captures `repo_sha` but it's not easily accessible after the artifact is written.

#### Task 0.1: Add `metadata` subcommand to check-report.py

- **Location:** `quality-control/check-report.py`
- **What:** Add a `metadata` CLI subcommand that reads a validated artifact JSON and prints machine-parseable metadata: `repo_sha`, `report_type`, finding count, tier counts.
- **Dependencies:** None
- **Acceptance criteria:** `uv run quality-control/check-report.py metadata .review-report-artifact.json` prints `{"repo_sha": "...", "report_type": "general", "finding_count": 3, ...}`
- **Validation:** Run the command on a test artifact

#### Task 0.2: Expose repo_sha through submit-candidate

- **Location:** `quality-control/ci/submit-candidate`
- **What:** After successful validation and render, also run `check-report.py metadata` on the artifact so the CI workflow can capture `repo_sha` for the thread poster.
- **Dependencies:** Task 0.1
- **Acceptance criteria:** `submit-candidate` prints `REPO_SHA=<sha>` on stdout after successful validation
- **Validation:** Run submit-candidate on a valid report and check for the REPO_SHA line

### Phase 1: Core — thread poster script

#### Task 1.1: Create post-validated-findings-as-review-threads.py

- **Location:** `quality-control/ci/post-validated-findings-as-review-threads.py`
- **What:** A mechanical Python script (no LLM) that:
  1. Reads the validated artifact JSON
  2. For each finding with an anchorable location (file exists in PR diff):
     - Posts a PR review comment via `POST /repos/{owner}/{repo}/pulls/{pull_number}/comments`
     - Uses `gh api` with `--method POST`
     - Body includes: finding tier, label, violated_invariant, proof_command, evidence, source attribution
     - Uses `commit_id` = PR head SHA, `path` = finding.location.path, `line` = finding.location.start_line
  3. For findings whose file is not in the PR diff (should not happen for PR-scoped reviews, but handle gracefully): collects into an "unthreadable" list
  4. Prints a structured summary: how many threads created, how many unthreadable, with URLs
  5. Writes a compact `.review-thread-summary.json` with thread IDs and URLs for downstream use
- **Arguments:**
  - `--artifact` (required): path to validated artifact JSON
  - `--pr-number` (required): PR number
  - `--repo` (required): `owner/repo` format
  - `--dry-run` (optional): print what would be posted without posting
- **Dependencies:** Task 0.1, Task 0.2
- **Acceptance criteria:**
  - Running with `--dry-run` prints each finding that would be posted without making API calls
  - Running without `--dry-run` posts review comments and prints thread URLs
  - Running on an artifact with 0 findings prints "No findings to post" and exits 0
  - Running on artifact where no files are in the diff: all findings go to unthreadable list
- **Validation:**
  - Unit-testable: extract the comment-body construction and finding-to-thread mapping into pure functions
  - Integration: run against a real PR with `--dry-run` to verify the API contract
  - CI: script exits 0 on success, 1 on API failure

**Comment body format (example):**

```md
### [General Review][tier1] Suppressed validator failure

**Concern.** The review runner can continue after validator failure.

**Violated invariant.** Every error path must fail loudly, but the CI runner
silently swallows diff-retrieval failures instead of aborting.

**Proof command.** `grep -n 'get_diff' quality-control/run-review.py`

**Evidence.**
- `quality-control/run-review.py:120-146` (diff-snippet)

Source: General Review run <run-id>, commit abc1234.
```

#### Task 1.2: Add `--findings-to-threads` subcommand support

- **Location:** `quality-control/check-report.py`
- **What:** Add a `finding-body` subcommand that takes a finding index and renders the review thread body from the artifact JSON. This lets the poster script be a thin shell script if desired, or keeps the body rendering logic in the validated module.
- **Dependencies:** Task 1.1 (can be done in parallel)
- **Acceptance criteria:** `uv run check-report.py finding-body .review-report-artifact.json --index 0` prints the markdown body for the first finding
- **Validation:** Run against a valid artifact and verify the output has the expected sections

### Phase 2: CI workflow changes

#### Task 2.1: Update general-review-opencode.yml

- **Location:** `.github/workflows/general-review-opencode.yml`
- **What:**
  1. Remove the "Reconcile with prior comments" step (the script doesn't exist and the design replaces it)
  2. Replace the "Post PR Comment" step with "Post validated findings as review threads"
  3. New step runs: `uv run quality-control/ci/post-validated-findings-as-review-threads.py --artifact .review-report-artifact.json --pr-number ${{ github.event.number }} --repo ${{ github.repository }}`
  4. Keep the "Check Threshold" step as-is
- **Dependencies:** Task 1.1, Task 1.2
- **Acceptance criteria:** CI run creates review threads instead of a single blob comment
- **Validation:** Trigger a PR CI run and verify review comments appear in "Files Changed" tab

#### Task 2.2: Update slop-review-opencode.yml

- **Location:** `.github/workflows/slop-review-opencode.yml`
- **What:** Same changes as Task 2.1, applied to the slop workflow
- **Dependencies:** Task 1.1, Task 1.2
- **Acceptance criteria:** Same as 2.1 for slop review
- **Validation:** Trigger a PR CI run and verify review comments appear in "Files Changed" tab

### Phase 3: Verification

#### Task 3.1: Test with a real artifact

- **What:** Run the full pipeline locally against a recent PR artifact (or generate a test artifact) to verify end-to-end
- **Dependencies:** Task 1.1
- **Acceptance criteria:** Script posts review threads and outputs a valid summary
- **Validation:** Check that review comments appear in the PR's "Files Changed" tab

## System-Level Validation

- **End-to-end:** A CI run produces review threads in the PR "Files Changed" tab instead of a single top-level comment blob
- **Dry-run safety:** `--dry-run` prints what would be posted without making any API calls
- **Zero-finding case:** Artifact with no findings exits 0 and prints "No findings to post"
- **Unthreadable handling:** Findings that can't be anchored are collected into a list (not lost)

## Risks / Rollback

| Risk | Mitigation | Rollback |
|------|-----------|----------|
| `gh api` call fails due to permissions | Script checks for `GH_TOKEN` and exits with clear error; CI already has `pull-requests: write` | Revert workflow YAML to previous `gh pr comment` step |
| File in finding is not in the PR diff | PR-scoped reviews should only flag files in the diff; handle gracefully with unthreadable list | Keep blob comment as fallback for unthreadable items |
| API rate limiting | Each review posts N + 1 comments (findings count). For typical review (3-8 findings), this is well within limits | N/A |
| Line number doesn't match PR diff | `line` parameter references the file line, not diff position; if out of range, API returns 422. Script catches and demotes to unthreadable | N/A |

## Stop Rules

- Do not proceed if `gh api` is not available or GH_TOKEN is not set
- Do not proceed if the artifact JSON schema has changed incompatibly
- Do not proceed if a finding's `location.path` doesn't exist in the repo (already validated by check-report.py, but guard in poster too)

## Execution Progress

### Phase 0: Pre-work

- [ ] Task 0.1: Add metadata subcommand to check-report.py
- [ ] Task 0.2: Expose repo_sha through submit-candidate

### Phase 1: Core implementation

- [ ] Task 1.1: Create post-validated-findings-as-review-threads.py
- [ ] Task 1.2: Add finding-body subcommand to check-report.py

### Phase 2: CI workflow changes

- [ ] Task 2.1: Update general-review-opencode.yml
- [ ] Task 2.2: Update slop-review-opencode.yml

### Phase 3: Verification

- [ ] Task 3.1: Test with a real artifact (dry-run and live)

### System-Level Validation

- [ ] Dry-run produces correct comment bodies
- [ ] Live run creates review threads visible in PR
- [ ] Zero-finding artifact exits cleanly
- [ ] Unthreadable findings are collected (not lost)
