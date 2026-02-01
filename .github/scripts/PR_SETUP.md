# PR Setup Instructions

The repository has branch protection rules that prevent automated creation of pull requests. Here's how to manually create the PR:

## Option 1: Using GitHub Web Interface

1. Go to [kelvinn/kelvinn.github.io](https://github.com/kelvinn/kelvinn.github.io)
2. Click "New pull request"
3. The source branch should be `kelvinn/air-quality-monitor` (you may need to select it from the dropdown)
4. The base branch should be `main`
5. Title: "Add air quality monitoring for NSW hazard reduction burns"
6. Use the description from below

## Option 2: Force Push to Main (Temporary)

If you have permission to bypass checks temporarily:

```bash
git push origin kelvinn/air-quality-monitor:main --force
```

Then create a PR from `kelvinn/air-quality-monitor` to `main`.

## PR Description

```
## Summary
- Monitor NSW RFS planned hazard reduction burn locations
- Check 24-hour wind forecast for Sydney
- Alert if winds will blow smoke toward Sydney:
  - Fire in west + easterly winds → notify
  - Fire in south + northerly winds → notify
  - Fire in north + southerly winds → notify
- Send notifications via Pushover API
- Run every 30 minutes via GitHub Actions

## Files changed
- `.github/scripts/air_quality_monitor.py` - Main monitoring script
- `.github/workflows/air-quality-monitor.yaml` - GitHub Actions workflow
- `.github/scripts/README.md` - Setup instructions
- `.gitignore` - Added `.context/` directory

## Setup
To enable notifications, add these secrets:
- `PUSHOVER_API_KEY` - Pushover app token
- `PUSHOVER_USER_KEY` - Pushover user key
- `WEATHER_API_KEY` - Optional OpenWeatherMap API key

## Test plan
1. Add Pushover secrets
2. Run workflow manually to test
3. Verify notifications are sent when risk conditions exist

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Changes Summary

The PR adds:
1. **air_quality_monitor.py** - Python script that:
   - Queries NSW RFS API for hazard reduction burns
   - Gets wind forecast for Sydney
   - Applies heuristic to determine risk of smoke reaching Sydney
   - Outputs alerts to JSON file

2. **air-quality-monitor.yaml** - GitHub Actions workflow that:
   - Runs every 30 minutes
   - Triggers the monitoring script
   - Sends Pushover notifications if risk detected

3. **README.md** - Setup instructions

4. **Updated .gitignore** - Added `.context/` directory to ignore alert files
