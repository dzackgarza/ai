# Repository Management (Clone, Create, Fork, Settings, Releases)

Consolidated from the former `github-repo-management` skill.

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

if [ "$AUTH" = "gh" ]; then
  GH_USER=$(gh api user --jq '.login')
else
  GH_USER=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | python3 -c "import sys,json; print(json.load(sys.stdin)['login'])")
fi
```

If inside a repo:
```bash
REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

* * *

## 1. Cloning Repositories

```bash
git clone https://github.com/owner/repo-name.git
git clone --depth 1 https://github.com/owner/repo-name.git
git clone git@github.com:owner/repo-name.git
```

**With gh:** `gh repo clone owner/repo-name`

## 2. Creating Repositories

**With gh:**
```bash
gh repo create my-new-project --public --clone
gh repo create my-new-project --private --description "A useful tool" --license MIT --clone
gh repo create my-org/my-new-project --public --clone
gh repo create my-project --source . --public --push
```

**Without gh:**
```bash
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{"name": "my-new-project", "private": false, "auto_init": true}'

cd /path/to/existing/project
git init && git add . && git commit -m "Initial commit"
git remote add origin https://github.com/$GH_USER/my-new-project.git
git push -u origin main
```

## 3. Forking Repositories

```bash
gh repo fork owner/repo-name --clone
```

**Without gh:**
```bash
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo-name/forks
sleep 3
git clone https://github.com/$GH_USER/repo-name.git
cd repo-name
git remote add upstream https://github.com/owner/repo-name.git
```

### Keeping a Fork in Sync

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## 4. Repository Settings

```bash
gh repo edit --description "Updated description" --visibility public
gh repo edit --enable-wiki=false --enable-issues=true
gh repo edit --default-branch main
gh repo edit --add-topic "machine-learning,python"
```

## 5. Branch Protection

```bash
# View current protection
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/branches/main/protection

# Set up branch protection
curl -s -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/branches/main/protection \
  -d '{
    "required_status_checks": {"strict": true, "contexts": ["ci/test", "ci/lint"]},
    "required_pull_request_reviews": {"required_approving_review_count": 1}
  }'
```

## 6. Secrets Management (GitHub Actions)

```bash
gh secret set API_KEY --body "your-secret-value"
gh secret list
gh secret delete API_KEY
```

For `gh`-less environments, secrets require encryption with the repo's public key.
Recommend installing `gh` for secrets operations — dramatically simpler.

## 7. Releases

```bash
gh release create v1.0.0 --title "v1.0.0" --generate-notes
gh release create v2.0.0-rc1 --draft --prerelease
gh release create v1.0.0 ./dist/binary --title "v1.0.0" --notes "Release notes"
gh release list
gh release download v1.0.0 --dir ./downloads
```

## 8. GitHub Actions Workflows

```bash
gh workflow list
gh run list --limit 10
gh run view <RUN_ID>
gh run view <RUN_ID> --log-failed
gh run rerun <RUN_ID>
gh run rerun <RUN_ID> --failed
gh workflow run ci.yml --ref main
```

## 9. Gists

```bash
gh gist create script.py --public --desc "Useful script"
gh gist list
```

## Quick Reference

| Action | gh | git + curl |
| --- | --- | --- |
| Clone | `gh repo clone o/r` | `git clone https://github.com/o/r.git` |
| Create repo | `gh repo create name --public` | `curl POST /user/repos` |
| Fork | `gh repo fork o/r --clone` | `curl POST /repos/o/r/forks` + `git clone` |
| Edit settings | `gh repo edit --...` | `curl PATCH /repos/o/r` |
| Create release | `gh release create v1.0` | `curl POST /repos/o/r/releases` |
| List workflows | `gh workflow list` | `curl GET /repos/o/r/actions/workflows` |
| Rerun CI | `gh run rerun ID` | `curl POST /repos/o/r/actions/runs/ID/rerun` |
| Set secret | `gh secret set KEY` | `curl PUT /repos/o/r/actions/secrets/KEY` (+ encryption) |
