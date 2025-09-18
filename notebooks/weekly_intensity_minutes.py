import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

from garmindb import GarminConnectConfigManager
from garmindb.summarydb import DaysSummary, SummaryDb

# Set up seaborn theme
sns.set_theme(style="whitegrid")

# Initialize database connection
gc_config = GarminConnectConfigManager()
db_params_dict = gc_config.get_db_params()

# Get data for 2025
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

# Query daily summaries
sum_db = SummaryDb(db_params_dict, False)
data_period = DaysSummary.get_for_period(sum_db, start_date, end_date, DaysSummary)

# Filter for days with intensity data
intensity_data = [entry for entry in data_period if entry.intensity_time is not None]
print(f"Found {len(intensity_data)} days with intensity data in 2025")

# Convert to DataFrame
df = pd.DataFrame([vars(s) for s in intensity_data])

# Convert time objects to minutes
def time_to_minutes(time_obj):
    if pd.isna(time_obj) or time_obj is None:
        return 0
    return time_obj.hour * 60 + time_obj.minute

# Calculate total intensity minutes (vigorous minutes are doubled)
df['date'] = pd.to_datetime(df['day'])
df['moderate_mins'] = df['moderate_activity_time'].apply(time_to_minutes)
df['vigorous_mins'] = df['vigorous_activity_time'].apply(time_to_minutes)
df['intensity_minutes'] = df['moderate_mins'] + 2 * df['vigorous_mins']

# Resample by week
df.set_index('date', inplace=True)
# Export per-week data to CSV
weekly_summary = df['intensity_minutes'].resample('W-SUN').sum()

export_df = weekly_summary.reset_index()
export_df.columns = ['week_end', 'intensity_minutes']
os.makedirs('data', exist_ok=True)
csv_path = os.path.join('data', 'weekly_intensity_minutes_per_week.csv')
export_df.to_csv(csv_path, index=False)
print(f"Exported weekly intensity data to {csv_path}")

# Calculate averages and stats
average_weekly_intensity = weekly_summary.mean()
q3_start = pd.Timestamp('2025-07-01')
q3_end = pd.Timestamp('2025-09-30')
q3_data = weekly_summary.loc[q3_start:q3_end]
q3_average = q3_data.mean()
weeks_above_target = len(weekly_summary[weekly_summary >= 800])
q3_weeks_above_target = len(q3_data[q3_data >= 800])

print(f"Overall average weekly intensity minutes: {average_weekly_intensity:.2f}")
print(f"Q3 average weekly intensity minutes: {q3_average:.2f}")
print(f"Weeks above target (800) in Q3: {q3_weeks_above_target} out of {len(q3_data)}")

# Create plot
plt.figure(figsize=(16, 6))
weekly_summary.plot(kind='bar', width=0.8, color='#69b3a2', align='center')
plt.axhline(y=800, color='r', linestyle='--', label='Weekly Target (800)')
plt.axhline(y=average_weekly_intensity, color='g', linestyle='--', label=f'Weekly Average ({average_weekly_intensity:.0f})')

# Format plot
plt.title('Weekly Intensity Minutes for 2025', fontsize=20, fontweight='bold', pad=20)
plt.xlabel('Week Ending')
plt.ylabel('Total Intensity Minutes')
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.tight_layout()

# Save plot
output_dir = os.path.join(os.path.dirname(__file__), 'images')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'weekly_intensity_minutes.png')
plt.savefig(output_path)
plt.close()

print(f"Chart saved to {output_path}")
