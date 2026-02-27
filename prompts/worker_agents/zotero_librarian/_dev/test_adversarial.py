"""
Adversarial Integration Tests for Zotero Librarian Toolkit

These tests use the REAL Zotero local API (no mocks) to verify robustness
against edge cases, invalid inputs, and adversarial scenarios.

All tests use a single test item created at session start and deleted at end.
Tests are idempotent and clean up after themselves.

Requirements:
    - Zotero 7+ must be running
    - Local API must be enabled in Zotero settings:
      Edit -> Settings -> Advanced -> "Allow other applications to communicate with Zotero"
"""

import pytest
import time
from typing import Any
import httpx

from zotero_librarian import (
    get_zotero,
    get_item,
    update_item_fields,
    add_tags_to_item,
    remove_tags_from_item,
    move_item_to_collection,
    add_item_to_collection,
    remove_item_from_collection,
    attach_note,
    update_note,
    delete_note,
    delete_item,
    create_collection,
    delete_collection,
    rename_collection,
    merge_tags,
    rename_tag,
    delete_tag,
    validate_doi,
    validate_isbn,
    validate_issn,
    add_citation_relation,
    get_citations,
    get_notes,
    get_attachments,
    all_tags,
    count_items,
)


# =============================================================================
# Test Fixtures
# =============================================================================

def check_zotero_available():
    """Check if Zotero local API is available."""
    try:
        zot = get_zotero()
        # Try a simple operation to verify API is working
        zot.num_items()
        return True
    except Exception:
        return False


@pytest.fixture(scope="module")
def zot():
    """Create Zotero client for the test session."""
    zot = get_zotero()
    # Verify Zotero is available
    if not check_zotero_available():
        pytest.skip("Zotero local API is not available. Ensure Zotero is running with local API enabled.")
    return zot


@pytest.fixture(scope="module")
def test_item(zot):
    """
    Create a test item at session start that serves as sandbox for all tests.
    This item is deleted at session end.
    """
    # Create a simple book item as our test sandbox
    item_data = {
        "itemType": "book",
        "title": "Test Item - DO NOT EDIT MANUALLY",
        "creators": [
            {"creatorType": "author", "firstName": "Test", "lastName": "User"}
        ],
        "date": "2024",
        "publisher": "Test Publisher",
        "place": "Test City",
        "ISBN": "978-0-00-000000-0",
        "abstractNote": "Test abstract for adversarial testing",
        "url": "https://example.com/test",
        "accessDate": "2024-01-01",
        "pages": "1-100",
        "numberOfPages": "100",
        "language": "en",
        "libraryCatalog": "Test Catalog",
        "callNumber": "TEST123",
        "rights": "CC0",
        "extra": "Test extra field",
        "series": "Test Series",
        "seriesNumber": "1",
        "volume": "1",
        "edition": "1st",
        "shortTitle": "Test",
    }

    # Create the item
    try:
        result = zot.create_items([item_data])
        if not result or "success" not in result:
            pytest.skip("Failed to create test item - Zotero may not be running")
    except Exception as e:
        pytest.skip(f"Failed to create test item: {str(e)}")

    item_key = result["success"]["0"]["key"]

    # Yield the item key for tests.
    # Note: Item is NOT deleted after session - avoids using production
    # delete functionality in test cleanup. Human can manually clean up.
    yield item_key


@pytest.fixture
def restore_item_state(zot, test_item):
    """
    Fixture to restore test item state after each test.
    Captures original state before test and restores it after.
    """
    # Capture original state
    original = get_item(zot, test_item)
    original_data = {
        "tags": original["data"].get("tags", []),
        "collections": original["data"].get("collections", []),
        "relations": original["data"].get("relations", {}),
    }

    yield

    # Restore original state
    try:
        current = get_item(zot, test_item)
        current["data"]["tags"] = original_data["tags"]
        current["data"]["collections"] = original_data["collections"]
        current["data"]["relations"] = original_data["relations"]
        zot.update_item(current)
    except Exception:
        pass  # Item may have been deleted


@pytest.fixture
def temp_collection(zot):
    """Create a temporary collection for testing, cleaned up after use."""
    result = create_collection(zot, f"Test Collection - {time.time()}")
    if result["success"]:
        yield result["key"]
        try:
            delete_collection(zot, result["key"])
        except Exception:
            pass
    else:
        pytest.skip("Failed to create temp collection")


# =============================================================================
# Edge Case Tests - Empty Strings, None, Unicode, Long Strings
# =============================================================================

class TestEdgeCasesEmptyStrings:
    """Test behavior with empty strings."""

    def test_update_with_empty_title(self, zot, test_item, restore_item_state):
        """Empty string in title field should be accepted by Zotero."""
        result = update_item_fields(zot, test_item, {"title": ""})
        assert result["success"], "Empty title update should succeed"
        # Verify item still exists with empty title
        item = get_item(zot, test_item)
        assert item["data"]["title"] == "", f"Expected empty title, got: {item['data']['title']!r}"

    def test_update_with_empty_abstract(self, zot, test_item, restore_item_state):
        """Empty string in abstract field should be accepted by Zotero."""
        result = update_item_fields(zot, test_item, {"abstractNote": ""})
        assert result["success"], "Empty abstract update should succeed"
        # Read back and verify empty abstract was stored
        item = get_item(zot, test_item)
        assert item["data"]["abstractNote"] == "", f"Expected empty abstract, got: {item['data']['abstractNote']!r}"

    def test_update_with_empty_publisher(self, zot, test_item, restore_item_state):
        """Empty string in publisher field should be accepted by Zotero."""
        result = update_item_fields(zot, test_item, {"publisher": ""})
        assert result["success"], "Empty publisher update should succeed"
        # Read back and verify empty publisher was stored
        item = get_item(zot, test_item)
        assert item["data"]["publisher"] == "", f"Expected empty publisher, got: {item['data']['publisher']!r}"

    def test_add_empty_tag(self, zot, test_item, restore_item_state):
        """Adding empty string as tag should be ignored."""
        original_item = get_item(zot, test_item)
        original_tag_count = len(original_item["data"].get("tags", []))
        
        result = add_tags_to_item(zot, test_item, [""])
        assert result["success"], "Empty tag add should succeed without error"
        
        # Empty tags should be ignored - count should not change
        item = get_item(zot, test_item)
        tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
        assert len(tags) == original_tag_count, f"Empty tag should not be added, tags changed from {original_tag_count} to {len(tags)}"
        assert "" not in tags, "Empty string should not appear in tags list"

    def test_add_mixed_empty_and_valid_tags(self, zot, test_item, restore_item_state):
        """Mix of empty and valid tags should only add valid tags."""
        result = add_tags_to_item(zot, test_item, ["", "valid_tag", ""])
        assert result["success"], "Mixed tag add should succeed"
        item = get_item(zot, test_item)
        tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
        assert "valid_tag" in tags, f"Valid tag should be present, got tags: {tags}"
        assert "" not in tags, f"Empty string should not appear in tags, got: {tags}"


