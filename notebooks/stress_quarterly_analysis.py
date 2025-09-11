#!/usr/bin/env python3
"""
Create a heatmap showing average stress level per day of the week for each quarter of 2025.
Quarters on y-axis, days of week on x-axis, with average column for each quarter.
"""

import matplotlib.pyplot as plt
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

def create_quarterly_stress_heatmap():
    """Create a heatmap showing average stress levels per day of week for each quarter of 2025."""
    
    # Create images directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    # Define quarters for 2025
    quarters = {
        'Q1': {'months': [1, 2, 3], 'name': 'Q1 (Jan-Mar)'},
        'Q2': {'months': [4, 5, 6], 'name': 'Q2 (Apr-Jun)'},
        'Q3': {'months': [7, 8, 9], 'name': 'Q3 (Jul-Sep)'},
        'Q4': {'months': [10, 11, 12], 'name': 'Q4 (Oct-Dec)'}
    }
    
    print("Creating quarterly stress analysis for 2025...")
    
    # Initialize Garmin database connection
    gc_config = GarminConnectConfigManager()
    db_params_dict = gc_config.get_db_params()
    sum_db = SummaryDb(db_params_dict, False)
    
    # Day names for x-axis labels
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # Create the heatmap data matrix
    # Rows: quarters, Columns: days of week + average column
    heatmap_matrix = []
    quarter_labels = []
    
    for quarter_key, quarter_info in quarters.items():
        print(f"\nProcessing {quarter_info['name']}...")
        
        # Collect all stress data for this quarter
        quarter_stress_data = {}
        
        for month in quarter_info['months']:
            # Get start and end dates for the month
            start_date = datetime(2025, month, 1).date()
            if month == 12:
                end_date = datetime(2026, 1, 1).date() - timedelta(days=1)
            else:
                end_date = datetime(2025, month + 1, 1).date() - timedelta(days=1)
            
            print(f"  Month {month}: {start_date} to {end_date}")
            
            # Query stress data for this month
            start_ts = datetime.combine(start_date, datetime.min.time())
            end_ts = datetime.combine(end_date, datetime.max.time())
            
            data_period = DaysSummary.get_for_period(sum_db, start_ts, end_ts, DaysSummary)
            
            # Filter data with stress values
            month_stress_data = [entry for entry in data_period if entry.stress_avg is not None]
            print(f"    Found {len(month_stress_data)} days with stress data")
            
            # Group by day of week
            for entry in month_stress_data:
                day_of_week = entry.day.weekday()  # 0=Monday, 6=Sunday
                
                if day_of_week not in quarter_stress_data:
                    quarter_stress_data[day_of_week] = []
                
                quarter_stress_data[day_of_week].append(entry.stress_avg)
        
        # Calculate average stress for each day of week for this quarter
        quarter_values = []
        for day in range(7):  # Monday to Sunday
            if day in quarter_stress_data and quarter_stress_data[day]:
                avg_stress = np.mean(quarter_stress_data[day])
                quarter_values.append(avg_stress)
            else:
                quarter_values.append(np.nan)  # No data for this day
        
        # Calculate overall average for the quarter
        all_quarter_values = []
        for day_values in quarter_stress_data.values():
            all_quarter_values.extend(day_values)
        
        if all_quarter_values:
            quarter_avg = np.mean(all_quarter_values)
            quarter_values.append(quarter_avg)
        else:
            quarter_values.append(np.nan)
        
        heatmap_matrix.append(quarter_values)
        quarter_labels.append(quarter_info['name'])
        
        # Print summary for this quarter
        valid_values = [v for v in quarter_values[:-1] if not np.isnan(v)]
        if valid_values:
            print(f"  Average stress by day: {[f'{v:.1f}' if not np.isnan(v) else 'N/A' for v in quarter_values[:-1]]}")
            print(f"  Overall quarter average: {quarter_values[-1]:.1f}")
        else:
            print(f"  No data available for this quarter")
    
    # Convert to numpy array
    heatmap_array = np.array(heatmap_matrix)
    
    # Create column labels (days + average)
    column_labels = day_names + ['Avg']
    
    # Create the heatmap
    fig_height = max(8, len(quarters) * 1.5)
    plt.figure(figsize=(12, fig_height))
    
    # Create heatmap
    ax = sns.heatmap(heatmap_array,
                     xticklabels=column_labels,
                     yticklabels=quarter_labels,
                     annot=True,
                     fmt='.1f',
                     cmap='YlOrRd',
                     cbar_kws={'label': 'Average Stress Level'},
                     linewidths=0.5,
                     square=False,
                     cbar=True,
                     mask=np.isnan(heatmap_array))
    
    plt.title('Average Stress Level per Day of Week by Quarter (2025)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Day of Week', fontsize=14)
    plt.ylabel('Quarter', fontsize=14)
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('images/stress_level_per_day.png', dpi=300, bbox_inches='tight')
    print(f"\nHeatmap saved as 'images/stress_level_per_day.png'")
    
    plt.show()
    
    # Print summary statistics
    print(f"\nSummary Statistics:")
    print(f"Quarters analyzed: {len(quarters)}")
    
    # Calculate overall statistics
    valid_values = heatmap_array[~np.isnan(heatmap_array)]
    if len(valid_values) > 0:
        print(f"Overall stress level - Min: {valid_values.min():.1f}, Max: {valid_values.max():.1f}, Mean: {valid_values.mean():.1f}")
    
    # Show data availability by quarter
    print(f"\nData availability by quarter:")
    for i, quarter in enumerate(quarter_labels):
        quarter_data = heatmap_array[i, :-1]  # Exclude average column
        valid_count = np.sum(~np.isnan(quarter_data))
        print(f"{quarter}: {valid_count}/7 days with data ({valid_count/7*100:.1f}%)")
    
    return heatmap_array, quarter_labels, column_labels

if __name__ == "__main__":
    create_quarterly_stress_heatmap()
