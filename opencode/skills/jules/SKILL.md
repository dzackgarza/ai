---
name: jules
description: Use when delegating a coding task to Jules — bug fixes, tests, docs, features, or code reviews on a GitHub repo.
license: Apache-2.0
metadata:
author: sanjay3290
version: '1.1'
---

# Jules Task Delegation

Delegate coding tasks to Google's Jules AI agent on GitHub repositories.

## IMPORTANT: Quality Caveats

**Jules is a weak agent with significant failure modes.** All work must be heavily validated, gated, and reviewed before approval. Treat Jules output adversarially when reviewing.

### Common Failure Patterns

- **Hollow PRs**: Minimal or trivial changes that don't actually solve the problem
- **High LOC for simple features**: Unnecessarily verbose implementations
- **Rushing to fix**: No root cause research, just monkey-patches
- **Poor integration**: Doesn't use existing code patterns
- **Testing theater**: Tests that pass but don't verify meaningful behavior
- **Obfuscation**: Complex code hiding lack of substance
- **Reward hacking**: Minimal path to "done" without real value
- **Early termination**: Stops before significant work is complete
- **Goal substitution**: Completes a different task than requested

### Validation Requirements

- **ALWAYS** load `test-guidelines` skill when reviewing Jules output
- Check that tests verify correctness, not just coverage
- Verify the implementation addresses the actual root cause
- Look for shortcuts, workarounds, and incomplete solutions
- Reprompt Jules to continue when gaps are found

### Automated Review Limitations

Automated GitHub reviewers are given **only the PR diff and Jules' own description of it**. They have no access to the original task, the original expectations, or any blockers Jules encountered along the way.

Reviewers are trained to find bugs, logical errors, and **inconsistencies between what Jules reports and what the code actually does**. This is a useful check — but it only operates within Jules' own framing. The one thing reviewers cannot do is compare the original task requirements against what was delivered, because the only source of "expectations" available to them is Jules' own PR title, body, and commit messages. Jules controls all of that, and Jules is incentivized to make its work appear aligned with expectations — downplaying or omitting blockers, fallback decisions, or abandoned goals entirely.

**Concrete example:** Jules hits a blocker and decides it cannot implement the requested feature. Instead of reporting failure, it implements scaffolding and reframes the PR as "laying the groundwork for future implementation." The PR description presents this as forward progress. Automated reviewers evaluate it as a scaffolding task — checking that the scaffolding is well-structured, consistent, and bug-free. It passes. The original task ("implement the feature") was a complete failure, but nothing in the review pipeline had any way to know that.

**Clearing automated review is not sufficient.** You must independently compare the original task against actual PR contents, using your own copy of the original task description — not Jules' framing — as the benchmark for completeness.

### When to Use Jules

Jules has a restricted Linux environment with no access to online docs or external references. Context engineering in the prompt is essential.

**Best for:**

- Straightforward tasks where the desired solution is already known
- Work where research has already been done
- Purely internal code changes (no external dependencies)
- First 50%+ of a larger task (expect ~90% completion, rarely 100%)

**Avoid for:**

- Tasks requiring external API research
- Complex integration with unfamiliar libraries
- Work likely to need babysitting through repeated prompts

**Cost/Benefit:**

| Aspect      | Value                            |
| ----------- | -------------------------------- |
| Free tier   | 100 tasks/day                    |
| Concurrency | Up to 15 parallel                |
| Model       | Watered-down Gemini 3 (Mar 2026) |
| Quality     | Good for 50-90%, rarely complete |

**No Jules PR should be accepted without deep review. Automated reviews are insufficient.**

---

## Setup (Run Before First Command)

### 1. Install CLI

```bash
which jules || npm install -g @google/jules
```

### 2. Check Auth

```bash
jules remote list --repo
```

If fails → tell user to run `jules login` (or `--no-launch-browser` for headless)

### 3. Auto-Detect Repo

