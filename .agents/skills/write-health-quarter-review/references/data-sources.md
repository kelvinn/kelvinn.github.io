# Data Sources

## Repo Assets

Quarter posts live under:

`content/posts/YYYY-qN-health-review/`

The canonical new-post template is:

`content/posts/20NN-qN-health-review-TEMPLATE/`

Expected generated images:

- `summary.png`
- `correlation_matrix.png`
- `weekly_intensity_minutes.png`
- `sleep_score_per_day.png`
- `stress_level_per_day.png`
- `stress_level_per_week.png`
- `average_resting_hr_per_month.png`
- `average_sleep_score_per_month.png`
- `average_active_calories_per_month.png`

Optional image when VO2 max data exists:

- `monthly_vo2_max.png`

Expected generated CSVs under `data/`:

- `quarterly_metrics_raw.csv`
- `weekly_intensity_minutes_per_week.csv`
- `average_sleep_score_per_month.csv`
- `average_resting_hr_per_month.csv`
- `average_active_calories_per_month.csv`
- `correlation_matrix.csv`
- `stress_quarterly_per_quarter.csv`
- `sleep_score_per_day_per_quarter.csv`
- `summary_quartet_per_month.csv`
- `monthly_vo2_max_per_month.csv`

## LifeDB MCP

Use the `lifedb` MCP server at `https://lifedb.fly.dev/mcp` for Garmin health, fitness, sleep, stress, body battery, HRV, steps, VO2 max, and activity data.
Use only LifeDB MCP for Garmin data. Do not read GarminDB SQLite files or `~/HealthData/DBs` directly.

Default workflow:

1. Start with `get_sync_status` and `get_data_freshness` when freshness matters.
2. Use `list_tables` to confirm table names.
3. Use `describe_table(table_name)` before SQL against a table not yet inspected.
4. Use read-only `SELECT` or `WITH` queries only.
5. Use inclusive start and exclusive end dates, for example:

```sql
where calendar_date >= '2026-04-01'
  and calendar_date < '2026-07-01'
```

Include row counts in aggregate answers.

For chart and CSV generation, follow `lifedb-mcp-export.md`: query LifeDB MCP, save `data/lifedb_export.json`, then render local assets from that export.

## Biomarker Google Sheet

Spreadsheet:

`https://docs.google.com/spreadsheets/d/1COdRXGsGo0Zbx-DpOTHFN7XTBktHY3XF6i7St1GBJSc/edit`

Use the Google Sheets connector. Read spreadsheet metadata before live range reads.

Relevant tabs:

- `Biomarkers`
- `PhenoAge History`

`Biomarkers` columns:

- `Biomarker`
- `Value`
- `Units`
- `Reference Range`
- `Test Date`
- `Notes`

`PhenoAge History` columns:

- `Date`
- `Chronological Age`
- `Phenotypic Age`
- `Difference`

Use displayed values for user-facing biomarker tables so values like `<0.2` and `>90` remain intact.
