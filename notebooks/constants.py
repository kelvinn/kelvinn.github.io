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
