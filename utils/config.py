"""
config.py

Stores application configuration, API endpoints,
model names, and Streamlit secrets.

Author: Ashish Kumar Mishra
"""

import streamlit as st
from groq import Groq

# ==========================================
# API URLs
# ==========================================

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# ==========================================
# Groq Configuration
# ==========================================

MODEL_NAME = "llama-3.3-70b-versatile"

# ==========================================
# Dashboard Configuration
# ==========================================

APP_TITLE = "🌍 Air Quality Intelligence Dashboard"

PAGE_ICON = "🌍"

PAGE_LAYOUT = "wide"

AQI_MAX = 300

CACHE_TIME = 600  # seconds

# ==========================================
# Create Groq Client
# ==========================================

def get_groq_client():
    """
    Returns an authenticated Groq client.
    """

    try:

        api_key = st.secrets["GROQ_API_KEY"]

        return Groq(api_key=api_key)

    except Exception:

        st.error(
            "❌ GROQ_API_KEY not found.\n\n"
            "Please add it inside:\n"
            ".streamlit/secrets.toml"
        )

        st.stop()