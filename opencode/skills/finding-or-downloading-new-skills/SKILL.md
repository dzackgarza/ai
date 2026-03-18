---
name: finding-or-downloading-new-skills
description: Use when asked to find, evaluate, or download new skills from skill marketplaces or repositories.
---

# Finding or Downloading New Skills

## Mandatory Research Fail-Safe Protocol (DO NOT SKIP)

If a search yields nothing or a tool fails (e.g., interactive hang, web block):

1. **Never Give Up**: A single failed search is not evidence of absence.
2. **Announce Blockers**: IMMEDIATELY report tool/blocker failures; never work around them silently.
3. **Check `--help`**: Before assuming a tool limit, run `tool --help`. Smithery, for example, is a direct tool for search/download/install — learn its CLI.
4. **Hunt the Raw Source**: Always seek the original GitHub repository. Raw files (`raw.githubusercontent.com`) bypass most web blockers.
5. **No Memory-Writing (STRICTLY BANNED)**: You must NEVER fabricate content from memory.
   - You must fetch content using the `write` tool _only after_ fetching the raw source via `webfetch` (e.g., raw GitHub URL).
   - If research fails, report the gap using the Epistemic Integrity format below.
6. **Report Negatives**: Use the Epistemic Integrity format (Searched, Found, Conclusion, Confidence, Gaps).

---

This skill covers three approaches:

1. **Smithery** - MCP server and skill discovery
2. **LobeHub Marketplace** - Large marketplace with 100,000+ skills via CLI
3. **Manual Download** - For skills from GitHub or custom repositories

## Smithery

Smithery is NOT just a registry; it is a full CLI for searching, accessing, and downloading components.

### CLI Usage (Check `--help` first)

```bash
# Discover how to use search/download/install
npx smithery --help
npx smithery skill --help
```

### Searching & Downloading

```bash
# Search by keyword
npx smithery skill search "pdf processing"
```

Use `smithery` commands to directly search, access, and install components. Do not treat it as a UI-only tool.

### Canonical Fetching Workflow (Bypass UI/Blockers)

1. **Find Repo**: Identify the source GitHub repository for the skill.
2. **Fetch Content**: Use `webfetch` to pull the _raw_ `SKILL.md` from the repo's URL (`https://raw.githubusercontent.com/...`).
3. **Verify**: Ensure the fetched content is the canonical version.
4. **Save**: Use `write` to save the fetched content to `~/ai/skills/skill-name/SKILL.md`.

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
