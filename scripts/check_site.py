"""Check generated local file links and anchors before publication."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])


def check(root):
    root = Path(root).resolve()
    pages = {}
    for path in root.rglob("*.html"):
        page = Page(path)
        page.feed(path.read_text())
        pages[path] = page
    if not pages or root / "index.html" not in pages:
        raise ValueError("Generated site has no homepage.")
    errors = []
    for page in pages.values():
        for link in page.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            path = unquote(parsed.path)
            target = root / path.lstrip("/") if path.startswith("/") else page.path.parent / path
            if not path:
                target = page.path
            target = target.resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.is_relative_to(root) or not target.exists():
                errors.append(f"{page.path.relative_to(root)}: missing local link {link}")
            elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                errors.append(f"{page.path.relative_to(root)}: missing anchor {link}")
    if errors:
        raise ValueError("\n".join(errors))
    print(f"PASS: file links and anchors in {len(pages)} generated pages.")


if __name__ == "__main__":
    check(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "_site")
