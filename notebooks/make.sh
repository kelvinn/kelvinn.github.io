#!/bin/bash

source .venv/bin/activate
python3 average_sleep_score_per_month.py
python3 average_resting_hr_per_month.py
python3 average_active_calories_per_month.py
python3 summary_quartet.py
python3 stress_quarterly_analysis.py
python3 stress_heatmap_12weeks.py