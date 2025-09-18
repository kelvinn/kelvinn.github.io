import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pandas as pd
import seaborn as sns
import os
from datetime import datetime, timedelta
from collections import defaultdict

from garmindb import GarminConnectConfigManager
from garmindb.garmindb import GarminSummaryDb, DaysSummary, MonitoringDb, MonitoringHeartRate, Sleep, GarminDb
from garmindb.summarydb import DaysSummary, SummaryDb

# Set up seaborn theme
sns.set_theme(style="whitegrid")

# Initialize database connection
gc_config = GarminConnectConfigManager()
db_params_dict = gc_config.get_db_params()
garmin_db = GarminDb(db_params_dict)

# Define date range starting from 2019
start_date = datetime(2019, 1, 1)
end_date = datetime.now()

print(f"Querying active calories data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")

# Query daily summary data for active calories
sum_db = SummaryDb(db_params_dict, False)
data_period = DaysSummary.get_for_period(sum_db, start_date, end_date, DaysSummary)

print(f"Found {len(data_period)} days of data for the period")

# Filter data with active calories values
calories_data = [entry for entry in data_period if entry.calories_avg is not None]
print(f"Found {len(calories_data)} days with active calories data")

if not calories_data:
    print("No active calories data available for the period")
    exit(1)

# Group data by month
monthly_data = defaultdict(list)

for entry in calories_data:
    # Get the date and active calories
    record_date = entry.day
    calories = entry.calories_avg
    
    if calories is not None:
        # Create month key (YYYY-MM format)
        month_key = record_date.strftime('%Y-%m')
        monthly_data[month_key].append(calories)

# Sort months chronologically
sorted_months = sorted(monthly_data.keys())

# Calculate monthly averages and standard deviations
monthly_averages = []
monthly_stds = []
month_labels = []
export_rows = []

for month in sorted_months:
    calories_values = monthly_data[month]
    if len(calories_values) > 0:
        avg_calories = np.mean(calories_values)
        std_calories = np.std(calories_values)
        
        monthly_averages.append(avg_calories)
        monthly_stds.append(std_calories)
        month_labels.append(month)
        
        print(f"{month}: {len(calories_values)} records, avg={avg_calories:.1f}, std={std_calories:.1f}")

# Prepare export for CSV (insert)
export_rows = []
for month in sorted_months:
    calories_values = monthly_data[month]
    if len(calories_values) > 0:
        year = int(month.split('-')[0])
        mon = int(month.split('-')[1])
        export_rows.append({'year': year, 'month': mon, 'average_active_calories': float(np.mean(calories_values)), 'count': len(calories_values), 'std_dev': float(np.std(calories_values))})

df_export = pd.DataFrame(export_rows)
os.makedirs('data', exist_ok=True)
csv_path = os.path.join('data', 'average_active_calories_per_month.csv')
df_export.to_csv(csv_path, index=False)
print(f"Exported monthly active calories data to {csv_path}")

# Create the line plot
plt.figure(figsize=(15, 8))

# Convert month labels to datetime for proper x-axis formatting
month_dates = [datetime.strptime(month, '%Y-%m') for month in month_labels]

# Create the line plot with error bars
plt.errorbar(month_dates, monthly_averages, yerr=monthly_stds, 
             marker='o', linewidth=2, markersize=6, capsize=5, capthick=2,
             color='#2E86AB', ecolor='#A23B72', alpha=0.8)

# Customize the plot
plt.title('Average Active Calories per Month (2019-Present)', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Active Calories', fontsize=12, fontweight='bold')

# Format x-axis to show months nicely
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=3))  # Show every 3 months
plt.xticks(rotation=45)

# Add grid for better readability
plt.grid(True, alpha=0.3)

# Add some styling
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Save the plot
plt.savefig('images/average_active_calories_per_month.png', dpi=300, bbox_inches='tight')
print("Line plot saved as 'images/average_active_calories_per_month.png'")

print(f"\nSummary:")
print(f"Total months with data: {len(monthly_averages)}")
print(f"Overall average active calories: {np.mean(monthly_averages):.1f}")
print(f"Overall standard deviation: {np.std(monthly_averages):.1f}")
