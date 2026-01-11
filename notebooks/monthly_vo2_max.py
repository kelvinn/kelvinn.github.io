import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pandas as pd
import seaborn as sns
import os
from datetime import datetime, timedelta
from collections import defaultdict
from constants import start_date, end_date

from garmindb import GarminConnectConfigManager
from garmindb.garmindb import GarminSummaryDb, DaysSummary, MonitoringDb, MonitoringHeartRate, Sleep, GarminDb, RestingHeartRate, Activities, ActivitiesDb
from garmindb.summarydb import DaysSummary, SummaryDb
from sqlalchemy.orm import sessionmaker
from vo2max_db import Vo2MaxActivities, engine

# Set up seaborn theme
sns.set_theme(style="whitegrid")

# Initialize database connection
gc_config = GarminConnectConfigManager()
db_params_dict = gc_config.get_db_params()
garmin_db = GarminDb(db_params_dict)
activities_db = ActivitiesDb(db_params_dict)
vo2_max_activities_db = Vo2MaxActivities()

print(f"Querying VO2 Max data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Querying all columns from both tables using a join
results = session.query(Activities, Vo2MaxActivities).join(Activities, Activities.activity_id == Vo2MaxActivities.activity_id).all()

# Prepare data for plotting
data = []
for activity, vo2 in results:
    if activity.start_time and vo2.vo2_max is not None:
        data.append({
            'date': activity.start_time,
            'vo2_max': vo2.vo2_max
        })

# Create a DataFrame
df = pd.DataFrame(data)

# Convert date to datetime and set as index
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Group by month and calculate 95th percentile vo2_max


monthly_95th_percentile = df.resample('ME').quantile(0.95)

# Export per-month VO2 max 95th percentile data
export_df = monthly_95th_percentile.reset_index()
export_df.columns = ['date','vo2_max_95th']
export_df['year'] = export_df['date'].dt.year
export_df['month'] = export_df['date'].dt.month
export_df = export_df[['year','month','vo2_max_95th']]
os.makedirs('data', exist_ok=True)
csv_path = os.path.join('data', 'monthly_vo2_max_per_month.csv')
export_df.to_csv(csv_path, index=False)
print(f"Exported monthly VO2 max data to {csv_path}")

# Plotting
plt.figure(figsize=(12, 6))


plt.plot(monthly_95th_percentile.index, monthly_95th_percentile['vo2_max'], marker='o', label='95th Percentile VO2 Max')


plt.title('Monthly 95th Percentile VO2 Max Values')
plt.xlabel('Date')
plt.ylabel('VO2 Max')
plt.xticks(rotation=45)
plt.grid()
plt.legend()

plt.tight_layout()
plt.savefig('images/monthly_vo2_max.png')
