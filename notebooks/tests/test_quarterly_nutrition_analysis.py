import sys
import os
import pandas as pd
import pytest
# Ensure tests can import the module from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from quarterly_nutrition_analysis import compute_macro_means, compute_vitamin_quarterly_means

def test_compute_macro_means_basic():
    df = pd.DataFrame({
        'Year': [2025, 2025],
        'Quarter': [2, 3],
        'Energy (kcal)': [100.0, 200.0],
        'Carbs (g)': [10.0, 20.0],
        'Protein (g)': [5.0, 15.0],
        'Fiber (g)': [3.0, 4.0],
        'Fat (g)': [6.0, 7.0],
        'Saturated (g)': [1.0, 2.0],
    })
    res = compute_macro_means(df, ['Energy (kcal)', 'Carbs (g)', 'Protein (g)'])
    assert list(res.columns) == ['Year', 'Quarter', 'Energy (kcal)', 'Carbs (g)', 'Protein (g)']
    assert len(res) == 2
    assert res.iloc[0]['Energy (kcal)'] == 100.0
    assert res.iloc[1]['Quarter'] == 3

def test_compute_vitamin_quarterly_means_basic():
    df = pd.DataFrame({
        'Date': ['2025-05-01', '2025-08-01'],
        'B1 (Thiamine) (mg)': [5.0, 2.0],
        'B2 (Riboflavin) (mg)': [3.0, 4.0],
        'B3 (Niacin) (mg)': [1.0, 2.0],
    })
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.quarter
    res = compute_vitamin_quarterly_means(df)
    assert 'Year' in res.columns
    assert 'Quarter' in res.columns
    assert len(res) == 2
    assert res.iloc[0]['B1 (Thiamine) (mg)'] == 5.0
    assert res.iloc[1]['B1 (Thiamine) (mg)'] == 2.0