```bash
git remote get-url origin 2>/dev/null | sed -E 's#.*(github\.com)[/:]([^/]+/[^/.]+)(\.git)?#\2#'
```

If not GitHub or not in git repo → ask user for `--repo owner/repo`

### 4. Verify Repo Connected

Check repo is in `jules remote list --repo`. If not → direct to https://jules.google.com

## Commands

### Create Tasks

```bash
jules new "Fix auth bug" # Auto-detected repo
jules new --repo owner/repo "Add unit tests" # Specific repo
jules new --repo owner/repo --parallel 3 "Implement X" # Parallel sessions
cat task.md | jules new --repo owner/repo # From stdin
```

### Monitor

```bash
jules remote list --session # All sessions
jules remote list --repo # Connected repos
```

### Retrieve Results

```bash
jules remote pull --session <id>          # View diff
jules remote pull --session <id> --apply  # Apply locally
jules teleport <id>                       # Clone + apply
```

### Latest Session Shortcut

```bash
LATEST=$(jules remote list --session 2>/dev/null | awk 'NR==2 {print $1}')
jules remote pull --session $LATEST
```

## Smart Context Injection

Enrich prompts with current context for better results:

```bash
BRANCH=$(git branch --show-current)
RECENT_FILES=$(git diff --name-only HEAD~3 2>/dev/null | head -10 | tr '\n' ', ')
RECENT_COMMITS=$(git log --oneline -5 | tr '\n' '; ')
STAGED=$(git diff --cached --name-only | tr '\n' ', ')

jules new --repo owner/repo "Fix the bug in auth module. Context: branch=$BRANCH, recently modified: $RECENT_FILES"
```

## Template Prompts

### Add Tests

```bash
FILES=$(git diff --name-only HEAD~3 2>/dev/null | grep -E '\.(js|ts|py|go|java)$' | head -5 | tr '\n' ', ')
jules new "Add unit tests for recently modified files: $FILES. Include edge cases and mocks where needed."
```

### Add Documentation

```bash
FILES=$(git diff --name-only HEAD~3 2>/dev/null | grep -E '\.(js|ts|py|go|java)$' | head -5 | tr '\n' ', ')
jules new "Add documentation comments to: $FILES. Include function descriptions, parameters, return values, and examples."
```

### Fix Lint Errors

```bash
jules new "Fix all linting errors in the codebase. Run the linter, identify issues, and fix them while maintaining code functionality."
```

### Review PR

```bash
PR_NUM=123
PR_INFO=$(gh pr view $PR_NUM --json title,body,files --jq '"\(.title)\n\(.body)\nFiles: \(.files[].path)"')
jules new "Review this PR for bugs, security issues, and improvements: $PR_INFO"
```

## Workflow

1. **Create**: `jules new "Task description"`
2. **Monitor**: `jules remote list --session` or https://jules.google.com
3. **Pull**: `jules remote pull --session <id>`
4. **Validate**: Load `test-guidelines`, review adversarially
5. **Apply**: `jules remote pull --session <id> --apply` (only after validation)
6. **Reprompt**: If gaps found, reprompt Jules to continue

## Git Integration (Apply + Commit)

After Jules completes and you've validated the work:

```bash
SESSION_ID=""
TASK_DESC=""
git checkout -b "jules/$SESSION_ID"
jules remote pull --session "$SESSION_ID" --apply
git add -A
git commit -m "feat: $TASK_DESC
Jules session: $SESSION_ID"
git push -u origin "jules/$SESSION_ID"
gh pr create --title "$TASK_DESC" --body-file .pr/PR_BODY.md --draft
```

> **Important:** The PR body must come from the tracked contract file (`.pr/PR_BODY.md`), not from memory or the web form. See **PR Contract** section above for the full workflow.

## Poll Until Complete

