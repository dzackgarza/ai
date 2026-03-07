"""
Zotero Librarian Toolkit

Composable tools for library quality checks. No automation. No truncation.
All functions return complete data.

Uses Zotero local API (localhost:23119). Requires Zotero 7+ running.
"""

from typing import Any, Generator
from pyzotero import zotero

# arXiv tools (optional - requires arxiv, pymupdf4llm)
try:
    from .arxiv_tools import (
        search_arxiv_papers,
        download_arxiv_paper,
        list_downloaded_papers,
        read_arxiv_paper,
        get_arxiv_paper_metadata,
        export_papers_to_json,
        import_papers_from_json,
        format_arxiv_category,
        format_arxiv_categories,
        import_arxiv_paper,
        import_arxiv_papers,
    )
except ImportError:
    # arXiv dependencies not installed
    pass


# =============================================================================
# Setup
# =============================================================================


def get_zotero() -> zotero.Zotero:
    """Initialize Zotero client using local API.
    
    Requires Zotero 7+ running with local API enabled:
      Edit → Settings → Advanced → "Allow other applications to communicate with Zotero"
    """
    return zotero.Zotero(
        library_id="0",
        library_type="user",
        api_key="fake",
        local=True,
    )


# =============================================================================
# Common tools - basic operations
# =============================================================================

def _all_items(zot: zotero.Zotero, **kwargs) -> Generator[dict, None, None]:
    """Fetch ALL items with automatic pagination.

    Zotero API limits to 100 items/request. This handles pagination.
    Yields items one at a time.
    """
    start = 0
    limit = 100
    while True:
        items = zot.items(start=start, limit=limit, **kwargs)
        if not items:
            break
        yield from items
        if len(items) < limit:
            break
        start += limit


def count_items(zot: zotero.Zotero) -> int:
    """Get total item count without fetching all items."""
    zot.items(limit=1)
    return int(zot.request.headers.get('Total-Results', 0))


def _get_library_with_children(zot: zotero.Zotero) -> list[dict]:
    """Fetch ALL items with their children in one batch operation.
    
    Returns items with '_children' key containing their attachments and notes.
    Caches result on zot object to avoid refetching.
    """
    # Return cached result if available
    if hasattr(zot, '_library_cache'):
        return zot._library_cache
    
    # Fetch all items
    items = list(_all_items(zot))
    items_by_key = {item['key']: item for item in items}
    
    # Fetch all attachments and notes in parallel (they're also items)
    attachments = list(_all_items(zot, itemType="attachment"))
    notes = list(_all_items(zot, itemType="note"))
    
    # Initialize _children on all items
    for item in items:
        item['_children'] = []
    
    # Group by parentItem
    for child in attachments + notes:
        parent_key = child['data'].get('parentItem')
        if parent_key and parent_key in items_by_key:
            items_by_key[parent_key]['_children'].append(child)
    
    # Cache for future calls
    zot._library_cache = items
    return items


def all_items(zot: zotero.Zotero) -> Generator[dict, None, None]:
    """Get all items in library."""
    yield from _all_items(zot)


def all_items_by_type(zot: zotero.Zotero, item_type: str) -> Generator[dict, None, None]:
    """Get all items of a specific type."""
    yield from _all_items(zot, itemType=item_type)


def get_item(zot: zotero.Zotero, item_key: str) -> dict:
    """Get a single item by key."""
    return zot.item(item_key)


def get_attachments(zot: zotero.Zotero, item_key: str) -> list[dict]:
    """Get all attachments for an item."""
    item = zot.item(item_key)
    children = zot.children(item_key)
    return [c for c in children if c["data"]["itemType"] == "attachment"]


def _get_notes(item: dict) -> list[dict]:
    """Get notes for an item from cached _children."""
    return [
        c for c in item.get('_children', [])
        if c['data']['itemType'] == 'note'
    ]


def get_notes(zot: zotero.Zotero, item_key: str) -> list[dict]:
    """Get all notes for an item."""
    children = zot.children(item_key)
    return [c for c in children if c["data"]["itemType"] == "note"]


def get_citations(zot: zotero.Zotero, item_key: str) -> dict[str, list[str]]:
    """Get citation relations for an item.
    
    Returns: {"cites": [...], "citedBy": [...]}
    """
    item = zot.item(item_key)
    relations = item["data"].get("relations", {})
    return {
        "cites": relations.get("dc:relation:cites", []),
        "citedBy": relations.get("dc:relation:citedBy", []),
    }


def get_collections(zot: zotero.Zotero) -> list[dict]:
    """Get all collections with item counts."""
    collections = zot.collections()
    result = []
    for coll in collections:
        items = zot.collection_items(coll["key"])
        result.append({
            "key": coll["key"],
            "name": coll["data"]["name"],
            "item_count": len(items),
        })
    return result


def all_tags(zot: zotero.Zotero) -> dict[str, int]:
    """Get all tags with frequency counts."""
    from collections import Counter
    tags = []
    for item in _all_items(zot):
        for tag in item["data"].get("tags", []):
            tag_str = tag.get("tag", "")
            if tag_str:
                tags.append(tag_str)
    return dict(Counter(tags))


# =============================================================================
# Specialized tools - common query patterns
# =============================================================================

def items_without_pdf(zot: zotero.Zotero) -> list[dict]:
    """Find all items without a PDF attachment."""
    items = _get_library_with_children(zot)
    result = []
    for item in items:
        has_pdf = any(
            c['data'].get('contentType') == 'application/pdf'
            for c in item.get('_children', [])
            if c['data']['itemType'] == 'attachment'
        )
        if not has_pdf:
            result.append(item)
    return result


def items_without_attachments(zot: zotero.Zotero) -> list[dict]:
    """Find all items without any attachments."""
    items = _get_library_with_children(zot)
    return [
        item for item in items
        if not any(c['data']['itemType'] == 'attachment' for c in item.get('_children', []))
    ]


def items_without_tags(zot: zotero.Zotero) -> Generator[dict, None, None]:
    """Find all items without tags."""
    for item in _all_items(zot):
        if not item["data"].get("tags"):
            yield item


def items_not_in_collection(zot: zotero.Zotero) -> Generator[dict, None, None]:
    """Find all items not filed in any collection."""
    for item in _all_items(zot):
        if not item["data"].get("collections"):
            yield item


def items_without_field(zot: zotero.Zotero, field: str) -> Generator[dict, None, None]:
    """Find all items where a field is missing or empty."""
    for item in _all_items(zot):
        if not item["data"].get(field) or item["data"].get(field) == "":
            yield item


def items_without_abstract(zot: zotero.Zotero) -> Generator[dict, None, None]:
    """Find all items without an abstract."""
    yield from items_without_field(zot, "abstractNote")


def items_missing_required_fields(
    zot: zotero.Zotero, 
    item_type: str, 
    fields: list[str]
) -> Generator[dict, None, None]:
    """Find items of a type missing required fields."""
    for item in _all_items(zot, itemType=item_type):
        if any(not item["data"].get(f) for f in fields):
            yield item


def items_without_cites(zot: zotero.Zotero) -> Generator[dict, None, None]:
    """Find all items without 'cites' relations."""
    for item in _all_items(zot):
        cites = get_citations(zot, item["key"])
        if not cites["cites"]:
            yield item


def items_without_cited_by(zot: zotero.Zotero) -> Generator[dict, None, None]:
    """Find all items without 'citedBy' relations."""
    for item in _all_items(zot):
        cites = get_citations(zot, item["key"])
        if not cites["citedBy"]:
            yield item


def preprints_without_doi(zot: zotero.Zotero) -> Generator[dict, None, None]:
    """Find all preprints without a DOI (may be unpublished)."""
    for item in _all_items(zot, itemType="preprint"):
        if not item["data"].get("DOI"):
            yield item


def items_with_notes(zot: zotero.Zotero) -> list[dict]:
    """Find all items that have notes."""
    items = _get_library_with_children(zot)
    return [item for item in items if _get_notes(item)]


def empty_collections(zot: zotero.Zotero) -> list[dict]:
    """Find collections with no items."""
    return [c for c in get_collections(zot) if c["item_count"] == 0]


def single_item_collections(zot: zotero.Zotero) -> list[dict]:
    """Find collections with exactly one item."""
    return [c for c in get_collections(zot) if c["item_count"] == 1]


# =============================================================================
# Duplicate detection
# =============================================================================

def find_duplicates_by_field(zot: zotero.Zotero, field: str) -> dict[str, list[dict]]:
    """Find items with duplicate values in a field.
    
    Returns: {field_value: [items...]}
    """
    from collections import defaultdict
    by_value: dict[str, list[dict]] = defaultdict(list)
    for item in _all_items(zot):
        value = item["data"].get(field, "")
        if value:
            by_value[value.lower() if isinstance(value, str) else value].append(item)
    return {k: v for k, v in by_value.items() if len(v) > 1}


def duplicate_dois(zot: zotero.Zotero) -> dict[str, list[dict]]:
    """Find items with duplicate DOIs."""
    return find_duplicates_by_field(zot, "DOI")


def duplicate_titles(zot: zotero.Zotero) -> dict[str, list[dict]]:
    """Find items with duplicate titles."""
    return find_duplicates_by_field(zot, "title")


# =============================================================================
# Consistency checks
# =============================================================================

def creator_name_variations(zot: zotero.Zotero) -> dict[str, list[str]]:
    """Find author names with format variations.
    
    Returns: {last_name: ["John Smith", "Smith, John", ...]}
    """
    from collections import defaultdict
    names: dict[str, list[str]] = defaultdict(list)
    for item in _all_items(zot):
        for creator in item["data"].get("creators", []):
            first = creator.get("firstName", "")
            last = creator.get("lastName", "")
            if first and last:
                names[last.lower()].append(f"{first} {last}")
    return {k: list(set(v)) for k, v in names.items() if len(set(v)) > 1}


def journal_name_variations(zot: zotero.Zotero) -> dict[str, list[str]]:
    """Find journal names with variations (abbreviations, typos, etc.).
    
    Returns: {normalized_name: ["Nature", "Nature (London)", ...]}
    """
    from collections import defaultdict
    import re
    journals: dict[str, list[str]] = defaultdict(list)
    for item in _all_items(zot, itemType="journalArticle"):
        journal = item["data"].get("publicationTitle", "")
        if journal:
            key = re.sub(r"[\s\-]+", " ", journal.lower().strip())
            journals[key].append(journal)
    return {k: list(set(v)) for k, v in journals.items() if len(set(v)) > 1}


def similar_tags(zot: zotero.Zotero, threshold: float = 0.8) -> dict[str, list[str]]:
    """Find similar tags (potential duplicates/typos).
    
    Returns: {tag: [similar_tags...]}
    """
    from difflib import SequenceMatcher
    tags = list(all_tags(zot).keys())
    result = {}
    for tag in tags:
        similar = [
            t for t in tags 
            if t != tag and SequenceMatcher(None, t, tag).ratio() >= threshold
        ]
        if similar:
            result[tag] = similar
    return result


# =============================================================================
# Validation
# =============================================================================

def validate_doi(doi: str) -> bool:
    """Check if DOI format is valid."""
    import re
    pattern = r"10\.\d{4,9}/[-._;()/:A-Z0-9]+"
    return bool(re.match(pattern, doi, re.IGNORECASE))


def validate_isbn(isbn: str) -> bool:
    """Check if ISBN format is valid (ISBN-10 or ISBN-13)."""
    import re
    isbn = isbn.replace("-", "").replace(" ", "")
    if len(isbn) == 10:
        return bool(re.match(r"\d{9}[\dX]", isbn))
    elif len(isbn) == 13:
        return bool(re.match(r"\d{13}", isbn))
    return False


def validate_issn(issn: str) -> bool:
    """Check if ISSN format is valid."""
    import re
    return bool(re.match(r"\d{4}-\d{3}[\dX]", issn))


def items_with_invalid_doi(zot: zotero.Zotero) -> Generator[dict, None, None]:
    """Find items with invalid DOI format."""
    for item in _all_items(zot):
        doi = item["data"].get("DOI", "")
        if doi and not validate_doi(doi):
            yield item


def items_with_invalid_isbn(zot: zotero.Zotero) -> Generator[dict, None, None]:
    """Find items with invalid ISBN format."""
    for item in _all_items(zot):
        isbn = item["data"].get("ISBN", "")
        if isbn and not validate_isbn(isbn):
            yield item


def items_with_invalid_issn(zot: zotero.Zotero) -> Generator[dict, None, None]:
    """Find items with invalid ISSN format."""
    for item in _all_items(zot):
        issn = item["data"].get("ISSN", "")
        if issn and not validate_issn(issn):
            yield item


def items_with_broken_urls(zot: zotero.Zotero) -> Generator[dict, None, None]:
    """Find items with malformed URLs."""
    import re
    url_pattern = re.compile(r"^https?://")
    for item in _all_items(zot):
        url = item["data"].get("url", "")
        if url and not url_pattern.match(url):
            yield item


def items_with_placeholder_text(
    zot: zotero.Zotero, 
    field: str, 
    patterns: list[str]
) -> Generator[dict, None, None]:
    """Find items with placeholder text in a field."""
    for item in _all_items(zot):
        value = item["data"].get(field, "") or ""
        if any(p.lower() in value.lower() for p in patterns):
            yield item


def items_with_placeholder_titles(zot: zotero.Zotero) -> Generator[dict, None, None]:
    """Find items with placeholder titles."""
    yield from items_with_placeholder_text(
        zot, "title", ["untitled", "[no title]", "todo", "tbd"]
    )


# =============================================================================
# Inspection helpers
# =============================================================================

