#!/usr/bin/env python3
"""
Create a heatmap showing daily stress level per week for the previous 12 weeks from today.
Week of year on vertical axis, day of week on horizontal axis.
Cells have vertical padding for better visualization.
"""

import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pandas as pd
import seaborn as sns
import os
from datetime import datetime, timedelta
from constants import end_date

from garmindb import GarminConnectConfigManager
from garmindb.garmindb import GarminSummaryDb, DaysSummary, MonitoringDb, MonitoringHeartRate, Sleep, GarminDb
from garmindb.summarydb import DaysSummary, SummaryDb

# Set up seaborn theme
sns.set_theme(style="whitegrid")


def create_stress_heatmap_12weeks():
    """Create a heatmap showing daily stress levels for the previous 12 weeks."""
    
    # Create images directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    # Calculate date range for previous 12 weeks (84 days)
    start_date = end_date - timedelta(days=84)  # Exactly 12 weeks
    
    print(f"Creating heatmap for stress levels from {start_date} to {end_date}")
    print(f"Date range: {end_date - start_date} days (12 weeks)")
    
    # Initialize Garmin database connection
    gc_config = GarminConnectConfigManager()
    db_params_dict = gc_config.get_db_params()
    
    # Query stress data for the previous 12 weeks
    start_ts = datetime.combine(start_date, datetime.min.time())
    end_ts = datetime.combine(end_date, datetime.max.time())
    
    # Get daily summary data for the period
    sum_db = SummaryDb(db_params_dict, False)
    data_period = DaysSummary.get_for_period(sum_db, start_ts, end_ts, DaysSummary)
    
    print(f"Found {len(data_period)} days of data for the period")
    
    # Filter data with stress values
    stress_data = [entry for entry in data_period if entry.stress_avg is not None]
    print(f"Found {len(stress_data)} days with stress data")
    
    if not stress_data:
        print("No stress data available for the period")
        return
    
    # Create a 12x7 matrix initialized with NaN (12 weeks, 7 days per week)
    heatmap_matrix = [[np.nan for _ in range(7)] for _ in range(12)]
    
    # Populate the matrix by relative week index (0 = oldest week, 11 = most recent)
    for entry in stress_data:
        diff_days = (entry.day - start_date).days
        if 0 <= diff_days < 12 * 7:
            week_idx = diff_days // 7
            day_of_week = entry.day.weekday()  # 0=Monday, 6=Sunday
            heatmap_matrix[week_idx][day_of_week] = entry.stress_avg
    
    # Week labels (1-12)
    week_labels = [f"Week {i+1}" for i in range(12)]
    # Day names for x-axis labels
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # Convert to numpy array
    heatmap_array = np.array(heatmap_matrix)
    
    # Create the heatmap with vertical padding
    # Use a larger figure size and adjust the aspect ratio for vertical padding
    fig_height = max(12, 12 * 1.2)  # Increased height for more vertical padding
    plt.figure(figsize=(12, fig_height))
    
    # Create heatmap with vertical padding
    ax = sns.heatmap(heatmap_array,
                     xticklabels=day_names,
                     yticklabels=week_labels,
                     annot=True,
                     fmt='.1f',
                     cmap='YlOrRd',
                     cbar_kws={'label': 'Stress Level'},
                     linewidths=0.5,
 
                     square=False,  # Allow rectangular cells for vertical padding
                     cbar=True,
                     mask=np.isnan(heatmap_array))
    
    # ax.set_yticklabels(ax.get_yticklabels(), ha='center')
    
    # Add vertical padding by adjusting the aspect ratio
    ax.set_aspect('auto')
    
    # Add extra vertical padding by adjusting the spacing
    ax.figure.subplots_adjust(left=0.15, right=0.85, top=0.95, bottom=0.1)
    
    plt.title(f'Daily Stress Level per Week (Previous 12 Weeks)\n({start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")})', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Day of Week', fontsize=14)
    plt.ylabel('Week of Year', fontsize=14)
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    
    # Add more vertical padding by adjusting the y-axis spacing
    ax.set_yticks(range(len(week_labels)))
    ax.set_yticklabels(week_labels)

    plt.tight_layout()
    
    # Save the plot
    plt.savefig('images/stress_level_per_week.png', dpi=300, bbox_inches='tight')
    print("Heatmap saved as 'images/stress_level_per_week.png'")
    
    # Print summary statistics
    print(f"\nSummary Statistics:")
    # Weeks with any data
    weeks_with_data = [i for i, row in enumerate(heatmap_array) if np.any(~np.isnan(row))]
    print(f"Total weeks with data: {len(weeks_with_data)}")
    if weeks_with_data:
        print(f"Week range: {weeks_with_data[0]+1} to {weeks_with_data[-1]+1}")
    
    # Calculate overall statistics
    valid_values = heatmap_array[~np.isnan(heatmap_array)]
    if len(valid_values) > 0:
        print(f"Overall stress level - Min: {valid_values.min():.1f}, Max: {valid_values.max():.1f}, Mean: {valid_values.mean():.1f}")
    
    # Show data availability by day of week
    print(f"\nData availability by day of week:")
    for i, day in enumerate(day_names):
        day_data = heatmap_array[:, i]
        valid_count = np.sum(~np.isnan(day_data))
        print(f"{day}: {valid_count}/{len(week_labels)} weeks ({valid_count/len(week_labels)*100:.1f}%)")
    
    return heatmap_array, week_labels, day_names


if __name__ == "__main__":
    heatmap_array, week_labels, day_names = create_stress_heatmap_12weeks()
    weeks_with_data = [i for i, row in enumerate(heatmap_array) if np.any(~np.isnan(row))]
    if weeks_with_data:
        print(f"Week data range: Week {weeks_with_data[0]+1} to Week {weeks_with_data[-1]+1}")
