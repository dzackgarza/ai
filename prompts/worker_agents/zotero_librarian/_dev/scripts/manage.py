#!/usr/bin/env python3
"""
Zotero Librarian - Command Line Tools

Well-documented scripts for common library tasks.
Each script is self-contained, readable, and adaptable.

Usage:
    python scripts/stats.py
    python scripts/find-duplicates.py
    python scripts/tag-needs-pdf.py

These are NOT automation tools. They are starting points for
intelligent agents to understand, modify, and execute with judgment.
"""

import sys
import os

# Add parent directory to path so we can import agents
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)  # _dev
root_dir = os.path.dirname(parent_dir)     # project root
sys.path.insert(0, root_dir)

from agents import ZoteroAgent


def print_header(title: str, emoji: str = "📚"):
    """Print a formatted section header."""
    print(f"\n{emoji} {title}")
    print("=" * 60)


def stats():
    """
    Show library statistics.
    
    Displays item counts, collection counts, attachment rates.
    Useful for getting a quick overview of library health.
    """
    print_header("Library Statistics", "📊")
    
    lib = ZoteroAgent()
    s = lib.library_stats()
    
    print(f"\n  Items:              {s['item_count']}")
    print(f"  Collections:        {s['collection_count']}")
    print(f"  Tags:               {s['tag_count']}")
    print(f"\n  Items with PDF:     {s['items_with_pdf']}")
    print(f"  Items without PDF:  {s['items_without_pdf']}")
    print(f"  Attachment rate:    {s['items_with_attachments']}/{s['item_count']}")
    print()


def quality_report():
    """
    Show all quality issues in the library.
    
    Groups issues by type with counts. Use specific find-* scripts
    to see details and take action.
    """
    print_header("Quality Report", "🔍")
    
    lib = ZoteroAgent()
    issues = lib.find_quality_issues()
    
    for issue_type, items in sorted(issues.items()):
        count = len(items)
        if count > 0:
            label = issue_type.replace("_", " ").title()
            print(f"  {count:4d}  {label}")
    
    total = sum(len(v) for v in issues.values())
    print(f"\n  Total issues: {total}")
    print()


def find_no_pdf():
    """
    Find items without PDF attachments.
    
    Shows first 50 items. Use tag-needs-pdf.py to tag them all.
    """
    print_header("Items Without PDF", "📄")
    
    lib = ZoteroAgent()
    items = lib.find_items_without_pdf()
    
    print(f"\n{len(items)} items without PDF:\n")
    
    for i, item in enumerate(items[:50]):
        key = item["key"]
        title = item["data"].get("title", "Untitled")
        print(f"  [{key}] {title[:60]}")
    
    if len(items) > 50:
        print(f"  ... and {len(items) - 50} more")
    
    print()


def find_duplicates():
    """
    Find duplicate titles.
    
    Groups items by title. Review and decide which to keep.
    Use lib.delete_item() to remove duplicates (moves to trash).
    """
    print_header("Duplicate Titles", "📋")
    
    lib = ZoteroAgent()
    dups = lib.find_duplicates_by_title()
    
    print(f"\n{len(dups)} groups of duplicates:\n")
    
    for i, (title, items) in enumerate(list(dups.items())[:20]):
        print(f"  {title[:50]}...")
        for item in items:
            date = item["data"].get("date", "no date")[:4]
            print(f"    [{item['key']}] ({date})")
        print()


def find_similar_tags():
    """
    Find similar tags (potential typos or variations).
    
    Uses string similarity to find tags that might be duplicates.
    Review and merge manually using lib.add_tags() and lib.remove_tags().
    """
    print_header("Similar Tags", "🏷️")
    
    lib = ZoteroAgent()
    similar = lib.find_similar_tags(threshold=0.8)
    
    print(f"\n{len(similar)} groups of similar tags:\n")
    
    for tag, variants in list(similar.items())[:20]:
        print(f"  {tag}:")
        for v in variants:
            print(f"    - {v}")
        print()


def list_collections():
    """
    List all collections with item counts.
    
    Sorted by item count (largest first).
    """
    print_header("Collections", "📁")
    
    lib = ZoteroAgent()
    colls = lib.list_collections()
    
    for c in sorted(colls, key=lambda x: -x["item_count"]):
        print(f"  {c['item_count']:4d}  {c['name']}")
    
    print()


def list_tags():
    """
    List all tags with frequency counts.
    
    Shows top 50 tags by usage.
    """
    print_header("Tags", "🏷️")
    
    lib = ZoteroAgent()
    tags = lib.list_tags()
    
    for tag, count in sorted(tags.items(), key=lambda x: -x[1])[:50]:
        print(f"  {count:4d}  {tag}")
    
    print()


def tag_needs_pdf():
    """
    Tag all items without PDF with "needs-pdf".
    
    Non-destructive: only adds tags, doesn't remove anything.
    Review results with find-needs-pdf.py first.
    """
    print_header("Tagging Items Without PDF", "🏷️")
    
    lib = ZoteroAgent()
    items = lib.find_items_without_pdf()
    
    print(f"\nTagging {len(items)} items with 'needs-pdf'...\n")
    
    for item in items:
        lib.add_tags(item["key"], ["needs-pdf"])
    
    print(f"✅ Done. Tagged {len(items)} items.")
    print()


def help():
    """Show available commands."""
    print(__doc__)
    print("\nAvailable commands:")
    print("  stats              - Library overview")
    print("  quality            - All quality issues")
    print("  find-no-pdf        - Items without PDF")
    print("  find-duplicates    - Duplicate titles")
    print("  find-similar-tags  - Similar tags (typos)")
    print("  list-collections   - All collections")
    print("  list-tags          - All tags")
    print("  tag-needs-pdf      - Tag items missing PDF")
    print()


def main():
    if len(sys.argv) < 2:
        help()
        return
    
    cmd = sys.argv[1]
    
    commands = {
        "stats": stats,
        "quality": quality_report,
        "find-no-pdf": find_no_pdf,
        "find-duplicates": find_duplicates,
        "find-similar-tags": find_similar_tags,
        "list-collections": list_collections,
        "list-tags": list_tags,
        "tag-needs-pdf": tag_needs_pdf,
        "help": help,
        "--help": help,
        "-h": help,
    }
    
    if cmd in commands:
        commands[cmd]()
    else:
        print(f"Unknown command: {cmd}")
        help()


if __name__ == "__main__":
    main()
