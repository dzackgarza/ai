"""
arXiv Tools for Zotero Librarian

Simple, composable tools for searching and downloading arXiv papers.
No MCP layer - pure Python functions.

Dependencies:
    pip install arxiv httpx python-dateutil pymupdf4llm

Usage:
    from zotero_librarian.arxiv_tools import (
        search_arxiv_papers,
        download_arxiv_paper,
        list_downloaded_papers,
        read_arxiv_paper,
    )
    
    # Search for papers
    results = search_arxiv_papers("transformer attention", max_results=10, categories=["cs.LG"])
    
    # Download a paper
    download_arxiv_paper("2301.12345", output_dir="~/papers")
    
    # List downloaded papers
    papers = list_downloaded_papers("~/papers")
    
    # Read paper content
    content = read_arxiv_paper("2301.12345", "~/papers")
"""

import arxiv
import httpx
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
from dateutil import parser as date_parser


# =============================================================================
# Configuration
# =============================================================================

# arXiv API endpoint for raw queries
ARXIV_API_URL = "https://export.arxiv.org/api/query"

# XML namespaces for arXiv Atom feed
ARXIV_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}

# Valid arXiv category prefixes
VALID_CATEGORIES = {
    "cs", "econ", "eess", "math", "physics", "q-bio", "q-fin", "stat",
    "astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat", "hep-ph",
    "hep-th", "math-ph", "nlin", "nucl-ex", "nucl-th", "quant-ph",
}

