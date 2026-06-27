# Agent Notes

## Quarterly Health Analysis Runbook

Use this guide to regenerate each quarter's health analysis and post assets.

### 1. Prepare Quarter Config

From the repo root:

```bash
cd notebooks
cp -n report_config.env.example report_config.env
```

Edit `notebooks/report_config.env`:

- `REPORT_QUERY_START_DATE`: earliest date for long-range trend charts (usually `2019-01-01`)
- `REPORT_QUARTER_START_DATE`: first day of target quarter
- `REPORT_QUARTER_END_DATE`: last day of target quarter
- `REPORT_POST_OUTPUT_DIR`: destination post folder (for example `../content/posts/2026-q1-health-review`)

Quarter boundaries:

- Q1: `YYYY-01-01` to `YYYY-03-31`
- Q2: `YYYY-04-01` to `YYYY-06-30`
- Q3: `YYYY-07-01` to `YYYY-09-30`
- Q4: `YYYY-10-01` to `YYYY-12-31`

### 2. Run the Analysis Pipeline

From `notebooks/`:

```bash
bash go.sh
```

Notes:

- `go.sh` validates `report_config.env` before running.
- It runs all analysis scripts, then moves generated images and CSV files into `REPORT_POST_OUTPUT_DIR`.

### 3. Validate Generated Outputs

Check the destination folder (example: `content/posts/2026-q1-health-review/`):

- Images: `summary.png`, `correlation_matrix.png`, `weekly_intensity_minutes.png`, `sleep_score_per_day.png`, `stress_level_per_day.png`, `stress_level_per_week.png`, and monthly trend charts
- CSVs in `data/`: quarterly metrics, stress/sleep quarter summaries, intensity series, monthly trend exports

Key behavior:

- Quarter-specific scripts output only the configured target quarter.
- Rolling windows are anchored to `REPORT_QUARTER_END_DATE`.
- Long-history monthly charts run from `REPORT_QUERY_START_DATE` to `REPORT_QUARTER_END_DATE`.

### 4. Update the Quarter Post

Edit the target post markdown file:

- `content/posts/YYYY-qN-health-review/index.md`

Use the generated CSVs in `content/posts/YYYY-qN-health-review/data/` to populate:

- quarter-over-quarter metrics
- intensity statistics
- sleep and stress observations
- correlation highlights

### 5. Optional Verification Commands

From repo root:

```bash
./.venv/bin/ruff check src/ .github/scripts/
./.venv/bin/pytest tests/ -v
cd notebooks && .venv/bin/pytest -q tests/
```

# Agent Notes

## Querying LifeDB MCP for Garmin Data

Use the LifeDB MCP server when the user asks about Garmin health, fitness, sleep, stress, body battery, HRV, steps, VO2 max, or activity data. Prefer MCP queries over guessing from memory.

The LifeDB MCP server exposes these core tools:

- `list_tables`: discover available Garmin/LifeDB tables and row counts.
- `describe_table(table_name)`: inspect columns, types, indexes, and inline schema comments.
- `execute_read_query(sql)`: run read-only `SELECT` or `WITH` SQL against the SQLite database.
- `search_activities(...)`: search workouts by sport, date range, and minimum distance.
- `get_activity_time_series(activity_id, metrics)`: pivot high-frequency activity metrics.
- `get_sync_status`: check sync/staleness status.
- `get_database_stats`: inspect database and archive size/table stats.
- `get_data_freshness`: check latest data by Garmin domain.

Recommended workflow:

1. Start with `get_sync_status` and `get_data_freshness` when freshness matters.
2. Use `list_tables` to confirm table names. Garmin tables may be singular, such as `activity`, not `activities`.
3. Use `describe_table` before writing SQL against a table you have not queried in this thread.
4. Use `execute_read_query` for aggregations, trends, date ranges, joins, and report calculations.
5. Include counts in aggregate answers so the user can see coverage, for example number of nights, days, or activities.

Important query rules:

- Only run read-only SQL. Do not attempt inserts, updates, deletes, schema changes, PRAGMAs, or attachment commands.
- Use explicit date ranges with inclusive start and exclusive end: `calendar_date >= '2026-04-01' and calendar_date < '2026-05-01'`.
- Prefer `calendar_date` for daily sleep records.
- Prefer `sleep_time_seconds` for total sleep duration, converting to hours with `sleep_time_seconds / 3600.0`.
- Activity distances are usually stored in meters; convert to kilometres with `distance / 1000.0` unless `describe_table` shows otherwise.
- Durations are usually seconds; convert to minutes or hours for user-facing answers.
- Keep result sets small unless the user explicitly asks for raw rows. Summaries and aggregates are usually better.

Example: average sleep in April 2026:

```sql
select
  count(*) as nights,
  round(avg(sleep_time_seconds) / 3600.0, 2) as avg_sleep_hours_decimal,
  cast(avg(sleep_time_seconds) / 3600 as integer) as avg_hours,
  cast((avg(sleep_time_seconds) % 3600) / 60 as integer) as avg_minutes,
  round(avg(score_overall_value), 1) as avg_sleep_score
from sleep
where calendar_date >= '2026-04-01'
  and calendar_date < '2026-05-01'
  and sleep_time_seconds is not null;
```

Example: recent activity volume by week:

```sql
select
  strftime('%Y-%W', start_ts) as week,
  count(*) as activities,
  round(sum(distance) / 1000.0, 1) as distance_km,
  round(sum(duration) / 3600.0, 1) as duration_hours
from activity
where start_ts >= '2026-01-01'
  and start_ts < '2026-04-01'
group by week
order by week;
```
