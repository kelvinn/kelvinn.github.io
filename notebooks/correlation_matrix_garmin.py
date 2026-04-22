#!/usr/bin/env python3

"""
Correlation Matrix Generator for Garmin Health Data.
"""

import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from constants import quarter_end_ts, quarter_label, quarter_start_ts
from garmindb import GarminConnectConfigManager
from garmindb.summarydb import DaysSummary, SummaryDb


def time_to_minutes(t):
    """Convert time object to minutes since midnight."""
    if t is None:
        return None
    return t.hour * 60 + t.minute


def create_correlation_matrix():
    # Set up seaborn theme
    sns.set_theme(style="whitegrid")

    # Initialize database connection
    gc_config = GarminConnectConfigManager()
    db_params_dict = gc_config.get_db_params()
    sum_db = SummaryDb(db_params_dict, False)

    print(
        f"Querying health metrics for {quarter_label} "
        f"({quarter_start_ts.strftime('%Y-%m-%d')} to {quarter_end_ts.strftime('%Y-%m-%d')})..."
    )

    # Query daily summaries
    data_period = DaysSummary.get_for_period(sum_db, quarter_start_ts, quarter_end_ts, DaysSummary)
    print(f"Found {len(data_period)} days of data")

    # Create a list to store daily data
    daily_data = []

    for entry in data_period:
        try:
            mod_time = getattr(entry, "moderate_activity_time", None)
            vig_time = getattr(entry, "vigorous_activity_time", None)

            mod_minutes = time_to_minutes(mod_time) if mod_time else 0.0
            vig_minutes = time_to_minutes(vig_time) if vig_time else 0.0

            data = {
                "date": entry.day,
                "hr_min": float(entry.hr_min) if hasattr(entry, "hr_min") and entry.hr_min is not None else 0.0,
                "hr_max": float(entry.hr_max) if hasattr(entry, "hr_max") and entry.hr_max is not None else 0.0,
                "rhr_min": float(entry.rhr_min) if hasattr(entry, "rhr_min") and entry.rhr_min is not None else 0.0,
                "stress_avg": float(entry.stress_avg) if hasattr(entry, "stress_avg") and entry.stress_avg is not None else 0.0,
                "floors": float(entry.floors) if hasattr(entry, "floors") and entry.floors is not None else 0.0,
                "weight_avg": float(entry.weight_avg) if hasattr(entry, "weight_avg") and entry.weight_avg is not None else 0.0,
                "sleep_avg": float(time_to_minutes(entry.sleep_avg)) if hasattr(entry, "sleep_avg") and entry.sleep_avg is not None else 0.0,
                "calories_active_avg": float(entry.calories_active_avg) if hasattr(entry, "calories_active_avg") and entry.calories_active_avg is not None else 0.0,
                "bb_max": float(entry.bb_max) if hasattr(entry, "bb_max") and entry.bb_max is not None else 0.0,
                "bb_min": float(entry.bb_min) if hasattr(entry, "bb_min") and entry.bb_min is not None else 0.0,
                "moderate_activity_time": float(mod_minutes),
                "vigorous_activity_time": float(vig_minutes),
                "steps": float(entry.steps) if hasattr(entry, "steps") and entry.steps is not None else 0.0,
            }
            daily_data.append(data)
        except (ValueError, TypeError) as exc:
            print(f"Skipping entry for {entry.day}: {exc}")

    if not daily_data:
        print("No data found for the specified period")
        return

    # Convert to DataFrame
    df = pd.DataFrame(daily_data)
    df.set_index("date", inplace=True)

    metric_groups = [
        "hr_min",
        "hr_max",
        "rhr_min",
        "bb_max",
        "bb_min",
        "sleep_avg",
        "steps",
        "floors",
        "moderate_activity_time",
        "vigorous_activity_time",
        "calories_active_avg",
        "stress_avg",
        "weight_avg",
    ]
    metrics = [col for col in metric_groups if col in df.columns]

    # Calculate correlation matrix
    correlation_matrix = df[metrics].corr()

    plt.figure(figsize=(15, 13))
    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="RdYlBu_r",
        vmin=-1,
        vmax=1,
        center=0,
        square=True,
        fmt=".2f",
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
        annot_kws={"size": 8},
    )

    plt.title(
        f"Garmin Health Metrics Correlation Matrix\n{quarter_label} Analysis",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )

    plt.xticks(rotation=45, ha="right", fontsize=11)
    plt.yticks(rotation=0, fontsize=11)
    plt.subplots_adjust(left=0.2, bottom=0.2)

    plt.figtext(
        0.02,
        0.02,
        "Color intensity indicates correlation strength\n"
        "Blue: positive correlation | Red: negative correlation\n"
        "Range: -1 (perfect negative) to 1 (perfect positive)",
        fontsize=10,
        alpha=0.7,
    )

    plt.tight_layout()

    os.makedirs("data", exist_ok=True)
    os.makedirs("images", exist_ok=True)

    correlation_data = {
        "matrix": correlation_matrix,
        "metrics": metrics,
        "date_range": {"start": quarter_start_ts, "end": quarter_end_ts},
    }
    with open("data/correlation_data.pkl", "wb") as f:
        pickle.dump(correlation_data, f)
    print("Correlation data saved as 'data/correlation_data.pkl'")

    correlation_matrix.to_csv("data/correlation_matrix.csv")
    print("Correlation matrix also saved as 'data/correlation_matrix.csv'")

    plt.savefig("images/correlation_matrix.png", dpi=300, bbox_inches="tight")
    print("Correlation matrix plot saved as 'images/correlation_matrix.png'")

    print("\nData Summary:")
    print(f"Total days analyzed: {len(df)}")
    print("\nMissing values per metric:")
    print(df[metrics].isnull().sum())

    print("\nTop 10 strongest correlations:")
    correlations = []
    for i in range(len(metrics)):
        for j in range(i + 1, len(metrics)):
            corr = correlation_matrix.iloc[i, j]
            if not pd.isna(corr):
                correlations.append((metrics[i], metrics[j], abs(corr), corr))

    correlations.sort(key=lambda x: x[2], reverse=True)
    for metric1, metric2, _, corr in correlations[:10]:
        print(f"{metric1} vs {metric2}: {corr:.3f}")


if __name__ == "__main__":
    create_correlation_matrix()
