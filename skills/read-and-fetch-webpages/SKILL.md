---
name: read-and-fetch-webpages
description: Get complete web page content - use tavily for search, w3m or CLI tools for reading pages
---

# Read and Fetch Web Pages

## Pattern

1. **Search first** → use tavily to find relevant pages
2. **Read pages** → use the appropriate tool below

## Tools

| Tool           | Command                                               | When                                       |
| -------------- | ----------------------------------------------------- | ------------------------------------------ |
| **tavily**     | `tavily_research` or `tavily_search`                  | Finding pages on a topic                   |
| **gh CLI**     | `gh issue view N --repo owner/repo --comments`        | GitHub issues/PRs                          |
| **curl + w3m** | `curl -sL --compressed URL \| w3m -dump -T text/html` | Reading any page                           |
| **uvx/ruff**   | `uvx ruff check .`                                    | Python linting (don't fetch docs for this) |

## Reading Pages

### GitHub

```bash
gh issue view 123 --repo owner/repo --comments
gh pr view 123 --repo owner/repo --comments
```

### Other sites

```bash
curl -sL --compressed "https://example.com/page" | w3m -dump -T text/html > /tmp/page.txt
grep -n "keyword" /tmp/page.txt
sed -n '100,150p' /tmp/page.txt
```

## Why Not webfetch

webfetch summarizes content and may miss critical details (comments, footnotes, late sections). Use w3m or CLI tools instead.

## When webfetch Is Acceptable

- Quick exploration, don't care about details
- Verifying a page exists
