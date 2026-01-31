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

# NSW RFS API endpoints
NSW_RFS_BASE_URL = "https://www.rfs.nsw.gov.au/api/feeds"
NSW_RFS_INCIDENTS_URL = f"{NSW_RFS_BASE_URL}/majorIncidents.json"
NSW_RFS_BURNS_URL = f"{NSW_RFS_BASE_URL}/incidentUpdates.json"

# OpenWeatherMap API
WEATHER_API_BASE = "https://api.openweathermap.org/data/3.0/onecall"
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


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


def send_notification(risk_data: Dict):
    """Send notification if air quality risk is detected."""
    if not risk_data["at_risk"]:
        logger.info("No air quality risk detected")
        return

    # Create GitHub Actions compatible output
    output = {
        "alert": "Air Quality Risk Detected",
        "timestamp": risk_data["checked_at"],
        "wind_directions": risk_data["wind_directions_forecast"],
        "risks": risk_data["risks"]
    }

    # Write to output file for GitHub Actions
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", ".context")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "air_quality_alert.json")
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    logger.info(f"Alert written to {output_file}")

    # Also print to stdout for GitHub Actions to capture
    print("::warning::Air Quality Risk Detected!")
    print(f"::notice::Wind directions forecast: {', '.join(risk_data['wind_directions_forecast'])}")

    for risk in risk_data["risks"]:
        burn = risk["burn"]
        print(f"::warning::Risk: {burn['title']} ({burn['direction_from_sydney']} of Sydney)")
        for reason in risk["reasons"]:
            print(f"::notice::  - {reason}")


def main():
    """Main execution function."""
    logger.info("Starting Air Quality Monitor check...")

    # Fetch data
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

    # Check for risk
    risk_data = check_air_quality_risk(list(unique_burns), wind_forecast)

    # Send notification if needed
    send_notification(risk_data)

    logger.info("Air Quality Monitor check complete")


if __name__ == "__main__":
    main()
