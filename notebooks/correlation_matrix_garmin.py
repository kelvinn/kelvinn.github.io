#!/usr/bin/env python3

"""
Correlation Matrix Generator for Garmin Health Data

Technical Implementation Guide:
1. Data Source:
   - Uses GarminDB SQLite database (install garmindb package)
   - Primary data from DaysSummary table in SummaryDb

2. Key Dependencies:
   - pandas: Data manipulation and correlation calculations
   - seaborn: Heatmap visualization
   - matplotlib: Plot customization
   - numpy: Numerical operations
   - pickle: Data serialization

3. Implementation Steps:
   a. Database Connection:
      - Use GarminConnectConfigManager for db_params
      - Connect to SummaryDb for daily metrics
   
   b. Data Processing:
      - Query date range using DaysSummary.get_for_period()
      - Convert time objects to minutes using time_to_minutes()
      - Group metrics by category (heart rate, activity, recovery, etc.)
   
   c. Visualization:
      - Create correlation matrix using pandas df.corr()
      - Generate heatmap with seaborn
      - Customize using matplotlib (font sizes, rotation, padding)

4. Metric Categories:
   - Heart Rate: hr_min, hr_max, rhr_min
   - Recovery: bb_max, bb_min, sleep_avg
   - Activity: steps, floors, moderate/vigorous activity
   - Energy: calories_active_avg
   - Health: stress_avg, weight_avg

5. Output Files:
   a. Correlation Data:
      - 'data/correlation_data.pkl': Pickle file containing:
         * correlation_matrix: pandas DataFrame
         * metrics: list of metric names
         * date_range: start and end dates
      - 'data/correlation_matrix.csv': Human-readable CSV format
   
   b. Visualization:
      - 'images/correlation_matrix.png': Heatmap visualization

6. Using the Saved Data:
   Example code to load and use the correlation data:
   ```python
   import pickle
   
   # Load the correlation data
   with open('data/correlation_data.pkl', 'rb') as f:
       corr_data = pickle.load(f)
   
   # Access components
   matrix = corr_data['matrix']
   metrics = corr_data['metrics']
   date_range = corr_data['date_range']
   ```

7. Usage:
   - Ensure GarminDB is populated with recent data
   - Adjust date range as needed (default: Q3 2025)
   - Results saved in both data/ and images/ directories
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pickle
from datetime import datetime

from garmindb import GarminConnectConfigManager
from garmindb.summarydb import DaysSummary, SummaryDb
from garmindb.garmindb import Sleep

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
                'rhr_min': float(entry.rhr_min) if hasattr(entry, 'rhr_min') and entry.rhr_min is not None else 0.0,
                'stress_avg': float(entry.stress_avg) if hasattr(entry, 'stress_avg') and entry.stress_avg is not None else 0.0,
                'floors': float(entry.floors) if hasattr(entry, 'floors') and entry.floors is not None else 0.0,
                'weight_avg': float(entry.weight_avg) if hasattr(entry, 'weight_avg') and entry.weight_avg is not None else 0.0,
                'sleep_avg': float(time_to_minutes(entry.sleep_avg)) if hasattr(entry, 'sleep_avg') and entry.sleep_avg is not None else 0.0,
                'calories_active_avg': float(entry.calories_active_avg) if hasattr(entry, 'calories_active_avg') and entry.calories_active_avg is not None else 0.0,
                'bb_max': float(entry.bb_max) if hasattr(entry, 'bb_max') and entry.bb_max is not None else 0.0,
                'bb_min': float(entry.bb_min) if hasattr(entry, 'bb_min') and entry.bb_min is not None else 0.0,
                'moderate_activity_time': float(mod_minutes),
                'vigorous_activity_time': float(vig_minutes),
                'steps': float(entry.steps) if hasattr(entry, 'steps') and entry.steps is not None else 0.0
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

    # List of metrics for correlation, grouped by category
    metric_groups = [
        # Heart rate metrics
        'hr_min', 'hr_max', 'rhr_min',
        # Recovery metrics
        'bb_max', 'bb_min', 'sleep_avg',
        # Activity metrics
        'steps', 'floors', 'moderate_activity_time', 'vigorous_activity_time',
        # Energy metrics
        'calories_active_avg',
        # Other health metrics
        'stress_avg', 'weight_avg'
    ]
    metrics = [col for col in metric_groups if col in df.columns]

    # Calculate correlation matrix
    correlation_matrix = df[metrics].corr()

    # Create heatmap with larger size for more metrics
    plt.figure(figsize=(15, 13))
    
    # Create heatmap
    sns.heatmap(correlation_matrix, 
                annot=True,
                cmap='RdYlBu_r',
                vmin=-1, vmax=1,
                center=0,
                square=True,
                fmt='.2f',
                linewidths=0.5,
                cbar_kws={"shrink": .8},
                annot_kws={"size": 8})

    plt.title('Garmin Health Metrics Correlation Matrix\nQ3 2025 Analysis', fontsize=16, pad=20)
    
    # Rotate labels for better readability
    plt.xticks(rotation=45, ha='right', fontsize=11)
    plt.yticks(rotation=0, fontsize=11)
    
    # Adjust layout to prevent label cutoff
    plt.subplots_adjust(left=0.2, bottom=0.2)
    
    # Add legend for interpretation
    plt.figtext(0.02, 0.02, 
                'Color intensity indicates correlation strength\n' +
                'Blue: positive correlation | Red: negative correlation\n' +
                'Range: -1 (perfect negative) to 1 (perfect positive)',
                fontsize=10, alpha=0.7)

    # Adjust layout
    plt.tight_layout()

    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('images', exist_ok=True)

    # Save correlation data
    correlation_data = {
        'matrix': correlation_matrix,
        'metrics': metrics,
        'date_range': {'start': start_date, 'end': end_date}
    }
    with open('data/correlation_data.pkl', 'wb') as f:
        pickle.dump(correlation_data, f)
    print("Correlation data saved as 'data/correlation_data.pkl'")

    # Save as CSV for human readability
    correlation_matrix.to_csv('data/correlation_matrix.csv')
    print("Correlation matrix also saved as 'data/correlation_matrix.csv'")

    # Save plot
    plt.savefig('images/correlation_matrix.png', dpi=300, bbox_inches='tight')
    print("Correlation matrix plot saved as 'images/correlation_matrix.png'")

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
