#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

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

    # Define date range for Q3 2025
    start_date = datetime(2025, 7, 1)
    end_date = datetime(2025, 9, 30)

    print(f"Querying health metrics for Q3 2025 ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})...")

    # Query daily summaries
    data_period = DaysSummary.get_for_period(sum_db, start_date, end_date, DaysSummary)
    print(f"Found {len(data_period)} days of data")

    # Create a list to store daily data
    daily_data = []

    for entry in data_period:
        try:
            # Convert activity times to minutes
            mod_time = getattr(entry, 'moderate_activity_time', None)
            vig_time = getattr(entry, 'vigorous_activity_time', None)
            sleep_val = getattr(entry, 'sleep_avg', None)
            
            # Convert times to minutes
            mod_minutes = time_to_minutes(mod_time) if mod_time else 0.0
            vig_minutes = time_to_minutes(vig_time) if vig_time else 0.0
            sleep_minutes = time_to_minutes(sleep_val) if sleep_val else 0.0
            
            data = {
                'date': entry.day,
                'hr_min': float(entry.hr_min) if hasattr(entry, 'hr_min') and entry.hr_min is not None else 0.0,
                'hr_max': float(entry.hr_max) if hasattr(entry, 'hr_max') and entry.hr_max is not None else 0.0,
                'stress_avg': float(entry.stress_avg) if hasattr(entry, 'stress_avg') and entry.stress_avg is not None else 0.0,
                'floors': float(entry.floors) if hasattr(entry, 'floors') and entry.floors is not None else 0.0,
                'sleep_score': sleep_minutes,
                'moderate_activity_time': float(mod_minutes),
                'vigorous_activity_time': float(vig_minutes)
            }
            daily_data.append(data)
        except (ValueError, TypeError) as e:
            print(f"Skipping entry for {entry.day}: {str(e)}")

    if not daily_data:
        print("No data found for the specified period")
        return

    # Convert to DataFrame
    df = pd.DataFrame(daily_data)
    df.set_index('date', inplace=True)

    # List of metrics for correlation
    metrics = [col for col in ['hr_min', 'hr_max', 'stress_avg', 'floors', 'sleep_score', 
                              'moderate_activity_time', 'vigorous_activity_time'] 
              if col in df.columns]

    # Calculate correlation matrix
    correlation_matrix = df[metrics].corr()

    # Create heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, 
                annot=True,
                cmap='RdYlBu_r',
                vmin=-1, vmax=1,
                center=0,
                square=True,
                fmt='.2f',
                linewidths=0.5,
                cbar_kws={"shrink": .8})

    plt.title('Health Metrics Correlation Matrix - Q3 2025\n', fontsize=16, pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    # Adjust layout
    plt.tight_layout()

    # Save plot
    os.makedirs('images', exist_ok=True)
    plt.savefig('images/correlation_matrix.png', dpi=300, bbox_inches='tight')
    print("Correlation matrix saved as 'images/correlation_matrix.png'")

    # Print summary statistics
    print("\nData Summary:")
    print(f"Total days analyzed: {len(df)}")
    print("\nMissing values per metric:")
    print(df[metrics].isnull().sum())

    # Show strongest correlations
    print("\nTop 10 strongest correlations:")
    correlations = []
    for i in range(len(metrics)):
        for j in range(i+1, len(metrics)):
            corr = correlation_matrix.iloc[i, j]
            if not pd.isna(corr):
                correlations.append((metrics[i], metrics[j], abs(corr), corr))

    correlations.sort(key=lambda x: x[2], reverse=True)
    for metric1, metric2, abs_corr, corr in correlations[:10]:
        print(f"{metric1} vs {metric2}: {corr:.3f}")

if __name__ == '__main__':
    create_correlation_matrix()
