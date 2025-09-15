from garmin_fit_sdk import Decoder, Stream
import numpy as np
import datetime
import logging
from sqlalchemy import Column, String, Float, Integer, DateTime, Time, Enum, ForeignKey, PrimaryKeyConstraint, desc, literal_column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from vo2max_db import Vo2MaxActivities # Import the class
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

# Define the path to the FIT file directory
fit_file_path = "/Users/kelvinnicholson/HealthData/FitFiles/Activities/"

# Database URL
DATABASE_URL = "sqlite:////Users/kelvinnicholson/HealthData/DBs/garmin_activities.db"

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

logger = logging.getLogger(__name__)

try:
    # Create the database tables if they don't exist
    # Ensure the engine is available before creating tables
    #try:
    #    # idbutils.DB.create returns a DB object that should manage its engine.
    #    # We need to ensure the engine is accessible for create_all.
    #    # Accessing ActivitiesDb.Base.metadata.bind is a common SQLAlchemy pattern.
    #    if ActivitiesDb.Base.metadata.bind is None:
    #        # If bind is None, it means the engine hasn't been associated yet.
    #        # idbutils.DB.create should handle engine creation internally.
    #        # We might need to explicitly get the engine from the ActivitiesDb instance.
    #        # Let's try accessing it directly, assuming it's created upon DB.create.
    #        if not hasattr(ActivitiesDb, 'engine') or ActivitiesDb.engine is None:
    #            # If it's still not available, we might need to explicitly initialize it.
    #            # This is a common pattern if the DB object itself holds the engine.
    #            # However, idbutils might manage this differently.
    #            # For now, we'll rely on the assumption that ActivitiesDb.engine should exist.
    #            # If this fails, we'll need to consult idbutils documentation or examples.
    #            pass # Placeholder if explicit initialization is needed.

    #    # Use the engine associated with ActivitiesDb.Base.metadata
    #    if ActivitiesDb.Base.metadata.bind:
    #        ActivitiesDb.Base.metadata.create_all(ActivitiesDb.Base.metadata.bind)
    #    else:
    #        print("ActivitiesDb engine is not available via metadata.bind. Cannot create tables.")
    #        # Exit or handle this critical error
    #except Exception as e:
    #    print(f"Error during database table creation: {e}")
    #    # Handle the error appropriately, perhaps by exiting or logging

    # Decode the FIT file
    for filename in os.listdir(fit_file_path):
        if filename.endswith(".fit"):
            print(f"Processing file: {filename}")
            # Extract activity ID from filename
            activity_id = filename.split("_")[0]
            print(f"\nActivity ID extracted from filename: {activity_id}")
            fit_file = os.path.join(fit_file_path, filename)
            stream = Stream.from_file(fit_file)
            decoder = Decoder(stream)
            messages, errors = decoder.read()


            if not activity_id and 'file_id_mesgs' in messages and messages['file_id_mesgs']:
                file_id_mesgs = messages['file_id_mesgs']
                print(f"Contents of file_id_mesgs: {file_id_mesgs}")
                if file_id_mesgs:
                    for mesg in file_id_mesgs:
                        if 'activity_id' in mesg:
                            activity_id = mesg['activity_id']
                            break
                        elif 8 in mesg: # Common field for activity_id in file_id_mesgs
                            activity_id = mesg[8]
                            print(f"Activity ID found in 'file_id_mesgs' with key 8: {activity_id}")
                            break

            if not activity_id:
                print("\nActivity ID not found. Skipping file.")
                continue

            if activity_id:

                # The message key can be an integer or a string, so we check for both.
                vo2_max_mesgs = messages.get(140) or messages.get('140')

                if vo2_max_mesgs:
                    vo2_max_found = False
                    print("\n--- Raw VO2 Max from FIT File ---")
                    for i, mesg in enumerate(vo2_max_mesgs):
                        if 7 in mesg:
                            unscaled_vo2_max = mesg[7]
                            if unscaled_vo2_max > 0:
                                # Apply scaling factor as per the article
                                scaled_vo2_max = unscaled_vo2_max * 3.5 / 65536
                                print(f"Found non-zero VO2 Max value in message {i}:")
                                print(f"Unscaled Raw VO2 Max (field 7): {unscaled_vo2_max}")
                                print(f"Scaled Raw VO2 Max: {scaled_vo2_max:.2f} mL/kg/min")
                                vo2_max_found = True

                    
                                if scaled_vo2_max is not None and scaled_vo2_max > 0:
                                    try:
                                        db = SessionLocal()
                                        vo2max_activity = Vo2MaxActivities(activity_id=activity_id, vo2_max=scaled_vo2_max)
                                        
                                        # Use INSERT OR REPLACE to handle duplicates
                                        db.merge(vo2max_activity)
                                        
                                        db.commit()
                                        print(f"Successfully inserted/updated VO2 Max data for activity ID {activity_id} using new method.")
                                    except Exception as db_error:
                                        print(f"Error inserting/updating data into vo2max_activities table: {db_error}")
                                    finally:
                                        db.close()
                                else:
                                    print("\nVO2 Max not found or is zero. Skipping insertion.")
                            break # Found a valid value, no need to continue

                    if not vo2_max_found:
                        print("Searched all messages of type 140, but no non-zero VO2 Max value found in field 7.")
                        print("Dumping first message of type 140 for inspection:")
                        if vo2_max_mesgs:
                            for field, value in vo2_max_mesgs[0].items():
                                print(f"- Field {field}: {value}")
                else:
                    print("\n--- Raw VO2 Max from FIT File ---")
                    print("Message type 140 (containing VO2 Max) not found in this FIT file.")

                


    # --- Raw VO2 Max Extraction ---
    # Based on https://medium.com/@daniel.lepold/visualise-your-precise-vo%E2%82%82-max-from-garmin-data-in-python-2d76e50e437c
    
    # The message key can be an integer or a string, so we check for both.
    # vo2_max_mesgs = messages.get(140) or messages.get('140')

    # if vo2_max_mesgs:
    #     vo2_max_found = False
    #     print("\n--- Raw VO2 Max from FIT File ---")
    #     for i, mesg in enumerate(vo2_max_mesgs):
    #         if 7 in mesg:
    #             unscaled_vo2_max = mesg[7]
    #             if unscaled_vo2_max > 0:
    #                 # Apply scaling factor as per the article
    #                 scaled_vo2_max = unscaled_vo2_max * 3.5 / 65536
    #                 print(f"Found non-zero VO2 Max value in message {i}:")
    #                 print(f"Unscaled Raw VO2 Max (field 7): {unscaled_vo2_max}")
    #                 print(f"Scaled Raw VO2 Max: {scaled_vo2_max:.2f} mL/kg/min")
    #                 vo2_max_found = True
    #                 break # Found a valid value, no need to continue
        
    #     if not vo2_max_found:
    #         print("Searched all messages of type 140, but no non-zero VO2 Max value found in field 7.")
    #         print("Dumping first message of type 140 for inspection:")
    #         if vo2_max_mesgs:
    #             for field, value in vo2_max_mesgs[0].items():
    #                 print(f"- Field {field}: {value}")
    # else:
    #     print("\n--- Raw VO2 Max from FIT File ---")
    #     print("Message type 140 (containing VO2 Max) not found in this FIT file.")


    # if not activity_id and 'file_id_mesgs' in messages and messages['file_id_mesgs']:
    #     file_id_mesgs = messages['file_id_mesgs']
    #     print(f"Contents of file_id_mesgs: {file_id_mesgs}")
    #     if file_id_mesgs:
    #         for mesg in file_id_mesgs:
    #             if 'activity_id' in mesg:
    #                 activity_id = mesg['activity_id']
    #                 break
    #             elif 8 in mesg: # Common field for activity_id in file_id_mesgs
    #                 activity_id = mesg[8]
    #                 print(f"Activity ID found in 'file_id_mesgs' with key 8: {activity_id}")
    #                 break

    #     if activity_id:
    #         print(f"\nActivity ID found: {activity_id}")
    #         print(f"Type of Activity ID: {type(activity_id)}")  # Add this line
    #         # Insert the data into the new table if scaled_vo2_max is available
    #         if scaled_vo2_max is not None and scaled_vo2_max > 0:
    #             try:
    #                 db = SessionLocal()
    #                 vo2max_activity = Vo2MaxActivities(activity_id=activity_id, vo2_max=scaled_vo2_max)
    #                 db.add(vo2max_activity)
    #                 db.commit()
    #                 db.refresh(vo2max_activity)
    #                 print(f"Successfully inserted VO2 Max data for activity ID {activity_id} using new method.")
    #             except Exception as db_error:
    #                 print(f"Error inserting data into vo2max_activities table: {db_error}")
    #             finally:
    #                 db.close()
    #         else:
    #             print("\nVO2 Max not found or is zero. Skipping insertion.")

except Exception as e:
    print(f"Error processing FIT file: {e}")
