"""
Zotero Librarian - Agent Interface

High-level interface for AI agents to interact with Zotero library.
All functions work without truncation and return complete data.

Usage:
    from agents import ZoteroAgent
    
    agent = ZoteroAgent()
    
    # Library overview
    stats = agent.library_stats()
    issues = agent.find_quality_issues()
    
    # Search and query
    items = agent.find_items_without_pdf()
    duplicates = agent.find_duplicate_titles()
    
    # Fix issues
    agent.add_tags_to_item("ABC123", ["needs-review"])
"""

from typing import Any, Optional
import sys
import os

# Add _dev/src to path for imports
_dev_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_dev", "src")
sys.path.insert(0, _dev_path)

from zotero_librarian import (
    get_zotero,
    count_items,
    all_items,
    get_item,
    get_collections,
    all_tags,
    items_without_pdf,
    items_without_attachments,
    items_without_tags,
    items_not_in_collection,
    items_without_abstract,
    items_missing_required_fields,
    duplicate_dois,
    duplicate_titles,
    creator_name_variations,
    journal_name_variations,
    similar_tags,
    items_with_invalid_doi,
    items_with_placeholder_titles,
    attachment_info,
    add_tags_to_item,
    remove_tags_from_item,
    move_item_to_collection,
    add_item_to_collection,
    remove_item_from_collection,
    update_item_fields,
    delete_item,
)


