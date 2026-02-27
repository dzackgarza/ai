# Agent Usage Guidelines

## Design Philosophy

This library provides **simple, composable tools** for intelligent agents to manage Zotero libraries. It is **NOT** meant to completely automate complex tasks.

> **"Composable tools for library quality checks. No automation. No truncation."**

## Key Principles

### 1. Atomic Operations
Each function does one thing well:
- `items_without_pdf()` → returns list of items
- `add_tags_to_item()` → adds tags to a single item
- `duplicate_dois()` → finds duplicate DOIs

### 2. Agent Composes Workflows
The library provides building blocks; the agent designs the workflow:

```python
from zotero_librarian import get_zotero, items_without_pdf, batch_add_tags

zot = get_zotero()

# Agent decides: find items without PDFs, tag first 10
no_pdf = items_without_pdf(zot)
batch_add_tags(zot, no_pdf[:10], ["needs-pdf"])
```

### 3. Human-in-the-Loop for Destructive Operations
Write tools intentionally avoid permanent destruction:
- `delete_item()` moves to trash (requires manual empty in Zotero UI)
- `delete_collection()` moves to trash (items preserved)
- No "permanent delete" functions exist

### 4. Returns Data, Doesn't Act On It
Read tools return complete data; the agent decides what to do:
- `items_missing_required_fields()` → returns list, doesn't fix them
- `duplicate_titles()` → returns duplicates, doesn't merge them
- `similar_tags()` → returns suggestions, doesn't merge them

### 5. Quality Check Questions → Tools
The library maps quality questions to tools (see `TODO.md`):

| Question | Tools to Use |
|----------|--------------|
| Can I find this? | `items_without_field()`, `items_not_in_collection()` |
| Is it complete? | `items_missing_required_fields()` |
| Is the PDF there? | `items_without_pdf()`, `attachment_info()` |
| Are there duplicates? | `duplicate_dois()`, `duplicate_titles()` |
| Is anything broken? | `validate_doi()`, `items_with_invalid_doi()` |
| Are names consistent? | `creator_name_variations()`, `journal_name_variations()` |

## Example Agent Patterns

### Pattern 1: Inspect → Report → Wait
```python
# Inspect
incomplete = list(items_missing_required_fields(zot, "journalArticle", ["volume", "pages"]))

# Report to user
for item in incomplete:
    print(f"{item['data']['title']}: missing volume/pages")

# Wait for user decision on how to proceed
```

### Pattern 2: Inspect → Propose → Confirm → Act
```python
# Inspect
dups = duplicate_dois(zot)

# Propose
for doi, items in dups.items():
    if len(items) > 1:
        print(f"Duplicate DOI {doi}: merge {items[0]['key']} into {items[1]['key']}?")

# After user confirms:
# Act
merge_items(zot, items[0]["key"], items[1]["key"])
```

### Pattern 3: Batch with Limits
```python
# Don't process entire library at once
no_pdf = items_without_pdf(zot)
batch_add_tags(zot, no_pdf[:20], ["needs-pdf"])  # First 20 only
```

## What This Library Is NOT

- ❌ Not an autonomous librarian
- ❌ Not a decision-maker
- ❌ Not a workflow engine
- ❌ Not a replacement for human judgment

## What This Library IS

- ✅ Infrastructure for agents
- ✅ Composable building blocks
- ✅ Data retrieval and modification primitives
- ✅ A toolkit that requires intelligence from the caller
