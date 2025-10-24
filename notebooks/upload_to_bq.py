import datetime
from garmindb import GarminConnectConfigManager
from garmindb.garmindb import GarminSummaryDb, DaysSummary, MonitoringDb, MonitoringHeartRate, Sleep, GarminDb, Stress, Attributes, Device, DeviceInfo, File, Weight, RestingHeartRate, DailySummary, MonitoringDb, MonitoringInfo, MonitoringHeartRate, MonitoringIntensity, MonitoringClimb, Monitoring, \
    MonitoringRespirationRate, MonitoringPulseOx
from garmindb.summarydb import DaysSummary, SummaryDb
import pandas as pd
from pandas_gbq import to_gbq



# Set your BigQuery details
project_id = "quantified-life-451208"
dataset_id = "life_logging"

gc_config = GarminConnectConfigManager()
db_params = gc_config.get_db_params()

# start date
start_ts = datetime.datetime.combine(datetime.date(year=2019, month=1, day=1), datetime.datetime.min.time())
# end date (today)
end_ts = datetime.datetime.now()


monitoring_names = MonitoringInfo, MonitoringHeartRate, MonitoringIntensity, MonitoringClimb, Monitoring, \
    MonitoringRespirationRate, MonitoringPulseOx

garmin_db = GarminDb(db_params)
mon_db = MonitoringDb(db_params)

garmin_data = {
    'monitoring': {
        'db': mon_db,
        'names': [MonitoringInfo, MonitoringHeartRate, MonitoringIntensity, MonitoringClimb, Monitoring, \
    MonitoringRespirationRate, MonitoringPulseOx]
    },
    'garmin': {
        'db': garmin_db,
        'names': [Stress, Attributes, Device, DeviceInfo, Weight, RestingHeartRate, DailySummary, Sleep]
    }
}

def main():

    for db_name, db_info in garmin_data.items():
        db = db_info['db']
        names = db_info['names']

        for statistic in names:
            data = statistic.get_for_period(db, start_ts, end_ts, statistic)

            df = pd.DataFrame(data)
            data_dict = [obj.__dict__ for obj in data]
            df = pd.DataFrame(data_dict)

            df = df.drop('_sa_instance_state', axis=1, errors='ignore')

            print(f"{db_name} - {statistic.__name__}:")
            print(df.tail())

            to_gbq(
                df,
                destination_table=f"{dataset_id}.{statistic.__tablename__}",
                project_id=project_id,
                if_exists="replace",
            )


if __name__ == "__main__":
    main()
