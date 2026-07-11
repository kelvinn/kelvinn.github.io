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

## Chart Format Rules

Use the completed Q1 2026 health review images as the visual baseline for future quarters.

- `summary.png`: 2x2 monthly bar grid for the trailing 12 calendar months ending in the quarter-end month. Do not include partial pre-window months or any month after the quarter end. Add dashed trendlines and value labels on bars.
- `weekly_intensity_minutes.png`: trailing 12-month weekly bar chart with Sunday-ended bins, a red 800-minute target line, and a green average line. Convert LifeDB `TIME` fields to minutes before summing; do not coerce `HH:MM:SS` strings directly to numbers.
- `average_sleep_score_per_month.png`: start at the first month with sleep-score data, not at a configured historical query date with empty leading space. Use a blue line plus a translucent blue range band for variability.
- `sleep_score_per_day.png`: heatmap with one row per quarter from the first quarter with sleep-score data through the target quarter, columns Monday through Sunday plus `Avg`. Use a green-to-amber-to-red scale where higher scores are greener, and scores at or below 60 are clearly red.
- `stress_level_per_day.png`: same quarter-by-day heatmap structure as sleep, from the first quarter with daily stress data through the target quarter.
- `stress_level_per_week.png`: 12x7 trailing-week heatmap ending on the last complete Sunday on or before quarter end. For example, Q2 2026 ends on Tuesday, June 30, 2026, so this chart ends on Sunday, June 28, 2026.
- `monthly_vo2_max.png`: render when `monthly_vo2_max_per_month.csv` has rows. Use actual data months only and never include post-quarter readings.

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
