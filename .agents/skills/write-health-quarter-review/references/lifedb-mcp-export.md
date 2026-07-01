# LifeDB MCP Export

Connect to the `lifedb` MCP server at `https://lifedb.fly.dev/mcp`.
Use only LifeDB MCP for Garmin data. Do not read GarminDB SQLite files, `~/HealthData/DBs`, or repo-local `.db` files for health-review Garmin metrics.

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
      "vo2_max_generic": 51.0,
      "vo2_max_cycling": null
    }
  ]
}
```

Use displayed `null` for unavailable metrics. `calories_active_avg` and `weight_avg` may be null when LifeDB does not expose equivalent daily data.

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

Use this SQL as the default, adjusting only when table schemas differ:

```sql
with recursive dates(day) as (
  select date(:query_start)
  union all
  select date(day, '+1 day') from dates where day < date(:query_end_exclusive, '-1 day')
),
sleep_daily as (
  select
    calendar_date as day,
    avg(score_overall_value) as sleep_avg,
    min(resting_heart_rate) as rhr_min
  from sleep
  where calendar_date >= :query_start
    and calendar_date < :query_end_exclusive
  group by calendar_date
),
stress_daily as (
  select date(timestamp) as day, avg(value) as stress_avg
  from stress
  where timestamp >= :query_start
    and timestamp < :query_end_exclusive
    and value >= 0
  group by date(timestamp)
),
body_battery_daily as (
  select date(timestamp) as day, max(value) as bb_max, min(value) as bb_min
  from body_battery
  where timestamp >= :query_start
    and timestamp < :query_end_exclusive
  group by date(timestamp)
),
steps_daily as (
  select date(timestamp) as day, sum(value) as steps
  from steps
  where timestamp >= :query_start
    and timestamp < :query_end_exclusive
  group by date(timestamp)
),
heart_rate_daily as (
  select date(timestamp) as day, min(value) as hr_min, max(value) as hr_max
  from heart_rate
  where timestamp >= :query_start
    and timestamp < :query_end_exclusive
    and value > 0
  group by date(timestamp)
),
floors_daily as (
  select date(timestamp) as day, sum(ascended) as floors
  from floors
  where timestamp >= :query_start
    and timestamp < :query_end_exclusive
  group by date(timestamp)
),
training_daily as (
  select
    date as day,
    sum(moderate_minutes) as moderate_activity_time,
    sum(vigorous_minutes) as vigorous_activity_time,
    sum(total_intensity_minutes) as intensity_minutes
  from training_load
  where date >= :query_start
    and date < :query_end_exclusive
  group by date
)
select
  d.day as date,
  hr.hr_min,
  hr.hr_max,
  s.rhr_min,
  bb.bb_max,
  bb.bb_min,
  sl.sleep_avg,
  st.steps,
  fl.floors,
  tr.moderate_activity_time,
  tr.vigorous_activity_time,
  tr.intensity_minutes,
  null as calories_active_avg,
  stress.stress_avg,
  null as weight_avg
from dates d
left join heart_rate_daily hr on hr.day = d.day
left join sleep_daily s on s.day = d.day
left join sleep_daily sl on sl.day = d.day
left join body_battery_daily bb on bb.day = d.day
left join steps_daily st on st.day = d.day
left join floors_daily fl on fl.day = d.day
left join training_daily tr on tr.day = d.day
left join stress_daily stress on stress.day = d.day
order by d.day;
```

## VO2 Max Query

```sql
select
  date,
  vo2_max_generic,
  vo2_max_cycling
from vo2_max
where date >= :query_start
  and date < :query_end_exclusive
order by date;
```