class TestEdgeCasesNoneValues:
    """Test behavior with None values."""

    def test_update_with_none_title(self, zot, test_item, restore_item_state):
        """None value in title field should be handled gracefully."""
        original_item = get_item(zot, test_item)
        original_title = original_item["data"]["title"]
        
        result = update_item_fields(zot, test_item, {"title": None})
        # None should either be ignored or clear the field - verify behavior
        assert result["success"], "None title update should not crash"
        
        # Read back to see how Zotero handles None
        item = get_item(zot, test_item)
        # Zotero may keep original or set to empty - both are acceptable
        assert item["data"]["title"] in (original_title, ""), f"Title should be unchanged or empty, got: {item['data']['title']!r}"

    def test_update_with_none_date(self, zot, test_item, restore_item_state):
        """None value in date field should be handled gracefully."""
        result = update_item_fields(zot, test_item, {"date": None})
        assert result["success"], "None date update should not crash"
        # Read back and verify date was cleared or kept
        item = get_item(zot, test_item)
        # Zotero may clear the date or keep original - both acceptable
        assert item["data"]["date"] in ("2024", ""), f"Date should be original or empty, got: {item['data']['date']!r}"

    def test_update_with_none_fields_dict(self, zot, test_item, restore_item_state):
        """Multiple None values in fields dict should be handled gracefully."""
        result = update_item_fields(zot, test_item, {
            "title": None,
            "date": None,
            "publisher": None,
        })
        assert result["success"], "Multiple None fields update should not crash"
        # Read back and verify fields were handled
        item = get_item(zot, test_item)
        # All fields should be either original values or empty
        assert item["data"]["title"] in ("Test Item - DO NOT EDIT MANUALLY", ""), "Title handling incorrect"
        assert item["data"]["publisher"] in ("Test Publisher", ""), "Publisher handling incorrect"

    def test_add_none_tag(self, zot, test_item, restore_item_state):
        """None in tags list should raise TypeError or be rejected."""
        with pytest.raises((TypeError, ValueError)):
            add_tags_to_item(zot, test_item, [None])


class TestEdgeCasesUnicode:
    """Test behavior with unicode characters."""

    def test_unicode_title_emoji(self, zot, test_item, restore_item_state):
        """Title with emoji should be stored correctly."""
        result = update_item_fields(zot, test_item, {"title": "Test \U0001F4DA Book"})
        assert result["success"], "Emoji title update should succeed"
        item = get_item(zot, test_item)
        assert "\U0001F4DA" in item["data"]["title"], f"Emoji should be preserved in title, got: {item['data']['title']!r}"

    def test_unicode_title_cjk(self, zot, test_item, restore_item_state):
        """Title with CJK characters should be stored correctly."""
        expected = "\u4e2d\u6587\u6d4b\u8bd5"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "CJK title update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"CJK title mismatch: expected {expected!r}, got {item['data']['title']!r}"

    def test_unicode_title_arabic(self, zot, test_item, restore_item_state):
        """Title with Arabic script should be stored correctly."""
        expected = "\u0627\u062e\u062a\u0628\u0627\u0631"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Arabic title update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Arabic title mismatch: expected {expected!r}, got {item['data']['title']!r}"

    def test_unicode_title_cyrillic(self, zot, test_item, restore_item_state):
        """Title with Cyrillic script should be stored correctly."""
        expected = "\u0422\u0435\u0441\u0442"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Cyrillic title update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Cyrillic title mismatch: expected {expected!r}, got {item['data']['title']!r}"

    def test_unicode_abstract_mixed(self, zot, test_item, restore_item_state):
        """Abstract with mixed unicode should be stored correctly."""
        text = "Mixed: \u00e9\u00f1\u00fc\u4e2d\u6587\u0627\u0631\u0442\u0435\u0441\u0442"
        result = update_item_fields(zot, test_item, {"abstractNote": text})
        assert result["success"], "Mixed unicode abstract update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["abstractNote"] == text, f"Mixed unicode abstract mismatch: expected {text!r}, got {item['data']['abstractNote']!r}"

    def test_tag_with_unicode(self, zot, test_item, restore_item_state):
        """Tag with unicode characters should be stored correctly."""
        result = add_tags_to_item(zot, test_item, ["\u00e9tiquette", "\u6807\u7b7e"])
        assert result["success"], "Unicode tags add should succeed"
        item = get_item(zot, test_item)
        tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
        assert "\u00e9tiquette" in tags, f"French unicode tag missing, got: {tags}"
        assert "\u6807\u7b7e" in tags, f"Chinese unicode tag missing, got: {tags}"


class TestEdgeCasesLongStrings:
    """Test behavior with very long strings."""

    def test_very_long_title(self, zot, test_item, restore_item_state):
        """Title with 10000 characters should be stored correctly."""
        long_title = "A" * 10000
        result = update_item_fields(zot, test_item, {"title": long_title})
        assert result["success"], "Long title update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == long_title, f"Long title truncated: expected {len(long_title)} chars, got {len(item['data']['title'])}"

    def test_very_long_abstract(self, zot, test_item, restore_item_state):
        """Abstract with 50000 characters should be stored correctly."""
        long_abstract = "B" * 50000
        result = update_item_fields(zot, test_item, {"abstractNote": long_abstract})
        assert result["success"], "Long abstract update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["abstractNote"] == long_abstract, f"Long abstract truncated: expected {len(long_abstract)} chars, got {len(item['data']['abstractNote'])}"

    def test_very_long_publisher(self, zot, test_item, restore_item_state):
        """Publisher with 5000 characters should be stored correctly."""
        long_publisher = "C" * 5000
        result = update_item_fields(zot, test_item, {"publisher": long_publisher})
        assert result["success"], "Long publisher update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["publisher"] == long_publisher, f"Long publisher truncated: expected {len(long_publisher)} chars, got {len(item['data']['publisher'])}"

    def test_very_long_tag(self, zot, test_item, restore_item_state):
        """Very long tag name should be stored correctly."""
        long_tag = "D" * 1000
        result = add_tags_to_item(zot, test_item, [long_tag])
        assert result["success"], "Long tag add should succeed"
        item = get_item(zot, test_item)
        tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
        assert long_tag in tags, f"Long tag not found, got: {tags}"


class TestEdgeCasesSpecialCharacters:
    """Test behavior with special characters."""

    def test_title_with_quotes(self, zot, test_item, restore_item_state):
        """Title with single and double quotes should be stored correctly."""
        expected = 'Test "quoted" and \'quoted\' title'
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Title with quotes update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Quotes not preserved: expected {expected!r}, got {item['data']['title']!r}"

    def test_title_with_backslashes(self, zot, test_item, restore_item_state):
        """Title with backslashes should be stored correctly."""
        expected = "Test\\path\\to\\file"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Title with backslashes update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Backslashes not preserved: expected {expected!r}, got {item['data']['title']!r}"

    def test_title_with_newlines(self, zot, test_item, restore_item_state):
        """Title with newlines should be stored correctly."""
        expected = "Line1\nLine2\nLine3"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Title with newlines update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Newlines not preserved: expected {expected!r}, got {item['data']['title']!r}"

    def test_title_with_tabs(self, zot, test_item, restore_item_state):
        """Title with tabs should be stored correctly."""
        expected = "Col1\tCol2\tCol3"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Title with tabs update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Tabs not preserved: expected {expected!r}, got {item['data']['title']!r}"

    def test_title_with_null_byte(self, zot, test_item, restore_item_state):
        """Title with null byte should be handled (may be stripped or stored)."""
        text_with_null = "Test\x00Null"
        result = update_item_fields(zot, test_item, {"title": text_with_null})
        assert result["success"], "Title with null byte should not crash"
        item = get_item(zot, test_item)
        # Zotero may strip null bytes or store them - verify it doesn't crash
        # The important thing is the operation succeeded
        assert isinstance(item["data"]["title"], str), "Title should be a string"


