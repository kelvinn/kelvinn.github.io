"""Rendered-site smoke tests for shared UI regressions."""

from __future__ import annotations

import subprocess
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TagCounter(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1_count = 0
        self.skip_links = 0
        self.mobile_related = 0
        self.post_navs = 0
        self.post_tags = 0
        self.tables = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        classes = set((attr.get("class") or "").split())
        if tag == "h1":
            self.h1_count += 1
        if tag == "a" and "skip-link" in classes and attr.get("href") == "#main-content":
            self.skip_links += 1
        if tag == "section" and "mobile-related" in classes:
            self.mobile_related += 1
        if tag == "nav" and "paginav" in classes:
            self.post_navs += 1
        if tag == "ul" and "post-tags" in classes:
            self.post_tags += 1
        if tag == "table":
            self.tables += 1


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
    assert "kelvinism.css" not in home_html
    assert "post-summary" in home_html
    assert "entry-tags" not in home_html

    article = ROOT / "public/2026/06/2026-q2-health-review.html"
    parsed = parse_html(article)
    assert parsed.skip_links == 1
    assert parsed.h1_count == 0
    assert parsed.mobile_related == 1
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
    assert ".mobile-related" in css
    assert "overflow-x:auto" in css
