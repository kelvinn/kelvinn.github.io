#!/usr/bin/env python3
"""
Create a heatmap showing daily stress level per week for the previous 12 weeks from today.
Week of year on vertical axis, day of week on horizontal axis.
Cells have vertical padding for better visualization.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
import datetime as dt
import pandas as pd
import seaborn as sns
import os
from datetime import datetime, timedelta

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
    end_date = datetime.now().date()
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
    
    # Create a dictionary to store data by week and day
    # Structure: {week_number: {day_of_week: stress_value}}
    week_data = {}
    
    for entry in stress_data:
        # Get week number of the year
        week_number = entry.day.isocalendar()[1]  # ISO week number
        day_of_week = entry.day.weekday()  # 0=Monday, 6=Sunday
        
        if week_number not in week_data:
            week_data[week_number] = {}
        
        week_data[week_number][day_of_week] = entry.stress_avg
    
    # Get all week numbers and sort them
    week_numbers = sorted(week_data.keys())
    print(f"Week numbers found: {week_numbers}")
    
    # Create the heatmap data matrix
    # Rows: weeks, Columns: days of week (Monday=0 to Sunday=6)
    heatmap_matrix = []
    week_labels = []
    
    for week_num in week_numbers:
        week_values = []
        for day in range(7):  # Monday to Sunday
            if day in week_data[week_num]:
                week_values.append(week_data[week_num][day])
            else:
                week_values.append(np.nan)  # No data for this day
        
        heatmap_matrix.append(week_values)
        week_labels.append(f"Week {week_num}")
    
    # Convert to numpy array
    heatmap_array = np.array(heatmap_matrix)
    
    # Day names for x-axis labels
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # Create the heatmap with vertical padding
    # Use a larger figure size and adjust the aspect ratio for vertical padding
    fig_height = max(12, len(week_numbers) * 1.2)  # Increased height for more vertical padding
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
    
    # Add vertical padding by adjusting the aspect ratio
    # This creates more vertical space between rows
    ax.set_aspect('auto')
    
    # Add extra vertical padding by adjusting the spacing
    # Increase the spacing between cells
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
    
    plt.show()
    
    # Print summary statistics
    print(f"\nSummary Statistics:")
    print(f"Total weeks with data: {len(week_numbers)}")
    print(f"Week range: {min(week_numbers)} to {max(week_numbers)}")
    
    # Calculate overall statistics
    valid_values = heatmap_array[~np.isnan(heatmap_array)]
    if len(valid_values) > 0:
        print(f"Overall stress level - Min: {valid_values.min():.1f}, Max: {valid_values.max():.1f}, Mean: {valid_values.mean():.1f}")
    
    # Show data availability by day of week
    print(f"\nData availability by day of week:")
    for i, day in enumerate(day_names):
        day_data = heatmap_array[:, i]
        valid_count = np.sum(~np.isnan(day_data))
        print(f"{day}: {valid_count}/{len(week_numbers)} weeks ({valid_count/len(week_numbers)*100:.1f}%)")
    
    return heatmap_array, week_numbers, day_names

if __name__ == "__main__":
    create_stress_heatmap_12weeks()
