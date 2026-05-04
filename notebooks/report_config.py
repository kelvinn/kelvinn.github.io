from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Mapping


REQUIRED_KEYS = (
    "REPORT_QUERY_START_DATE",
    "REPORT_QUARTER_START_DATE",
    "REPORT_QUARTER_END_DATE",
    "REPORT_POST_OUTPUT_DIR",
)

DEFAULT_PREVIOUS_QUARTERS = 13


class ReportConfigError(ValueError):
    """Raised when quarterly report configuration is missing or invalid."""


@dataclass(frozen=True)
class QuarterWindow:
    label: str
    start_dt: datetime
    end_dt: datetime

    @property
    def start_ts(self) -> datetime:
        return datetime.combine(self.start_dt.date(), time.min)

    @property
    def end_ts(self) -> datetime:
        return datetime.combine(self.end_dt.date(), time.max)


@dataclass(frozen=True)
class ReportConfig:
    query_start_dt: datetime
    quarter_start_dt: datetime
    quarter_end_dt: datetime
    post_output_dir: str

    @property
    def quarter_label(self) -> str:
        quarter = ((self.quarter_start_dt.month - 1) // 3) + 1
        return f"Q{quarter} {self.quarter_start_dt.year}"

    @property
    def quarter_slug(self) -> str:
        quarter = ((self.quarter_start_dt.month - 1) // 3) + 1
        return f"{self.quarter_start_dt.year}-q{quarter}"

    @property
    def query_start_ts(self) -> datetime:
        return datetime.combine(self.query_start_dt.date(), time.min)

    @property
    def quarter_start_ts(self) -> datetime:
        return datetime.combine(self.quarter_start_dt.date(), time.min)

    @property
    def quarter_end_ts(self) -> datetime:
        return datetime.combine(self.quarter_end_dt.date(), time.max)

    @property
    def day_of_week_quarter_windows(self) -> list[QuarterWindow]:
        return quarter_windows_ending_at(self.quarter_start_dt)


def parse_iso_date_to_datetime(value: str, key_name: str) -> datetime:
    try:
        parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ReportConfigError(
            f"Invalid {key_name}='{value}'. Expected YYYY-MM-DD."
        ) from exc
    return datetime.combine(parsed_date, time.min)


def inclusive_day_bounds(start_value: datetime | date, end_value: datetime | date) -> tuple[datetime, datetime]:
    start_day = start_value.date() if isinstance(start_value, datetime) else start_value
    end_day = end_value.date() if isinstance(end_value, datetime) else end_value
    return datetime.combine(start_day, time.min), datetime.combine(end_day, time.max)


def quarter_number_for_month(month: int) -> int:
    return ((month - 1) // 3) + 1


def quarter_start_for(value: datetime | date) -> datetime:
    value_date = value.date() if isinstance(value, datetime) else value
    quarter = quarter_number_for_month(value_date.month)
    start_month = ((quarter - 1) * 3) + 1
    return datetime.combine(date(value_date.year, start_month, 1), time.min)


def add_quarters(quarter_start_dt: datetime, quarter_offset: int) -> datetime:
    quarter = quarter_number_for_month(quarter_start_dt.month)
    zero_based_quarter = quarter - 1 + quarter_offset
    year = quarter_start_dt.year + (zero_based_quarter // 4)
    target_quarter = (zero_based_quarter % 4) + 1
    target_month = ((target_quarter - 1) * 3) + 1
    return datetime.combine(date(year, target_month, 1), time.min)


def quarter_end_for_start(quarter_start_dt: datetime) -> datetime:
    next_quarter_start = add_quarters(quarter_start_dt, 1)
    return datetime.combine((next_quarter_start - timedelta(days=1)).date(), time.min)


def quarter_label_for_start(quarter_start_dt: datetime) -> str:
    quarter = quarter_number_for_month(quarter_start_dt.month)
    return f"Q{quarter} {quarter_start_dt.year}"


def quarter_windows_ending_at(
    focus_quarter_start_dt: datetime | date,
    previous_quarters: int = DEFAULT_PREVIOUS_QUARTERS,
) -> list[QuarterWindow]:
    if previous_quarters < 0:
        raise ReportConfigError("previous_quarters must be greater than or equal to 0.")

    focus_start = quarter_start_for(focus_quarter_start_dt)
    first_start = add_quarters(focus_start, -previous_quarters)

    windows = []
    for offset in range(previous_quarters + 1):
        window_start = add_quarters(first_start, offset)
        windows.append(
            QuarterWindow(
                label=quarter_label_for_start(window_start),
                start_dt=window_start,
                end_dt=quarter_end_for_start(window_start),
            )
        )
    return windows


def load_report_config(env: Mapping[str, str] | None = None) -> ReportConfig:
    env_map = env if env is not None else os.environ

    missing = [key for key in REQUIRED_KEYS if not env_map.get(key)]
    if missing:
        raise ReportConfigError(
            "Missing required report config keys: " + ", ".join(missing)
        )

    query_start_dt = parse_iso_date_to_datetime(
        env_map["REPORT_QUERY_START_DATE"], "REPORT_QUERY_START_DATE"
    )
    quarter_start_dt = parse_iso_date_to_datetime(
        env_map["REPORT_QUARTER_START_DATE"], "REPORT_QUARTER_START_DATE"
    )
    quarter_end_dt = parse_iso_date_to_datetime(
        env_map["REPORT_QUARTER_END_DATE"], "REPORT_QUARTER_END_DATE"
    )

    if not (query_start_dt <= quarter_start_dt <= quarter_end_dt):
        raise ReportConfigError(
            "Invalid report date range ordering. Expected "
            "REPORT_QUERY_START_DATE <= REPORT_QUARTER_START_DATE <= REPORT_QUARTER_END_DATE."
        )

    post_output_dir = env_map["REPORT_POST_OUTPUT_DIR"].strip()
    if not post_output_dir:
        raise ReportConfigError("REPORT_POST_OUTPUT_DIR must not be empty.")

    return ReportConfig(
        query_start_dt=query_start_dt,
        quarter_start_dt=quarter_start_dt,
        quarter_end_dt=quarter_end_dt,
        post_output_dir=post_output_dir,
    )


if __name__ == "__main__":
    cfg = load_report_config()
    print(
        f"Loaded report config: query_start={cfg.query_start_dt.date()}, "
        f"quarter_start={cfg.quarter_start_dt.date()}, quarter_end={cfg.quarter_end_dt.date()}, "
        f"output_dir={cfg.post_output_dir}"
    )
