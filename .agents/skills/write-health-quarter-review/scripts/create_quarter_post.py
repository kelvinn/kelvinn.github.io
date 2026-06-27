#!/usr/bin/env python3
"""Create a quarterly health review post from the repo template."""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


QUARTER_MONTHS = {
    1: (1, 3),
    2: (4, 6),
    3: (7, 9),
    4: (10, 12),
}


def repo_root_from(path: Path) -> Path:
    for candidate in [path.resolve(), *path.resolve().parents]:
        if (candidate / "content" / "posts").exists():
            return candidate
    raise SystemExit("Could not find repo root containing content/posts.")


def quarter_end_day(year: int, quarter: int) -> int:
    return {1: 31, 2: 30, 3: 30, 4: 31}[quarter]


def update_frontmatter(markdown: str, year: int, quarter: int) -> str:
    _, end_month = QUARTER_MONTHS[quarter]
    slug = f"{year}-q{quarter}-health-review"
    title = f"{year} Q{quarter} Health Review"
    tz = ZoneInfo("Australia/Sydney")
    date_value = datetime(year, end_month, quarter_end_day(year, quarter), 21, 30, tzinfo=tz).isoformat()
    url = f"/{year}/{end_month:02d}/{slug}.html"

    replacements = {
        "title": title,
        "date": date_value,
        "draft": "true",
        "url": url,
    }

    def replace_field(match: re.Match[str]) -> str:
        key = match.group(1)
        return f"{key}: {replacements[key]}"

    pattern = re.compile(r"^(title|date|draft|url): .*$", re.MULTILINE)
    return pattern.sub(replace_field, markdown)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--quarter", type=int, choices=(1, 2, 3, 4), required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--force", action="store_true", help="overwrite an existing target folder")
    args = parser.parse_args()

    root = repo_root_from(args.repo_root)
    template = root / "content" / "posts" / "20NN-qN-health-review-TEMPLATE"
    slug = f"{args.year}-q{args.quarter}-health-review"
    target = root / "content" / "posts" / slug

    if not template.exists():
        raise SystemExit(f"Missing template folder: {template}")
    if target.exists():
        if not args.force:
            raise SystemExit(f"Target already exists: {target}")
        shutil.rmtree(target)

    shutil.copytree(template, target)
    index_path = target / "index.md"
    index_path.write_text(update_frontmatter(index_path.read_text(), args.year, args.quarter))
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
