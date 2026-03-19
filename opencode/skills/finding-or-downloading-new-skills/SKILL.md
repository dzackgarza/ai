---
name: finding-or-downloading-new-skills
description: Use when asked to find, evaluate, or download new skills from skill marketplaces or repositories.
---

# Finding or Downloading New Skills

## Research & Acquisition Protocol

Follow this workflow for all skill acquisition tasks to ensure research depth and tool accuracy.

### 1. Research & Discovery

- **Check Tooling First**: Run `npx tool --help` or `tool --help` for every tool before concluding it lacks search/download capability.
- **Exhaustive Discovery**: If initial searches yield nothing, pivot search terms immediately. Do not conclude absence based on one failure.
- **Hunt the Raw Source**: Always locate the authoritative GitHub repository. Webfetch the **raw** `SKILL.md` file from `https://raw.githubusercontent.com/...` to bypass site-specific UI blockers or JS-rendering requirements.
- **Report Negatives**: If research is exhausted, report the gap using the Epistemic Integrity format:
  - **Searched**: [List sources/commands]
  - **Found**: [Summary of findings]
  - **Conclusion**: [Inference based on evidence]
  - **Confidence**: [High/Medium/Low]
  - **Gaps**: [Unsearched areas]

### 2. Acquisition & Installation

- **Use Official CLI**: Prefer native CLI tools for search/install when non-interactive flags exist.
- **Verify Canonical Path**: Install/copy all skill content strictly into `~/ai/skills/skill-name/`.
- **Manual Installation**: If CLI fails, manually download raw files and place them in the canonical path.
- **Strict Fabrication Ban**: NEVER write or fabricate skill content from memory. Content must be fetched, verified, and saved using the `write` tool.

---

This skill covers three approaches:

1. **Smithery** - MCP server and skill discovery
2. **LobeHub Marketplace** - Large marketplace with 100,000+ skills via CLI
3. **Manual Download** - For skills from GitHub or custom repositories

## Smithery

Smithery is the canonical tool for searching, inspecting, and installing MCP servers and agent skills.

### Searching & Viewing

Use Smithery to search or inspect a skill without manually downloading files first.

```bash
# Search by keyword
npx smithery skill search "pdf processing"

# View skill details/content without installing
npx -y @smithery/cli@latest skill view <namespace>/<name>
```

### Installing

```bash
npx @smithery/cli@latest skill add <namespace>/<name> -a universal -g
```

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

### After Installing

1. Read `SKILL.md` inside the installed directory.
2. Follow its instructions to complete the task.

## Manual Download

For skills not on LobeHub or custom repositories, use manual download:

### 1. Identify the skills directory

All skills live in `~/ai/skills/` (the git repo root).

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

## Name Matching

The `name` field in SKILL.md frontmatter MUST match the directory name. If it doesn't, rename the directory or edit the frontmatter.
