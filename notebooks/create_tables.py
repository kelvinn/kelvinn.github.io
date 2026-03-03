"""
Create garmindb tables in existing Turso databases.
Databases should already exist at ~/HealthData/DBs/
"""

import os
import yaml
import sqlite3
import libsql


def load_credentials():
    """Load credentials from credentials.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), "credentials.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def get_db_path(db_filename):
    """Get the local path for the database file"""
    home = os.path.expanduser("~")
    return os.path.join(home, "HealthData", "DBs", db_filename)


def create_tables():
    """Create garmindb tables in each Turso database"""
    credentials = load_credentials()
    turso_config = credentials.get("turso", {})

    # Import garmindb classes
    from garmindb.garmindb import GarminDb, GarminSummaryDb, MonitoringDb
    from garmindb.summarydb import SummaryDb
    from garmindb.garmindb import ActivitiesDb
    from sqlalchemy import create_engine

    results = []

    # Map database names to their garmindb classes and target filenames
    # Note: GarminDb uses 'garmin', MonitoringDb uses 'garmin_monitoring', ActivitiesDb uses 'garmin_activities'
    db_mapping = {
        "garmin": (GarminDb, "garmin.db"),
        "monitoring": (MonitoringDb, "monitoring.db"),
        "summary": (SummaryDb, "summary.db"),
        "activities": (ActivitiesDb, "activities.db"),
        "garmin_monitoring": (MonitoringDb, "garmin_monitoring.db"),
        "garmin_activities": (ActivitiesDb, "garmin_activities.db"),
    }

    for db_name, db_config in turso_config.items():
        url = db_config.get("url")
        auth_token = db_config.get("auth_token")
        db_filename = db_config.get("db_filename")

        if not url or not auth_token:
            print(f"Skipping {db_name}: missing url or auth_token")
            results.append((db_name, False, "missing url or auth_token"))
            continue

        local_db_path = get_db_path(db_filename)

        if db_name not in db_mapping:
            print(f"Skipping {db_name}: no mapping found")
            results.append((db_name, False, "no mapping"))
            continue

        db_class, target_filename = db_mapping[db_name]

        # Get the actual file path the db_class uses
        actual_db_path = get_db_path(target_filename)

        try:
            # Create engine pointing to the actual file
            engine = create_engine(f'sqlite:///{actual_db_path}')

            # Create all tables from the db_class Base metadata
            db_class.Base.metadata.create_all(engine)

            engine.dispose()

            print(f"Successfully created tables in {db_name} ({db_filename})")
            results.append((db_name, True, local_db_path))

        except Exception as e:
            print(f"Failed to create tables in {db_name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((db_name, False, str(e)))

    return results


if __name__ == "__main__":
    print("Creating garmindb tables in Turso databases...\n")
    results = create_tables()
    print("\n--- Summary ---")
    success = sum(1 for _, ok, _ in results if ok)
    failed = sum(1 for _, ok, _ in results if not ok)
    print(f"Success: {success}, Failed: {failed}")
