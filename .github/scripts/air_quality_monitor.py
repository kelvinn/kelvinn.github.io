#!/usr/bin/env python3
"""
Air Quality Monitor for NSW, Australia.
Checks planned hazard reduction burns and wind direction to predict poor air quality.
"""

import os
import json
import logging
import math
from datetime import datetime, timedelta, time
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

# Sydney approximate coordinates (for determining directions)
SYDNEY_LAT = -33.8688
SYDNEY_LON = 151.2093

# North Sydney coordinates for AQI checking
NORTH_SYDNEY_LAT = -33.8391
NORTH_SYDNEY_LON = 151.2069

# AQI threshold for North Sydney (PM2.5 in µg/m³)
AQI_THRESHOLD = 35

# AQI threshold for regional validation
REGIONAL_AQI_THRESHOLD = 50

# Sydney outskirts regions for validation smoke detection
# These regions surround Sydney and help validate smoke direction
SYDNEY_OUTSKIRTS = {
    "north": {
        "name": "North Sydney (Brooklyn/Central Coast)",
        "lat": -33.5300,
        "lon": 151.2500,
        "description": "North of Sydney"
    },
    "south": {
        "name": "South Sydney (Wollongong area)",
        "lat": -34.2000,
        "lon": 150.9000,
        "description": "South of Sydney"
    },
    "east": {
        "name": "East Sydney (Northern Beaches/Coast)",
        "lat": -33.7500,
        "lon": 151.3500,
        "description": "East of Sydney"
    },
    "west": {
        "name": "West Sydney (Blue Mountains)",
        "lat": -33.7000,
        "lon": 150.3000,
        "description": "West of Sydney"
    },
    "northeast": {
        "name": "Northeast Sydney (Newport/Avalon)",
        "lat": -33.6500,
        "lon": 151.3500,
        "description": "Northeast of Sydney"
    },
    "southeast": {
        "name": "Southeast Sydney (Royal National Park area)",
        "lat": -34.1000,
        "lon": 151.2000,
        "description": "Southeast of Sydney"
    },
    "northwest": {
        "name": "Northwest Sydney (Hawkesbury)",
        "lat": -33.6000,
        "lon": 150.9000,
        "description": "Northwest of Sydney"
    },
    "southwest": {
        "name": "Southwest Sydney (Campbelltown/Wollondilly)",
        "lat": -34.0500,
        "lon": 150.8000,
        "description": "Southwest of Sydney"
    }
}

# Mapping from fire direction to expected smoke region
# Fire in X + winds from Y = smoke should be in Z
FIRE_WIND_TO_SMOKE_REGION = {
    # Fire south of Sydney + northern winds = smoke in South Sydney
    "south": {
        "N": "south",
        "NE": "south",
        "NW": "southwest"
    },
    # Fire north of Sydney + southern winds = smoke in North Sydney
    "north": {
        "S": "north",
        "SE": "northeast",
        "SW": "northwest"
    },
    # Fire east of Sydney + western winds = smoke in East Sydney
    "east": {
        "W": "east",
        "NW": "northeast",
        "SW": "southeast"
    },
    # Fire west of Sydney + eastern winds = smoke in West Sydney
    "west": {
        "E": "west",
        "NE": "northwest",
        "SE": "southwest"
    },
    # Fire southeast of Sydney + northwest winds = smoke in Southeast Sydney
    "southeast": {
        "NW": "southeast",
        "N": "south",
        "W": "east"
    },
    # Fire southwest of Sydney + northeast winds = smoke in Southwest Sydney
    "southwest": {
        "NE": "southwest",
        "N": "west",
        "E": "south"
    },
    # Fire northeast of Sydney + southwest winds = smoke in Northeast Sydney
    "northeast": {
        "SW": "northeast",
        "S": "east",
        "W": "north"
    },
    # Fire northwest of Sydney + southeast winds = smoke in Northwest Sydney
    "northwest": {
        "SE": "northwest",
        "S": "west",
        "E": "north"
    }
}

# NSW RFS API endpoints
NSW_RFS_INCIDENTS_URL = "https://www.rfs.nsw.gov.au/feeds/majorIncidents.json"

# OpenWeatherMap API (for wind forecast only)
WEATHER_API_BASE = "https://api.openweathermap.org/data/3.0/onecall"
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# PurpleAir API (for AQI)
PURPLEAIR_API_KEY = os.getenv("PURPLEAIR_API_KEY")
PURPLEAIR_API_BASE = "https://api.purpleair.com/v1"

