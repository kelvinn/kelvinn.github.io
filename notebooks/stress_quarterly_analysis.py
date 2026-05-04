#!/usr/bin/env python3
"""
Create a heatmap showing average stress level per day of the week by quarter.
Quarter on y-axis, days of week on x-axis, with average column.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from constants import (
    day_of_week_quarter_range_label,
    day_of_week_quarter_start_ts,
    day_of_week_quarter_windows,
    quarter_end_ts,
)
from garmindb import GarminConnectConfigManager
from garmindb.summarydb import DaysSummary, SummaryDb

# Set up seaborn theme
sns.set_theme(style="whitegrid")


def quarter_index_for_date(value):
    return (value.year * 4) + ((value.month - 1) // 3)


def mean_or_nan(values):
    return np.mean(values) if values else np.nan


def create_quarterly_stress_heatmap():
    """Create a heatmap for average stress levels per day of week by quarter."""

    os.makedirs("images", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    print(
        f"Creating quarterly stress analysis for {day_of_week_quarter_range_label} "
        f"({day_of_week_quarter_start_ts.strftime('%Y-%m-%d')} to "
        f"{quarter_end_ts.strftime('%Y-%m-%d')})..."
    )

    gc_config = GarminConnectConfigManager()
    db_params_dict = gc_config.get_db_params()
    sum_db = SummaryDb(db_params_dict, False)

    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    column_labels = day_names + ["Avg"]
    quarter_by_index = {
        quarter_index_for_date(window.start_dt): window
        for window in day_of_week_quarter_windows
    }

    data_period = DaysSummary.get_for_period(
        sum_db, day_of_week_quarter_start_ts, quarter_end_ts, DaysSummary
    )
    stress_data = [entry for entry in data_period if entry.stress_avg is not None]

    print(f"Found {len(stress_data)} days with stress data")
    if not stress_data:
        print("No stress data available for configured quarter range")
        return None, [], []

    stress_by_quarter_day = {
        window.label: {day: [] for day in range(7)}
        for window in day_of_week_quarter_windows
    }
    for entry in stress_data:
        quarter_window = quarter_by_index.get(quarter_index_for_date(entry.day))
        if quarter_window is None:
            continue
        stress_by_quarter_day[quarter_window.label][entry.day.weekday()].append(
            entry.stress_avg
        )

    heatmap_matrix = []
    quarter_labels = []
    for window in day_of_week_quarter_windows:
        quarter_day_values = stress_by_quarter_day[window.label]
        quarter_values = [mean_or_nan(quarter_day_values[day]) for day in range(7)]
        all_values = [
            value
            for values in quarter_day_values.values()
            for value in values
        ]
        quarter_values.append(mean_or_nan(all_values))
        heatmap_matrix.append(quarter_values)
        quarter_labels.append(window.label)

    export_df = pd.DataFrame(heatmap_matrix, columns=column_labels)
    export_df.insert(0, "quarter", quarter_labels)
    csv_path = os.path.join("data", "stress_quarterly_per_quarter.csv")
    export_df.to_csv(csv_path, index=False)
    print(f"Exported quarterly stress data to {csv_path}")

    heatmap_array = np.array(heatmap_matrix)

    plt.figure(figsize=(12, 8.5))
    sns.heatmap(
        heatmap_array,
        xticklabels=column_labels,
        yticklabels=quarter_labels,
        annot=True,
        fmt=".1f",
        cmap="viridis",
        cbar_kws={"label": "Average Stress Level"},
        linewidths=0.5,
        square=True,
        cbar=True,
        mask=np.isnan(heatmap_array),
    )

    plt.title(
        f"Average Stress Level per Day of Week ({day_of_week_quarter_range_label})",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    plt.xlabel("Day of Week", fontsize=14)
    plt.ylabel("Quarter", fontsize=14)
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)

    plt.tight_layout()
    plt.savefig("images/stress_level_per_day.png", dpi=300, bbox_inches="tight")
    print("\nHeatmap saved as 'images/stress_level_per_day.png'")

    valid_values = heatmap_array[~np.isnan(heatmap_array)]
    if len(valid_values) > 0:
        print(
            f"Overall stress level - Min: {valid_values.min():.1f}, "
            f"Max: {valid_values.max():.1f}, Mean: {valid_values.mean():.1f}"
        )

    return heatmap_array, quarter_labels, column_labels


if __name__ == "__main__":
    create_quarterly_stress_heatmap()
