"""
dashboard.py

Main dashboard for the Air Quality Intelligence application.

Author: Ashish Kumar Mishra
"""

from pathlib import Path

import streamlit as st

from utils.ai import get_ai_health_advice
from utils.api import fetch_city_report
from utils.charts import (
    create_gauge,
    create_health_score,
    create_pollutant_chart,
)
from utils.components import (
    ai_panel,
    footer,
    status_badge,
    weather_card,
)
from utils.helpers import (
    calculate_health_score,
    get_aqi_status,
)
from utils.report import generate_pdf_report


# ==========================================================
# LOAD CSS
# ==========================================================

def load_css() -> None:
    css_file = Path("assets/style.css")

    if css_file.exists():
        with open(css_file, encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )


# ==========================================================
# MAIN DASHBOARD
# ==========================================================

def run_dashboard() -> None:
    load_css()

    st.markdown("""
<div class="hero">

<h1>🌍 Air Quality Intelligence</h1>

<p>
Real-time Air Quality Monitoring • Weather Intelligence • AI Health Advisor
</p>

</div>
""", unsafe_allow_html=True)
    # ------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------

    col1, col2 = st.columns([4, 1])

    with col1:
        city = st.text_input(
            "Enter City",
            value="Lucknow",
            placeholder="Delhi, Mumbai, London...",
        )

    with col2:
        st.write("")
        analyze = st.button(
            "🔍 Analyze",
            use_container_width=True,
            type="primary",
        )

    if not analyze:
        st.info("Enter a city and click Analyze.")
        return

    # ------------------------------------------------------
    # DATA FETCH
    # ------------------------------------------------------

    with st.spinner("🌍 Fetching live air quality and weather data..."):
        report = fetch_city_report(city)

    if report is None:
        st.error("City not found or data could not be fetched.")
        return

    location = report["location"]
    weather = report["weather"]
    air = report["air_quality"]

    if weather is None or air is None:
        st.error("Unable to fetch live data.")
        return

    # ------------------------------------------------------
    # CORE VALUES
    # ------------------------------------------------------

    aqi = air["european_aqi"]
    status, color = get_aqi_status(aqi)
    health_score = calculate_health_score(aqi)

    # ------------------------------------------------------
    # TOP SECTION
    # ------------------------------------------------------

    st.subheader(f"📍 {location['city']}, {location['country']}")
    status_badge(status, color)
    st.divider()

    # ------------------------------------------------------
    # CHARTS
    # ------------------------------------------------------

    left, right = st.columns([1.3, 1])

    with left:
        st.plotly_chart(
            create_gauge(aqi),
            use_container_width=True,
        )

    with right:
        st.plotly_chart(
            create_health_score(health_score),
            use_container_width=True,
        )

    st.divider()

    # ------------------------------------------------------
    # WEATHER
    # ------------------------------------------------------

    weather_card(weather)
    st.divider()

    # ------------------------------------------------------
    # POLLUTANTS
    # ------------------------------------------------------

    st.subheader("🌫 Live Pollutants")

    st.plotly_chart(
        create_pollutant_chart(air),
        use_container_width=True,
    )

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("PM2.5", f"{air['pm2_5']} μg/m³")

    with m2:
        st.metric("PM10", f"{air['pm10']} μg/m³")

    with m3:
        st.metric("NO₂", f"{air['nitrogen_dioxide']} μg/m³")

    m4, m5, m6 = st.columns(3)

    with m4:
        st.metric("SO₂", f"{air['sulphur_dioxide']} μg/m³")

    with m5:
        st.metric("O₃", f"{air['ozone']} μg/m³")

    with m6:
        st.metric("CO", f"{air['carbon_monoxide']} μg/m³")

    st.divider()

    # ------------------------------------------------------
    # AI HEALTH ADVISOR
    # ------------------------------------------------------

    st.subheader("🤖 AI Health Advisor")

    with st.spinner("Generating personalized health advice..."):
        ai_text = get_ai_health_advice(
            city=location["city"],
            weather=weather,
            air_quality=air,
            status=status,
        )

    ai_panel(ai_text)

    st.divider()

    # ------------------------------------------------------
    # DOWNLOAD REPORT
    # ------------------------------------------------------

    pdf = generate_pdf_report(
        city=location["city"],
        location=location,
        weather=weather,
        air_quality=air,
        status=status,
        health_score=health_score,
        ai_advice=ai_text,
    )

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf,
        file_name=f"{location['city']}_AQI_Report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    st.divider()

    # ------------------------------------------------------
    # LOCATION INFORMATION
    # ------------------------------------------------------

    st.subheader("📍 Location")

    info1, info2, info3 = st.columns(3)

    with info1:
        st.metric("City", location["city"])

    with info2:
        st.metric("State", location["state"] or "-")

    with info3:
        st.metric("Country", location["country"])

    footer()