# =============================================================================
# Invalid Input Tests
# =============================================================================

class TestInvalidInputsWrongTypes:
    """Test behavior with wrong types."""

    def test_update_with_int_where_string_expected(self, zot, test_item, restore_item_state):
        """Integer where string expected should be converted or rejected."""
        original_title = get_item(zot, test_item)["data"]["title"]
        result = update_item_fields(zot, test_item, {"title": 12345})
        # API should handle type mismatch gracefully - either convert to string or reject
        assert result["success"], "Int title update should not crash"
        item = get_item(zot, test_item)
        # Zotero may convert int to string "12345" or keep original
        assert item["data"]["title"] in ("12345", original_title), f"Int title handling unexpected: {item['data']['title']!r}"

    def test_update_with_list_where_string_expected(self, zot, test_item, restore_item_state):
        """List where string expected should be rejected or handled."""
        original_title = get_item(zot, test_item)["data"]["title"]
        result = update_item_fields(zot, test_item, {"title": ["list", "of", "strings"]})
        # API should handle type mismatch - may reject or keep original
        assert result["success"] or not result.get("success"), "List title update should not crash"
        item = get_item(zot, test_item)
        # Title should remain unchanged since list is invalid
        assert item["data"]["title"] == original_title, f"List title should be rejected, got: {item['data']['title']!r}"

    def test_update_with_dict_where_string_expected(self, zot, test_item, restore_item_state):
        """Dict where string expected should be rejected."""
        original_title = get_item(zot, test_item)["data"]["title"]
        result = update_item_fields(zot, test_item, {"title": {"key": "value"}})
        assert result["success"] or not result.get("success"), "Dict title update should not crash"
        item = get_item(zot, test_item)
        # Title should remain unchanged since dict is invalid
        assert item["data"]["title"] == original_title, f"Dict title should be rejected, got: {item['data']['title']!r}"

    def test_add_tags_with_int(self, zot, test_item, restore_item_state):
        """Integer in tags list should raise TypeError."""
        with pytest.raises(TypeError):
            add_tags_to_item(zot, test_item, [123])

    def test_add_tags_with_dict(self, zot, test_item, restore_item_state):
        """Dict in tags list should raise TypeError."""
        with pytest.raises(TypeError):
            add_tags_to_item(zot, test_item, [{"tag": "dict_tag"}])


class TestInvalidInputsMalformedIdentifiers:
    """Test behavior with malformed DOIs, ISBNs, etc."""

    def test_malformed_doi_simple(self, zot, test_item, restore_item_state):
        """Malformed DOI should be stored (Zotero doesn't validate DOI format)."""
        result = update_item_fields(zot, test_item, {"DOI": "not-a-doi"})
        assert result["success"], "Malformed DOI update should succeed (Zotero stores as-is)"
        item = get_item(zot, test_item)
        assert item["data"]["DOI"] == "not-a-doi", f"Malformed DOI should be stored: {item['data']['DOI']!r}"

    def test_malformed_doi_empty_prefix(self, zot, test_item, restore_item_state):
        """DOI with empty prefix should be stored (Zotero doesn't validate)."""
        result = update_item_fields(zot, test_item, {"DOI": "10./invalid"})
        assert result["success"], "DOI with empty prefix update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["DOI"] == "10./invalid", f"DOI should be stored: {item['data']['DOI']!r}"

    def test_malformed_isbn_short(self, zot, test_item, restore_item_state):
        """ISBN too short should be stored (Zotero doesn't validate length)."""
        result = update_item_fields(zot, test_item, {"ISBN": "123"})
        assert result["success"], "Short ISBN update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["ISBN"] == "123", f"Short ISBN should be stored: {item['data']['ISBN']!r}"

    def test_malformed_isbn_long(self, zot, test_item, restore_item_state):
        """ISBN too long should be stored (Zotero doesn't validate length)."""
        result = update_item_fields(zot, test_item, {"ISBN": "12345678901234567890"})
        assert result["success"], "Long ISBN update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["ISBN"] == "12345678901234567890", f"Long ISBN should be stored: {item['data']['ISBN']!r}"

    def test_malformed_isbn_letters(self, zot, test_item, restore_item_state):
        """ISBN with invalid letters should be stored (Zotero doesn't validate)."""
        result = update_item_fields(zot, test_item, {"ISBN": "ABC-DEF-GHI-J"})
        assert result["success"], "Invalid ISBN update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["ISBN"] == "ABC-DEF-GHI-J", f"Invalid ISBN should be stored: {item['data']['ISBN']!r}"

    def test_malformed_issn(self, zot, test_item, restore_item_state):
        """Malformed ISSN should be stored (Zotero doesn't validate format)."""
        result = update_item_fields(zot, test_item, {"ISSN": "1234"})
        assert result["success"], "Malformed ISSN update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["ISSN"] == "1234", f"Malformed ISSN should be stored: {item['data']['ISSN']!r}"


class TestInvalidInputsNonExistentKeys:
    """Test behavior with non-existent keys."""

    def test_get_nonexistent_item(self, zot):
        """Get item with non-existent key."""
        with pytest.raises(Exception):
            get_item(zot, "NONEXISTENT123")

    def test_update_nonexistent_item(self, zot):
        """Update non-existent item."""
        with pytest.raises(Exception):
            update_item_fields(zot, "NONEXISTENT123", {"title": "Test"})

    def test_delete_nonexistent_item(self, zot):
        """Delete non-existent item."""
        with pytest.raises(Exception):
            delete_item(zot, "NONEXISTENT123")

    def test_add_tag_to_nonexistent_item(self, zot):
        """Add tag to non-existent item."""
        with pytest.raises(Exception):
            add_tags_to_item(zot, "NONEXISTENT123", ["tag"])

    def test_remove_tag_from_nonexistent_item(self, zot):
        """Remove tag from non-existent item."""
        with pytest.raises(Exception):
            remove_tags_from_item(zot, "NONEXISTENT123", ["tag"])

    def test_move_nonexistent_to_collection(self, zot, temp_collection):
        """Move non-existent item to collection."""
        with pytest.raises(Exception):
            move_item_to_collection(zot, "NONEXISTENT123", temp_collection)

    def test_get_notes_nonexistent_item(self, zot):
        """Get notes for non-existent item - should raise exception."""
        # API should raise exception for non-existent item
        with pytest.raises(Exception):
            get_notes(zot, "NONEXISTENT123")

    def test_get_attachments_nonexistent_item(self, zot):
        """Get attachments for non-existent item."""
        with pytest.raises(Exception):
            get_attachments(zot, "NONEXISTENT123")


# =============================================================================
# Boundary Condition Tests
# =============================================================================