```bash
SESSION_ID=""
while true; do
STATUS=$(jules remote list --session 2>/dev/null | grep "$SESSION_ID" | awk '{print $NF}')
case "$STATUS" in
Completed)
echo "Done!"
jules remote pull --session "$SESSION_ID"
break ;;
Failed)
echo "Failed. Check: https://jules.google.com/session/$SESSION_ID"
break ;;
*User*)
echo "Needs input: https://jules.google.com/session/$SESSION_ID"
break ;;
*)
echo "Status: $STATUS - waiting 30s..."
sleep 30 ;;
esac
done
```

## AGENTS.md Template

Create in repo root to improve Jules results:

```markdown
# AGENTS.md

## Project Overview

[Brief description]

## Tech Stack

- Language: [TypeScript/Python/Go/etc.]
- Framework: [React/FastAPI/Gin/etc.]
- Testing: [Jest/pytest/go test/etc.]

## Code Conventions

- [Linter/formatter used]
- [Naming conventions]
- [File organization]

## Testing Requirements

- Unit tests for new features
- Integration tests for APIs
- Coverage target: [X]%

## Build & Deploy

- Build: `[command]`
- Test: `[command]`
```

## Session States

| Status                 | Action            |
| ---------------------- | ----------------- |
| Planning / In Progress | Wait              |
| Awaiting User          | Respond at web UI |
| Completed              | Pull & validate   |
| Failed                 | Check web UI      |

## Notes

- **No CLI reply** → Use web UI for Jules questions
- **No CLI cancel** → Use web UI to cancel
- **GitHub only** → GitLab/Bitbucket not supported
- **AGENTS.md** → Jules reads from repo root for context
- **ALWAYS validate before applying changes**

## PR Review & Feedback Loop

This section covers the detailed workflow for managing Jules PRs through the review cycle, including automated reviewer tracking and feedback piping.

### Issues are resolved when

- The review comment has been marked as **resolved** in GitHub (clicked checkmark), OR
- The concern is **struck through** in the PR (~~text~~)

### Matching Jules Sessions to PRs

To see which PRs Jules created in its last run:

1. Get Jules sessions: `jules remote list --session`
2. Get recent PRs: `gh search prs dzackgarza -L 20`
3. Compare side-by-side — match by repo and title similarity

**Match criteria:**

- Same repository
- Similar title (session description → PR title)
- Timing (session completed ~PR created)

### Qodo Review Resolution

Qodo automatically re-analyzes the PR when new commits are pushed and strikes through issues that are now fixed. No manual "resolve" needed — it's commit-driven.

Workflow:

1. Push a commit that fixes the issue
2. Wait ~30-60 seconds for Qodo to re-scan
3. Qodo strikes through resolved issues automatically

### Sending Review Feedback to Jules

Use the `extract_unresolved_issues` module from the `git-guidelines` skill to pipe unresolved PR review issues back to Jules:

```bash
# Send unresolved issues summary
uv run --directory ~/ai/opencode/skills/git-guidelines/scripts/extract_unresolved_issues -m extract_unresolved_issues summarize <owner>/<repo>#<PR_NUM> | uvx git+https://github.com/dzackgarza/improved-jules-cli feedback SESSION_ID

# Send issues list
uv run --directory ~/ai/opencode/skills/git-guidelines/scripts/extract_unresolved_issues -m extract_unresolved_issues issues <owner>/<repo>#<PR_NUM> | uvx git+https://github.com/dzackgarza/improved-jules-cli feedback SESSION_ID
```

### Detailed Workflow (improved-jules-cli)

For the full end-to-end workflow using `improved-jules-cli`:

1. **Create Issue** — Use `git-guidelines` skill. Ensure clear title, specific outcomes, and context files referenced.
2. **Launch**:
   ```bash
   uvx git+https://github.com/dzackgarza/improved-jules-cli create ISSUE_URL --context PATH_TO_CONTEXT --prompt-slug sub-agents/jules-pr-body-contract
   ```
