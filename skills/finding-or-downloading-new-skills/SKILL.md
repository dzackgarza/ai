---
name: finding-or-downloading-new-skills
description: Use when asked to find, evaluate, or download new skills from skill marketplaces or repositories.
---

# Finding or Downloading New Skills

This skill covers three approaches:

1. **Context7 Skills Registry** - Search, install, and generate skills with trust scores and security scanning
2. **LobeHub Marketplace** - Large marketplace with 100,000+ skills via CLI
3. **Manual Download** - For skills from GitHub or custom repositories

## Context7 Skills Registry

Context7 maintains a searchable skills registry indexed from GitHub repositories. Skills are identified by repository path (e.g., `/anthropics/skills`) and skill name. Features include trust scores (0-10), prompt injection detection, and AI-powered skill generation.

### Searching

```bash
# Search by keyword
npx ctx7 skills search pdf
npx ctx7 skills search "react testing"

# Browse all skills in a repository
npx ctx7 skills info /anthropics/skills

# Get suggestions based on project dependencies
npx ctx7 skills suggest
```

### Installing

````bash
# Install interactively (prompts to pick)
npx ctx7 skills install /anthropics/skills

# Install a specific skill by name
npx ctx7 skills install /anthropics/skills pdf

# Install Skills — Canonical Directory Only

All skill installations must target the canonical directory `~/ai/skills/`. Do not use client-specific flags (e.g., `--claude`, `--cursor`) or custom directories. If the `--global` flag ensures installation into `~/ai/skills/`, it may be used. Otherwise, manually copy skills into this directory:

```bash
npx ctx7 skills install /anthropics/skills pdf --global
# Or manually copy the skill to ~/ai/skills
````

### Generating Custom Skills

```bash
# Requires login — opens interactive generation flow
npx ctx7 login
npx ctx7 skills generate
```

### Trust & Security

| Score    | Level  | Meaning                                 |
| -------- | ------ | --------------------------------------- |
| 7.0–10.0 | High   | Verified or well-established source     |
| 3.0–6.9  | Medium | Standard community contribution         |
| 0.0–2.9  | Low    | New or unverified — review before using |

For detailed instructions on skill validation, see [creating-skills/SKILL.md](../creating-skills/SKILL.md), which provides guidance and a validation workflow.

## LobeHub Marketplace

LobeHub Marketplace contains a wide variety of skills, including many for mathematical, scientific, and research agent workflows. Use the `@lobehub/market-cli` tool for discovery operations.

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

## Manual Download

For skills not on LobeHub or custom repositories, use manual download:

### 1. Identify the skills directory

All skills live in `~/ai/skills/` (the git repo root). This directory is symlinked into all harness-specific skill directories.

### 2. Create the skill directory

```bash
mkdir -p ~/ai/skills/skill-name
```

### 3. Find the download URL

- **LobeHub API**: `https://market.lobehub.com/api/v1/skills/{skill-id}/download`
- **GitHub**: Download raw files from `.claude/skills/` or `.agents/skills/` directories

### 4. Download and extract

```bash
curl -fsSL "DOWNLOAD_URL" -o /tmp/skill-name.zip
unzip -o /tmp/skill-name.zip -d /tmp/skill-name-extract
cp -r /tmp/skill-name-extract/* ~/ai/skills/skill-name/
```

### 5. Verify

For skill validation and quality checks, see [creating-skills/SKILL.md](../creating-skills/SKILL.md), which includes a validation script and workflow.

```bash
ls -la ~/ai/skills/skill-name/
```

## Name Matching

The `name` field in SKILL.md frontmatter MUST match the directory name. If it doesn't, rename the directory or edit the frontmatter.
