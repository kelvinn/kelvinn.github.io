# Air Quality Monitor

This script monitors NSW hazard reduction burns, current air quality, and weather forecasts to predict and detect poor air quality in Sydney.

## How it works

The script runs every 30 minutes via GitHub Actions and checks two types of risks:

### 1. Current Air Quality Alert
- Gets real-time air quality data for North Sydney from **PurpleAir** sensors
- Averages readings from nearby outdoor sensors
- Alerts if PM2.5 exceeds **35 µg/m³**
- **Higher priority** notifications (priority=2) for immediate action

### 2. Forecast Risk Alert
- Fetches current hazard reduction burns from NSW RFS (Rural Fire Service)
- Gets the 24-hour wind forecast for Sydney
- Applies a heuristic to determine if smoke will blow toward Sydney:
  - Fire in the west + eastern winds → risk
  - Fire in the south + northern winds → risk
  - Fire in the north + southern winds → risk

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

#### For Current Air Quality: `PURPLEAIR_API_KEY`

Get an API key from [PurpleAir](https://develop.purpleair.com/api/keys):
1. Sign up or log in at purpleair.com
2. Go to your account settings and create an API key
3. Add it as a secret named `PURPLEAIR_API_KEY`

**This is required for current AQI checks.** Without this key, the script will skip AQI monitoring.

#### For Wind Forecast: `WEATHER_API_KEY` (Optional)

Get a free API key from [OpenWeatherMap](https://openweathermap.org/api):
1. Sign up at openweathermap.org
2. Navigate to API keys
3. Copy your API key
4. Add it as a secret named `WEATHER_API_KEY`

This is only used for wind forecasts. Without this key, the script will skip forecast risk checks.

### Testing

You can test the workflow manually:
1. Go to Actions tab in GitHub
2. Select "Air Quality Monitor"
3. Click "Run workflow"

## Local Development

To run the script locally with Pushover notifications:

```bash
# Install dependencies
pip install requests

# Set the API keys
export PURPLEAIR_API_KEY="your-purpleair-key"
export WEATHER_API_KEY="your-openweathermap-key"
export PUSHOVER_API_KEY="your-pushover-api-key"
export PUSHOVER_USER_KEY="your-pushover-user-key"

# Run the script
python .github/scripts/air_quality_monitor.py
```

The script will send Pushover notifications directly when:
1. Current PM2.5 in North Sydney exceeds 35 µg/m³ (priority=2 - emergency)
2. Fires + wind direction predict smoke reaching Sydney (priority=1 - high)

## Data Sources

- **NSW RFS API**: `https://www.rfs.nsw.gov.au/api/feeds/`
- **Air Quality**: PurpleAir Sensor Network API
- **Weather Forecast**: OpenWeatherMap 5-day/3-hour forecast API

## Alert Output

When a risk is detected, the script:
1. Creates a JSON alert file in `.context/air_quality_alert.json`
2. Prints GitHub Actions annotations (visible in workflow logs)
3. Sends a Pushover notification:
   - **Priority 2** (emergency) for current AQI alerts
   - **Priority 1** (high) for forecast risk alerts

## AQI Threshold

The default threshold for PM2.5 is **35 µg/m³** in North Sydney. You can modify this by changing the `AQI_THRESHOLD` constant in `air_quality_monitor.py`.

## Finding PurpleAir Sensors

To see what sensors are available in your area, visit [PurpleAir Map](https://map.purpleair.com/). The script automatically finds all outdoor sensors within the search radius around North Sydney.