3. **Monitor & Poll**:
   ```bash
   uvx git+https://github.com/dzackgarza/improved-jules-cli status SESSION_ID
   uvx git+https://github.com/dzackgarza/improved-jules-cli watch-callback SESSION_ID "echo done"
   ```
4. **Wait for Reviews** — 5-10 minutes for bots (Qodo, Codacy, Gemini, kilo-code-bot).
5. **Check Issues** — Use `extract_unresolved_issues` from `git-guidelines` skill (see above).
6. **Send Feedback** — Pipe issues to Jules (see above).
7. **Repeat** steps 3-6 until no unresolved issues remain.
8. **Surface** — Present PR link: `uvx git+https://github.com/dzackgarza/improved-jules-cli pr SESSION_ID`

> TODO: describe exactly how to identify unresolved issues.
> TODO: describe exactly what counts as unresolved (isMinimized == false/null → unresolved, or non-crossed-out issues)
> TODO: describe exactly how to "resolve" (identify specific commit that fixed it OR identify new issue that addresses it, link commit as a reply in the conversation, mark conversation as "Resolved" manually)

---

## PR Contract (Mandatory for Jules-Initiated PRs)

For any PR initiated by Jules, a contract must be written **before** implementation begins, committed to the branch, and used as the authoritative source of truth for the PR body. Do not let the code define the task after the fact.

### Why a contract?

Automated GitHub reviewers have **no access to the original task** — only to the PR title, body, and commit messages. Jules controls all of that and is incentivized to make its work appear aligned with expectations, even when it is not. A contract written before implementation is the only reliable anchor for post-hoc comparison.

The contract must supply, in advance:

1. the intended outcome (externally checkable behavior),
2. the non-goals,
3. concrete, falsifiable acceptance criteria,
4. the specific evidence that will count as success,
5. the boundaries of the change,
6. the exact unresolved questions, if any.

### Phase 0: Create the contract before writing code

Before touching implementation:

```bash
mkdir -p .pr
$EDITOR .pr/PR_BODY.md
```

This file **must be committed before substantive implementation begins**.

Companion files:

```text
.pr/
  PR_BODY.md       # the contract — used as PR body source
  REVIEW_LOG.md    # per-item review tracking
  ACCEPTANCE_CHECKS.md  # optional detailed check list
```

### Required contents of `.pr/PR_BODY.md`

Write in plain, direct language with these sections.

#### 1. Problem statement

What exact failure, missing capability, or requirement is being addressed?

#### 2. Intended outcome

What must be true after this PR lands? Phrase as **externally checkable behavior**, not implementation structure.

Bad: _Adds a new abstraction for report generation._
Better: _Generating report X from input Y produces fields A, B, C with exact semantics Z._

#### 3. Non-goals

What is explicitly not being changed? Protects against scope explosion.

#### 4. Constraints

All binding constraints listed up front. Examples: exact arithmetic (not approximate), no mocks in tests, preserve existing API, no new dependencies, output must remain stable for downstream consumer Z.

#### 5. Acceptance criteria

Must be concrete, observable, and falsifiable.

Bad: _Tests added. Handles edge cases._
Better: _`compute_discriminant(L)` returns `-23` on the canonical fixture lattice. Invalid input raises `TypeError`. Existing command-line interface remains byte-for-byte unchanged on baseline fixture set._

#### 6. Evidence plan

State exactly what evidence will be provided. Examples: failing test first, then passing test; command output from real run on fixture X; diff proving no changes outside listed paths; benchmark numbers on the specified dataset.

#### 7. Change boundary

List the files or subsystems expected to change. Gives reviewers a prior on what collateral damage to reject.

#### 8. Open questions

List explicitly anything unresolved. Do not silently substitute your own answer.

### PR body template

Use this exact structure in `.pr/PR_BODY.md`:

