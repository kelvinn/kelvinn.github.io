# Air Quality Monitor

This script monitors NSW hazard reduction burns and combines them with weather forecasts to predict potential poor air quality days in Sydney.

## How it works

The script runs every 30 minutes via GitHub Actions and:

1. Fetches current hazard reduction burns from NSW RFS (Rural Fire Service)
2. Gets the 24-hour wind forecast for Sydney
3. Applies a heuristic to determine if smoke will blow toward Sydney:
   - Fire in the west + eastern winds → risk
   - Fire in the south + northern winds → risk
   - Fire in the north + southern winds → risk
4. Sends a Pushover notification if risk conditions are met

## Setup

### Required GitHub Secrets

Add the following secrets to your GitHub repository (Settings → Secrets and variables → Actions):

#### For Notifications: `PUSHOVER_API_KEY` and `PUSHOVER_USER_KEY`

1. Sign up at [Pushover.net](https://pushover.net)
2. Create an application to get your API Token
3. Find your User Key on the Pushover dashboard
4. Add them as secrets:
   - `PUSHOVER_API_KEY` - Your application's API token
   - `PUSHOVER_USER_KEY` - Your user key

#### Optional (Recommended): `WEATHER_API_KEY`

Get a free API key from [OpenWeatherMap](https://openweathermap.org/api):
1. Sign up at openweathermap.org
2. Navigate to API keys
3. Copy your API key
4. Add it as a secret named `WEATHER_API_KEY`

Without this key, the script will use mock wind data for testing.

### Testing

You can test the workflow manually:
1. Go to Actions tab in GitHub
2. Select "Air Quality Monitor"
3. Click "Run workflow"

## Local Development

To run the script locally:

```bash
# Install dependencies
pip install requests

# Set the weather API key (optional)
export WEATHER_API_KEY="your-key-here"

# Run the script
python .github/scripts/air_quality_monitor.py
```

## Data Sources

- **NSW RFS API**: `https://www.rfs.nsw.gov.au/api/feeds/`
- **Weather**: OpenWeatherMap API (or mock data if no key)

## Alert Output

When a risk is detected, the script:
1. Creates a JSON alert file in `.context/air_quality_alert.json`
2. Prints GitHub Actions annotations (visible in workflow logs)
3. Sends a Pushover notification with priority=1 (high priority)