# Pushover API (for notifications)
PUSHOVER_API_KEY = os.getenv("PUSHOVER_API_KEY")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"

# Redis configuration (for rate limiting)
REDIS_URL = os.getenv("REDIS_URL")
REDIS_NOTIFICATION_KEY = "air_quality_monitor:last_notification"

# Rate limiting: once per calendar day
NOTIFICATION_COOLDOWN_HOURS = 24  # Fallback to 24h if Redis unavailable

# Blackout period: no notifications between these hours (24-hour format)
BLACKOUT_START_HOUR = 22  # 10:00 PM
BLACKOUT_END_HOUR = 6     # 6:00 AM

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
        # Test connection
        _redis_client.ping()
        logger.info("Redis connection established")
        return _redis_client
    except Exception as e:
        logger.warning(f"Failed to connect to Redis: {e}, rate limiting disabled")
        return None


def is_in_blackout_period() -> bool:
    """
    Check if current time is within the blackout period.
    Blackout: 10:00 PM to 6:00 AM.
    """
    now = datetime.now()
    current_hour = now.hour

    if BLACKOUT_START_HOUR > BLACKOUT_END_HOUR:
        # Blackout spans midnight (e.g., 22:00 to 06:00)
        return current_hour >= BLACKOUT_START_HOUR or current_hour < BLACKOUT_END_HOUR
    else:
        # Blackout within same day (e.g., 02:00 to 06:00)
        return BLACKOUT_START_HOUR <= current_hour < BLACKOUT_END_HOUR


def can_send_notification() -> tuple[bool, str]:
    """
    Check if a notification can be sent based on rate limiting (once per day) and blackout period.

    Returns:
        tuple: (can_send: bool, reason: str)
    """
    # Check blackout period first
    if is_in_blackout_period():
        return False, f"Blackout period (between {BLACKOUT_START_HOUR}:00 and {BLACKOUT_END_HOUR}:00)"

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
            # No notification sent today, allow
            return True, "First notification today"

        # Already sent a notification today
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

        # Set key to expire at end of day (roughly 24 hours from now)
        # This ensures the key is available for the rest of today and expires tomorrow
        client.setex(
            daily_key,
            timedelta(hours=48),  # Keep for 48 hours to cover edge cases
            datetime.now().isoformat()
        )
        logger.info(f"Notification recorded in Redis for {today}")
    except Exception as e:
        logger.warning(f"Failed to record notification: {e}")

# North Sydney PurpleAir sensor IDs (you can add more sensors here)
# Find sensors at: https://map.purpleair.com/
NORTH_SYDNEY_SENSORS = [
    # Sydney area sensors - add more as needed
    # You can find sensor IDs by clicking on sensors in the PurpleAir map
    # and extracting the ID from the URL
]


class Burn:
    """Represents a hazard reduction burn or incident."""

    def __init__(self, data: Dict):
        self.id = data.get("id", "")
        self.title = data.get("title", "")
        self.description = data.get("description", "")
        self.category = data.get("category", "")
        self.latitude = data.get("latitude", 0.0)
        self.longitude = data.get("longitude", 0.0)
        self.pub_date = data.get("pubDate", "")
        self.guid = data.get("guid", "")

    @property
    def is_burn(self) -> bool:
        """Check if this is a hazard reduction burn."""
        burn_keywords = ["burn", "hazard reduction", "back burn"]
        title_lower = self.title.lower()
        desc_lower = self.description.lower()
        return any(keyword in title_lower or keyword in desc_lower for keyword in burn_keywords)

    def get_direction_from_sydney(self) -> str:
        """Get the cardinal direction of this burn from Sydney."""
        lat_diff = self.latitude - SYDNEY_LAT
        lon_diff = self.longitude - SYDNEY_LON

        # Calculate angle from Sydney
        import math
        angle = math.degrees(math.atan2(lat_diff, lon_diff))
        if angle < 0:
            angle += 360

        # Convert angle to 8-point cardinal direction
        # 0=E, 45=NE, 90=N, 135=NW, 180=W, 225=SW, 270=S, 315=SE
        directions = ["east", "northeast", "north", "northwest", "west", "southwest", "south", "southeast"]
        index = round(angle / 45) % 8
        return directions[index]

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "direction_from_sydney": self.get_direction_from_sydney(),
            "pub_date": self.pub_date
        }


