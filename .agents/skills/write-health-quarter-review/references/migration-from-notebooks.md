# Migration From Notebooks

The current analysis pipeline lives in `notebooks/`. Treat it as the behavior source while migrating toward skill-owned scripts.

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

Migration phases:

1. Keep using `notebooks/go.sh` through `scripts/generate_health_assets.py`.
2. Port chart/data generation into skill scripts while matching filenames and CSV schemas.
3. Replace direct GarminDB dependencies with LifeDB queries where possible.
4. Delete `notebooks/` only after generated assets and validation match the old pipeline.

When changing chart generation, keep output filenames stable so existing markdown image references continue to work.
