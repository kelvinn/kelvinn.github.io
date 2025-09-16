import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pandas as pd
import seaborn as sns
import os
from datetime import datetime, timedelta
from collections import defaultdict

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

# Define date range starting from 2019
start_date = datetime(2019, 1, 1)
end_date = datetime.now()

print(f"Querying VO2 Max data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")

# Query daily summary data for active calories
# activities_db = ActivitiesDb(db_params_dict, False)
# data_period = DaysSummary.get_for_period(sum_db, start_date, end_date, DaysSummary)

# activities = Activities.get_by_sport(activities_db, "running")
# vo2max_values = Vo2MaxActivities.get_all(vo2_max_activities_db)


vo2_all_activities = Vo2MaxActivities.get_all(activities_db)

print("Count of vo2_max_activities: %s" % len(vo2_all_activities))
# print(vo2_all_activities)

# one = vo2_all_activities[50]
# print(one)

activities = Activities.get_all(activities_db)
activity_obj = activities[50]

Session = sessionmaker(bind=engine)
session = Session()


# activities_with_vo2_max = session.query(Vo2MaxActivities).join(Activities).all() 
# print(activities_with_vo2_max[:5])

users_with_addresses = session.query(Vo2MaxActivities).join(Activities).all() 
print(users_with_addresses[1])


# Querying all columns from both tables using a join
results = session.query(Activities, Vo2MaxActivities).join(Activities, Activities.activity_id == Vo2MaxActivities.activity_id).all()

# # Printing the results
# # for company, buyer in results:
# #     print(f"Company ID: {company.activity_id}, Company Name: {company.start_time}, Buyer ID: {buyer.activity_id}, Buyer Name: {buyer.vo2_max}")

# print(results[10])

# users_left_join = session.query(Activities).outerjoin(Vo2MaxActivities).all() 

# print(users_left_join[:5][0])

# laps = ActivityLaps.get_activity(garmin_act_db, activity_obj.id)


# v = Vo2MaxActivities.get_all(activities_db)
# print(str(laps['vo2_max']))

# print(laps)
# # Get corresponding VO2Max values from StepsActivities, filtering for 2025 and the specific quarter
# vo2max_values = []
# for activity in activities:
#     # Check if activity is within the date range (2025 and specific quarter)
#     if (hasattr(activity, 'start_time') and 
#         activity.start_time and 
#         start_date <= activity.start_time <= end_date):
        
#         steps_activity = StepsActivities.get(activities_db, activity.activity_id)
#         if steps_activity and steps_activity.vo2_max is not None:
#             vo2max_values.append(steps_activity.vo2_max)