def fetch_nsw_rfs_incidents() -> List[Burn]:
    """Fetch incidents from NSW RFS API."""
    logger.info("Fetching NSW RFS incidents...")

    try:
        # Try major incidents feed
        response = requests.get(NSW_RFS_INCIDENTS_URL, timeout=30)
        response.raise_for_status()
        data = response.json()

        burns = []
        if isinstance(data, dict) and "features" in data:
            # GeoJSON format
            for feature in data["features"]:
                props = feature.get("properties", {})
                geometry = feature.get("geometry", {})
                if geometry and "coordinates" in geometry:
                    # GeoJSON is [lon, lat]
                    props["longitude"] = geometry["coordinates"][0]
                    props["latitude"] = geometry["coordinates"][1]
                burns.append(Burn(props))
        elif isinstance(data, list):
            for item in data:
                burns.append(Burn(item))
        else:
            logger.warning(f"Unexpected data format: {type(data)}")

        logger.info(f"Found {len(burns)} incidents")
        return burns

    except requests.RequestException as e:
        logger.error(f"Error fetching NSW RFS incidents: {e}")
        return []


def fetch_nsw_rfs_burns() -> List[Burn]:
    """Fetch hazard reduction burns from NSW RFS."""
    # The major incidents feed includes all incidents, we filter for burns in the main function
    return []


def get_wind_forecast(lat: float = SYDNEY_LAT, lon: float = SYDNEY_LON) -> List[Dict]:
    """Get wind forecast from OpenWeatherMap."""
    if not WEATHER_API_KEY:
        logger.warning("WEATHER_API_KEY not set, using default wind data")
        # Return mock data for testing
        return [
            {"time": datetime.now() + timedelta(hours=h), "direction": "E", "speed": 15}
            for h in range(0, 24, 3)
        ]

    logger.info(f"Fetching weather forecast for {lat}, {lon}...")

    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        forecasts = []
        for item in data.get("list", []):
            dt = datetime.fromtimestamp(item.get("dt", 0))
            wind = item.get("wind", {})
            wind_deg = wind.get("deg", 0)

            # Convert degrees to cardinal direction
            directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
            direction = directions[int((wind_deg + 22.5) / 45) % 8]

            forecasts.append({
                "time": dt,
                "direction": direction,
                "degrees": wind_deg,
                "speed": wind.get("speed", 0)
            })

        logger.info(f"Retrieved {len(forecasts)} forecast entries")
        return forecasts

    except requests.RequestException as e:
        logger.error(f"Error fetching weather forecast: {e}")
        return []