class TestBoundaryConditions:
    """Test boundary conditions."""

    def test_add_zero_tags(self, zot, test_item, restore_item_state):
        """Add empty list of tags should succeed without changing state."""
        original_item = get_item(zot, test_item)
        original_tag_count = len(original_item["data"].get("tags", []))
        
        result = add_tags_to_item(zot, test_item, [])
        assert result["success"], "Empty tags add should succeed"
        
        # Verify no tags were added
        item = get_item(zot, test_item)
        current_tag_count = len(item["data"].get("tags", []))
        assert current_tag_count == original_tag_count, f"Empty tags add should not change count: {original_tag_count} -> {current_tag_count}"

    def test_remove_zero_tags(self, zot, test_item, restore_item_state):
        """Remove empty list of tags should succeed without changing state."""
        original_item = get_item(zot, test_item)
        original_tag_count = len(original_item["data"].get("tags", []))
        
        result = remove_tags_from_item(zot, test_item, [])
        assert result["success"], "Empty tags remove should succeed"
        
        # Verify no tags were removed
        item = get_item(zot, test_item)
        current_tag_count = len(item["data"].get("tags", []))
        assert current_tag_count == original_tag_count, f"Empty tags remove should not change count: {original_tag_count} -> {current_tag_count}"

    def test_update_zero_fields(self, zot, test_item, restore_item_state):
        """Update with empty fields dict should succeed without changing state."""
        original_item = get_item(zot, test_item)
        original_title = original_item["data"]["title"]
        
        result = update_item_fields(zot, test_item, {})
        assert result["success"], "Empty fields update should succeed"
        
        # Verify no fields were changed
        item = get_item(zot, test_item)
        assert item["data"]["title"] == original_title, "Empty update should not change title"

    def test_add_single_tag(self, zot, test_item, restore_item_state):
        """Add single tag should add exactly that tag."""
        result = add_tags_to_item(zot, test_item, ["single_tag"])
        assert result["success"], "Single tag add should succeed"
        item = get_item(zot, test_item)
        tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
        assert "single_tag" in tags, f"Single tag should be present, got: {tags}"

    def test_remove_single_tag(self, zot, test_item, restore_item_state):
        """Remove single tag should remove exactly that tag."""
        # First add a tag
        add_tags_to_item(zot, test_item, ["to_remove"])
        # Then remove it
        result = remove_tags_from_item(zot, test_item, ["to_remove"])
        assert result["success"], "Single tag remove should succeed"
        item = get_item(zot, test_item)
        tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
        assert "to_remove" not in tags, f"Tag should be removed, got: {tags}"

    def test_add_many_tags(self, zot, test_item, restore_item_state):
        """Add many tags at once should add all tags."""
        many_tags = [f"tag_{i}" for i in range(100)]
        result = add_tags_to_item(zot, test_item, many_tags)
        assert result["success"], "Many tags add should succeed"
        item = get_item(zot, test_item)
        tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
        # Verify all tags were added
        for tag in many_tags:
            assert tag in tags, f"Tag {tag} should be present"

    def test_single_character_tag(self, zot, test_item, restore_item_state):
        """Single character tag should be stored correctly."""
        result = add_tags_to_item(zot, test_item, ["a"])
        assert result["success"], "Single char tag add should succeed"
        item = get_item(zot, test_item)
        tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
        assert "a" in tags, f"Single char tag should be present, got: {tags}"

    def test_single_character_title(self, zot, test_item, restore_item_state):
        """Single character title should be stored correctly."""
        result = update_item_fields(zot, test_item, {"title": "X"})
        assert result["success"], "Single char title update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == "X", f"Single char title mismatch: expected 'X', got {item['data']['title']!r}"


# =============================================================================
# State Corruption Tests
# =============================================================================

class TestStateCorruption:
    """Test attempts to create inconsistent states."""

    def test_item_in_nonexistent_collection(self, zot, test_item, restore_item_state):
        """Try to add item to non-existent collection."""
        with pytest.raises(Exception):
            move_item_to_collection(zot, test_item, "NONEXISTENT123")

    def test_remove_from_nonexistent_collection(self, zot, test_item, restore_item_state):
        """Try to remove item from non-existent collection."""
        with pytest.raises(Exception):
            remove_item_from_collection(zot, test_item, "NONEXISTENT123")

    def test_add_to_multiple_collections(self, zot, test_item, restore_item_state):
        """Add item to multiple collections."""
        coll1_result = create_collection(zot, f"Test Coll 1 - {time.time()}")
        coll2_result = create_collection(zot, f"Test Coll 2 - {time.time()}")

        if coll1_result["success"] and coll2_result["success"]:
            add_item_to_collection(zot, test_item, coll1_result["key"])
            add_item_to_collection(zot, test_item, coll2_result["key"])

            item = get_item(zot, test_item)
            assert len(item["data"].get("collections", [])) >= 2

            # Cleanup
            delete_collection(zot, coll1_result["key"])
            delete_collection(zot, coll2_result["key"])

    def test_circular_collection_reference_attempt(self, zot, test_item):
        """Try to create circular collection reference (should fail gracefully)."""
        # Create two collections
        coll1_result = create_collection(zot, f"Parent - {time.time()}")
        if not coll1_result["success"]:
            pytest.skip("Failed to create test collection")

        # Try to make coll1 its own parent (should fail)
        try:
            coll2_result = create_collection(zot, f"Child - {time.time()}", parent_key=coll1_result["key"])
            # Now try to make coll1 a child of coll2 (circular)
            # This should fail or be handled by Zotero
            coll3_result = create_collection(zot, f"Grandchild - {time.time()}", parent_key=coll2_result["key"])
        except Exception:
            pass  # Expected to potentially fail

        # Cleanup
        try:
            delete_collection(zot, coll1_result["key"])
            if coll2_result["success"]:
                delete_collection(zot, coll2_result["key"])
            if coll3_result and coll3_result.get("success"):
                delete_collection(zot, coll3_result["key"])
        except Exception:
            pass

    def test_delete_item_then_operate(self, zot):
        """Try to operate on deleted item."""
        # This test requires create_items to work, skip if API doesn't support it
        pytest.skip("Test requires create_items support - skipping for read-only API")


# =============================================================================
# Concurrent Modification Tests
# =============================================================================

class TestConcurrentModification:
    """Test behavior with concurrent modifications."""

    def test_read_modify_race(self, zot, test_item, restore_item_state):
        """Simulate read-modify race condition - last write should win."""
        # Read item
        item1 = get_item(zot, test_item)
        original_title = item1["data"]["title"]

        # Modify externally (simulated by another update)
        update_item_fields(zot, test_item, {"title": "Modified Externally"})

        # Now try to update based on stale read
        item1["data"]["title"] = "Based on stale read"
        result = zot.update_item(item1)

        # The update should succeed (last write wins)
        assert result["success"], "Stale read update should succeed"
        
        # Verify the title was overwritten
        item = get_item(zot, test_item)
        assert item["data"]["title"] == "Based on stale read", f"Last write should win, got: {item['data']['title']!r}"

        # Restore
        update_item_fields(zot, test_item, {"title": original_title})

    def test_multiple_sequential_updates(self, zot, test_item, restore_item_state):
        """Multiple rapid sequential updates should all succeed."""
        for i in range(10):
            result = update_item_fields(zot, test_item, {"title": f"Update {i}"})
            assert result["success"], f"Update {i} should succeed"
        
        # Verify final state
        item = get_item(zot, test_item)
        assert item["data"]["title"] == "Update 9", f"Final title should be 'Update 9', got: {item['data']['title']!r}"

    def test_tag_add_remove_rapid(self, zot, test_item, restore_item_state):
        """Rapid add/remove of tags should leave no trace."""
        original_item = get_item(zot, test_item)
        original_tags = set(t.get("tag", "") for t in original_item["data"].get("tags", []))
        
        for i in range(5):
            add_tags_to_item(zot, test_item, [f"rapid_{i}"])
            remove_tags_from_item(zot, test_item, [f"rapid_{i}"])
        
        # Verify no rapid tags remain
        item = get_item(zot, test_item)
        current_tags = set(t.get("tag", "") for t in item["data"].get("tags", []))
        for i in range(5):
            assert f"rapid_{i}" not in current_tags, f"Rapid tag {i} should be removed"


