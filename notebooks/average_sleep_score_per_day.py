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

# Initialize database connection
gc_config = GarminConnectConfigManager()
db_params_dict = gc_config.get_db_params()
garmin_db = GarminDb(db_params_dict)

# Define quarters for 2025
quarters = {
    'Q1': (datetime(2025, 1, 1), datetime(2025, 3, 31)),
    'Q2': (datetime(2025, 4, 1), datetime(2025, 6, 30)),
    'Q3': (datetime(2025, 7, 1), datetime(2025, 9, 30)),
    'Q4': (datetime(2025, 10, 1), datetime(2025, 12, 31))
}

# Day names in order (Monday to Sunday)
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Initialize data structure
quarter_data = {}

# First, let's examine the sleep data structure to find the correct attributes
print("Examining sleep data structure...")
start_ts = datetime(2025, 1, 1)
end_ts = datetime(2025, 1, 7)  # Just get a week to examine structure
sample_sleep_data = Sleep.get_for_period(garmin_db, start_ts, end_ts, Sleep)

if sample_sleep_data:
    sample_sleep = sample_sleep_data[0]
    print(f"Sample sleep record attributes: {[attr for attr in dir(sample_sleep) if not attr.startswith('_')]}")
    
    # Use the correct attributes based on the output
    date_attr = 'day'  # datetime.date object
    score_attr = 'score'  # int value
    
    print(f"Using date attribute: {date_attr}")
    print(f"Using score attribute: {score_attr}")
else:
    print("No sleep data found for 2025")
    exit(1)

# Query sleep data for each quarter
for quarter_name, (start_date, end_date) in quarters.items():
    print(f"Querying sleep data for {quarter_name} 2025...")
    
    # Get sleep data for the quarter
    sleep_data = Sleep.get_for_period(garmin_db, start_date, end_date, Sleep)
    
    # Initialize day of week data
    day_scores = {day: [] for day in day_names}
    
    # Process each sleep record
    for sleep_record in sleep_data:
        sleep_score = getattr(sleep_record, score_attr, None)
        if sleep_score is not None:
            # Get the day of the week (0=Monday, 6=Sunday)
            sleep_date = getattr(sleep_record, date_attr)
            day_of_week = sleep_date.weekday()
            day_name = day_names[day_of_week]
            day_scores[day_name].append(sleep_score)
    
    # Calculate averages for each day
    quarter_data[quarter_name] = {}
    for day in day_names:
        if day_scores[day]:
            quarter_data[quarter_name][day] = np.mean(day_scores[day])
        else:
            quarter_data[quarter_name][day] = np.nan
    
    print(f"Found {len(sleep_data)} sleep records for {quarter_name}")

print("Sleep data query completed.")

# Create DataFrame for heatmap - only include quarters with data
df_data = []
quarter_labels = []
for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
    row = [quarter_data[quarter][day] for day in day_names]
    # Calculate weekly average (excluding NaN values)
    weekly_avg = np.nanmean(row)
    
    # Only include quarters that have at least some data (not all NaN)
    if not np.isnan(weekly_avg):
        row.append(weekly_avg)
        df_data.append(row)
        quarter_labels.append(quarter)

# Create DataFrame
columns = day_names + ['Weekly Average']
df = pd.DataFrame(df_data, index=quarter_labels, columns=columns)

print("DataFrame created:")
print(df)

# Create the heatmap
plt.figure(figsize=(12, 8))

# Create custom colormap
cmap = sns.cm.rocket_r

# Create the heatmap
ax = sns.heatmap(df, 
                 annot=True, 
                 fmt='.1f', 
                 cmap=cmap,
                 cbar_kws={'label': 'Average Sleep Score'},
                 linewidths=0.5,
                 linecolor='white',
                 xticklabels=columns,
                 yticklabels=True)

# Customize the plot
plt.title('Average Sleep Score per Day of Week by Quarter (2025)', fontsize=16, fontweight='bold', pad=40)
plt.xlabel('Day of Week', fontsize=12, fontweight='bold')
plt.ylabel('Quarter', fontsize=12, fontweight='bold')

# Rotate x-axis labels for better readability
plt.xticks(rotation=90, ha='center')

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Save the plot
plt.savefig('images/sleep_score_per_day.png', dpi=300, bbox_inches='tight')
print("Heatmap saved as 'images/sleep_score_per_day.png'")

# Display the plot
plt.show()