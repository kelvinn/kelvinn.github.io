# LifeDB MCP Export

Use the LifeDB plugin [@dev-6a3eed984df88191900b4e84b06efa19](plugin://dev-6a3eed984df88191900b4e84b06efa19@created-by-me-remote) for Garmin data.
Do not read GarminDB SQLite files, `~/HealthData/DBs`, or repo-local `.db` files for health-review Garmin metrics.

The local renderer consumes an export JSON because scripts cannot call MCP tools directly. The agent must create this JSON from MCP query results, then run:

```bash
python .agents/skills/write-health-quarter-review/scripts/generate_health_assets.py \
  --input-json content/posts/YYYY-qN-health-review/data/lifedb_export.json \
  --post-dir content/posts/YYYY-qN-health-review
```

## Export Shape

```json
{
  "metadata": {
    "year": 2026,
    "quarter": 2,
    "quarter_label": "Q2 2026",
    "query_start_date": "2019-01-01",
    "quarter_start_date": "2026-04-01",
    "quarter_end_date": "2026-06-30",
    "freshness": {}
  },
  "daily_metrics": [
    {
      "date": "2026-04-01",
      "hr_min": 48,
      "hr_max": 156,
      "rhr_min": 54,
      "bb_max": 89,
      "bb_min": 22,
      "sleep_avg": 81,
      "steps": 10000,
      "floors": 4,
      "moderate_activity_time": 20,
      "vigorous_activity_time": 40,
      "intensity_minutes": 100,
      "calories_active_avg": null,
      "stress_avg": 26,
      "weight_avg": null
    }
  ],
  "vo2_max": [
    {
      "date": "2026-04-01",
      "vo2_max": 51.0
    }
  ]
}
```

Use displayed `null` for unavailable metrics. `calories_active_avg` and `weight_avg` may be null when LifeDB does not expose equivalent daily data.
LifeDB `TIME` fields such as `moderate_activity_time`, `vigorous_activity_time`, and `intensity_time` are usually returned as `HH:MM:SS` strings; renderers must parse them into minutes before summing or plotting.

## MCP Workflow

1. Call `get_sync_status`.
2. Call `get_data_freshness`.
3. Call `list_tables`.
4. Call `describe_table` for any table not already described in the current thread.
5. Run read-only `WITH` / `SELECT` queries with `execute_read_query`.
6. Save rows into `data/lifedb_export.json`.
7. Render assets from that JSON.

If freshness ends before `quarter_end_date`, still render available data, but mention the latest available date in the post and keep the quarter provisional.

## Daily Metrics Query

Set:

- `:query_start` to `REPORT_QUERY_START_DATE`
- `:query_end_exclusive` to the day after quarter end

Use this SQL as the default for the current LifeDB MCP schema, adjusting only when table schemas differ:

```sql
select
  date(ds.day) as date,
  ds.hr_min,
  ds.hr_max,
  ds.rhr as rhr_min,
  ds.bb_max,
  ds.bb_min,
  s.score as sleep_avg,
  ds.steps,
  ds.floors_up as floors,
  ds.moderate_activity_time,
  ds.vigorous_activity_time,
  null as intensity_minutes,
  ds.calories_active as calories_active_avg,
  ds.stress_avg,
  w.weight as weight_avg
from daily_summary ds
left join sleep s on date(s.day) = date(ds.day)
left join weight w on date(w.day) = date(ds.day)
where ds.day >= :query_start
  and ds.day < :query_end_exclusive
order by ds.day;
```

## VO2 Max Query

```sql
select
  date(a.start_time) as date,
  s.vo2_max
from activities a
join steps_activities s on s.activity_id = a.activity_id
where a.start_time >= :query_start
  and a.start_time < :query_end_exclusive
  and s.vo2_max is not null
order by a.start_time;
```
