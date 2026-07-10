# Issue Management (View, Create, Manage, Triage)

Consolidated from the former `github-issues` skill.

Issue *filing rules and templates* are in SKILL.md (Issue Workflow section).
This reference covers the CLI mechanics for viewing, creating, managing, and triaging
issues. It is mechanics only.

For planning-tree issues — roadmap, phase, feature, story, proof obligation, or
implementation node — load and read `plan/references/externalization.md` before
creating or restructuring anything. The model it defines (single root roadmap issue,
story-shaped nodes at altitude, milestones scoped to subtree roots, proof obligations
in issue bodies) is not reconstructable from the CLI commands below.

## Setup

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
    fi
  fi
fi

REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

* * *

## 1. Viewing Issues

**With gh:**
```bash
gh issue list
gh issue list --state open --label "bug"
gh issue list --assignee @me
gh issue list --search "authentication error" --state all
gh issue view 42
```

**Without gh:**
```bash
# List open issues
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/issues?state=open&per_page=20" \
  | python3 -c "
import sys, json
for i in json.load(sys.stdin):
    if 'pull_request' not in i:
        labels = ', '.join(l['name'] for l in i['labels'])
        print(f\"#{i['number']:5}  {i['state']:6}  {labels:30}  {i['title']}\")"

# View a specific issue
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42 \
  | python3 -c "
import sys, json
i = json.load(sys.stdin)
labels = ', '.join(l['name'] for l in i['labels'])
print(f\"#{i['number']}: {i['title']}\")
print(f\"State: {i['state']}  Labels: {labels}\")
print(f\"\n{i['body']}\")"
```

## 2. Creating Issues

### `itree`-governed repositories

Create every work unit beneath an explicit grouping parent:

```bash
uvx --from git+https://github.com/dzackgarza/itree \
  itree new owner/repo "Login redirect ignores ?next= parameter" \
  --under owner/repo#<grouping-issue> \
  --body-file issue.md
gh issue edit <new-issue-number> --repo owner/repo --add-label "bug,backend" --add-assignee "username"
```

Omitting `--under` creates nothing. The command prints the existing work units and valid
grouping targets plus exact placement commands, then exits nonzero. Use that output to
choose a parent; never treat omission as default-root creation.

### Explicitly non-`itree`-governed repositories

**With `gh`:**

```bash
gh issue create \
  --title "Login redirect ignores ?next= parameter" \
  --body "## Description\nAfter logging in, users always land on /dashboard." \
  --label "bug,backend" \
  --assignee "username"
```

**Without `gh`:**

```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues \
  -d '{
    "title": "Login redirect ignores ?next= parameter",
    "body": "## Description\nAfter logging in, users always land on /dashboard.",
    "labels": ["bug", "backend"],
    "assignees": ["username"]
  }'
```

## 3. Managing Issues

### Add/Remove Labels

```bash
gh issue edit 42 --add-label "priority:high,bug"
gh issue edit 42 --remove-label "needs-triage"
```

**Without gh:**
```bash
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42/labels \
  -d '{"labels": ["priority:high", "bug"]}'

curl -s -X DELETE -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42/labels/needs-triage
```

### Assignment

```bash
gh issue edit 42 --add-assignee username
```

### Parent and Sub-Issues

Use native sub-issues for tree edges when the repository's GitHub surface supports them.
Do not use labels, title numbering, or dependencies to simulate ordinary parent/child
order.

For an `itree`-governed repository, create beneath a grouping parent and route later
placement changes through `itree`:

```bash
uvx --from git+https://github.com/dzackgarza/itree \
  itree new owner/repo "<child story or implementation node>" \
  --under owner/repo#42 \
  --body-file issue.md
uvx --from git+https://github.com/dzackgarza/itree itree attach owner/repo#42 owner/repo#43
uvx --from git+https://github.com/dzackgarza/itree itree move owner/repo#43 --under owner/repo#42
uvx --from git+https://github.com/dzackgarza/itree itree detach owner/repo#43
```

For an explicitly non-`itree`-governed repository, use the raw GitHub mechanics:

```bash
# Create a new child issue under a parent.
gh issue create --title "<child story or implementation node>" --body-file issue.md --parent 42

# Attach or detach existing issues.
gh issue edit 42 --add-sub-issue 43
gh issue edit 42 --remove-sub-issue 43

gh issue edit 43 --parent 42
gh issue edit 43 --remove-parent
```

