"""Rendered-site smoke tests for shared UI regressions."""

from __future__ import annotations

import subprocess
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TagCounter(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.description_values: list[str] = []
        self.generic_heading_links = 0
        self.link_stack: list[list[str]] = []
        self.link_texts: list[str] = []
        self.h1_count = 0
        self.skip_links = 0
        self.sidebars = 0
        self.post_navs = 0
        self.post_tags = 0
        self.tables = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        classes = set((attr.get("class") or "").split())
        if tag == "a":
            self.link_stack.append([])
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta" and attr.get("name") == "description":
            self.description_values.append(attr.get("content") or "")
        if tag == "a" and "skip-link" in classes and attr.get("href") == "#main-content":
            self.skip_links += 1
        if tag == "a" and "anchor" in classes and attr.get("aria-label") == "Link to this heading":
            self.generic_heading_links += 1
        if tag == "aside" and "sidebar" in classes and attr.get("aria-label") == "Related site sections":
            self.sidebars += 1
        if tag == "nav" and "paginav" in classes:
            self.post_navs += 1
        if tag == "ul" and "post-tags" in classes:
            self.post_tags += 1
        if tag == "table":
            self.tables += 1

    def handle_data(self, data: str) -> None:
        if self.link_stack:
            self.link_stack[-1].append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.link_stack:
            text = " ".join("".join(self.link_stack.pop()).split())
            self.link_texts.append(text)


def parse_html(path: Path) -> TagCounter:
    parser = TagCounter()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def test_rendered_site_shared_ui_smoke() -> None:
    result = subprocess.run(
        ["hugo", "--minify"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    assert "WARN" not in output

    home_html = (ROOT / "public/index.html").read_text(encoding="utf-8")
    home_parsed = parse_html(ROOT / "public/index.html")
    assert home_parsed.description_values
    assert all(value.strip() for value in home_parsed.description_values)
    assert "Read more" not in home_parsed.link_texts
    assert "<meta name=author content>" not in home_html
    assert "rel=preload as=style" in home_html
    assert "this.rel=\"stylesheet\"" in home_html
    assert "https://www.googletagmanager.com/gtag/js?id=G-81J08BMTJ0" in home_html
    assert "<script async src=\"https://www.googletagmanager.com/gtag/js" not in home_html
    assert "localStorage.getItem(\"pref-theme\")" not in home_html
    assert "id=top-link" not in home_html
    assert "kelvinism.css" not in home_html
    assert "post-summary" in home_html
    assert "entry-tags" not in home_html

    article = ROOT / "public/2026/06/2026-q2-health-review.html"
    parsed = parse_html(article)
    assert parsed.description_values
    assert all(value.strip() for value in parsed.description_values)
    assert parsed.generic_heading_links == 0
    assert parsed.skip_links == 1
    assert parsed.h1_count == 0
    assert parsed.sidebars == 1
    assert parsed.post_navs == 0
    assert parsed.post_tags == 0
    assert parsed.tables >= 1

    css_files = sorted(
        (ROOT / "public/assets/css").glob("stylesheet.*.css"),
        key=lambda path: path.stat().st_mtime,
    )
    assert css_files, "expected Hugo to generate a bundled stylesheet"
    css = css_files[-1].read_text(encoding="utf-8")
    assert ".skip-link" in css
    assert ".sidebar" in css
    assert "overflow-x:auto" in css
