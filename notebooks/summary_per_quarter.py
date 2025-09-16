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
from sqlalchemy.orm import sessionmaker
from vo2max_db import Vo2MaxActivities, engine

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

def get_vo2max_95th_percentile(activities_db, start_date, end_date):
    """Get the 95th percentile VO2Max value for running activities within the quarter's date range."""
    Session = sessionmaker(bind=engine)
    session = Session()

    results = session.query(Activities, Vo2MaxActivities) \
        .join(Activities, Activities.activity_id == Vo2MaxActivities.activity_id) \
        .filter(Activities.start_time >= start_date, Activities.start_time <= end_date) \
        .all()

    vo2_values = [vo2.vo2_max for activity, vo2 in results if vo2 is not None and vo2.vo2_max is not None]

    if not vo2_values:
        return np.nan

    return np.percentile(vo2_values, 95)

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
    """Create quarterly metrics table (raw, non-normalized) and print it instead of a heatmap."""
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
        vo2max_value = get_vo2max_95th_percentile(activities_db, start_date, end_date)
        quarter_metrics.append(vo2max_value)
        
        data_matrix.append(quarter_metrics)
        
        print(f"Q{quarter} metrics:", dict(zip(metrics.keys(), quarter_metrics)))
    
    # Build DataFrame for raw metrics (no normalization)
    df = pd.DataFrame(data_matrix, columns=list(metrics.keys()), index=[f'Q{q}' for q in quarters])
    print("\nQuarterly Metrics Table (raw):")
    print(df.to_string(index=True))
    
    # Optional: If you want to save this as a CSV for external viewing:
    # df.to_csv('images/quarterly_metrics_2025_raw.csv')
    
    # End of function
if __name__ == "__main__":
    create_quarterly_metrics_heatmap()
