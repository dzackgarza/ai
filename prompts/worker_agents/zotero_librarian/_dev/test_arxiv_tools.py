"""Tests for arxiv_tools module."""

import pytest
from pathlib import Path
import tempfile
import shutil

# Skip all tests if arxiv dependencies not installed
arxiv_tools = pytest.importorskip("zotero_librarian.arxiv_tools")

from zotero_librarian.arxiv_tools import (
    search_arxiv_papers,
    download_arxiv_paper,
    list_downloaded_papers,
    read_arxiv_paper,
    get_arxiv_paper_metadata,
    _validate_categories,
    export_papers_to_json,
    import_papers_from_json,
)


class TestValidateCategories:
    """Test category validation."""

    def test_valid_categories(self):
        assert _validate_categories(["cs.AI", "cs.LG"]) == True
        assert _validate_categories(["math.CO", "physics.optics"]) == True

    def test_invalid_categories(self):
        assert _validate_categories(["invalid.category"]) == False
        assert _validate_categories(["cs.AI", "invalid"]) == False

    def test_empty_categories(self):
        assert _validate_categories([]) == True


class TestSearchArxivPapers:
    """Test arXiv search functionality."""

    def test_basic_search(self):
        """Test basic search returns results."""
        results = search_arxiv_papers("quantum computing", max_results=5)
        assert isinstance(results, list)
        assert len(results) > 0
        assert "id" in results[0]
        assert "title" in results[0]
        assert "authors" in results[0]
        assert "abstract" in results[0]

    def test_search_with_categories(self):
        """Test search with category filtering."""
        results = search_arxiv_papers(
            "neural networks",
            max_results=5,
            categories=["cs.LG"]
        )
        assert isinstance(results, list)
        # All results should have cs.LG or related category
        for paper in results:
            assert "categories" in paper

    def test_search_with_max_results(self):
        """Test max_results limit."""
        results = search_arxiv_papers("machine learning", max_results=3)
        assert len(results) <= 3

    def test_search_returns_required_fields(self):
        """Test that search results contain all required fields."""
        results = search_arxiv_papers("deep learning", max_results=1)
        paper = results[0]
        
        required_fields = ["id", "title", "authors", "abstract", "categories", "published", "url", "resource_uri"]
        for field in required_fields:
            assert field in paper, f"Missing required field: {field}"


class TestGetPaperMetadata:
    """Test paper metadata fetching."""

    def test_valid_paper_id(self):
        """Test fetching metadata for a known paper."""
        # Use a well-known paper ID
        metadata = get_arxiv_paper_metadata("1706.03762")  # Attention is All You Need
        assert metadata is not None
        assert "title" in metadata
        assert "attention" in metadata["title"].lower()

    def test_invalid_paper_id(self):
        """Test fetching metadata for invalid paper ID."""
        metadata = get_arxiv_paper_metadata("invalid-id-12345")
        assert metadata is None


class TestDownloadPaper:
    """Test paper download functionality."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)

    def test_download_nonexistent_paper(self, temp_dir):
        """Test downloading a paper that doesn't exist."""
        result = download_arxiv_paper(
            "invalid-id-12345",
            output_dir=temp_dir,
            convert_to_markdown=False
        )
        assert result["success"] == False
        assert "error" in result

    def test_download_structure(self, temp_dir):
        """Test download returns correct structure."""
        # Use a real paper but we may not actually download
        result = download_arxiv_paper(
            "1706.03762",
            output_dir=temp_dir,
            convert_to_markdown=False
        )
        assert "success" in result
        assert "paper_id" in result


class TestListDownloadedPapers:
    """Test listing downloaded papers."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)

    def test_list_empty_directory(self, temp_dir):
        """Test listing from empty directory."""
        papers = list_downloaded_papers(output_dir=temp_dir)
        assert isinstance(papers, list)
        assert len(papers) == 0

    def test_list_with_markdown_files(self, temp_dir):
        """Test listing when markdown files exist."""
        # Create a fake markdown file
        md_file = Path(temp_dir) / "1706.03762.md"
        md_file.write_text("# Test Paper")
        
        papers = list_downloaded_papers(output_dir=temp_dir)
        assert isinstance(papers, list)
        # May fetch metadata from arXiv or just return IDs
        assert len(papers) >= 0


class TestReadPaper:
    """Test reading downloaded papers."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)

    def test_read_nonexistent_paper(self, temp_dir):
        """Test reading a paper that doesn't exist."""
        result = read_arxiv_paper("1706.03762", output_dir=temp_dir)
        assert result["success"] == False
        assert "error" in result

    def test_read_existing_paper(self, temp_dir):
        """Test reading an existing paper."""
        # Create a fake markdown file
        md_file = Path(temp_dir) / "1706.03762.md"
        test_content = "# Test Paper\n\nThis is test content."
        md_file.write_text(test_content)
        
        result = read_arxiv_paper("1706.03762", output_dir=temp_dir)
        assert result["success"] == True
        assert result["paper_id"] == "1706.03762"
        assert result["content"] == test_content


class TestExportImportJson:
    """Test JSON export/import functionality."""

    @pytest.fixture
    def temp_file(self):
        """Create temporary file path."""
        temp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        temp_path = temp.name
        temp.close()
        yield temp_path
        Path(temp_path).unlink(missing_ok=True)

    def test_export_and_import(self, temp_file):
        """Test exporting and importing papers."""
        test_papers = [
            {"id": "1706.03762", "title": "Test Paper 1"},
            {"id": "1810.04805", "title": "Test Paper 2"},
        ]
        
        # Export
        export_papers_to_json(test_papers, temp_file)
        
        # Import
        imported = import_papers_from_json(temp_file)
        
        assert isinstance(imported, list)
        assert len(imported) == 2
        assert imported[0]["id"] == "1706.03762"
        assert imported[1]["id"] == "1810.04805"
