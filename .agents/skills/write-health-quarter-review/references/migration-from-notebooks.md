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
