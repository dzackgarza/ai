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
- **Installation Locations**: Most agent CLIs (Smithery, LobeHub, Claude Code, Codex, etc.) install skills to paths that are **symlinked** to the canonical OpenCode skills directory:
  - `~/.agents/skills/` → `~/ai/opencode/skills/`
  - `~/.openclaw/skills/` → `~/ai/opencode/skills/`
  - `./.claude/skills/` → `~/ai/opencode/skills/`
  - `./.agents/skills/` → `~/ai/opencode/skills/`

  Always check if the skill already exists in the canonical path before manually copying.

- **Post-Install Copy**: If CLI installs to a different path, copy to canonical path:
  ```bash
  cp -r ~/.agents/skills/<skill-name>/* ~/ai/opencode/skills/<skill-name>/
  ```
- **Verify Canonical Path**: Install/copy all skill content strictly into `~/ai/opencode/skills/skill-name/`.
- **Manual Installation**: If CLI fails, manually download raw files and place them in the canonical path.
- **Strict Fabrication Ban**: NEVER write or fabricate skill content from memory. Content must be fetched, verified, and saved using the `write` tool.

---

This skill covers three approaches:

1. **Smithery** - MCP server and skill discovery
2. **LobeHub Marketplace** - Large marketplace with 100,000+ skills via CLI
3. **Manual Download** - For skills from GitHub or custom repositories

## Locating Skills (Proven Techniques)

When the CLI search doesn't find a skill or you're having difficulty locating it, use these techniques:

### Direct URL Inspection

The LobeHub CLI search may not find skills by partial identifier. Instead, **webfetch the skill page directly** using the URL from the user's request:

```bash
# User provides: https://lobehub.com/skills/minimax-ai-skills-shader-dev
# Extract identifier from URL and fetch the page
webfetch https://lobehub.com/skills/minimax-ai-skills-shader-dev
```

The page content contains:

- The exact CLI install command with the correct identifier
- GitHub repository link
- Version and category information

### CLI Search Strategy

If direct URL inspection doesn't work, try broader search terms:

```bash
# Search with related keywords
npx -y @lobehub/market-cli skills search --q "shader" --output json
npx -y @lobehub/market-cli skills search --q "glsl" --output json

# Use JSON output for programmatic inspection
npx -y @lobehub/market-cli skills search --q "shader" --page-size 50 --output json
```

### Finding the Skill Identifier

The identifier format is typically `{author}-{repo}-{skill-name}`. After locating a skill:

1. Note the identifier from search results or web page
2. Install using: `npx -y @lobehub/market-cli skills install <identifier>`
3. Verify installation location matches canonical path

## Smithery

Smithery is the canonical tool for searching, inspecting, and installing MCP servers and agent skills.

### Searching & Viewing

Use Smithery to search or inspect a skill without manually downloading files first.

```bash
# Search by keyword
npx @smithery/cli skill search "pdf processing"

# View skill details/content without installing
npx @smithery/cli skill view <namespace>/<name>
```

### Installing

```bash
npx @smithery/cli skill add <namespace>/<name> -a opencode --global
```

The `--global` flag installs to `~/.agents/skills/` (symlinked to `~/ai/opencode/skills/`), which is the canonical OpenCode skills path. Available agent targets: `claude-code`, `cursor`, `codex`, `windsurf`, `opencode`, `github-copilot`, and 30+ others. Run `npx @smithery/cli skill agents` to list them.

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
3. **Verify name matching**: Ensure the `name` field in SKILL.md frontmatter matches the directory name. If not, edit the frontmatter:
   ```bash
   # Check current name
   grep "^name:" ~/ai/opencode/skills/<skill-name>/SKILL.md
   # Fix if needed using edit tool
   ```

## Manual Download

For skills not on LobeHub or custom repositories, use manual download:

### 1. Identify the skills directory

All skills live in `~/ai/opencode/skills/` (the git repo root).

### 2. Create the skill directory

```bash
mkdir -p ~/ai/opencode/skills/skill-name
```

### 3. Find the download URL

- **LobeHub API**: `https://market.lobehub.com/api/v1/skills/{skill-id}/download`
- **GitHub**: Download raw files from `.claude/skills/` or `.agents/skills/` directories

### 4. Download and extract

```bash
uvx --from httpie http --download --output /tmp/skill-name.zip GET "DOWNLOAD_URL"
unzip -o /tmp/skill-name.zip -d /tmp/skill-name-extract
cp -r /tmp/skill-name-extract/* ~/ai/opencode/skills/skill-name/
```

### 5. Verify

For skill validation and quality checks, see [creating-skills/SKILL.md](../creating-skills/SKILL.md), which includes a validation script and workflow.

## Name Matching

The `name` field in SKILL.md frontmatter MUST match the directory name. If it doesn't, rename the directory or edit the frontmatter.
