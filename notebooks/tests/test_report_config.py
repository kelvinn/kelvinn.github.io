import os
import sys
from datetime import datetime

import pytest

# Ensure tests can import modules from notebooks/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from report_config import ReportConfigError, load_report_config, quarter_windows_ending_at


def _valid_env():
    return {
        "REPORT_QUERY_START_DATE": "2019-01-01",
        "REPORT_QUARTER_START_DATE": "2026-01-01",
        "REPORT_QUARTER_END_DATE": "2026-03-31",
        "REPORT_POST_OUTPUT_DIR": "../content/posts/2026-q1-health-review",
    }


def test_load_report_config_valid():
    cfg = load_report_config(_valid_env())

    assert cfg.query_start_dt.strftime("%Y-%m-%d") == "2019-01-01"
    assert cfg.quarter_start_dt.strftime("%Y-%m-%d") == "2026-01-01"
    assert cfg.quarter_end_dt.strftime("%Y-%m-%d") == "2026-03-31"
    assert cfg.post_output_dir == "../content/posts/2026-q1-health-review"


def test_day_of_week_quarter_windows_cover_focus_and_previous_13_quarters():
    cfg = load_report_config(_valid_env())

    windows = cfg.day_of_week_quarter_windows

    assert len(windows) == 14
    assert windows[0].label == "Q4 2022"
    assert windows[0].start_dt.strftime("%Y-%m-%d") == "2022-10-01"
    assert windows[0].end_dt.strftime("%Y-%m-%d") == "2022-12-31"
    assert windows[-1].label == "Q1 2026"
    assert windows[-1].start_dt.strftime("%Y-%m-%d") == "2026-01-01"
    assert windows[-1].end_dt.strftime("%Y-%m-%d") == "2026-03-31"


def test_quarter_windows_are_chronological_and_calendar_aligned():
    windows = quarter_windows_ending_at(datetime(2026, 1, 1), previous_quarters=13)

    assert [window.label for window in windows] == [
        "Q4 2022",
        "Q1 2023",
        "Q2 2023",
        "Q3 2023",
        "Q4 2023",
        "Q1 2024",
        "Q2 2024",
        "Q3 2024",
        "Q4 2024",
        "Q1 2025",
        "Q2 2025",
        "Q3 2025",
        "Q4 2025",
        "Q1 2026",
    ]
    assert all(
        windows[index].start_dt > windows[index - 1].start_dt
        for index in range(1, len(windows))
    )
    assert all(window.start_ts.strftime("%H:%M:%S") == "00:00:00" for window in windows)
    assert all(window.end_ts.strftime("%H:%M:%S.%f") == "23:59:59.999999" for window in windows)


def test_load_report_config_missing_key():
    env = _valid_env()
    env.pop("REPORT_QUERY_START_DATE")

    with pytest.raises(ReportConfigError, match="Missing required report config keys"):
        load_report_config(env)


def test_load_report_config_bad_date_format():
    env = _valid_env()
    env["REPORT_QUARTER_START_DATE"] = "2026/01/01"

    with pytest.raises(ReportConfigError, match="Expected YYYY-MM-DD"):
        load_report_config(env)


def test_load_report_config_invalid_order_quarter_end_before_start():
    env = _valid_env()
    env["REPORT_QUARTER_START_DATE"] = "2026-04-01"
    env["REPORT_QUARTER_END_DATE"] = "2026-03-31"

    with pytest.raises(ReportConfigError, match="Invalid report date range ordering"):
        load_report_config(env)


def test_load_report_config_invalid_order_query_start_after_quarter_end():
    env = _valid_env()
    env["REPORT_QUERY_START_DATE"] = "2026-04-01"

    with pytest.raises(ReportConfigError, match="Invalid report date range ordering"):
        load_report_config(env)
