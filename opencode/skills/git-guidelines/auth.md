# GitHub Authentication

Consolidated from the former `github-auth` skill.

## Detection Flow

Run this first:

```bash
git --version
gh auth status 2>&1
```

1. `gh auth status` succeeds: authenticated, use `gh` for everything
2. `gh` installed but not authenticated: use "gh auth" method below
3. `gh` not installed: use "git-only" method below

* * *

## Git-Only Authentication (No gh, No sudo)

### Option A: HTTPS with Personal Access Token (Recommended)

**Step 1: Create a token**

Tell the user to go to: **https://github.com/settings/tokens**

- Click "Generate new token (classic)"
- Give it a name like "hermes-agent"
- Select scopes: `repo`, `workflow`, `read:org`
- Set expiration (90 days default)
- Copy the token

**Step 2: Configure git credential cache**

```bash
# Cache in memory for 8 hours — avoids plaintext disk storage
git config --global credential.helper 'cache --timeout=28800'
```

Then test:
```bash
git ls-remote https://github.com/<your-username>/<any-repo>.git
```
Username: your GitHub username. Password: paste the token (not your GitHub password).

**Do not use `credential.helper store`** — saves tokens in plaintext. Do not embed tokens in remote URLs.

**Step 3: Configure git identity**

```bash
git config --global user.name "Their Name"
git config --global user.email "their-email@example.com"
```

### Option B: SSH Key Authentication

```bash
# Check for existing keys
ls ~/.ssh/id_*.pub

# Generate if needed
ssh-keygen -t ed25519 -C "their-email@example.com" -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub
```

Tell user to add the public key at: **https://github.com/settings/keys**

```bash
# Test connection
ssh -T git@github.com
# Expected: "Hi <username>! You've successfully authenticated..."

# Rewrite HTTPS GitHub URLs to SSH automatically
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

* * *

## gh CLI Authentication

### Interactive Browser Login

```bash
gh auth login
# Select: GitHub.com → HTTPS → Login via browser
```

### Token-Based Login (Headless / SSH Servers)

```bash
echo "<THEIR_TOKEN>" | gh auth login --with-token
gh auth setup-git
```

### Verify

```bash
gh auth status
```

* * *

## Using the GitHub API Without gh

```bash
export GITHUB_TOKEN="<token>"

# Then use in curl calls:
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

### Auth Detection Pattern

```bash
if gh auth status 2>&1; then
  echo "AUTH_METHOD=gh"
elif [ -n "$GITHUB_TOKEN" ]; then
  echo "AUTH_METHOD=curl"
else
  echo "AUTH_METHOD=none"
  echo "Need authentication. See: gh auth login"
fi
```

* * *

## Troubleshooting

| Problem | Solution |
| --- | --- |
| `git push` asks for password | GitHub disabled password auth. Use a personal access token, or switch to SSH |
| `remote: Permission to X denied` | Token may lack `repo` scope — regenerate with correct scopes |
| `fatal: Authentication failed` | Cached credentials may be stale — run `git credential reject` then re-authenticate |
| `ssh: connect to host github.com port 22: Connection refused` | Try SSH over HTTPS port: add `Host github.com` with `Port 443` and `Hostname ssh.github.com` to `~/.ssh/config` |
| Multiple GitHub accounts | Use SSH with different keys per host alias in `~/.ssh/config` |
| `gh: command not found` + no sudo | Use git-only Method 1 above — no installation needed |
