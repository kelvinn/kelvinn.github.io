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
              [Fiber (g)], [Fat (g)], [Saturated (g)], Completed
            FROM daily_summary
            """
            
            df = pd.read_sql_query(query, conn)
  
            if df.empty:
                return None
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df = df.dropna(subset=['Date', 'Energy (kcal)', 'Carbs (g)', 'Protein (g)'])
            df = df[df['Completed'] == 'true'] if 'Completed' in df.columns else df
            df['Year'] = df['Date'].dt.year
            df['Quarter'] = df['Date'].dt.quarter
            
            cols = ['Year','Quarter','Energy (kcal)','Carbs (g)',
                    'Protein (g)','Fiber (g)','Fat (g)','Saturated (g)']
            df = df[cols]
            
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

        # Do not filter to 2025 anymore
        return df
 

def print_macros_markdown(df):
    
    if df is None or df.empty:
        print("Macros: no 2025 macro data available.")
        return
    macro_cols = [c for c in ['Energy (kcal)','Carbs (g)','Protein (g)','Fiber (g)','Fat (g)','Saturated (g)'] if c in df.columns]
    header_cols = ['Year','Quarter'] + macro_cols
    header = "| " + " | ".join(header_cols) + " |"
    sep = "|" + "|".join(['---'] * len(header_cols)) + "|"
    print(header)
    print(sep)
    for _, row in df.iterrows():
        # Do not skip rows with missing macro data to ensure Q2-Q4 are shown
        vals = [str(int(row['Year'])), str(int(row['Quarter']))]
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

def compute_macro_means(df, value_cols):
    if df is None or df.empty:
        return None
    for c in value_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    grouped = df.groupby(['Year','Quarter'], as_index=False)[value_cols].mean()
    return grouped

def main():
    macros_df = load_macros_from_db()

    macro_cols = []
    if macros_df is not None and 'Year' in macros_df.columns:
        macro_cols = [c for c in ['Energy (kcal)','Carbs (g)','Protein (g)','Fiber (g)','Fat (g)','Saturated (g)'] if c in macros_df.columns]
        if macro_cols:
            macros_df = compute_macro_means(macros_df, macro_cols)
        else:
            macros_df = macros_df.copy()
    if macros_df is not None:
        if not macros_df.empty:
            pass
    print_macros_markdown(macros_df)

    print()

    vitamins_df = load_vitamins_from_db()
    if vitamins_df is not None:
        print(vitamins_df.head())

if __name__ == "__main__":
    main()
