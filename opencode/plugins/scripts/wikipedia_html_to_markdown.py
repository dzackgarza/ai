import re
import sys
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from markdownify import markdownify as to_markdown


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: wikipedia_html_to_markdown.py <html_path> <source_url> <page_title>", file=sys.stderr)
        return 2

    html_path = sys.argv[1]
    source_url = sys.argv[2]
    page_title = sys.argv[3]

    with open(html_path, "r", encoding="utf-8") as fh:
        html = fh.read()

    soup = BeautifulSoup(html, "html.parser")

    for selector in [
        "style",
        "script",
        "noscript",
        "meta",
        "link",
        ".mw-editsection",
        ".reference",
        ".mw-cite-backlink",
        ".shortdescription",
        ".hatnote",
        ".navbox",
        ".reflist",
        ".metadata",
        ".mw-authority-control",
    ]:
        for node in soup.select(selector):
            node.decompose()

    for annotation in soup.select("annotation[encoding='application/x-tex']"):
        tex = annotation.get_text(" ", strip=True)
        if not tex:
            continue
        math_parent = annotation.find_parent("math")
        replacement = soup.new_string(f"${tex}$")
        if math_parent is not None:
            math_parent.replace_with(replacement)
        else:
            annotation.replace_with(replacement)

    for img in soup.select("img.mwe-math-fallback-image-inline, img.mwe-math-fallback-image-display"):
        alt = (img.get("alt") or "").strip()
        img.replace_with(soup.new_string(f"${alt}$" if alt else ""))

    parsed = urlparse(source_url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    for anchor in soup.find_all("a"):
        href = anchor.get("href")
        if not href:
            continue
        if href.startswith("//"):
            anchor["href"] = f"https:{href}"
            continue
        if href.startswith("/"):
            anchor["href"] = f"{base}{href}"

    markdown = to_markdown(str(soup), heading_style="ATX")
    markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip()

    print(source_url)
    print("")
    print(f"# {page_title}")
    print("")
    print(markdown if markdown else "[no content extracted]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
