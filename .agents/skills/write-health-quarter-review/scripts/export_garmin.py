#!/usr/bin/env python3
"""Export quarterly health-review metrics from the local Garmin databases in ~/HealthData/DBs.

Writes the `garmin_export.json` consumed by generate_health_assets.py. All reads are read-only.

Sources:
- garmin_summary.db  `days_summary`   daily metrics (RHR, stress, steps, body battery, intensity, active calories, weight)
- garmin.db          `sleep`          sleep score per day
- garmin_activities.db `activities` + `steps_activities`   VO2 max readings and activity counts
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import date, timedelta
from pathlib import Path

DB_DIR = Path.home() / "HealthData" / "DBs"


def quarter_bounds(year: int, quarter: int) -> tuple[date, date]:
    start = date(year, (quarter - 1) * 3 + 1, 1)
    next_start = date(year + (quarter == 4), 1 if quarter == 4 else quarter * 3 + 1, 1)
    return start, next_start - timedelta(days=1)


def ro(path: Path) -> sqlite3.Connection:
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--db-dir", type=Path, default=DB_DIR)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--quarter", type=int, required=True, choices=[1, 2, 3, 4])
    parser.add_argument("--query-start", default="2019-01-01")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    q_start, q_end = quarter_bounds(args.year, args.quarter)
    start = args.query_start
    end_excl = (q_end + timedelta(days=1)).isoformat()

    summary = ro(args.db_dir / "garmin_summary.db")
    rows = summary.execute(
        "select substr(day,1,10), hr_min, hr_max, rhr_min, bb_max, bb_min, steps, floors, moderate_activity_time, "
        "vigorous_activity_time, calories_active_avg, stress_avg, weight_avg from days_summary "
        "where day >= ? and day < ? order by day",
        (start, end_excl),
    ).fetchall()
    latest_day = summary.execute("select substr(max(day),1,10) from days_summary").fetchone()[0]
    summary.close()

    garmin = ro(args.db_dir / "garmin.db")
    scores = dict(
        garmin.execute(
            "select substr(day,1,10), score from sleep where score is not null and day >= ? and day < ?",
            (start, end_excl),
        )
    )
    garmin.close()

    activities = ro(args.db_dir / "garmin_activities.db")
    vo2 = [
        {"date": day, "vo2_max": value}
        for day, value in activities.execute(
            "select substr(a.start_time,1,10), s.vo2_max from activities a join steps_activities s on s.activity_id = a.activity_id "
            "where a.start_time >= ? and a.start_time < ? and s.vo2_max is not null order by a.start_time",
            (start, end_excl),
        )
    ]
    by_type = {
        sport: {"count": count, "distance_km": round(distance or 0, 1), "hours": round((moving or 0) / 3600.0, 1)}
        for sport, count, distance, moving in activities.execute(
            "select coalesce(sport,'unknown'), count(*), sum(distance), sum(moving_time) from ("
            "select sport, distance, strftime('%s', moving_time) - strftime('%s','00:00:00') as moving_time from activities "
            "where start_time >= ? and start_time < ?) group by 1 order by 2 desc",
            (q_start.isoformat(), end_excl),
        )
    }
    activity_count = activities.execute(
        "select count(*) from activities where start_time >= ? and start_time < ?", (q_start.isoformat(), end_excl)
    ).fetchone()[0]
    activities.close()

    daily = [
        {
            "date": day,
            "hr_min": hr_min,
            "hr_max": hr_max,
            "rhr_min": rhr,
            "bb_max": bb_max,
            "bb_min": bb_min,
            "sleep_avg": scores.get(day),
            "steps": steps,
            "floors": floors,
            "moderate_activity_time": moderate,
            "vigorous_activity_time": vigorous,
            "intensity_minutes": None,  # renderer derives moderate + 2 x vigorous
            "calories_active_avg": calories,
            "stress_avg": stress,
            "weight_avg": weight,
        }
        for day, hr_min, hr_max, rhr, bb_max, bb_min, steps, floors, moderate, vigorous, calories, stress, weight in rows
    ]

    payload = {
        "metadata": {
            "year": args.year,
            "quarter": args.quarter,
            "quarter_label": f"Q{args.quarter} {args.year}",
            "query_start_date": start,
            "quarter_start_date": q_start.isoformat(),
            "quarter_end_date": q_end.isoformat(),
            "source": "local Garmin data (~/HealthData/DBs)",
            "freshness": {"latest_day": latest_day},
            "quarter_activity_count": activity_count,
            "quarter_activities_by_sport": by_type,
        },
        "daily_metrics": daily,
        "vo2_max": vo2,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=1))
    covered = {k: sum(1 for row in daily if row[k] is not None) for k in daily[0] if k != "date"}
    print(f"wrote {args.output} ({len(daily)} days, {len(vo2)} VO2 readings, {activity_count} quarter activities)")
    print("non-null days per metric:", covered)
    print("latest day in database:", latest_day)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