def check_regional_aqi_validation(fire_direction: str, wind_directions: List[str]) -> Dict:
    """
    Check if smoke is being detected in the expected region based on fire location and wind direction.
    This validates that the fire + wind combination is actually producing smoke in the expected area.

    Args:
        fire_direction: Direction of fire from Sydney (e.g., "south", "north", "southeast")
        wind_directions: List of forecast wind directions (e.g., ["N", "NE", "NW"])

    Returns:
        Dict with validation results
    """
    if not PURPLEAIR_API_KEY:
        return {
            "validated": False,
            "reason": "PurpleAir API not available for validation"
        }

    # Check which regions we should validate based on wind directions
    regions_to_check = []

    for wind_dir in wind_directions:
        if fire_direction in FIRE_WIND_TO_SMOKE_REGION:
            if wind_dir in FIRE_WIND_TO_SMOKE_REGION[fire_direction]:
                region_key = FIRE_WIND_TO_SMOKE_REGION[fire_direction][wind_dir]
                if region_key in SYDNEY_OUTSKIRTS and region_key not in regions_to_check:
                    regions_to_check.append(region_key)

    if not regions_to_check:
        return {
            "validated": False,
            "reason": f"No validation regions found for fire {fire_direction} with winds {wind_directions}"
        }

    logger.info(f"Validating smoke detection in regions: {regions_to_check}")

    regional_results = []
    for region_key in regions_to_check:
        region = SYDNEY_OUTSKIRTS[region_key]
        aqi_data = get_current_aqi(
            lat=region["lat"],
            lon=region["lon"],
            search_radius_km=25  # Larger radius for regional areas
        )

        if aqi_data:
            aqi_value = aqi_data.get("aqi", 0)
            is_above_threshold = aqi_value > REGIONAL_AQI_THRESHOLD

            result = {
                "region": region_key,
                "region_name": region["name"],
                "aqi": aqi_value,
                "aqi_description": aqi_data.get("aqi_description", ""),
                "pm2_5": aqi_data.get("pm2_5", 0),
                "above_threshold": is_above_threshold,
                "sensor_count": aqi_data.get("sensor_count", 0)
            }
            regional_results.append(result)

            logger.info(f"Regional AQI check {region_key}: AQI={aqi_value}, threshold={REGIONAL_AQI_THRESHOLD}, above={is_above_threshold}")
        else:
            regional_results.append({
                "region": region_key,
                "region_name": region["name"],
                "aqi": None,
                "error": "No data available"
            })
            logger.warning(f"No AQI data available for region {region_key}")

    # Determine if validation passed
    # Validation passes if at least one expected region shows elevated AQI
    validation_passed = any(
        r.get("above_threshold", False) or (r.get("aqi", 0) > REGIONAL_AQI_THRESHOLD if r.get("aqi") else False)
        for r in regional_results
    )

    # Find the highest AQI reading
    max_aqi = 0
    max_aqi_region = None
    for r in regional_results:
        if r.get("aqi") and r["aqi"] > max_aqi:
            max_aqi = r["aqi"]
            max_aqi_region = r["region_name"]

    return {
        "validated": validation_passed,
        "fire_direction": fire_direction,
        "wind_directions": wind_directions,
        "regions_checked": regions_to_check,
        "regional_results": regional_results,
        "max_aqi": max_aqi,
        "max_aqi_region": max_aqi_region,
        "validation_summary": (
            f"Smoke detected in {max_aqi_region} (AQI: {max_aqi})" if validation_passed
            else f"No elevated AQI (> {REGIONAL_AQI_THRESHOLD}) detected in expected regions"
        )
    }