# Complete arXiv category name mappings (from Zotero arXiv.org translator)
# Maps arXiv category codes to human-readable names
ARXIV_CATEGORIES = {
    # Top-level archives
    "cs": "Computer Science",
    "econ": "Economics",
    "eess": "Electrical Engineering and Systems Science",
    "math": "Mathematics",
    "nlin": "Nonlinear Sciences",
    "physics": "Physics",
    "q-fin": "Quantitative Finance",
    "stat": "Statistics",
    
    # Mathematics subcategories
    "math.AC": "Commutative Algebra",
    "math.AG": "Algebraic Geometry",
    "math.AP": "Analysis of PDEs",
    "math.AT": "Algebraic Topology",
    "math.CA": "Classical Analysis and ODEs",
    "math.CO": "Combinatorics",
    "math.CT": "Category Theory",
    "math.CV": "Complex Variables",
    "math.DG": "Differential Geometry",
    "math.DS": "Dynamical Systems",
    "math.FA": "Functional Analysis",
    "math.GM": "General Mathematics",
    "math.GN": "General Topology",
    "math.GR": "Group Theory",
    "math.GT": "Geometric Topology",
    "math.HO": "History and Overview",
    "math.IT": "Information Theory",
    "math.KT": "K-Theory and Homology",
    "math.LO": "Logic",
    "math.MG": "Metric Geometry",
    "math.MP": "Mathematical Physics",
    "math.NA": "Numerical Analysis",
    "math.NT": "Number Theory",
    "math.OA": "Operator Algebras",
    "math.OC": "Optimization and Control",
    "math.PR": "Probability",
    "math.QA": "Quantum Algebra",
    "math.RA": "Rings and Algebras",
    "math.RT": "Representation Theory",
    "math.SG": "Symplectic Geometry",
    "math.SP": "Spectral Theory",
    "math.ST": "Statistics Theory",
    
    # Physics subcategories
    "acc-phys": "Accelerator Physics",
    "astro-ph": "Astrophysics",
    "astro-ph.CO": "Cosmology and Nongalactic Astrophysics",
    "astro-ph.EP": "Earth and Planetary Astrophysics",
    "astro-ph.GA": "Astrophysics of Galaxies",
    "astro-ph.HE": "High Energy Astrophysical Phenomena",
    "astro-ph.IM": "Instrumentation and Methods for Astrophysics",
    "astro-ph.SR": "Solar and Stellar Astrophysics",
    "atom-ph": "Atomic, Molecular and Optical Physics",
    "chem-ph": "Chemical Physics",
    "cond-mat": "Condensed Matter",
    "cond-mat.dis-nn": "Disordered Systems and Neural Networks",
    "cond-mat.mes-hall": "Mesoscale and Nanoscale Physics",
    "cond-mat.mtrl-sci": "Materials Science",
    "cond-mat.other": "Other Condensed Matter",
    "cond-mat.quant-gas": "Quantum Gases",
    "cond-mat.soft": "Soft Condensed Matter",
    "cond-mat.stat-mech": "Statistical Mechanics",
    "cond-mat.str-el": "Strongly Correlated Electrons",
    "cond-mat.supr-con": "Superconductivity",
    "gr-qc": "General Relativity and Quantum Cosmology",
    "hep-ex": "High Energy Physics - Experiment",
    "hep-lat": "High Energy Physics - Lattice",
    "hep-ph": "High Energy Physics - Phenomenology",
    "hep-th": "High Energy Physics - Theory",
    "math-ph": "Mathematical Physics",
    "nucl-ex": "Nuclear Experiment",
    "nucl-th": "Nuclear Theory",
    "physics.acc-ph": "Accelerator Physics",
    "physics.ao-ph": "Atmospheric and Oceanic Physics",
    "physics.app-ph": "Applied Physics",
    "physics.atm-clus": "Atomic and Molecular Clusters",
    "physics.atom-ph": "Atomic Physics",
    "physics.bio-ph": "Biological Physics",
    "physics.chem-ph": "Chemical Physics",
    "physics.class-ph": "Classical Physics",
    "physics.comp-ph": "Computational Physics",
    "physics.data-an": "Data Analysis, Statistics and Probability",
    "physics.ed-ph": "Physics Education",
    "physics.flu-dyn": "Fluid Dynamics",
    "physics.gen-ph": "General Physics",
    "physics.geo-ph": "Geophysics",
    "physics.hist-ph": "History and Philosophy of Physics",
    "physics.ins-det": "Instrumentation and Detectors",
    "physics.med-ph": "Medical Physics",
    "physics.optics": "Optics",
    "physics.plasm-ph": "Plasma Physics",
    "physics.pop-ph": "Popular Physics",
    "physics.soc-ph": "Physics and Society",
    "physics.space-ph": "Space Physics",
    "quant-ph": "Quantum Physics",
    
    # Computer Science subcategories
    "cs.AI": "Artificial Intelligence",
    "cs.AR": "Hardware Architecture",
    "cs.CC": "Computational Complexity",
    "cs.CE": "Computational Engineering, Finance, and Science",
    "cs.CG": "Computational Geometry",
    "cs.CL": "Computation and Language",
    "cs.CR": "Cryptography and Security",
    "cs.CV": "Computer Vision and Pattern Recognition",
    "cs.CY": "Computers and Society",
    "cs.DB": "Databases",
    "cs.DC": "Distributed, Parallel, and Cluster Computing",
    "cs.DL": "Digital Libraries",
    "cs.DM": "Discrete Mathematics",
    "cs.DS": "Data Structures and Algorithms",
    "cs.ET": "Emerging Technologies",
    "cs.FL": "Formal Languages and Automata Theory",
    "cs.GL": "General Literature",
    "cs.GR": "Graphics",
    "cs.GT": "Computer Science and Game Theory",
    "cs.HC": "Human-Computer Interaction",
    "cs.IR": "Information Retrieval",
    "cs.IT": "Information Theory",
    "cs.LG": "Machine Learning",
    "cs.LO": "Logic in Computer Science",
    "cs.MA": "Multiagent Systems",
    "cs.MM": "Multimedia",
    "cs.MS": "Mathematical Software",
    "cs.NA": "Numerical Analysis",
    "cs.NE": "Neural and Evolutionary Computing",
    "cs.NI": "Networking and Internet Architecture",
    "cs.OH": "Other Computer Science",
    "cs.OS": "Operating Systems",
    "cs.PF": "Performance",
    "cs.PL": "Programming Languages",
    "cs.RO": "Robotics",
    "cs.SC": "Symbolic Computation",
    "cs.SD": "Sound",
    "cs.SE": "Software Engineering",
    "cs.SI": "Social and Information Networks",
    "cs.SY": "Systems and Control",
    
    # Other subcategories
    "econ.EM": "Econometrics",
    "econ.GN": "General Economics",
    "econ.TH": "Theoretical Economics",
    "eess.AS": "Audio and Speech Processing",
    "eess.IV": "Image and Video Processing",
    "eess.SP": "Signal Processing",
    "eess.SY": "Systems and Control",
    "nlin.AO": "Adaptation and Self-Organizing Systems",
    "nlin.CD": "Chaotic Dynamics",
    "nlin.CG": "Cellular Automata and Lattice Gases",
    "nlin.PS": "Pattern Formation and Solitons",
    "nlin.SI": "Exactly Solvable and Integrable Systems",
    "q-bio": "Quantitative Biology",
    "q-bio.BM": "Biomolecules",
    "q-bio.CB": "Cell Behavior",
    "q-bio.GN": "Genomics",
    "q-bio.MN": "Molecular Networks",
    "q-bio.NC": "Neurons and Cognition",
    "q-bio.OT": "Other Quantitative Biology",
    "q-bio.PE": "Populations and Evolution",
    "q-bio.QM": "Quantitative Methods",
    "q-bio.SC": "Subcellular Processes",
    "q-bio.TO": "Tissues and Organs",
    "q-fin.CP": "Computational Finance",
    "q-fin.EC": "Economics",
    "q-fin.GN": "General Finance",
    "q-fin.MF": "Mathematical Finance",
    "q-fin.PM": "Portfolio Management",
    "q-fin.PR": "Pricing of Securities",
    "q-fin.RM": "Risk Management",
    "q-fin.ST": "Statistical Finance",
    "q-fin.TR": "Trading and Market Microstructure",
    "stat.AP": "Applications",
    "stat.CO": "Computation",
    "stat.ME": "Methodology",
    "stat.ML": "Machine Learning",
    "stat.OT": "Other Statistics",
    "stat.TH": "Statistics Theory",
}

