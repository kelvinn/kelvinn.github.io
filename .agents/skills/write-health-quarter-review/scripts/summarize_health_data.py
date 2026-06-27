#!/usr/bin/env python3
"""Summarize generated quarterly health-review CSVs."""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date, timedelta
from pathlib import Path
from statistics import mean, median


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def quarter_bounds_from_post_dir(post_dir: Path) -> tuple[date, date] | None:
    match = re.search(r"(\d{4})-q([1-4])-health-review", post_dir.name)
    if not match:
        return None
    year = int(match.group(1))
    quarter = int(match.group(2))
    start_month = ((quarter - 1) * 3) + 1
    start = date(year, start_month, 1)
    if quarter == 4:
        next_start = date(year + 1, 1, 1)
    else:
        next_start = date(year, start_month + 3, 1)
    return start, next_start - timedelta(days=1)


def summarize_weekly_intensity(data_dir: Path, quarter_bounds: tuple[date, date] | None) -> dict[str, object]:
    rows = read_csv(data_dir / "weekly_intensity_minutes_per_week.csv")
    if quarter_bounds:
        start, end = quarter_bounds
        rows = [
            row
            for row in rows
            if row.get("week_end") and start <= date.fromisoformat(row["week_end"]) <= end
        ]
    values = [as_float(row.get("intensity_minutes")) for row in rows]
    values = [value for value in values if value is not None]
    if not values:
        return {"weeks": 0}
    return {
        "weeks": len(values),
        "mean": round(mean(values), 1),
        "median": round(median(values), 1),
        "weeks_at_or_above_800": sum(1 for value in values if value >= 800),
        "max": round(max(values), 1),
        "min": round(min(values), 1),
    }


def summarize_quarterly_metrics(data_dir: Path) -> list[dict[str, str]]:
    return read_csv(data_dir / "quarterly_metrics_raw.csv")


def summarize_correlation_matrix(data_dir: Path, limit: int = 8) -> list[dict[str, object]]:
    rows = read_csv(data_dir / "correlation_matrix.csv")
    if not rows:
        return []
    metrics = [key for key in rows[0].keys() if key]
    values: list[dict[str, object]] = []
    for row in rows:
        metric_a = row.get("", "")
        for metric_b in metrics:
            if metric_a >= metric_b:
                continue
            corr = as_float(row.get(metric_b))
            if corr is None:
                continue
            values.append({"a": metric_a, "b": metric_b, "correlation": round(corr, 3), "abs": abs(corr)})
    return sorted(values, key=lambda item: item["abs"], reverse=True)[:limit]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("post_dir", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    data_dir = args.post_dir / "data"
    summary = {
        "post_dir": str(args.post_dir),
        "data_dir_exists": data_dir.exists(),
        "quarterly_metrics": summarize_quarterly_metrics(data_dir),
        "weekly_intensity": summarize_weekly_intensity(data_dir, quarter_bounds_from_post_dir(args.post_dir)),
        "top_correlations": summarize_correlation_matrix(data_dir),
    }

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Post: {summary['post_dir']}")
        print(f"Data folder exists: {summary['data_dir_exists']}")
        print(f"Weekly intensity: {summary['weekly_intensity']}")
        print("Quarterly metrics:")
        for row in summary["quarterly_metrics"]:
            print(f"  {row}")
        print("Top correlations:")
        for row in summary["top_correlations"]:
            print(f"  {row['a']} vs {row['b']}: {row['correlation']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
