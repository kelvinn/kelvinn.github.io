import numpy as np
import datetime
from IPython.display import display
import pandas as pd
from pandas_gbq import to_gbq

from garmindb import GarminConnectConfigManager
from garmindb.garmindb import GarminSummaryDb, DaysSummary, MonitoringDb, MonitoringHeartRate, Sleep, GarminDb
from garmindb.summarydb import DaysSummary, SummaryDb

# start date
start_ts = datetime.datetime.combine(datetime.date(year=2019, month=1, day=1), datetime.datetime.min.time())
# end date (today)
end_ts = datetime.datetime.combine(datetime.date.today(), datetime.datetime.max.time())

# Set your BigQuery details
project_id = "quantified-life-451208"
dataset_id = "garmin"
table_id = "daily_summary"

gc_config = GarminConnectConfigManager()
db_params = gc_config.get_db_params()

garmin_db = GarminDb(db_params)
sum_db = SummaryDb(db_params, False)
data = DaysSummary.get_for_period(sum_db, start_ts, end_ts, DaysSummary)

df = pd.DataFrame(data)

print(len(data))

data_dict = [obj.__dict__ for obj in data]
print(len(data_dict))
df = pd.DataFrame(data_dict)

df = df.drop('_sa_instance_state', axis=1)
df = df.drop('day', axis=1)

print(df.head())

print(df.shape)
print(df.columns)






# print(df.head())
to_gbq(
    df,
    destination_table=f"{dataset_id}.{table_id}",
    project_id=project_id,
    if_exists="replace",  # or "append" if you want to add to an existing table
    # table_schema=table_schema,  # optional
    # credentials=credentials  # only if you're not using gcloud CLI auth
)