# Default storage directory for downloaded papers
DEFAULT_STORAGE_PATH = Path.home() / ".arxiv-papers"


def format_arxiv_category(category: str) -> Optional[str]:
    """
    Format an arXiv category code as a human-readable name.
    
    Matches the Zotero arXiv.org translator's category formatting.
    
    Args:
        category: arXiv category code (e.g., "math.AG", "cs.LG")
    
    Returns:
        Human-readable category name (e.g., "Mathematics - Algebraic Geometry")
        or None if category not found.
    
    Examples:
        >>> format_arxiv_category("math.AG")
        'Mathematics - Algebraic Geometry'
        >>> format_arxiv_category("cs.LG")
        'Computer Science - Machine Learning'
        >>> format_arxiv_category("math")
        'Mathematics'
    """
    if category in ARXIV_CATEGORIES:
        name = ARXIV_CATEGORIES[category]
        # For subcategories, add main archive prefix
        if "." in category:
            main_cat = category.split(".")[0]
            if main_cat in ARXIV_CATEGORIES:
                return f"{ARXIV_CATEGORIES[main_cat]} - {name}"
        return name
    return None


def format_arxiv_categories(categories: List[str]) -> List[str]:
    """
    Format a list of arXiv category codes as human-readable names.
    
    Args:
        categories: List of arXiv category codes
    
    Returns:
        List of formatted category names
    
    Example:
        >>> format_arxiv_categories(["math.AG", "math.DG"])
        ['Mathematics - Algebraic Geometry', 'Mathematics - Differential Geometry']
    """
    formatted = []
    for cat in categories:
        formatted_name = format_arxiv_category(cat)
        if formatted_name:
            formatted.append(formatted_name)
        else:
            formatted.append(cat)  # Keep original if not found
    return formatted


# =============================================================================
# Search Tools
# =============================================================================

def search_arxiv_papers(
    query: str,
    max_results: int = 10,
    categories: Optional[List[str]] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    sort_by: str = "relevance",
) -> List[Dict[str, Any]]:
    """
    Search for papers on arXiv with advanced filtering.

    Args:
        query: Search query. Use quoted phrases for exact matches:
               '"machine learning" OR "deep learning"'.
               Field-specific searches: ti:"title", au:"author", abs:"abstract".
        max_results: Maximum results to return (default: 10, max: 50).
        categories: Optional arXiv categories to filter (e.g., ["cs.AI", "cs.LG"]).
                    For math papers, always specify category (default focus: math.AG).
        date_from: Start date in YYYY-MM-DD format.
        date_to: End date in YYYY-MM-DD format.
        sort_by: Sort by "relevance" (default) or "date".

    Returns:
        List of paper dictionaries with keys:
        - id: arXiv ID (e.g., "2301.12345")
        - title: Paper title
        - authors: List of author names
        - abstract: Paper abstract
        - categories: List of arXiv categories
        - published: Publication date (ISO format)
        - url: PDF URL
        - resource_uri: arxiv:// URI

    Example:
        >>> # Search in algebraic geometry (default focus)
        >>> results = search_arxiv_papers(
        ...     "derived categories",
        ...     max_results=10,
        ...     categories=["math.AG"]
        ... )
        >>> for paper in results:
        ...     print(f"{paper['id']}: {paper['title']}")
    """
    # Validate categories
    if categories and not _validate_categories(categories):
        raise ValueError("Invalid arXiv category provided")

    # Use raw HTTP API for date filtering (avoids URL encoding issues)
    if date_from or date_to:
        return _raw_arxiv_search(
            query=query,
            max_results=max_results,
            categories=categories,
            date_from=date_from,
            date_to=date_to,
            sort_by=sort_by,
        )

    # Use arxiv package for simple queries
    return _arxiv_package_search(
        query=query,
        max_results=max_results,
        categories=categories,
        sort_by=sort_by,
    )


