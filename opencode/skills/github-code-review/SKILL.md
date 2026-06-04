---
name: github-code-review
description: "Review PRs: diffs, inline comments via gh or REST."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitHub, Code-Review, Pull-Requests, Git, Quality]
    related_skills: [github-auth, github-pr-workflow]
---
# GitHub Code Review

Perform code reviews on local changes before pushing, or review open PRs on GitHub.
Most of this skill uses plain `git` — the `gh`/`curl` split only matters for PR-level
interactions.

> [!IMPORTANT]
> **Authority and Routing Constraint**:
> This skill is strictly for *performing code reviews and generating review feedback comments*. It must NOT be used as the authority for consuming, triaging, or acting on review comments or CI failures.
> If you are acting on, resolving, or replying to existing review feedback or automated comments, you must load and use [pr-feedback-triage](file:///home/dzack/ai/opencode/skills/pr-feedback-triage/SKILL.md) instead.

## Prerequisites

- Authenticated with GitHub (see `github-auth` skill)

- Inside a git repository

* * *

## 1. Reviewing Local Changes (Pre-Push)

This is pure `git` — works everywhere, no API needed.

### Get the Diff

```bash
# Staged changes (what would be committed)
git diff --staged

# All changes vs main (what a PR would contain)
git diff main...HEAD

# File names only
git diff main...HEAD --name-only

# Stat summary (insertions/deletions per file)
git diff main...HEAD --stat
```

### Review Strategy

1. **Get the big picture first:**

```bash
git diff main...HEAD --stat
git log main..HEAD --oneline
```

2. **Review file by file** — use `read_file` on changed files for full context, and the
   diff to see what changed:

```bash
git diff main...HEAD -- src/auth/login.py
```

3. **Check for common issues:**

```bash
# Debug statements, TODOs, console.logs left behind
git diff main...HEAD | grep -n "print(\|console\.log\|TODO\|FIXME\|HACK\|XXX\|debugger"

# Large files accidentally staged
git diff main...HEAD --stat | sort -t'|' -k2 -rn | head -10

# Secrets or credential patterns
git diff main...HEAD | grep -in "password\|secret\|api_key\|token.*=\|private_key"

# Merge conflict markers
git diff main...HEAD | grep -n "<<<<<<\|>>>>>>\|======="
```

4. **Present structured feedback** to the user.

### Review Output Format

When reviewing local changes, present findings in this structure:

```
## Code Review Summary

### Critical
- **<file>:<line>** — <Critical finding description>.
  Suggestion: <Remediation step>.

### Warnings
- **<file>:<line>** — <Warning description>.

### Suggestions
- **<file>:<line>** — <Suggestion description>.

### Looks Good
- <What looks good, e.g. clean separation of concerns in the middleware layer>
```

* * *

## 2. Reviewing a Pull Request on GitHub

### View PR Details

**With gh:**

```bash
gh pr view 123
gh pr diff 123
gh pr diff 123 --name-only
```

**With git + curl:**

```bash
PR_NUMBER=123

# Get PR details
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \
  | python3 -c "
import sys, json
pr = json.load(sys.stdin)
print(f\"Title: {pr['title']}\")
print(f\"Author: {pr['user']['login']}\")
print(f\"Branch: {pr['head']['ref']} -> {pr['base']['ref']}\")
print(f\"State: {pr['state']}\")
print(f\"Body:\n{pr['body']}\")"

# List changed files
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/files \
  | python3 -c "
import sys, json
for f in json.load(sys.stdin):
    print(f\"{f['status']:10} +{f['additions']:-4} -{f['deletions']:-4}  {f['filename']}\")"
```

### Check Out PR Locally for Full Review

This works with plain `git` — no `gh` needed:

```bash
# Fetch the PR branch and check it out
git fetch origin pull/123/head:pr-123
git checkout pr-123

# Now you can use read_file, search_files, run tests, etc.

# View diff against the base branch
git diff main...pr-123
```

**With gh (shortcut):**

```bash
gh pr checkout 123
```

### Leave Comments on a PR

**General PR comment — with gh:**

```bash
gh pr comment 123 --body "Overall looks good, a few suggestions below."
```

**General PR comment — with curl:**

```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/$PR_NUMBER/comments \
  -d '{"body": "Overall looks good, a few suggestions below."}'
```

### Leave Inline Review Comments

**Single inline comment — with gh (via API):**

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

**Single inline comment — with curl:**

```bash
# Get the head commit SHA
HEAD_SHA=$(curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")

curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/comments \
  -d "{
    \"body\": \"<Feedback detail>\",
    \"path\": \"<file_path>\",
    \"commit_id\": \"$HEAD_SHA\",
    \"line\": <line_number>,
    \"side\": \"RIGHT\"
  }"
```

### Submit a Formal Review (Approve / Request Changes)

**With gh:**

```bash
gh pr review 123 --approve --body "LGTM!"
gh pr review 123 --request-changes --body "See inline comments."
gh pr review 123 --comment --body "Some suggestions, nothing blocking."
```

**With curl — multi-comment review submitted atomically:**

```bash
HEAD_SHA=$(curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")

curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/reviews \
  -d "{
    \"commit_id\": \"$HEAD_SHA\",
    \"event\": \"COMMENT\",
    \"body\": \"Code review from Hermes Agent\",
    \"comments\": [
      {\"path\": \"<file_path>\", \"line\": <line_number>, \"body\": \"<Feedback detail>\"}
    ]
  }"
```

Event values: `"APPROVE"`, `"REQUEST_CHANGES"`, `"COMMENT"`

The `line` field refers to the line number in the *new* version of the file.
For deleted lines, use `"side": "LEFT"`.

* * *

## 3. Review Checklist

When performing a code review (local or PR), do not invent local review standards or use generic code smell advice. All code evaluation rules, anti-slop guidelines, and validation-evasion auditing are delegated to the canonical policy skills:

- **Code Review Policy & Bridge-Burning**: Delegate to [reviewing-llm-code](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/SKILL.md) and its [Bridge-Burning Red Flags Catalog](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/references/bridge-burning-red-flags.md).
- **PR Guidance & Triage Rules**: Delegate to [pr-feedback-triage](file:///home/dzack/ai/opencode/skills/pr-feedback-triage/SKILL.md) and the global policy index.
- **Proof & Test Obligations**: Delegate to [test-guidelines](file:///home/dzack/ai/opencode/skills/test-guidelines/SKILL.md).

Always consult [policy-index](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md) to find the canonical source-of-truth skill for any code review, testing, or remediation question.


* * *

## 4. Pre-Push Review Workflow

When the user asks you to “review the code” or “check before pushing”:

1. `git diff main...HEAD --stat` — see scope of changes

2. `git diff main...HEAD` — read the full diff

3. For each changed file, use `read_file` if you need more context

4. Apply the checklist above

5. Present findings in the structured format (Critical / Warnings / Suggestions / Looks
   Good)

6. If critical issues found, offer to fix them before the user pushes

* * *

## 5. PR Review Workflow (End-to-End)

When the user asks you to “review PR #N”, “look at this PR”, or gives you a PR URL,
follow this recipe:

### Step 1: Set up environment

Ensure you are authenticated using the [github-auth](file:///home/dzack/ai/opencode/skills/github-auth/SKILL.md) skill.

### Step 2: Gather PR context

Get the PR metadata, description, and list of changed files to understand scope before
diving into code.

**With gh:**
```bash
gh pr view 123
gh pr diff 123 --name-only
gh pr checks 123
```

**With curl:**
```bash
PR_NUMBER=123

# PR details (title, author, description, branch)
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER

# Changed files with line counts
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER/files
```

### Step 3: Check out the PR locally

This gives you full access to `read_file`, `search_files`, and the ability to run tests.

```bash
git fetch origin pull/$PR_NUMBER/head:pr-$PR_NUMBER
git checkout pr-$PR_NUMBER
```

### Step 4: Read the diff and understand changes

```bash
# Full diff against the base branch
git diff main...HEAD

# Or file-by-file for large PRs
git diff main...HEAD --name-only
# Then for each file:
git diff main...HEAD -- path/to/file.py
```

For each changed file, use `read_file` to see full context around the changes — diffs
alone can miss issues visible only with surrounding code.

### Step 5: Run automated checks locally (if applicable)

Always run the repository's configured global Quality Control command (typically `just test` or `just qc`) to verify that changes pass checks and tests. Never run ad-hoc command runners (like `pytest`, `npm test`, or `ruff`) directly.

```bash
# Run global test/QC suite
just test
```

### Step 6: Apply the review checklist (Section 3)

Go through each category: Correctness, Security, Code Quality, Testing, Performance,
Documentation.

### Step 7: Post the review to GitHub

Collect your findings and submit them as a formal review with inline comments.

**With gh:**
```bash
# If no issues — approve
gh pr review $PR_NUMBER --approve --body "Reviewed by Hermes Agent. Code looks clean — good test coverage, no security concerns."

# If issues found — request changes with inline comments
gh pr review $PR_NUMBER --request-changes --body "Found a few issues — see inline comments."
```

**With curl — atomic review with multiple inline comments:**
```bash
HEAD_SHA=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")

# Build the review JSON — event is APPROVE, REQUEST_CHANGES, or COMMENT
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER/reviews \
  -d "{
    \"commit_id\": \"$HEAD_SHA\",
    \"event\": \"REQUEST_CHANGES\",
    \"body\": \"## Code Review Feedback\n\nIdentified issues during review. See inline comments.\",
    \"comments\": [
      {\"path\": \"<file_path>\", \"line\": <line_number>, \"body\": \"🔴 **Critical:** <Critical finding details>\"}
    ]
  }"
```

### Step 8: Also post a summary comment

In addition to inline comments, leave a top-level summary so the PR author gets the full
picture at a glance.
Use the review output format from `references/review-output-template.md`.

**With gh:**
```bash
gh pr comment $PR_NUMBER --body "$(cat <<'EOF'
## Code Review Summary

**Verdict: Changes Requested**

### 🔴 Critical
- **<file_path>:<line_number>** — <Critical finding details>

### ⚠️ Warnings
- **<file_path>:<line_number>** — <Warning details>

### 💡 Suggestions
- **<file_path>:<line_number>** — <Suggestion details>

### ✅ Looks Good
- <Positive feedback item>

---
*Reviewed by Hermes Agent*
EOF
)"
```

### Step 9: Clean up

```bash
git checkout main
git branch -D pr-$PR_NUMBER
```

### Decision: Approve vs Request Changes vs Comment

- **Approve** — no critical or warning-level issues, only minor suggestions or all clear

- **Request Changes** — any critical or warning-level issue that should be fixed before
  merge

- **Comment** — observations and suggestions, but nothing blocking (use when you’re
  unsure or the PR is a draft)
