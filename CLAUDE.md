# Quarterly Health Analysis Runbook

Use this guide to regenerate each quarter's health analysis and post assets.

## 1. Prepare Quarter Config

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

## 2. Run the Analysis Pipeline

From `notebooks/`:

```bash
bash go.sh
```

Notes:

- `go.sh` validates `report_config.env` before running.
- It runs all analysis scripts, then moves generated images and CSV files into `REPORT_POST_OUTPUT_DIR`.

## 3. Validate Generated Outputs

Check the destination folder (example: `content/posts/2026-q1-health-review/`):

- Images: `summary.png`, `correlation_matrix.png`, `weekly_intensity_minutes.png`, `sleep_score_per_day.png`, `stress_level_per_day.png`, `stress_level_per_week.png`, and monthly trend charts
- CSVs in `data/`: quarterly metrics, stress/sleep quarter summaries, intensity series, monthly trend exports

Key behavior:

- Quarter-specific scripts output only the configured target quarter.
- Rolling windows are anchored to `REPORT_QUARTER_END_DATE`.
- Long-history monthly charts run from `REPORT_QUERY_START_DATE` to `REPORT_QUARTER_END_DATE`.

## 4. Update the Quarter Post

Edit the target post markdown file:

- `content/posts/YYYY-qN-health-review/index.md`

Use the generated CSVs in `content/posts/YYYY-qN-health-review/data/` to populate:

- quarter-over-quarter metrics
- intensity statistics
- sleep and stress observations
- correlation highlights

## 5. Optional Verification Commands

From repo root:

```bash
./.venv/bin/ruff check src/ .github/scripts/
./.venv/bin/pytest tests/ -v
cd notebooks && .venv/bin/pytest -q tests/
```
