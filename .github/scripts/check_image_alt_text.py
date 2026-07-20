#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> int:
    public_dir = Path("public")
    missing_alt: list[str] = []

    for html_file in public_dir.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        img_tags = re.findall(r"<img([^>]*)>", content, re.IGNORECASE)

        for img in img_tags:
            if 'class="image' in img or "figure" in img:
                continue

            if "alt=" not in img.lower():
                missing_alt.append(f"{html_file.relative_to(public_dir)}: {img[:100]}")

    if missing_alt:
        print("Images missing alt text:")
        for img in missing_alt[:20]:
            print(f"  - {img}")
        if len(missing_alt) > 20:
            print(f"  ... and {len(missing_alt) - 20} more")
        return 1

    print("All images have alt text")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
