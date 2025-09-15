from sqlalchemy import Column, String, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from garmindb.garmindb import SportActivities, ActivitiesDb
from garmindb.garmindb.activities_db import ActivitiesCommon
import fitfile
import idbutils

#if __name__ == '__main__':
#    # Example usage
#    db_path = 'garmin_activities.db'  # Replace with your actual database path
#    add_vo2_max_activity(db_path, '20367188259', 45.5)
#    print("Added VO2 Max activity")


# Define the database URL
DATABASE_URL = "sqlite:////Users/kelvinnicholson/HealthData/DBs/garmin_activities.db"

# Vo2MaxActivitiesDb = idbutils.DB.create('vo2max_activities', 13, "Database for storing activities data.")


class Vo2MaxActivities(ActivitiesDb.Base, idbutils.DbObject):
    """Step based activity table."""

    __tablename__ = 'vo2max_activities'

    db = ActivitiesDb
    table_version = 3

    activity_id = Column(String, ForeignKey('activities.activity_id'), primary_key=True)
    vo2_max = Column(Float)

    __table_args__ = (PrimaryKeyConstraint("activity_id"),)

    def __repr__(self):
        return f"<Vo2MaxActivities(activity_id='{self.activity_id}', vo2_max={self.vo2_max})>"

    def add_vo2_max_activity(session, activity_id_val, vo2_max_val):
        new_record = Vo2MaxActivities(activity_id=activity_id_val, vo2_max=vo2_max_val)
        session.add(new_record)
    
    @classmethod
    def _view_selectable(cls):
        # The query fails to generate sql when using the func.round clause.
        selectable = [
            Vo2MaxActivities.activity_id.label('activity_id'),
            Vo2MaxActivities.vo2_max.label('vo2_max')
        ]

    @classmethod
    def s_get(cls, session, activity_id, default=None):
        """Return a single instance for the given id."""
        instance = session.query(cls).filter(cls.activity_id == activity_id).scalar()
        if instance is None:
            return default
        return instance
    
    @classmethod
    def s_get_activity(cls, session, activity_id):
        """Return all laps for a given activity_id."""
        return session.query(cls).filter(cls.activity_id == activity_id)
    
    @classmethod
    def get_activity(cls, db, activity_id):
        """Return vo2_max for a given activity_id."""
        with db.managed_session() as session:
            return cls.s_get_activity(session, activity_id)
        
# Create the database engine
engine = create_engine(DATABASE_URL)

# Create the table in the database
ActivitiesDb.Base.metadata.create_all(engine)

print("Table 'vo2max_activities' created successfully in garmin_activities.db")
