import os
import sys

import pytest

# Ensure tests can import modules from notebooks/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from report_config import ReportConfigError, load_report_config


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
