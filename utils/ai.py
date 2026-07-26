"""
ai.py

Groq-powered AI Health Advisor.

Features
--------
✓ Groq (Llama 3.3 70B)
✓ Streamlit caching
✓ Retry mechanism
✓ Graceful fallback
✓ Professional prompt

Author: Ashish Kumar Mishra
"""

from __future__ import annotations

import time
from typing import Dict

import streamlit as st

from utils.config import MODEL_NAME, get_groq_client
from utils.helpers import (
    aqi_description,
    health_risk,
    mask_recommendation,
    outdoor_activity,
    sensitive_group_advice,
)

# ======================================================
# AI HEALTH ADVISOR
# ======================================================


@st.cache_data(ttl=600)
def get_ai_health_advice(
    city: str,
    weather: Dict,
    air_quality: Dict,
    status: str,
) -> str:
    """
    Generate AI-powered health recommendations.
    """

    client = get_groq_client()

    prompt = f"""
You are an environmental health expert.

Analyze the following air quality report and provide practical health advice.

### Current Conditions

City: {city}

AQI: {air_quality["european_aqi"]}

Category: {status}

PM2.5: {air_quality["pm2_5"]} μg/m³

PM10: {air_quality["pm10"]} μg/m³

NO₂: {air_quality["nitrogen_dioxide"]} μg/m³

SO₂: {air_quality["sulphur_dioxide"]} μg/m³

O₃: {air_quality["ozone"]} μg/m³

Temperature: {weather["temperature_2m"]} °C

Humidity: {weather["relative_humidity_2m"]} %

Wind Speed: {weather["wind_speed_10m"]} km/h

---

Respond ONLY in Markdown.

Use EXACTLY these headings:

## 🌤 Air Summary

Two short sentences.

## 🩺 Health Risk

One sentence.

## 😷 Recommended Mask

One sentence.

## 🚶 Outdoor Activities

One sentence.

## 👶 Sensitive Groups

One sentence.

## ✅ Immediate Precautions

• Bullet 1

• Bullet 2

• Bullet 3

Maximum 150 words.

Do NOT mention AI.

Keep the tone friendly, professional and practical.
"""

    for attempt in range(3):

        try:

            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0.3,
                max_tokens=300,
            )

            return completion.choices[0].message.content

        except Exception as e:

            print(f"[Groq Attempt {attempt + 1}] {e}")

            time.sleep(2)

    return fallback_advice(
        air_quality["european_aqi"]
    )


# ======================================================
# FALLBACK ADVICE
# ======================================================


def fallback_advice(aqi: float) -> str:
    """
    Offline health recommendations if Groq is unavailable.
    """

    return f"""
## 🌤 Air Summary

{aqi_description(aqi)}

## 🩺 Health Risk

{health_risk(aqi)}

## 😷 Recommended Mask

{mask_recommendation(aqi)}

## 🚶 Outdoor Activities

{outdoor_activity(aqi)}

## 👶 Sensitive Groups

{sensitive_group_advice(aqi)}

## ✅ Immediate Precautions

- Stay hydrated.
- Monitor local AQI updates.
- Limit prolonged outdoor exposure.
"""