---
name: github-auth
description: "GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitHub, Authentication, Git, gh-cli, SSH, Setup]
    related_skills: [github-pr-workflow, github-code-review, github-issues, github-repo-management]
---
# GitHub Authentication Setup

This skill sets up authentication so the agent can work with GitHub repositories, PRs,
issues, and CI. It covers two paths:

- **`git` (always available)** — uses HTTPS personal access tokens or SSH keys

- **`gh` CLI (if installed)** — richer GitHub API access with a simpler auth flow

## Detection Flow

When a user asks you to work with GitHub, run this check first:

```bash
# Check what's available
git --version
gh auth status 2>&1
```

1. `gh auth status` succeeds: authenticated, use `gh` for everything
2. `gh` is installed but not authenticated: use “gh auth” method below
3. `gh` is not installed: use “git-only” method below

* * *

## Method 1: Git-Only Authentication (No gh, No sudo)

This works on any machine with `git` installed.
No root access needed.

### Option A: HTTPS with Personal Access Token (Recommended)

This is the most portable method — works everywhere, no SSH config needed.

**Step 1: Create a personal access token**

Tell the user to go to: **https://github.com/settings/tokens**

- Click “Generate new token (classic)”

- Give it a name like “hermes-agent”

- Select scopes:

  - `repo` (full repository access — read, write, push, PRs)

  - `workflow` (trigger and manage GitHub Actions)

  - `read:org` (if working with organization repos)

- Set expiration (90 days is a good default)

- Copy the token — it won’t be shown again

**Step 2: Configure git credential cache**

```bash
# Cache credentials in memory for 8 hours (28800 seconds)
# This avoids plaintext storage on disk.
git config --global credential.helper 'cache --timeout=28800'
```

Then do a test operation that triggers auth — git will prompt for credentials:
- Username: your GitHub username
- Password: paste the personal access token (not your GitHub password)

```bash
git ls-remote https://github.com/<your-username>/<any-repo>.git
```

After entering credentials once, they're cached in memory for the timeout duration.

**Do not use `credential.helper store`** — it saves tokens in plaintext to
`~/.git-credentials`. Do not embed tokens in remote URLs. Use the memory cache or `gh`
credential helper instead.

After entering credentials once, they’re saved and reused for all future operations.

**Alternative: cache helper (credentials expire from memory)**

```bash
# Cache in memory for 8 hours (28800 seconds) instead of saving to disk
git config --global credential.helper 'cache --timeout=28800'
```

**Step 3: Configure git identity**

```bash
# Required for commits — set name and email
git config --global user.name "Their Name"
git config --global user.email "their-email@example.com"
```

**Step 4: Verify**

```bash
# Test push access (this should work without any prompts now)
git ls-remote https://github.com/<their-username>/<any-repo>.git

# Verify identity
git config --global user.name
git config --global user.email
```

### Option B: SSH Key Authentication

Good for users who prefer SSH or already have keys set up.

**Step 1: Check for existing SSH keys**

```bash
ls ~/.ssh/id_*.pub
# If this returns "No such file or directory", no keys exist — proceed to Step 2.
```

**Step 2: Generate a key if needed**

```bash
# Generate an ed25519 key (modern, secure, fast)
ssh-keygen -t ed25519 -C "their-email@example.com" -f ~/.ssh/id_ed25519 -N ""

# Display the public key for them to add to GitHub
cat ~/.ssh/id_ed25519.pub
```

Tell the user to add the public key at: **https://github.com/settings/keys**

- Click “New SSH key”

- Paste the public key content

- Give it a title like “hermes-agent-<machine-name>”

**Step 3: Test the connection**

```bash
ssh -T git@github.com
# Expected: "Hi <username>! You've successfully authenticated..."
```

**Step 4: Configure git to use SSH for GitHub**

```bash
# Rewrite HTTPS GitHub URLs to SSH automatically
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

**Step 5: Configure git identity**

```bash
git config --global user.name "Their Name"
git config --global user.email "their-email@example.com"
```

* * *

## Method 2: gh CLI Authentication

If `gh` is installed, it handles both API access and git credentials in one step.

### Interactive Browser Login (Desktop)

```bash
gh auth login
# Select: GitHub.com
# Select: HTTPS
# Authenticate via browser
```

### Token-Based Login (Headless / SSH Servers)

```bash
echo "<THEIR_TOKEN>" | gh auth login --with-token

# Set up git credentials through gh
gh auth setup-git
```

### Verify

```bash
gh auth status
```

* * *

## Using the GitHub API Without gh

When `gh` is not available, you can still access the full GitHub API using `curl` with a
personal access token.
This is how the other GitHub skills implement their fallbacks.

### Setting the Token for API Calls

```bash
# Option 1: Export as env var (preferred — keeps it out of commands)
export GITHUB_TOKEN="<token>"

# Then use in curl calls:
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

### Auth Detection

Use this pattern at the start of any GitHub workflow:

```bash
# Prefer gh for all GitHub operations.
# Fall back to GITHUB_TOKEN env var for curl API calls.
if gh auth status 2>&1; then
  echo "AUTH_METHOD=gh"
elif [ -n "$GITHUB_TOKEN" ]; then
  echo "AUTH_METHOD=curl"
else
  echo "AUTH_METHOD=none"
  echo "Need to set up authentication first. See: gh auth login"
fi
```

* * *

## Troubleshooting

| Problem | Solution |
| --- | --- |
| `git push` asks for password | GitHub disabled password auth. Use a personal access token as the password, or switch to SSH |
| `remote: Permission to X denied` | Token may lack `repo` scope — regenerate with correct scopes |
| `fatal: Authentication failed` | Cached credentials may be stale — run `git credential reject` then re-authenticate |
| `ssh: connect to host github.com port 22: Connection refused` | Try SSH over HTTPS port: add `Host github.com` with `Port 443` and `Hostname ssh.github.com` to `~/.ssh/config` |
| Credentials not persisting | Check `git config --global credential.helper` — must be `store` or `cache` |
| Multiple GitHub accounts | Use SSH with different keys per host alias in `~/.ssh/config`, or per-repo credential URLs |
| `gh: command not found` + no sudo | Use git-only Method 1 above — no installation needed |
