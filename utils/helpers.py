"""
helpers.py

Utility functions for AQI interpretation,
health recommendations, colors and UI helpers.

Author: Ashish Kumar Mishra
"""

from typing import Tuple

# =====================================================
# AQI COLOR PALETTE
# =====================================================

AQI_COLORS = {
    "Good": "#00E400",
    "Moderate": "#FFFF00",
    "Unhealthy for Sensitive Groups": "#FF7E00",
    "Unhealthy": "#FF0000",
    "Very Unhealthy": "#8F3F97",
    "Hazardous": "#7E0023"
}


# =====================================================
# AQI CATEGORY
# =====================================================

def get_aqi_status(aqi: float) -> Tuple[str, str]:
    """
    Returns AQI category and corresponding color.

    Parameters
    ----------
    aqi : float

    Returns
    -------
    tuple
        (status, color)
    """

    if aqi <= 50:
        return "Good", AQI_COLORS["Good"]

    elif aqi <= 100:
        return "Moderate", AQI_COLORS["Moderate"]

    elif aqi <= 150:
        return (
            "Unhealthy for Sensitive Groups",
            AQI_COLORS["Unhealthy for Sensitive Groups"],
        )

    elif aqi <= 200:
        return "Unhealthy", AQI_COLORS["Unhealthy"]

    elif aqi <= 300:
        return "Very Unhealthy", AQI_COLORS["Very Unhealthy"]

    return "Hazardous", AQI_COLORS["Hazardous"]


# =====================================================
# HEALTH SCORE
# =====================================================

def calculate_health_score(aqi: float) -> int:
    """
    Converts AQI into a score out of 100.

    Higher score = healthier air.
    """

    score = max(0, round(100 - (aqi / 3)))
    return score


# =====================================================
# MASK RECOMMENDATION
# =====================================================

def mask_recommendation(aqi: float) -> str:
    """
    Return the recommended mask based on AQI.
    """

    if aqi <= 50:
        return "😄 No mask needed."

    elif aqi <= 100:
        return "🙂 Mask optional for sensitive individuals."

    elif aqi <= 150:
        return "😷 Wear an N95 mask if outdoors for long periods."

    elif aqi <= 200:
        return "😷 N95 mask strongly recommended."

    return "🚨 Certified N95/FFP2 mask is highly recommended."


# =====================================================
# OUTDOOR ACTIVITY
# =====================================================

def outdoor_activity(aqi: float) -> str:
    """
    Recommended outdoor exposure duration.
    """

    if aqi <= 50:
        return "🏃 Perfect for outdoor exercise."

    elif aqi <= 100:
        return "🚶 Outdoor activities are generally safe."

    elif aqi <= 150:
        return "⚠ Reduce prolonged outdoor exercise."

    elif aqi <= 200:
        return "❌ Avoid heavy outdoor activities."

    return "🚫 Stay indoors whenever possible."


# =====================================================
# SENSITIVE GROUP ADVICE
# =====================================================

def sensitive_group_advice(aqi: float) -> str:

    if aqi <= 100:
        return (
            "Children, older adults and people with asthma "
            "should monitor symptoms."
        )

    elif aqi <= 150:
        return (
            "Children, pregnant women, elderly people and "
            "asthma patients should reduce outdoor exposure."
        )

    return (
        "Children, elderly people, pregnant women and people "
        "with heart or lung disease should remain indoors."
    )


# =====================================================
# HEALTH RISK
# =====================================================

def health_risk(aqi: float) -> str:

    if aqi <= 50:
        return "🟢 Low"

    elif aqi <= 100:
        return "🟡 Mild"

    elif aqi <= 150:
        return "🟠 Moderate"

    elif aqi <= 200:
        return "🔴 High"

    elif aqi <= 300:
        return "🟣 Very High"

    return "⚫ Extreme"


# =====================================================
# AQI DESCRIPTION
# =====================================================

def aqi_description(aqi: float) -> str:

    if aqi <= 50:
        return (
            "Air quality is excellent with minimal health risk."
        )

    elif aqi <= 100:
        return (
            "Air quality is acceptable, although unusually "
            "sensitive people may notice minor effects."
        )

    elif aqi <= 150:
        return (
            "Sensitive groups may experience health effects."
        )

    elif aqi <= 200:
        return (
            "Everyone may begin to experience adverse effects."
        )

    elif aqi <= 300:
        return (
            "Health alert. Serious health effects are possible."
        )

    return (
        "Emergency conditions. Everyone should avoid outdoor exposure."
    )


# =====================================================
# POLLUTANT SEVERITY
# =====================================================

def pollutant_level(value: float, good: float, moderate: float) -> str:
    """
    Returns a severity label for pollutant values.

    Example
    -------
    pollutant_level(pm25, 15, 35)
    """

    if value <= good:
        return "🟢 Good"

    elif value <= moderate:
        return "🟡 Moderate"

    return "🔴 High"


def dominant_pollutant(air_quality: dict) -> tuple[str, float]:
    """
    Return the pollutant with the highest concentration.
    """

    pollutants = {
        "PM2.5": air_quality["pm2_5"],
        "PM10": air_quality["pm10"],
        "NO₂": air_quality["nitrogen_dioxide"],
        "SO₂": air_quality["sulphur_dioxide"],
        "O₃": air_quality["ozone"],
    }

    pollutant = max(
        pollutants,
        key=pollutants.get,
    )

    return pollutant, pollutants[pollutant]


__all__ = [
    "AQI_COLORS",
    "get_aqi_status",
    "calculate_health_score",
    "mask_recommendation",
    "outdoor_activity",
    "sensitive_group_advice",
    "health_risk",
    "aqi_description",
    "pollutant_level",
]