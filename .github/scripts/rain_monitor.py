#!/usr/bin/env python3
"""
Rain Monitor for Neutral Bay, NSW, Australia.
Checks multiple weather sources for rain probability and sends notifications.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Neutral Bay, NSW coordinates
NEUTRAL_BAY_LAT = -33.8461
NEUTRAL_BAY_LON = 151.2389

# Notification thresholds
RAIN_PROBABILITY_4H_THRESHOLD = 50  # 50% chance in next 4 hours
RAIN_PROBABILITY_90M_THRESHOLD = 80  # 80% chance in next 90 minutes

# Weather API configurations
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

# Pushover API (for notifications)
PUSHOVER_API_KEY = os.getenv("PUSHOVER_API_KEY")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"

# Redis configuration (for rate limiting)
REDIS_URL = os.getenv("REDIS_URL")
REDIS_NOTIFICATION_KEY = "rain_monitor:last_notification"

# Rate limiting: once per calendar day
NOTIFICATION_COOLDOWN_HOURS = 24

# Blackout period: no notifications outside 7am-6pm (already enforced by workflow schedule)
# But we add an additional check here for safety
BLACKOUT_START_HOUR = 7
BLACKOUT_END_HOUR = 18

# BOM Radar URLs for Sydney
BOM_RADAR_ID = "IDR713"  # Sydney (Broadmeadow)
BOM_RADAR_URLS = {
    "512km": f"https://radar.bom.gov.au/radar/{BOM_RADAR_ID}.png",
    "256km": f"https://radar.bom.gov.au/radar/TAF/{BOM_RADAR_ID}.png",
}

# Initialize Redis client
_redis_client = None


def get_redis_client():
    """Get or create Redis client."""
    global _redis_client
    if _redis_client is not None:
        return _redis_client

    if not REDIS_AVAILABLE:
        logger.warning("redis package not installed, rate limiting disabled")
        return None

    if not REDIS_URL:
        logger.info("REDIS_URL not set, rate limiting disabled")
        return None

    try:
        _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        _redis_client.ping()
        logger.info("Redis connection established")
        return _redis_client
    except Exception as e:
        logger.warning(f"Failed to connect to Redis: {e}, rate limiting disabled")
        return None


def is_in_blackout_period() -> bool:
    """Check if current time is outside operating hours (7am-6pm)."""
    now = datetime.now()
    current_hour = now.hour

    return current_hour < BLACKOUT_START_HOUR or current_hour >= BLACKOUT_END_HOUR


def can_send_notification() -> tuple[bool, str]:
    """
    Check if a notification can be sent based on rate limiting (once per day) and blackout period.

    Returns:
        tuple: (can_send: bool, reason: str)
    """
    # Check blackout period first
    if is_in_blackout_period():
        return False, f"Outside operating hours ({BLACKOUT_START_HOUR}:00-{BLACKOUT_END_HOUR}:00)"

    # Check rate limiting with Redis
    client = get_redis_client()
    if client is None:
        # No Redis, allow notification (degraded mode)
        return True, "Rate limiting disabled (Redis unavailable)"

    try:
        today = datetime.now().date().isoformat()
        daily_key = f"{REDIS_NOTIFICATION_KEY}:{today}"

        last_notification_str = client.get(daily_key)
        if last_notification_str is None:
            return True, "First notification today"

        last_notification = datetime.fromisoformat(last_notification_str)
        return False, f"Already sent notification today at {last_notification.strftime('%H:%M')}"

    except Exception as e:
        logger.warning(f"Error checking rate limit: {e}, allowing notification")
        return True, "Rate limiting bypassed (error)"


def record_notification_sent():
    """Record that a notification was sent (once per calendar day)."""
    client = get_redis_client()
    if client is None:
        return

    try:
        today = datetime.now().date().isoformat()
        daily_key = f"{REDIS_NOTIFICATION_KEY}:{today}"

        client.setex(
            daily_key,
            timedelta(hours=48),
            datetime.now().isoformat()
        )
        logger.info(f"Notification recorded in Redis for {today}")
    except Exception as e:
        logger.warning(f"Failed to record notification: {e}")


def get_openweather_rain_probability() -> Optional[Dict]:
    """Get rain probability from OpenWeatherMap."""
    if not WEATHER_API_KEY:
        logger.warning("WEATHER_API_KEY not set, skipping OpenWeatherMap")
        return None

    logger.info("Fetching rain probability from OpenWeatherMap...")

    try:
        # Use One Call API 3.0 for hourly forecast
        url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            "lat": NEUTRAL_BAY_LAT,
            "lon": NEUTRAL_BAY_LON,
            "appid": WEATHER_API_KEY,
            "units": "metric",
            "exclude": "minutely,daily,alerts"
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        hourly = data.get("hourly", [])

        # Analyze next 4 hours (8 x 30-minute intervals)
        prob_4h = 0
        for i, hour in enumerate(hourly[:8]):
            pop = hour.get("pop", 0) * 100  # Convert to percentage
            prob_4h = max(prob_4h, pop)

        # Analyze next 90 minutes (first 2 intervals)
        prob_90m = 0
        for hour in hourly[:2]:
            pop = hour.get("pop", 0) * 100
            prob_90m = max(prob_90m, pop)

        # Get current conditions
        current = data.get("current", {})
        current_weather = current.get("weather", [{}])[0].get("description", "Unknown")

        result = {
            "source": "OpenWeatherMap",
            "probability_4h": round(prob_4h, 1),
            "probability_90m": round(prob_90m, 1),
            "current_condition": current_weather,
            "checked_at": datetime.now().isoformat()
        }

        logger.info(f"OpenWeatherMap: 4h={prob_4h:.1f}%, 90m={prob_90m:.1f}%")
        return result

    except requests.RequestException as e:
        logger.error(f"Error fetching OpenWeatherMap data: {e}")
        return None


def get_weatherstack_rain_probability() -> Optional[Dict]:
    """Get rain probability from Weatherstack."""
    if not WEATHERSTACK_API_KEY:
        logger.warning("WEATHERSTACK_API_KEY not set, skipping Weatherstack")
        return None

    logger.info("Fetching rain probability from Weatherstack...")

    try:
        # Current weather and forecast
        url = "http://api.weatherstack.com/current"
        params = {
            "access_key": WEATHERSTACK_API_KEY,
            "query": f"{NEUTRAL_BAY_LAT},{NEUTRAL_BAY_LON}",
            "forecast": "8"  # Next 8 hours (3-hour intervals)
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            logger.error(f"Weatherstack API error: {data['error']}")
            return None

        current = data.get("current", {})
        forecast = data.get("forecast", {})

        # Get probability of precipitation from forecast
        prob_4h = 0
        prob_90m = 0

        hourly_forecast = forecast.get("hourly", [])
        for i, hour in enumerate(hourly_forecast[:8]):
            # weatherstack uses "chanceofrain" or "precip"
            pop = hour.get("chanceofrain", 0) or hour.get("precip", 0) * 100
            if i < 2:  # First 2 hours
                prob_90m = max(prob_90m, pop)
            prob_4h = max(prob_4h, pop)

        result = {
            "source": "Weatherstack",
            "probability_4h": round(prob_4h, 1),
            "probability_90m": round(prob_90m, 1),
            "current_condition": current.get("weather_descriptions", ["Unknown"])[0],
            "checked_at": datetime.now().isoformat()
        }

        logger.info(f"Weatherstack: 4h={prob_4h:.1f}%, 90m={prob_90m:.1f}%")
        return result

    except requests.RequestException as e:
        logger.error(f"Error fetching Weatherstack data: {e}")
        return None


def get_weather_forecast_dot_gov_au() -> Optional[Dict]:
    """Get rain probability from BOM (Weather.gov.au API)."""
    logger.info("Fetching rain probability from BOM (weather.gov.au)...")

    try:
        # BOM provides forecast via weather.gov.au
        # Using the BOM forecast API
        url = f"https://api.weather.gov.au/forecasts/{NEUTRAL_BAY_LAT},{NEUTRAL_BAY_LON}"

        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Parse BOM data
        # Note: BOM uses different structure
        daily = data.get("data", {}).get("weather", [])

        prob_4h = 0
        prob_90m = 0

        # BOM forecast is by day, need to check hourly if available
        # Look for precip_prob in next periods
        for i, day in enumerate(daily[:2]):  # Check today and tomorrow
            for period in day.get("forecast_periods", [])[:8]:  # Up to 24 hours
                precip = period.get("precip_probability_max", 0)
                hour_index = i * 8 + period.get("index", 0)

                if hour_index < 3:  # First ~3 hours
                    prob_90m = max(prob_90m, precip)
                if hour_index < 8:  # First 4 hours
                    prob_4h = max(prob_4h, precip)

        result = {
            "source": "BOM (weather.gov.au)",
            "probability_4h": round(prob_4h, 1),
            "probability_90m": round(prob_90m, 1),
            "current_condition": daily[0].get("forecast_summary", "Unknown") if daily else "Unknown",
            "checked_at": datetime.now().isoformat()
        }

        logger.info(f"BOM: 4h={prob_4h:.1f}%, 90m={prob_90m:.1f}%")
        return result

    except requests.RequestException as e:
        logger.error(f"Error fetching BOM data: {e}")
        return None


def get_most_reliable_rain_probability() -> Dict:
    """
    Get rain probability from weather sources.
    Primary: OpenWeatherMap
    Fallback: Weatherstack (only used if OpenWeatherMap fails)
    """
    sources = []

    # Primary source: OpenWeatherMap
    openweather = get_openweather_rain_probability()
    if openweather:
        sources.append(openweather)

    # Fallback: Weatherstack (only if OpenWeatherMap is unavailable)
    if not sources:
        logger.info("OpenWeatherMap unavailable, trying Weatherstack as fallback...")
        weatherstack = get_weatherstack_rain_probability()
        if weatherstack:
            sources.append(weatherstack)

    if not sources:
        return {
            "error": "No weather data available",
            "probability_4h": 0,
            "probability_90m": 0,
            "sources": []
        }

    # Use the highest probability from available sources
    prob_4h = max(s.get("probability_4h", 0) for s in sources)
    prob_90m = max(s.get("probability_90m", 0) for s in sources)

    return {
        "probability_4h": prob_4h,
        "probability_90m": prob_90m,
        "sources": sources,
        "checked_at": datetime.now().isoformat(),
        "alert_4h": prob_4h >= RAIN_PROBABILITY_4H_THRESHOLD,
        "alert_90m": prob_90m >= RAIN_PROBABILITY_90M_THRESHOLD
    }


def get_bom_radar_url() -> str:
    """Get BOM radar image URL for Sydney."""
    return BOM_RADAR_URLS["512km"]


def check_rain_risk() -> Dict:
    """
    Check if there's a risk of rain in Neutral Bay.

    Returns:
        Dict with risk assessment
    """
    logger.info("Checking rain risk for Neutral Bay...")

    rain_data = get_most_reliable_rain_probability()

    if "error" in rain_data:
        return {
            "at_risk": False,
            "error": rain_data["error"],
            "checked_at": datetime.now().isoformat()
        }

    prob_4h = rain_data.get("probability_4h", 0)
    prob_90m = rain_data.get("probability_90m", 0)

    # Determine if alerts should be triggered
    alert_4h = prob_4h >= RAIN_PROBABILITY_4H_THRESHOLD
    alert_90m = prob_90m >= RAIN_PROBABILITY_90M_THRESHOLD

    result = {
        "at_risk": alert_4h or alert_90m,
        "probability_4h": prob_4h,
        "probability_90m": prob_90m,
        "alert_4h": alert_4h,
        "alert_90m": alert_90m,
        "sources": rain_data.get("sources", []),
        "checked_at": datetime.now().isoformat(),
        "location": "Neutral Bay, NSW"
    }

    logger.info(f"Rain risk check: 4h={prob_4h:.1f}% (threshold={RAIN_PROBABILITY_4H_THRESHOLD}%), "
                f"90m={prob_90m:.1f}% (threshold={RAIN_PROBABILITY_90M_THRESHOLD}%)")
    logger.info(f"Alerts: 4h={alert_4h}, 90m={alert_90m}")

    return result


def send_pushover_notification(title: str, message: str, priority: int = 0, attachment_url: str = None) -> bool:
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

        # Add attachment if provided (for radar image)
        # Note: Pushover supports image attachments but requires specific setup
        # For now, we'll include the URL in the message

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


def send_rain_notification(risk_data: Dict):
    """Send notification if rain risk is detected."""
    if not risk_data.get("at_risk", False):
        logger.info("No rain risk detected")
        return

    # Check rate limiting and blackout period
    can_send, reason = can_send_notification()
    if not can_send:
        logger.info(f"Notification skipped: {reason}")
        return

    logger.info(f"Notification allowed: {reason}")

    prob_4h = risk_data.get("probability_4h", 0)
    prob_90m = risk_data.get("probability_90m", 0)
    alert_4h = risk_data.get("alert_4h", False)
    alert_90m = risk_data.get("alert_90m", False)

    # Build alert output
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", ".context")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "rain_alert.json")
    with open(output_file, "w") as f:
        json.dump(risk_data, f, indent=2, default=str)

    logger.info(f"Alert written to {output_file}")

    # Print to stdout for GitHub Actions
    print(f"::warning::Rain Alert Detected for Neutral Bay!")
    print(f"::notice::4-hour probability: {prob_4h:.1f}% (threshold: {RAIN_PROBABILITY_4H_THRESHOLD}%)")
    print(f"::notice::90-minute probability: {prob_90m:.1f}% (threshold: {RAIN_PROBABILITY_90M_THRESHOLD}%)")

    for source in risk_data.get("sources", []):
        src_name = source.get("source", "Unknown")
        src_4h = source.get("probability_4h", 0)
        src_90m = source.get("probability_90m", 0)
        print(f"::notice::{src_name}: 4h={src_4h:.1f}%, 90m={src_90m:.1f}%")

    # Build Pushover message
    title = "Rain Alert - Neutral Bay"
    message_parts = []

    if alert_90m:
        message_parts.append(f"🌧️ HIGH PRIORITY: {prob_90m:.0f}% chance of rain in the next 90 minutes!")
        message_parts.append(f"Radar: {get_bom_radar_url()}")
    elif alert_4h:
        message_parts.append(f"🌂 Rain likely: {prob_4h:.0f}% chance in the next 4 hours")

    message_parts.append(f"\nProbabilities:")
    message_parts.append(f"  Next 90 min: {prob_90m:.1f}%")
    message_parts.append(f"  Next 4 hours: {prob_4h:.1f}%")

    message_parts.append(f"\nSource readings:")
    for source in risk_data.get("sources", []):
        src_name = source.get("source", "Unknown")
        src_4h = source.get("probability_4h", 0)
        src_90m = source.get("probability_90m", 0)
        current = source.get("current_condition", "Unknown")
        message_parts.append(f"  {src_name}: 4h={src_4h:.1f}%, 90m={src_90m:.1f}% (current: {current})")

    message_parts.append(f"\nBOM Radar: {get_bom_radar_url()}")

    message = "\n".join(message_parts)

    # Priority: 2 for 90m alert (high urgency), 1 for 4h alert
    priority = 2 if alert_90m else 1

    if send_pushover_notification(title, message, priority):
        record_notification_sent()


def main():
    """Main execution function."""
    logger.info("Starting Rain Monitor check for Neutral Bay...")

    # Check Redis connectivity
    if REDIS_URL and REDIS_AVAILABLE:
        redis_client = get_redis_client()
        if redis_client is None:
            logger.warning("Failed to connect to Redis, continuing with rate limiting disabled")

    # Check rain risk
    risk_data = check_rain_risk()

    # Send notification if needed
    send_rain_notification(risk_data)

    logger.info("Rain Monitor check complete")


if __name__ == "__main__":
    main()