### Dependencies

Use dependencies for blockers, not roadmap traversal order.

For an `itree`-governed repository, create the issue under its grouping parent first,
then add the dependency to the returned issue reference:

```bash
uvx --from git+https://github.com/dzackgarza/itree \
  itree new owner/repo "<blocked work>" \
  --under owner/repo#<grouping-issue> \
  --body-file issue.md
gh issue edit <new-issue-number> --repo owner/repo --add-blocked-by 41
```

For an explicitly non-`itree`-governed repository, raw creation remains available:

```bash
gh issue create --title "<blocked work>" --body-file issue.md --blocked-by 41
gh issue edit 42 --add-blocked-by 41 --add-blocking 44
gh issue edit 42 --remove-blocked-by 41 --remove-blocking 44
```

### Milestones

Milestones are delivery/progress buckets over issues and PRs. They do not replace the
issue tree.

In an `itree`-governed repository, create a GitHub Milestone and matching ledger beneath
an explicit grouping parent:

```bash
uvx --from git+https://github.com/dzackgarza/itree \
  itree milestone owner/repo "<milestone>" \
  --under owner/repo#<grouping-issue> \
  --body-file milestone.md \
  --issues owner/repo#42 owner/repo#43
```

Omitting `--under` creates nothing, prints placement guidance, and exits nonzero. The
named parent must be an open grouping issue.

Each `--issues` work unit moves beneath the new ledger in argument order and receives the
new milestone assignment. This is one preflighted orchestration command, not a GitHub
transaction. After any partial or indeterminate failure, preserve the reported
confirmed/untouched/indeterminate outcomes and reread live GitHub and `itree` state before
recovery.

The following raw edit changes the assignment on an existing issue. It does not create a
milestone or ledger and must not substitute for the governed command above:

```bash
gh issue edit 42 --milestone "<milestone>"
```

### Commenting

```bash
gh issue comment 42 --body "Investigated — root cause is in auth middleware."
```

### Closing and Reopening

```bash
gh issue close 42
gh issue close 42 --reason "not planned"
gh issue reopen 42
```

### Linking Issues to PRs

Issues close automatically when a PR merges with these keywords in the body:
```
Closes #42
Fixes #42
Resolves #42
```

## 4. Issue Triage Workflow

1. **List untriaged issues:**
```bash
gh issue list --label "needs-triage" --state open
```

2. **Read and categorize** each issue
3. **Apply labels and priority**
4. **Assign** if the owner is clear
5. **Comment with triage notes** if needed

## 5. Bulk Operations

```bash
# Close all issues with a specific label
gh issue list --label "wontfix" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {} --reason "not planned"
```

## Quick Reference

| Action | Command | Direct API endpoint |
| --- | --- | --- |
| List issues | `gh issue list` | `GET /repos/{o}/{r}/issues` |
| View issue | `gh issue view N` | `GET /repos/{o}/{r}/issues/N` |
| Create governed work unit | `itree new ... --under ...` | Owned by `itree` |
| Create governed milestone and ledger | `itree milestone ... --under ...` | Owned by `itree` |
| Create explicitly non-governed issue | `gh issue create ...` | `POST /repos/{o}/{r}/issues` |
| Add labels | `gh issue edit N --add-label ...` | `POST /repos/{o}/{r}/issues/N/labels` |
| Assign | `gh issue edit N --add-assignee ...` | `POST /repos/{o}/{r}/issues/N/assignees` |
| Add sub-issue | `gh issue edit PARENT --add-sub-issue CHILD` | Use GitHub CLI native sub-issue support |
| Add blocker | `gh issue edit N --add-blocked-by BLOCKER` | Use GitHub CLI native dependency support |
| Set milestone | `gh issue edit N --milestone "<milestone>"` | `PATCH /repos/{o}/{r}/issues/N` |
| Comment | `gh issue comment N --body ...` | `POST /repos/{o}/{r}/issues/N/comments` |
| Close | `gh issue close N` | `PATCH /repos/{o}/{r}/issues/N` |
| Search | `gh issue list --search "..."` | `GET /search/issues?q=...` |
