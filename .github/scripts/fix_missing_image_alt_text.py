#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


EMPTY_IMAGE_RE = re.compile(r"!\[\]\(([^)]+)\)")
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.S)

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


def should_treat_as_generic(stem: str, humanized: str) -> bool:
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


def get_page_title(markdown: str, fallback: str) -> str:
    match = FRONT_MATTER_RE.match(markdown)
    if not match:
        return fallback

    front_matter = match.group(1)
    title_match = re.search(r"^title:\s*['\"]?(.*?)['\"]?$", front_matter, re.M)
    if title_match:
        return title_match.group(1).strip()
    return fallback


def replacement_for_image(src: str, title: str, index: int) -> str:
    src_path = src.split("?", 1)[0].split("#", 1)[0]
    stem = Path(src_path).stem
    humanized = humanize_stem(stem)

    if not humanized or humanized.isdigit() or should_treat_as_generic(stem, humanized):
        return f"{title} image {index}"

    return humanized[0].upper() + humanized[1:]


def update_markdown(path: Path) -> int:
    original = path.read_text(encoding="utf-8")
    title = get_page_title(original, path.parent.name.replace("-", " ").title())
    counter = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        alt = replacement_for_image(match.group(1), title, counter)
        return f"![{alt}]({match.group(1)})"

    updated = EMPTY_IMAGE_RE.sub(replace, original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return counter

    return 0


def main() -> int:
    total_updates = 0
    updated_files = 0

    for path in sorted(Path("content/posts").rglob("index.md")):
        updates = update_markdown(path)
        if updates:
            updated_files += 1
            total_updates += updates

    print(f"Updated {total_updates} image alt text entries across {updated_files} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