def _raw_arxiv_search(
    query: str,
    max_results: int,
    categories: Optional[List[str]],
    date_from: Optional[str],
    date_to: Optional[str],
    sort_by: str,
) -> List[Dict[str, Any]]:
    """
    Perform arXiv search using raw HTTP requests.

    This bypasses the arxiv Python package to avoid URL encoding issues
    with date filters (the '+' in '+TO+' must remain literal).
    """
    query_parts = []

    if query.strip():
        query_parts.append(f"({query})")

    if categories:
        category_filter = " OR ".join(f"cat:{cat}" for cat in categories)
        query_parts.append(f"({category_filter})")

    if date_from or date_to:
        try:
            start_date = date_parser.parse(date_from).strftime("%Y%m%d0000") if date_from else "199107010000"
            end_date = date_parser.parse(date_to).strftime("%Y%m%d2359") if date_to else datetime.now().strftime("%Y%m%d2359")
            # CRITICAL: '+TO+' must remain literal, not URL-encoded
            date_filter = f"submittedDate:[{start_date}+TO+{end_date}]"
            query_parts.append(date_filter)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid date format. Use YYYY-MM-DD: {e}")

    if not query_parts:
        raise ValueError("No search criteria provided")

    final_query = " AND ".join(query_parts)

    # Map sort parameter
    sort_map = {"relevance": "relevance", "date": "submittedDate"}
    sort_order = "descending"

    # Build URL manually to preserve '+TO+' in date ranges
    encoded_query = final_query.replace(" AND ", "+AND+").replace(" OR ", "+OR+").replace(" ", "+")
    base_params = f"max_results={max_results}&sortBy={sort_map.get(sort_by, 'relevance')}&sortOrder={sort_order}"
    url = f"{ARXIV_API_URL}?search_query={encoded_query}&{base_params}"

    # Make request
    response = httpx.get(url, timeout=30.0)
    response.raise_for_status()

    return _parse_arxiv_atom_response(response.text)


def _arxiv_package_search(
    query: str,
    max_results: int,
    categories: Optional[List[str]],
    sort_by: str,
) -> List[Dict[str, Any]]:
    """
    Perform arXiv search using the arxiv Python package.

    More robust parsing for non-date queries.
    """
    query_parts = []

    if query.strip():
        query_parts.append(f"({query})")

    if categories:
        category_filter = " OR ".join(f"cat:{cat}" for cat in categories)
        query_parts.append(f"({category_filter})")

    if not query_parts:
        raise ValueError("No search criteria provided")

    final_query = " ".join(query_parts)

    # Determine sort method
    sort_criterion = arxiv.SortCriterion.SubmittedDate if sort_by == "date" else arxiv.SortCriterion.Relevance

    search = arxiv.Search(
        query=final_query,
        max_results=max_results,
        sort_by=sort_criterion,
    )

    client = arxiv.Client()
    results = []

    for paper in client.results(search):
        if len(results) >= max_results:
            break
        results.append(_process_paper(paper))

    return results