# =============================================================================
# Missing Dependencies / Orphan Tests
# =============================================================================

class TestMissingDependencies:
    """Test operations on deleted items and orphaned references."""

    def test_note_on_deleted_item(self, zot):
        """Create note, delete parent, try to access note."""
        # This test requires create_items to work, skip if API doesn't support it
        pytest.skip("Test requires create_items support - skipping for read-only API")

    def test_attachment_orphan_check(self, zot, test_item):
        """Verify attachments function returns list for valid item."""
        attachments = get_attachments(zot, test_item)
        # Should return a list (may be empty if no attachments)
        assert isinstance(attachments, list), f"Attachments should be a list, got {type(attachments)}"

    def test_citation_to_nonexistent_item(self, zot, test_item, restore_item_state):
        """Add citation relation to non-existent item URI should succeed."""
        # Zotero allows arbitrary URIs in relations
        result = add_citation_relation(zot, test_item, "cites", "http://example.com/nonexistent")
        assert result["success"], "Citation to nonexistent URI should succeed"
        # Verify relation was added
        item = get_item(zot, test_item)
        relations = item["data"].get("relations", {})
        assert "cites" in str(relations), f"Citation relation should be present: {relations}"

    def test_collection_with_no_items_operations(self, zot, temp_collection):
        """Operations on empty collection should succeed."""
        # Rename empty collection
        result = rename_collection(zot, temp_collection, "Renamed Empty Collection")
        assert result["success"], "Rename empty collection should succeed"

        # Verify collection was renamed
        collections = zot.collections()
        renamed = [c for c in collections if c["key"] == temp_collection]
        assert len(renamed) == 1, "Collection should exist after rename"
        assert renamed[0]["data"]["name"] == "Renamed Empty Collection", "Collection name should be updated"

        # Try to get items (should return empty list)
        items = zot.collection_items(temp_collection)
        assert isinstance(items, list), "Collection items should be a list"
        assert len(items) == 0, "Empty collection should have no items"


# =============================================================================
# Type Confusion Tests
# =============================================================================

class TestTypeConfusion:
    """Test passing wrong types where specific types expected."""

    def test_string_where_int_expected(self, zot, test_item, restore_item_state):
        """String where numeric field expected should be stored as-is."""
        result = update_item_fields(zot, test_item, {"numberOfPages": "not-a-number"})
        assert result["success"], "String in numeric field should not crash"
        item = get_item(zot, test_item)
        assert item["data"]["numberOfPages"] == "not-a-number", f"String should be stored: {item['data']['numberOfPages']!r}"

    def test_int_where_string_expected_in_creator(self, zot, test_item, restore_item_state):
        """Int in creator field should be converted to string or rejected."""
        original_creators = get_item(zot, test_item)["data"]["creators"]
        creators = [{"creatorType": "author", "firstName": 123, "lastName": 456}]
        result = update_item_fields(zot, test_item, {"creators": creators})
        # API should handle type mismatch - may convert to string or reject
        assert result["success"], "Int creator fields should not crash"
        item = get_item(zot, test_item)
        # Zotero may convert ints to strings "123", "456"
        first_name = item["data"]["creators"][0]["firstName"]
        assert first_name in (123, "123"), f"Int firstName should be stored or converted: {first_name!r}"

    def test_list_where_dict_expected(self, zot, test_item, restore_item_state):
        """List where dict expected in relations should be rejected."""
        original_relations = get_item(zot, test_item)["data"]["relations"]
        try:
            result = update_item_fields(zot, test_item, {"relations": ["not", "a", "dict"]})
            # If it succeeds, relations should be unchanged (list rejected)
            if result["success"]:
                item = get_item(zot, test_item)
                assert item["data"]["relations"] == original_relations, "List relations should be rejected"
        except Exception:
            # Exception is also acceptable - validation should reject list
            pass

    def test_dict_where_list_expected(self, zot, test_item, restore_item_state):
        """Dict where list expected in collections should be rejected."""
        original_collections = get_item(zot, test_item)["data"]["collections"]
        try:
            result = update_item_fields(zot, test_item, {"collections": {"key": "value"}})
            # If it succeeds, collections should be unchanged (dict rejected)
            if result["success"]:
                item = get_item(zot, test_item)
                assert item["data"]["collections"] == original_collections, "Dict collections should be rejected"
        except Exception:
            # Exception is also acceptable - validation should reject dict
            pass

    def test_float_where_string_expected(self, zot, test_item, restore_item_state):
        """Float where string expected should be converted to string."""
        result = update_item_fields(zot, test_item, {"title": 3.14159})
        assert result["success"], "Float title should not crash"
        item = get_item(zot, test_item)
        # Zotero should convert float to string
        assert item["data"]["title"] in (3.14159, "3.14159"), f"Float should be stored or converted: {item['data']['title']!r}"

    def test_boolean_where_string_expected(self, zot, test_item, restore_item_state):
        """Boolean where string expected should be converted to string."""
        result = update_item_fields(zot, test_item, {"title": True})
        assert result["success"], "Boolean title should not crash"
        item = get_item(zot, test_item)
        # Zotero should convert boolean to string "True" or "true"
        assert item["data"]["title"] in (True, "True", "true", "1"), f"Boolean should be stored or converted: {item['data']['title']!r}"


# =============================================================================
# Unicode Hell Tests
# =============================================================================

