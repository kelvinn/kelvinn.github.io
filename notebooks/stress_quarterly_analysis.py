#!/usr/bin/env python3
"""
Create a heatmap showing average stress level per day of the week for the configured quarter.
Quarter on y-axis (single row), days of week on x-axis, with average column.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from constants import quarter_end_ts, quarter_label, quarter_start_ts
from garmindb import GarminConnectConfigManager
from garmindb.summarydb import DaysSummary, SummaryDb

# Set up seaborn theme
sns.set_theme(style="whitegrid")


def create_quarterly_stress_heatmap():
    """Create a heatmap for configured-quarter average stress levels per day of week."""

    os.makedirs("images", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    print(
        f"Creating quarterly stress analysis for {quarter_label} "
        f"({quarter_start_ts.strftime('%Y-%m-%d')} to {quarter_end_ts.strftime('%Y-%m-%d')})..."
    )

    gc_config = GarminConnectConfigManager()
    db_params_dict = gc_config.get_db_params()
    sum_db = SummaryDb(db_params_dict, False)

    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    data_period = DaysSummary.get_for_period(sum_db, quarter_start_ts, quarter_end_ts, DaysSummary)
    stress_data = [entry for entry in data_period if entry.stress_avg is not None]

    print(f"Found {len(stress_data)} days with stress data")
    if not stress_data:
        print("No stress data available for configured quarter")
        return None, [], []

    stress_by_day = {day: [] for day in range(7)}
    for entry in stress_data:
        stress_by_day[entry.day.weekday()].append(entry.stress_avg)

    quarter_values = []
    for day in range(7):
        values = stress_by_day[day]
        quarter_values.append(np.mean(values) if values else np.nan)

    all_values = [value for values in stress_by_day.values() for value in values]
    quarter_avg = np.mean(all_values) if all_values else np.nan
    quarter_values.append(quarter_avg)

    heatmap_matrix = [quarter_values]
    quarter_labels = [quarter_label]

    export_df = pd.DataFrame(
        [
            {
                "quarter": quarter_label,
                "Mon": quarter_values[0],
                "Tue": quarter_values[1],
                "Wed": quarter_values[2],
                "Thu": quarter_values[3],
                "Fri": quarter_values[4],
                "Sat": quarter_values[5],
                "Sun": quarter_values[6],
                "Avg": quarter_values[7],
            }
        ]
    )
    csv_path = os.path.join("data", "stress_quarterly_per_quarter.csv")
    export_df.to_csv(csv_path, index=False)
    print(f"Exported quarterly stress data to {csv_path}")

    heatmap_array = np.array(heatmap_matrix)
    column_labels = day_names + ["Avg"]

    plt.figure(figsize=(8, 3.5))
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
        f"Average Stress Level per Day of Week ({quarter_label})",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )
    plt.xlabel("Day of Week", fontsize=12)
    plt.ylabel("Quarter", fontsize=12)
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
