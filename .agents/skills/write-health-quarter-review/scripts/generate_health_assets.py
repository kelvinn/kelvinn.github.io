#!/usr/bin/env python3
"""Generate quarterly health assets using the current notebooks pipeline."""

from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
from datetime import date, timedelta
from pathlib import Path


def repo_root_from(path: Path) -> Path:
    for candidate in [path.resolve(), *path.resolve().parents]:
        if (candidate / "notebooks" / "go.sh").exists():
            return candidate
    raise SystemExit("Could not find repo root containing notebooks/go.sh.")


def quarter_bounds(year: int, quarter: int) -> tuple[date, date]:
    start_month = ((quarter - 1) * 3) + 1
    start = date(year, start_month, 1)
    if quarter == 4:
        next_start = date(year + 1, 1, 1)
    else:
        next_start = date(year, start_month + 3, 1)
    return start, next_start - timedelta(days=1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--quarter", type=int, choices=(1, 2, 3, 4), required=True)
    parser.add_argument("--query-start-date", default="2019-01-01")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    root = repo_root_from(args.repo_root)
    start, end = quarter_bounds(args.year, args.quarter)
    output_dir = root / "content" / "posts" / f"{args.year}-q{args.quarter}-health-review"
    output_dir.mkdir(parents=True, exist_ok=True)

    config = "\n".join(
        [
            f"REPORT_QUERY_START_DATE={args.query_start_date}",
            f"REPORT_QUARTER_START_DATE={start.isoformat()}",
            f"REPORT_QUARTER_END_DATE={end.isoformat()}",
            f"REPORT_POST_OUTPUT_DIR={output_dir}",
            "",
        ]
    )

    with tempfile.NamedTemporaryFile("w", suffix=".env", delete=False) as handle:
        handle.write(config)
        config_path = handle.name

    env = os.environ.copy()
    env["REPORT_CONFIG_FILE"] = config_path
    try:
        subprocess.run(["bash", "go.sh"], cwd=root / "notebooks", env=env, check=True)
    finally:
        Path(config_path).unlink(missing_ok=True)

    print(output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
