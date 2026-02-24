#!/usr/bin/env python3
"""
Temperature Monitor for Neutral Bay, NSW, Australia.
Checks if tomorrow's max temperature will exceed 29°C and sends notifications.
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
import requests

# Add src directory to path for db modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from db_notification import can_send_notification_db, record_notification_db, is_database_available

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Neutral Bay, NSW coordinates
NEUTRAL_BAY_LAT = -33.8461
NEUTRAL_BAY_LON = 151.2389

# Temperature threshold (in Celsius)
TEMP_THRESHOLD = 29

# Weather API configurations
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Pushover API (for notifications)
PUSHOVER_API_KEY = os.getenv("PUSHOVER_API_KEY")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"

# Notification source name for database
NOTIFICATION_SOURCE = "temperature"

# Rate limiting: once per calendar day
NOTIFICATION_COOLDOWN_HOURS = 24

# Blackout period: no notifications outside 7am-6pm
BLACKOUT_START_HOUR = 7
BLACKOUT_END_HOUR = 18


def is_in_blackout_period() -> bool:
    """Check if current time is outside operating hours (7am-6pm)."""
    now = datetime.now()
    current_hour = now.hour

    return current_hour < BLACKOUT_START_HOUR or current_hour >= BLACKOUT_END_HOUR


def can_send_notification(alert_type: Optional[str] = None) -> tuple[bool, str]:
    """
    Check if a notification can be sent based on rate limiting (once per day) and blackout period.

    Args:
        alert_type: Optional specific alert type (e.g., "tomorrow_hot")

    Returns:
        tuple: (can_send: bool, reason: str)
    """
    # Check blackout period first
    if is_in_blackout_period():
        return False, f"Outside operating hours ({BLACKOUT_START_HOUR}:00-{BLACKOUT_END_HOUR}:00)"

    # Check rate limiting with database
    return can_send_notification_db(NOTIFICATION_SOURCE, alert_type)


def record_notification_sent(alert_type: Optional[str] = None, message: str = ""):
    """Record that a notification was sent in the database."""
    record_notification_db(NOTIFICATION_SOURCE, message, alert_type)


def get_tomorrow_temperature() -> Optional[Dict]:
    """Get tomorrow's temperature forecast from OpenWeatherMap."""
    if not WEATHER_API_KEY:
        logger.warning("WEATHER_API_KEY not set, skipping temperature check")
        return None

    logger.info("Fetching temperature forecast from OpenWeatherMap...")

    try:
        # Use One Call API 3.0 for daily forecast
        url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            "lat": NEUTRAL_BAY_LAT,
            "lon": NEUTRAL_BAY_LON,
            "appid": WEATHER_API_KEY,
            "units": "metric",
            "exclude": "minutely,hourly,alerts"
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        daily = data.get("daily", [])

        if not daily:
            logger.warning("No daily forecast data available")
            return None

        # Get tomorrow's forecast (index 1, as index 0 is today)
        tomorrow = daily[1] if len(daily) > 1 else daily[0]

        temp = tomorrow.get("temp", {})
        max_temp = temp.get("max", 0)
        min_temp = temp.get("min", 0)
        weather = tomorrow.get("weather", [{}])[0]
        weather_desc = weather.get("description", "Unknown")
        weather_icon = weather.get("icon", "")

        # Also get today's max for comparison
        today = daily[0]
        today_temp = today.get("temp", {})
        today_max = today_temp.get("max", 0)

        result = {
            "source": "OpenWeatherMap",
            "tomorrow_max": round(max_temp, 1),
            "tomorrow_min": round(min_temp, 1),
            "today_max": round(today_max, 1),
            "weather": weather_desc,
            "icon": weather_icon,
            "checked_at": datetime.now().isoformat()
        }

        logger.info(f"OpenWeatherMap: Tomorrow max={max_temp:.1f}°C, min={min_temp:.1f}°C, today max={today_max:.1f}°C")
        return result

    except requests.RequestException as e:
        logger.error(f"Error fetching OpenWeatherMap data: {e}")
        return None


