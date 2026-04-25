#!/bin/bash
set -euo pipefail

# Quarterly report configuration file.
# Override with REPORT_CONFIG_FILE=/path/to/file.env ./go.sh
CONFIG_FILE="${REPORT_CONFIG_FILE:-report_config.env}"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "Missing config file: $CONFIG_FILE"
  echo "Create it from report_config.env.example."
  exit 1
fi

set -a
source "$CONFIG_FILE"
set +a

# Validate required configuration before running the pipeline.
python3 -c "from report_config import load_report_config; load_report_config()"

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

mkdir -p "$REPORT_POST_OUTPUT_DIR/data"
mv images/*.png "$REPORT_POST_OUTPUT_DIR/"
mv data/*.csv "$REPORT_POST_OUTPUT_DIR/data/"
