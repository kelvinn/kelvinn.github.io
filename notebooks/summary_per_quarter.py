#!/usr/bin/env python3
"""
Create a heatmap showing quarterly health metrics for 2025:
- Resting Heart Rate (RHR): Median of daily minimum RHR
- Stress Levels: Median of daily average stress
- Steps: Average of daily steps
- Body Battery (max): Median of daily max body battery
- Intensity Minutes: Median of weekly averages
- VO2Max: 95th percentile of running activities
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
from datetime import datetime, timedelta
from collections import defaultdict

from garmindb import GarminConnectConfigManager
from garmindb.garmindb import (
    GarminDb, Activities, StepsActivities, ActivitiesDb
)
from garmindb.summarydb import DaysSummary, SummaryDb

# Set up seaborn theme
sns.set_theme(style="whitegrid")

def time_to_minutes(time_obj):
    """Convert time object to minutes."""
    if pd.isna(time_obj) or time_obj is None:
        return 0
    return time_obj.hour * 60 + time_obj.minute

def get_quarter_data(quarter, year=2025):
    """Get start and end dates for a quarter."""
    quarter_months = {
        1: (1, 3),
        2: (4, 6),
        3: (7, 9),
        4: (10, 12)
    }
    start_month, end_month = quarter_months[quarter]
    start_date = datetime(year, start_month, 1)
    if end_month == 12:
        end_date = datetime(year, end_month, 31)
    else:
        end_date = datetime(year, end_month + 1, 1) - timedelta(days=1)
    return start_date, end_date

def get_vo2max_max(activities_db, start_date, end_date):
    """Get maximum VO2Max value from running activities within a date range."""
    # Get running activities
    activities = Activities.get_by_sport(activities_db, "running")
    if not activities:
        return np.nan
    
    # Get corresponding VO2Max values from StepsActivities, filtering for 2025 and the specific quarter
    vo2max_values = []
    for activity in activities:
        # Check if activity is within the date range (2025 and specific quarter)
        if (hasattr(activity, 'start_time') and 
            activity.start_time and 
            start_date <= activity.start_time <= end_date):
            
            steps_activity = StepsActivities.get(activities_db, activity.activity_id)
            if steps_activity and steps_activity.vo2_max is not None:
                vo2max_values.append(steps_activity.vo2_max)
    
    if not vo2max_values:
        return np.nan
    
    return max(vo2max_values)

def calculate_weekly_intensity_minutes(data_period):
    """Calculate weekly averages of intensity minutes."""
    daily_minutes = []
    for entry in data_period:
        if entry.intensity_time is not None:
            daily_minutes.append({
                'date': pd.to_datetime(entry.day),
                'minutes': time_to_minutes(entry.intensity_time)
            })
    
    if not daily_minutes:
        return np.nan
    
    # Convert to DataFrame for weekly resampling
    df = pd.DataFrame(daily_minutes)
    df.set_index('date', inplace=True)
    weekly_avg = df['minutes'].resample('W').mean()
    
    return np.median(weekly_avg)

def create_quarterly_metrics_heatmap():
    """Create heatmap showing quarterly health metrics."""
    
    # Create images directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    # Initialize database connections
    gc_config = GarminConnectConfigManager()
    db_params_dict = gc_config.get_db_params()
    activities_db = ActivitiesDb(db_params_dict)
    garmin_db = GarminDb(db_params_dict)
    sum_db = SummaryDb(db_params_dict, False)
    
    # Define metrics and their descriptions
    metrics = {
        'RHR': 'Median daily minimum RHR',
        'Stress': 'Median daily average stress',
        'Steps': 'Average daily steps',
        'Body Battery': 'Median daily max body battery',
        'Intensity': 'Median of weekly intensity minutes',
        'VO2Max': 'Maximum value from running activities'
    }
    
    # Initialize data structure for quarters
    quarters = range(1, 5)
    data_matrix = []
    
    print("Processing quarterly data for 2025...")
    
    for quarter in quarters:
        start_date, end_date = get_quarter_data(quarter)
        print(f"\nProcessing Q{quarter} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        
        # Get data for the quarter
        data_period = DaysSummary.get_for_period(sum_db, start_date, end_date)
        
        quarter_metrics = []
        
        # RHR (Median of daily minimum)
        rhr_values = [day.rhr_min for day in data_period if day.rhr_min is not None]
        quarter_metrics.append(np.median(rhr_values) if rhr_values else np.nan)
        
        # Stress (Median of daily average)
        stress_values = [day.stress_avg for day in data_period if day.stress_avg is not None]
        quarter_metrics.append(np.median(stress_values) if stress_values else np.nan)
        
        # Steps (Average of daily sum)
        steps_values = [day.steps for day in data_period if day.steps is not None]
        quarter_metrics.append(np.mean(steps_values) if steps_values else np.nan)
        
        # Body Battery (Median of daily max)
        bb_values = [day.bb_max for day in data_period if day.bb_max is not None]
        quarter_metrics.append(np.median(bb_values) if bb_values else np.nan)
        
        # Intensity Minutes (Median of weekly averages)
        intensity_median = calculate_weekly_intensity_minutes(data_period)
        quarter_metrics.append(intensity_median)
        
        # VO2Max (maximum value from running activities)
        vo2max_value = get_vo2max_max(activities_db, start_date, end_date)
        quarter_metrics.append(vo2max_value)
        
        data_matrix.append(quarter_metrics)
        
        print(f"Q{quarter} metrics:", dict(zip(metrics.keys(), quarter_metrics)))
    
    # Convert to numpy array
    data_array = np.array(data_matrix)
    
    # Create the heatmap
    plt.figure(figsize=(12, 8))
    
    # Create heatmap with custom formatting
    ax = sns.heatmap(data_array,
                     xticklabels=list(metrics.keys()),
                     yticklabels=[f'Q{q}' for q in quarters],
                     annot=True,
                     fmt='.1f',
                     cmap='YlOrRd',
                     cbar_kws={'label': 'Value'},
                     linewidths=0.5)
    
    plt.title('Quarterly Health Metrics (2025)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Metrics', fontsize=12)
    plt.ylabel('Quarter', fontsize=12)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Add metrics descriptions as footnote
    footnote = "Metrics Calculation Methods:\n"
    for metric, desc in metrics.items():
        footnote += f"• {metric}: {desc}\n"
    
    plt.figtext(0.1, -0.2, footnote, wrap=True, fontsize=8)
    
    # Adjust layout to prevent label cutoff and accommodate footnote
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.3)  # Make room for footnote
    
    # Save the plot
    plt.savefig('images/quarterly_metrics_2025.png', dpi=300, bbox_inches='tight')
    print("\nHeatmap saved as 'images/quarterly_metrics_2025.png'")
    
    # Print summary statistics for each metric
    print("\nSummary Statistics:")
    for i, metric in enumerate(metrics.keys()):
        values = data_array[:, i]
        valid_values = values[~np.isnan(values)]
        if len(valid_values) > 0:
            print(f"\n{metric}:")
            print(f"  Min: {np.min(valid_values):.1f}")
            print(f"  Max: {np.max(valid_values):.1f}")
            print(f"  Mean: {np.mean(valid_values):.1f}")
            print(f"  Available quarters: {len(valid_values)}/4")

if __name__ == "__main__":
    create_quarterly_metrics_heatmap()