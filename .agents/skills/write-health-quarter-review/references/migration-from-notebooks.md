# Migration From Notebooks

The old analysis pipeline lives in `notebooks/`. Treat it as historical behavior reference only. New Garmin data access must use LifeDB MCP.

Current wrapper:

`notebooks/go.sh`

It reads `report_config.env`, validates it, runs the analysis scripts, then moves generated PNG and CSV files into `REPORT_POST_OUTPUT_DIR`.

Important config keys:

- `REPORT_QUERY_START_DATE`
- `REPORT_QUARTER_START_DATE`
- `REPORT_QUARTER_END_DATE`
- `REPORT_POST_OUTPUT_DIR`

Important scripts to preserve or port:

- `average_sleep_score_per_month.py`
- `average_resting_hr_per_month.py`
- `average_active_calories_per_month.py`
- `summary_quartet.py`
- `summary_per_quarter.py`
- `stress_quarterly_analysis.py`
- `stress_heatmap_12weeks.py`
- `weekly_intensity_minutes.py`
- `correlation_matrix_garmin.py`
- `average_sleep_score_per_day.py`
- `monthly_vo2_max.py`

Migration status:

1. Chart/data rendering has moved into `scripts/generate_health_assets.py`.
2. Garmin data extraction is defined in `lifedb-mcp-export.md` and must be done through LifeDB MCP.
3. Direct GarminDB dependencies should not be used by this skill.
4. `notebooks/` can be deleted for this skill once the MCP export/render path has been verified for the target quarter.

When changing chart generation, keep output filenames stable so existing markdown image references continue to work.

Visual compatibility notes:

- The MCP renderer should match the completed Q1 2026 notebook outputs unless a post explicitly asks for a new format.
- Keep `summary.png` as the Q1-style 2x2 trailing-12-month bar grid with trendlines and value labels.
- Keep day-of-week sleep and stress charts as quarter-by-day heatmaps from data start through the target quarter, not target-quarter-only heatmaps.
- Keep the 12-week stress heatmap ending on the last complete Sunday on or before quarter end.
- Prefer actual data start dates for long-range monthly charts; do not show empty leading ranges just because `REPORT_QUERY_START_DATE` is earlier than the first available metric.
