---
name: read-and-fetch-webpages
description: Use when fetching web pages where complete, untruncated content is required - for technical documentation, issue trackers, code repositories, or any detail-oriented work where AI summarization tools may miss critical information
---

# Read and Fetch Web Pages

## Overview

Default web fetch tools (WebFetch, AI-powered summarizers) return truncated or summarized content. This is good for skimming, deadly for detail-oriented work.

**Core principle:** When details matter, fetch the full page as text and read it directly.

**The problem:** AI web fetch tools optimize for brevity. They truncate long pages, summarize content, and miss critical details. Consider fetching a GitHub issue where the solution is in the last comment that closes the issue—the summarizer returns the first 3 comments and declares the issue "discusses X problem."

## When to Use

**Use when:**
- Fetching technical documentation where specific details matter
- Reading issue trackers, pull requests, or code reviews
- Fetching specifications, RFCs, or standards documents
- Reading research papers or academic content
- Any situation where missing a detail could change your understanding

**Don't use for:**
- Quick lookups where a summary is sufficient
- Browsing news articles or blog posts for general understanding
- When you explicitly want a summary rather than full content

## The Iron Law

```
NO DETAIL-ORIENTED WORK FROM SUMMARIZED WEB CONTENT
```

If the content matters, fetch it complete and read it yourself.

## Available Tools

### Text-Based Browsers (Preferred)

These convert HTML to readable text without AI summarization:

| Tool | Command | Best For |
|------|---------|----------|
| **w3m** | `w3m -dump URL` | General purpose, preserves structure |
| **elinks** | `elinks -dump URL` | Complex pages, handles JavaScript better |
| **links** | `links -dump URL` | Simple pages, fast |

### Installation

```bash
# Check what's available
which w3m elinks links

# Install if needed
sudo apt-get install w3m elinks links
```

## The Pattern

### Step 1: Check Available Tools

```bash
which w3m elinks links
```

Use whatever is available. `w3m` is most common.

### Step 2: Fetch to Temp File

```bash
w3m -dump "https://example.com/page" > /tmp/page-content.txt
```

**Why a file:**
- Pages can be thousands of lines
- You need to search, scroll, reference specific sections
- AI context windows may truncate anyway

### Step 3: Read the Content

```bash
# Check size first
wc -l /tmp/page-content.txt

# Read in chunks if large
head -100 /tmp/page-content.txt
tail -100 /tmp/page-content.txt

# Search for specific content
grep -n "keyword" /tmp/page-content.txt

# Read specific sections
sed -n '200,300p' /tmp/page-content.txt
```

### Step 4: Extract Relevant Sections

```bash
# Extract section between markers
sed -n '/## Installation/,/## Usage/p' /tmp/page-content.txt > /tmp/relevant-section.txt

# Extract all code blocks
grep -A5 "^\s*```" /tmp/page-content.txt > /tmp/code-examples.txt
```

## Examples

### Example 1: GitHub Issue

**Problem:** Need to understand a bug and its fix from a GitHub issue.

**Wrong approach:**
```
Use webfetch tool to summarize the issue.
```

Result: Gets first few comments, misses the actual fix in comment #47.

**Right approach:**
```bash
w3m -dump "https://github.com/owner/repo/issues/123" > /tmp/issue-123.txt
wc -l /tmp/issue-123.txt
# 847 lines

# Find the solution
grep -n -i "fix\|solution\|resolved" /tmp/issue-123.txt
# Line 723: "**Fixed in PR #125:** The issue was..."

# Read the fix
sed -n '720,750p' /tmp/issue-123.txt
```

### Example 2: Technical Documentation

**Problem:** Need specific API parameters from documentation.

**Wrong approach:**
```
WebFetch the documentation URL.
```

Result: Returns summary, misses edge cases and optional parameters.

**Right approach:**
```bash
w3m -dump "https://docs.example.com/api/reference" > /tmp/api-docs.txt

# Find the specific endpoint
grep -n -A20 "POST /api/users" /tmp/api-docs.txt

# Extract parameter table
sed -n '/## Parameters/,/## Example/p' /tmp/api-docs.txt
```

### Example 3: Research Paper (arXiv)

**Problem:** Need to understand methodology from a paper.

**Wrong approach:**
```
Use AI to summarize the paper.
```

Result: Gets abstract and high-level summary, misses methodology details.

**Right approach:**
```bash
# Use the read-arxiv-paper skill, which fetches the PDF
# Or for HTML versions:
w3m -dump "https://arxiv.org/html/2301.12345" > /tmp/paper.txt

# Find methodology section
grep -n -i "method\|approach\|algorithm" /tmp/paper.txt

# Extract relevant sections
sed -n '150,250p' /tmp/paper.txt
```

### Example 4: Stack Overflow

**Problem:** Need the accepted solution, not just the question.

**Wrong approach:**
```
WebFetch the Stack Overflow URL.
```

Result: Often returns question and top answer, but may miss comments with crucial corrections.

**Right approach:**
```bash
w3m -dump "https://stackoverflow.com/questions/12345/..." > /tmp/so-answer.txt

# Find accepted answer
grep -n -A30 "✓\|accepted\|solution" /tmp/so-answer.txt

# Check for corrections in comments
grep -n -B2 -A5 "comment" /tmp/so-answer.txt
```

## Common Failure Modes

| Failure | Prevention |
|---------|------------|
| Trusting AI summary of technical content | Always fetch full text for detail-oriented work |
| Missing content in comments/footnotes | Use grep to search entire page, not just main content |
| Not checking page length | Run `wc -l` first to understand scope |
| Reading only the beginning | Check the end too—solutions often appear late |
| Assuming first result is correct | For issues/PRs, read chronologically to understand evolution |

## Anti-Patterns

### ❌ Relying on WebFetch for Technical Content

```
WebFetch: "This GitHub issue discusses a memory leak problem."

Reality: The issue has 89 comments. Comment #67 contains the actual fix.
Comment #82 explains why the fix doesn't work for edge case X.
You missed both.
```

### ❌ Not Checking What Was Truncated

```
AI WebFetch returns 2000 characters of a 50,000 character page.

You don't know what you don't know. The missing 48,000 characters
might contain the exact information you need.
```

### ❌ Assuming Summary Equals Understanding

```
Summary: "The documentation covers installation and usage."

What you needed: The specific environment variable that must be set
before installation, mentioned only in the "Troubleshooting" section
at the bottom of the page.
```

## When AI WebFetch Is Acceptable

AI-powered web fetch is fine when:
- You're exploring and don't need precision
- The page is short enough that truncation isn't an issue
- You explicitly want a summary, not details
- You're checking if a page is worth reading in full

**Rule of thumb:** If being wrong about the content would cause problems, fetch it complete.

## Comparison: Tools for Web Content

| Tool | Complete Content | Searchable | Preserves Structure | Best Use |
|------|-----------------|------------|---------------------|----------|
| **w3m -dump** | ✅ Yes | ✅ Yes (grep) | ✅ Yes | Technical docs, issues |
| **elinks -dump** | ✅ Yes | ✅ Yes (grep) | ✅ Yes | Complex pages |
| **WebFetch (AI)** | ❌ Summarized | ❌ No | ❌ Reformatted | Skimming, exploration |
| **Browser (manual)** | ✅ Yes | ✅ Yes (Ctrl+F) | ✅ Yes | When you need visual layout |

## The Bottom Line

**For detail-oriented work, AI summarization is not your friend.**

Fetch the page as text. Read it yourself. Search for what you need.

The extra 30 seconds prevents hours of debugging based on incomplete information.