def _parse_arxiv_atom_response(xml_text: str) -> List[Dict[str, Any]]:
    """Parse arXiv Atom XML response into paper dictionaries."""
    results = []

    try:
        root = ET.fromstring(xml_text)

        for entry in root.findall("atom:entry", ARXIV_NS):
            # Extract paper ID
            id_elem = entry.find("atom:id", ARXIV_NS)
            if id_elem is None or id_elem.text is None:
                continue

            paper_id = id_elem.text.split("/abs/")[-1]
            short_id = paper_id.split("v")[0] if "v" in paper_id else paper_id

            # Title
            title_elem = entry.find("atom:title", ARXIV_NS)
            title = title_elem.text.strip().replace("\n", " ") if title_elem is not None and title_elem.text else ""

            # Authors
            authors = []
            for author in entry.findall("atom:author", ARXIV_NS):
                name_elem = author.find("atom:name", ARXIV_NS)
                if name_elem is not None and name_elem.text:
                    authors.append(name_elem.text)

            # Abstract
            summary_elem = entry.find("atom:summary", ARXIV_NS)
            abstract = summary_elem.text.strip().replace("\n", " ") if summary_elem is not None and summary_elem.text else ""

            # Categories
            categories = []
            for cat in entry.findall("arxiv:primary_category", ARXIV_NS):
                term = cat.get("term")
                if term:
                    categories.append(term)
            for cat in entry.findall("atom:category", ARXIV_NS):
                term = cat.get("term")
                if term and term not in categories:
                    categories.append(term)

            # Published date
            published_elem = entry.find("atom:published", ARXIV_NS)
            published = published_elem.text if published_elem is not None and published_elem.text else ""

            # PDF URL
            pdf_url = None
            for link in entry.findall("atom:link", ARXIV_NS):
                if link.get("title") == "pdf":
                    pdf_url = link.get("href")
                    break
            if not pdf_url:
                pdf_url = f"http://arxiv.org/pdf/{paper_id}"

            results.append({
                "id": short_id,
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "categories": categories,
                "published": published,
                "url": pdf_url,
                "resource_uri": f"arxiv://{short_id}",
            })

    except ET.ParseError as e:
        raise ValueError(f"Failed to parse arXiv API response: {e}")

    return results


def _process_paper(paper: arxiv.Result) -> Dict[str, Any]:
    """Process paper from arxiv package Result object."""
    return {
        "id": paper.get_short_id(),
        "title": paper.title,
        "authors": [author.name for author in paper.authors],
        "abstract": paper.summary,
        "categories": paper.categories,
        "published": paper.published.isoformat(),
        "url": paper.pdf_url,
        "resource_uri": f"arxiv://{paper.get_short_id()}",
    }


def _validate_categories(categories: List[str]) -> bool:
    """Validate arXiv category prefixes."""
    for category in categories:
        prefix = category.split(".")[0] if "." in category else category
        if prefix not in VALID_CATEGORIES:
            return False
    return True


# =============================================================================
# Download Tools
# =============================================================================

def download_arxiv_paper(
    paper_id: str,
    output_dir: Optional[str] = None,
    convert_to_markdown: bool = True,
) -> Dict[str, Any]:
    """
    Download a paper from arXiv.

    Downloads the PDF and optionally converts it to Markdown using pymupdf4llm.

    Args:
        paper_id: arXiv ID (e.g., "2301.12345").
        output_dir: Directory to save paper (default: ~/.arxiv-papers).
        convert_to_markdown: Whether to convert PDF to Markdown (default: True).

    Returns:
        Dict with keys:
        - success: bool
        - paper_id: str
        - pdf_path: Path to PDF file (if downloaded)
        - markdown_path: Path to Markdown file (if converted)
        - error: Error message (if failed)

    Example:
        >>> result = download_arxiv_paper("2301.12345")
        >>> if result["success"]:
        ...     print(f"Downloaded to {result['pdf_path']}")
    """
    try:
        storage_path = Path(output_dir) if output_dir else DEFAULT_STORAGE_PATH
        storage_path.mkdir(parents=True, exist_ok=True)

        pdf_path = storage_path / f"{paper_id}.pdf"
        markdown_path = storage_path / f"{paper_id}.md"

        # Check if already downloaded
        if markdown_path.exists():
            return {
                "success": True,
                "paper_id": paper_id,
                "markdown_path": str(markdown_path),
                "message": "Paper already available",
            }

        if pdf_path.exists() and not convert_to_markdown:
            return {
                "success": True,
                "paper_id": paper_id,
                "pdf_path": str(pdf_path),
                "message": "PDF already downloaded",
            }

        # Download PDF
        client = arxiv.Client()
        paper = next(client.results(arxiv.Search(id_list=[paper_id])))
        paper.download_pdf(dirpath=str(pdf_path.parent), filename=pdf_path.name)

        result = {
            "success": True,
            "paper_id": paper_id,
            "pdf_path": str(pdf_path),
        }

        # Convert to Markdown if requested
        if convert_to_markdown:
            try:
                import pymupdf4llm
                markdown = pymupdf4llm.to_markdown(pdf_path, show_progress=False)
                with open(markdown_path, "w", encoding="utf-8") as f:
                    f.write(markdown)
                result["markdown_path"] = str(markdown_path)
                result["message"] = "Paper downloaded and converted to Markdown"
            except ImportError:
                result["message"] = "PDF downloaded. Install pymupdf4llm for Markdown conversion"
            except Exception as e:
                result["message"] = f"PDF downloaded but Markdown conversion failed: {e}"

        return result

    except StopIteration:
        return {
            "success": False,
            "paper_id": paper_id,
            "error": f"Paper not found on arXiv: {paper_id}",
        }
    except Exception as e:
        return {
            "success": False,
            "paper_id": paper_id,
            "error": f"Download failed: {e}",
        }


