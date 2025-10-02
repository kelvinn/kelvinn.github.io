#!/usr/bin/env python3
"""
quarterly_nutrition_analysis.py

Unified script to print 2025 macro quarterly data and 2025 vitamins/minerals tables as Markdown,
with values formatted to a single decimal place. If sources are missing, the script will
fall back to the nutrition.db (daily_summary) to derive 2025 macros and vitamins.

This script prints:
- Macros: Year, Quarter, QuarterLabel, Energy (kcal), Carbs (g), Protein (g), Fiber (g),
  Fat (g), Saturated (g)
- Vitamins/Minerals: Year, Quarter, QuarterLabel, B1, B2, B3, B5, B6, B12, Folate,
  Vitamin D, Iron, Zinc, Leucine, Lysine, Methionine (B12 included via header variants)

If any columns are missing, those rows/columns are skipped gracefully.
"""
import os
import sqlite3
from pathlib import Path
import pandas as pd

def load_macros_from_db():
    db_path = Path(os.path.expanduser('~/HealthData/DBs/nutrition.db'))
    if not db_path.exists():
        return None
    try:
        with sqlite3.connect(str(db_path)) as conn:
            query = """
            SELECT
              Date,
              [Energy (kcal)], [Carbs (g)], [Protein (g)],
              [Fiber (g)], [Fat (g)], [Saturated (g)]
            FROM daily_summary
            """
            df = pd.read_sql_query(query, conn)
  
            if df.empty:
                return None
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df = df.dropna(subset=['Date'])

            df = df[df['Year'] == 2025]
            df['Year'] = df['Date'].dt.year
            df['Quarter'] = df['Date'].dt.quarter
            df['QuarterLabel'] = df['Year'].astype(str) + "-Q" + df['Quarter'].astype(str)
            
            cols = ['Year','Quarter','QuarterLabel','Energy (kcal)','Carbs (g)',
                    'Protein (g)','Fiber (g)','Fat (g)','Saturated (g)']
            df = df[cols]
            df = df.drop_duplicates(subset=['Year','Quarter','QuarterLabel'])
            # Drop Date if present in the final macro dataframe
            
            if 'Date' in df.columns:
                df = df.drop(columns=['Date'])
            return df
    except Exception:
        return None

def load_vitamins_from_db():
    db_path = Path(os.path.expanduser('~/HealthData/DBs/nutrition.db'))
    if not db_path.exists():
        return None
    with sqlite3.connect(str(db_path)) as conn:
        vit_candidates = [
            '[B1 (Thiamine) (mg)]', '[B2 (Riboflavin) (mg)]', '[B3 (Niacin) (mg)]',
            '[B5 (Pantothenic Acid) (mg)]', '[B6 (Pyridoxine) (mg)]', '[B12 (Cobalamin) (mcg)]',
            '[Folate (mcg)]', '[Vitamin D (IU)]', '[Iron (mg)]', '[Zinc (mg)]',
            '[Leucine (g)]', '[Lysine (g)]', '[Methionine (g)]'
        ]
        # Load all vitamin-related columns if possible
        df = pd.read_sql_query("SELECT Date, " + ", ".join(vit_candidates) + " FROM daily_summary", conn)
        if df.empty:
            return None
        
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Year'] = df['Date'].dt.year
        df['Quarter'] = df['Date'].dt.quarter
        df['QuarterLabel'] = df['Year'].astype(str) + "-Q" + df['Quarter'].astype(str)

        df = df[df['Year'] == 2025]

        return df
 

def print_macros_markdown(df):
    
    if df is None or df.empty:
        print("Macros: no 2025 macro data available.")
        return
    macro_cols = [c for c in ['Energy (kcal)','Carbs (g)','Protein (g)','Fiber (g)','Fat (g)','Saturated (g)'] if c in df.columns]
    header_cols = ['Year','Quarter','QuarterLabel'] + macro_cols
    header = "| " + " | ".join(header_cols) + " |"
    sep = "|" + "|".join(['---'] * len(header_cols)) + "|"
    print(header)
    print(sep)
    for _, row in df.iterrows():
        if all(pd.isna(row[c]) for c in macro_cols):
            continue
        vals = [str(int(row['Year'])), str(int(row['Quarter'])), row['QuarterLabel']]
        for c in macro_cols:
            v = row[c]
            if pd.isna(v):
                vals.append("NaN")
            else:
                try:
                    vals.append(f"{float(v):.1f}")
                except Exception:
                    vals.append(str(v))
        print("| " + " | ".join(vals) + " |")

def print_vitamins_markdown(df):
    if df is None or df.empty:
        print("Vitamins: no 2025 vitamin data available.")
        return

    vit_cols = [c for c in df.columns if c not in ['Year','Quarter','QuarterLabel','Date']]
    headers = ['Year', 'Quarter', 'QuarterLabel'] + vit_cols
    header = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join(['---'] * len(headers)) + " |"
    print(header)
    print(sep)
    for _, row in df.iterrows():
        vals = [str(int(row['Year'])), str(int(row['Quarter'])), row['QuarterLabel']]
        for c in vit_cols:
            v = row[c]
            try:
                vals.append(f"{float(v):.1f}")
            except Exception:
                vals.append("NaN" if pd.isna(v) else str(v))
        print("| " + " | ".join(vals) + " |")

def main():
    macros_df = load_macros_from_db()
    if macros_df is not None and 'Year' in macros_df.columns:
        macros_df = macros_df[macros_df['Year'] == 2025]
        macro_cols = [c for c in ['Energy (kcal)','Carbs (g)','Protein (g)','Fiber (g)','Fat (g)','Saturated (g)'] if c in macros_df.columns]
        if macro_cols:
            for c in macro_cols:
                macros_df[c] = pd.to_numeric(macros_df[c], errors='coerce')
        macros_df = macros_df.groupby(['Year','Quarter','QuarterLabel'], as_index=False).agg({c: 'mean' for c in macro_cols})
    macros_df = macros_df.drop_duplicates(subset=['Year','Quarter','QuarterLabel'])
    print_macros_markdown(macros_df)

    print()

    vitamins_df = load_vitamins_from_db()
    print(vitamins_df.head())
    # if vitamins_df is not None and 'Year' in vitamins_df.columns:

    #     vitamins_df = vitamins_df[(vitamins_df['Year'] == 2025)]
    #     # Exclude non-vitamin columns from aggregation, notably 'Date'
    #     vit_cols = [c for c in vitamins_df.columns if c not in ['Year','Quarter','QuarterLabel','Date']]
    #     if vit_cols:
    #         vitamins_df = vitamins_df.groupby(['Year','Quarter','QuarterLabel'])[vit_cols].mean().reset_index()
    #         vitamins_df = vitamins_df.drop_duplicates(subset=['Year','Quarter','QuarterLabel'])
    #     print_vitamins_markdown(vitamins_df)

if __name__ == "__main__":
    main()
