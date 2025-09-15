from sqlalchemy import Column, String, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from garmindb.garmindb import SportActivities, ActivitiesDb
import fitfile
import idbutils

#if __name__ == '__main__':
#    # Example usage
#    db_path = 'garmin_activities.db'  # Replace with your actual database path
#    add_vo2_max_activity(db_path, '20367188259', 45.5)
#    print("Added VO2 Max activity")


# Define the database URL
DATABASE_URL = "sqlite:////Users/kelvinnicholson/HealthData/DBs/garmin_activities.db"

class Vo2MaxActivities(ActivitiesDb.Base, SportActivities):
    """Step based activity table."""

    __tablename__ = 'vo2max_activities'

    db = ActivitiesDb
    table_version = 3
    view_version = 6

    activity_id = Column(String, ForeignKey('activities.activity_id'), primary_key=True)
    vo2_max = Column(Float)

    def __repr__(self):
        return f"&lt;Vo2MaxActivities(activity_id='{self.activity_id}', vo2_max={self.vo2_max})&gt;"

    def add_vo2_max_activity(session, activity_id_val, vo2_max_val):
        new_record = Vo2MaxActivities(activity_id=activity_id_val, vo2_max=vo2_max_val)
        session.add(new_record)


# Create the database engine
engine = create_engine(DATABASE_URL)

# Create the table in the database
ActivitiesDb.Base.metadata.create_all(engine)

print("Table 'vo2max_activities' created successfully in garmin_activities.db")