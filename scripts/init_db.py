#!/usr/bin/env python3
"""Initialize the database for notification history."""

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from db import init_db, seed_sources, get_session


def main():
    """Initialize the database tables and seed default data."""
    print("Initializing database...")

    try:
        # Create tables
        init_db()
        print("Tables created successfully")

        # Seed default sources
        session = get_session()
        try:
            seed_sources(session)
            print("Default sources seeded successfully")
        finally:
            session.close()

        print("Database initialization complete!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