def get_current_aqi(lat: float = NORTH_SYDNEY_LAT, lon: float = NORTH_SYDNEY_LON, search_radius_km: int = 10) -> Optional[Dict]:
    """
    Get current air quality data from PurpleAir sensors.

    Args:
        lat: Latitude for search center
        lon: Longitude for search center
        search_radius_km: Search radius in kilometers

    Returns dict with AQI data or None if unavailable.
    """
    api_key = PURPLEAIR_API_KEY

    if not api_key:
        logger.warning("PURPLEAIR_API_KEY not set, skipping AQI check")
        return None

    logger.info(f"Fetching current AQI for North Sydney ({lat}, {lon})...")

    try:
        # Step 1: Find nearby sensors using location-based search
        # Note: Using max_distance parameter which seems to work better than bounding box
        headers = {"X-API-Key": api_key}
        search_params = {
            "fields": "name,pm2.5_atm,latitude,longitude,last_seen",
            "location_type": 0  # Outdoor sensors only
        }

        # Try using max_distance search with center point
        url = f"{PURPLEAIR_API_BASE}/sensors"
        search_params["lat"] = lat
        search_params["lon"] = lon
        search_params["max_distance"] = 50000  # 50km radius

        response = requests.get(url, headers=headers, params=search_params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if "data" not in data or len(data["data"]) == 0:
            logger.warning("No PurpleAir sensors found in area")
            return None

        # Step 2: Get readings from all nearby sensors
        sensors = data.get("data", [])
        fields = data.get("fields", [])

        # Map field names to indices
        field_index = {field: i for i, field in enumerate(fields)}

        pm25_readings = []

        for sensor in sensors:
            # Parse sensor data based on field positions
            sensor_id = sensor[field_index.get("sensor_index", 0)] if len(sensor) > 0 else None
            name = sensor[field_index.get("name", 2)] if len(sensor) > 2 else "Unknown"
            pm25 = sensor[field_index.get("pm2.5_atm", 5)] if "pm2.5_atm" in field_index and len(sensor) > field_index["pm2.5_atm"] else None
            sensor_lat = sensor[field_index.get("latitude", 3)] if len(sensor) > 3 else None
            sensor_lon = sensor[field_index.get("longitude", 4)] if len(sensor) > 4 else None
            last_seen = sensor[field_index.get("last_seen", 1)] if len(sensor) > 1 else None

            # Filter by actual distance (in case API doesn't filter correctly)
            if sensor_lat is not None and sensor_lon is not None:
                # Calculate distance using simple approximation
                lat_diff = sensor_lat - lat
                lon_diff = sensor_lon - lon
                distance_km = ((lat_diff * 111) ** 2 + (lon_diff * 111 * abs(lat / 90)) ** 2) ** 0.5 * 100

                # Only include sensors within 50km
                if distance_km > 50:
                    continue

            # Skip sensors without recent data (older than 1 hour)
            if last_seen:
                last_seen_time = datetime.fromtimestamp(last_seen)
                if datetime.now() - last_seen_time > timedelta(hours=1):
                    logger.debug(f"Skipping {name}: data too old ({last_seen_time})")
                    continue

            if pm25 is not None:
                pm25_readings.append({
                    "sensor_id": sensor_id,
                    "name": name,
                    "pm2_5": pm25,
                    "latitude": sensor_lat,
                    "longitude": sensor_lon
                })

        if not pm25_readings:
            logger.warning("No recent PurpleAir data available")
            return None

        # Calculate average PM2.5
        avg_pm25 = sum(r["pm2_5"] for r in pm25_readings) / len(pm25_readings)

        # Calculate AQI from PM2.5 using US EPA formula
        # PM2.5 breakpoints for AQI calculation
        def pm25_to_aqi(pm25):
            if pm25 <= 12.0:
                return (50 / 12.0) * pm25
            elif pm25 <= 35.4:
                return 50 + ((49 / 23.4) * (pm25 - 12))
            elif pm25 <= 55.4:
                return 100 + ((49 / 20.0) * (pm25 - 35.4))
            elif pm25 <= 150.4:
                return 150 + ((49 / 95.0) * (pm25 - 55.4))
            elif pm25 <= 250.4:
                return 200 + ((99 / 100.0) * (pm25 - 150.4))
            else:
                return 300 + ((199 / 100.0) * (pm25 - 250.4))

        aqi = int(pm25_to_aqi(avg_pm25))

        # Get AQI description
        if aqi <= 50:
            aqi_desc = "Good"
        elif aqi <= 100:
            aqi_desc = "Moderate"
        elif aqi <= 150:
            aqi_desc = "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            aqi_desc = "Unhealthy"
        elif aqi <= 300:
            aqi_desc = "Very Unhealthy"
        else:
            aqi_desc = "Hazardous"

        result = {
            "aqi": aqi,
            "aqi_description": aqi_desc,
            "pm2_5": round(avg_pm25, 1),  # PM2.5 in µg/m³
            "sensor_count": len(pm25_readings),
            "sensors": pm25_readings,
            "checked_at": datetime.now().isoformat(),
            "source": "PurpleAir"
        }

        logger.info(f"PurpleAir AQI: {aqi} ({aqi_desc}), PM2.5: {avg_pm25:.1f} µg/m³ from {len(pm25_readings)} sensor(s)")
        return result

    except requests.RequestException as e:
        logger.error(f"Error fetching PurpleAir data: {e}")
        return None


def check_current_aqi_risk(aqi_data: Optional[Dict], threshold: float = AQI_THRESHOLD) -> Dict:
    """
    Check if current AQI in North Sydney exceeds threshold.

    Args:
        aqi_data: AQI data from get_current_aqi()
        threshold: PM2.5 threshold in µg/m³ (default: 35)

    Returns:
        Dict with risk information
    """
    if not aqi_data:
        return {
            "at_risk": False,
            "reason": "AQI data unavailable"
        }

    pm2_5 = aqi_data.get("pm2_5", 0)

    if pm2_5 > threshold:
        return {
            "at_risk": True,
            "reason": f"Current PM2.5 ({pm2_5:.1f} µg/m³) exceeds threshold ({threshold} µg/m³)",
            "aqi_data": aqi_data
        }

    return {
        "at_risk": False,
        "reason": f"Current PM2.5 ({pm2_5:.1f} µg/m³) below threshold ({threshold} µg/m³)",
        "aqi_data": aqi_data
    }


def check_air_quality_risk(burns: List[Burn], wind_forecast: List[Dict]) -> Dict:
    """
    Check if there's a risk of poor air quality based on burn locations and wind direction.

    Heuristic:
    - Fire in west + eastern winds = risk
    - Fire in south + northern winds = risk
    - Fire in north + southern winds = risk
    - Fire in SE + NW winds = risk (smoke toward NE Sydney)

    Now includes regional AQI validation to confirm smoke is actually being detected.
    """
    risk_factors = []

    # Get unique wind directions for next 24 hours
    next_24h = datetime.now() + timedelta(hours=24)
    relevant_forecasts = [
        f for f in wind_forecast
        if f["time"] <= next_24h
    ]

    wind_directions = list(set(f["direction"] for f in relevant_forecasts))

    # Check each burn
    for burn in burns:
        if burn.latitude == 0 and burn.longitude == 0:
            continue

        direction = burn.get_direction_from_sydney()

        # Check if wind will blow smoke toward Sydney
        at_risk = False
        risk_reasons = []
        matching_winds = []

        # Check all 8 directions
        if direction == "west":
            # West fire needs eastern winds (E, SE, NE)
            easterly = set(wind_directions) & {"E", "SE", "NE"}
            if easterly:
                at_risk = True
                matching_winds = list(easterly)
                risk_reasons.append(f"Fire west of Sydney with {', '.join(easterly)} winds forecast")

        elif direction == "south":
            # South fire needs northern winds (N, NE, NW)
            northerly = set(wind_directions) & {"N", "NE", "NW"}
            if northerly:
                at_risk = True
                matching_winds = list(northerly)
                risk_reasons.append(f"Fire south of Sydney with {', '.join(northerly)} winds forecast")

        elif direction == "north":
            # North fire needs southern winds (S, SE, SW)
            southerly = set(wind_directions) & {"S", "SE", "SW"}
            if southerly:
                at_risk = True
                matching_winds = list(southerly)
                risk_reasons.append(f"Fire north of Sydney with {', '.join(southerly)} winds forecast")

        elif direction == "east":
            # East fire needs western winds (W, NW, SW)
            westerly = set(wind_directions) & {"W", "NW", "SW"}
            if westerly:
                at_risk = True
                matching_winds = list(westerly)
                risk_reasons.append(f"Fire east of Sydney with {', '.join(westerly)} winds forecast")

        elif direction == "southeast":
            # SE fire needs NW winds (or N, W)
            risk_winds = set(wind_directions) & {"NW", "N", "W"}
            if risk_winds:
                at_risk = True
                matching_winds = list(risk_winds)
                risk_reasons.append(f"Fire SE of Sydney with {', '.join(risk_winds)} winds forecast")

        elif direction == "southwest":
            # SW fire needs NE winds (or N, E)
            risk_winds = set(wind_directions) & {"NE", "N", "E"}
            if risk_winds:
                at_risk = True
                matching_winds = list(risk_winds)
                risk_reasons.append(f"Fire SW of Sydney with {', '.join(risk_winds)} winds forecast")

        elif direction == "northeast":
            # NE fire needs SW winds (or S, W)
            risk_winds = set(wind_directions) & {"SW", "S", "W"}
            if risk_winds:
                at_risk = True
                matching_winds = list(risk_winds)
                risk_reasons.append(f"Fire NE of Sydney with {', '.join(risk_winds)} winds forecast")

        elif direction == "northwest":
            # NW fire needs SE winds (or S, E)
            risk_winds = set(wind_directions) & {"SE", "S", "E"}
            if risk_winds:
                at_risk = True
                matching_winds = list(risk_winds)
                risk_reasons.append(f"Fire NW of Sydney with {', '.join(risk_winds)} winds forecast")

        if at_risk:
            # Perform regional AQI validation to confirm smoke is actually being detected
            validation_result = check_regional_aqi_validation(direction, matching_winds)

            # Only add to risk factors if regional validation passes (AQI > 50 in expected region)
            # This ensures we have both: fire reported AND elevated AQI in the outer region
            if validation_result.get("validated"):
                risk_factor = {
                    "burn": burn.to_dict(),
                    "reasons": risk_reasons,
                    "matching_winds": matching_winds,
                    "wind_forecast": relevant_forecasts[:5],  # First 5 forecasts
                    "regional_validation": validation_result
                }
                risk_factors.append(risk_factor)
            else:
                # Log but don't add to risk factors - no notification needed
                logger.info(f"Skipping risk factor for {burn.title}: {validation_result.get('validation_summary', 'Validation failed')}")

    return {
        "at_risk": len(risk_factors) > 0,
        "risk_count": len(risk_factors),
        "risks": risk_factors,
        "checked_at": datetime.now().isoformat(),
        "wind_directions_forecast": wind_directions
    }


def serialize_for_json(obj):
    """Convert datetime objects to ISO format strings for JSON serialization."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    else:
        return obj


def send_pushover_notification(title: str, message: str, priority: int = 0) -> bool:
    """
    Send a notification via Pushover.

    Args:
        title: Notification title
        message: Notification message
        priority: Priority level (0=normal, 1=high, 2=emergency)

    Returns:
        bool: True if notification was sent successfully
    """
    if not PUSHOVER_API_KEY or not PUSHOVER_USER_KEY:
        logger.warning("PUSHOVER_API_KEY or PUSHOVER_USER_KEY not set, skipping Pushover notification")
        return False

    try:
        response = requests.post(
            PUSHOVER_API_URL,
            data={
                "token": PUSHOVER_API_KEY,
                "user": PUSHOVER_USER_KEY,
                "title": title,
                "message": message,
                "priority": priority
            },
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


def send_notification(risk_data: Dict, aqi_risk_data: Dict = None):
    """
    Send notification if air quality risk is detected.

    Notifications are sent when:
    1. Current AQI in North Sydney exceeds threshold (35), OR
    2. A fire is reported AND wind would blow smoke toward Sydney AND regional AQI > 50

    Args:
        risk_data: Forecast risk data from check_air_quality_risk() - requires regional AQI validation
        aqi_risk_data: Current AQI risk data from check_current_aqi_risk()
    """
    forecast_at_risk = risk_data.get("at_risk", False)
    aqi_at_risk = aqi_risk_data.get("at_risk", False) if aqi_risk_data else False

    if not forecast_at_risk and not aqi_at_risk:
        logger.info("No air quality risk detected")
        return

    # Check rate limiting and blackout period before sending
    can_send, reason = can_send_notification()
    if not can_send:
        logger.info(f"Notification skipped: {reason}")
        return

    logger.info(f"Notification allowed: {reason}")

    # Build alert output
    output = {
        "alert": "Air Quality Alert",
        "timestamp": datetime.now().isoformat(),
        "forecast_risk": forecast_at_risk,
        "current_aqi_risk": aqi_at_risk
    }

    # Add forecast risk details
    if forecast_at_risk:
        output["wind_directions"] = risk_data.get("wind_directions_forecast", [])
        output["forecast_risks"] = serialize_for_json(risk_data.get("risks", []))

    # Add current AQI details
    if aqi_at_risk and aqi_risk_data:
        output["current_aqi"] = aqi_risk_data.get("aqi_data", {})
        output["aqi_reason"] = aqi_risk_data.get("reason", "")

    # Write to output file for GitHub Actions
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", ".context")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "air_quality_alert.json")
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    logger.info(f"Alert written to {output_file}")

    # Also print to stdout for GitHub Actions to capture
    print("::warning::Air Quality Alert Detected!")

    if aqi_at_risk and aqi_risk_data:
        aqi_data = aqi_risk_data.get("aqi_data", {})
        print(f"::warning::CURRENT AQI ALERT: {aqi_risk_data.get('reason', '')}")
        print(f"::notice::AQI: {aqi_data.get('aqi', 'N/A')} ({aqi_data.get('aqi_description', 'N/A')})")
        print(f"::notice::PM2.5: {aqi_data.get('pm2_5', 0):.1f} µg/m³")

    if forecast_at_risk:
        print(f"::warning::FORECAST RISK: Smoke from burns may reach Sydney")
        print(f"::notice::Wind directions forecast: {', '.join(risk_data.get('wind_directions_forecast', []))}")

        for risk in risk_data.get("risks", []):
            burn = risk["burn"]
            print(f"::warning::Risk: {burn['title']} ({burn['direction_from_sydney']} of Sydney)")
            for reason in risk["reasons"]:
                print(f"::notice::  - {reason}")

            # Show regional validation results
            if "regional_validation" in risk:
                validation = risk["regional_validation"]
                print(f"::notice::  Regional validation: {validation.get('validation_summary', 'N/A')}")
                if validation.get("max_aqi", 0) > 0:
                    print(f"::notice::    Max AQI in expected region: {validation['max_aqi']} at {validation.get('max_aqi_region', 'Unknown')}")

                # Show individual regional results
                for region_result in validation.get("regional_results", []):
                    region_name = region_result.get("region_name", "Unknown")
                    region_aqi = region_result.get("aqi", "N/A")
                    above = region_result.get("above_threshold", False)
                    status = "⚠️ ABOVE" if above else "OK"
                    print(f"::notice::    {region_name}: AQI={region_aqi} {status}")
            if "validation_note" in risk:
                print(f"::notice::  Note: {risk['validation_note']}")

    # Build and send Pushover notification
    title = "Air Quality Alert - Sydney"
    message_parts = []

    if aqi_at_risk and aqi_risk_data:
        aqi_data = aqi_risk_data.get("aqi_data", {})
        message_parts.append("🚨 CURRENT AIR QUALITY ALERT")
        message_parts.append(aqi_risk_data.get('reason', ''))
        message_parts.append(f"AQI: {aqi_data.get('aqi', 'N/A')} ({aqi_data.get('aqi_description', 'N/A')})")
        message_parts.append(f"PM2.5: {aqi_data.get('pm2_5', 0):.1f} µg/m³")

    if forecast_at_risk:
        message_parts.append("🔥 FORECAST RISK: Smoke from hazard reduction burns may affect Sydney")
        message_parts.append(f"Wind forecast: {', '.join(risk_data.get('wind_directions_forecast', []))}")
        message_parts.append(f"Risks found: {len(risk_data.get('risks', []))}")
        message_parts.append("Details:")
        for risk in risk_data.get("risks", []):
            burn = risk["burn"]
            message_parts.append(f"- {burn['title']} ({burn['direction_from_sydney']} of Sydney)")

            # Add regional validation info to Pushover
            if "regional_validation" in risk:
                validation = risk["regional_validation"]
                if validation.get("validated"):
                    message_parts.append(f"  ✓ Smoke detected: {validation.get('validation_summary', '')}")
                else:
                    message_parts.append(f"  ⏳ Validation pending: {validation.get('validation_summary', '')}")
            if "validation_note" in risk:
                message_parts.append(f"  ⚠️ {risk['validation_note']}")

    if message_parts:
        message = "\n".join(message_parts)
        # Set priority based on alert type
        priority = 2 if aqi_at_risk else 1  # Emergency for current AQI, high for forecast
        if send_pushover_notification(title, message, priority):
            # Only record if notification was actually sent
            record_notification_sent()


def main():
    """Main execution function."""
    logger.info("Starting Air Quality Monitor check...")

    # Check Redis connectivity first - fail fast if unavailable
    if not REDIS_URL:
        error_msg = "REDIS_URL environment variable not set. Redis is required for rate limiting."
        logger.error(error_msg)
        print(f"::error::{error_msg}")
        raise SystemExit(f"Redis configuration error: {error_msg}")

    if not REDIS_AVAILABLE:
        error_msg = "redis package not installed. Install with: pip install redis"
        logger.error(error_msg)
        print(f"::error::{error_msg}")
        raise SystemExit(f"Redis dependency error: {error_msg}")

    redis_client = get_redis_client()
    if redis_client is None:
        error_msg = f"Failed to connect to Redis at {REDIS_URL}. Check that Redis is accessible."
        logger.error(error_msg)
        print(f"::error::{error_msg}")
        raise SystemExit(f"Redis connection error: {error_msg}")

    # Check current AQI in North Sydney
    current_aqi = get_current_aqi()
    aqi_risk_data = check_current_aqi_risk(current_aqi)

    if aqi_risk_data["at_risk"]:
        logger.warning(f"Current AQI risk: {aqi_risk_data['reason']}")
    else:
        logger.info(f"Current AQI OK: {aqi_risk_data['reason']}")

    # Fetch data for forecast risk
    all_burns = []

    # Get burns from multiple sources
    incidents = fetch_nsw_rfs_incidents()
    all_burns.extend([i for i in incidents if i.is_burn])

    burns = fetch_nsw_rfs_burns()
    all_burns.extend(burns)

    # Remove duplicates by GUID
    unique_burns = {b.guid: b for b in all_burns if b.guid}.values()

    logger.info(f"Total unique burns found: {len(unique_burns)}")

    # Get wind forecast
    wind_forecast = get_wind_forecast()

    # Check for forecast risk
    risk_data = check_air_quality_risk(list(unique_burns), wind_forecast)

    if risk_data["at_risk"]:
        logger.warning(f"Forecast risk detected: {risk_data['risk_count']} risks")
    else:
        logger.info("No forecast risk detected")

    # Send notification if needed (either risk type)
    send_notification(risk_data, aqi_risk_data)

    logger.info("Air Quality Monitor check complete")


if __name__ == "__main__":
    main()
