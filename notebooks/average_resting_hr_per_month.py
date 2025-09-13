import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pandas as pd
import seaborn as sns
import os
from datetime import datetime, timedelta
from collections import defaultdict

from garmindb import GarminConnectConfigManager
from garmindb.garmindb import GarminSummaryDb, DaysSummary, MonitoringDb, MonitoringHeartRate, Sleep, GarminDb, RestingHeartRate
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

print(f"Querying resting heart rate data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")

# Query resting heart rate data
hr_data = RestingHeartRate.get_for_period(garmin_db, start_date, end_date, RestingHeartRate)

print(f"Found {len(hr_data)} heart rate records")

# Group data by month
monthly_data = defaultdict(list)

for hr_record in hr_data:
    # Get the date and resting heart rate
    record_date = hr_record.day
    resting_hr = hr_record.resting_heart_rate
    
    if resting_hr is not None:
        # Create month key (YYYY-MM format)
        month_key = record_date.strftime('%Y-%m')
        monthly_data[month_key].append(resting_hr)

# Sort months chronologically
sorted_months = sorted(monthly_data.keys())

# Calculate monthly averages and standard deviations
monthly_averages = []
monthly_stds = []
month_labels = []

for month in sorted_months:
    hr_values = monthly_data[month]
    if len(hr_values) > 0:
        avg_hr = np.mean(hr_values)
        std_hr = np.std(hr_values)
        
        monthly_averages.append(avg_hr)
        monthly_stds.append(std_hr)
        month_labels.append(month)
        
        print(f"{month}: {len(hr_values)} records, avg={avg_hr:.1f}, std={std_hr:.1f}")

# Create the line plot
plt.figure(figsize=(15, 8))

# Convert month labels to datetime for proper x-axis formatting
month_dates = [datetime.strptime(month, '%Y-%m') for month in month_labels]

# Create the line plot with error bars
plt.errorbar(month_dates, monthly_averages, yerr=monthly_stds, 
             marker='o', linewidth=2, markersize=6, capsize=5, capthick=2,
             color='#2E86AB', ecolor='#A23B72', alpha=0.8)

# Customize the plot
plt.title('Average Resting Heart Rate per Month (2019-Present)', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Resting Heart Rate (BPM)', fontsize=12, fontweight='bold')

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
plt.savefig('images/average_resting_hr_per_month.png', dpi=300, bbox_inches='tight')
print("Line plot saved as 'images/average_resting_hr_per_month.png'")

# Display the plot
plt.show()

print(f"\nSummary:")
print(f"Total months with data: {len(monthly_averages)}")
print(f"Overall average resting HR: {np.mean(monthly_averages):.1f} BPM")
print(f"Overall standard deviation: {np.std(monthly_averages):.1f} BPM")