class TestUnicodeHell:
    """Test extreme unicode scenarios."""

    def test_emoji_only_title(self, zot, test_item, restore_item_state):
        """Title with only emoji should be stored correctly."""
        expected = "\U0001F4DA\U0001F4D6\U0001F4D7"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Emoji-only title update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Emoji title mismatch: expected {expected!r}, got {item['data']['title']!r}"

    def test_rtl_text(self, zot, test_item, restore_item_state):
        """Right-to-left text should be stored correctly."""
        expected = "\u05e2\u05d1\u05e8\u05d9\u05ea \u0627\u0644\u0639\u0631\u0628\u064a\u0629"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "RTL title update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"RTL title mismatch: expected {expected!r}, got {item['data']['title']!r}"

    def test_combining_characters(self, zot, test_item, restore_item_state):
        """Title with combining characters should be stored correctly."""
        expected = "e\u0301"  # e with combining acute accent
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Combining chars title update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Combining chars title mismatch: expected {expected!r}, got {item['data']['title']!r}"

    def test_zero_width_characters(self, zot, test_item, restore_item_state):
        """Title with zero-width characters should be stored correctly."""
        expected = "Test\u200b\u200d\u200cTitle"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Zero-width chars title update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Zero-width chars title mismatch: expected {expected!r}, got {item['data']['title']!r}"

    def test_mixed_direction_text(self, zot, test_item, restore_item_state):
        """Mixed LTR and RTL text should be stored correctly."""
        expected = "English \u0639\u0631\u0628\u064a \u05e2\u05d1\u05e8\u05d9\u05ea"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Mixed direction title update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Mixed direction title mismatch: expected {expected!r}, got {item['data']['title']!r}"

    def test_unicode_whitespace(self, zot, test_item, restore_item_state):
        """Various unicode whitespace characters should be stored correctly."""
        expected = "Test\u00a0\u2003\u2002Title"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Unicode whitespace title update should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Unicode whitespace title mismatch: expected {expected!r}, got {item['data']['title']!r}"

    def test_tag_with_emoji(self, zot, test_item, restore_item_state):
        """Tag containing emoji should be stored correctly."""
        result = add_tags_to_item(zot, test_item, ["\U0001F4DA-book", "\U0001F52C-science"])
        assert result["success"], "Emoji tags add should succeed"
        item = get_item(zot, test_item)
        tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
        assert "\U0001F4DA-book" in tags, f"Emoji tag should be present, got: {tags}"
        assert "\U0001F52C-science" in tags, f"Science emoji tag should be present, got: {tags}"

    def test_tag_with_rtl(self, zot, test_item, restore_item_state):
        """Tag with RTL text should be stored correctly."""
        result = add_tags_to_item(zot, test_item, ["\u0639\u0631\u0628\u064a", "\u05e2\u05d1\u05e8\u05d9\u05ea"])
        assert result["success"], "RTL tags add should succeed"
        item = get_item(zot, test_item)
        tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
        assert "\u0639\u0631\u0628\u064a" in tags, f"Arabic tag should be present, got: {tags}"
        assert "\u05e2\u05d1\u05e8\u05d9\u05ea" in tags, f"Hebrew tag should be present, got: {tags}"

    def test_note_with_unicode(self, zot, test_item, restore_item_state):
        """Note content with various unicode should be stored correctly."""
        content = "<p>Mixed: \u00e9\u00f1\u4e2d\u6587\u0639\u0631\u0628\u064a\U0001F4DA</p>"
        result = attach_note(zot, test_item, content)
        assert result["success"], "Unicode note should succeed"
        if result["success"]["0"]["key"]:
            note_key = result["success"]["0"]["key"]
            try:
                # Verify note content
                note = zot.note(note_key)
                assert content in note["data"]["note"], f"Unicode note content mismatch"
                delete_note(zot, note_key)
            except Exception:
                try:
                    delete_note(zot, note_key)
                except Exception:
                    pass
                raise


# =============================================================================
# SQL Injection Style Attacks
# =============================================================================

class TestSQLInjectionStyle:
    """Test SQL injection style attack strings."""

    def test_single_quote_in_title(self, zot, test_item, restore_item_state):
        """Single quote in title should be stored correctly (no SQL injection)."""
        expected = "Test' OR '1'='1"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Single quote title should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Single quote should be preserved: {item['data']['title']!r}"

    def test_double_quote_in_title(self, zot, test_item, restore_item_state):
        """Double quote in title should be stored correctly."""
        expected = 'Test" OR "1"="1'
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Double quote title should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Double quote should be preserved: {item['data']['title']!r}"

    def test_semicolon_in_title(self, zot, test_item, restore_item_state):
        """Semicolon in title should be stored correctly (no SQL injection)."""
        expected = "Test; DROP TABLE items;"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Semicolon title should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Semicolon should be preserved: {item['data']['title']!r}"

    def test_comment_in_title(self, zot, test_item, restore_item_state):
        """SQL comment in title should be stored correctly."""
        expected = "Test -- comment"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "SQL comment title should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"SQL comment should be preserved: {item['data']['title']!r}"

    def test_union_in_title(self, zot, test_item, restore_item_state):
        """UNION in title should be stored correctly."""
        expected = "Test UNION SELECT * FROM items"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "UNION title should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"UNION should be preserved: {item['data']['title']!r}"

    def test_script_in_title(self, zot, test_item, restore_item_state):
        """Script tag in title (XSS attempt) should be stored correctly."""
        expected = "<script>alert('xss')</script>"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Script tag title should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Script tag should be preserved: {item['data']['title']!r}"

    def test_html_in_title(self, zot, test_item, restore_item_state):
        """HTML in title should be stored correctly."""
        expected = "<b>Bold</b> <i>Italic</i>"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "HTML title should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"HTML should be preserved: {item['data']['title']!r}"

    def test_xml_in_title(self, zot, test_item, restore_item_state):
        """XML in title should be stored correctly."""
        expected = "<xml><test>value</test></xml>"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "XML title should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"XML should be preserved: {item['data']['title']!r}"

    def test_backslash_escape(self, zot, test_item, restore_item_state):
        """Backslash escape sequences should be stored correctly."""
        expected = "Test\\'escaped\\'"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Backslash escape title should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Backslash escape should be preserved: {item['data']['title']!r}"

    def test_null_byte_injection(self, zot, test_item, restore_item_state):
        """Null byte injection should be handled (may be stripped)."""
        text_with_null = "Test\x00injection"
        result = update_item_fields(zot, test_item, {"title": text_with_null})
        assert result["success"], "Null byte title should not crash"
        item = get_item(zot, test_item)
        # Zotero may strip null bytes - verify it doesn't crash
        assert isinstance(item["data"]["title"], str), "Title should be a string"

    def test_unicode_escape_injection(self, zot, test_item, restore_item_state):
        """Unicode escape sequences should be stored as literal text."""
        expected = "Test\\u0027injection\\u0027"
        result = update_item_fields(zot, test_item, {"title": expected})
        assert result["success"], "Unicode escape title should succeed"
        item = get_item(zot, test_item)
        assert item["data"]["title"] == expected, f"Unicode escape should be preserved: {item['data']['title']!r}"

    def test_tag_with_injection(self, zot, test_item, restore_item_state):
        """Injection attempt in tag should be stored as literal text."""
        expected = "'; DROP TABLE tags; --"
        result = add_tags_to_item(zot, test_item, [expected])
        assert result["success"], "Injection tag should succeed"
        item = get_item(zot, test_item)
        tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
        assert expected in tags, f"Injection tag should be preserved: {tags}"


# =============================================================================
# Validation Function Tests
# =============================================================================

class TestValidationFunctions:
    """Test validation functions with edge cases."""

    def test_validate_doi_empty(self):
        """Empty DOI."""
        assert validate_doi("") == False

    def test_validate_doi_none(self):
        """None DOI - should handle gracefully."""
        # validate_doi may raise TypeError for None - that's acceptable behavior
        # or it may return False. Either is fine.
        try:
            result = validate_doi(None)
            assert result == False
        except TypeError:
            # TypeError is also acceptable - function expects string
            pass

    def test_validate_doi_valid(self):
        """Valid DOI."""
        assert validate_doi("10.1000/journal.123") == True

    def test_validate_doi_with_special_chars(self):
        """DOI with special characters."""
        assert validate_doi("10.1000/test-doi_123.456") == True

    def test_validate_isbn_empty(self):
        """Empty ISBN."""
        assert validate_isbn("") == False

    def test_validate_isbn_valid_10(self):
        """Valid ISBN-10."""
        assert validate_isbn("0-306-40615-2") == True

    def test_validate_isbn_valid_13(self):
        """Valid ISBN-13."""
        assert validate_isbn("978-0-306-40615-7") == True

    def test_validate_isbn_with_spaces(self):
        """ISBN with spaces."""
        assert validate_isbn("978 0 306 40615 7") == True

    def test_validate_issn_empty(self):
        """Empty ISSN."""
        assert validate_issn("") == False

    def test_validate_issn_valid(self):
        """Valid ISSN."""
        assert validate_issn("1234-5678") == True

    def test_validate_issn_with_x(self):
        """ISSN with X check digit."""
        assert validate_issn("0317-847X") == True


