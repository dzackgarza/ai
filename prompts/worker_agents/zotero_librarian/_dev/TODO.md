# Zotero Librarian - Feature Checklist

## ✅ Complete

### Read Tools
- [x] `all_items()` - Get all items
- [x] `all_items_by_type()` - Get items by type
- [x] `get_item()` - Get single item
- [x] `get_attachments()` - Get attachments for item
- [x] `get_notes()` - Get notes for item
- [x] `get_citations()` - Get citation relations
- [x] `get_collections()` - Get all collections
- [x] `all_tags()` - Get all tags with frequency
- [x] `count_items()` - Get total item count
- [x] `items_without_pdf()` - Find items without PDF
- [x] `items_without_attachments()` - Find items without any attachments
- [x] `items_without_tags()` - Find items without tags
- [x] `items_not_in_collection()` - Find unfiled items
- [x] `items_without_abstract()` - Find items without abstract
- [x] `items_missing_required_fields()` - Find incomplete items by type
- [x] `items_without_cites()` - Find items without "cites" relations
- [x] `items_without_cited_by()` - Find items without "citedBy" relations
- [x] `preprints_without_doi()` - Find preprints without DOI
- [x] `items_with_notes()` - Find items with notes
- [x] `empty_collections()` - Find empty collections
- [x] `single_item_collections()` - Find single-item collections
- [x] `duplicate_dois()` - Find duplicate DOIs
- [x] `duplicate_titles()` - Find duplicate titles
- [x] `creator_name_variations()` - Find author name inconsistencies
- [x] `journal_name_variations()` - Find journal name inconsistencies
- [x] `similar_tags()` - Find similar tags (potential duplicates)
- [x] `validate_doi()` - Validate DOI format
- [x] `validate_isbn()` - Validate ISBN format
- [x] `validate_issn()` - Validate ISSN format
- [x] `items_with_invalid_doi()` - Find invalid DOIs
- [x] `items_with_invalid_isbn()` - Find invalid ISBNs
- [x] `items_with_invalid_issn()` - Find invalid ISSNs
- [x] `items_with_broken_urls()` - Find malformed URLs
- [x] `items_with_placeholder_titles()` - Find placeholder titles
- [x] `attachment_info()` - Get detailed attachment info
- [x] `check_item_completeness()` - Check item against required fields
- [x] `search_by_title()` - Search items by title substring
- [x] `search_by_author()` - Search items by author name
- [x] `search_by_year()` - Filter items by exact year
- [x] `search_by_year_range()` - Filter items by year range
- [x] `search_by_collection()` - Get items in collection
- [x] `search_by_tag()` - Get items with specific tag
- [x] `search_advanced()` - Combined search with multiple filters

### Write Tools
- [x] `update_item_fields()` - Update fields on an item
- [x] `add_tags_to_item()` - Add tags to an item
- [x] `remove_tags_from_item()` - Remove tags from an item
- [x] `add_item_to_collection()` - Add item to collection
- [x] `move_item_to_collection()` - Move item to collection
- [x] `remove_item_from_collection()` - Remove item from collection
- [x] `attach_pdf()` - Attach PDF (metadata only)
- [x] `attach_url()` - Attach URL/link
- [x] `attach_note()` - Add note to item
- [x] `add_citation_relation()` - Add cites/citedBy relation
- [x] `delete_item()` - Move item to trash (requires manual empty)
- [x] `batch_update_items()` - Update multiple items at once
- [x] `batch_add_tags()` - Add tags to multiple items
- [x] `batch_remove_tags()` - Remove tags from multiple items
- [x] `batch_move_to_collection()` - Move multiple items to collection
- [x] `batch_delete_items()` - Delete multiple items

**Note:** No permanent delete - destructive operations require human confirmation in Zotero UI.

### Export Tools
- [x] `export_to_json()` - Export library/items to JSON
- [x] `export_to_csv()` - Export items to CSV
- [x] `export_to_bibtex()` - Export items to BibTeX
- [x] `export_collection()` - Export specific collection
- [ ] `export_with_attachments()` - Export with attachment files

### Import Tools
- [x] `import_by_doi()` - Fetch item metadata by DOI from CrossRef
- [x] `import_by_isbn()` - Fetch item metadata by ISBN from Open Library
- [x] `import_by_arxiv()` - Fetch item metadata by arXiv ID
- [x] `import_from_bibtex()` - Import items from BibTeX content
- [x] `import_from_json()` - Import items from Zotero JSON format

### Collection Management
- [x] `create_collection()` - Create new collection
- [x] `delete_collection()` - Delete collection
- [x] `rename_collection()` - Rename collection
- [x] `move_collection()` - Move collection (change parent)
- [x] `merge_collections()` - Merge two collections

### Tag Management
- [x] `merge_tags()` - Merge multiple tags into one
- [x] `rename_tag()` - Rename tag across all items
- [x] `delete_tag()` - Remove tag from all items
- [x] `delete_unused_tags()` - Remove tags not used by any item
- [x] `get_unused_tags()` - List tags not used by any item

### File Operations
- [x] `upload_pdf()` - Actually upload PDF file (not just metadata)
- [x] `download_attachment()` - Download attachment to file
- [x] `delete_attachment()` - Remove attachment from item
- [x] `replace_attachment()` - Replace attachment file
- [x] `extract_text_from_pdf()` - Extract text from PDF attachment

### Note Management
- [x] `update_note()` - Update existing note content
- [x] `delete_note()` - Delete note from item
- [x] `get_all_notes()` - Get all notes in library
- [x] `search_notes()` - Search note content

### Item Management
- [x] `convert_item_type()` - Convert item type (book → bookSection)
- [x] `merge_items()` - Merge duplicate items, transfer relations
- [x] `copy_item()` - Duplicate an item
- [x] `transfer_relations()` - Copy relations between items

### Library Statistics
- [x] `items_per_type()` - Count items by type
- [x] `items_per_collection()` - Count items per collection
- [x] `items_per_year()` - Count items by year
- [x] `tag_cloud()` - Get tag frequency for visualization
- [x] `library_summary()` - Overall library statistics
- [x] `attachment_summary()` - Attachment types and sizes

### Sync Helpers
- [x] `get_sync_status()` - Check sync status
- [x] `get_last_sync()` - Get last sync timestamp
- [x] `check_conflicts()` - Find sync conflicts
- [x] `resolve_conflict()` - Resolve sync conflict

### Utility
- [x] `get_item_by_key()` - Get item by Zotero key
- [x] `get_item_by_doi()` - Find item by DOI
- [x] `get_item_by_isbn()` - Find item by ISBN
- [x] `get_orphaned_attachments()` - Find attachments without parent
- [x] `get_trash_items()` - Get items in trash

---

## Notes

- Write tools need actual file upload implementation (`Zupload`)
- Merge operations need conflict resolution logic
- Export tools should support chunking for large libraries
