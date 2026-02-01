#!/usr/bin/env python3
"""
Air Quality Monitor for NSW, Australia.
Checks planned hazard reduction burns and wind direction to predict poor air quality.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests

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

# NSW RFS API endpoints
NSW_RFS_BASE_URL = "https://www.rfs.nsw.gov.au/api/feeds"
NSW_RFS_INCIDENTS_URL = f"{NSW_RFS_BASE_URL}/majorIncidents.json"
NSW_RFS_BURNS_URL = f"{NSW_RFS_BASE_URL}/incidentUpdates.json"

# OpenWeatherMap API (for wind forecast only)
WEATHER_API_BASE = "https://api.openweathermap.org/data/3.0/onecall"
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# PurpleAir API (for AQI)
PURPLEAIR_API_KEY = os.getenv("PURPLEAIR_API_KEY")
PURPLEAIR_API_BASE = "https://api.purpleair.com/v1"

# North Sydney PurpleAir sensor IDs (you can add more sensors here)
# Find sensors at: https://map.purpleair.com/
NORTH_SYDNEY_SENSORS = [
    # Example sensors - replace with actual North Sydney sensor IDs
    # You can find sensor IDs by looking at the PurpleAir map
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

        # Determine primary direction
        if abs(lat_diff) > abs(lon_diff):
            return "north" if lat_diff > 0 else "south"
        else:
            return "east" if lon_diff > 0 else "west"

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
    logger.info("Fetching NSW RFS incident updates (for burns)...")

    burns = []

    try:
        # Try incident updates RSS feed
        response = requests.get(NSW_RFS_BURNS_URL, timeout=30)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "features" in data:
            for feature in data["features"]:
                props = feature.get("properties", {})
                geometry = feature.get("geometry", {})
                if geometry and "coordinates" in geometry:
                    props["longitude"] = geometry["coordinates"][0]
                    props["latitude"] = geometry["coordinates"][1]
                burn = Burn(props)
                if burn.is_burn:
                    burns.append(burn)
        elif isinstance(data, list):
            for item in data:
                burn = Burn(item)
                if burn.is_burn:
                    burns.append(burn)

        logger.info(f"Found {len(burns)} hazard reduction burns")
        return burns

    except requests.RequestException as e:
        logger.error(f"Error fetching NSW RFS burns: {e}")
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
        # Step 1: Find nearby sensors
        headers = {"X-API-Key": api_key}
        search_params = {
            "nwlat": lat + 0.1,
            "nwlon": lon - 0.1,
            "selat": lat - 0.1,
            "selon": lon + 0.1,
            "fields": "name,pm2.5_atm,latitude,longitude,last_seen",
            "location_type": 0  # Outdoor sensors only
        }

        response = requests.get(
            f"{PURPLEAIR_API_BASE}/sensors",
            headers=headers,
            params=search_params,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        if "data" not in data or len(data["data"]) == 0:
            logger.warning("No PurpleAir sensors found in area")
            return None

        # Step 2: Get readings from all nearby sensors
        sensors = data["data"]
        pm25_readings = []

        for sensor in sensors:
            sensor_id = sensor.get("sensor_index")
            name = sensor.get("name", "Unknown")
            pm25 = sensor.get("pm2.5_atm")
            last_seen = sensor.get("last_seen")

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
                    "latitude": sensor.get("latitude"),
                    "longitude": sensor.get("longitude")
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
    """
    risk_factors = []

    # Get unique wind directions for next 24 hours
    next_24h = datetime.now() + timedelta(hours=24)
    relevant_forecasts = [
        f for f in wind_forecast
        if f["time"] <= next_24h
    ]

    wind_directions = set(f["direction"] for f in relevant_forecasts)

    # Check each burn
    for burn in burns:
        if burn.latitude == 0 and burn.longitude == 0:
            continue

        direction = burn.get_direction_from_sydney()

        # Check if wind will blow smoke toward Sydney
        at_risk = False
        risk_reasons = []

        if direction == "west":
            # West fire needs eastern winds (E, SE, NE)
            easterly = wind_directions & {"E", "SE", "NE"}
            if easterly:
                at_risk = True
                risk_reasons.append(f"Fire west of Sydney with {', '.join(easterly)} winds forecast")

        elif direction == "south":
            # South fire needs northern winds (N, NE, NW)
            northerly = wind_directions & {"N", "NE", "NW"}
            if northerly:
                at_risk = True
                risk_reasons.append(f"Fire south of Sydney with {', '.join(northerly)} winds forecast")

        elif direction == "north":
            # North fire needs southern winds (S, SE, SW)
            southerly = wind_directions & {"S", "SE", "SW"}
            if southerly:
                at_risk = True
                risk_reasons.append(f"Fire north of Sydney with {', '.join(southerly)} winds forecast")

        if at_risk:
            risk_factors.append({
                "burn": burn.to_dict(),
                "reasons": risk_reasons,
                "wind_forecast": relevant_forecasts[:5]  # First 5 forecasts
            })

    return {
        "at_risk": len(risk_factors) > 0,
        "risk_count": len(risk_factors),
        "risks": risk_factors,
        "checked_at": datetime.now().isoformat(),
        "wind_directions_forecast": list(wind_directions)
    }


def send_notification(risk_data: Dict, aqi_risk_data: Dict = None):
    """
    Send notification if air quality risk is detected.

    Args:
        risk_data: Forecast risk data from check_air_quality_risk()
        aqi_risk_data: Current AQI risk data from check_current_aqi_risk()
    """
    forecast_at_risk = risk_data.get("at_risk", False)
    aqi_at_risk = aqi_risk_data.get("at_risk", False) if aqi_risk_data else False

    if not forecast_at_risk and not aqi_at_risk:
        logger.info("No air quality risk detected")
        return

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
        output["forecast_risks"] = risk_data.get("risks", [])

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


def main():
    """Main execution function."""
    logger.info("Starting Air Quality Monitor check...")

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
