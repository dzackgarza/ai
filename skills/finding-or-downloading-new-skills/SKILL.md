---
name: finding-or-downloading-new-skills
description: Use when asked to find, evaluate, or download new skills from skill marketplaces or repositories.
---

# Finding or Downloading New Skills

This skill covers using the **LobeHub Skills Marketplace** to automatically search for and install skills. The marketplace CLI handles authentication, download, and installation automatically.

## LobeHub Marketplace (Recommended)

The LobeHub Skills Marketplace is the world's largest skills marketplace with 100,000+ skills. Use the `@lobehub/market-cli` tool for all marketplace operations.

### Prerequisites: Registration

First-time use requires device registration:

```bash
npx -y @lobehub/market-cli register --source codex --name "your-agent-name"
```

This creates credentials at `~/.lobehub-market/credentials.json`. Registration is one-time.

### Searching for Skills

Search marketplace by keyword:

```bash
npx -y @lobehub/market-cli skills search --q "KEYWORD"
```

**Examples:**

```bash
# Search for PDF-related skills
npx -y @lobehub/market-cli skills search --q "pdf"

# Search for image processing
npx -y @lobehub/market-cli skills search --q "image editor"

# Search for API integration
npx -y @lobehub/market-cli skills search --q "api integration"
```

**Search options:**

| Option        | Description                                                               |
| ------------- | ------------------------------------------------------------------------- |
| `--q`         | Search keyword (required)                                                 |
| `--category`  | Filter by category                                                        |
| `--page`      | Page number (default: 1)                                                  |
| `--page-size` | Results per page (1-100, default: 20)                                     |
| `--sort`      | Sort by: createdAt, updatedAt, installCount, stars, forks, watchers, name |
| `--order`     | Sort order: asc, desc (default: desc)                                     |
| `--locale`    | Locale code (en-US, zh-CN, etc.)                                          |
| `--output`    | Output format: text (default) or json                                     |

### Installing Skills

Install a skill by identifier:

```bash
npx -y @lobehub/market-cli skills install <identifier>
```

**Examples:**

```bash
# Install a skill by name
npx -y @lobehub/market-cli skills install lobehub-pdf-tools

# Install for a specific agent (determines install path)
npx -y @lobehub/market-cli skills install lobehub-pdf-tools --agent open-claw
npx -y @lobehub/market-cli skills install lobehub-pdf-tools --agent claude-code
npx -y @lobehub/market-cli skills install lobehub-pdf-tools --agent codex
npx -y @lobehub/market-cli skills install lobehub-pdf-tools --agent cursor

# Install specific version
npx -y @lobehub/market-cli skills install lobehub-pdf-tools --version 1.0.0

# Install to global directory
npx -y @lobehub/market-cli skills install lobehub-pdf-tools --global

# Install to custom directory
npx -y @lobehub/market-cli skills install lobehub-pdf-tools --dir ~/my-skills
```

**Install paths by agent:**

| Agent       | Path                  | Scope  |
| ----------- | --------------------- | ------ |
| open-claw   | `~/.openclaw/skills/` | Global |
| claude-code | `./.claude/skills/`   | Local  |
| codex       | `./.agents/skills/`   | Local  |
| cursor      | `./.cursor/skills/`   | Local  |
| (default)   | `./.agents/skills/`   | Local  |
| --global    | `~/.agents/skills/`   | Global |

### After Installing

1. Read `SKILL.md` inside the installed directory
2. Follow its instructions to complete the task

### Rating & Feedback

Rate skills after use:

```bash
# Rate a skill (1-5)
npx -y @lobehub/market-cli skills rate <identifier> --score <1-5>

# Add a comment with rating
npx -y @lobehub/market-cli skills comment <identifier> -c "Your feedback" --rating <1-5>

# Read existing comments
npx -y @lobehub/market-cli skills comments <identifier>
```

**Rating guide:**

| Score | Meaning                                      |
| ----- | -------------------------------------------- |
| 5     | Excellent — solved the task perfectly        |
| 4     | Good — worked well with minor issues         |
| 3     | Okay — got the job done but could be clearer |
| 2     | Poor — partially worked, confusing           |
| 1     | Broken — didn't work, errors                 |

## Legacy: Manual Download

For skills not on LobeHub or custom repositories, use manual download:

### 1. Identify the skills directory

Skills are stored in `~/skills` (which may be symlinked).

### 2. Create the skill directory

```bash
mkdir -p ~/skills/skill-name
```

### 3. Find the download URL

- **LobeHub API**: `https://market.lobehub.com/api/v1/skills/{skill-id}/download`
- **GitHub**: Download raw files from `.claude/skills/` or `.agents/skills/` directories

### 4. Download and extract

```bash
curl -fsSL "DOWNLOAD_URL" -o /tmp/skill-name.zip
unzip -o /tmp/skill-name.zip -d /tmp/skill-name-extract
cp -r /tmp/skill-name-extract/* ~/skills/skill-name/
```

### 5. Verify

```bash
ls -la ~/skills/skill-name/
```

## Name Matching

The `name` field in SKILL.md frontmatter MUST match the directory name. If it doesn't, rename the directory or edit the frontmatter.
