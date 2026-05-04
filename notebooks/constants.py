from report_config import load_report_config


_config = load_report_config()

# Backward-compatible names used by existing scripts.
start_date = _config.query_start_dt
end_date = _config.quarter_end_dt

# Explicit quarter window names for quarter-specific analysis.
quarter_start_date = _config.quarter_start_dt
quarter_end_date = _config.quarter_end_dt
quarter_start_ts = _config.quarter_start_ts
quarter_end_ts = _config.quarter_end_ts
quarter_label = _config.quarter_label

# Chronological quarter windows for day-of-week heatmaps.
day_of_week_quarter_windows = _config.day_of_week_quarter_windows
day_of_week_quarter_start_ts = day_of_week_quarter_windows[0].start_ts
day_of_week_quarter_range_label = (
    f"{day_of_week_quarter_windows[0].label} to {day_of_week_quarter_windows[-1].label}"
)
