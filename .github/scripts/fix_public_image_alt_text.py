#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


IMG_TAG_RE = re.compile(r"<img(?P<attrs>[^>]*?)>", re.IGNORECASE)
TITLE_RE = re.compile(r"<title>(?P<title>.*?)\s*\|\s*[^<]+</title>", re.IGNORECASE | re.DOTALL)
SRC_RE = re.compile(r"""src=(?:"(?P<dq>[^"]*)"|'(?P<sq>[^']*)'|(?P<bare>[^ >]+))""", re.IGNORECASE)

GENERIC_PREFIXES = (
    "img",
    "dsc",
    "dscf",
    "pano",
    "pasted image",
    "screenshot",
    "screen shot",
)


def humanize_stem(stem: str) -> str:
    text = stem.replace("_", " ").replace("-", " ")
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def generic_stem(stem: str, humanized: str) -> bool:
    lowered = stem.lower()
    if lowered.startswith(GENERIC_PREFIXES):
        return True
    if re.fullmatch(r"(?:img|dsc|dscf|pano|screenshot|pasted image)[\s_-]*\d+[a-z0-9\s_-]*", lowered):
        return True
    if len(humanized.split()) == 2:
        left, right = humanized.split()
        if left.lower() in {"img", "dsc", "dscf", "pano"} and right.isdigit():
            return True
    return False


def alt_text_for(src: str, page_title: str, index: int) -> str:
    src_path = src.split("?", 1)[0].split("#", 1)[0]
    stem = Path(src_path).stem
    humanized = humanize_stem(stem)
    if not humanized or humanized.isdigit() or generic_stem(stem, humanized):
        return f"{page_title} image {index}"
    return humanized[0].upper() + humanized[1:]


def patch_html(path: Path) -> int:
    original = path.read_text(encoding="utf-8")
    title_match = TITLE_RE.search(original)
    page_title = title_match.group("title").strip() if title_match else path.stem
    image_index = 0
    changed = False

    def replace(match: re.Match[str]) -> str:
        nonlocal image_index, changed
        attrs = match.group("attrs")
        if "alt=" in attrs.lower():
            return match.group(0)

        src_match = SRC_RE.search(attrs)
        if not src_match:
            return match.group(0)

        src = src_match.group("dq") or src_match.group("sq") or src_match.group("bare") or ""
        image_index += 1
        alt = alt_text_for(src, page_title, image_index)
        changed = True
        return f'<img alt="{alt}"{attrs}>'

    updated = IMG_TAG_RE.sub(replace, original)
    if changed:
        path.write_text(updated, encoding="utf-8")
        return 1
    return 0


def main() -> int:
    updated_files = 0
    for html_file in Path("public").rglob("*.html"):
        updated_files += patch_html(html_file)
    print(f"Updated image alt text in {updated_files} HTML files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
