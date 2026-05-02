# Weather Monitor Scripts

This directory contains scripts used by GitHub Actions weather alerts.

## Active script

- `temperature_monitor.py`: checks Neutral Bay forecast temperatures and emits an alert when tomorrow's max is above the configured threshold.

## Required GitHub Secrets

Add these secrets in repository Actions settings:

- `PUSHOVER_API_KEY`
- `PUSHOVER_USER_KEY`
- `WEATHER_API_KEY`
- `WEATHERSTACK_API_KEY` (optional fallback provider)

## Local run

```bash
python .github/scripts/temperature_monitor.py
```
