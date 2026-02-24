---
name: finding-or-downloading-new-skills
description: Use when asked to find, evaluate, or download new skills from skill marketplaces or repositories.
---

# Finding or Downloading New Skills

When asked to add or download new skills, follow this procedure:

## Critical Rule

ALWAYS use the download + unzip + copy methodology. NEVER reconstruct skills from web-fetched content, HTML, or summaries. Only download and copy raw files verbatim to preserve data integrity.

## Procedure

### 1. Identify the skills directory

Skills are stored in `~/skills` (which may be symlinked, e.g., `~/.kilocode/skills` → `~/skills`).

### 2. Create the skill directory

```bash
mkdir -p ~/skills/skill-name
```

For agent-specific skills, use:
- `~/skills-code/` for code mode
- `~/skills-architect/` for architect mode

### 3. Find the download URL

**LobeHub**: `https://market.lobehub.com/api/v1/skills/{skill-id}/download`

**GitHub**: Download raw files from `.claude/skills/` or `.kilocode/skills/` directories.

### 4. Download and extract

```bash
curl -fsSL "DOWNLOAD_URL" -o /tmp/skill-name.zip
unzip -o /tmp/skill-name.zip -d /tmp/skill-name-extract
```

For GitHub raw:
```bash
curl -fsSL "https://raw.githubusercontent.com/owner/repo/main/path/SKILL.md" -o ~/skills/skill-name/SKILL.md
```

### 5. Copy files verbatim

```bash
cp /tmp/skill-name-extract/SKILL.md ~/skills/skill-name/SKILL.md
# If bundled resources exist:
cp -r /tmp/skill-name-extract/* ~/skills/skill-name/
```

### 6. Verify

```bash
ls -la ~/skills/skill-name/
```

### 7. Confirm to the user

Inform the user the skill has been installed and note that they may need to restart their coding agent for it to be detected.

## Name Matching

The `name` field in SKILL.md frontmatter MUST match the directory name. If it doesn't, rename the directory or edit the frontmatter.