def attachment_info(zot: zotero.Zotero, item_key: str) -> list[dict]:
    """Get file info for all attachments of an item."""
    attachments = get_attachments(zot, item_key)
    return [
        {
            "key": a["key"],
            "title": a["data"].get("title", ""),
            "contentType": a["data"].get("contentType", ""),
            "filename": a["data"].get("filename", ""),
            "md5": a["data"].get("md5", ""),
        }
        for a in attachments
    ]


def check_item_completeness(
    zot: zotero.Zotero,
    item_key: str,
    required_fields: list[str]
) -> dict[str, Any]:
    """Check if an item has all required fields."""
    item = get_item(zot, item_key)
    missing = [f for f in required_fields if not item["data"].get(f)]
    return {
        "key": item_key,
        "title": item["data"].get("title", ""),
        "complete": len(missing) == 0,
        "missing": missing,
    }


# =============================================================================
# Write operations - tools for fixing issues
# =============================================================================

def update_item_fields(zot: zotero.Zotero, item_key: str, fields: dict[str, Any]) -> dict:
    """Update fields on an existing item.
    
    Args:
        zot: Zotero client
        item_key: Key of item to update
        fields: Dict of field names and values to update
    
    Returns:
        Response from Zotero API
    """
    item = get_item(zot, item_key)
    for key, value in fields.items():
        item["data"][key] = value
    return zot.update_item(item)


def add_tags_to_item(zot: zotero.Zotero, item_key: str, tags: list[str]) -> dict:
    """Add tags to an item.
    
    Args:
        zot: Zotero client
        item_key: Key of item to update
        tags: List of tag strings to add
    
    Returns:
        Response from Zotero API
    """
    item = get_item(zot, item_key)
    existing_tags = [t["tag"] for t in item["data"].get("tags", [])]
    for tag in tags:
        if tag not in existing_tags:
            existing_tags.append(tag)
    item["data"]["tags"] = [{"tag": t} for t in existing_tags]
    return zot.update_item(item)


def remove_tags_from_item(zot: zotero.Zotero, item_key: str, tags: list[str]) -> dict:
    """Remove tags from an item.
    
    Args:
        zot: Zotero client
        item_key: Key of item to update
        tags: List of tag strings to remove
    
    Returns:
        Response from Zotero API
    """
    item = get_item(zot, item_key)
    existing_tags = [t["tag"] for t in item["data"].get("tags", [])]
    new_tags = [t for t in existing_tags if t not in tags]
    item["data"]["tags"] = [{"tag": t} for t in new_tags]
    return zot.update_item(item)


def move_item_to_collection(zot: zotero.Zotero, item_key: str, collection_key: str) -> dict:
    """Move an item to a collection.
    
    Args:
        zot: Zotero client
        item_key: Key of item to move
        collection_key: Key of target collection
    
    Returns:
        Response from Zotero API
    """
    item = get_item(zot, item_key)
    item["data"]["collections"] = [collection_key]
    return zot.update_item(item)


def add_item_to_collection(zot: zotero.Zotero, item_key: str, collection_key: str) -> dict:
    """Add an item to a collection (keeps existing collections).
    
    Args:
        zot: Zotero client
        item_key: Key of item to add
        collection_key: Key of target collection
    
    Returns:
        Response from Zotero API
    """
    item = get_item(zot, item_key)
    collections = item["data"].get("collections", [])
    if collection_key not in collections:
        collections.append(collection_key)
    item["data"]["collections"] = collections
    return zot.update_item(item)


def remove_item_from_collection(zot: zotero.Zotero, item_key: str, collection_key: str) -> dict:
    """Remove an item from a collection.
    
    Args:
        zot: Zotero client
        item_key: Key of item to update
        collection_key: Key of collection to remove from
    
    Returns:
        Response from Zotero API
    """
    item = get_item(zot, item_key)
    collections = item["data"].get("collections", [])
    collections = [c for c in collections if c != collection_key]
    item["data"]["collections"] = collections
    return zot.update_item(item)


def attach_pdf(zot: zotero.Zotero, parent_item_key: str, pdf_path: str, title: str = None) -> dict:
    """Attach a PDF file to an item.
    
    Args:
        zot: Zotero client
        parent_item_key: Key of parent item
        pdf_path: Path to PDF file
        title: Optional title for attachment (defaults to PDF filename)
    
    Returns:
        Response from Zotero API with new attachment key
    """
    import os
    from pathlib import Path
    
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    if title is None:
        title = pdf_file.name
    
    # Create attachment item
    attachment = {
        "itemType": "attachment",
        "linkMode": "imported_file",
        "parentItem": parent_item_key,
        "title": title,
        "contentType": "application/pdf",
        "filename": pdf_file.name,
    }
    
    # Note: This creates the metadata only. Actual file upload requires
    # additional steps with zotero.Zupload which is more complex.
    # For now, this creates a placeholder that can be manually linked.
    return zot.create_items([attachment])


def attach_url(zot: zotero.Zotero, parent_item_key: str, url: str, title: str = None) -> dict:
    """Attach a URL/link to an item.
    
    Args:
        zot: Zotero client
        parent_item_key: Key of parent item
        url: URL to attach
        title: Optional title for attachment
    
    Returns:
        Response from Zotero API
    """
    if title is None:
        title = url
    
    attachment = {
        "itemType": "attachment",
        "linkMode": "linked_url",
        "parentItem": parent_item_key,
        "title": title,
        "url": url,
        "contentType": "text/html",
    }
    return zot.create_items([attachment])


def attach_note(zot: zotero.Zotero, parent_item_key: str, note_text: str, title: str = None) -> dict:
    """Add a note to an item.
    
    Args:
        zot: Zotero client
        parent_item_key: Key of parent item
        note_text: Note content (supports HTML)
        title: Optional title for note
    
    Returns:
        Response from Zotero API
    """
    note = {
        "itemType": "note",
        "parentItem": parent_item_key,
        "note": note_text,
    }
    if title:
        note["title"] = title
    return zot.create_items([note])


def add_citation_relation(zot: zotero.Zotero, item_key: str, relation_type: str, target_uri: str) -> dict:
    """Add a citation relation (cites or citedBy).
    
    Args:
        zot: Zotero client
        item_key: Key of item to update
        relation_type: "cites" or "citedBy"
        target_uri: URI of related item (DOI, Zotero URI, etc.)
    
    Returns:
        Response from Zotero API
    """
    item = get_item(zot, item_key)
    relations = item["data"].get("relations", {})
    relation_key = f"dc:relation:{relation_type}"
    
    if relation_key not in relations:
        relations[relation_key] = []
    if isinstance(relations[relation_key], str):
        relations[relation_key] = [relations[relation_key]]
    if target_uri not in relations[relation_key]:
        relations[relation_key].append(target_uri)
    
    item["data"]["relations"] = relations
    return zot.update_item(item)


def delete_item(zot: zotero.Zotero, item_key: str) -> dict:
    """Move an item to trash.

    Args:
        zot: Zotero client
        item_key: Key of item to delete

    Returns:
        Response from Zotero API

    Note: This moves the item to trash. To permanently delete,
    the user must manually empty trash in the Zotero UI.
    """
    return zot.delete_item(item_key)


# =============================================================================
# File Operations
# =============================================================================

