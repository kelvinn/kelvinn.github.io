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

# Define start date (2019) and end date (current)
start_date = datetime(2019, 1, 1)
end_date = datetime.now()

print(f"Querying sleep data from {start_date.date()} to {end_date.date()}...")

# Query all sleep data for the period
sleep_data = Sleep.get_for_period(garmin_db, start_date, end_date, Sleep)

print(f"Found {len(sleep_data)} sleep records")

# Group sleep scores by month
monthly_data = defaultdict(list)

for sleep_record in sleep_data:
    # Get the sleep score and date
    sleep_score = getattr(sleep_record, 'score', None)
    sleep_date = getattr(sleep_record, 'day')
    
    if sleep_score is not None:
        # Create month key (YYYY-MM format)
        month_key = sleep_date.strftime('%Y-%m')
        monthly_data[month_key].append(sleep_score)

# Sort months chronologically
sorted_months = sorted(monthly_data.keys())

# Calculate monthly averages and standard deviations
months = []
averages = []
std_devs = []

for month in sorted_months:
    scores = monthly_data[month]
    if len(scores) > 0:
        months.append(month)
        averages.append(np.mean(scores))
        std_devs.append(np.std(scores))

print(f"Calculated statistics for {len(months)} months")

# Create the plot
plt.figure(figsize=(14, 8))

# Convert month strings to datetime for plotting
month_dates = [datetime.strptime(month, '%Y-%m') for month in months]

# Create the lineplot with error bars for standard deviation
plt.errorbar(month_dates, averages, yerr=std_devs, 
             fmt='o-', linewidth=2, markersize=6, 
             capsize=5, capthick=2, alpha=0.8,
             color='steelblue', ecolor='lightblue')

# Fill area between average +/- std dev for better visualization
upper_bound = [avg + std for avg, std in zip(averages, std_devs)]
lower_bound = [avg - std for avg, std in zip(averages, std_devs)]
plt.fill_between(month_dates, lower_bound, upper_bound, alpha=0.3, color='lightblue')

# Customize the plot
plt.title('Average Sleep Score per Month (2023-Present)', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Average Sleep Score', fontsize=12, fontweight='bold')

# Format x-axis to show years and months clearly
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=6))
plt.xticks(rotation=45, ha='right')

# Add grid for better readability
plt.grid(True, alpha=0.3)

# Set y-axis limits with some padding
min_score = min(lower_bound) - 5
max_score = max(upper_bound) + 5
plt.ylim(min_score, max_score)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Save the plot
plt.savefig('images/average_sleep_score_per_month.png', dpi=300, bbox_inches='tight')
print("Plot saved as 'images/average_sleep_score_per_month.png'")

# Display the plot
plt.show()

# Print some summary statistics
print(f"\nSummary Statistics:")
print(f"Total months with data: {len(months)}")
print(f"Overall average sleep score: {np.mean(averages):.1f}")
print(f"Overall standard deviation: {np.mean(std_devs):.1f}")
print(f"Highest monthly average: {max(averages):.1f} ({months[np.argmax(averages)]})")
print(f"Lowest monthly average: {min(averages):.1f} ({months[np.argmin(averages)]})")
