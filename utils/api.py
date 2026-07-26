"""
api.py

Handles all communication with the Open-Meteo APIs.

Features
--------
✓ City Geocoding
✓ Live Air Quality
✓ Current Weather
✓ Streamlit Caching
✓ Request Timeout
✓ Error Handling

Author: Ashish Kumar Mishra
"""

from typing import Optional

import requests
import streamlit as st

from utils.config import (
    AIR_QUALITY_URL,
    CACHE_TIME,
    GEOCODING_URL,
)

# ======================================================
# CONSTANTS
# ======================================================

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

REQUEST_TIMEOUT = 10


# ======================================================
# CITY → LATITUDE & LONGITUDE
# ======================================================

@st.cache_data(ttl=CACHE_TIME)
def get_coordinates(city: str) -> Optional[dict]:
    """
    Fetch latitude and longitude for a city.

    Returns
    -------
    dict | None
    """

    try:

        response = requests.get(
            GEOCODING_URL,
            params={
                "name": city.strip(),
                "count": 1,
            },
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        results = response.json().get("results")

        if not results:
            return None

        place = results[0]

        return {
            "city": place.get("name"),
            "country": place.get("country"),
            "state": place.get("admin1", ""),
            "latitude": place.get("latitude"),
            "longitude": place.get("longitude"),
        }

    except requests.RequestException as e:

        print(f"[Geocoding Error] {e}")

        return None


# ======================================================
# LIVE AIR QUALITY
# ======================================================

@st.cache_data(ttl=CACHE_TIME)
def get_air_quality(latitude: float, longitude: float) -> Optional[dict]:
    """
    Fetch current air quality.
    """

    try:

        response = requests.get(
            AIR_QUALITY_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": ",".join(
                    [
                        "european_aqi",
                        "pm10",
                        "pm2_5",
                        "carbon_monoxide",
                        "nitrogen_dioxide",
                        "ozone",
                        "sulphur_dioxide",
                    ]
                ),
            },
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json().get("current")

    except requests.RequestException as e:

        print(f"[AQI Error] {e}")

        return None


# ======================================================
# CURRENT WEATHER
# ======================================================

@st.cache_data(ttl=CACHE_TIME)
def get_weather(latitude: float, longitude: float) -> Optional[dict]:
    """
    Fetch current weather.
    """

    try:

        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": ",".join(
                    [
                        "temperature_2m",
                        "relative_humidity_2m",
                        "wind_speed_10m",
                        "weather_code",
                    ]
                ),
            },
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json().get("current")

    except requests.RequestException as e:

        print(f"[Weather Error] {e}")

        return None


# ======================================================
# COMPLETE CITY REPORT
# ======================================================

@st.cache_data(ttl=CACHE_TIME)
def fetch_city_report(city: str) -> Optional[dict]:
    """
    Fetch all dashboard data for a city.

    Returns
    -------
    {
        "location": ...,
        "air_quality": ...,
        "weather": ...
    }
    """

    location = get_coordinates(city)

    if location is None:
        return None

    latitude = location["latitude"]
    longitude = location["longitude"]

    air_quality = get_air_quality(latitude, longitude)
    weather = get_weather(latitude, longitude)

    if air_quality is None or weather is None:
        return None

    return {
        "location": location,
        "air_quality": air_quality,
        "weather": weather,
    }