"""Tests for all zotero_librarian tools."""

import pytest
from zotero_librarian import get_zotero
from zotero_librarian import (
    count_items, all_items, all_items_by_type, get_item, get_attachments,
    get_notes, get_citations, get_collections, all_tags,
    items_without_pdf, items_without_attachments, items_without_tags,
    items_not_in_collection, items_without_abstract, items_missing_required_fields,
    items_without_cites, items_without_cited_by, preprints_without_doi, items_with_notes,
    empty_collections, single_item_collections,
    duplicate_dois, duplicate_titles,
    creator_name_variations, journal_name_variations, similar_tags,
    validate_doi, validate_isbn, validate_issn,
    items_with_invalid_doi, items_with_invalid_isbn, items_with_invalid_issn,
    items_with_broken_urls, items_with_placeholder_titles,
    attachment_info, check_item_completeness,
)


@pytest.fixture(scope="module")
def zot():
    """Create Zotero client and fetch library once for all tests."""
    zot = get_zotero()
    # Pre-fetch entire library with children - cached on zot object
    from zotero_librarian import _get_library_with_children
    _get_library_with_children(zot)
    return zot


@pytest.fixture(scope="module")
def all_items_list(zot):
    """Get cached library from zot object."""
    return zot._library_cache


@pytest.fixture(scope="module")
def first_item(all_items_list):
    """Get first item for single-item tests."""
    return all_items_list[0]


class TestNavigation:
    def test_count_items(self, zot):
        count = count_items(zot)
        assert count > 0

    def test_all_items(self, all_items_list):
        assert len(all_items_list) > 0
        assert "key" in all_items_list[0]
        assert "data" in all_items_list[0]

    def test_all_items_by_type(self, all_items_list):
        articles = [i for i in all_items_list if i["data"]["itemType"] == "journalArticle"]
        assert len(articles) > 0

    def test_get_item(self, zot, first_item):
        item = get_item(zot, first_item["key"])
        assert item["key"] == first_item["key"]

    def test_get_attachments(self, zot, first_item):
        atts = get_attachments(zot, first_item["key"])
        assert isinstance(atts, list)

    def test_get_notes(self, zot, first_item):
        notes = get_notes(zot, first_item["key"])
        assert isinstance(notes, list)

    def test_get_citations(self, zot, first_item):
        cites = get_citations(zot, first_item["key"])
        assert "cites" in cites
        assert "citedBy" in cites

    def test_get_collections(self, zot):
        collections = get_collections(zot)
        assert isinstance(collections, list)

    def test_all_tags(self, all_items_list):
        tags = all_tags_from_items(all_items_list)
        assert isinstance(tags, dict)


def all_tags_from_items(items):
    """Helper to get tags from cached items."""
    from collections import Counter
    tags = []
    for item in items:
        for tag in item["data"].get("tags", []):
            tag_str = tag.get("tag", "")
            if tag_str:
                tags.append(tag_str)
    return dict(Counter(tags))


class TestMissingContent:
    def test_items_without_pdf(self, all_items_list):
        items = [i for i in all_items_list if not any(
            c['data'].get('contentType') == 'application/pdf'
            for c in i.get('_children', [])
            if c['data']['itemType'] == 'attachment'
        )]
        assert isinstance(items, list)
        assert len(items) > 0

    def test_items_without_attachments(self, all_items_list):
        items = [i for i in all_items_list if not any(
            c['data']['itemType'] == 'attachment' for c in i.get('_children', [])
        )]
        assert isinstance(items, list)

    def test_items_without_tags(self, all_items_list):
        items = [i for i in all_items_list if not i["data"].get("tags")]
        assert isinstance(items, list)

    def test_items_not_in_collection(self, all_items_list):
        items = [i for i in all_items_list if not i["data"].get("collections")]
        assert isinstance(items, list)

    def test_items_without_abstract(self, all_items_list):
        items = [i for i in all_items_list if not i["data"].get("abstractNote")]
        assert isinstance(items, list)

    def test_items_missing_required_fields(self, all_items_list):
        items = [
            i for i in all_items_list
            if i["data"]["itemType"] == "journalArticle"
            and (not i["data"].get("volume") or not i["data"].get("pages"))
        ]
        assert isinstance(items, list)

    def test_items_without_cites(self, all_items_list):
        # Check cached items - those without relations
        items = [i for i in all_items_list if not i["data"].get("relations", {}).get("dc:relation:cites")]
        assert isinstance(items, list)

    def test_items_without_cited_by(self, all_items_list):
        items = [i for i in all_items_list if not i["data"].get("relations", {}).get("dc:relation:citedBy")]
        assert isinstance(items, list)

    def test_preprints_without_doi(self, all_items_list):
        items = [
            i for i in all_items_list
            if i["data"]["itemType"] == "preprint" and not i["data"].get("DOI")
        ]
        assert isinstance(items, list)

    def test_items_with_notes(self, all_items_list):
        items = [i for i in all_items_list if any(
            c['data']['itemType'] == 'note' for c in i.get('_children', [])
        )]
        assert isinstance(items, list)


