import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime, timedelta

from garmindb import GarminConnectConfigManager
from garmindb.garmindb import GarminSummaryDb, DaysSummary, MonitoringDb, MonitoringHeartRate, Sleep, GarminDb
from garmindb.summarydb import DaysSummary, SummaryDb

# Set up seaborn theme
sns.set_theme(style="whitegrid")

# Initialize Garmin DB connection
gc_config = GarminConnectConfigManager()
db_params_dict = gc_config.get_db_params()
garmin_db = GarminDb(db_params_dict)

# Define date range starting from 2025
start_date = datetime(2025, 1, 1)
end_date = datetime.now()
# Query resting heart rate data

end_date = datetime.now().date()
start_date = end_date - timedelta(days=365)  # Exactly 1 year

print(f"Date range: {end_date - start_date} days (1 year)")

# Initialize Garmin database connection
gc_config = GarminConnectConfigManager()
db_params_dict = gc_config.get_db_params()

# Query stress data for the previous 1 year
start_ts = datetime.combine(start_date, datetime.min.time())
end_ts = datetime.combine(end_date, datetime.max.time())

# Get daily summary data for the period
sum_db = SummaryDb(db_params_dict, False)
data_period = DaysSummary.get_for_period(sum_db, start_ts, end_ts, DaysSummary)

intensity_data = [entry for entry in data_period if entry.intensity_time is not None]
print(f"Found {len(intensity_data)} days with intensity data")