def get_weatherstack_temperature() -> Optional[Dict]:
    """Get tomorrow's temperature from Weatherstack as fallback."""
    if not os.getenv("WEATHERSTACK_API_KEY"):
        logger.warning("WEATHERSTACK_API_KEY not set, skipping Weatherstack")
        return None

    logger.info("Fetching temperature from Weatherstack...")

    try:
        url = "http://api.weatherstack.com/forecast"
        params = {
            "access_key": os.getenv("WEATHERSTACK_API_KEY"),
            "query": f"{NEUTRAL_BAY_LAT},{NEUTRAL_BAY_LON}",
            "forecast_days": 2
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            logger.error(f"Weatherstack API error: {data['error']}")
            return None

        # Weatherstack forecast structure
        forecast = data.get("forecast", {})

        # Get tomorrow's data (second day)
        # The forecast contains dates as keys
        dates = sorted(forecast.keys())
        tomorrow_date = dates[1] if len(dates) > 1 else dates[0]
        tomorrow = forecast.get(tomorrow_date, {})
        today = forecast.get(dates[0], {})

        maxtemp = tomorrow.get("maxtemp", 0)
        mintemp = tomorrow.get("mintemp", 0)
        today_maxtemp = today.get("maxtemp", 0)

        result = {
            "source": "Weatherstack",
            "tomorrow_max": maxtemp,
            "tomorrow_min": mintemp,
            "today_max": today_maxtemp,
            "weather": tomorrow.get("weather_descriptions", ["Unknown"])[0],
            "checked_at": datetime.now().isoformat()
        }

        logger.info(f"Weatherstack: Tomorrow max={maxtemp}°C, min={mintemp}°C")
        return result

    except requests.RequestException as e:
        logger.error(f"Error fetching Weatherstack data: {e}")
        return None


def get_temperature_forecast() -> Dict:
    """
    Get temperature forecast from available sources.
    Primary: OpenWeatherMap
    Fallback: Weatherstack
    """
    sources = []

    # Primary source: OpenWeatherMap
    openweather = get_tomorrow_temperature()
    if openweather:
        sources.append(openweather)

    # Fallback: Weatherstack (only if OpenWeatherMap is unavailable)
    if not sources:
        logger.info("OpenWeatherMap unavailable, trying Weatherstack as fallback...")
        weatherstack = get_weatherstack_temperature()
        if weatherstack:
            sources.append(weatherstack)

    if not sources:
        return {
            "error": "No temperature data available",
            "tomorrow_max": 0,
            "sources": []
        }

    # Use the highest max temperature from available sources
    max_temp = max(s.get("tomorrow_max", 0) for s in sources)
    min_temp = min(s.get("tomorrow_min", 0) for s in sources) if sources else 0

    # Get today's max from primary source
    today_max = sources[0].get("today_max", 0) if sources else 0

    return {
        "tomorrow_max": max_temp,
        "tomorrow_min": min_temp,
        "today_max": today_max,
        "sources": sources,
        "checked_at": datetime.now().isoformat(),
        "will_be_hot": max_temp >= TEMP_THRESHOLD
    }


def check_temperature_risk() -> Dict:
    """
    Check if tomorrow will be hot in Neutral Bay.

    Returns:
        Dict with temperature risk assessment
    """
    logger.info("Checking temperature forecast for Neutral Bay...")

    temp_data = get_temperature_forecast()

    if "error" in temp_data:
        return {
            "at_risk": False,
            "error": temp_data["error"],
            "checked_at": datetime.now().isoformat()
        }

    tomorrow_max = temp_data.get("tomorrow_max", 0)
    tomorrow_min = temp_data.get("tomorrow_min", 0)
    today_max = temp_data.get("today_max", 0)

    # Determine if alert should be triggered
    alert = tomorrow_max >= TEMP_THRESHOLD

    result = {
        "at_risk": alert,
        "tomorrow_max": tomorrow_max,
        "tomorrow_min": tomorrow_min,
        "today_max": today_max,
        "threshold": TEMP_THRESHOLD,
        "sources": temp_data.get("sources", []),
        "checked_at": datetime.now().isoformat(),
        "location": "Neutral Bay, NSW"
    }

    logger.info(f"Temperature check: Tomorrow max={tomorrow_max:.1f}°C (threshold={TEMP_THRESHOLD}°C)")
    logger.info(f"Alert: {alert}")

    return result


def send_pushover_notification(title: str, message: str, priority: int = 0) -> bool:
    """Send a notification via Pushover."""
    if not PUSHOVER_API_KEY or not PUSHOVER_USER_KEY:
        logger.warning("PUSHOVER_API_KEY or PUSHOVER_USER_KEY not set, skipping Pushover notification")
        return False

    try:
        data = {
            "token": PUSHOVER_API_KEY,
            "user": PUSHOVER_USER_KEY,
            "title": title,
            "message": message,
            "priority": priority
        }

        response = requests.post(
            PUSHOVER_API_URL,
            data=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        if result.get("status") == 1:
            logger.info(f"Pushover notification sent: {title}")
            return True
        else:
            logger.error(f"Pushover notification failed: {result}")
            return False
    except requests.RequestException as e:
        logger.error(f"Error sending Pushover notification: {e}")
        return False


def send_temperature_notification(risk_data: Dict, db_available: bool = True):
    """Send notification if tomorrow will be hot.

    Args:
        risk_data: The risk data from check_temperature_risk()
        db_available: Whether the database is available
    """
    if not risk_data.get("at_risk", False):
        logger.info("No hot weather risk detected")
        return

    # If database is unavailable, skip notification
    if not db_available:
        logger.warning("Database unavailable - skipping notification")
        return

    # Check rate limiting and blackout period
    can_send, reason = can_send_notification(alert_type="tomorrow_hot")
    if not can_send:
        logger.info(f"Notification skipped: {reason}")
        return

    logger.info(f"Notification allowed: {reason}")

    tomorrow_max = risk_data.get("tomorrow_max", 0)
    tomorrow_min = risk_data.get("tomorrow_min", 0)
    today_max = risk_data.get("today_max", 0)

    # Build alert output
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", ".context")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "temperature_alert.json")
    with open(output_file, "w") as f:
        json.dump(risk_data, f, indent=2, default=str)

    logger.info(f"Alert written to {output_file}")

    # Print to stdout for GitHub Actions
    print("::warning::Hot Weather Alert Detected for Neutral Bay!")
    print(f"::notice::Tomorrow's max temperature: {tomorrow_max:.1f}°C (threshold: {TEMP_THRESHOLD}°C)")
    print(f"::notice::Tomorrow's min: {tomorrow_min:.1f}°C, Today's max: {today_max:.1f}°C")

    for source in risk_data.get("sources", []):
        src_name = source.get("source", "Unknown")
        src_max = source.get("tomorrow_max", 0)
        src_weather = source.get("weather", "Unknown")
        print(f"::notice::{src_name}: {src_max:.1f}°C ({src_weather})")

    # Build Pushover message
    title = "Hot Weather Alert - Neutral Bay"
    message_parts = []

    message_parts.append(f"🔥 Tomorrow's max: {tomorrow_max:.1f}°C (threshold: {TEMP_THRESHOLD}°C)")
    message_parts.append(f"Expected range: {tomorrow_min:.1f}°C - {tomorrow_max:.1f}°C")
    message_parts.append(f"Today's max: {today_max:.1f}°C")

    message_parts.append("\nSource readings:")
    for source in risk_data.get("sources", []):
        src_name = source.get("source", "Unknown")
        src_max = source.get("tomorrow_max", 0)
        src_min = source.get("tomorrow_min", 0)
        src_weather = source.get("weather", "Unknown")
        message_parts.append(f"  {src_name}: {src_min:.1f}°C - {src_max:.1f}°C ({src_weather})")

    message = "\n".join(message_parts)

    # Priority: 1 for hot weather
    priority = 1

    if send_pushover_notification(title, message, priority):
        record_notification_sent(alert_type="tomorrow_hot", message=message[:500])


def main():
    """Main execution function."""
    logger.info("Starting Temperature Monitor check for Neutral Bay...")

    # Check database availability - if unavailable, skip notification
    db_available = is_database_available()
    if not db_available:
        logger.warning("Database unavailable - notifications will be skipped")

    # Check temperature risk
    risk_data = check_temperature_risk()

    # Send notification if needed
    send_temperature_notification(risk_data, db_available)

    logger.info("Temperature Monitor check complete")


if __name__ == "__main__":
    main()