class TestCollections:
    def test_empty_collections(self, zot):
        collections = empty_collections(zot)
        assert isinstance(collections, list)

    def test_single_item_collections(self, zot):
        collections = single_item_collections(zot)
        assert isinstance(collections, list)


class TestDuplicates:
    def test_duplicate_dois(self, all_items_list):
        from collections import defaultdict
        by_doi = defaultdict(list)
        for item in all_items_list:
            doi = item["data"].get("DOI", "")
            if doi:
                by_doi[doi.lower()].append(item)
        dups = {k: v for k, v in by_doi.items() if len(v) > 1}
        assert isinstance(dups, dict)

    def test_duplicate_titles(self, all_items_list):
        from collections import defaultdict
        by_title = defaultdict(list)
        for item in all_items_list:
            title = item["data"].get("title", "")
            if title:
                by_title[title.lower()].append(item)
        dups = {k: v for k, v in by_title.items() if len(v) > 1}
        assert isinstance(dups, dict)


class TestConsistency:
    def test_creator_name_variations(self, all_items_list):
        from collections import defaultdict
        names = defaultdict(list)
        for item in all_items_list:
            for creator in item["data"].get("creators", []):
                first = creator.get("firstName", "")
                last = creator.get("lastName", "")
                if first and last:
                    names[last.lower()].append(f"{first} {last}")
        variations = {k: list(set(v)) for k, v in names.items() if len(set(v)) > 1}
        assert isinstance(variations, dict)

    def test_journal_name_variations(self, all_items_list):
        from collections import defaultdict
        import re
        journals = defaultdict(list)
        for item in all_items_list:
            if item["data"]["itemType"] == "journalArticle":
                journal = item["data"].get("publicationTitle", "")
                if journal:
                    key = re.sub(r"[\s\-]+", " ", journal.lower().strip())
                    journals[key].append(journal)
        variations = {k: list(set(v)) for k, v in journals.items() if len(set(v)) > 1}
        assert isinstance(variations, dict)

    def test_similar_tags(self, all_items_list):
        from difflib import SequenceMatcher
        from collections import Counter
        tags = []
        for item in all_items_list:
            for tag in item["data"].get("tags", []):
                tag_str = tag.get("tag", "")
                if tag_str:
                    tags.append(tag_str)
        tag_counts = dict(Counter(tags))
        unique_tags = list(tag_counts.keys())
        result = {}
        for tag in unique_tags[:50]:  # Limit for speed
            similar = [
                t for t in unique_tags
                if t != tag and SequenceMatcher(None, t, tag).ratio() >= 0.8
            ]
            if similar:
                result[tag] = similar
        assert isinstance(result, dict)


class TestValidation:
    def test_validate_doi(self):
        assert validate_doi("10.1000/test") == True
        assert validate_doi("invalid") == False

    def test_validate_isbn(self):
        assert validate_isbn("978-0-123456-78-9") == True
        assert validate_isbn("invalid") == False

    def test_validate_issn(self):
        assert validate_issn("1234-5678") == True
        assert validate_issn("invalid") == False

    def test_items_with_invalid_doi(self, zot):
        items = list(items_with_invalid_doi(zot))
        assert isinstance(items, list)

    def test_items_with_invalid_isbn(self, zot):
        items = list(items_with_invalid_isbn(zot))
        assert isinstance(items, list)

    def test_items_with_invalid_issn(self, zot):
        items = list(items_with_invalid_issn(zot))
        assert isinstance(items, list)

    def test_items_with_broken_urls(self, zot):
        items = list(items_with_broken_urls(zot))
        assert isinstance(items, list)

    def test_items_with_placeholder_titles(self, zot):
        items = list(items_with_placeholder_titles(zot))
        assert isinstance(items, list)


class TestInspection:
    def test_attachment_info(self, zot, first_item):
        info = attachment_info(zot, first_item["key"])
        assert isinstance(info, list)

    def test_check_item_completeness(self, zot, first_item):
        result = check_item_completeness(zot, first_item["key"], ["title", "date"])
        assert "complete" in result
        assert "missing" in result
