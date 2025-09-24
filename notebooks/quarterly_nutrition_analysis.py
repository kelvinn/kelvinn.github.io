#!/usr/bin/env python3
import os
import sqlite3
import pandas as pd

def load_nutrition_tables(db_path=None):
    # Resolve default path if not provided
    if db_path is None:
        db_path = os.path.expanduser('~/HealthData/DBs/Nutrition.db')
    # Normalize the path
    db_path = os.path.expanduser(db_path)
    if not os.path.isabs(db_path):
        db_path = os.path.abspath(db_path)

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Nutrition database not found at {db_path}")

    # Connect and read tables into DataFrames
    with sqlite3.connect(db_path) as conn:
        daily_summary_df = pd.read_sql_query("SELECT * FROM daily_summary", conn)
        servings_df = pd.read_sql_query("SELECT * FROM servings", conn)

    return daily_summary_df, servings_df

def main():
    try:
        ds, sv = load_nutrition_tables()
        print("Loaded nutrition tables:")
        print(f"  daily_summary: {ds.shape}")
        print(f"  servings: {sv.shape}")
        # Optional: show a preview
        print(" daily_summary head:")
        print(ds.tail())
        print(" servings head:")
        print(sv.head())

        # Save to CSV for quick verification
        os.makedirs('data', exist_ok=True)
        ds.to_csv('data/DailySummary_Nutrition.csv', index=False)
        sv.to_csv('data/Servings_Nutrition.csv', index=False)
        print("Saved CSVs: data/DailySummary_Nutrition.csv, data/Servings_Nutrition.csv")
    except Exception as e:
        print(f"Error loading nutrition data: {e}")

if __name__ == '__main__':
    main()