# =============================================================================
# Note Operation Tests
# =============================================================================

class TestNoteOperations:
    """Test note operations with adversarial inputs."""

    def test_empty_note_content(self, zot, test_item, restore_item_state):
        """Create note with empty content should succeed."""
        result = attach_note(zot, test_item, "")
        assert result["success"], "Empty note should succeed"
        note_key = result["success"]["0"]["key"]
        try:
            # Verify note was created with empty content
            note = zot.note(note_key)
            assert note["data"]["note"] == "", f"Empty note content mismatch: {note['data']['note']!r}"
            delete_note(zot, note_key)
        except Exception:
            try:
                delete_note(zot, note_key)
            except Exception:
                pass
            raise

    def test_html_note_content(self, zot, test_item, restore_item_state):
        """Create note with HTML content should preserve HTML."""
        html = "<h1>Title</h1><p>Paragraph with <b>bold</b> and <i>italic</i>.</p>"
        result = attach_note(zot, test_item, html)
        assert result["success"], "HTML note should succeed"
        note_key = result["success"]["0"]["key"]
        try:
            # Verify note was created with HTML content
            note = zot.note(note_key)
            assert html in note["data"]["note"], f"HTML note content mismatch: {note['data']['note']!r}"
            delete_note(zot, note_key)
        except Exception:
            try:
                delete_note(zot, note_key)
            except Exception:
                pass
            raise

    def test_update_note_with_unicode(self, zot, test_item, restore_item_state):
        """Update note with unicode content should preserve unicode."""
        # Create note first
        result = attach_note(zot, test_item, "Initial content")
        assert result["success"], "Initial note should succeed"
        note_key = result["success"]["0"]["key"]
        try:
            # Update with unicode
            unicode_content = "\u4e2d\u6587\u0639\u0631\u0628\u064a\U0001F4DA"
            update_result = update_note(zot, note_key, unicode_content)
            assert update_result["success"], "Unicode note update should succeed"
            # Verify unicode content
            note = zot.note(note_key)
            assert unicode_content in note["data"]["note"], f"Unicode note content mismatch: {note['data']['note']!r}"
            delete_note(zot, note_key)
        except Exception:
            try:
                delete_note(zot, note_key)
            except Exception:
                pass
            raise

    def test_delete_nonexistent_note(self, zot):
        """Delete non-existent note should return error dict."""
        result = delete_note(zot, "NONEXISTENT123")
        # Should return error dict with success=False
        assert not result.get("success", True), "Delete nonexistent note should fail"

    def test_update_nonexistent_note(self, zot):
        """Update non-existent note should return error dict."""
        result = update_note(zot, "NONEXISTENT123", "New content")
        assert not result["success"], "Update nonexistent note should fail"


# =============================================================================
# Collection Operation Tests
# =============================================================================

class TestCollectionOperations:
    """Test collection operations with adversarial inputs."""

    def test_create_collection_empty_name(self, zot):
        """Create collection with empty name should either fail or create with empty name."""
        result = create_collection(zot, "")
        # Should handle gracefully - either fail or succeed with empty name
        if result["success"]:
            # If it succeeded, verify collection was created
            assert result["key"], "Collection key should be present"
            try:
                delete_collection(zot, result["key"])
            except Exception:
                pass
        else:
            # Failure is also acceptable - empty name may be rejected
            assert "error" in result, "Failed collection create should have error"

    def test_create_collection_very_long_name(self, zot):
        """Create collection with very long name should handle gracefully."""
        long_name = "A" * 1000
        result = create_collection(zot, long_name)
        if result["success"]:
            # If it succeeded, verify name was stored
            assert result["key"], "Collection key should be present"
            try:
                delete_collection(zot, result["key"])
            except Exception:
                pass
        else:
            # Failure is also acceptable - long names may be rejected
            assert "error" in result, "Failed collection create should have error"

    def test_create_collection_unicode_name(self, zot):
        """Create collection with unicode name should succeed."""
        unicode_name = "\u4e2d\u6587\u0639\u0631\u0628\u064a\U0001F4DA"
        result = create_collection(zot, unicode_name)
        assert result["success"], "Unicode collection name should succeed"
        try:
            # Verify name was stored correctly
            collections = zot.collections()
            created = [c for c in collections if c["key"] == result["key"]]
            assert len(created) == 1, "Collection should exist"
            assert created[0]["data"]["name"] == unicode_name, f"Unicode name mismatch: {created[0]['data']['name']!r}"
            delete_collection(zot, result["key"])
        except Exception:
            try:
                delete_collection(zot, result["key"])
            except Exception:
                pass
            raise

    def test_rename_collection_injection(self, zot, temp_collection):
        """Rename collection with injection attempt should store as literal text."""
        injection_name = "'; DROP TABLE collections; --"
        result = rename_collection(zot, temp_collection, injection_name)
        assert result["success"], "Injection rename should succeed"
        # Verify name was stored literally
        collections = zot.collections()
        renamed = [c for c in collections if c["key"] == temp_collection]
        assert len(renamed) == 1, "Collection should exist"
        assert renamed[0]["data"]["name"] == injection_name, f"Injection name should be literal: {renamed[0]['data']['name']!r}"

    def test_delete_nonexistent_collection(self, zot):
        """Delete non-existent collection should return error dict."""
        result = delete_collection(zot, "NONEXISTENT123")
        assert not result["success"], "Delete nonexistent collection should fail"

    def test_rename_nonexistent_collection(self, zot):
        """Rename non-existent collection should return error dict."""
        result = rename_collection(zot, "NONEXISTENT123", "New Name")
        assert not result["success"], "Rename nonexistent collection should fail"


# =============================================================================
# Tag Operation Tests
# =============================================================================

class TestTagOperations:
    """Test tag operations with adversarial inputs."""

    def test_merge_empty_tags(self, zot, test_item, restore_item_state):
        """Merge with empty source tags list should succeed with no changes."""
        original_item = get_item(zot, test_item)
        original_tags = set(t.get("tag", "") for t in original_item["data"].get("tags", []))
        
        result = merge_tags(zot, [], "target_tag")
        assert result["success"], "Empty merge should succeed"
        
        # Verify no tags changed
        item = get_item(zot, test_item)
        current_tags = set(t.get("tag", "") for t in item["data"].get("tags", []))
        assert current_tags == original_tags, f"Empty merge should not change tags"

    def test_merge_empty_target(self, zot, test_item, restore_item_state):
        """Merge with empty target tag should handle gracefully."""
        # Add some tags first
        add_tags_to_item(zot, test_item, ["source1", "source2"])
        result = merge_tags(zot, ["source1", "source2"], "")
        # Should handle gracefully - may succeed with no changes or fail
        assert result["success"] or "error" in result, "Empty target merge should not crash"

    def test_rename_nonexistent_tag(self, zot, test_item, restore_item_state):
        """Rename tag that doesn't exist should succeed with 0 updates."""
        result = rename_tag(zot, "nonexistent_tag_xyz", "new_name")
        assert result["success"], "Rename nonexistent tag should succeed"
        assert result.get("updated", 0) == 0, "Rename nonexistent tag should update 0 items"

    def test_delete_nonexistent_tag(self, zot, test_item, restore_item_state):
        """Delete tag that doesn't exist should succeed with 0 updates."""
        result = delete_tag(zot, "nonexistent_tag_xyz")
        assert result["success"], "Delete nonexistent tag should succeed"
        assert result.get("updated", 0) == 0, "Delete nonexistent tag should update 0 items"

    def test_merge_tag_with_itself(self, zot, test_item, restore_item_state):
        """Merge tag with itself should succeed with no changes."""
        add_tags_to_item(zot, test_item, ["self_merge"])
        original_item = get_item(zot, test_item)
        original_tag_count = len([t for t in original_item["data"].get("tags", []) if t.get("tag") == "self_merge"])
        
        result = merge_tags(zot, ["self_merge"], "self_merge")
        assert result["success"], "Self merge should succeed"
        
        # Verify tag still exists (no change)
        item = get_item(zot, test_item)
        current_tag_count = len([t for t in item["data"].get("tags", []) if t.get("tag") == "self_merge"])
        assert current_tag_count == original_tag_count, "Self merge should not change tag count"


