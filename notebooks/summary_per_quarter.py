#!/usr/bin/env python3
"""
Create a table showing configured-quarter health metrics:
- Resting Heart Rate (RHR): Median of daily minimum RHR
- Stress Levels: Median of daily average stress
- Steps: Average of daily steps
- Body Battery (max): Median of daily max body battery
- Intensity Minutes: Median of weekly sums
- VO2Max: 95th percentile of running activities
"""

import os

import numpy as np
import pandas as pd
import seaborn as sns
from constants import quarter_end_ts, quarter_label, quarter_start_ts
from garmindb import GarminConnectConfigManager
from garmindb.garmindb import Activities
from garmindb.summarydb import DaysSummary, SummaryDb
from sqlalchemy.orm import sessionmaker
from vo2max_db import Vo2MaxActivities, engine

# Set up seaborn theme
sns.set_theme(style="whitegrid")


def time_to_minutes(time_obj):
    """Convert time object to minutes."""
    if pd.isna(time_obj) or time_obj is None:
        return 0
    return time_obj.hour * 60 + time_obj.minute


def get_vo2max_95th_percentile(start_ts, end_ts):
    """Get the 95th percentile VO2Max value for running activities within date range."""
    Session = sessionmaker(bind=engine)
    session = Session()
    results = (
        session.query(Activities, Vo2MaxActivities)
        .join(Activities, Activities.activity_id == Vo2MaxActivities.activity_id)
        .filter(Activities.start_time >= start_ts, Activities.start_time <= end_ts)
        .all()
    )
    session.close()

    vo2_values = [vo2.vo2_max for _, vo2 in results if vo2 is not None and vo2.vo2_max is not None]
    if not vo2_values:
        return np.nan

    return np.percentile(vo2_values, 95)


def calculate_weekly_intensity_minutes(data_period):
    """Calculate the median of weekly summed intensity minutes."""
    daily_minutes = []
    for entry in data_period:
        if entry.intensity_time is not None:
            daily_minutes.append({"date": pd.to_datetime(entry.day), "minutes": time_to_minutes(entry.intensity_time)})

    if not daily_minutes:
        return np.nan

    df = pd.DataFrame(daily_minutes)
    df.set_index("date", inplace=True)
    weekly_sum = df["minutes"].resample("W").sum()

    return np.median(weekly_sum)


def create_quarterly_metrics_heatmap():
    """Create configured-quarter metrics table (raw, non-normalized)."""
    os.makedirs("images", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    gc_config = GarminConnectConfigManager()
    db_params_dict = gc_config.get_db_params()
    sum_db = SummaryDb(db_params_dict, False)

    metrics = {
        "RHR": "Median daily minimum RHR",
        "Stress": "Median daily average stress",
        "Steps": "Average daily steps",
        "Body Battery": "Median daily max body battery",
        "Intensity": "Median of weekly intensity minutes",
        "VO2Max": "95th percentile from running activities",
    }

    print(
        f"Processing quarterly data for {quarter_label} "
        f"({quarter_start_ts.strftime('%Y-%m-%d')} to {quarter_end_ts.strftime('%Y-%m-%d')})"
    )

    data_period = DaysSummary.get_for_period(sum_db, quarter_start_ts, quarter_end_ts, DaysSummary)

    quarter_metrics = []

    rhr_values = [day.rhr_min for day in data_period if day.rhr_min is not None]
    quarter_metrics.append(np.median(rhr_values) if rhr_values else np.nan)

    stress_values = [day.stress_avg for day in data_period if day.stress_avg is not None]
    quarter_metrics.append(np.median(stress_values) if stress_values else np.nan)

    steps_values = [day.steps for day in data_period if day.steps is not None]
    quarter_metrics.append(int(np.mean(steps_values)) if steps_values else np.nan)

    bb_values = [day.bb_max for day in data_period if day.bb_max is not None]
    quarter_metrics.append(np.median(bb_values) if bb_values else np.nan)

    intensity_median = calculate_weekly_intensity_minutes(data_period)
    quarter_metrics.append(intensity_median)

    vo2max_value = get_vo2max_95th_percentile(quarter_start_ts, quarter_end_ts)
    quarter_metrics.append(round(vo2max_value, 2) if not np.isnan(vo2max_value) else np.nan)

    print(f"{quarter_label} metrics:", dict(zip(metrics.keys(), quarter_metrics)))

    df = pd.DataFrame([quarter_metrics], columns=list(metrics.keys()), index=[quarter_label])
    print("\nQuarterly Metrics Table (raw):")
    print(df.to_string(index=True))

    df.to_csv("data/quarterly_metrics_raw.csv")


if __name__ == "__main__":
    create_quarterly_metrics_heatmap()
