---
name: general-cleanup
description: Universal cleanup and organization skill for any file type. Provides file-type-agnostic workflows for organizing, deduplicating, and cleaning up files, directories, and repositories safely.
---

# General Cleanup

## Overview

A universal, file-type-agnostic skill for organizing and cleaning up any collection of files. Applies systematic workflows for organization, deduplication, dead content removal, and repository maintenance—regardless of file type (code, docs, configs, media, data, etc.).

## When to Use

- Files are disorganized or inconsistently named
- Duplicate files suspected across directories
- Unused or stale content needs identification
- Repository or directory has grown bloated
- Establishing organization conventions for new projects
- Periodic maintenance of any file collection

## When to Avoid

- Active work in progress that needs current structure
- Files with unclear ownership or no rollback plan
- Time-critical tasks (cleanup should be deliberate)

---

## Core Principles

### 1. Safety First

| Principle | Action |
|-----------|--------|
| Verify before delete | Confirm content is truly unused |
| Archive before remove | Move to archive folder first |
| Baseline state | Capture current state before changes |
| Validate after | Check nothing broke post-cleanup |

### 2. Organization Patterns

**Grouping strategies** (apply any that fit your context):

- **By type**: Extension, MIME type, format family
- **By purpose**: Source, config, output, documentation
- **By date**: Creation date, modification date, access date
- **By status**: Active, archived, deprecated, draft
- **By owner**: Author, team, department, project
- **By lifecycle**: In-progress, review, approved, obsolete

**Naming conventions**:

- Be consistent (pick one pattern and apply everywhere)
- Include dates in sortable format (YYYY-MM-DD)
- Use lowercase with hyphens or underscores
- Avoid spaces and special characters
- Include version numbers when applicable (v1, v2, or 1.0, 2.0)

### 3. Duplicate Detection

**Signals that files may be duplicates**:

- Same filename (case-insensitive)
- Same file size (within 1%)
- Same content hash (MD5, SHA256)
- Similar names with version suffixes (_v1, _copy, _final)
- Same content in different locations

**Before removing duplicates**:

1. Verify content is actually identical (hash comparison)
2. Check which copy is referenced/linked elsewhere
3. Keep the one in the more canonical location
4. Archive the other instead of deleting

---

## Workflows

### Workflow 1: Organize Disorganized Files

**Use when**: Files are scattered without clear structure

```
1. INVENTORY
   - List all files in target directory
   - Group by extension/type
   - Note total count and size

2. ANALYZE PATTERNS
   - What types of files exist?
   - What's the dominant use case?
   - Are there natural groupings?

3. DESIGN STRUCTURE
   - Propose folder hierarchy
   - Define naming conventions
   - Document the scheme

4. EXECUTE
   - Create folder structure
   - Move files to appropriate folders
   - Rename files to match conventions

5. VERIFY
   - Spot-check moved files
   - Ensure nothing is missing
   - Update any references/links
```

### Workflow 2: Remove Dead/Unused Content

**Use when**: Suspect files are no longer needed

```
1. IDENTIFY CANDIDATES
   - Files not modified in X months
   - Files in temp/cache/draft folders
   - Files with "old", "backup", "deprecated" in name
   - Files with no incoming references

2. VERIFY UNUSED
   - Search for references in other files
   - Check if regenerated automatically
   - Confirm no active processes depend on it
   - Ask stakeholders if uncertain

3. ARCHIVE (don't delete yet)
   - Move to archive folder with date stamp
   - Document what was archived and why
   - Set reminder to review in 30-90 days

4. DELETE (after archive period)
   - Confirm nothing broke during archive period
   - Permanently remove archived content
   - Update documentation
```

### Workflow 3: Deduplicate Files

**Use when**: Same content exists in multiple places