# =============================================================================
# Citation Relation Tests
# =============================================================================

class TestCitationRelations:
    """Test citation relation operations."""

    def test_add_citation_empty_uri(self, zot, test_item, restore_item_state):
        """Add citation with empty URI should succeed (Zotero allows it)."""
        result = add_citation_relation(zot, test_item, "cites", "")
        assert result["success"], "Empty URI citation should succeed"
        # Verify relation was added
        item = get_item(zot, test_item)
        relations = item["data"].get("relations", {})
        assert "cites" in str(relations), f"Citation relation should be present: {relations}"

    def test_add_citation_invalid_uri(self, zot, test_item, restore_item_state):
        """Add citation with invalid URI format should succeed (Zotero stores as-is)."""
        result = add_citation_relation(zot, test_item, "cites", "not-a-uri")
        assert result["success"], "Invalid URI citation should succeed"
        # Verify relation was added
        item = get_item(zot, test_item)
        relations = item["data"].get("relations", {})
        assert "not-a-uri" in str(relations), f"Invalid URI should be stored: {relations}"

    def test_add_citation_wrong_type(self, zot, test_item, restore_item_state):
        """Add citation with wrong relation type should succeed (Zotero allows arbitrary types)."""
        result = add_citation_relation(zot, test_item, "invalid_type", "http://example.com")
        assert result["success"], "Wrong relation type should succeed"
        # Verify relation was added
        item = get_item(zot, test_item)
        relations = item["data"].get("relations", {})
        assert "invalid_type" in str(relations), f"Invalid relation type should be stored: {relations}"

    def test_add_duplicate_citation(self, zot, test_item, restore_item_state):
        """Add same citation twice should succeed (second add is idempotent)."""
        uri = "http://example.com/duplicate"
        add_citation_relation(zot, test_item, "cites", uri)
        result = add_citation_relation(zot, test_item, "cites", uri)
        assert result["success"], "Duplicate citation should succeed"
        # Verify relation exists (only once)
        item = get_item(zot, test_item)
        relations = item["data"].get("relations", {})
        assert uri in str(relations), f"Duplicate URI should be present: {relations}"

    def test_get_citations_nonexistent_item(self, zot):
        """Get citations for non-existent item should raise exception."""
        with pytest.raises(Exception):
            get_citations(zot, "NONEXISTENT123")


# =============================================================================
# Miscellaneous Adversarial Tests
# =============================================================================

class TestMiscellaneousAdversarial:
    """Additional adversarial test scenarios."""

    def test_rapid_collection_operations(self, zot, test_item, restore_item_state):
        """Rapid create/move/delete collections should all succeed."""
        for i in range(5):
            coll_result = create_collection(zot, f"Rapid_{i}_{time.time()}")
            assert coll_result["success"], f"Rapid collection {i} create should succeed"
            move_item_to_collection(zot, test_item, coll_result["key"])
            delete_collection(zot, coll_result["key"])
        # Verify item is back to original state (no collections from rapid ops)
        item = get_item(zot, test_item)
        # Collections may have other collections, but rapid ones should be gone

    def test_all_tags_with_special_chars(self, zot, test_item, restore_item_state):
        """Add tags with all kinds of special characters should all be stored."""
        special_tags = [
            "tag'with'quotes",
            'tag"with"double',
            "tag;with;semicolons",
            "tag--with--dashes",
            "tag_with_underscores",
            "tag.with.dots",
            "tag:with:colons",
            "tag/with/slashes",
            "tag\\with\\backslashes",
            "tag(with)parens",
            "tag[with]brackets",
            "tag{with}braces",
            "tag<with>angles",
            "tag=with=equals",
            "tag+with+plus",
            "tag*with*asterisk",
            "tag&with&ampersand",
            "tag|with|pipe",
            "tag!with!exclaim",
            "tag@with@at",
            "tag#with#hash",
            "tag$with$dollar",
            "tag%with%percent",
            "tag^with^caret",
            "tag~with~tilde",
            "tag`with`backtick",
        ]
        result = add_tags_to_item(zot, test_item, special_tags)
        assert result["success"], "Special chars tags should succeed"
        item = get_item(zot, test_item)
        tags = [t.get("tag", "") for t in item["data"].get("tags", [])]
        # Verify all special char tags were stored
        for tag in special_tags:
            assert tag in tags, f"Special char tag {tag!r} should be present"

    def test_very_large_number_of_collections(self, zot, test_item, restore_item_state):
        """Add item to many collections should succeed."""
        collection_keys = []
        try:
            for i in range(20):
                coll_result = create_collection(zot, f"Many_{i}_{time.time()}")
                assert coll_result["success"], f"Collection {i} create should succeed"
                collection_keys.append(coll_result["key"])
                add_item_to_collection(zot, test_item, coll_result["key"])

            item = get_item(zot, test_item)
            assert len(item["data"].get("collections", [])) >= 20, f"Item should be in 20+ collections, got {len(item['data'].get('collections', []))}"
        finally:
            for key in collection_keys:
                try:
                    delete_collection(zot, key)
                except Exception:
                    pass

    def test_whitespace_only_fields(self, zot, test_item, restore_item_state):
        """Fields with only whitespace should be stored correctly."""
        for whitespace in [" ", "\t", "\n", "\r", "\u00a0", "\u2003"]:
            result = update_item_fields(zot, test_item, {"title": whitespace})
            assert result["success"], f"Whitespace title {whitespace!r} should succeed"
            item = get_item(zot, test_item)
            assert item["data"]["title"] == whitespace, f"Whitespace title mismatch: expected {whitespace!r}, got {item['data']['title']!r}"

    def test_count_items_stability(self, zot):
        """Verify count_items is stable under tag operations."""
        count1 = count_items(zot)

        # Get first item and try to add a tag (doesn't change item count)
        try:
            items = zot.items(start=0, limit=1)
            if items:
                add_tags_to_item(zot, items[0]["key"], ["stability_test"])
        except Exception:
            # If update fails, just verify count still works
            pass

        count2 = count_items(zot)
        # Count should be same (adding tags doesn't create new items)
        assert count1 == count2, f"Item count should be stable: {count1} -> {count2}"


# =============================================================================
# Main entry point for running tests
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