class ZoteroAgent:
    """High-level agent interface for Zotero library management.
    
    All methods return complete, untruncated data.
    No automation - all changes require explicit agent action.
    """
    
    def __init__(self):
        """Initialize Zotero agent with local API connection."""
        self.zot = get_zotero()
        self._item_cache: dict[str, Any] = {}
    
    # =========================================================================
    # Library Overview
    # =========================================================================
    
    def library_stats(self) -> dict[str, Any]:
        """Get library overview statistics.
        
        Returns:
            Dict with item_count, collection_count, tag_count, attachment_stats
        """
        collections = get_collections(self.zot)
        tags = all_tags(self.zot)
        
        # Count attachments
        total_items = 0
        items_with_pdf = 0
        items_with_attachments = 0
        
        for item in all_items(self.zot):
            total_items += 1
            children = getattr(item, '_children', [])
            has_pdf = any(
                c['data'].get('contentType') == 'application/pdf'
                for c in children
                if c['data']['itemType'] == 'attachment'
            )
            has_attachment = any(
                c['data']['itemType'] == 'attachment'
                for c in children
            )
            if has_pdf:
                items_with_pdf += 1
            if has_attachment:
                items_with_attachments += 1
        
        return {
            "item_count": total_items,
            "collection_count": len(collections),
            "tag_count": len(tags),
            "items_with_pdf": items_with_pdf,
            "items_with_attachments": items_with_attachments,
            "items_without_pdf": total_items - items_with_pdf,
        }
    
    def find_quality_issues(self) -> dict[str, list[Any]]:
        """Find all quality issues in library.
        
        Returns:
            Dict mapping issue type to list of affected items
        """
        return {
            "missing_pdf": list(items_without_pdf(self.zot)),
            "missing_attachments": list(items_without_attachments(self.zot)),
            "missing_tags": list(items_without_tags(self.zot)),
            "not_in_collection": list(items_not_in_collection(self.zot)),
            "missing_abstract": list(items_without_abstract(self.zot)),
            "duplicate_dois": list(duplicate_dois(self.zot).values()),
            "duplicate_titles": list(duplicate_titles(self.zot).values()),
            "invalid_dois": list(items_with_invalid_doi(self.zot)),
            "placeholder_titles": list(items_with_placeholder_titles(self.zot)),
        }
    
    # =========================================================================
    # Search and Query
    # =========================================================================
    
    def find_items_without_pdf(self) -> list[dict]:
        """Find all items without PDF attachments."""
        return items_without_pdf(self.zot)
    
    def find_items_without_tags(self) -> list[dict]:
        """Find all items without tags."""
        return list(items_without_tags(self.zot))
    
    def find_items_not_in_collection(self) -> list[dict]:
        """Find all items not filed in any collection."""
        return list(items_not_in_collection(self.zot))
    
    def find_duplicates_by_title(self) -> dict[str, list[dict]]:
        """Find items with duplicate titles.
        
        Returns:
            Dict mapping title to list of duplicate items
        """
        return duplicate_titles(self.zot)
    
    def find_duplicates_by_doi(self) -> dict[str, list[dict]]:
        """Find items with duplicate DOIs.
        
        Returns:
            Dict mapping DOI to list of duplicate items
        """
        return duplicate_dois(self.zot)
    
    def find_name_variations(self) -> dict[str, list[str]]:
        """Find author names with format variations.
        
        Returns:
            Dict mapping last name to list of name variations
        """
        return creator_name_variations(self.zot)
    
    def find_journal_variations(self) -> dict[str, list[str]]:
        """Find journal name variations.
        
        Returns:
            Dict mapping normalized name to list of variations
        """
        return journal_name_variations(self.zot)
    
    def find_similar_tags(self, threshold: float = 0.8) -> dict[str, list[str]]:
        """Find similar tags (potential duplicates/typos).
        
        Args:
            threshold: Similarity threshold (0.0-1.0)
            
        Returns:
            Dict mapping tag to list of similar tags
        """
        return similar_tags(self.zot, threshold)
    
    def get_item(self, item_key: str) -> dict:
        """Get single item by key.
        
        Args:
            item_key: Zotero item key
            
        Returns:
            Complete item dict with metadata and children
        """
        if item_key not in self._item_cache:
            self._item_cache[item_key] = get_item(self.zot, item_key)
        return self._item_cache[item_key]
    
    def get_attachments(self, item_key: str) -> list[dict]:
        """Get attachment info for an item.
        
        Args:
            item_key: Zotero item key
            
        Returns:
            List of attachment info dicts
        """
        return attachment_info(self.zot, item_key)
    
    # =========================================================================
    # Write Operations
    # =========================================================================
    
    def add_tags(self, item_key: str, tags: list[str]) -> dict:
        """Add tags to an item.
        
        Args:
            item_key: Zotero item key
            tags: List of tag strings to add
            
        Returns:
            API response dict
        """
        self._item_cache.pop(item_key, None)  # Invalidate cache
        return add_tags_to_item(self.zot, item_key, tags)
    
    def remove_tags(self, item_key: str, tags: list[str]) -> dict:
        """Remove tags from an item.
        
        Args:
            item_key: Zotero item key
            tags: List of tag strings to remove
            
        Returns:
            API response dict
        """
        self._item_cache.pop(item_key, None)
        return remove_tags_from_item(self.zot, item_key, tags)
    
    def move_to_collection(self, item_key: str, collection_key: str) -> dict:
        """Move item to a collection (removes from other collections).
        
        Args:
            item_key: Zotero item key
            collection_key: Target collection key
            
        Returns:
            API response dict
        """
        self._item_cache.pop(item_key, None)
        return move_item_to_collection(self.zot, item_key, collection_key)
    
    def add_to_collection(self, item_key: str, collection_key: str) -> dict:
        """Add item to a collection (keeps existing collections).
        
        Args:
            item_key: Zotero item key
            collection_key: Target collection key
            
        Returns:
            API response dict
        """
        self._item_cache.pop(item_key, None)
        return add_item_to_collection(self.zot, item_key, collection_key)
    
    def remove_from_collection(self, item_key: str, collection_key: str) -> dict:
        """Remove item from a collection.
        
        Args:
            item_key: Zotero item key
            collection_key: Collection key to remove from
            
        Returns:
            API response dict
        """
        self._item_cache.pop(item_key, None)
        return remove_item_from_collection(self.zot, item_key, collection_key)
    
    def update_fields(self, item_key: str, fields: dict[str, Any]) -> dict:
        """Update fields on an item.
        
        Args:
            item_key: Zotero item key
            fields: Dict of field names and values
            
        Returns:
            API response dict
        """
        self._item_cache.pop(item_key, None)
        return update_item_fields(self.zot, item_key, fields)
    
    def delete_item(self, item_key: str) -> dict:
        """Move item to trash (does not permanently delete).
        
        Args:
            item_key: Zotero item key
            
        Returns:
            API response dict
        """
        self._item_cache.pop(item_key, None)
        return delete_item(self.zot, item_key)
    
    # =========================================================================
    # Collections and Tags
    # =========================================================================
    
    def list_collections(self) -> list[dict]:
        """Get all collections with item counts.
        
        Returns:
            List of dicts with key, name, item_count
        """
        return get_collections(self.zot)
    
    def list_tags(self) -> dict[str, int]:
        """Get all tags with frequency counts.
        
        Returns:
            Dict mapping tag to count
        """
        return all_tags(self.zot)
    
    def find_empty_collections(self) -> list[dict]:
        """Find collections with no items.
        
        Returns:
            List of empty collection dicts
        """
        return [c for c in self.list_collections() if c["item_count"] == 0]
    
    def find_single_item_collections(self) -> list[dict]:
        """Find collections with exactly one item.
        
        Returns:
            List of single-item collection dicts
        """
        return [c for c in self.list_collections() if c["item_count"] == 1]


# =============================================================================
# Convenience functions (module-level)
# =============================================================================

def agent() -> ZoteroAgent:
    """Create new ZoteroAgent instance.
    
    Returns:
        New ZoteroAgent connected to local Zotero instance
    """
    return ZoteroAgent()


def quick_stats() -> dict[str, Any]:
    """Get quick library statistics.
    
    Returns:
        Dict with item_count, collection_count, tag_count
    """
    return ZoteroAgent().library_stats()


def quick_issues() -> dict[str, list[Any]]:
    """Find all quality issues.
    
    Returns:
        Dict mapping issue type to affected items
    """
    return ZoteroAgent().find_quality_issues()
