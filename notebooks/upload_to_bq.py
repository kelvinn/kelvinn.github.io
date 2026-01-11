import datetime
import re
from garmindb import GarminConnectConfigManager
from garmindb.garmindb import GarminSummaryDb, DaysSummary, MonitoringDb, MonitoringHeartRate, Sleep, GarminDb, Stress, Attributes, Device, DeviceInfo, File, Weight, RestingHeartRate, DailySummary, MonitoringDb, MonitoringInfo, MonitoringHeartRate, MonitoringIntensity, MonitoringClimb, Monitoring, \
    MonitoringRespirationRate, MonitoringPulseOx, Activities, ActivitiesDb, Act
from garmindb.summarydb import DaysSummary, SummaryDb
import pandas as pd
from pandas_gbq import to_gbq



# Set your BigQuery details
project_id = "quantified-life-451208"
dataset_id = "life_logging"

gc_config = GarminConnectConfigManager()
db_params = gc_config.get_db_params()

# start date
start_ts = datetime.datetime.combine(datetime.date(year=2025, month=9, day=1), datetime.datetime.min.time())
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

# Nutrition helpers
def sanitize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize all column names to be BigQuery-friendly identifiers
    new_cols = []
    for col in df.columns:
        new = str(col).strip().replace(' ', '_')
        new = re.sub(r'[^0-9a-zA-Z_]', '_', new)
        new = re.sub(r'_+', '_', new)
        new = new.strip('_')
        if new == '':
            new = 'col'
        new_cols.append(new)
    df.columns = new_cols
    return df

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = sanitize_column_names(df)
    return df

def ensure_datetime_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    if column_name in df.columns:
        df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
    return df

def combine_day_time(df: pd.DataFrame, day_col: str, time_col: str, new_col: str) -> pd.DataFrame:
    if day_col in df.columns and time_col in df.columns:
        df[new_col] = pd.to_datetime(df[day_col].astype(str) + ' ' + df[time_col].astype(str), errors='coerce')
    return df

def drop_columns(df: pd.DataFrame, cols_to_drop) -> pd.DataFrame:
    existing = [c for c in cols_to_drop if c in df.columns]
    if existing:
        df = df.drop(columns=existing)
    return df

def log_preview(name: str, df: pd.DataFrame):
    print(f"{name} preview:")
    print(df.tail())

def upload_to_gbq(df: pd.DataFrame, table: str):
    to_gbq(
        df,
        destination_table=table,
        project_id=project_id,
        if_exists="replace",
    )

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


    # Nutrition data uploads
    try:
        daily_path = "data/dailysummary.csv"
        daily_df = load_csv(daily_path)
        daily_df = ensure_datetime_column(daily_df, "Date")
        # Filter to only Completed rows
        if 'Completed' in daily_df.columns:
            daily_df = daily_df[daily_df['Completed'].astype(str).str.lower() == 'true']

        print("nutrition_daily_summary:")
        log_preview("nutrition_daily_summary", daily_df)

        upload_to_gbq(daily_df, f"{dataset_id}.nutrition_daily_summary")
    except Exception as e:
        print(f"Error uploading nutrition_daily_summary: {e}")

    try:
        servings_path = "data/servings.csv"
        servings_df = load_csv(servings_path)
        # Build a combined DateTime from Day and Time if available
        if 'Day' in servings_df.columns and 'Time' in servings_df.columns:
            servings_df = combine_day_time(servings_df, 'Day', 'Time', 'DateTime')
        # Clean up to keep only relevant columns for BigQuery
        for drop in ['Day', 'Time']:
            if drop in servings_df.columns:
                servings_df = servings_df.drop(columns=[drop])
        # If DateTime exists, ensure it's a datetime type
        if 'DateTime' in servings_df.columns:
            servings_df['DateTime'] = pd.to_datetime(servings_df['DateTime'], errors='coerce')

        print("nutrition_servings:")
        log_preview("nutrition_servings", servings_df)

        upload_to_gbq(servings_df, f"{dataset_id}.nutrition_servings")
    except Exception as e:
        print(f"Error uploading nutrition_servings: {e}")

if __name__ == "__main__":
    main()