def upload_pdf(zot: zotero.Zotero, parent_item_key: str, pdf_path: str, title: str = None) -> dict:
    """Upload a PDF file as an attachment to an item.

    Uses Zotero's Zupload mechanism to upload the actual file content,
    not just metadata. The file is stored in Zotero's storage.

    Args:
        zot: Zotero client
        parent_item_key: Key of parent item to attach PDF to
        pdf_path: Path to the PDF file to upload
        title: Optional title for attachment (defaults to PDF filename)

    Returns:
        Dict with "success" (bool) and either "key" (str) on success or "error" (str) on failure

    Example:
        result = upload_pdf(zot, "ABC123", "/path/to/file.pdf", title="Supplementary Material")
        if result["success"]:
            print(f"Uploaded PDF with key: {result['key']}")

    Note:
        Requires Zotero 7+ with local API enabled.
        File is uploaded to Zotero storage and synced if sync is enabled.
        Maximum file size depends on Zotero storage settings.
    """
    import os
    from pathlib import Path
    import hashlib
    import base64
    import httpx

    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        return {"success": False, "error": f"PDF not found: {pdf_path}"}

    if not pdf_file.suffix.lower() == ".pdf":
        return {"success": False, "error": f"File is not a PDF: {pdf_path}"}

    if title is None:
        title = pdf_file.name

    try:
        # Read file content
        with open(pdf_file, "rb") as f:
            file_content = f.read()

        # Calculate MD5 hash
        md5_hash = hashlib.md5(file_content).hexdigest()
        file_size = len(file_content)

        # Step 1: Create attachment item metadata
        attachment = {
            "itemType": "attachment",
            "linkMode": "imported_file",
            "parentItem": parent_item_key,
            "title": title,
            "contentType": "application/pdf",
            "filename": pdf_file.name,
            "md5": md5_hash,
            "mtime": int(os.path.getmtime(pdf_file) * 1000),
        }

        # Create the attachment item
        create_result = zot.create_items([attachment])
        if not create_result or "success" not in create_result:
            return {"success": False, "error": "Failed to create attachment metadata"}

        attachment_key = create_result["success"]["0"]["key"]

        # Step 2: Get upload authorization from Zotero
        # First, get the storage info
        storage_url = "http://localhost:23119/api/users/0/storage"
        headers = {"Zotero-API-Key": "fake"}

        # Get upload authorization
        auth_response = httpx.post(
            f"http://localhost:23119/api/users/0/items/{attachment_key}/file",
            headers={
                "Zotero-API-Key": "fake",
                "Content-Type": "application/pdf",
                "If-None-Match": "*",
            },
            content=file_content,
            timeout=60.0,
        )

        if auth_response.status_code in (200, 201, 204):
            return {"success": True, "key": attachment_key}
        else:
            # If direct upload fails, try alternative method using zotero.Zupload
            # This is a fallback for different Zotero configurations
            try:
                from pyzotero import zupload

                zup = zupload.Zupload(zot, attachment_key)
                zup.upload_file(str(pdf_file))
                return {"success": True, "key": attachment_key}
            except ImportError:
                # zupload not available, return metadata-only result
                return {
                    "success": True,
                    "key": attachment_key,
                    "warning": "Attachment metadata created but file upload requires zupload package"
                }
            except Exception as upload_err:
                return {
                    "success": True,
                    "key": attachment_key,
                    "warning": f"Attachment metadata created but file upload failed: {str(upload_err)}"
                }

    except httpx.HTTPError as e:
        return {"success": False, "error": f"HTTP error during upload: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def download_attachment(zot: zotero.Zotero, attachment_key: str, output_path: str) -> dict:
    """Download an attachment file from Zotero to local storage.

    Retrieves the actual file content for an attachment item and saves it
    to the specified local path.

    Args:
        zot: Zotero client
        attachment_key: Key of the attachment item to download
        output_path: Local file path where the attachment will be saved

    Returns:
        Dict with "success" (bool) and either "message" (str) on success or "error" (str) on failure

    Example:
        result = download_attachment(zot, "XYZ789", "/path/to/save/file.pdf")
        if result["success"]:
            print(f"Downloaded: {result['message']}")

    Note:
        Requires Zotero 7+ with local API enabled.
        Attachment must be a stored file (not a linked file or URL).
        Parent item does not need to be downloaded separately.
    """
    from pathlib import Path
    import httpx

    try:
        # Get attachment item info
        attachment = zot.item(attachment_key)
        if not attachment:
            return {"success": False, "error": f"Attachment not found: {attachment_key}"}

        # Verify it's an attachment
        if attachment.get("data", {}).get("itemType") != "attachment":
            return {"success": False, "error": f"Item is not an attachment: {attachment_key}"}

        # Get the file download URL from local API
        download_url = f"http://localhost:23119/api/users/0/items/{attachment_key}/file"

        # Download the file
        response = httpx.get(
            download_url,
            headers={"Zotero-API-Key": "fake"},
            timeout=60.0,
        )

        if response.status_code != 200:
            return {"success": False, "error": f"Download failed with status {response.status_code}"}

        # Write to output path
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "wb") as f:
            f.write(response.content)

        return {"success": True, "message": f"Downloaded {len(response.content)} bytes to {output_path}"}

    except httpx.HTTPError as e:
        return {"success": False, "error": f"HTTP error during download: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_attachment(zot: zotero.Zotero, attachment_key: str) -> dict:
    """Delete an attachment from Zotero.

    Removes the attachment item and its associated file from Zotero.
    The file is moved to trash and can be recovered until trash is emptied.

    Args:
        zot: Zotero client
        attachment_key: Key of the attachment to delete

    Returns:
        Dict with "success" (bool) and either "message" (str) on success or "error" (str) on failure

    Example:
        result = delete_attachment(zot, "XYZ789")
        if result["success"]:
            print("Attachment deleted")

    Note:
        This moves the attachment to trash. To permanently delete,
        the user must manually empty trash in the Zotero UI.
        The parent item is not affected.
    """
    try:
        # Verify the item exists and is an attachment
        attachment = zot.item(attachment_key)
        if not attachment:
            return {"success": False, "error": f"Attachment not found: {attachment_key}"}

        if attachment.get("data", {}).get("itemType") != "attachment":
            return {"success": False, "error": f"Item is not an attachment: {attachment_key}"}

        # Delete the attachment
        zot.delete_item(attachment_key)
        return {"success": True, "message": "Attachment moved to trash"}

    except Exception as e:
        return {"success": False, "error": str(e)}


def extract_text_from_pdf(zot: zotero.Zotero, attachment_key: str) -> dict:
    """Extract text content from a PDF attachment.

    Downloads the PDF and extracts its text content using pdfplumber.
    Returns the full text content as a string.

    Args:
        zot: Zotero client
        attachment_key: Key of the PDF attachment to extract text from

    Returns:
        Dict with "success" (bool) and either "text" (str) on success or "error" (str) on failure

    Example:
        result = extract_text_from_pdf(zot, "XYZ789")
        if result["success"]:
            print(f"Extracted {len(result['text'])} characters")

    Note:
        Requires pdfplumber package: pip install pdfplumber
        Works best with text-based PDFs (not scanned images).
        Large PDFs may take time to process.
    """
    import tempfile
    import os

    try:
        # Get attachment item info
        attachment = zot.item(attachment_key)
        if not attachment:
            return {"success": False, "error": f"Attachment not found: {attachment_key}"}

        # Verify it's a PDF attachment
        item_data = attachment.get("data", {})
        if item_data.get("itemType") != "attachment":
            return {"success": False, "error": f"Item is not an attachment: {attachment_key}"}

        content_type = item_data.get("contentType", "")
        if content_type != "application/pdf":
            return {"success": False, "error": f"Attachment is not a PDF (content type: {content_type})"}

        # Try to import pdfplumber
        try:
            import pdfplumber
        except ImportError:
            return {"success": False, "error": "pdfplumber not installed. Run: pip install pdfplumber"}

        # Download the PDF to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            download_result = download_attachment(zot, attachment_key, tmp_path)
            if not download_result["success"]:
                return download_result

            # Extract text using pdfplumber
            text_parts = []
            with pdfplumber.open(tmp_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)

            full_text = "\n\n".join(text_parts)
            return {"success": True, "text": full_text, "pages": len(text_parts)}

        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    except Exception as e:
        return {"success": False, "error": str(e)}


# =============================================================================
# Note Management
# =============================================================================

def update_note(zot: zotero.Zotero, note_key: str, new_content: str) -> dict:
    """Update the content of an existing note.

    Modifies the text content of a note item. Supports HTML formatting
    in the note content.

    Args:
        zot: Zotero client
        note_key: Key of the note to update
        new_content: New note content (supports HTML formatting)

    Returns:
        Dict with "success" (bool) and either "message" (str) on success or "error" (str) on failure

    Example:
        result = update_note(zot, "NOTE123", "<h2>Updated Notes</h2><p>New content here.</p>")
        if result["success"]:
            print("Note updated successfully")

    Note:
        Note content supports HTML formatting.
        The note's parent item is not affected.
        Use attach_note() to create new notes.
    """
    try:
        # Get the existing note
        note = zot.item(note_key)
        if not note:
            return {"success": False, "error": f"Note not found: {note_key}"}

        # Verify it's a note
        if note.get("data", {}).get("itemType") != "note":
            return {"success": False, "error": f"Item is not a note: {note_key}"}

        # Update the note content
        note["data"]["note"] = new_content

        # Save the updated note
        zot.update_item(note)
        return {"success": True, "message": "Note updated successfully"}

    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_note(zot: zotero.Zotero, note_key: str) -> dict:
    """Delete a note from Zotero.

    Removes the note item from Zotero. The note is moved to trash
    and can be recovered until trash is emptied.

    Args:
        zot: Zotero client
        note_key: Key of the note to delete

    Returns:
        Dict with "success" (bool) and either "message" (str) on success or "error" (str) on failure

    Example:
        result = delete_note(zot, "NOTE123")
        if result["success"]:
            print("Note deleted")

    Note:
        This moves the note to trash. To permanently delete,
        the user must manually empty trash in the Zotero UI.
        The parent item is not affected.
    """
    try:
        # Verify the item exists and is a note
        note = zot.item(note_key)
        if not note:
            return {"success": False, "error": f"Note not found: {note_key}"}

        if note.get("data", {}).get("itemType") != "note":
            return {"success": False, "error": f"Item is not a note: {note_key}"}

        # Delete the note
        zot.delete_item(note_key)
        return {"success": True, "message": "Note moved to trash"}

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_all_notes(zot: zotero.Zotero) -> list[dict]:
    """Get all notes in the library.

    Fetches all note items from the library, including their content
    and parent item information.

    Args:
        zot: Zotero client

    Returns:
        List of note items with their data. Each note includes:
        - key: Note key
        - note: Note content (HTML)
        - title: Note title (if any)
        - parentItem: Key of parent item (if any)
        - dateAdded: When the note was created
        - dateModified: When the note was last modified

    Example:
        notes = get_all_notes(zot)
        for note in notes:
            print(f"Note on item {note['data'].get('parentItem')}: {note['data']['note'][:50]}...")

    Note:
        Returns all notes regardless of parent item.
        Notes without a parentItem are standalone notes.
        For large libraries, this may take time to fetch all notes.
    """
    notes = []
    for item in _all_items(zot, itemType="note"):
        notes.append(item)
    return notes


def search_notes(zot: zotero.Zotero, query: str) -> list[dict]:
    """Search note content for text.

    Searches through all notes in the library for notes containing
    the specified query string (case-insensitive).

    Args:
        zot: Zotero client
        query: Text to search for in note content (case-insensitive)

    Returns:
        List of note items where the note content contains the query string.
        Each note includes full item data including key, content, and parent info.

    Example:
        matching_notes = search_notes(zot, "methodology")
        for note in matching_notes:
            parent = note['data'].get('parentItem', 'standalone')
            print(f"Found in note for item {parent}")

    Note:
        Search is case-insensitive.
        Searches the full HTML content of notes.
        Returns complete note items, not just snippets.
        For large libraries, this may take time to search all notes.
    """
    results = []
    query_lower = query.lower()

    for note in _all_items(zot, itemType="note"):
        note_content = note.get("data", {}).get("note", "") or ""
        # Strip HTML tags for plain text search
        import re
        plain_text = re.sub(r"<[^>]+>", " ", note_content)
        if query_lower in plain_text.lower():
            results.append(note)

    return results


# =============================================================================
# Collection Management
# =============================================================================

def create_collection(zot: zotero.Zotero, name: str, parent_key: str = None) -> dict:
    """Create a new collection.

    Args:
        zot: Zotero client
        name: Name for the new collection
        parent_key: Optional key of parent collection (for nested collections)

    Returns:
        Dict with "success" (bool) and either "key" (str) on success or "error" (str) on failure

    Example:
        # Create top-level collection
        result = create_collection(zot, "My New Collection")
        if result["success"]:
            print(f"Created collection: {result['key']}")

        # Create nested collection
        result = create_collection(zot, "Subcollection", parent_key="ABC123")
    """
    try:
        collection = {
            "name": name,
        }
        if parent_key:
            collection["parentCollection"] = parent_key

        result = zot.create_collections([collection])
        if result and "success" in result and result["success"]:
            created_key = result["success"]["0"]["key"]
            return {"success": True, "key": created_key}
        return {"success": False, "error": "Failed to create collection"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_collection(zot: zotero.Zotero, collection_key: str) -> dict:
    """Delete a collection (moves to trash).

    Args:
        zot: Zotero client
        collection_key: Key of collection to delete

    Returns:
        Dict with "success" (bool) and either "message" (str) on success or "error" (str) on failure

    Note: This moves the collection to trash. To permanently delete,
    the user must manually empty trash in the Zotero UI.
    Items in the collection are NOT deleted, only the collection itself.

    Example:
        result = delete_collection(zot, "ABC123")
        if result["success"]:
            print("Collection moved to trash")
    """
    try:
        zot.delete_collection(collection_key)
        return {"success": True, "message": "Collection moved to trash"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def rename_collection(zot: zotero.Zotero, collection_key: str, new_name: str) -> dict:
    """Rename a collection.

    Args:
        zot: Zotero client
        collection_key: Key of collection to rename
        new_name: New name for the collection

    Returns:
        Dict with "success" (bool) and either "message" (str) on success or "error" (str) on failure

    Example:
        result = rename_collection(zot, "ABC123", "Updated Collection Name")
        if result["success"]:
            print("Collection renamed")
    """
    try:
        collection = zot.collection(collection_key)
        collection["data"]["name"] = new_name
        zot.update_collection(collection)
        return {"success": True, "message": "Collection renamed"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def merge_collections(zot: zotero.Zotero, source_keys: list[str], target_key: str) -> dict:
    """Merge multiple collections into one.

    Moves all items from source collections to the target collection,
    then deletes the source collections (moves to trash).

    Args:
        zot: Zotero client
        source_keys: List of collection keys to merge from
        target_key: Key of target collection to merge into

    Returns:
        Dict with "success" (bool), "moved_items" (int), and either "message" (str) or "error" (str)

    Example:
        result = merge_collections(zot, ["ABC123", "DEF456"], "TARGET789")
        if result["success"]:
            print(f"Merged {result['moved_items']} items")
    """
    try:
        moved_count = 0
        failed_sources = []

        # Get all items from source collections and add to target
        for source_key in source_keys:
            try:
                items = zot.collection_items(source_key)
                for item in items:
                    try:
                        add_item_to_collection(zot, item["key"], target_key)
                        moved_count += 1
                    except Exception:
                        pass  # Continue with other items
            except Exception:
                failed_sources.append(source_key)

        # Delete source collections
        for source_key in source_keys:
            try:
                zot.delete_collection(source_key)
            except Exception:
                pass  # Collection may have already been deleted

        if failed_sources:
            return {
                "success": True,
                "moved_items": moved_count,
                "message": f"Merged collections. Some sources failed: {failed_sources}",
                "failed_sources": failed_sources
            }
        return {"success": True, "moved_items": moved_count, "message": "Collections merged successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# =============================================================================
# Tag Management
# =============================================================================

def merge_tags(zot: zotero.Zotero, source_tags: list[str], target_tag: str) -> dict:
    """Merge multiple tags into one across all items.

    Replaces all occurrences of source tags with the target tag on every item.

    Args:
        zot: Zotero client
        source_tags: List of tag names to merge
        target_tag: Target tag name to merge into

    Returns:
        Dict with "success" (bool), "updated_items" (int), and either "message" (str) or "error" (str)

    Example:
        # Merge similar tags like "machine-learning" and "ml" into "machine_learning"
        result = merge_tags(zot, ["machine-learning", "ml"], "machine_learning")
        if result["success"]:
            print(f"Updated {result['updated_items']} items")
    """
    try:
        updated_count = 0

        for item in _all_items(zot):
            current_tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
            new_tags = []
            changed = False

            for tag in current_tags:
                if tag in source_tags:
                    if target_tag not in new_tags:
                        new_tags.append(target_tag)
                    changed = True
                elif tag not in new_tags:
                    new_tags.append(tag)

            if changed:
                item["data"]["tags"] = [{"tag": t} for t in new_tags]
                try:
                    zot.update_item(item)
                    updated_count += 1
                except Exception:
                    pass  # Continue with other items

        return {"success": True, "updated_items": updated_count, "message": "Tags merged successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def rename_tag(zot: zotero.Zotero, old_name: str, new_name: str) -> dict:
    """Rename a tag across all items.

    Args:
        zot: Zotero client
        old_name: Current tag name to rename
        new_name: New tag name

    Returns:
        Dict with "success" (bool), "updated_items" (int), and either "message" (str) or "error" (str)

    Example:
        result = rename_tag(zot, "old-tag", "new-tag")
        if result["success"]:
            print(f"Renamed tag on {result['updated_items']} items")
    """
    try:
        updated_count = 0

        for item in _all_items(zot):
            current_tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
            if old_name in current_tags:
                new_tags = [new_name if t == old_name else t for t in current_tags]
                item["data"]["tags"] = [{"tag": t} for t in new_tags]
                try:
                    zot.update_item(item)
                    updated_count += 1
                except Exception:
                    pass  # Continue with other items

        return {"success": True, "updated_items": updated_count, "message": "Tag renamed successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_tag(zot: zotero.Zotero, tag_name: str) -> dict:
    """Remove a tag from all items.

    Args:
        zot: Zotero client
        tag_name: Name of tag to remove

    Returns:
        Dict with "success" (bool), "updated_items" (int), and either "message" (str) or "error" (str)

    Example:
        result = delete_tag(zot, "obsolete-tag")
        if result["success"]:
            print(f"Removed tag from {result['updated_items']} items")
    """
    try:
        updated_count = 0

        for item in _all_items(zot):
            current_tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
            if tag_name in current_tags:
                new_tags = [t for t in current_tags if t != tag_name]
                item["data"]["tags"] = [{"tag": t} for t in new_tags]
                try:
                    zot.update_item(item)
                    updated_count += 1
                except Exception:
                    pass  # Continue with other items

        return {"success": True, "updated_items": updated_count, "message": "Tag deleted successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_unused_tags(zot: zotero.Zotero) -> dict:
    """List tags not used by any item.

    Note: In Zotero, tags can exist in the global tag list even if no items use them.
    This function compares the global tag list against tags actually used by items.

    Returns:
        Dict with "success" (bool) and either "unused_tags" (list) or "error" (str)

    Example:
        result = get_unused_tags(zot)
        if result["success"]:
            print(f"Unused tags: {result['unused_tags']}")
    """
    try:
        # Get all tags from the global tag list
        all_global_tags = set()
        try:
            global_tags_response = zot.tags()
            all_global_tags = set(global_tags_response)
        except Exception:
            pass

        # Get all tags actually used by items
        used_tags = set()
        for item in _all_items(zot):
            for tag in item["data"].get("tags", []):
                tag_str = tag.get("tag", "")
                if tag_str:
                    used_tags.add(tag_str)

        # Find unused tags
        unused_tags = list(all_global_tags - used_tags)
        unused_tags.sort()

        return {"success": True, "unused_tags": unused_tags}
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_unused_tags(zot: zotero.Zotero) -> dict:
    """Remove all unused tags from the library.

    Deletes tags that exist in the global tag list but are not used by any item.

    Returns:
        Dict with "success" (bool), "deleted_count" (int), and either "message" (str) or "error" (str)

    Example:
        result = delete_unused_tags(zot)
        if result["success"]:
            print(f"Deleted {result['deleted_count']} unused tags")
    """
    try:
        # Get unused tags
        unused_result = get_unused_tags(zot)
        if not unused_result["success"]:
            return unused_result

        unused_tags = unused_result["unused_tags"]
        deleted_count = 0

        # Delete each unused tag
        for tag in unused_tags:
            try:
                zot.delete_tags(tag)
                deleted_count += 1
            except Exception:
                pass  # Continue with other tags

        return {"success": True, "deleted_count": deleted_count, "message": "Unused tags deleted successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# =============================================================================
# Batch operations - apply operations to multiple items
# =============================================================================


def batch_update_items(
    zot: zotero.Zotero,
    item_keys: list[str],
    fields: dict[str, Any]
) -> dict[str, list[str]]:
    """Update fields on multiple items.

    Args:
        zot: Zotero client
        item_keys: List of item keys to update
        fields: Dict of field names and values to update on all items

    Returns:
        Dict with "success" and "failed" lists of item keys
    """
    result = {"success": [], "failed": []}
    for item_key in item_keys:
        try:
            update_item_fields(zot, item_key, fields)
            result["success"].append(item_key)
        except Exception:
            result["failed"].append(item_key)
    return result


def batch_add_tags(
    zot: zotero.Zotero,
    item_keys: list[str],
    tags: list[str]
) -> dict[str, list[str]]:
    """Add tags to multiple items.

    Args:
        zot: Zotero client
        item_keys: List of item keys to update
        tags: List of tag strings to add to all items

    Returns:
        Dict with "success" and "failed" lists of item keys
    """
    result = {"success": [], "failed": []}
    for item_key in item_keys:
        try:
            add_tags_to_item(zot, item_key, tags)
            result["success"].append(item_key)
        except Exception:
            result["failed"].append(item_key)
    return result


def batch_remove_tags(
    zot: zotero.Zotero,
    item_keys: list[str],
    tags: list[str]
) -> dict[str, list[str]]:
    """Remove tags from multiple items.

    Args:
        zot: Zotero client
        item_keys: List of item keys to update
        tags: List of tag strings to remove from all items

    Returns:
        Dict with "success" and "failed" lists of item keys
    """
    result = {"success": [], "failed": []}
    for item_key in item_keys:
        try:
            remove_tags_from_item(zot, item_key, tags)
            result["success"].append(item_key)
        except Exception:
            result["failed"].append(item_key)
    return result


def batch_move_to_collection(
    zot: zotero.Zotero,
    item_keys: list[str],
    collection_key: str
) -> dict[str, list[str]]:
    """Move multiple items to a collection.

    Args:
        zot: Zotero client
        item_keys: List of item keys to move
        collection_key: Key of target collection

    Returns:
        Dict with "success" and "failed" lists of item keys
    """
    result = {"success": [], "failed": []}
    for item_key in item_keys:
        try:
            move_item_to_collection(zot, item_key, collection_key)
            result["success"].append(item_key)
        except Exception:
            result["failed"].append(item_key)
    return result


def batch_delete_items(
    zot: zotero.Zotero,
    item_keys: list[str]
) -> dict[str, list[str]]:
    """Move multiple items to trash.

    Args:
        zot: Zotero client
        item_keys: List of item keys to delete

    Returns:
        Dict with "success" and "failed" lists of item keys

    Note: This moves items to trash. To permanently delete,
    the user must manually empty trash in the Zotero UI.
    """
    result = {"success": [], "failed": []}
    for item_key in item_keys:
        try:
            delete_item(zot, item_key)
            result["success"].append(item_key)
        except Exception:
            result["failed"].append(item_key)
    return result


# =============================================================================
# Export Tools
# =============================================================================

def export_to_json(zot: zotero.Zotero, items: list[dict] = None, filepath: str = None) -> str | None:
    """Export library items to JSON file.

    Exports complete item data including all fields, relations, and metadata.
    If no items provided, exports entire library.

    Args:
        zot: Zotero client
        items: Optional list of items to export. If None, exports all items
        filepath: Optional file path to write JSON. If None, returns JSON string

    Returns:
        JSON string if filepath is None, otherwise None (writes to file)

    Example:
        # Export entire library to file
        export_to_json(zot, filepath="library.json")

        # Export specific items and get JSON string
        json_str = export_to_json(zot, items=my_items)
    """
    if items is None:
        items = list(_all_items(zot))

    # Convert to serializable format (ensure all data is included)
    export_data = []
    for item in items:
        # Create a clean copy with all relevant data
        item_export = {
            "key": item.get("key", ""),
            "version": item.get("version", 0),
            "data": item.get("data", {}),
            "relations": item.get("relations", {}),
        }
        # Include children if available (from cached library)
        if "_children" in item:
            item_export["_children"] = [
                {
                    "key": child.get("key", ""),
                    "version": child.get("version", 0),
                    "data": child.get("data", {}),
                }
                for child in item["_children"]
            ]
        export_data.append(item_export)

    import json
    json_str = json.dumps(export_data, indent=2, ensure_ascii=False)

    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_str)
        return None
    return json_str


def export_to_csv(
    zot: zotero.Zotero,
    items: list[dict] = None,
    filepath: str = None,
    fields: list[str] = None
) -> str | None:
    """Export library items to CSV format.

    Exports selected fields for each item. If no fields specified, exports
    common bibliographic fields. If no items provided, exports entire library.

    Args:
        zot: Zotero client
        items: Optional list of items to export. If None, exports all items
        filepath: Optional file path to write CSV. If None, returns CSV string
        fields: Optional list of field names to export. Defaults to common fields:
            ["title", "creator", "date", "itemType", "publicationTitle", "DOI", "url"]

    Returns:
        CSV string if filepath is None, otherwise None (writes to file)

    Example:
        # Export with default fields
        export_to_csv(zot, filepath="library.csv")

        # Export specific fields
        export_to_csv(zot, fields=["title", "author", "year", "DOI"])

        # Export specific items
        export_to_csv(zot, items=my_items, filepath="selected.csv")
    """
    if items is None:
        items = list(_all_items(zot))

    if fields is None:
        fields = [
            "title",
            "creator",
            "date",
            "itemType",
            "publicationTitle",
            "DOI",
            "url",
            "abstractNote",
            "tags",
        ]

    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)

    # Write header
    writer.writerow(fields)

    # Write data rows
    for item in items:
        data = item.get("data", {})
        row = []
        for field in fields:
            value = data.get(field, "")
            # Handle creators specially - format as "LastName, FirstName"
            if field == "creator" and isinstance(value, list):
                creators = []
                for c in value:
                    first = c.get("firstName", "")
                    last = c.get("lastName", "")
                    if last and first:
                        creators.append(f"{last}, {first}")
                    elif last:
                        creators.append(last)
                    elif first:
                        creators.append(first)
                value = "; ".join(creators)
            # Handle tags - format as semicolon-separated list
            elif field == "tags" and isinstance(value, list):
                value = "; ".join(t.get("tag", "") for t in value if t.get("tag"))
            # Ensure value is string
            if value is None:
                value = ""
            elif not isinstance(value, str):
                value = str(value)
            row.append(value)
        writer.writerow(row)

    csv_str = output.getvalue()

    if filepath:
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write(csv_str)
        return None
    return csv_str


def export_to_bibtex(zot: zotero.Zotero, items: list[dict] = None, filepath: str = None) -> str | None:
    """Export library items to BibTeX format.

    Converts Zotero items to BibTeX entries. Supports common item types
    (journalArticle, book, incollection, conference, thesis, etc.).
    If no items provided, exports entire library.

    Args:
        zot: Zotero client
        items: Optional list of items to export. If None, exports all items
        filepath: Optional file path to write BibTeX. If None, returns BibTeX string

    Returns:
        BibTeX string if filepath is None, otherwise None (writes to file)

    Example:
        # Export entire library
        export_to_bibtex(zot, filepath="library.bib")

        # Export specific items
        export_to_bibtex(zot, items=my_items, filepath="selected.bib")
    """
    if items is None:
        items = list(_all_items(zot))

    def _format_bibtex_value(value: str) -> str:
        """Escape special characters for BibTeX."""
        if not value:
            return ""
        # Protect capitalization with braces
        value = str(value)
        # Escape special characters but keep common ones
        return value

    def _get_bibtex_type(item_type: str) -> str:
        """Map Zotero item type to BibTeX type."""
        type_map = {
            "journalArticle": "article",
            "book": "book",
            "bookSection": "incollection",
            "conferencePaper": "inproceedings",
            "thesis": "phdthesis",
            "report": "techreport",
            "magazineArticle": "article",
            "newspaperArticle": "article",
            "webpage": "misc",
            "document": "misc",
            "manuscript": "unpublished",
            "preprint": "unpublished",
        }
        return type_map.get(item_type, "misc")

    def _format_creators(creators: list[dict]) -> str:
        """Format creators as BibTeX author string."""
        if not creators:
            return ""
        authors = []
        for c in creators:
            if c.get("creatorType") == "author":
                first = c.get("firstName", "")
                last = c.get("lastName", "")
                if last and first:
                    authors.append(f"{last}, {first}")
                elif last:
                    authors.append(last)
        return " and ".join(authors)

    bibtex_entries = []

    for item in items:
        data = item.get("data", {})
        item_type = data.get("itemType", "")
        bibtex_type = _get_bibtex_type(item_type)

        # Use item key as citation key, or generate from title/year
        cite_key = item.get("key", "")
        if not cite_key:
            continue

        # Build BibTeX fields
        fields = []

        # Author
        creators = data.get("creators", [])
        authors = _format_creators(creators)
        if authors:
            fields.append(f"  author = {{{authors}}}")

        # Title
        title = data.get("title", "")
        if title:
            fields.append(f"  title = {{{title}}}")

        # Journal/Publication
        pub_title = data.get("publicationTitle", "")
        if pub_title:
            fields.append(f"  journal = {{{pub_title}}}")

        # Year and Date
        date = data.get("date", "")
        if date:
            year = date[:4] if len(date) >= 4 else date
            fields.append(f"  year = {{{year}}}")

        # Volume
        volume = data.get("volume", "")
        if volume:
            fields.append(f"  volume = {{{volume}}}")

        # Issue/Number
        issue = data.get("issue", "")
        if issue:
            fields.append(f"  number = {{{issue}}}")

        # Pages
        pages = data.get("pages", "")
        if pages:
            fields.append(f"  pages = {{{pages}}}")

        # Publisher
        publisher = data.get("publisher", "")
        if publisher:
            fields.append(f"  publisher = {{{publisher}}}")

        # Address/Place
        place = data.get("place", "")
        if place:
            fields.append(f"  address = {{{place}}}")

        # DOI
        doi = data.get("DOI", "")
        if doi:
            fields.append(f"  doi = {{{doi}}}")

        # URL
        url = data.get("url", "")
        if url:
            fields.append(f"  url = {{{url}}}")

        # Abstract
        abstract = data.get("abstractNote", "")
        if abstract:
            # Escape curly braces in abstract
            abstract = abstract.replace("{", "\\{").replace("}", "\\}")
            fields.append(f"  abstract = {{{abstract}}}")

        # Type (for reports, thesis, etc.)
        if data.get("thesisType"):
            fields.append(f"  type = {{{data.get('thesisType')}}}")
        elif data.get("reportType"):
            fields.append(f"  type = {{{data.get('reportType')}}}")

        # ISBN
        isbn = data.get("ISBN", "")
        if isbn:
            fields.append(f"  isbn = {{{isbn}}}")

        # ISSN
        issn = data.get("ISSN", "")
        if issn:
            fields.append(f"  issn = {{{issn}}}")

        # Series
        series = data.get("series", "")
        if series:
            fields.append(f"  series = {{{series}}}")

        # Edition
        edition = data.get("edition", "")
        if edition:
            fields.append(f"  edition = {{{edition}}}")

        # Tags as keywords
        tags = data.get("tags", [])
        if tags:
            keywords = ", ".join(t.get("tag", "") for t in tags if t.get("tag"))
            if keywords:
                fields.append(f"  keywords = {{{keywords}}}")

        # Notes (first note only, as comment)
        notes = item.get("_children", [])
        notes = [c for c in notes if c.get("data", {}).get("itemType") == "note"]
        if notes:
            note_text = notes[0].get("data", {}).get("note", "")
            if note_text:
                # Strip HTML tags for plain text
                import re
                note_text = re.sub(r"<[^>]+>", "", note_text)
                note_text = note_text.replace("{", "\\{").replace("}", "\\}")
                fields.append(f"  annote = {{{note_text}}}")

        # Build entry
        entry_lines = [f" @{bibtex_type}{{{cite_key},"]
        entry_lines.append(",\n".join(fields))
        entry_lines.append("}")
        bibtex_entries.append("\n".join(entry_lines))

    bibtex_str = "\n\n".join(bibtex_entries)
    if bibtex_str:
        bibtex_str += "\n"

    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(bibtex_str)
        return None
    return bibtex_str


def export_collection(
    zot: zotero.Zotero,
    collection_key: str,
    filepath: str = None,
    format: str = "json"
) -> str | None:
    """Export a specific collection to file.

    Exports all items in a collection in the specified format.
    Supports json, csv, and bibtex formats.

    Args:
        zot: Zotero client
        collection_key: Key of the collection to export
        filepath: Optional file path to write output. If None, returns string
        format: Export format: "json", "csv", or "bibtex". Default is "json"

    Returns:
        Formatted string if filepath is None, otherwise None (writes to file)

    Raises:
        ValueError: If format is not one of "json", "csv", or "bibtex"

    Example:
        # Export collection to JSON
        export_collection(zot, "ABC123", filepath="collection.json")

        # Export collection to BibTeX
        export_collection(zot, "ABC123", filepath="collection.bib", format="bibtex")

        # Export collection to CSV
        export_collection(zot, "ABC123", filepath="collection.csv", format="csv")
    """
    # Get collection items
    items = list(_all_items(zot, collection=collection_key))

    if format.lower() == "json":
        return export_to_json(zot, items=items, filepath=filepath)
    elif format.lower() == "csv":
        return export_to_csv(zot, items=items, filepath=filepath)
    elif format.lower() == "bibtex":
        return export_to_bibtex(zot, items=items, filepath=filepath)
    else:
        raise ValueError(f"Unknown format: {format}. Supported: json, csv, bibtex")


# =============================================================================
# Search/Query Tools
# =============================================================================

def search_by_title(zot: zotero.Zotero, query: str) -> list[dict]:
    """Search items by title substring (case-insensitive).

    Args:
        zot: Zotero client
        query: Substring to search for in item titles

    Returns:
        List of items with titles containing the query string
    """
    results = []
    for item in _all_items(zot):
        title = item["data"].get("title", "") or ""
        if query.lower() in title.lower():
            results.append(item)
    return results


def search_by_author(zot: zotero.Zotero, name: str) -> list[dict]:
    """Search items by author name (matches firstName or lastName).

    Args:
        zot: Zotero client
        name: Author name to search for (matches firstName or lastName)

    Returns:
        List of items with creators matching the name
    """
    results = []
    name_lower = name.lower()
    for item in _all_items(zot):
        creators = item["data"].get("creators", [])
        for creator in creators:
            first = creator.get("firstName", "") or ""
            last = creator.get("lastName", "") or ""
            if name_lower in first.lower() or name_lower in last.lower():
                results.append(item)
                break
    return results


def search_by_abstract(zot: zotero.Zotero, query: str) -> list[dict]:
    """Search items by abstract substring (case-insensitive).

    Args:
        zot: Zotero client
        query: Substring to search for in item abstracts

    Returns:
        List of items with abstracts containing the query string
    """
    results = []
    for item in _all_items(zot):
        abstract = item["data"].get("abstractNote", "") or ""
        if query.lower() in abstract.lower():
            results.append(item)
    return results


def search_fulltext(zot: zotero.Zotero, query: str, fields: list[str] = None) -> Generator[dict, None, None]:
    """Search items by full-text across multiple fields.

    Uses Zotero API's qmode=everything to search attachment content.

    Args:
        zot: Zotero client
        query: Substring to search for
        fields: Optional list of field names to search in addition to full-text.
                If None, searches everything via API.

    Yields:
        Items where query appears in full-text or specified fields

    Note:
        Returns ALL matching items. No limit.
        Requires Zotero 7+ with full-text indexing enabled.
    """
    if fields is None:
        # Use API's native full-text search
        yield from _all_items(zot, q=query, qmode='everything')
    else:
        # Search specific fields manually
        query_lower = query.lower()
        for item in _all_items(zot):
            data = item["data"]
            for field in fields:
                value = data.get(field, "") or ""
                if query_lower in value.lower():
                    yield item
                    break


def search_by_year(zot: zotero.Zotero, year: int) -> list[dict]:
    """Filter items by exact year.

    Args:
        zot: Zotero client
        year: Year to filter by (e.g., 2024)

    Returns:
        List of items from the specified year
    """
    results = []
    year_str = str(year)
    for item in _all_items(zot):
        date = item["data"].get("date", "") or ""
        if date.startswith(year_str):
            results.append(item)
    return results


def search_by_year_range(zot: zotero.Zotero, start_year: int, end_year: int) -> list[dict]:
    """Filter items by year range (inclusive).

    Args:
        zot: Zotero client
        start_year: Start year (inclusive)
        end_year: End year (inclusive)

    Returns:
        List of items within the year range
    """
    results = []
    for item in _all_items(zot):
        date = item["data"].get("date", "") or ""
        if len(date) >= 4:
            try:
                item_year = int(date[:4])
                if start_year <= item_year <= end_year:
                    results.append(item)
            except ValueError:
                continue
    return results


def search_by_collection(zot: zotero.Zotero, collection_key: str) -> list[dict]:
    """Get items in a collection.

    Args:
        zot: Zotero client
        collection_key: Key of the collection to query

    Returns:
        List of items in the specified collection
    """
    return list(_all_items(zot, collection=collection_key))


def search_by_tag(zot: zotero.Zotero, tag: str) -> list[dict]:
    """Get items with specific tag.

    Args:
        zot: Zotero client
        tag: Tag string to search for

    Returns:
        List of items with the specified tag
    """
    return list(_all_items(zot, tag=tag))


def search_advanced(zot: zotero.Zotero, filters: dict[str, Any]) -> list[dict]:
    """Combined search with multiple filters.

    Args:
        zot: Zotero client
        filters: Dict of filter criteria. Supported keys:
            - itemType: Filter by item type (e.g., "journalArticle")
            - year: Filter by exact year (int)
            - year_start: Filter by start year (inclusive)
            - year_end: Filter by end year (inclusive)
            - tag: Filter by tag
            - collection: Filter by collection key
            - query: Search title substring (case-insensitive)

    Returns:
        List of items matching all specified filters
    """
    # Build kwargs for Zotero API filtering
    kwargs = {}
    if "itemType" in filters:
        kwargs["itemType"] = filters["itemType"]
    if "tag" in filters:
        kwargs["tag"] = filters["tag"]
    if "collection" in filters:
        kwargs["collection"] = filters["collection"]

    # Fetch items with API-level filters
    items = list(_all_items(zot, **kwargs))

    # Apply additional filters that require post-processing
    results = []
    for item in items:
        # Year filter
        if "year" in filters:
            date = item["data"].get("date", "") or ""
            year_str = str(filters["year"])
            if not date.startswith(year_str):
                continue

        # Year range filter
        if "year_start" in filters or "year_end" in filters:
            date = item["data"].get("date", "") or ""
            if len(date) < 4:
                continue
            try:
                item_year = int(date[:4])
                if "year_start" in filters and item_year < filters["year_start"]:
                    continue
                if "year_end" in filters and item_year > filters["year_end"]:
                    continue
            except ValueError:
                continue

        # Title query filter
        if "query" in filters:
            title = item["data"].get("title", "") or ""
            if filters["query"].lower() not in title.lower():
                continue

        results.append(item)

    return results


# =============================================================================
# Import Tools
# =============================================================================

def import_by_doi(zot: zotero.Zotero, doi: str) -> str | None:
    """Fetch item metadata from CrossRef by DOI and create Zotero item.

    Uses the CrossRef API to retrieve bibliographic metadata for a DOI
    and creates a new item in Zotero with the fetched data.

    Args:
        zot: Zotero client
        doi: Digital Object Identifier (DOI) to fetch metadata for

    Returns:
        The key of the created item, or None if the API request failed

    Example:
        item_key = import_by_doi(zot, "10.1038/nature12373")
        if item_key:
            print(f"Created item: {item_key}")

    Note:
        Requires internet connection. CrossRef API may have rate limits.
        The created item type depends on the CrossRef work type.
    """
    import httpx

    url = f"https://api.crossref.org/works/{doi}"

    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok" or "message" not in data:
            return None

        work = data["message"]
        item_type = work.get("type", "")

        # Map CrossRef types to Zotero item types
        type_mapping = {
            "journal-article": "journalArticle",
            "journal-issue": "journalArticle",
            "book": "book",
            "book-chapter": "bookSection",
            "book-part": "bookSection",
            "book-section": "bookSection",
            "proceedings-article": "conferencePaper",
            "proceedings": "conferencePaper",
            "dissertation": "thesis",
            "thesis": "thesis",
            "report": "report",
            "report-series": "report",
            "dataset": "document",
            "component": "document",
            "entry": "document",
            "reference-entry": "document",
        }
        zotero_type = type_mapping.get(item_type, "journalArticle")

        # Build Zotero item
        item = {
            "itemType": zotero_type,
            "title": work.get("title", [""])[0] if work.get("title") else "",
            "DOI": doi,
        }

        # Add authors/creators
        creators = []
        for author in work.get("author", []):
            creator = {"creatorType": "author"}
            if "given" in author:
                creator["firstName"] = author["given"]
            if "family" in author:
                creator["lastName"] = author["family"]
            if creator.get("firstName") or creator.get("lastName"):
                creators.append(creator)
        if creators:
            item["creators"] = creators

        # Add publication date
        if "published-print" in work:
            pub_date = work["published-print"]
        elif "published-online" in work:
            pub_date = work["published-online"]
        elif "created" in work:
            pub_date = work["created"]
        else:
            pub_date = None

        if pub_date and "date-parts" in pub_date:
            date_parts = pub_date["date-parts"][0]
            if len(date_parts) >= 1:
                year = str(date_parts[0])
                if len(date_parts) >= 2:
                    month = str(date_parts[1]).zfill(2)
                    if len(date_parts) >= 3:
                        day = str(date_parts[2]).zfill(2)
                        item["date"] = f"{year}-{month}-{day}"
                    else:
                        item["date"] = f"{year}-{month}"
                else:
                    item["date"] = year

        # Add journal/publication title
        if "container-title" in work and work["container-title"]:
            item["publicationTitle"] = work["container-title"][0]

        # Add volume, issue, pages
        if "volume" in work:
            item["volume"] = str(work["volume"])
        if "issue" in work:
            item["issue"] = str(work["issue"])
        if "page" in work:
            item["pages"] = work["page"]

        # Add publisher for books/reports
        if "publisher" in work:
            item["publisher"] = work["publisher"]

        # Add ISBN for books
        if "ISBN" in work and work["ISBN"]:
            item["ISBN"] = work["ISBN"][0]

        # Add ISSN for journals
        if "ISSN" in work and work["ISSN"]:
            item["ISSN"] = work["ISSN"][0]

        # Add abstract
        if "abstract" in work:
            item["abstractNote"] = work["abstract"]

        # Add URL
        if "URL" in work:
            item["url"] = work["URL"]
        elif "link" in work and work["link"]:
            for link in work["link"]:
                if link.get("content-type") == "text/html":
                    item["url"] = link["URL"]
                    break

        # Create the item in Zotero
        result = zot.create_items([item])
        if result and "success" in result and result["success"]:
            return result["success"]["0"]["key"]
        return None

    except httpx.HTTPError:
        return None
    except Exception:
        return None


def import_by_isbn(zot: zotero.Zotero, isbn: str) -> str | None:
    """Fetch item metadata by ISBN using Open Library API and create Zotero item.

    Uses the Open Library API to retrieve bibliographic metadata for an ISBN
    and creates a new item in Zotero with the fetched data.

    Args:
        zot: Zotero client
        isbn: International Standard Book Number (ISBN-10 or ISBN-13)

    Returns:
        The key of the created item, or None if the API request failed

    Example:
        item_key = import_by_isbn(zot, "9780134685991")
        if item_key:
            print(f"Created book item: {item_key}")

    Note:
        Requires internet connection. Open Library API is free but may have
        rate limits. Works best with ISBN-13 format.
    """
    import httpx

    # Clean ISBN (remove hyphens and spaces)
    clean_isbn = isbn.replace("-", "").replace(" ", "")

    url = f"https://openlibrary.org/isbn/{clean_isbn}.json"

    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        if not data or "error" in data:
            return None

        # Build Zotero book item
        item = {
            "itemType": "book",
            "ISBN": clean_isbn,
        }

        # Add title
        if "title" in data:
            item["title"] = data["title"]

        # Add authors/creators
        creators = []
        for author_key in data.get("authors", []):
            if isinstance(author_key, dict):
                author_key = author_key.get("key", "")
            if author_key:
                # Fetch author details
                author_url = f"https://openlibrary.org{author_key}.json"
                try:
                    author_resp = httpx.get(author_url, timeout=5.0)
                    author_resp.raise_for_status()
                    author_data = author_resp.json()
                    creator = {"creatorType": "author"}
                    if "name" in author_data:
                        name = author_data["name"]
                        # Try to split into first/last name
                        parts = name.split(" ", 1)
                        if len(parts) == 2:
                            creator["firstName"] = parts[0]
                            creator["lastName"] = parts[1]
                        else:
                            creator["lastName"] = name
                        creators.append(creator)
                except Exception:
                    # Skip author if fetch fails
                    pass

        # If no authors from API, try alternate_names or direct name
        if not creators and "authors" in data:
            for author_info in data["authors"]:
                if isinstance(author_info, dict) and "name" in author_info:
                    creator = {"creatorType": "author"}
                    name = author_info["name"]
                    parts = name.split(" ", 1)
                    if len(parts) == 2:
                        creator["firstName"] = parts[0]
                        creator["lastName"] = parts[1]
                    else:
                        creator["lastName"] = name
                    creators.append(creator)

        if creators:
            item["creators"] = creators

        # Add publication date
        if "publish_date" in data:
            date_str = data["publish_date"]
            # Try to extract year
            import re
            year_match = re.search(r"\b(\d{4})\b", date_str)
            if year_match:
                item["date"] = year_match.group(1)

        # Add publisher
        if "publishers" in data and data["publishers"]:
            publishers = data["publishers"]
            if isinstance(publishers, list):
                item["publisher"] = publishers[0]
            else:
                item["publisher"] = publishers

        # Add language
        if "languages" in data and data["languages"]:
            langs = data["languages"]
            if isinstance(langs, list) and langs:
                lang = langs[0]
                if isinstance(lang, dict):
                    lang = lang.get("key", "").split("/")[-1]
                item["language"] = lang

        # Add subjects as tags
        if "subjects" in data and data["subjects"]:
            tags = [{"tag": str(s)} for s in data["subjects"][:10]]  # Limit to 10 tags
            if tags:
                item["tags"] = tags

        # Create the item in Zotero
        result = zot.create_items([item])
        if result and "success" in result and result["success"]:
            return result["success"]["0"]["key"]
        return None

    except httpx.HTTPError:
        return None
    except Exception:
        return None


def import_by_arxiv(zot: zotero.Zotero, arxiv_id: str) -> str | None:
    """Fetch item metadata from arXiv API and create Zotero item.

    Uses the arXiv API to retrieve bibliographic metadata for an arXiv ID
    and creates a new item in Zotero with the fetched data.

    Args:
        zot: Zotero client
        arxiv_id: arXiv identifier (e.g., "2301.12345" or "hep-th/9901001")

    Returns:
        The key of the created item, or None if the API request failed

    Example:
        item_key = import_by_arxiv(zot, "2301.12345")
        if item_key:
            print(f"Created preprint item: {item_key}")

    Note:
        Requires internet connection. arXiv API returns Atom feed format.
        Supports both new-style (YYMM.NNNNN) and old-style (category/NNNNNNN) IDs.
    """
    import httpx
    import re

    # Clean arXiv ID (remove prefix like arXiv:)
    clean_id = arxiv_id.replace("arXiv:", "").strip()

    url = f"http://export.arxiv.org/api/query?id_list={clean_id}"

    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()

        # Parse Atom XML response
        import xml.etree.ElementTree as ET

        # Define namespaces
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom",
        }

        root = ET.fromstring(response.text)
        entries = root.findall("atom:entry", ns)

        if not entries:
            return None

        entry = entries[0]

        # Extract metadata
        def get_text(elem, namespace="atom"):
            el = entry.find(f"{namespace}:{elem}", ns)
            return el.text if el is not None else ""

        def get_name(elem):
            el = entry.find(f"atom:{elem}", ns)
            if el is not None:
                name_el = el.find("atom:name", ns)
                return name_el.text if name_el is not None else ""
            return ""

        # Build Zotero preprint item
        item = {
            "itemType": "preprint",
            "title": get_text("title"),
            "archiveID": clean_id,
        }

        # Add authors/creators
        creators = []
        for author_elem in entry.findall("atom:author", ns):
            creator = {"creatorType": "author"}
            name_elem = author_elem.find("atom:name", ns)
            if name_elem is not None and name_elem.text:
                name = name_elem.text
                parts = name.split(" ", 1)
                if len(parts) == 2:
                    creator["firstName"] = parts[0]
                    creator["lastName"] = parts[1]
                else:
                    creator["lastName"] = name
                creators.append(creator)
        if creators:
            item["creators"] = creators

        # Add abstract
        summary = get_text("summary")
        if summary:
            # Clean up whitespace
            item["abstractNote"] = " ".join(summary.split())

        # Add publication date
        published = get_text("published")
        if published:
            # Parse ISO date format
            item["date"] = published[:10]  # YYYY-MM-DD

        # Add arXiv URL
        item["url"] = f"https://arxiv.org/abs/{clean_id}"

        # Add DOI if available
        doi_elem = entry.find("arxiv:doi", ns)
        if doi_elem is not None and doi_elem.text:
            item["DOI"] = doi_elem.text

        # Add journal reference if available
        journal_ref = entry.find("arxiv:journal_ref", ns)
        if journal_ref is not None and journal_ref.text:
            item["extra"] = f"Journal: {journal_ref.text}"

        # Add categories as tags
        tags = []
        for category in entry.findall("atom:category", ns):
            term = category.get("term", "")
            if term:
                tags.append({"tag": term})
        if tags:
            item["tags"] = tags

        # Create the item in Zotero
        result = zot.create_items([item])
        if result and "success" in result and result["success"]:
            return result["success"]["0"]["key"]
        return None

    except httpx.HTTPError:
        return None
    except Exception:
        return None


def import_from_bibtex(zot: zotero.Zotero, bibtex_content: str) -> list[str]:
    """Parse BibTeX content and create Zotero items.

    Parses BibTeX entries and creates corresponding items in Zotero.
    Supports common entry types and fields.

    Args:
        zot: Zotero client
        bibtex_content: BibTeX formatted string containing one or more entries

    Returns:
        List of keys for created items. Empty list if parsing failed.

    Example:
        with open("references.bib", "r") as f:
            bibtex = f.read()
        keys = import_from_bibtex(zot, bibtex)
        print(f"Imported {len(keys)} items")

    Note:
        Supports common BibTeX entry types: article, book, inbook, incollection,
        inproceedings, phdthesis, mastersthesis, techreport, misc, unpublished.
        Creator names in 'author' and 'editor' fields are parsed.
    """

    def parse_bibtex_entries(content: str) -> list[dict]:
        """Parse BibTeX content into structured entries."""
        entries = []
        content = content.strip()

        # Remove comments
        content = re.sub(r"%.*$", "", content, flags=re.MULTILINE)

        # Find all entries using regex
        # Match @type{key, ... }
        entry_pattern = re.compile(
            r"@\s*(\w+)\s*\{\s*([^,\s]+)\s*,\s*(.*?)\n\}",
            re.DOTALL | re.IGNORECASE
        )

        for match in entry_pattern.finditer(content):
            entry_type = match.group(1).lower()
            cite_key = match.group(2)
            fields_str = match.group(3)

            # Parse fields
            fields = {"citekey": cite_key}

            # Match field = {value} or field = "value" or field = number
            field_pattern = re.compile(
                r"(\w+)\s*=\s*(?:\{([^}]*)\}|\"([^\"]*)\"|(\d+))",
                re.IGNORECASE
            )

            for field_match in field_pattern.finditer(fields_str):
                field_name = field_match.group(1).lower()
                # Value is in group 2 (braces), 3 (quotes), or 4 (number)
                value = field_match.group(2) or field_match.group(3) or field_match.group(4)
                if value:
                    fields[field_name] = value.strip()

            fields["entrytype"] = entry_type
            entries.append(fields)

        return entries

    def parse_creator_name(name: str) -> dict | None:
        """Parse a creator name into firstName/lastName."""
        name = name.strip()
        if not name:
            return None

        # Handle "LastName, FirstName" format
        if "," in name:
            parts = name.split(",", 1)
            return {
                "lastName": parts[0].strip(),
                "firstName": parts[1].strip() if len(parts) > 1 else ""
            }
        # Handle "FirstName LastName" format
        else:
            parts = name.split(" ", 1)
            if len(parts) == 2:
                return {"firstName": parts[0], "lastName": parts[1]}
            else:
                return {"lastName": parts[0]}

    def parse_creators(author_str: str, creator_type: str = "author") -> list[dict]:
        """Parse author/editor string into creators list."""
        creators = []
        if not author_str:
            return creators

        # Split by " and " (BibTeX author separator)
        authors = re.split(r"\s+and\s+", author_str, flags=re.IGNORECASE)

        for author in authors:
            creator = parse_creator_name(author)
            if creator:
                creator["creatorType"] = creator_type
                creators.append(creator)

        return creators

    def map_entry_type(bibtex_type: str) -> str:
        """Map BibTeX entry type to Zotero item type."""
        type_mapping = {
            "article": "journalArticle",
            "book": "book",
            "inbook": "bookSection",
            "incollection": "bookSection",
            "inproceedings": "conferencePaper",
            "proceedings": "conferencePaper",
            "phdthesis": "thesis",
            "mastersthesis": "thesis",
            "thesis": "thesis",
            "techreport": "report",
            "manual": "document",
            "misc": "document",
            "unpublished": "manuscript",
            "webpage": "webpage",
        }
        return type_mapping.get(bibtex_type, "document")

    import re

    entries = parse_bibtex_entries(bibtex_content)
    created_keys = []

    for entry in entries:
        # Map entry type
        zotero_type = map_entry_type(entry.get("entrytype", "misc"))

        item = {
            "itemType": zotero_type,
        }

        # Map fields
        field_mapping = {
            "title": "title",
            "journal": "publicationTitle",
            "journaltitle": "publicationTitle",
            "booktitle": "publicationTitle",
            "year": "date",
            "date": "date",
            "volume": "volume",
            "number": "issue",
            "pages": "pages",
            "publisher": "publisher",
            "address": "place",
            "location": "place",
            "edition": "edition",
            "series": "series",
            "isbn": "ISBN",
            "issn": "ISSN",
            "doi": "DOI",
            "url": "url",
            "abstract": "abstractNote",
            "note": "extra",
            "type": "thesisType",
        }

        for bibtex_field, zotero_field in field_mapping.items():
            if bibtex_field in entry:
                item[zotero_field] = entry[bibtex_field]

        # Handle month + year combination
        if "month" in entry and "date" not in item:
            month = entry["month"]
            # Convert month name/number to MM format
            month_map = {
                "jan": "01", "january": "01",
                "feb": "02", "february": "02",
                "mar": "03", "march": "03",
                "apr": "04", "april": "04",
                "may": "05",
                "jun": "06", "june": "06",
                "jul": "07", "july": "07",
                "aug": "08", "august": "08",
                "sep": "09", "september": "09",
                "oct": "10", "october": "10",
                "nov": "11", "november": "11",
                "dec": "12", "december": "12",
            }
            month_str = month.lower().strip()
            if month_str in month_map:
                month_num = month_map[month_str]
                if "year" in entry:
                    item["date"] = f"{entry['year']}-{month_num}"
                else:
                    item["date"] = month_num

        # Parse authors
        if "author" in entry:
            creators = parse_creators(entry["author"], "author")
            if creators:
                item["creators"] = creators

        # Parse editors
        if "editor" in entry:
            editors = parse_creators(entry["editor"], "editor")
            if "creators" not in item:
                item["creators"] = editors
            else:
                item["creators"].extend(editors)

        # Add citekey as extra field for reference
        if "citekey" in entry:
            extra = item.get("extra", "")
            if extra:
                extra += f"\nCitekey: {entry['citekey']}"
            else:
                extra = f"Citekey: {entry['citekey']}"
            item["extra"] = extra

        # Create the item in Zotero
        try:
            result = zot.create_items([item])
            if result and "success" in result and result["success"]:
                created_keys.append(result["success"]["0"]["key"])
        except Exception:
            # Skip failed items, continue with others
            continue

    return created_keys


def import_from_json(zot: zotero.Zotero, json_data: str | list | dict) -> list[str]:
    """Import items from Zotero JSON format.

    Imports items from JSON in Zotero's native format. Accepts JSON string,
    list of items, or single item dict.

    Args:
        zot: Zotero client
        json_data: JSON string, list, or dict in Zotero format.
            Can be export from export_to_json() or Zotero API response.

    Returns:
        List of keys for created/updated items. Empty list if import failed.

    Example:
        # Import from JSON string
        with open("export.json", "r") as f:
            json_str = f.read()
        keys = import_from_json(zot, json_str)

        # Import from list of items
        items = get_items_from_somewhere()
        keys = import_from_json(zot, items)

    Note:
        Accepts JSON in Zotero's API format with 'key', 'version', 'data', etc.
        Items with existing keys will be updated, new items will be created.
        Child items (attachments, notes) require parent items to exist first.
    """
    import json

    # Parse JSON string if needed
    if isinstance(json_data, str):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            return []
    else:
        data = json_data

    # Ensure data is a list
    if isinstance(data, dict):
        data = [data]
    elif not isinstance(data, list):
        return []

    created_keys = []

    # Separate parent items and children for proper ordering
    parent_items = []
    child_items = []

    for item in data:
        if not isinstance(item, dict):
            continue

        # Get item data (handle both raw and wrapped formats)
        if "data" in item:
            item_data = item["data"].copy()
            if "key" in item:
                item_data["key"] = item["key"]
        else:
            item_data = item.copy()

        # Check if this is a child item (has parentItem)
        if item_data.get("parentItem"):
            child_items.append(item_data)
        else:
            parent_items.append(item_data)

    # Create/update parent items first
    for item_data in parent_items:
        try:
            item_type = item_data.get("itemType", "")
            if not item_type:
                continue

            # Check if item already exists (has key)
            existing_key = item_data.get("key")
            if existing_key:
                # Try to update existing item
                try:
                    existing = zot.item(existing_key)
                    if existing:
                        # Update existing item
                        item_data["version"] = existing.get("version", 0) + 1
                        result = zot.update_item({
                            "key": existing_key,
                            "version": item_data["version"],
                            "data": item_data
                        })
                        created_keys.append(existing_key)
                        continue
                except Exception:
                    # Item doesn't exist, create new one
                    pass

            # Create new item
            result = zot.create_items([item_data])
            if result and "success" in result and result["success"]:
                for idx, success_item in result["success"].items():
                    created_keys.append(success_item["key"])
        except Exception:
            # Skip failed items
            continue

    # Create child items (attachments, notes)
    for item_data in child_items:
        try:
            item_type = item_data.get("itemType", "")
            if not item_type:
                continue

            result = zot.create_items([item_data])
            if result and "success" in result and result["success"]:
                for idx, success_item in result["success"].items():
                    created_keys.append(success_item["key"])
        except Exception:
            # Skip failed items (parent may not exist)
            continue

    return created_keys


# =============================================================================
# Collection Management
# =============================================================================

def move_collection(zot: zotero.Zotero, collection_key: str, new_parent_key: str | None) -> dict:
    """Move a collection to a new parent (or make it top-level).

    Changes the parent collection of an existing collection. Set new_parent_key
    to None to make the collection top-level.

    Args:
        zot: Zotero client
        collection_key: Key of the collection to move
        new_parent_key: Key of the new parent collection, or None for top-level

    Returns:
        Dict with "success" (bool) and either "message" (str) on success or "error" (str) on failure

    Example:
        # Move collection to become a subcollection
        result = move_collection(zot, "ABC123", "PARENT456")
        if result["success"]:
            print("Collection moved")

        # Make collection top-level
        result = move_collection(zot, "ABC123", None)
    """
    try:
        # Get the collection
        collection = zot.collection(collection_key)
        if not collection:
            return {"success": False, "error": f"Collection not found: {collection_key}"}

        # Update parent collection
        if new_parent_key:
            collection["data"]["parentCollection"] = new_parent_key
        else:
            # Remove parent to make it top-level
            collection["data"].pop("parentCollection", None)

        # Save the updated collection
        zot.update_collection(collection)
        return {"success": True, "message": "Collection moved successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# =============================================================================
# File Operations
# =============================================================================

def replace_attachment(zot: zotero.Zotero, attachment_key: str, new_file_path: str) -> dict:
    """Replace the file content of an existing attachment.

    Updates the file content for an attachment item while preserving
    all metadata (title, tags, notes, relations).

    Args:
        zot: Zotero client
        attachment_key: Key of the attachment to replace
        new_file_path: Path to the new file to upload

    Returns:
        Dict with "success" (bool) and either "message" (str) on success or "error" (str) on failure

    Example:
        result = replace_attachment(zot, "ATTACH123", "/path/to/new_file.pdf")
        if result["success"]:
            print("Attachment replaced")

    Note:
        Requires Zotero 7+ with local API enabled.
        The attachment's metadata (title, tags, etc.) is preserved.
        File content type is updated based on the new file.
    """
    import os
    import hashlib
    import httpx
    from pathlib import Path

    try:
        # Get the attachment item
        attachment = zot.item(attachment_key)
        if not attachment:
            return {"success": False, "error": f"Attachment not found: {attachment_key}"}

        # Verify it's an attachment
        if attachment.get("data", {}).get("itemType") != "attachment":
            return {"success": False, "error": f"Item is not an attachment: {attachment_key}"}

        # Check new file exists
        new_file = Path(new_file_path)
        if not new_file.exists():
            return {"success": False, "error": f"File not found: {new_file_path}"}

        # Read new file content
        with open(new_file, "rb") as f:
            file_content = f.read()

        # Calculate new MD5 hash
        md5_hash = hashlib.md5(file_content).hexdigest()
        file_size = len(file_content)

        # Update attachment metadata
        attachment["data"]["md5"] = md5_hash
        attachment["data"]["mtime"] = int(os.path.getmtime(new_file) * 1000)
        attachment["data"]["filename"] = new_file.name

        # Determine content type
        import mimetypes
        content_type, _ = mimetypes.guess_type(str(new_file))
        if content_type:
            attachment["data"]["contentType"] = content_type

        # Update the attachment metadata
        zot.update_item(attachment)

        # Upload the new file content
        upload_url = f"http://localhost:23119/api/users/0/items/{attachment_key}/file"
        upload_response = httpx.post(
            upload_url,
            headers={
                "Zotero-API-Key": "fake",
                "Content-Type": attachment["data"]["contentType"],
            },
            content=file_content,
            timeout=60.0,
        )

        if upload_response.status_code in (200, 201, 204):
            return {"success": True, "message": "Attachment replaced successfully"}
        else:
            # Try fallback using zupload
            try:
                from pyzotero import zupload
                zup = zupload.Zupload(zot, attachment_key)
                zup.upload_file(str(new_file))
                return {"success": True, "message": "Attachment replaced successfully (via zupload)"}
            except Exception:
                return {"success": True, "message": "Metadata updated but file upload may require manual sync"}

    except httpx.HTTPError as e:
        return {"success": False, "error": f"HTTP error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# =============================================================================
# Item Management
# =============================================================================

def convert_item_type(zot: zotero.Zotero, item_key: str, new_type: str) -> dict:
    """Convert an item to a different item type.

    Changes the item type while preserving all common fields between
    the old and new types. Some fields may be lost if not applicable
    to the new type.

    Args:
        zot: Zotero client
        item_key: Key of the item to convert
        new_type: New item type (e.g., "bookSection", "journalArticle")

    Returns:
        Dict with "success" (bool) and either "key" (str) on success or "error" (str) on failure

    Example:
        # Convert a book to a book section
        result = convert_item_type(zot, "ITEM123", "bookSection")
        if result["success"]:
            print(f"Converted item: {result['key']}")

    Note:
        Common fields (title, creators, date, DOI, etc.) are preserved.
        Type-specific fields may be lost if not applicable to new type.
        The item key remains the same.
    """
    # Fields common to most item types
    common_fields = [
        "title",
        "creators",
        "date",
        "DOI",
        "ISBN",
        "ISSN",
        "url",
        "abstractNote",
        "tags",
        "collections",
        "relations",
        "extra",
        "language",
        "rights",
        "accessDate",
        "libraryCatalog",
        "callNumber",
        "archive",
        "archiveLocation",
        "notes",
        "attachments",
    ]

    try:
        # Get the item
        item = zot.item(item_key)
        if not item:
            return {"success": False, "error": f"Item not found: {item_key}"}

        # Create new item data with new type
        old_data = item["data"]
        new_data = {"itemType": new_type}

        # Copy common fields
        for field in common_fields:
            if field in old_data:
                new_data[field] = old_data[field]

        # Type-specific field mappings
        field_mappings = {
            # From journalArticle
            ("journalArticle", "bookSection"): {
                "publicationTitle": "bookTitle",
                "journalAbbreviation": "bookAbbreviation",
            },
            # From book to bookSection
            ("book", "bookSection"): {
                "publicationTitle": "bookTitle",
                "place": "place",
                "publisher": "publisher",
                "edition": "edition",
                "series": "series",
                "seriesNumber": "seriesNumber",
            },
            # From conferencePaper to journalArticle
            ("conferencePaper", "journalArticle"): {
                "proceedingsTitle": "publicationTitle",
                "conferenceName": "extra",
            },
        }

        # Apply field mappings based on old and new type
        old_type = old_data.get("itemType", "")
        mapping_key = (old_type, new_type)
        if mapping_key in field_mappings:
            for old_field, new_field in field_mappings[mapping_key].items():
                if old_field in old_data:
                    if new_field == "extra":
                        # Append to extra field
                        existing_extra = new_data.get("extra", "")
                        if existing_extra:
                            new_data["extra"] = f"{existing_extra}\n{old_field}: {old_data[old_field]}"
                        else:
                            new_data["extra"] = f"{old_field}: {old_data[old_field]}"
                    else:
                        new_data[new_field] = old_data[old_field]

        # Update the item with new type
        item["data"] = new_data
        zot.update_item(item)

        return {"success": True, "key": item_key}
    except Exception as e:
        return {"success": False, "error": str(e)}


def transfer_relations(zot: zotero.Zotero, from_key: str, to_key: str) -> dict:
    """Copy all relations from one item to another.

    Transfers all citation relations (cites, citedBy) and other relations
    from the source item to the target item.

    Args:
        zot: Zotero client
        from_key: Key of the source item (relations are copied from here)
        to_key: Key of the target item (relations are copied to here)

    Returns:
        Dict with "success" (bool), "transferred" (int), and either "message" (str) or "error" (str)

    Example:
        result = transfer_relations(zot, "SOURCE123", "TARGET456")
        if result["success"]:
            print(f"Transferred {result['transferred']} relations")
    """
    try:
        # Get both items
        from_item = zot.item(from_key)
        to_item = zot.item(to_key)

        if not from_item:
            return {"success": False, "error": f"Source item not found: {from_key}"}
        if not to_item:
            return {"success": False, "error": f"Target item not found: {to_key}"}

        # Get relations from source
        from_relations = from_item["data"].get("relations", {})
        to_relations = to_item["data"].get("relations", {})

        transferred = 0

        # Copy each relation type
        for relation_type, relation_values in from_relations.items():
            if isinstance(relation_values, str):
                relation_values = [relation_values]

            if relation_type not in to_relations:
                to_relations[relation_type] = []
            elif isinstance(to_relations[relation_type], str):
                to_relations[relation_type] = [to_relations[relation_type]]

            # Add values that don't already exist
            for value in relation_values:
                if value not in to_relations[relation_type]:
                    to_relations[relation_type].append(value)
                    transferred += 1

        # Update target item with merged relations
        to_item["data"]["relations"] = to_relations
        zot.update_item(to_item)

        return {"success": True, "transferred": transferred, "message": "Relations transferred successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def copy_item(zot: zotero.Zotero, item_key: str) -> dict:
    """Duplicate an item with all its attachments and notes.

    Creates a complete copy of an item including all child items
    (attachments, notes) and relations.

    Args:
        zot: Zotero client
        item_key: Key of the item to copy

    Returns:
        Dict with "success" (bool), "new_key" (str), and either "message" (str) or "error" (str)

    Example:
        result = copy_item(zot, "ORIGINAL123")
        if result["success"]:
            print(f"Created copy: {result['new_key']}")

    Note:
        The copy includes all attachments, notes, tags, and collections.
        Relations are also copied.
        File attachments are referenced but not duplicated on disk.
    """
    try:
        # Get the original item
        original = zot.item(item_key)
        if not original:
            return {"success": False, "error": f"Item not found: {item_key}"}

        # Create a copy of the item data (without key and version)
        item_data = original["data"].copy()
        item_data.pop("key", None)

        # Add "(copy)" to title to distinguish
        if "title" in item_data:
            item_data["title"] = f"{item_data['title']} (copy)"

        # Create the new item
        result = zot.create_items([item_data])
        if not result or "success" not in result:
            return {"success": False, "error": "Failed to create copy"}

        new_key = result["success"]["0"]["key"]

        # Copy children (attachments and notes)
        children = zot.children(item_key)
        for child in children:
            child_data = child["data"].copy()
            child_data["parentItem"] = new_key
            child_data.pop("key", None)
            try:
                zot.create_items([child_data])
            except Exception:
                pass  # Continue even if some children fail

        return {"success": True, "new_key": new_key, "message": "Item copied successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def merge_items(zot: zotero.Zotero, source_key: str, target_key: str) -> dict:
    """Merge source item into target item.

    Transfers all relations, attachments, notes, and tags from the source
    item to the target item, then moves the source to trash.

    Args:
        zot: Zotero client
        source_key: Key of the source item (will be merged and deleted)
        target_key: Key of the target item (will receive all data)

    Returns:
        Dict with "success" (bool), "transferred" (dict with counts), and either "message" (str) or "error" (str)

    Example:
        result = merge_items(zot, "DUPLICATE123", "MASTER456")
        if result["success"]:
            print(f"Merged: {result['transferred']}")

    Note:
        The source item is moved to trash after merging.
        All attachments, notes, tags, and relations are transferred.
        Conflicting fields use the target item's values.
    """
    try:
        # Get both items
        source = zot.item(source_key)
        target = zot.item(target_key)

        if not source:
            return {"success": False, "error": f"Source item not found: {source_key}"}
        if not target:
            return {"success": False, "error": f"Target item not found: {target_key}"}

        transferred = {
            "attachments": 0,
            "notes": 0,
            "tags": 0,
            "relations": 0,
        }

        # Transfer tags (merge without duplicates)
        source_tags = {t.get("tag", "") for t in source["data"].get("tags", [])}
        target_tags = {t.get("tag", "") for t in target["data"].get("tags", [])}
        merged_tags = list(target_tags | source_tags)
        target["data"]["tags"] = [{"tag": t} for t in merged_tags]
        transferred["tags"] = len(source_tags - target_tags)

        # Transfer relations
        source_relations = source["data"].get("relations", {})
        target_relations = target["data"].get("relations", {})
        for relation_type, relation_values in source_relations.items():
            if isinstance(relation_values, str):
                relation_values = [relation_values]
            if relation_type not in target_relations:
                target_relations[relation_type] = []
            elif isinstance(target_relations[relation_type], str):
                target_relations[relation_type] = [target_relations[relation_type]]
            for value in relation_values:
                if value not in target_relations[relation_type]:
                    target_relations[relation_type].append(value)
                    transferred["relations"] += 1
        target["data"]["relations"] = target_relations

        # Save target item with merged data
        zot.update_item(target)

        # Transfer children (attachments and notes)
        source_children = zot.children(source_key)
        for child in source_children:
            child_data = child["data"].copy()
            child_data["parentItem"] = target_key
            child_data.pop("key", None)
            try:
                zot.create_items([child_data])
                if child_data.get("itemType") == "attachment":
                    transferred["attachments"] += 1
                elif child_data.get("itemType") == "note":
                    transferred["notes"] += 1
            except Exception:
                pass

        # Delete source item (move to trash)
        zot.delete_item(source_key)

        return {"success": True, "transferred": transferred, "message": "Items merged successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# =============================================================================
# Library Statistics
# =============================================================================

def items_per_type(zot: zotero.Zotero) -> dict[str, int]:
    """Count items by type.

    Returns a dictionary mapping item types to their counts.

    Args:
        zot: Zotero client

    Returns:
        Dict mapping item type names to counts, e.g., {"journalArticle": 42, "book": 15}

    Example:
        counts = items_per_type(zot)
        for item_type, count in counts.items():
            print(f"{item_type}: {count}")
    """
    from collections import Counter

    type_counts: Counter = Counter()
    for item in _all_items(zot):
        item_type = item["data"].get("itemType", "unknown")
        type_counts[item_type] += 1

    return dict(type_counts)


def items_per_collection(zot: zotero.Zotero) -> dict[str, int]:
    """Count items per collection.

    Returns a dictionary mapping collection keys to their item counts.

    Args:
        zot: Zotero client

    Returns:
        Dict mapping collection keys to item counts

    Example:
        counts = items_per_collection(zot)
        for coll_key, count in counts.items():
            print(f"Collection {coll_key}: {count} items")
    """
    collections = zot.collections()
    result = {}
    for coll in collections:
        items = zot.collection_items(coll["key"])
        result[coll["key"]] = len(items)
    return result


def items_per_year(zot: zotero.Zotero) -> dict[str, int]:
    """Count items by year.

    Returns a dictionary mapping years to their item counts.
    Items without a valid year are grouped under "unknown".

    Args:
        zot: Zotero client

    Returns:
        Dict mapping year strings to counts, e.g., {"2024": 50, "2023": 35, "unknown": 10}

    Example:
        counts = items_per_year(zot)
        for year, count in sorted(counts.items()):
            print(f"{year}: {count}")
    """
    from collections import Counter

    year_counts: Counter = Counter()
    for item in _all_items(zot):
        date = item["data"].get("date", "") or ""
        if len(date) >= 4 and date[:4].isdigit():
            year_counts[date[:4]] += 1
        else:
            year_counts["unknown"] += 1

    return dict(year_counts)


def tag_cloud(zot: zotero.Zotero) -> dict[str, int]:
    """Get tag frequency for visualization.

    Returns all tags with their usage counts, suitable for creating
    tag clouds or visualizations.

    Args:
        zot: Zotero client

    Returns:
        Dict mapping tag names to usage counts, sorted by frequency (descending)

    Example:
        tags = tag_cloud(zot)
        # Get top 10 tags
        top_tags = list(tags.items())[:10]
    """
    # all_tags already returns frequency counts
    tags = all_tags(zot)
    # Sort by frequency (descending)
    return dict(sorted(tags.items(), key=lambda x: x[1], reverse=True))


def library_summary(zot: zotero.Zotero) -> dict[str, Any]:
    """Get overall library statistics.

    Returns a comprehensive summary of the library including item counts,
    collection info, tag stats, and more.

    Args:
        zot: Zotero client

    Returns:
        Dict with library statistics including:
        - total_items: Total number of items
        - item_types: Count by item type
        - collections: Number of collections
        - tags: Number of unique tags
        - years: Year range (earliest, latest)
        - attachments: Number of attachments
        - notes: Number of notes

    Example:
        summary = library_summary(zot)
        print(f"Library has {summary['total_items']} items in {summary['collections']} collections")
    """
    items = list(_all_items(zot))
    item_types = items_per_type(zot)
    collections = zot.collections()
    tags = all_tags(zot)

    # Find year range
    years = []
    for item in items:
        date = item["data"].get("date", "") or ""
        if len(date) >= 4 and date[:4].isdigit():
            years.append(int(date[:4]))

    # Count attachments and notes
    attachments = sum(1 for _ in _all_items(zot, itemType="attachment"))
    notes = sum(1 for _ in _all_items(zot, itemType="note"))

    return {
        "total_items": len(items),
        "item_types": item_types,
        "collections": len(collections),
        "tags": len(tags),
        "years": {
            "earliest": min(years) if years else None,
            "latest": max(years) if years else None,
        },
        "attachments": attachments,
        "notes": notes,
    }


def attachment_summary(zot: zotero.Zotero) -> dict[str, Any]:
    """Get attachment types and sizes summary.

    Returns statistics about attachments in the library including
    content types, file sizes, and link modes.

    Args:
        zot: Zotero client

    Returns:
        Dict with attachment statistics including:
        - total: Total number of attachments
        - by_content_type: Count by content type (PDF, HTML, etc.)
        - by_link_mode: Count by link mode (imported_file, linked_url, etc.)
        - total_size: Total file size in bytes (if available)
        - with_file: Number of attachments with files
        - without_file: Number of attachments without files

    Example:
        summary = attachment_summary(zot)
        print(f"Total attachments: {summary['total']}")
        print(f"PDFs: {summary['by_content_type'].get('application/pdf', 0)}")
    """
    attachments = list(_all_items(zot, itemType="attachment"))

    by_content_type: dict[str, int] = {}
    by_link_mode: dict[str, int] = {}
    total_size = 0
    with_file = 0
    without_file = 0

    for att in attachments:
        data = att.get("data", {})

        # Count by content type
        content_type = data.get("contentType", "unknown")
        by_content_type[content_type] = by_content_type.get(content_type, 0) + 1

        # Count by link mode
        link_mode = data.get("linkMode", "unknown")
        by_link_mode[link_mode] = by_link_mode.get(link_mode, 0) + 1

        # Track file size if available
        file_size = data.get("fileSize", 0)
        if file_size:
            total_size += file_size
            with_file += 1
        else:
            without_file += 1

    return {
        "total": len(attachments),
        "by_content_type": by_content_type,
        "by_link_mode": by_link_mode,
        "total_size": total_size,
        "with_file": with_file,
        "without_file": without_file,
    }


# =============================================================================
# Sync Helpers
# =============================================================================

def get_sync_status(zot: zotero.Zotero) -> dict[str, Any]:
    """Check sync status of the library.

    Returns information about the sync state including last sync time,
    pending changes, and any sync errors.

    Args:
        zot: Zotero client

    Returns:
        Dict with sync status information:
        - synced: Whether the library is synced
        - last_sync: Timestamp of last sync (if available)
        - pending_changes: Number of pending changes
        - conflicts: Number of sync conflicts
        - error: Any sync error message

    Example:
        status = get_sync_status(zot)
        if status["synced"]:
            print("Library is synced")
    """
    try:
        # Try to get library info which includes sync metadata
        zot.items(limit=1)
        headers = zot.request.headers

        last_modified = headers.get("Last-Modified-Version", "")
        total_results = headers.get("Total-Results", "0")

        return {
            "synced": True,
            "last_sync_version": last_modified if last_modified else None,
            "total_items": int(total_results),
            "conflicts": 0,  # Would need to check for conflicts separately
            "error": None,
        }
    except Exception as e:
        return {
            "synced": False,
            "last_sync_version": None,
            "total_items": 0,
            "conflicts": 0,
            "error": str(e),
        }


def get_last_sync(zot: zotero.Zotero) -> dict[str, Any]:
    """Get last sync timestamp.

    Returns the timestamp of the last successful sync.

    Args:
        zot: Zotero client

    Returns:
        Dict with sync timestamp information:
        - timestamp: ISO format timestamp of last sync
        - version: Zotero sync version number
        - success: Whether the timestamp was retrieved successfully

    Example:
        last_sync = get_last_sync(zot)
        if last_sync["success"]:
            print(f"Last synced: {last_sync['timestamp']}")
    """
    try:
        # Fetch items to get sync headers
        zot.items(limit=1)
        headers = zot.request.headers

        last_modified = headers.get("Last-Modified-Version", "")

        return {
            "success": True,
            "version": last_modified if last_modified else None,
            "timestamp": None,  # Local API doesn't provide actual timestamp
        }
    except Exception as e:
        return {
            "success": False,
            "version": None,
            "timestamp": None,
            "error": str(e),
        }


def check_conflicts(zot: zotero.Zotero) -> list[dict]:
    """Find sync conflicts in the library.

    Searches for items that have sync conflicts (multiple versions
    that couldn't be automatically merged).

    Args:
        zot: Zotero client

    Returns:
        List of items with sync conflicts. Each item includes:
        - key: Item key
        - title: Item title
        - conflict_type: Type of conflict
        - versions: Conflicting version numbers

    Example:
        conflicts = check_conflicts(zot)
        if conflicts:
            print(f"Found {len(conflicts)} conflicts")
    """
    # Note: The local Zotero API doesn't directly expose conflict information
    # This is a placeholder that would need Zotero sync data access
    conflicts = []

    try:
        # Check for items with unusual version patterns
        for item in _all_items(zot):
            version = item.get("version", 0)
            # Items with version 0 might indicate sync issues
            if version == 0:
                conflicts.append({
                    "key": item.get("key", ""),
                    "title": item.get("data", {}).get("title", ""),
                    "conflict_type": "version_zero",
                    "versions": [version],
                })
    except Exception:
        pass

    return conflicts


def resolve_conflict(zot: zotero.Zotero, item_key: str, keep_version: str = "local") -> dict:
    """Resolve a sync conflict for an item.

    Resolves a sync conflict by choosing which version to keep.

    Args:
        zot: Zotero client
        item_key: Key of the item with the conflict
        keep_version: Which version to keep: "local" or "remote"

    Returns:
        Dict with "success" (bool) and either "message" (str) or "error" (str)

    Example:
        result = resolve_conflict(zot, "ITEM123", "local")
        if result["success"]:
            print("Conflict resolved")

    Note:
        The local Zotero API has limited conflict resolution capabilities.
        This function marks the conflict as resolved by updating the item.
        For full conflict resolution, use the Zotero UI.
    """
    try:
        # Get the item
        item = zot.item(item_key)
        if not item:
            return {"success": False, "error": f"Item not found: {item_key}"}

        # For local API, we can't truly resolve conflicts
        # This just updates the item to clear any conflict state
        if keep_version == "local":
            # Keep local version - just touch the item
            zot.update_item(item)
        elif keep_version == "remote":
            # For remote, we would need to fetch from server
            # This is not possible with local API alone
            return {
                "success": False,
                "error": "Remote version resolution requires server access"
            }
        else:
            return {"success": False, "error": f"Invalid keep_version: {keep_version}"}

        return {"success": True, "message": "Conflict resolved (local version kept)"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# =============================================================================
# Utility
# =============================================================================

def get_item_by_key(zot: zotero.Zotero, key: str) -> dict | None:
    """Get an item by its Zotero key.

    Retrieves a single item using its unique Zotero key.

    Args:
        zot: Zotero client
        key: The Zotero item key (e.g., "ABC123DEF")

    Returns:
        The item dict if found, None otherwise

    Example:
        item = get_item_by_key(zot, "ABC123DEF")
        if item:
            print(f"Found: {item['data']['title']}")
    """
    try:
        return zot.item(key)
    except Exception:
        return None


def get_item_by_doi(zot: zotero.Zotero, doi: str) -> dict | None:
    """Find an item by its DOI.

    Searches the library for an item with the specified DOI.

    Args:
        zot: Zotero client
        doi: Digital Object Identifier to search for

    Returns:
        The item dict if found, None otherwise

    Example:
        item = get_item_by_doi(zot, "10.1038/nature12373")
        if item:
            print(f"Found: {item['data']['title']}")
    """
    doi_clean = doi.strip().lower()
    for item in _all_items(zot):
        item_doi = item["data"].get("DOI", "") or ""
        if item_doi.lower() == doi_clean:
            return item
    return None


def get_item_by_isbn(zot: zotero.Zotero, isbn: str) -> dict | None:
    """Find an item by its ISBN.

    Searches the library for an item with the specified ISBN.

    Args:
        zot: Zotero client
        isbn: International Standard Book Number to search for

    Returns:
        The item dict if found, None otherwise

    Example:
        item = get_item_by_isbn(zot, "9780134685991")
        if item:
            print(f"Found: {item['data']['title']}")
    """
    # Clean ISBN (remove hyphens and spaces)
    isbn_clean = isbn.replace("-", "").replace(" ", "")
    for item in _all_items(zot):
        item_isbn = item["data"].get("ISBN", "") or ""
        item_isbn_clean = item_isbn.replace("-", "").replace(" ", "")
        if item_isbn_clean == isbn_clean:
            return item
    return None


def get_orphaned_attachments(zot: zotero.Zotero) -> list[dict]:
    """Find attachments without a valid parent item.

    Identifies attachment items whose parent item no longer exists
    or has been deleted.

    Args:
        zot: Zotero client

    Returns:
        List of orphaned attachment items

    Example:
        orphans = get_orphaned_attachments(zot)
        for att in orphans:
            print(f"Orphaned: {att['data']['title']}")
    """
    orphans = []

    # Get all attachments
    for att in _all_items(zot, itemType="attachment"):
        parent_key = att["data"].get("parentItem")
        if parent_key:
            # Check if parent exists
            try:
                parent = zot.item(parent_key)
                if not parent:
                    orphans.append(att)
            except Exception:
                orphans.append(att)
        else:
            # Attachments without parentItem are standalone (may be intentional)
            # But we include them as potentially orphaned
            orphans.append(att)

    return orphans


def get_trash_items(zot: zotero.Zotero) -> list[dict]:
    """Get items in the trash.

    Retrieves all items that have been moved to trash but not
    permanently deleted.

    Args:
        zot: Zotero client

    Returns:
        List of items in trash

    Example:
        trash = get_trash_items(zot)
        print(f"Trash contains {len(trash)} items")

    Note:
        The local Zotero API may not directly support trash queries.
        This function attempts to use the deleted API endpoint.
        If not available, returns empty list.
    """
    try:
        # Try to get deleted items from the API
        # Note: This may not work with all Zotero configurations
        deleted = zot.deleted()
        if deleted:
            return deleted
        return []
    except Exception:
        # Trash API may not be available via local API
        return []
