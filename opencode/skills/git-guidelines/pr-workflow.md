# PR Workflow (Branch → Commit → Push → Merge)

Consolidated from the former `github-pr-workflow` skill.

## 1. Branch Creation

```bash
git fetch origin
git checkout main && git pull origin main
git checkout -b feat/add-user-authentication
```

Naming: `feat/description`, `fix/description`, `refactor/description`, `docs/description`, `ci/description`.

## 2. Making Commits

Use the standard edit workflow (see SKILL.md → Edit Workflow), then:

```bash
git add src/auth.py src/models/user.py tests/test_auth.py
git commit -m "feat: add JWT-based user authentication

- Add login/register endpoints
- Add User model with password hashing
- Add unit tests for auth flow"
```

Commit types: `feat`, `fix`, `refactor`, `docs`, `test`, `ci`, `chore`, `perf`

## 3. Pushing and Creating a PR

```bash
git push -u origin HEAD
```

**With gh:**
```bash
# Externalize the finalized plan into a GitHub issue tree and milestone scope first.
# Prepare .pr/PR_BODY.md as a claim map for the selected issue set or subtree.
# See creating-prs.md for the admission gate and issue-linked claim-map format.
gh pr create \
  --title "feat: add JWT-based user authentication" \
  --body-file .pr/PR_BODY.md \
  --milestone "<milestone>" \
  --draft

# Later, after every claimed issue/proof item is complete and evidenced:
gh pr ready <PR_NUMBER>
gh pr comment <PR_NUMBER> --body '@codex review'
```

Options: `--draft`, `--reviewer user1,user2`, `--label "enhancement"`, `--base develop`

**Without gh:**
```bash
BRANCH=$(git branch --show-current)

jq -n \
  --arg title "feat: add JWT-based user authentication" \
  --rawfile body .pr/PR_BODY.md \
  --arg head "$BRANCH" \
  --arg base "main" \
  '{title: $title, body: $body, head: $head, base: $base}' \
  | curl -s -X POST \
      -H "Authorization: token $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github.v3+json" \
      https://api.github.com/repos/$OWNER/$REPO/pulls \
      -d @-
```

### Extracting Owner/Repo from Git Remote

```bash
REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

## 4. Monitoring CI Status

```bash
# One-shot check
gh pr checks

# Watch until all checks finish (polls every 10s)
gh pr checks --watch
```

**Without gh:**
```bash
SHA=$(git rev-parse HEAD)

curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Overall: {data['state']}\")
for s in data.get('statuses', []):
    print(f\"  {s['context']}: {s['state']} - {s.get('description', '')}\")"

# Also check GitHub Actions check runs
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/check-runs \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for cr in data.get('check_runs', []):
    print(f\"  {cr['name']}: {cr['status']} / {cr['conclusion'] or 'pending'}\")"
```

### Poll Until Complete

```bash
SHA=$(git rev-parse HEAD)
for i in $(seq 1 20); do
  STATUS=$(curl -s \
    -H "Authorization: token $GITHUB_TOKEN" \
    https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['state'])")
  echo "Check $i: $STATUS"
  if [ "$STATUS" = "success" ] || [ "$STATUS" = "failure" ] || [ "$STATUS" = "error" ]; then
    break
  fi
  sleep 30
done
```

## 5. Auto-Fixing CI Failures

### Step 1: Get Failure Details

**With gh:**
```bash
gh run list --branch $(git branch --show-current) --limit 5
gh run view <RUN_ID> --log-failed
```

**Without gh:**
```bash
BRANCH=$(git branch --show-current)
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/runs?branch=$BRANCH&per_page=5" \
  | python3 -c "
import sys, json
runs = json.load(sys.stdin)['workflow_runs']
for r in runs:
    print(f\"Run {r['id']}: {r['name']} - {r['conclusion'] or r['status']}\")"

RUN_ID=<run_id>
curl -s -L \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/logs \
  -o /tmp/ci-logs.zip
cd /tmp && unzip -o ci-logs.zip -d ci-logs && cat ci-logs/*.txt
```

### Step 2: Fix and Push

```bash
git add <fixed_files>
git commit -m "fix: resolve CI failure in <check_name>"
git push
```

### Step 3: Verify

Re-check CI status using the commands from Section 4 above.

> CI failures and PR review comments are different.
> CI failures can be fixed mechanically after root-cause diagnosis.
> Review comments must first be routed to `pr-feedback-triage`.
> Do not auto-fix review comments merely because they are unresolved.

### Auto-Fix Loop Pattern

1. Check CI status → identify failures
2. Read failure logs → understand the error
3. Fix the code
4. `git add <modified files> && git commit -m "fix: ..." && git push`
5. Wait for CI → re-check status
6. Repeat if still failing (up to 3 attempts, then ask the user)

## 6. Merging

**With gh:**
```bash
# Squash merge + delete branch
gh pr merge --squash --delete-branch

# Enable auto-merge
gh pr merge --auto --squash --delete-branch
```

**Without gh:**
```bash
PR_NUMBER=<number>

# Merge via API (squash)
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/merge \
  -d "{
    \"merge_method\": \"squash\",
    \"commit_title\": \"feat: add user authentication (#$PR_NUMBER)\"
  }"

# Delete remote branch
BRANCH=$(git branch --show-current)
git push origin --delete $BRANCH

# Switch back to main
git checkout main && git pull origin main
git branch -d $BRANCH
```

Merge methods: `"merge"` (merge commit), `"squash"`, `"rebase"`.

## 7. Complete Workflow Example

```bash
# 1. Start from clean main
git checkout main && git pull origin main

# 2. Branch
git checkout -b fix/login-redirect-bug
# 3. Externalize the finalized plan into a GitHub issue tree and milestone scope.
#    Create or update .pr/PR_BODY.md as the issue-linked claim map before implementation
#    defines its own success criteria. Include Closes only for full claims and Refs for
#    parents, partial claims, and deferred work.
gh api repos/<OWNER>/<REPO>/milestones -f title="<milestone>" -f state=open -f description="<issue-tree scope>"
git add .pr/PR_BODY.md
git commit -m "Add PR tracking contract"
git push -u origin HEAD
gh pr create --title "fix: correct redirect URL after login" --body-file .pr/PR_BODY.md --milestone "<milestone>" --draft
gh pr view --json title,body,milestone,closingIssuesReferences,isDraft

# 4. (Agent makes code changes while the draft PR tracks open claim work)

# 5. Commit code changes
git add src/auth/login.py tests/test_login.py
git commit -m "fix: correct redirect URL after login"

# 6. Push implementation updates
git push -u origin HEAD

# 7. Republish the PR body as claim items are completed; keep deferred work out of checkboxes
gh pr edit --body-file .pr/PR_BODY.md --milestone "<milestone>"

# 8. Monitor CI while finishing claimed issue/proof work; deferred work stays out of checkboxes
gh pr checks --watch

# 9. Mark ready only after every claimed issue/proof item is complete and evidenced
gh pr ready <PR_NUMBER>
gh pr comment <PR_NUMBER> --body '@codex review'

# 10. Merge when green
gh pr merge --squash --delete-branch
```
