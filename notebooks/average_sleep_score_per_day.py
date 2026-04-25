import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from constants import quarter_end_ts, quarter_label, quarter_start_ts
from garmindb import GarminConnectConfigManager
from garmindb.garmindb import GarminDb, Sleep

# Set up seaborn theme
sns.set_theme(style="whitegrid")

# Initialize database connection
gc_config = GarminConnectConfigManager()
db_params_dict = gc_config.get_db_params()
garmin_db = GarminDb(db_params_dict)

# Day names in order (Monday to Sunday)
day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

print(
    f"Querying sleep data for {quarter_label} "
    f"({quarter_start_ts.strftime('%Y-%m-%d')} to {quarter_end_ts.strftime('%Y-%m-%d')})..."
)

sleep_data = Sleep.get_for_period(garmin_db, quarter_start_ts, quarter_end_ts, Sleep)

if not sleep_data:
    print("No sleep data found for configured quarter")
    raise SystemExit(1)

# Aggregate by day of week
day_scores = {day: [] for day in day_names}
for sleep_record in sleep_data:
    sleep_score = getattr(sleep_record, "score", None)
    sleep_date = getattr(sleep_record, "day", None)
    if sleep_score is None or sleep_date is None:
        continue
    day_name = day_names[sleep_date.weekday()]
    day_scores[day_name].append(sleep_score)

row = []
for day in day_names:
    values = day_scores[day]
    row.append(np.mean(values) if values else np.nan)

weekly_avg = np.nanmean(row)
row.append(weekly_avg)

columns = day_names + ["Avg"]
df = pd.DataFrame([row], index=[quarter_label], columns=columns)

# Export per-quarter data to CSV
os.makedirs("data", exist_ok=True)
export_df = df.reset_index().rename(columns={"index": "Quarter"})
csv_path = os.path.join("data", "sleep_score_per_day_per_quarter.csv")
export_df.to_csv(csv_path, index=False)
print(f"Exported per-quarter sleep score data to {csv_path}")

print("DataFrame created:")
print(df)

# Create the heatmap
plt.figure(figsize=(12, 2.6))
sns.heatmap(
    df,
    xticklabels=columns,
    yticklabels=True,
    annot=True,
    fmt=".1f",
    cmap="YlOrRd",
    cbar_kws={"label": "Average Sleep Score"},
    linewidths=0.5,
    square=True,
    cbar=True,
)

plt.title(
    f"Average Sleep Score per Day of Week ({quarter_label})",
    fontsize=16,
    fontweight="bold",
    pad=20,
)
plt.xlabel("Day of Week", fontsize=14)
plt.ylabel("Quarter", fontsize=14)
plt.xticks(rotation=0, ha="center")

plt.tight_layout()
os.makedirs("images", exist_ok=True)
plt.savefig("images/sleep_score_per_day.png", dpi=300, bbox_inches="tight")
print("Heatmap saved as 'images/sleep_score_per_day.png'")
