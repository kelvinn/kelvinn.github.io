import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from constants import end_date
from garmindb import GarminConnectConfigManager
from garmindb.summarydb import DaysSummary, SummaryDb

# Set up seaborn theme
sns.set_theme(style="whitegrid")

# Initialize database connection
gc_config = GarminConnectConfigManager()
db_params_dict = gc_config.get_db_params()

# Calculate date range for previous 12 months
start_date = end_date - timedelta(days=365)  # 12 months back


# Query daily summaries
sum_db = SummaryDb(db_params_dict, False)
data_period = DaysSummary.get_for_period(sum_db, start_date, end_date, DaysSummary)

# Filter for days with intensity data
intensity_data = [entry for entry in data_period if getattr(entry, 'intensity_time', None) is not None]
print(f"Found {len(intensity_data)} days with intensity data between {start_date.date()} and {end_date.date()}")

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
weekly_summary = df['intensity_minutes'].resample('W-SUN').sum()

# Ensure full weekly coverage across the date range
full_week_index = pd.date_range(start=start_date, end=end_date, freq='W-SUN')
weekly_summary_full = weekly_summary.reindex(full_week_index, fill_value=0)

# Export per-week data to CSV
export_df = weekly_summary_full.reset_index()
export_df.columns = ['week_end', 'intensity_minutes']
os.makedirs('data', exist_ok=True)
csv_path = os.path.join('data', 'weekly_intensity_minutes_per_week.csv')
export_df.to_csv(csv_path, index=False)
print(f"Exported weekly intensity data to {csv_path}")

# Calculate averages and stats
average_weekly_intensity = weekly_summary_full.mean()

# Quarterly averages (print only, no graph)
quarterly_mean = weekly_summary_full.resample('Q').mean()
print("Quarterly average intensity minutes:")
for quarter_end, value in quarterly_mean.items():
    print(f"  Quarter ending {quarter_end.date()}: {value:.2f} minutes")

# Graphing: weekly bars, one bar per week
plt.figure(figsize=(18, 6))
weekly_summary_full.plot(kind='bar', width=0.8, color='#69b3a2', align='center')
plt.axhline(y=800, color='r', linestyle='--', label='Weekly Target (800)')
plt.axhline(y=average_weekly_intensity, color='g', linestyle='--', label=f'Weekly Average ({average_weekly_intensity:.0f})')

plt.title('Weekly Intensity Minutes for 2025', fontsize=20, fontweight='bold', pad=20)
plt.xlabel('Week End Date')
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
