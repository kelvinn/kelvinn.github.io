#!/usr/bin/env python3
"""Validate a quarterly health review post folder."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_SECTIONS = [
    "### Reflection",
    "### Focus Areas",
    "#### Improve Fitness",
    "#### Improve Sleep",
    "#### Decrease Stress",
    "#### Improve Biomarkers",
    "#### Improve Nutrition",
    "### Supplement Stack",
    "### Focus For Next Quarter",
]

REQUIRED_IMAGES = [
    "summary.png",
    "correlation_matrix.png",
    "weekly_intensity_minutes.png",
    "sleep_score_per_day.png",
    "stress_level_per_day.png",
    "stress_level_per_week.png",
    "average_resting_hr_per_month.png",
    "average_sleep_score_per_month.png",
    "average_active_calories_per_month.png",
]

EXPECTED_CSVS = [
    "quarterly_metrics_raw.csv",
    "weekly_intensity_minutes_per_week.csv",
    "average_sleep_score_per_month.csv",
    "average_resting_hr_per_month.csv",
    "correlation_matrix.csv",
    "stress_quarterly_per_quarter.csv",
    "sleep_score_per_day_per_quarter.csv",
    "summary_quartet_per_month.csv",
]

PLACEHOLDER_PATTERNS = [
    r"\[(?:Biomarker|Supplement|Prior result|Latest result|Direction|In range|Out of range)[^\]]*\]",
    r"Which ",
    r"What ",
    r"How did ",
    r"Biomarker 1",
    r"Supplement \+ dose",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("post_dir", type=Path)
    args = parser.parse_args()

    post_dir = args.post_dir
    index_path = post_dir / "index.md"
    errors: list[str] = []
    warnings: list[str] = []

    if not index_path.exists():
        raise SystemExit(f"Missing index.md in {post_dir}")

    text = index_path.read_text()

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"Missing section: {section}")

    for image in REQUIRED_IMAGES:
        if not (post_dir / image).exists():
            errors.append(f"Missing image: {image}")

    data_dir = post_dir / "data"
    if not data_dir.exists():
        errors.append("Missing data/ folder")
    else:
        for csv_name in EXPECTED_CSVS:
            if not (data_dir / csv_name).exists():
                warnings.append(f"Missing expected CSV: {csv_name}")

    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, text):
            warnings.append(f"Possible template placeholder remains: {pattern}")

    for image_ref in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text):
        if image_ref.startswith(("http://", "https://")):
            continue
        local_ref = image_ref.replace("%20", " ")
        if not (post_dir / local_ref).exists():
            warnings.append(f"Referenced image does not exist: {image_ref}")

    for item in warnings:
        print(f"WARN: {item}")
    for item in errors:
        print(f"ERROR: {item}")

    if errors:
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