```
1. FIND DUPLICATES
   - Group files by size
   - Hash files with matching sizes
   - Compare content of same-hash files
   - List duplicate sets with locations

2. SELECT SURVIVOR
   - Keep file in most canonical location
   - Keep file with clearest name
   - Keep file with most references
   - Keep newest version (usually)

3. UPDATE REFERENCES
   - Find all links/imports pointing to duplicates
   - Update to point to survivor
   - Test that references work

4. ARCHIVE DUPLICATES
   - Move duplicates to archive
   - Document what was deduplicated
   - Delete after verification period
```

### Workflow 4: Repository/Directory Cleanup

**Use when**: Entire directory needs maintenance

```
1. BASELINE
   - Git status / current state snapshot
   - List directory structure
   - Note total size and file count
   - Run any existing tests/validations

2. SCAN FOR ISSUES
   - Dead content (unused files)
   - Duplicates (same content, different paths)
   - Disorganization (inconsistent structure)
   - Bloat (generated files, caches, artifacts)

3. PRIORITIZE
   - High confidence, low risk first
   - Generated/regeneratable files
   - Clearly unused content
   - Organizational improvements

4. EXECUTE BY CATEGORY
   - Clean generated files (safe to regenerate)
   - Archive dead content
   - Deduplicate files
   - Reorganize structure

5. VALIDATE
   - Run tests/builds
   - Check references still work
   - Verify nothing critical removed

6. DOCUMENT
   - What was cleaned
   - What was archived (and where)
   - New organization scheme
   - Follow-up items
```

---

## Safety Checklist

Before removing ANY file:

- [ ] Searched for references in other files
- [ ] Confirmed not generated by build/process
- [ ] Checked if anyone else uses it
- [ ] Verified not linked from documentation
- [ ] Archived first (not deleted directly)
- [ ] Can explain why it's safe to remove

---

## Report Format

Use this structure for cleanup reports:

```markdown
# Cleanup Report

## Summary
- Files reviewed: X
- Files organized: X
- Duplicates found: X sets (Y files total)
- Dead content: X files
- Space reclaimed: X MB

## Actions Taken

### Organized
| Original Path | New Path | Reason |
|---------------|----------|--------|

### Deduplicated
| Survivor | Removed Duplicates |
|----------|-------------------|

### Archived
| File | Archive Location | Reason |
|------|------------------|--------|

### Deleted
| File | Reason | Verified Unused |
|------|--------|-----------------|

## Validation
- [ ] Tests pass
- [ ] References updated
- [ ] Nothing critical broken

## Follow-up
- Items needing attention
- Future cleanup opportunities
```

---

## Common Patterns by Context

### Code Repositories
- Group by: component, layer, feature
- Archive: old builds, vendor deps, generated docs
- Watch for: dead functions, unused imports, old tests

### Document Collections
- Group by: topic, date, status, audience
- Archive: drafts, superseded versions, meeting notes
- Watch for: duplicate copies, outdated info

### Media Libraries
- Group by: date, event, type, project
- Archive: blurry shots, duplicates, raw exports
- Watch for: different resolutions of same image

### Data Files
- Group by: source, date range, type, pipeline stage
- Archive: intermediate results, failed runs
- Watch for: regenerated outputs, cached queries

### Config/Environments
- Group by: environment, component, scope
- Archive: deprecated envs, old schemas
- Watch for: hardcoded values, stale credentials

---

## Quick Commands

```bash
# Find duplicates by size
find . -type f -exec ls -l {} \; | sort -k5 -n

# Find duplicates by hash
find . -type f -exec md5sum {} \; | sort | uniq -d -w32

# Find files not modified in 90 days
find . -type f -mtime +90

# Find empty directories
find . -type d -empty

# Count files by extension
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

---

## Trigger Phrases

Use this skill when user says:

- "clean up this directory"
- "organize these files"
- "find duplicates"
- "remove unused files"
- "this is a mess, help me organize"
- "what can I delete?"
- "archive old files"
- "standardize naming"
- "repository cleanup"
- "file organization"
