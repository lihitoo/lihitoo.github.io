"""Validate local navigation and assets before publishing; standard library only."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.urls = []
        self.headings = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f"Duplicate ID: {attrs['id']}"
            self.ids.add(attrs["id"])
        self.headings += tag == "h1"
        for key in ("href", "src"):
            if key in attrs:
                self.urls.append(attrs[key])
        if tag == "img":
            assert "alt" in attrs, "Image is missing alt text"


def main():
    page = Page()
    page.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    assert page.headings == 1, "Expected one main heading"
    for base in ("https://example.github.io/", "https://example.github.io/REPOSITORY/"):
        for url in page.urls:
            parsed = urlsplit(url)
            assert url and not parsed.scheme and not parsed.netloc, f"Review external/empty URL: {url}"
            resolved = urlsplit(urljoin(base, url))
            prefix = urlsplit(base).path
            assert resolved.path.startswith(prefix), f"URL escapes deployment path: {url}"
            if parsed.path:
                asset = ROOT / unquote(resolved.path[len(prefix):])
                assert asset.is_file(), f"Missing asset: {asset}"
            if parsed.fragment:
                assert parsed.fragment in page.ids, f"Missing anchor: {url}"
    assert (ROOT / ".nojekyll").is_file(), "Missing .nojekyll"
    print(f"PASS: {len(page.urls)} URLs, image alt text, unique IDs and main heading; root and /REPOSITORY/ deployments.")


if __name__ == "__main__":
    main()