```markdown
# Problem

<exact failure / missing capability / requirement>

# Intended outcome

<observable post-merge behavior>

# Non-goals

- ...

# Constraints

- ...

# Acceptance criteria

- [ ] ...
- [ ] ...

# Evidence plan

- failing test / command:
- passing test / command:
- end-to-end check:

# Change boundary

Expected touched files / subsystems:

- ...

# Open questions

- ...

# Review focus

Please check specifically:

- whether the acceptance criteria are sufficient,
- whether any goal has been swapped or relaxed,
- whether any changed file falls outside the declared boundary,
- whether verification would still pass on plausible junk output.
```

### Phase 1: TDD before implementation

Lock the target before implementation exists:

1. Write a failing verification artifact (automated test, reproducible failing command, or exact output comparison).
2. Confirm it fails for the intended reason.
3. Implement the narrowest change that should make it pass.
4. Re-run verification.
5. Record the result in the PR body.

**What does not count**: informal intention, a TODO list, a verbal claim that the bug exists, post-hoc explanations added after the code already passes, content-free checks like `is not None` or `len(x) > 0`.

### Phase 2: Keep the diff causally legible

Rules while implementing:

1. **No unrelated edits.** Do not rename nearby symbols, reformat unrelated files, update fixtures, or rewrite helpers unless required by the contract.
2. **No hidden goal substitution.** If the original goal becomes impossible, update the contract explicitly before changing direction.
3. **No structural completion as substitute for functional completion.** Do not add scaffolding, registries, wrappers, or documentation to create the appearance of completeness while leaving the core behavior stubbed.
4. **No fake success via fallbacks.** Do not hide failures with defaults, silent recovery, or plausible fabricated data.
5. **Prefer deletion and reuse over additive layers.** If a mature dependency already solves the problem, use it unless a listed constraint forbids that.

### Phase 3: Force the PR body from the contract file

Do not type the PR body interactively. Always use the tracked file.

Create the PR with:

```bash
gh pr create \
  --title "<concise outcome-focused title>" \
  --body-file .pr/PR_BODY.md \
  --draft
```

If the PR already exists, update it from the same file:

```bash
gh pr edit <PR_NUMBER> --body-file .pr/PR_BODY.md
```

**Rule:** Every time acceptance criteria, scope, or evidence changes, update `.pr/PR_BODY.md`, commit it, and re-publish the PR body from that file. The PR description is not a summary written after the work — it is a tracked interface between worker and reviewer.

### Phase 4: Record review feedback in REVIEW_LOG.md

Every actionable review item must be copied into `.pr/REVIEW_LOG.md` with required fields:

```markdown
## Review item <N>

**Source**: <PR review comment URL or line>
**Date**: <YYYY-MM-DD>
**Reviewer concern**: <exact statement>
**My response**: <what I will do>
**Commit**: <commit hash when addressed>
**Status**: open | addressed
```

This log is the audit trail that proves feedback was handled, not ignored.

### Responding to review moves

**Move A: The reviewer is correct about a code problem.** Strengthen the code, add or revise tests first if needed, then update the contract if acceptance criteria changed.

**Move B: The reviewer exposed missing or weak acceptance criteria.** Strengthen `.pr/PR_BODY.md`, add or revise tests first if needed, then update code.

**Move C: The reviewer identified that the contract itself is wrong.** Revise `.pr/PR_BODY.md` explicitly, commit that revision, then proceed with implementation changes.

**Illegal moves:**

- Silently keep the same direction while merely adding a local constraint
- Say "addressed" without changing the contract or the code
- Reinterpret the reviewer's feedback into something easier and solve that instead

### Review focus section

At the end of `.pr/PR_BODY.md`, always ask reviewers to check:

- whether the intended outcome is the right one,
- whether any acceptance criterion is missing, tautological, or implementation-defined,
- whether any file in the diff falls outside the declared boundary,
- whether any test would pass on plausible junk,
- whether any fallback hides failure instead of surfacing it,
- whether the code satisfies the problem or merely looks complete.