# =============================================================================
# List Tools
# =============================================================================

def list_downloaded_papers(output_dir: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all downloaded papers.

    Args:
        output_dir: Directory to search (default: ~/.arxiv-papers).

    Returns:
        List of paper dictionaries with:
        - id: arXiv ID
        - title: Paper title
        - authors: List of authors
        - abstract: Paper abstract
        - pdf_url: PDF URL
        - links: List of related links

    Example:
        >>> papers = list_downloaded_papers()
        >>> for paper in papers:
        ...     print(f"{paper['id']}: {paper['title']}")
    """
    storage_path = Path(output_dir) if output_dir else DEFAULT_STORAGE_PATH

    if not storage_path.exists():
        return []

    # Find all markdown files
    paper_ids = [p.stem for p in storage_path.glob("*.md")]

    if not paper_ids:
        return []

    # Fetch metadata from arXiv
    try:
        client = arxiv.Client()
        results = client.results(arxiv.Search(id_list=paper_ids))

        papers = []
        for result in results:
            papers.append({
                "id": result.get_short_id(),
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "abstract": result.summary,
                "links": [link.href for link in result.links],
                "pdf_url": result.pdf_url,
            })

        return papers

    except Exception:
        # Return basic info if arXiv API fails
        return [{"id": pid} for pid in paper_ids]


# =============================================================================
# Read Tools
# =============================================================================

def read_arxiv_paper(paper_id: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Read the full content of a downloaded paper.

    Reads the Markdown version if available, otherwise returns error.

    Args:
        paper_id: arXiv ID (e.g., "2301.12345").
        output_dir: Directory to search (default: ~/.arxiv-papers).

    Returns:
        Dict with keys:
        - success: bool
        - paper_id: str
        - content: Markdown content (if found)
        - error: Error message (if not found)

    Example:
        >>> result = read_arxiv_paper("2301.12345")
        >>> if result["success"]:
        ...     print(result["content"][:500])  # First 500 chars
    """
    storage_path = Path(output_dir) if output_dir else DEFAULT_STORAGE_PATH
    markdown_path = storage_path / f"{paper_id}.md"

    if not markdown_path.exists():
        return {
            "success": False,
            "paper_id": paper_id,
            "error": f"Paper not found. Download it first using download_arxiv_paper('{paper_id}')",
        }

    try:
        content = markdown_path.read_text(encoding="utf-8")
        return {
            "success": True,
            "paper_id": paper_id,
            "content": content,
        }
    except Exception as e:
        return {
            "success": False,
            "paper_id": paper_id,
            "error": f"Error reading paper: {e}",
        }


# =============================================================================
# Utility Functions
# =============================================================================

def get_arxiv_paper_metadata(paper_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch metadata for a specific arXiv paper.

    Args:
        paper_id: arXiv ID (e.g., "2301.12345").

    Returns:
        Paper metadata dict or None if not found.

    Example:
        >>> metadata = get_arxiv_paper_metadata("2301.12345")
        >>> if metadata:
        ...     print(f"Title: {metadata['title']}")
    """
    try:
        client = arxiv.Client()
        paper = next(client.results(arxiv.Search(id_list=[paper_id])))
        return _process_paper(paper)
    except StopIteration:
        return None
    except Exception:
        return None


def _fetch_crossref_metadata(doi: str) -> Optional[Dict[str, Any]]:
    """
    Fetch publication metadata from CrossRef via DOI content negotiation.
    
    Matches the official translator's DOI lookup behavior.
    
    Args:
        doi: DOI to lookup
    
    Returns:
        Dict with publication metadata or None if lookup failed
    """
    try:
        # Use CrossRef API with content negotiation
        headers = {"Accept": "application/vnd.citationstyles.csl+json"}
        response = httpx.get(f"https://doi.org/{doi}", headers=headers, timeout=10.0)
        if response.status_code != 200:
            return None
        
        cr_data = response.json()
        
        # Map CrossRef fields to Zotero fields
        result = {}
        
        # Item type mapping
        type_map = {
            "journal-article": "journalArticle",
            "book-chapter": "bookSection",
            "book": "book",
            "proceedings-article": "conferencePaper",
            "report": "report",
            "thesis": "thesis",
        }
        result["itemType"] = type_map.get(cr_data.get("type"), "journalArticle")
        
        # Basic fields
        if "title" in cr_data and cr_data["title"]:
            result["title"] = cr_data["title"][0]
        if "container-title" in cr_data and cr_data["container-title"]:
            result["publicationTitle"] = cr_data["container-title"][0]
        if "short-container-title" in cr_data and cr_data["short-container-title"]:
            result["journalAbbreviation"] = cr_data["short-container-title"][0]
        if "volume" in cr_data:
            result["volume"] = cr_data["volume"]
        if "issue" in cr_data:
            result["issue"] = cr_data["issue"]
        if "page" in cr_data:
            result["pages"] = cr_data["page"]
        if "ISSN" in cr_data and cr_data["ISSN"]:
            result["ISSN"] = cr_data["ISSN"][0] if isinstance(cr_data["ISSN"], list) else cr_data["ISSN"]
        
        # Date handling
        if "published" in cr_data and "date-parts" in cr_data["published"]:
            date_parts = cr_data["published"]["date-parts"][0]
            if len(date_parts) >= 1:
                result["date"] = str(date_parts[0])
                if len(date_parts) >= 2:
                    result["date"] += f"-{date_parts[1]:02d}"
                    if len(date_parts) >= 3:
                        result["date"] += f"-{date_parts[2]:02d}"
        
        # Authors
        if "author" in cr_data:
            creators = []
            for author in cr_data["author"]:
                creators.append({
                    "creatorType": "author",
                    "firstName": author.get("given", ""),
                    "lastName": author.get("family", ""),
                })
            result["creators"] = creators
        
        return result
    except Exception:
        return None


def import_arxiv_paper(zot, paper_id: str, collection_key: str = None, attach_pdf: bool = True) -> Optional[Dict[str, Any]]:
    """
    Import an arXiv paper into Zotero library via the Connector API.
    
    Uses the exact same endpoints as the Zotero Connector browser extension:
    - POST http://localhost:23119/connector/saveItems (for item metadata)
    - POST http://localhost:23119/connector/saveStandaloneAttachment (for PDF)
    
    Note: PDFs are saved as standalone attachments. To link to parent item,
    manually set the parent in Zotero or use the Web API instead.
    
    Args:
        zot: Zotero client (local API)
        paper_id: arXiv ID (e.g., "2301.12345")
        collection_key: Optional collection key
        attach_pdf: Whether to download and attach PDF (default: True)
    
    Returns:
        Dict with success status and item info
    """
    metadata = get_arxiv_paper_metadata(paper_id)
    if not metadata:
        return {"success": False, "error": f"Could not fetch metadata for arXiv:{paper_id}"}
    
    # Build item
    pdf_url = metadata["url"].replace("/abs/", "/pdf/") + ".pdf"
    item = {
        "itemType": "preprint",
        "title": metadata["title"],
        "abstractNote": metadata["abstract"],
        "date": metadata["published"][:10] if metadata["published"] else "",
        "url": metadata["url"],
        "DOI": f"10.48550/arXiv.{paper_id}",
        "archiveID": f"arXiv:{paper_id}",
        "publisher": "arXiv",
        "extra": f"arXiv: {paper_id}",
    }
    
    # Format categories as tags
    formatted_tags = []
    for cat in metadata["categories"]:
        if "." in cat and cat.split(".")[0] in ARXIV_CATEGORIES:
            main_cat = cat.split(".")[0]
            formatted_tags.append(f"{ARXIV_CATEGORIES[main_cat]} - {ARXIV_CATEGORIES.get(cat, cat)}")
        elif cat in ARXIV_CATEGORIES:
            formatted_tags.append(ARXIV_CATEGORIES[cat])
        else:
            formatted_tags.append(cat)
    item["tags"] = [{"tag": tag} for tag in formatted_tags]
    
    # Parse authors
    creators = []
    for author in metadata["authors"]:
        if "," in author:
            parts = author.split(",", 1)
            creators.append({
                "creatorType": "author",
                "firstName": parts[1].strip(),
                "lastName": parts[0].strip(),
            })
        else:
            parts = author.rsplit(" ", 1)
            if len(parts) == 2:
                creators.append({
                    "creatorType": "author",
                    "firstName": parts[0],
                    "lastName": parts[1],
                })
            else:
                creators.append({
                    "creatorType": "author",
                    "firstName": "",
                    "lastName": author,
                })
    item["creators"] = creators
    
    try:
        import secrets
        import time
        
        # Step 1: Save item metadata
        response = httpx.post(
            "http://localhost:23119/connector/saveItems",
            json={"items": [item]},
            headers={"Content-Type": "application/json"},
            timeout=10.0
        )
        
        if response.status_code != 201:
            return {"success": False, "error": f"Failed to save item: {response.status_code}"}
        
        # Get the created item key
        time.sleep(0.5)  # Give Zotero time to process
        from zotero_librarian import search_by_title
        results = search_by_title(zot, metadata["title"][:50])
        item_key = results[0]["key"] if results else None
        
        result = {
            "success": True,
            "item": item,
            "key": item_key,
            "pdf_attached": False,
            "message": f"Imported arXiv:{paper_id}",
        }
        
        # Step 2: Download and attach PDF if requested
        if attach_pdf and item_key:
            sessionID = secrets.token_hex(8)
            pdf_response = httpx.get(pdf_url, timeout=60.0)
            
            if pdf_response.status_code == 200:
                metadata_json = json.dumps({
                    "url": pdf_url,
                    "contentType": "application/pdf",
                    "title": "Fulltext PDF",
                    "parentItemID": item_key,
                })
                
                attach_response = httpx.post(
                    "http://localhost:23119/connector/saveStandaloneAttachment",
                    content=pdf_response.content,
                    headers={
                        "Content-Type": "application/pdf",
                        "X-Metadata": metadata_json,
                    },
                    params={"sessionID": sessionID},
                    timeout=60.0
                )
                
                if attach_response.status_code == 201:
                    result["pdf_attached"] = True
                    result["message"] = f"Imported arXiv:{paper_id} with PDF"
        
        return result
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def import_arxiv_papers(zot, paper_ids: List[str], collection_key: str = None) -> Dict[str, Any]:
    """
    Import multiple arXiv papers into Zotero library.
    
    Args:
        zot: Zotero client
        paper_ids: List of arXiv IDs
        collection_key: Optional collection key to add all items to
    
    Returns:
        Dict with results:
        - success: List of successfully imported paper IDs
        - failed: List of failed paper IDs with error messages
        - keys: Dict mapping paper_id → Zotero item key
    
    Example:
        >>> result = import_arxiv_papers(zot, ["2301.12345", "2302.67890"])
        >>> print(f"Imported {len(result['success'])} papers")
    """
    results = {
        "success": [],
        "failed": [],
        "keys": {},
    }
    
    for paper_id in paper_ids:
        result = import_arxiv_paper(zot, paper_id, collection_key)
        if result["success"]:
            results["success"].append(paper_id)
            results["keys"][paper_id] = result["key"]
        else:
            results["failed"].append({"paper_id": paper_id, "error": result["error"]})
    
    return results


# =============================================================================
# Export/Import (JSON)
# =============================================================================


def export_papers_to_json(papers: List[Dict[str, Any]], filepath: str) -> None:
    """
    Export paper metadata to JSON file.

    Args:
        papers: List of paper dictionaries (from search or list).
        filepath: Path to output JSON file.

    Example:
        >>> results = search_arxiv_papers("machine learning", max_results=20)
        >>> export_papers_to_json(results, "papers.json")
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)


def import_papers_from_json(filepath: str) -> List[Dict[str, Any]]:
    """
    Import paper metadata from JSON file.

    Args:
        filepath: Path to JSON file.

    Returns:
        List of paper dictionaries.

    Example:
        >>> papers = import_papers_from_json("papers.json")
        >>> for paper in papers:
        ...     download_arxiv_paper(paper["id"])
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
