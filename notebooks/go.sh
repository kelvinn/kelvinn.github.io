#!/bin/bash

source .venv/bin/activate
garmindb_cli.py --all --download --import --analyze --latest
python3 average_sleep_score_per_month.py
python3 average_resting_hr_per_month.py
python3 average_active_calories_per_month.py
python3 summary_quartet.py
python3 summary_per_quarter.py
python3 stress_quarterly_analysis.py
python3 stress_heatmap_12weeks.py
python3 weekly_intensity_minutes.py
python3 correlation_matrix_garmin.py
python3 average_sleep_score_per_day.py
python3 monthly_vo2_max.py
deactivate

mv images/*.png ../content/posts/2025-q4-health-review/ 
mv data/*.csv ../content/posts/2025-q4-health-review/data/
