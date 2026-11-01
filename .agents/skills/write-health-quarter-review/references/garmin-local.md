# Local Garmin Sources

`scripts/export_garmin.py` reads the local Garmin databases in `~/HealthData/DBs` (override with `--db-dir`) read-only and writes `data/garmin_export.json` for `generate_health_assets.py`.

| Metric | Source |
| --- | --- |
| RHR, stress, steps, floors, HR min/max, body battery, weight, active calories, moderate/vigorous minutes | `garmin_summary.db` `days_summary` |
| sleep score | `garmin.db` `sleep.score` (available from 2023-01-05) |
| VO2 max readings | `garmin_activities.db` `steps_activities.vo2_max` joined to `activities` |
| activity counts, sport mix | `garmin_activities.db` `activities` (`sport`, `distance` in km, `moving_time`) |

Intensity minutes are derived by the renderer as moderate + 2 x vigorous. Timestamps are local time.

## Checks before writing a post

- Run the exporter and read the "non-null days per metric" line. Every Q-window metric should cover all days. If `bb_max`, `rhr_min`, `intensity` or sleep scores are missing for recent days, the databases are stale or partially rebuilt; do not write the post from them.
- Check `latest day in database` covers the quarter end.
- Compare the prior quarter's figures from this database to the published post. The 2026-10 rebuild matched Q1 2026 exactly (363 active calories, 75.0 body battery, 6,421 steps, 30.2 stress, 35.6 intensity/day) and restated Q2 slightly (steps 9,297 vs 9,069 published, calories 537 vs 520). Quote prior-quarter comparisons from the same database and say when they differ from the published post.
- The renderer's `quarterly_metrics_raw.csv` reports medians, but earlier posts quote means; compute means from the export when writing prose.
- After a broken sync, the databases can be rebuilt from `~/HealthData` with `garmindb_cli.py --rebuild_db`, or fully re-downloaded with `garmindb_cli.py --all --download --import --analyze` (needs Garmin credentials in `~/.GarminDb/GarminConnectConfig.json`).

## History

Earlier in 2026-10 the databases were partially empty (body battery only from 2026-07-12, intensity zero before it, only ~42 activities). Those were symptoms of an incomplete import, fixed by the re-download and rebuild, so the exporter no longer reads raw JSON files or splices values from earlier posts.
