# Code Review (Performing Reviews)

Consolidated from the former `github-code-review` skill.

> This skill is for *performing* code reviews and generating review feedback.
> For consuming, triaging, or acting on existing review comments, use `pr-feedback-triage` instead.

## 1. Reviewing Local Changes (Pre-Push)

```bash
# Staged changes
git diff --staged

# All changes vs main
git diff main...HEAD

# File names only
git diff main...HEAD --name-only

# Stat summary
git diff main...HEAD --stat
```

### Review Strategy

1. **Get the big picture:**
```bash
git diff main...HEAD --stat
git log main..HEAD --oneline
```

2. **Review file by file** — use `read_file` for full context:
```bash
git diff main...HEAD -- src/auth/login.py
```

3. **Check for common issues:**
```bash
# Debug statements, TODOs, console.logs
git diff main...HEAD | grep -n "print(\|console\.log\|TODO\|FIXME\|HACK\|XXX\|debugger"

# Large files accidentally staged
git diff main...HEAD --stat | sort -t'|' -k2 -rn | head -10

# Secrets or credential patterns
git diff main...HEAD | grep -in "password\|secret\|api_key\|token.*=\|private_key"

# Merge conflict markers
git diff main...HEAD | grep -n "<<<<<<\|>>>>>>\|======="
```

4. **Present structured feedback.**

### Review Output Format

```
## Code Review Summary

### Critical
- **<file>:<line>** — <Critical finding>. Suggestion: <Remediation>.

### Warnings
- **<file>:<line>** — <Warning description>.

### Suggestions
- **<file>:<line>** — <Suggestion description>.

### Looks Good
- <What looks good>
```

* * *

## 2. Reviewing a Pull Request on GitHub

Before reviewing the diff, inspect the live PR body.
If it does not contain one nested task-tree tracker, the PR is not review-ready.
Request changes or leave a blocking comment asking the author to normalize the body before substantive review.

Required body shape:

```md
- [ ] <Milestone or goal>
  - [ ] <Workstream or phase>
    - [ ] <Task>
      - [ ] <Subtask or proof obligation>
```

Checked lines must include same-line proof such as `Proof commit: <sha>`. Comments must not contain competing checkbox lists.

### View PR Details

**With gh:**
```bash
gh pr view 123
gh pr diff 123
gh pr diff 123 --name-only
```

**Without gh:**
```bash
PR_NUMBER=123

# PR details
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER

# Changed files
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/files \
  | python3 -c "
import sys, json
for f in json.load(sys.stdin):
    print(f\"{f['status']:10} +{f['additions']:-4} -{f['deletions']:-4}  {f['filename']}\")"
```

### Check Out PR Locally

```bash
git fetch origin pull/123/head:pr-123
git checkout pr-123

# View diff against base
git diff main...pr-123
```

**With gh (shortcut):** `gh pr checkout 123`

### Leave Comments

**General PR comment — with gh:**
```bash
gh pr comment 123 --body "Overall looks good, a few suggestions below."
```

**Single inline comment:**
```bash
HEAD_SHA=$(gh pr view 123 --json headRefOid --jq '.headRefOid')

gh api repos/$OWNER/$REPO/pulls/123/comments \
  --method POST \
  -f body="<Feedback detail>" \
  -f path="<file_path>" \
  -f commit_id="$HEAD_SHA" \
  -f line=<line_number> \
  -f side="RIGHT"
```

### Submit a Formal Review

```bash
gh pr review 123 --approve --body "LGTM!"
gh pr review 123 --request-changes --body "See inline comments."
gh pr review 123 --comment --body "Some suggestions, nothing blocking."
```

* * *

## 3. Review Delegation

All code evaluation rules, anti-slop guidelines, and validation-evasion auditing are delegated to canonical policy skills:

- **Code Review Policy & Bridge-Burning**: `reviewing-llm-code` and its red-flag catalogs
- **PR Guidance & Triage**: `pr-feedback-triage`
- **Proof & Test Obligations**: `test-guidelines`

Always consult `policy-index` to find the canonical skill for any code review, testing, or remediation question.

* * *

## 4. Pre-Push Review Workflow

1. `git diff main...HEAD --stat` — see scope of changes
2. `git diff main...HEAD` — read the full diff
3. For each changed file, use `read_file` for context
4. Apply the review checklist
5. Present findings (Critical / Warnings / Suggestions / Looks Good)
6. If critical issues found, offer to fix before push

* * *

## 5. PR Review Workflow (End-to-End)

### Step 1: Auth

Ensure authenticated (see `auth.md` in this skill).

### Step 2: Gather PR context

```bash
gh pr view 123
gh pr diff 123 --name-only
gh pr checks 123
```

### Step 3: Check out PR locally

```bash
git fetch origin pull/$PR_NUMBER/head:pr-$PR_NUMBER
git checkout pr-$PR_NUMBER
```

### Step 4: Read the diff

```bash
git diff main...HEAD --name-only
git diff main...HEAD -- path/to/file.py
```

### Step 5: Run automated checks

```bash
just test
```

### Step 6: Apply review checklist (see Section 3 above)

### Step 7: Post the review

```bash
# If no issues
gh pr review $PR_NUMBER --approve --body "Reviewed. Looks clean."

# If issues found
gh pr review $PR_NUMBER --request-changes --body "Found issues — see inline comments."
```

### Step 8: Also post a summary comment

```bash
gh pr comment $PR_NUMBER --body "$(cat <<'EOF'
## Code Review Summary

**Verdict: Changes Requested**

### Critical
- **<file>:<line>** — <Critical finding>

### Warnings
- **<file>:<line>** — <Warning>

### Suggestions
- **<file>:<line>** — <Suggestion>

### Looks Good
- <Positive feedback>
EOF
)"
```

### Step 9: Clean up

```bash
git checkout main
git branch -D pr-$PR_NUMBER
```

### Decision: Approve vs Request Changes vs Comment

- **Approve** — no critical or warning-level issues
- **Request Changes** — any critical or warning-level issue that should be fixed before merge
- **Comment** — observations and suggestions, nothing blocking
