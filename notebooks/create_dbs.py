"""
Create Turso databases from credentials.yaml
Creates local SQLite databases in ~/HealthData/DBs that sync to Turso.
Uses Turso CLI for database operations.
"""

import os
import subprocess
import yaml
import libsql


def load_credentials():
    """Load credentials from credentials.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), "credentials.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def get_db_path(db_filename):
    """Get the local path for the database file"""
    home = os.path.expanduser("~")
    db_dir = os.path.join(home, "HealthData", "DBs")
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, db_filename)


def create_databases():
    """Create/connect to each Turso database defined in credentials.yaml"""
    credentials = load_credentials()
    turso_config = credentials.get("turso", {})

    results = []

    for db_name, db_config in turso_config.items():
        url = db_config.get("url")
        auth_token = db_config.get("auth_token")
        db_filename = db_config.get("db_filename")

        if not url or not auth_token:
            print(f"Skipping {db_name}: missing url or auth_token")
            results.append((db_name, False, "missing url or auth_token"))
            continue

        local_db_path = get_db_path(db_filename)

        # Set auth token for Turso CLI
        env = os.environ.copy()
        env["TURSO_AUTH_TOKEN"] = auth_token

        try:
            # First, ensure the database exists on Turso by creating it if needed
            # Extract database name from URL (e.g., garmin-kelvinn from https://garmin-kelvinn.aws-ap-northeast-1.turso.io)
            db_identifier = url.replace("https://", "").split(".")[0]

            # Try to create the database (will fail gracefully if it already exists)
            subprocess.run(
                ["turso", "db", "create", db_identifier],
                env=env,
                capture_output=True,
                timeout=60
            )

            # Now connect using libsql
            conn = libsql.connect(
                local_db_path,
                sync_url=url,
                auth_token=auth_token
            )

            # Sync to verify connection
            conn.sync()

            print(f"Successfully created/synced {db_name} -> {local_db_path}")
            results.append((db_name, True, local_db_path))

            conn.close()

        except Exception as e:
            print(f"Failed to create {db_name}: {e}")
            results.append((db_name, False, str(e)))

    return results


if __name__ == "__main__":
    print("Creating Turso databases from credentials.yaml...\n")
    results = create_databases()
    print("\n--- Summary ---")
    success = sum(1 for _, ok, _ in results if ok)
    failed = sum(1 for _, ok, _ in results if not ok)
    print(f"Connected: {success}, Failed: {failed}")
